from manim import *
import random


# class FlickerFx(Scene):
#     def construct(self):
#         function = ImplicitFunction(
#             lambda x, y: x**2 + y**2 - 1, color=WHITE, stroke_opacity=1
#         )

#         # I want an effect like On/off-on/off....'n' times
#         def flickerreturn(t, n):
#             return int((2 * n) * t) % 2

#         self.add(function)
#         self.play(
#             function.animate(
#                 rate_func=lambda t: flickerreturn(t, 5), run_time=5
#             ).set_stroke(opacity=0)
#         )
#         self.wait()


class FlickeringLight(Scene):
    def construct(self):
        # Create a light source (circle)
        light = Circle(radius=0.5, color=YELLOW, fill_opacity=1).move_to(ORIGIN)
        self.add(light)

        # Flickering effect
        flicker_durations = [
            0.1,
            0.2,
            0.2,
            0.3,
            0.05,
            0.1,
            0.05,
            0.15,
            0.1,
        ]  # Example flicker durations
        flicker_opacities = [
            1,
            0.5,
            0.2,
            0.8,
            0.5,
            0.2,
            0.3,
            1,
            0.2,
            0.3,
        ]  # Example opacities to flicker through

        # Define the flickering animation
        for i in range(len(flicker_opacities)):
            self.play(
                light.animate.set_fill(opacity=flicker_opacities[i]),
                run_time=flicker_durations[i % len(flicker_durations)],
            )

        # Pause at the end
        self.wait(1)


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


if __name__ == "__main__":
    scene = FlickerOut()
    scene.render()
