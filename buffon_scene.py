from manim import *
import math
import random


class BuffonNeedleExperimentScene(Scene):
    def construct(self):
        # Scene parameters
        d = 1.45
        line_count = 5
        line_len = 12.0
        line_color = BLUE
        title_size = 36

        # Needle parameters
        needle_len = d
        half_needle_len = needle_len / 2
        neutral_needle_color = WHITE
        crossing_color = GREEN
        non_crossing_color = RED
        needle_width = 4
        needle_outline_color = GRAY
        needle_outline_width = 6

        # Visual parameters
        intersection_color = YELLOW
        box_fill_opacity = 0.78
        fast_drop_time = 0.22

        # Final deterministic experiment values
        final_total_count = 50000
        final_crossing_count = 31831

        # Derived values
        half_line_len = line_len / 2
        center_offset = (line_count - 1) / 2

        def format_decimal(value, digits=5):
            return f"{value:.{digits}f}".rstrip("0").rstrip(".")

        def get_line_ys():
            return [(i - center_offset) * d for i in range(line_count)]

        def create_text_box(content, min_width=0, buff=0.22, fill_opacity=box_fill_opacity):
            box_w = max(content.width + 2 * buff, min_width)
            box_h = content.height + 2 * buff

            background = RoundedRectangle(
                width=box_w,
                height=box_h,
                corner_radius=0.08,
                color=BLACK,
                fill_color=BLACK,
                fill_opacity=fill_opacity,
                stroke_opacity=0,
            )
            background.move_to(content.get_center())

            group = VGroup(background, content)
            group.set_z_index(30)

            return group

        def create_center_box(content, min_width=0):
            # Every black text box is centered at (0, 0),
            # except the experiment counter.
            content.move_to(ORIGIN)
            return create_text_box(content, min_width=min_width)

        def create_lines(line_ys):
            lines = VGroup()

            for line_y in line_ys:
                line = Line(
                    start=LEFT * half_line_len + UP * line_y,
                    end=RIGHT * half_line_len + UP * line_y,
                    color=line_color,
                )
                lines.add(line)

            return lines

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

                    label = MathTex("d", font_size=28, color=WHITE)

                    if marker_x < 0:
                        label.next_to(arrow, LEFT, buff=0.08)
                    else:
                        label.next_to(arrow, RIGHT, buff=0.08)

                    markers.add(VGroup(arrow, label))

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

            if abs(y2 - y1) < 1e-9:
                return False, None

            for line_y in line_ys:
                if lower_y <= line_y <= upper_y:
                    t = (line_y - y1) / (y2 - y1)
                    x = needle_start[0] + t * (needle_end[0] - needle_start[0])
                    crossing_point = RIGHT * x + UP * line_y

                    return True, crossing_point

            return False, None

        def create_needle(needle_mid, needle_angle, needle_color=None, opacity=1.0):
            needle_start, needle_end = get_needle_endpoints(needle_mid, needle_angle)
            crosses, crossing_point = get_crossing_data(needle_mid, needle_angle)

            if needle_color is None:
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
            needle_outline.set_opacity(opacity)

            needle_inner = Line(
                start=needle_start,
                end=needle_end,
                color=needle_color,
                stroke_width=needle_width,
            )
            needle_inner.set_opacity(opacity)

            needle = VGroup(needle_outline, needle_inner)

            return needle, crosses, crossing_point

        def create_length_marker(needle_mid, needle_angle):
            needle_start, needle_end = get_needle_endpoints(needle_mid, needle_angle)

            normal = LEFT * math.sin(needle_angle) + UP * math.cos(needle_angle)
            offset = normal * 0.24

            arrow = DoubleArrow(
                start=needle_start + offset,
                end=needle_end + offset,
                buff=0.02,
                color=WHITE,
                stroke_width=2.0,
                max_tip_length_to_length_ratio=0.24,
            )

            label = VGroup(
                Text("needle length", font_size=20, color=WHITE),
                MathTex("l", font_size=30, color=WHITE),
            )
            label.arrange(RIGHT, buff=0.18)
            label.next_to(arrow, UP, buff=0.10)

            return VGroup(arrow, label)

        def create_stats(total_count, crossing_count):
            probability = crossing_count / total_count
            probability_text = format_decimal(probability, digits=5)

            title_text = Text("Experiment", font_size=21)

            n_row = MathTex("N", "=", f"{total_count}", font_size=27, color=WHITE)

            k_row = MathTex("K", "=", f"{crossing_count}", font_size=27, color=WHITE)
            k_row[0].set_color(crossing_color)
            k_row[2].set_color(crossing_color)

            p_row = MathTex(
                r"P_{\mathrm{exp}}",
                r"\approx",
                r"\frac{",
                "K",
                r"}{",
                "N",
                r"}",
                "=",
                probability_text,
                font_size=26,
                color=WHITE,
            )
            p_row[3].set_color(crossing_color)

            content = VGroup(title_text, n_row, k_row, p_row)
            content.arrange(DOWN, aligned_edge=LEFT, buff=0.08)

            box_w = 3.15
            box_h = 1.74
            box_center_x = half_line_len - box_w / 2
            box_center = RIGHT * box_center_x + UP * 2.18

            background = RoundedRectangle(
                width=box_w,
                height=box_h,
                corner_radius=0.08,
                color=BLACK,
                fill_color=BLACK,
                fill_opacity=0.75,
                stroke_opacity=0,
            )
            background.move_to(box_center)

            content.move_to(background.get_center())
            content.align_to(background, LEFT)
            content.align_to(background, UP)
            content.shift(RIGHT * 0.15 + DOWN * 0.13)

            background.set_z_index(20)
            content.set_z_index(21)

            return VGroup(background, content)

        def create_random_text_box():
            content = VGroup(
                Text("Each throw is random", font_size=28, color=WHITE),
                Text("random position", font_size=22, color=WHITE),
                Text("random angle", font_size=22, color=WHITE),
            )
            content.arrange(DOWN, buff=0.12)
            return create_center_box(content, min_width=4.8)

        def play_random_throw(needle, needle_mid, needle_angle, show_info_text=False):
            info_box = None

            if show_info_text:
                info_box = create_random_text_box()
                self.play(FadeIn(info_box), run_time=0.45)
                self.wait(1.25)

            # 1. Random position: shown as a slowly moving dot.
            position_points = [
                LEFT * 4.6 + UP * 0.4,
                RIGHT * 2.8 + DOWN * 1.1,
                LEFT * 1.3 + DOWN * 2.0,
                needle_mid,
            ]

            dot = Dot(position_points[0], radius=0.06, color=YELLOW)
            dot.set_z_index(25)

            self.play(FadeIn(dot), run_time=0.35)

            for position_point in position_points[1:]:
                self.play(
                    dot.animate.move_to(position_point),
                    run_time=0.72,
                )

            self.wait(0.20)

            # 2. Random angle: the needle length stays fixed.
            angle_sequence = [0, PI / 3, -PI / 5, needle_angle]

            preview, _, _ = create_needle(
                needle_mid,
                angle_sequence[0],
                needle_color=neutral_needle_color,
                opacity=0.75,
            )
            preview.set_z_index(12)

            self.play(
                FadeOut(dot),
                FadeIn(preview),
                run_time=0.35,
            )

            for preview_angle in angle_sequence[1:]:
                next_preview, _, _ = create_needle(
                    needle_mid,
                    preview_angle,
                    needle_color=neutral_needle_color,
                    opacity=0.75,
                )
                next_preview.set_z_index(12)

                self.play(
                    ReplacementTransform(preview, next_preview),
                    run_time=0.72,
                )
                preview = next_preview

            needle.set_z_index(12)

            animations = [ReplacementTransform(preview, needle)]

            if info_box is not None:
                animations.append(FadeOut(info_box))

            self.play(*animations, run_time=0.42)

        def show_result(needle, crosses, crossing_point):
            if crosses:
                result_color = crossing_color
                result_text = "crossing"
            else:
                result_color = non_crossing_color
                result_text = "no crossing"

            label = Text(result_text, font_size=28, color=result_color)
            label_box = create_center_box(label, min_width=2.9)

            self.play(
                needle[1].animate.set_color(result_color),
                run_time=0.35,
            )

            self.play(FadeIn(label_box), run_time=0.35)

            if crosses:
                point = Dot(crossing_point, radius=0.07, color=intersection_color)
                point.set_z_index(25)

                ring = Circle(radius=0.18, color=intersection_color, stroke_width=3)
                ring.move_to(crossing_point)
                ring.set_z_index(25)

                self.play(
                    GrowFromCenter(point),
                    Create(ring),
                    run_time=0.4,
                )

                self.wait(0.65)

                self.play(
                    Indicate(ring, color=intersection_color),
                    run_time=0.7,
                )

                self.play(
                    FadeOut(point),
                    FadeOut(ring),
                    run_time=0.25,
                )
            else:
                self.wait(0.8)

            self.play(FadeOut(label_box), run_time=0.3)

        def make_many_throw_batch(seed, count):
            rng = random.Random(seed)
            data = []

            for _ in range(count):
                x = rng.uniform(-5.25, 5.15)
                y = rng.uniform(-2.55, 2.55)
                angle = rng.uniform(-PI / 2.15, PI / 2.15)
                data.append((RIGHT * x + UP * y, angle))

            return data

        def create_many_throw_batch(seed, count, opacity=0.22):
            batch = VGroup()

            for needle_mid, needle_angle in make_many_throw_batch(seed, count):
                needle, _, _ = create_needle(
                    needle_mid,
                    needle_angle,
                    opacity=opacity,
                )
                batch.add(needle)

            return batch

        def create_aligned_formula_row(
            left_tex,
            middle_tex,
            sign_tex,
            value_tex,
            y,
            font_size=34,
            sign_x=1.55,
        ):
            left = MathTex(left_tex, font_size=font_size, color=WHITE)
            middle = MathTex(middle_tex, font_size=font_size, color=WHITE)
            sign = MathTex(sign_tex, font_size=font_size, color=WHITE)
            value = MathTex(value_tex, font_size=font_size, color=WHITE)

            sign.move_to(RIGHT * sign_x + UP * y)
            middle.next_to(sign, LEFT, buff=0.26)
            left.next_to(middle, LEFT, buff=0.28)
            value.next_to(sign, RIGHT, buff=0.22)

            row = VGroup(left, middle, sign, value)
            row.value_part = value
            row.sign = sign

            return row

        def create_aligned_value_row(
            left_tex,
            sign_tex,
            value_tex,
            y,
            font_size=34,
            sign_x=1.55,
        ):
            left = MathTex(left_tex, font_size=font_size, color=WHITE)
            sign = MathTex(sign_tex, font_size=font_size, color=WHITE)
            value = MathTex(value_tex, font_size=font_size, color=WHITE)

            sign.move_to(RIGHT * sign_x + UP * y)
            left.next_to(sign, LEFT, buff=0.28)
            value.next_to(sign, RIGHT, buff=0.22)

            row = VGroup(left, sign, value)
            row.value_part = value
            row.sign = sign

            return row

        line_ys = get_line_ys()
        lines = create_lines(line_ys)
        distance_markers = create_distance_markers(line_ys)

        title = Text("Buffon's needle experiment", font_size=title_size)
        title.to_edge(UP)

        # Sample needle for l and d comparison. This is not counted as a throw.
        sample_mid = LEFT * 0.6 + UP * 0.75
        sample_angle = PI / 6
        sample_needle, _, _ = create_needle(
            sample_mid,
            sample_angle,
            needle_color=neutral_needle_color,
        )
        sample_length_marker = create_length_marker(sample_mid, sample_angle)

        condition_content = VGroup(
            Text("In this experiment:", font_size=25, color=WHITE),
            MathTex("l", "=", "d", font_size=40, color=WHITE),
        )
        condition_content.arrange(DOWN, buff=0.10)
        condition_box = create_center_box(condition_content, min_width=3.9)

        # Visible throws: first is no crossing, second is crossing.
        visible_throw_data = [
            (LEFT * 4.3 + UP * 2.23, PI / 10),
            (LEFT * 2.2 + UP * 1.25, -PI / 2.7),
            (RIGHT * 0.5 + DOWN * 0.35, PI / 4.0),
            (RIGHT * 3.2 + UP * 0.25, -PI / 3.0),
            (LEFT * 4.7 + DOWN * 1.15, PI / 8.0),
            (RIGHT * 2.0 + DOWN * 2.18, -PI / 6.0),
            (LEFT * 0.7 + UP * 2.62, PI / 2.9),
            (RIGHT * 4.6 + DOWN * 0.55, -PI / 5.5),
            (LEFT * 3.3 + DOWN * 2.30, PI / 3.6),
            (RIGHT * 0.1 + UP * 0.28, -PI / 8.0),
            (LEFT * 1.6 + DOWN * 0.90, PI / 2.8),
            (RIGHT * 5.1 + UP * 1.85, -PI / 7.0),
        ]

        visible_throw_records = []

        for index, (needle_mid, needle_angle) in enumerate(visible_throw_data):
            needle_color = neutral_needle_color if index < 2 else None

            needle, crosses, crossing_point = create_needle(
                needle_mid,
                needle_angle,
                needle_color=needle_color,
            )
            visible_throw_records.append((needle, crosses, crossing_point, needle_mid, needle_angle))

        many_batches = [
            create_many_throw_batch(seed=11, count=14, opacity=0.21),
            create_many_throw_batch(seed=22, count=16, opacity=0.19),
            create_many_throw_batch(seed=33, count=18, opacity=0.17),
            create_many_throw_batch(seed=44, count=22, opacity=0.15),
        ]

        visible_needles = VGroup()

        # 1. Title
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # 2. Parallel lines
        self.play(
            AnimationGroup(
                *[Create(line) for line in lines],
                lag_ratio=0,
            ),
            run_time=1.0,
        )
        self.wait(0.35)

        # 3. Distance d
        self.play(
            AnimationGroup(
                *[Create(marker) for marker in distance_markers],
                lag_ratio=0,
            ),
            run_time=1.0,
        )
        self.wait(1.2)

        # 4-5. Needle length l and condition l = d
        self.play(
            FadeIn(sample_needle, shift=DOWN * 0.25),
            run_time=0.8,
        )
        self.play(
            FadeIn(sample_length_marker),
            FadeIn(condition_box),
            run_time=0.65,
        )
        self.wait(1.7)

        self.play(
            FadeOut(sample_length_marker),
            FadeOut(condition_box),
            FadeOut(sample_needle),
            FadeOut(distance_markers),
            run_time=0.55,
        )
        self.wait(0.25)

        total_count = 0
        crossing_count = 0

        # 6-7. Randomness and first throw: no crossing
        first_needle, first_crosses, first_crossing_point, first_mid, first_angle = visible_throw_records[0]
        play_random_throw(first_needle, first_mid, first_angle, show_info_text=True)
        visible_needles.add(first_needle)

        show_result(first_needle, first_crosses, first_crossing_point)

        total_count += 1
        if first_crosses:
            crossing_count += 1

        # 8. Second throw: crossing. No repeated randomness text.
        second_needle, second_crosses, second_crossing_point, second_mid, second_angle = visible_throw_records[1]
        play_random_throw(second_needle, second_mid, second_angle, show_info_text=False)
        visible_needles.add(second_needle)

        show_result(second_needle, second_crosses, second_crossing_point)

        total_count += 1
        if second_crosses:
            crossing_count += 1

        # 9. Counter
        stats = create_stats(total_count, crossing_count)

        self.play(FadeIn(stats), run_time=0.65)
        self.wait(0.55)

        # 10. Short visible random-looking series
        for needle, crosses, crossing_point, _, _ in visible_throw_records[2:]:
            self.play(
                FadeIn(needle, shift=DOWN * 0.20),
                run_time=fast_drop_time,
            )
            visible_needles.add(needle)

            total_count += 1
            if crosses:
                crossing_count += 1

            new_stats = create_stats(total_count, crossing_count)

            self.play(
                Transform(stats, new_stats),
                run_time=0.24,
            )

        self.wait(0.4)

        # 11. Small sample is noisy
        noisy_text = Text("A small sample is noisy.", font_size=30, color=WHITE)
        noisy_box = create_center_box(noisy_text, min_width=4.8)

        self.play(FadeIn(noisy_box), run_time=0.45)
        self.wait(1.35)
        self.play(FadeOut(noisy_box), run_time=0.35)

        # 12. Many random throws
        repeat_text = Text("Now repeat randomly many times.", font_size=30, color=WHITE)
        repeat_box = create_center_box(repeat_text, min_width=6.1)

        self.play(FadeIn(repeat_box), run_time=0.45)
        self.wait(1.0)

        self.play(
            FadeOut(repeat_box),
            visible_needles.animate.set_opacity(0.36),
            run_time=0.55,
        )

        many_throw_stats = [
            (100, 64),
            (1000, 637),
            (5000, 3183),
            (final_total_count, final_crossing_count),
        ]

        for batch, (total_count, crossing_count) in zip(many_batches, many_throw_stats):
            self.play(
                AnimationGroup(
                    *[FadeIn(needle, shift=DOWN * 0.08) for needle in batch],
                    lag_ratio=0.02,
                ),
                run_time=0.85,
            )

            new_stats = create_stats(total_count, crossing_count)

            self.play(
                Transform(stats, new_stats),
                run_time=0.65,
            )
            self.bring_to_front(stats)
            self.wait(0.35)

        # 13. Final experiment result
        final_p = final_crossing_count / final_total_count
        final_result_content = VGroup(
            Text("After many random throws:", font_size=27, color=WHITE),
            MathTex(
                "N",
                "=",
                str(final_total_count),
                r"\qquad",
                "K",
                "=",
                str(final_crossing_count),
                font_size=34,
                color=WHITE,
            ),
            MathTex(
                r"P_{\mathrm{exp}}",
                "=",
                r"\frac{K}{N}",
                r"\approx",
                f"{format_decimal(final_p, digits=5)}\\ldots",
                font_size=36,
                color=WHITE,
            ),
        )
        final_result_content[1][4].set_color(crossing_color)
        final_result_content[1][6].set_color(crossing_color)
        final_result_content.arrange(DOWN, buff=0.18)
        final_result_box = create_center_box(final_result_content, min_width=6.7)

        self.play(FadeIn(final_result_box), run_time=0.6)
        self.wait(3.1)

        # 14. Pi tease formula scene
        dim_layer = Rectangle(
            width=14.5,
            height=8.3,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.65,
            stroke_opacity=0,
        )
        dim_layer.set_z_index(40)

        self.play(
            FadeOut(final_result_box),
            FadeIn(dim_layer),
            run_time=0.6,
        )

        row1 = create_aligned_formula_row(
            r"P_{\mathrm{exp}}",
            r"=\frac{K}{N}",
            r"\approx",
            r"0.63662\ldots",
            y=1.65,
            font_size=34,
        )

        row2 = create_aligned_formula_row(
            r"\frac{1}{P_{\mathrm{exp}}}",
            r"=\frac{N}{K}",
            r"\approx",
            r"1.57079\ldots",
            y=0.55,
            font_size=34,
        )

        row3 = create_aligned_formula_row(
            r"\frac{2}{P_{\mathrm{exp}}}",
            r"=\frac{2N}{K}",
            r"\approx",
            r"3.14159\ldots",
            y=-0.55,
            font_size=34,
        )

        pi_row = create_aligned_value_row(
            r"\pi",
            r"\approx",
            r"3.14159\ldots",
            y=-1.65,
            font_size=34,
        )
        pi_row[0].set_color(RED)

        formula_rows = VGroup(row1, row2, row3, pi_row)
        formula_rows.move_to(ORIGIN)
        formula_rows.set_z_index(45)

        for row in [row1, row2, row3, pi_row]:
            self.play(Write(row), run_time=0.95)
            self.wait(0.55)

        row3_highlight = SurroundingRectangle(
            row3.value_part,
            color=YELLOW,
            buff=0.10,
            stroke_width=3,
        )
        pi_highlight = SurroundingRectangle(
            pi_row.value_part,
            color=YELLOW,
            buff=0.10,
            stroke_width=3,
        )

        highlights = VGroup(row3_highlight, pi_highlight)
        highlights.set_z_index(46)

        self.play(
            Create(row3_highlight),
            Create(pi_highlight),
            run_time=0.85,
        )
        self.wait(1.15)

        eq_start = MathTex(
            r"\frac{2}{P_{\mathrm{exp}}}",
            "=",
            r"\frac{2N}{K}",
            r"\approx",
            r"\pi",
            font_size=44,
            color=WHITE,
        )
        eq_start[4].set_color(RED)
        eq_start.move_to(UP * 0.85)
        eq_start.set_z_index(47)

        self.play(
            FadeOut(row1),
            FadeOut(row2),
            FadeOut(pi_row),
            FadeOut(highlights),
            ReplacementTransform(row3, eq_start),
            run_time=0.9,
        )
        self.wait(0.85)

        eq_mid = MathTex(
            r"\frac{2}{P_{\mathrm{exp}}}",
            r"\approx",
            r"\pi",
            font_size=46,
            color=WHITE,
        )
        eq_mid[2].set_color(RED)
        eq_mid.move_to(UP * 0.85)
        eq_mid.set_z_index(47)

        self.play(
            TransformMatchingTex(eq_start, eq_mid),
            run_time=0.9,
        )
        self.wait(0.75)

        eq_result = MathTex(
            "P",
            r"\approx",
            r"\frac{2}{",
            r"\pi",
            "}",
            font_size=50,
            color=WHITE,
        )
        eq_result[3].set_color(RED)
        eq_result.move_to(UP * 0.85)
        eq_result.set_z_index(47)

        self.play(
            TransformMatchingTex(eq_mid, eq_result),
            run_time=0.9,
        )
        self.wait(0.9)

        # Final layout:
        # - P ≈ 2/pi slightly above the center
        # - left question below-left
        # - right question below-right
        # - proof prompt below the center
        eq_result.generate_target()
        eq_result.target.move_to(UP * 0.75)

        left_question = VGroup(
            Text("What is", font_size=32, color=WHITE),
            MathTex(r"\pi", font_size=40, color=RED),
            Text("doing here?", font_size=32, color=WHITE),
        )
        left_question.arrange(RIGHT, buff=0.12)
        left_question.move_to(LEFT * 2.85 + DOWN * 0.75)
        left_question.set_z_index(48)

        right_question = VGroup(
            Text("What if", font_size=32, color=WHITE),
            MathTex("l", "<", "d", font_size=40, color=WHITE),
            Text("?", font_size=32, color=WHITE),
        )
        right_question.arrange(RIGHT, buff=0.12)
        right_question.move_to(RIGHT * 2.85 + DOWN * 0.75)
        right_question.set_z_index(48)

        proof_prompt = Text(
            "Now we need a proof.",
            font_size=34,
            color=WHITE,
        )
        proof_prompt.move_to(DOWN * 2.0)
        proof_prompt.set_z_index(48)

        final_message_group = VGroup(
            eq_result,
            left_question,
            right_question,
            proof_prompt,
        )

        self.play(
            MoveToTarget(eq_result),
            FadeIn(left_question),
            FadeIn(right_question),
            FadeIn(proof_prompt),
            run_time=0.85,
        )
        self.wait(2.6)

        self.play(
            FadeOut(final_message_group),
            FadeOut(dim_layer),
            FadeOut(stats),
            FadeOut(visible_needles),
            *[FadeOut(batch) for batch in many_batches],
            FadeOut(lines),
            FadeOut(title),
            run_time=0.85,
        )
        self.wait(0.4)