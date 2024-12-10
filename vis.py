from manim import *
from typing import Tuple, Optional
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

        self.add(self.line, self.weight_label)

    def traverse(self) -> Animation:
        temp_copy = self.copy()
        temp_copy.set_stroke(color=YELLOW)
        return ShowPassingFlash(temp_copy, time_width=1, run_time=2)

    def select(self) -> Animation:
        self.selected_overlay = self.copy()
        self.selected_overlay.set_stroke(color=RED)
        return Create(self.selected_overlay, run_time=2)

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
        self.label = Text(name, font="Arial", color=RED).scale(0.5)
        self.out_edges: List["Edge"] = []

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

    def select(self) -> Animation:
        self.circle.set_stroke_color(RED)
        return Flash(self, color=RED, flash_radius=0.5)


class Graph:
    def __init__(self, src: List["Node"]):
        self.vertices: List["Node"] = []
        self.add_vertices(src)

    def add_vertices(self, vertices):
        self.vertices.extend(vertices)


class Dijkstra(Scene):
    def construct(self):

        graph_src = [
            Node("A", radius=0.3, pos=(-3, -2)),
            Node("B", radius=0.3, pos=(3, -3.5)),
            Node("C", radius=0.3, pos=(0, 0)),
            Node("D", radius=0.3, pos=(3, 3)),
            Node("E", radius=0.3, pos=(-3, 3)),
            Node("F", radius=0.3, pos=(5, -2)),
            Node("G", radius=0.3, pos=(4, 3)),
            Node("H", radius=0.3, pos=(6, 0)),
        ]

        graph1 = Graph(graph_src)
        self.add(*graph1.vertices)

        self.play(
            graph_src[0].connect_bulk(
                out_neighbours=[graph_src[1], graph_src[2]], weights=[1, 3]
            ),
            graph_src[1].connect_bulk(out_neighbours=[graph_src[2]], weights=[1]),
        )
        self.play(
            graph_src[0].select(),
            *[out_edge.select() for out_edge in graph_src[0].out_edges],
        )
        self.wait()
        self.play(graph_src[0].out_edges[0].traverse())
        self.wait()


if __name__ == "__main__":
    scene = Dijkstra()
    scene.render()
