from manim import *


class ParallelLinesScene(Scene):
    def construct(self):
        line_spacing = 1.5
        number_of_lines = 5
        line_length = 12
        line_color = BLUE
        title_font_size = 36

        lines = VGroup()

        half_line_length = line_length / 2
        center_offset = (number_of_lines - 1) / 2

        for line_index in range(number_of_lines):
            y = (line_index - center_offset) * line_spacing

            vertical_shift = UP * y
            start_point = LEFT * half_line_length + vertical_shift
            end_point = RIGHT * half_line_length + vertical_shift

            line = Line(
                start=start_point,
                end=end_point,
                color=line_color,
            )

            lines.add(line)

        title = Text("Buffon's needle experiment", font_size=title_font_size)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(Create(lines))
        self.wait(2)