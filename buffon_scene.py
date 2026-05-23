from manim import *
import math


class BuffonNeedleExperimentScene(Scene):
    def construct(self):
        # Scene parameters
        d = 1.5
        line_count = 5
        line_len = 12
        line_color = BLUE
        title_size = 36

        # Needle parameters
        needle_ratio = 2 / 3
        needle_len = needle_ratio * d
        crossing_color = GREEN
        non_crossing_color = RED
        needle_width = 4
        needle_outline_color = GRAY
        needle_outline_width = 10

        # Visual parameters
        intersection_color = YELLOW
        slow_drop_time = 0.9
        fast_drop_time = 0.25
        label_fade_time = 0.45
        label_hold_time = 0.9
        point_fade_time = 0.5
        point_hold_time = 1.0

        # First two needles are ordered for explanation:
        # 1) no crossing, 2) crossing
        needle_data = [
            (LEFT * 4.4 + UP * 2.25, PI / 9),
            (LEFT * 2.6 + UP * 1.45, PI / 2.8),
            (RIGHT * 0.2 + UP * 0.75, PI / 7),
            (RIGHT * 3.8 + UP * 0.35, PI / 2.8),
            (RIGHT * 2.5 + DOWN * 0.95, PI / 10),
            (RIGHT * 4.7 + DOWN * 1.95, PI / 2.6),
            (LEFT * 3.6 + DOWN * 0.55, PI / 4.5),
            (RIGHT * 1.8 + DOWN * 2.25, PI / 8),
            (LEFT * 5.0 + DOWN * 2.35, PI / 5),
            (LEFT * 0.4 + DOWN * 1.5, PI / 10),
        ]

        # Derived values
        half_line_len = line_len / 2
        half_needle_len = needle_len / 2
        center_offset = (line_count - 1) / 2

        def get_line_ys():
            line_ys = []

            for i in range(line_count):
                line_y = (i - center_offset) * d
                line_ys.append(line_y)

            return line_ys

        def create_distance_markers(line_ys):
            markers = VGroup()
            marker_xs = [-5.45, 5.45]

            for marker_x in marker_xs:
                for lower_y, upper_y in zip(line_ys[:-1], line_ys[1:]):
                    arrow = DoubleArrow(
                        start=RIGHT * marker_x + UP * lower_y,
                        end=RIGHT * marker_x + UP * upper_y,
                        buff=0.08,
                        color=WHITE,
                        stroke_width=2.0,
                    )

                    label = MathTex(
                        "d",
                        font_size=28,
                        color=WHITE,
                    )

                    if marker_x < 0:
                        label.next_to(arrow, LEFT, buff=0.08)
                    else:
                        label.next_to(arrow, RIGHT, buff=0.08)

                    marker = VGroup(arrow, label)
                    markers.add(marker)

            return markers

        def get_needle_endpoints(needle_mid, needle_angle):
            direction = RIGHT * math.cos(needle_angle) + UP * math.sin(needle_angle)

            needle_start = needle_mid - half_needle_len * direction
            needle_end = needle_mid + half_needle_len * direction

            return needle_start, needle_end

        def get_crossing_data(needle_mid, needle_angle):
            needle_start, needle_end = get_needle_endpoints(needle_mid, needle_angle)

            y1 = needle_start[1]
            y2 = needle_end[1]

            lower_y = min(y1, y2)
            upper_y = max(y1, y2)

            for line_y in line_ys:
                if lower_y <= line_y <= upper_y:
                    t = (line_y - y1) / (y2 - y1)
                    x = needle_start[0] + t * (needle_end[0] - needle_start[0])

                    crossing_point = RIGHT * x + UP * line_y

                    return True, crossing_point

            return False, None

        def create_needle(needle_mid, needle_angle):
            needle_start, needle_end = get_needle_endpoints(needle_mid, needle_angle)
            crosses, crossing_point = get_crossing_data(needle_mid, needle_angle)

            if crosses:
                needle_color = crossing_color
            else:
                needle_color = non_crossing_color

            needle_outline = Line(
                start=needle_start,
                end=needle_end,
                color=needle_outline_color,
                stroke_width=needle_outline_width,
            )

            needle_inner = Line(
                start=needle_start,
                end=needle_end,
                color=needle_color,
                stroke_width=needle_width,
            )

            needle = VGroup(needle_outline, needle_inner)

            return needle, crosses, crossing_point

        def create_stats(crossing_count, non_crossing_count):
            total_count = crossing_count + non_crossing_count
            probability = crossing_count / total_count
            probability_text = f"{probability:.2f}".rstrip("0").rstrip(".")

            formula = MathTex(
                r"P \approx \frac{",
                f"{crossing_count}",
                r"}{",
                f"{crossing_count}",
                r"+",
                f"{non_crossing_count}",
                r"}",
                r"=",
                probability_text,
                font_size=30,
                color=WHITE,
            )

            formula[1].set_color(crossing_color)
            formula[3].set_color(crossing_color)
            formula[5].set_color(non_crossing_color)

            content = VGroup(
                Text("Experiment", font_size=22),
                Text(
                    f"crossings = {crossing_count}",
                    font_size=20,
                    color=crossing_color,
                ),
                Text(
                    f"no crаossings = {non_crossing_count}",
                    font_size=20,
                    color=non_crossing_color,
                ),
                formula,
            )

            content.arrange(DOWN, aligned_edge=LEFT, buff=0.10)

            # Fixed statistics box position and size
            box_w = 3.3
            box_h = 1.65
            box_center = RIGHT * 4.5 + UP * 2.0

            background = RoundedRectangle(
                width=box_w,
                height=box_h,
                corner_radius=0.08,
                color=BLACK,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_opacity=0,
            )

            background.move_to(box_center)

            # Keep the text fixed inside the box.
            # This prevents horizontal jumping when P changes width.
            content.move_to(background.get_center())
            content.align_to(background, LEFT)
            content.align_to(background, UP)
            content.shift(RIGHT * 0.18 + DOWN * 0.14)

            return VGroup(background, content)

        def show_intro_needle(needle, crosses, crossing_point, label_side=RIGHT):
            if crosses:
                label = Text("crossing", font_size=28, color=crossing_color)
            else:
                label = Text("no crossing", font_size=28, color=non_crossing_color)

            label.next_to(needle, label_side, buff=0.28)

            self.play(
                FadeIn(needle, shift=DOWN * 0.3),
                run_time=slow_drop_time,
            )

            self.play(
                FadeIn(label),
                run_time=label_fade_time,
            )

            if crosses:
                point = Dot(
                    crossing_point,
                    radius=0.07,
                    color=intersection_color,
                )

                ring = Circle(
                    radius=0.18,
                    color=intersection_color,
                    stroke_width=3,
                )
                ring.move_to(crossing_point)

                self.play(
                    GrowFromCenter(point),
                    Create(ring),
                    run_time=point_fade_time,
                )

                self.wait(point_hold_time)

                self.play(
                    Indicate(ring, color=intersection_color),
                    run_time=0.8,
                )

                self.play(
                    FadeOut(point),
                    FadeOut(ring),
                    run_time=0.3,
                )
            else:
                self.wait(label_hold_time)

            self.wait(0.25)

            self.play(
                FadeOut(label),
                run_time=0.35,
            )

        # Create parallel lines
        line_ys = get_line_ys()
        lines = VGroup()

        for line_y in line_ys:
            line_shift = UP * line_y

            line = Line(
                start=LEFT * half_line_len + line_shift,
                end=RIGHT * half_line_len + line_shift,
                color=line_color,
            )

            lines.add(line)

        # Create line annotations
        distance_markers = create_distance_markers(line_ys)

        # Create needles and crossing information
        needle_records = []

        for needle_mid, needle_angle in needle_data:
            needle, crosses, crossing_point = create_needle(needle_mid, needle_angle)
            needle_records.append((needle, crosses, crossing_point))

        # Create title
        title = Text(
            "Buffon's needle experiment",
            font_size=title_size,
        )
        title.to_edge(UP)

        # Animate scene
        self.play(Write(title))
        self.play(
            AnimationGroup(
                *[Create(line) for line in lines],
                lag_ratio=0,
            ),
            run_time=1.0,
        )

        self.wait(0.4)

        self.play(
            AnimationGroup(
                *[Create(marker) for marker in distance_markers],
                lag_ratio=0,
            ),
            run_time=1.0,
        )

        self.wait(2.4)

        self.play(
            FadeOut(distance_markers),
            run_time=0.8,
        )

        self.wait(0.4)

        crossing_count = 0
        non_crossing_count = 0

        # 1st label is on the right, 2nd stays below
        intro_label_sides = [RIGHT, DOWN]

        # Slow explanation: no crossing, crossing
        for index, (needle, crosses, crossing_point) in enumerate(needle_records[:2]):
            show_intro_needle(
                needle,
                crosses,
                crossing_point,
                label_side=intro_label_sides[index],
            )

            if crosses:
                crossing_count += 1
            else:
                non_crossing_count += 1

        # Create counter after the first two examples
        stats = create_stats(crossing_count, non_crossing_count)
        self.play(FadeIn(stats), run_time=0.7)
        self.wait(0.5)

        # Continue experiment faster
        for needle, crosses, crossing_point in needle_records[2:]:
            self.play(
                FadeIn(needle, shift=DOWN * 0.3),
                run_time=fast_drop_time,
            )

            if crosses:
                crossing_count += 1
            else:
                non_crossing_count += 1

            new_stats = create_stats(crossing_count, non_crossing_count)

            self.play(
                Transform(stats, new_stats),
                run_time=0.25,
            )

        self.wait(2)