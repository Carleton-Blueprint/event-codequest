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
        # self.original = mobject.copy()  # TODO: is this really necessary?
        self.period_checkpoint = random.uniform(0.1, 0.3)
        self.flipflop = True
        super().__init__(mobject, remover=remover, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        actual_alpha = self.rate_func(alpha)

        if actual_alpha > self.period_checkpoint:
            self.flipflop = not self.flipflop
            self.period_checkpoint += random.uniform(0.1, 0.3)

        self.mobject.set_opacity((min(actual_alpha * 1.5, 1)) if self.flipflop else 0)


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
            z_index=5,
        )
        self.circle.move_to([*pos, 0])

        self.label = Text(name, font="Arial", color=WHITE, z_index=999).scale(0.5)
        self.label.move_to(self.circle.get_center())

        self.next: List["Node"] = []

        # self.add(self.label, self.circle)
        self.add(self.circle)
        self.add(self.label)

    def create(self) -> Animation:
        return Create(self)

    def connect_bulk(
        self, out_neighbours: List["Node"], weights: List[int]
    ) -> Animation:
        out_edges = []
        for node, weight in zip(out_neighbours, weights):
            if node not in self.next:
                self.next.append(node)

                weighted_line = VGroup()  # TODO: Change this to a custom VMobject
                weighted_line.add(
                    Line(
                        self.get_center(),
                        node.get_center(),
                        z_index=0,
                    )
                )

                weight_label = Text(
                    str(weight),
                    font="Arial",
                    color=WHITE,
                    z_index=0,
                ).scale(0.5)
                weight_label.move_to(weighted_line.get_center() + 0.3 * UP)
                weighted_line.add(weight_label)

                out_edges.append(weighted_line)

        return LaggedStart(
            *[Create(edge) for edge in out_edges], run_time=1, lag_ratio=0.25
        )

    def select(self) -> Animation:
        self.circle.set_stroke_color(YELLOW)
        return Flash(self, flash_radius=0.5)


class Graph:
    def __init__(self, src: List[Node]):
        self.vertices: List[Node] = []
        self.add_vertices(src)

    def add_vertices(self, vertices):
        self.vertices.extend(vertices)

    def create_vertices(self) -> AnimationGroup:
        animations = []
        for vertex in self.vertices:
            animations.append(vertex.create())
        return AnimationGroup(*animations)


class Dijkstra(Scene):
    def construct(self):

        node_a = Node("A", radius=0.3, pos=(-3, -2))
        node_b = Node("B", radius=0.3, pos=(3, -3.5))
        node_c = Node("C", radius=0.3, pos=(0, 0))

        graph_src = [
            node_a,
            node_b,
            node_c,
        ]

        graph1 = Graph(graph_src)

        self.play(graph1.create_vertices())

        self.play(
            node_a.connect_bulk(out_neighbours=[node_b, node_c], weights=[1, 3]),
            node_b.connect_bulk(out_neighbours=[node_c], weights=[1]),
        )
        self.play(node_a.select())

        self.play(*[FlickerOut(node) for node in graph1.vertices])

        self.wait(duration=2)


if __name__ == "__main__":
    scene = Dijkstra()
    scene.render()

    # open_media_file(scene.renderer.file_writer.movie_file_path)

    # values = []

    # start = 500
    # curr_val = start

    # while curr_val > 100:
    #     values.append(curr_val)
    #     curr_val = round(
    #         curr_val * random.uniform(0.8, 1)
    #     )  # might use perlin noise here

    # print(values)
