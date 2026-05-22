from manim import *


class ParallelLinesScene(Scene):
    def construct(self):
        # Distance between neighboring horizontal lines
        d = 1.5

        # Create a group for all parallel lines
        lines = VGroup()

        # y-coordinates of the horizontal lines
        y_values = [-3, -1.5, 0, 1.5, 3]

        for y in y_values:
            line = Line(
                start=LEFT * 6 + UP * y,
                end=RIGHT * 6 + UP * y,
                color=BLUE,
            )
            lines.add(line)

        title = Text("Buffon's needle experiment", font_size=36)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(Create(lines))
        self.wait(2)