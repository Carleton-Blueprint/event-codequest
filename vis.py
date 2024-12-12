from manim import *
from typing import Tuple, Optional
import math
import logging
import random

# Create a logger
logger = logging.getLogger("manim_logger")
logger.setLevel(logging.DEBUG)  # Set the logger level

# Create a file handler with overwrite mode
file_handler = logging.FileHandler(
    "manim.log", mode="w"
)  # Use mode='w' to overwrite the log file
file_handler.setLevel(logging.DEBUG)  # Set the logging level for the handler

# Define a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)  # Assign the formatter to the handler

# Add the file handler to the logger
logger.addHandler(file_handler)


class FlickerOut(Animation):
    def __init__(self, mobject: Mobject, remover=True, **kwargs):
        self.period_checkpoint = random.uniform(0.1, 0.3)
        self.flipflop = True
        super().__init__(mobject, remover=remover, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        actual_alpha = self.rate_func(alpha)

        if actual_alpha > self.period_checkpoint:
            self.flipflop = not self.flipflop
            self.period_checkpoint += random.uniform(0.1, 0.3)

        self.mobject.set_opacity((min(actual_alpha * 1.5, 1)) if self.flipflop else 0)


class Edge(VMobject):
    def __init__(self, weight: int, src_node: "Node", dest_node: "Node", **kwargs):
        super().__init__(**kwargs)

        self.weight = weight
        self.src_node = src_node
        self.dest_node = dest_node
        self.line = Line(
            src_node.get_center(),
            dest_node.get_center(),
        )
        self.weight_label = Text(
            str(weight),
            font="Arial",
            color=WHITE,
        ).scale(0.5)
        self.weight_label.move_to(self.line.get_center() + 0.3 * UP)
        self.visited_overlay = None

        self.add(self.line, self.weight_label)

    def traverse(self) -> AnimationGroup:
        temp_copy = self.copy()
        temp_copy.set_stroke(color=YELLOW)
        # temp_node_copy = self.dest_node.copy()
        # temp_node_copy.set_stroke(color=YELLOW)
        return AnimationGroup(
            ShowPassingFlash(temp_copy, time_width=1, run_time=1),
            # ShowPassingFlash(temp_node_copy, time_width=1, run_time=1),
        )

    def visit(self) -> Animation:
        self.visited_overlay = self.copy()
        self.visited_overlay.set_stroke(color=RED)
        return Create(self.visited_overlay, run_time=2)

    def deselect(self) -> Animation:
        return FlickerOut(self.copy, run_time=2)


class Node(VMobject):
    def __init__(
        self,
        name: str,
        radius: float,
        pos: Tuple[float, float],
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.circle = Circle(
            radius=radius,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=BLUE,
        )
        self.label = MathTex(r"\infty").scale(0.5)
        # self.label = MathTex(name).scale(0.5)
        self.cost = math.inf
        self.out_edges: List["Edge"] = []
        self.is_visited = False

        self.add(self.circle, self.label)
        self.move_to([*pos, 0])
        self.z_index = 1

    def connect_bulk(
        self, out_neighbours: List["Node"], weights: List[int]
    ) -> Animation:
        for node, weight in zip(out_neighbours, weights):
            self.out_edges.append(Edge(weight, self, node))

        return LaggedStart(
            *[Create(edge) for edge in self.out_edges], run_time=1, lag_ratio=0.25
        )

    def visit(self) -> AnimationGroup:
        self.circle.set_stroke_color(RED)
        self.is_visited = True
        return AnimationGroup(
            FadeOut(
                Text("Selected", color=YELLOW)
                .scale(0.5)
                .move_to(self.get_center() + 0.5 * UP)
            ),
            Flash(self, color=RED, flash_radius=0.5),
        )

    def update_cost(self, cost: int) -> AnimationGroup:
        if cost < self.cost:
            self.cost = cost
            self.label.become(
                MathTex(r"\infty" if math.isinf(cost) else cost)
                # MathTex(self.name if math.isinf(cost) else cost)
                .scale(0.5).move_to(self.get_center())
            )

            temp_copy = self.circle.copy()
            temp_copy.set_stroke(YELLOW)
            temp_copy.set_z_index(3)

            return AnimationGroup(
                ShowPassingFlash(temp_copy, time_width=1),
                FadeOut(
                    Text("Cost Reduced", color=YELLOW)
                    .scale(0.5)
                    .move_to(self.get_center() + 0.5 * UP)
                ),
            )
        return FadeOut(
            Text("No Change", color=WHITE)
            .scale(0.5)
            .move_to(self.get_center() + 0.5 * UP)
        )


class Main(Scene):
    def construct(self):
        # num_plane = NumberPlane().add_coordinates()
        # self.add(num_plane)

        graph_src = [
            Node("A", radius=0.3, pos=(-2, -3)),
            Node("B", radius=0.3, pos=(-5, 2)),
            Node("C", radius=0.3, pos=(0, 0)),
            Node("D", radius=0.3, pos=(1, 2)),
            Node("E", radius=0.3, pos=(2, -1)),
            Node("F", radius=0.3, pos=(4, 2)),
            Node("G", radius=0.3, pos=(6, -3)),
            Node("H", radius=0.3, pos=(4, 0)),
        ]
        self.add(*graph_src)

        self.play(
            graph_src[0].connect_bulk(
                out_neighbours=[graph_src[1], graph_src[2], graph_src[6]],
                weights=[1, 3, 6],
            ),
            graph_src[1].connect_bulk(
                out_neighbours=[graph_src[2], graph_src[5]],
                weights=[4, 8],
            ),
            graph_src[2].connect_bulk(out_neighbours=[graph_src[3]], weights=[1]),
            graph_src[3].connect_bulk(out_neighbours=[graph_src[4]], weights=[9]),
            graph_src[4].connect_bulk(out_neighbours=[graph_src[5]], weights=[2]),
            graph_src[5].connect_bulk(out_neighbours=[graph_src[6]], weights=[5]),
            graph_src[6].connect_bulk(out_neighbours=[graph_src[7]], weights=[7]),
            graph_src[7].connect_bulk(out_neighbours=[graph_src[4]], weights=[2]),
        )

        starting_vertex = graph_src[0]

        self.play(starting_vertex.update_cost(0))
        self.wait(0.5)
        self.play(
            starting_vertex.visit(),
            *[out_edge.visit() for out_edge in graph_src[0].out_edges],
        )

        edges = []
        for node in graph_src:
            edges.extend(node.out_edges)

        min_dest_edge = None
        min_dest_weight = math.inf

        for edge in edges:
            if edge.src_node.is_visited ^ edge.dest_node.is_visited:
                if not edge.src_node.is_visited:
                    new_cost = edge.dest_node.cost + edge.weight
                    self.play(edge.traverse(), edge.src_node.update_cost(new_cost))
                    if new_cost < min_dest_weight:
                        min_dest_weight = new_cost
                        min_dest_edge = edge
                elif not edge.dest_node.is_visited:
                    new_cost = edge.src_node.cost + edge.weight
                    self.play(edge.traverse(), edge.dest_node.update_cost(new_cost))
                    if new_cost < min_dest_weight:
                        min_dest_weight = new_cost
                        min_dest_edge = edge

        if min_dest_edge.src_node.is_visited:
            min_dest_edge.dest_node.visit()
        else:
            min_dest_edge.src_node.visit()

    # node_of_interest = graph_src[0]
    # for edge in node_of_interest.out_edges:
    #     self.play(edge.traverse())
    #     self.play(edge.dest_node.update_cost(1))
    # self.wait()


if __name__ == "__main__":
    scene = Main()
    scene.render()
