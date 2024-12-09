from manim import *
import random


class FlickerOut(Scene):
    def construct(self):
        values = []

        start = 300
        curr_val = start

        while curr_val > 10:
            values.append(curr_val)
            curr_val = round(
                curr_val * random.uniform(0.5, 0.9)
            )  # might use perlin noise here

        # Create a light source (circle)
        light = Circle(radius=0.5, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        self.add(light)

        for value in values:
            # light.set_fill(opacity=random.uniform(0.1, 1))
            light.set_fill(opacity=1)
            self.wait(duration=random.uniform(0.01, 0.1))
            light.set_fill(opacity=0)
            self.wait(duration=value / 1000)

        print(values)


class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        circle.set_fill(RED, opacity=1)
        self.wait()


if __name__ == "__main__":
    scene = FlickerOut()
    scene.render()
