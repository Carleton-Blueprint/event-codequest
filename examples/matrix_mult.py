from manim import *
import random


class Node:
    def __init__(self, items: List[str], left: "Node", right: "Node"):
        self.items = items
        self.left = left
        self.right = right

    def split_recurse(self) -> List[str]:
        n = len(self.items)

        if n == 1:
            return [self.items[0]]

        if n == 2:
            return ["(", self.items[0], self.items[1], ")"]

        rand_split = random.randint(1, n - 1)

        self.left = Node(self.items[:rand_split], None, None)
        self.right = Node(self.items[rand_split:], None, None)

        return ["(", *self.left.split_recurse(), *self.right.split_recurse(), ")"]


class Main(Scene):
    def null_construct(self):
        txt = MathTex(r"(", r"A \times B", r")", r"\times C")
        self.add(txt)
        self.wait(1)

        self.play(
            TransformMatchingTex(txt, MathTex(r"(", r"A \times B", r"\times C", r")"))
        )

    def construct(self):
        # Show random possible combinations
        root = Node(["A", "B", "C", "D", "E", "F", "G"], None, None)
        prev = MathTex(*root.split_recurse())
        for _ in range(5):
            new = MathTex(*root.split_recurse())
            self.play(TransformMatchingTex(prev, new, run_time=0.2))
            self.wait(0.5)
            prev = new

        # Factor out A (in front)
        without_a = Node(["B", "C", "D", "E", "F", "G"], None, None).split_recurse()
        new = MathTex("(", "A", *without_a, ")")
        self.play(TransformMatchingTex(prev, new, run_time=0.5))

        # Change substring partitioning using {{ }}
        old = new
        new = MathTex(rf"((A) {{{{ {''.join(without_a)} }}}} )")
        # # new.become(MathTex(r"(A {{" + "".join(without_a) + r"}} )"))
        self.play(TransformMatchingTex(old, new, run_time=0.001))
        self.wait(1)
        # # Text that goes `cost: ??`, or a constantly changing cost number (to demonstrate indeterminateness)

        # Truncate B...G
        # Note: We probably don't want to truncate this.. instead keep it in variable "superposition" form
        old = new
        new = (
            MathTex(r"( {{(A)}} {{(B \cdots G)}} )")
            .set_color_by_tex("(A)", BLUE)
            .set_color_by_tex("cdots", RED)
        )
        # for exp in another_new:
        #     self.add(index_labels(exp))
        self.play(TransformMatchingTex(old, new))
        self.wait(1)

        #
        # self.play(new.animate.move_to(UL))
        # new = MathTex(r"((AB) {{(C \cdots G)}} )", color=BLUE).set_color_by_tex(
        #     "cdots", RED
        # )
        # self.add(new)
        # self.wait(1)


if __name__ == "__main__":
    scene = Main()
    scene.render()
