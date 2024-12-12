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
    def __init__(self, weight: int, nodes: Tuple["Node"], **kwargs):
        """
        nodes: Tuple of two nodes that the edge connects.
        """

        super().__init__(**kwargs)

        self.weight = weight
        self.nodes = nodes
        self.line = Line(
            nodes[0].get_center(),
            nodes[1].get_center(),
        )
        self.weight_label = Text(
            str(weight),
            font="Arial",
            color=WHITE,
        ).scale(0.5)
        self.weight_label.move_to(self.line.get_center() + 0.3 * UP)
        self.visited_overlay = None

        self.add(self.line, self.weight_label)

    def get_other_node(self, node: "Node") -> "Node":
        """
        Get the other node that the edge connects to.
        """

        if node not in self.nodes:
            raise ValueError("Node must be part of the edge.nodes Tuple.")

        return self.nodes[0] if node == self.nodes[1] else self.nodes[1]

    def get_reachable_unexplored_node(self) -> Optional["Node"]:
        """
        Check if the edge has a reachable unexplored node.
        Returns the unexplored node if it exists, else None.
        The condition is an XOR between the two nodes' is_visited attributes.
        """

        if not self.nodes[0].is_visited ^ self.nodes[1].is_visited:
            return None

        return self.nodes[0] if not self.nodes[0].is_visited else self.nodes[1]

    def traverse(
        self,
        src_node: Optional["Node"] = None,
        dest_node: Optional["Node"] = None,
        color: Optional[ParsableManimColor] = YELLOW,
    ) -> AnimationGroup:
        """
        Traverse the edge. This animation is ephemeral and does not change the state of the edge.
        Specify src_node to indicate which node the traversal is coming from.
        Specify dest_node to indicate which node the traversal is going to.
        Both of these nodes must be in the edge, and only one of them can be specified at a time.
        """
        if not src_node and not dest_node:
            raise ValueError(
                "At least one of src_node and dest_node must be specified."
            )

        if src_node and src_node not in self.nodes:
            raise ValueError("`src_node` must be part of the edge.nodes Tuple.")

        if dest_node and dest_node not in self.nodes:
            raise ValueError("`dest_node` must be part of the edge.nodes Tuple.")

        if src_node and dest_node:
            raise ValueError("Only one of src_node and dest_node can be specified.")

        other_node = self.get_other_node(src_node or dest_node)

        if src_node:
            temp_line = Line(src_node.get_center(), other_node.get_center())
        elif dest_node:
            temp_line = Line(other_node.get_center(), dest_node.get_center())
        else:
            raise ValueError("Internal server error!")

        temp_line.set_stroke(color=color)
        return AnimationGroup(
            ShowPassingFlash(temp_line, time_width=1, run_time=1),
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
        self.name = name
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
        """
        Connect the node to multiple out neighbours with the specified weights.
        The term "out neighbours" here seems to be a misnomer, as the edges are undirected.
        """

        for node, weight in zip(out_neighbours, weights):
            self.out_edges.append(Edge(weight=weight, nodes=(self, node)))

        return LaggedStart(
            *[Create(edge) for edge in self.out_edges], run_time=1, lag_ratio=0.25
        )

    def visit(self) -> AnimationGroup:
        self.circle.set_stroke_color(RED)
        self.is_visited = True
        return AnimationGroup(
            FadeOut(
                Text("Selected", color=WHITE)
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

        edges: List["Edge"] = []
        for node in graph_src:
            edges.extend(node.out_edges)

        min_dest_edge = None
        min_dest_weight = math.inf

        for edge in edges:
            reachable_unexplored_node = edge.get_reachable_unexplored_node()
            if reachable_unexplored_node:
                src_node = edge.get_other_node(reachable_unexplored_node)
                new_cost = src_node.cost + edge.weight
                self.play(
                    edge.traverse(dest_node=reachable_unexplored_node),
                    reachable_unexplored_node.update_cost(new_cost),
                )
                if new_cost < min_dest_weight:
                    min_dest_weight = new_cost
                    min_dest_edge = edge

        self.wait()
        new_node_to_visit = min_dest_edge.get_reachable_unexplored_node()
        self.play(
            new_node_to_visit.visit(),
            min_dest_edge.traverse(dest_node=new_node_to_visit, color=WHITE),
        )


if __name__ == "__main__":
    scene = Main()
    scene.render()
