from manim import *
from typing import Tuple, Optional
import logging

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


class Node:
    def __init__(
        self,
        name: str,
        radius: float,
        color: ParsableManimColor,
        opacity: float,
        pos: Tuple[float, float],
        scene: Scene,
    ):
        self.mobj = VGroup(z_index=5)
        self.mobj.add(
            Circle(radius=radius, color=color, fill_opacity=opacity, stroke_color=BLUE)
        )
        self.mobj.add(Text(name, font="Arial", color=BLACK).scale(0.5))
        self.mobj.move_to([*pos, 0])
        self.next = []
        self.scene = scene

    def connect_bulk(
        self, out_neighbours: List["Node"], weights: List[int]
    ) -> LaggedStart:
        out_edges = []
        for node, weight in zip(out_neighbours, weights):
            if node not in self.next:
                self.next.append(node)

                weighted_line = VGroup()
                weighted_line.add(
                    Line(
                        self.mobj.get_center(),
                        node.mobj.get_center(),
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

    def select(self) -> Flash:
        self.mobj[0].set_fill(YELLOW)
        return Flash(self.mobj, flash_radius=0.5)


class Graph:
    def __init__(self, scene: Scene, src: List[Node]):
        self.scene = scene
        self.vertices: List[Node] = []
        self.add_vertices(src)

    def add_vertices(self, vertices):
        for vertex in vertices:
            self.vertices.append(vertex)

    def create_vertices(self):
        animations = []
        for vertex in self.vertices:
            animations.append(Create(vertex.mobj))
        self.scene.play(*animations)


class Dijkstra(Scene):
    def construct(self):

        node_a = Node("A", radius=0.3, color=WHITE, opacity=1, pos=(-3, -2), scene=self)
        node_b = Node(
            "B", radius=0.3, color=WHITE, opacity=1, pos=(3, -3.5), scene=self
        )
        node_c = Node("C", radius=0.3, color=WHITE, opacity=1, pos=(0, 0), scene=self)

        graph_src = [
            node_a,
            node_b,
            node_c,
        ]

        graph1 = Graph(self, graph_src)
        graph1.create_vertices()

        self.play(
            node_a.connect_bulk(out_neighbours=[node_b, node_c], weights=[1, 3]),
            node_b.connect_bulk(out_neighbours=[node_c], weights=[1]),
        )
        self.play(node_a.select())


if __name__ == "__main__":
    # scene = Dijkstra()
    # scene.render()

    # open_media_file(scene.renderer.file_writer.movie_file_path)

    values = []

    start = 500
    curr_val = start

    while curr_val > 100:
        values.append(curr_val)
        curr_val = round(
            curr_val * random.uniform(0.8, 1)
        )  # might use perlin noise here

    print(values)
