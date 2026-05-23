from manim import *


class ParallelLinesScene(Scene):
    def construct(self):
        d = 1.5
        line_count = 5
        line_len = 12
        line_color = BLUE

        needle_ratio = 2 / 3
        needle_len = needle_ratio * d
        needle_mid = RIGHT + DOWN * 0.1
        needle_angle = PI / 6
        needle_color = YELLOW
        needle_width = 4

        title_size = 36

        lines = VGroup()

        half_line_len = line_len / 2
        center_offset = (line_count - 1) / 2

        for i in range(line_count):
            line_y = (i - center_offset) * d
            line_shift = UP * line_y

            line = Line(
                start=LEFT * half_line_len + line_shift,
                end=RIGHT * half_line_len + line_shift,
                color=line_color,
            )

            lines.add(line)

        needle = Line(
            start=LEFT * (needle_len / 2),
            end=RIGHT * (needle_len / 2),
            color=needle_color,
            stroke_width=needle_width,
        )

        needle.rotate(needle_angle)
        needle.move_to(needle_mid)

        title = Text(
            "Buffon's needle experiment",
            font_size=title_size,
        )
        title.to_edge(UP)

        self.play(Write(title))
        self.play(Create(lines))
        self.play(FadeIn(needle, shift=DOWN * 0.3))
        self.wait(2)
