from manim import *
import random


class FlickerOut(Animation):
    def __init__(self, mobject: Mobject, remover=True, **kwargs):
        self.original = mobject.copy()  # TODO: is this really necessary?

        values = []
        start = 300  # ms
        curr_val = start
        while curr_val > 10:
            values.append(curr_val)
            curr_val = round(
                curr_val * random.uniform(0.5, 0.9)
            )  # might use perlin noise here

        anims: List[Animation] = []
        for value in values:
            anims.append(mobject.animate.set_fill(opacity=1))
            anims.append(Wait(run_time=random.uniform(0.01, 0.1)))
            anims.append(mobject.animate.set_fill(opacity=0))
            anims.append(Wait(duration=value / 1000))

        super().__init__(Succession(*anims), remover=remover, **kwargs)


class FlickerOutTest(Scene):
    def construct(self):
        values = []
        start = 300  # ms
        curr_val = start
        while curr_val > 10:
            values.append(curr_val)
            curr_val = round(
                curr_val * random.uniform(0.5, 0.9)
            )  # might use perlin noise here

        anims: List[Animation] = []
        for value in values:
            anims.append(mobject.animate.set_fill(opacity=1))
            anims.append(Wait(run_time=random.uniform(0.01, 0.1)))
            anims.append(mobject.animate.set_fill(opacity=0))
            anims.append(Wait(duration=value / 1000))


class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        circle.set_fill(RED, opacity=1)
        self.wait()


if __name__ == "__main__":
    scene = FlickerOut()
    scene.render()
