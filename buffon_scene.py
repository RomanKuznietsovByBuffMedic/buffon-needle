from dataclasses import dataclass
from dataclasses import field
import math
import random

from manim import *


@dataclass(frozen=True)
class BoardConfig:
    line_spacing: float = 1.45
    line_count: int = 5
    line_length: float = 18.0

    @property
    def needle_length(self):
        return self.line_spacing

    @property
    def half_needle_length(self):
        return self.needle_length / 2

    @property
    def half_line_length(self):
        return self.line_length / 2

    @property
    def center_offset(self):
        return (self.line_count - 1) / 2


@dataclass(frozen=True)
class VisualConfig:
    line_color = BLUE
    neutral_needle_color = WHITE
    crossing_color = GREEN
    non_crossing_color = RED
    needle_outline_color = GRAY
    intersection_color = YELLOW

    title_font_size: int = 36
    needle_width: int = 4
    needle_outline_width: int = 6
    box_fill_opacity: float = 0.78
    fast_drop_time: float = 0.22

    stats_box_width: float = 3.15
    stats_box_height: float = 1.74
    stats_box_center = RIGHT * 4.42 + UP * 2.18


@dataclass(frozen=True)
class ThrowSpec:
    midpoint: object
    angle: float


@dataclass(frozen=True)
class BatchSpec:
    seed: int
    count: int
    opacity: float
    total_after: int
    crossing_after: int


@dataclass
class ExperimentCounts:
    total: int = 0
    crossing: int = 0

    def add_throw(self, crosses):
        self.total += 1

        if crosses:
            self.crossing += 1


@dataclass(frozen=True)
class ExperimentConfig:
    final_total_count: int = 50_000
    final_crossing_count: int = 31_831

    visible_throws: list = field(
        default_factory=lambda: [
            ThrowSpec(LEFT * 4.3 + UP * 2.23, PI / 10),
            ThrowSpec(LEFT * 2.2 + UP * 1.25, -PI / 2.7),
            ThrowSpec(RIGHT * 0.5 + DOWN * 0.35, PI / 4.0),
            ThrowSpec(RIGHT * 3.2 + UP * 0.25, -PI / 3.0),
            ThrowSpec(LEFT * 4.7 + DOWN * 1.15, PI / 8.0),
            ThrowSpec(RIGHT * 2.0 + DOWN * 2.18, -PI / 6.0),
            ThrowSpec(LEFT * 0.7 + UP * 2.62, PI / 2.9),
            ThrowSpec(RIGHT * 4.6 + DOWN * 0.55, -PI / 5.5),
            ThrowSpec(LEFT * 3.3 + DOWN * 2.30, PI / 3.6),
            ThrowSpec(RIGHT * 0.1 + UP * 0.28, -PI / 8.0),
            ThrowSpec(LEFT * 1.6 + DOWN * 0.90, PI / 2.8),
            ThrowSpec(RIGHT * 5.1 + UP * 1.85, -PI / 7.0),
        ],
    )

    batch_specs: list = field(
        default_factory=lambda: [
            BatchSpec(11, 14, 0.21, 100, 64),
            BatchSpec(22, 16, 0.19, 1_000, 637),
            BatchSpec(33, 18, 0.17, 5_000, 3_183),
            BatchSpec(44, 22, 0.15, 50_000, 31_831),
        ],
    )


@dataclass
class NeedleRecord:
    needle: object
    crosses: bool
    crossing_point: object
    midpoint: object
    angle: float


class BuffonGeometry:
    def __init__(self, board):
        self.board = board

    def line_ys(self):
        return [
            (index - self.board.center_offset) * self.board.line_spacing
            for index in range(self.board.line_count)
        ]

    def needle_endpoints(self, midpoint, angle):
        direction = RIGHT * math.cos(angle) + UP * math.sin(angle)

        start = midpoint - self.board.half_needle_length * direction
        end = midpoint + self.board.half_needle_length * direction

        return start, end

    def crossing_data(self, midpoint, angle):
        start, end = self.needle_endpoints(midpoint, angle)

        y_start = start[1]
        y_end = end[1]

        lower_y = min(y_start, y_end)
        upper_y = max(y_start, y_end)

        if abs(y_end - y_start) < 1e-9:
            return False, None

        for line_y in self.line_ys():
            if lower_y <= line_y <= upper_y:
                t = (line_y - y_start) / (y_end - y_start)
                x = start[0] + t * (end[0] - start[0])
                crossing_point = RIGHT * x + UP * line_y

                return True, crossing_point

        return False, None

    def random_throw_specs(self, seed, count):
        rng = random.Random(seed)
        specs = []

        for _ in range(count):
            x = rng.uniform(-5.25, 5.15)
            y = rng.uniform(-2.55, 2.55)
            angle = rng.uniform(-PI / 2.15, PI / 2.15)
            midpoint = RIGHT * x + UP * y

            specs.append(ThrowSpec(midpoint, angle))

        return specs


class BuffonMobjectFactory:
    def __init__(self, board, visual, geometry):
        self.board = board
        self.visual = visual
        self.geometry = geometry

    def decimal_text(self, value, digits=5):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")

    def text_box(
        self,
        content,
        min_width=0,
        buff=0.22,
        fill_opacity=None,
    ):
        if fill_opacity is None:
            fill_opacity = self.visual.box_fill_opacity

        box_width = max(content.width + 2 * buff, min_width)
        box_height = content.height + 2 * buff

        background = RoundedRectangle(
            width=box_width,
            height=box_height,
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

    def center_box(self, content, min_width=0):
        content.move_to(ORIGIN)
        return self.text_box(content, min_width=min_width)

    def lines(self):
        lines = VGroup()

        for line_y in self.geometry.line_ys():
            line = Line(
                start=LEFT * self.board.half_line_length + UP * line_y,
                end=RIGHT * self.board.half_line_length + UP * line_y,
                color=self.visual.line_color,
            )
            lines.add(line)

        return lines

    def distance_markers(self):
        markers = VGroup()
        marker_xs = [-5.45, 5.45]
        line_ys = self.geometry.line_ys()

        for marker_x in marker_xs:
            for lower_y, upper_y in zip(line_ys[:-1], line_ys[1:]):
                marker = self.distance_marker(marker_x, lower_y, upper_y)
                markers.add(marker)

        return markers

    def distance_marker(self, marker_x, lower_y, upper_y):
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

        return VGroup(arrow, label)

    def needle(self, midpoint, angle, needle_color=None, opacity=1.0):
        start, end = self.geometry.needle_endpoints(midpoint, angle)
        crosses, crossing_point = self.geometry.crossing_data(midpoint, angle)

        if needle_color is None:
            needle_color = self.needle_color_for(crosses)

        outline = Line(
            start=start,
            end=end,
            color=self.visual.needle_outline_color,
            stroke_width=self.visual.needle_outline_width,
        )
        outline.set_opacity(opacity)

        inner = Line(
            start=start,
            end=end,
            color=needle_color,
            stroke_width=self.visual.needle_width,
        )
        inner.set_opacity(opacity)

        return VGroup(outline, inner), crosses, crossing_point

    def needle_color_for(self, crosses):
        if crosses:
            return self.visual.crossing_color

        return self.visual.non_crossing_color

    def length_marker(self, midpoint, angle):
        start, end = self.geometry.needle_endpoints(midpoint, angle)
        normal = LEFT * math.sin(angle) + UP * math.cos(angle)
        offset = normal * 0.24

        arrow = DoubleArrow(
            start=start + offset,
            end=end + offset,
            buff=0.02,
            color=WHITE,
            stroke_width=2.0,
            max_tip_length_to_length_ratio=0.24,
        )

        label = VGroup(
            Text("довжина голки", font_size=20, color=WHITE),
            MathTex("l", font_size=30, color=WHITE),
        )
        label.arrange(RIGHT, buff=0.18)
        label.next_to(arrow, UP, buff=0.10)

        return VGroup(arrow, label)

    def stats_box(self, total_count, crossing_count):
        probability = crossing_count / total_count
        probability_text = self.decimal_text(probability, digits=5)

        title = Text("Експеримент", font_size=21)
        n_row = MathTex(
            "N",
            "=",
            f"{total_count}",
            font_size=27,
            color=WHITE,
        )
        k_row = MathTex(
            "K",
            "=",
            f"{crossing_count}",
            font_size=27,
            color=WHITE,
        )
        k_row[0].set_color(self.visual.crossing_color)
        k_row[2].set_color(self.visual.crossing_color)

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
        p_row[3].set_color(self.visual.crossing_color)

        content = VGroup(title, n_row, k_row, p_row)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        background = RoundedRectangle(
            width=self.visual.stats_box_width,
            height=self.visual.stats_box_height,
            corner_radius=0.08,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.75,
            stroke_opacity=0,
        )
        background.move_to(self.visual.stats_box_center)

        content.move_to(background.get_center())
        content.align_to(background, LEFT)
        content.align_to(background, UP)
        content.shift(RIGHT * 0.15 + DOWN * 0.13)

        background.set_z_index(20)
        content.set_z_index(21)

        return VGroup(background, content)

    def random_info_box(self):
        content = VGroup(
            Text("Кожен кидок випадковий", font_size=28, color=WHITE),
            Text("випадкова позиція", font_size=22, color=WHITE),
            Text("випадковий кут", font_size=22, color=WHITE),
        )
        content.arrange(DOWN, buff=0.12)

        return self.center_box(content, min_width=4.8)

    def many_needle_batch(self, batch_spec):
        batch = VGroup()
        throw_specs = self.geometry.random_throw_specs(
            batch_spec.seed,
            batch_spec.count,
        )

        for throw_spec in throw_specs:
            needle, _, _ = self.needle(
                throw_spec.midpoint,
                throw_spec.angle,
                opacity=batch_spec.opacity,
            )
            batch.add(needle)

        return batch

    def aligned_formula_row(
        self,
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

    def aligned_value_row(
        self,
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


class BuffonNeedleExperimentScene(Scene):
    def construct(self):
        self.board = BoardConfig()
        self.visual = VisualConfig()
        self.experiment = ExperimentConfig()

        self.geometry = BuffonGeometry(self.board)
        self.factory = BuffonMobjectFactory(
            self.board,
            self.visual,
            self.geometry,
        )

        self.title = self.create_title()
        self.lines = self.factory.lines()
        self.distance_markers = self.factory.distance_markers()
        self.visible_needles = VGroup()

        self.visible_records = self.create_visible_records()
        self.many_batches = self.create_many_batches()

        self.play_title()
        self.play_floor_intro()
        self.play_parallel_lines()
        self.play_distance_markers()
        self.play_length_condition()

        counts = ExperimentCounts()
        stats = self.play_first_two_throws(counts)
        self.play_visible_throw_series(stats, counts)
        self.play_many_random_throws(stats)
        self.play_final_result()
        self.play_pi_tease(stats)

    def create_title(self):
        title = Text(
            "Експеримент з голкою Бюффона",
            font_size=self.visual.title_font_size,
        )
        title.to_edge(UP)

        return title

    def create_visible_records(self):
        records = []

        for index, throw_spec in enumerate(self.experiment.visible_throws):
            needle_color = self.visible_needle_color(index)
            needle, crosses, crossing_point = self.factory.needle(
                throw_spec.midpoint,
                throw_spec.angle,
                needle_color=needle_color,
            )

            record = NeedleRecord(
                needle=needle,
                crosses=crosses,
                crossing_point=crossing_point,
                midpoint=throw_spec.midpoint,
                angle=throw_spec.angle,
            )
            records.append(record)

        return records

    def visible_needle_color(self, index):
        if index < 2:
            return self.visual.neutral_needle_color

        return None

    def create_many_batches(self):
        return [
            self.factory.many_needle_batch(batch_spec)
            for batch_spec in self.experiment.batch_specs
        ]

    def play_title(self):
        self.play(Write(self.title), run_time=0.8)
        self.wait(0.3)

    def play_floor_intro(self):
        content = VGroup(
            Text("Нескінченна підлога", font_size=30, color=WHITE),
            Text(
                "рівновіддалені паралельні прямі",
                font_size=28,
                color=WHITE,
            ),
        )
        content.arrange(DOWN, buff=0.12)

        floor_intro_box = self.factory.center_box(content, min_width=6.4)

        self.play(FadeIn(floor_intro_box), run_time=0.55)
        self.wait(1.4)
        self.play(FadeOut(floor_intro_box), run_time=0.4)

    def play_parallel_lines(self):
        self.play(
            AnimationGroup(
                *[Create(line) for line in self.lines],
                lag_ratio=0,
            ),
            run_time=1.0,
        )
        self.wait(0.35)

    def play_distance_markers(self):
        self.play(
            AnimationGroup(
                *[Create(marker) for marker in self.distance_markers],
                lag_ratio=0,
            ),
            run_time=1.0,
        )
        self.wait(1.2)

    def play_length_condition(self):
        midpoint = LEFT * 0.6 + UP * 0.75
        angle = PI / 6

        sample_needle, _, _ = self.factory.needle(
            midpoint,
            angle,
            needle_color=self.visual.neutral_needle_color,
        )
        length_marker = self.factory.length_marker(midpoint, angle)
        condition_box = self.create_length_condition_box()

        self.play(
            FadeIn(sample_needle, shift=DOWN * 0.25),
            run_time=0.8,
        )
        self.play(
            FadeIn(length_marker),
            FadeIn(condition_box),
            run_time=0.65,
        )
        self.wait(1.7)

        self.play(
            FadeOut(length_marker),
            FadeOut(condition_box),
            FadeOut(sample_needle),
            FadeOut(self.distance_markers),
            run_time=0.55,
        )
        self.wait(0.25)

    def create_length_condition_box(self):
        content = VGroup(
            Text("У цьому експерименті:", font_size=25, color=WHITE),
            MathTex("l", "=", "d", font_size=40, color=WHITE),
        )
        content.arrange(DOWN, buff=0.10)

        return self.factory.center_box(content, min_width=3.9)

    def play_first_two_throws(self, counts):
        first_record = self.visible_records[0]
        self.play_random_throw(first_record, show_info_text=True)
        self.show_throw_result(first_record)
        self.register_visible_throw(first_record, counts)

        second_record = self.visible_records[1]
        self.play_random_throw(second_record, show_info_text=False)
        self.show_throw_result(second_record)
        self.register_visible_throw(second_record, counts)

        stats = self.factory.stats_box(counts.total, counts.crossing)

        self.play(FadeIn(stats), run_time=0.65)
        self.wait(0.55)

        return stats

    def play_random_throw(self, record, show_info_text=False):
        info_box = self.optional_random_info_box(show_info_text)
        dot = self.play_random_position(record.midpoint)
        preview = self.play_random_angle_preview(dot, record)

        record.needle.set_z_index(12)
        animations = [ReplacementTransform(preview, record.needle)]

        if info_box is not None:
            animations.append(FadeOut(info_box))

        self.play(*animations, run_time=0.42)

    def optional_random_info_box(self, show_info_text):
        if not show_info_text:
            return None

        info_box = self.factory.random_info_box()

        self.play(FadeIn(info_box), run_time=0.45)
        self.wait(1.25)

        return info_box

    def play_random_position(self, final_midpoint):
        position_points = [
            LEFT * 4.6 + UP * 0.4,
            RIGHT * 2.8 + DOWN * 1.1,
            LEFT * 1.3 + DOWN * 2.0,
            final_midpoint,
        ]

        dot = Dot(position_points[0], radius=0.06, color=YELLOW)
        dot.set_z_index(25)

        self.play(FadeIn(dot), run_time=0.35)

        for point in position_points[1:]:
            self.play(dot.animate.move_to(point), run_time=0.72)

        self.wait(0.20)

        return dot

    def play_random_angle_preview(self, dot, record):
        start_angle = 0
        preview, _, _ = self.factory.needle(
            record.midpoint,
            start_angle,
            needle_color=self.visual.neutral_needle_color,
            opacity=0.75,
        )
        preview.set_z_index(12)

        self.play(
            FadeOut(dot),
            FadeIn(preview),
            run_time=0.35,
        )

        self.rotate_preview_to_final_angle(
            preview,
            record.midpoint,
            record.angle,
        )

        return preview

    def rotate_preview_to_final_angle(self, preview, midpoint, final_angle):
        current_angle = 0
        angle_sequence = [PI / 3, -PI / 5, final_angle]

        for target_angle in angle_sequence:
            self.play(
                Rotate(
                    preview,
                    angle=target_angle - current_angle,
                    about_point=midpoint,
                ),
                run_time=0.72,
            )
            current_angle = target_angle

    def show_throw_result(self, record):
        result_color = self.result_color(record.crosses)
        result_text = self.result_text(record.crosses)

        label = Text(result_text, font_size=28, color=result_color)
        label_box = self.factory.center_box(label, min_width=2.9)

        self.play(
            record.needle[1].animate.set_color(result_color),
            run_time=0.35,
        )
        self.play(FadeIn(label_box), run_time=0.35)

        if record.crosses:
            self.highlight_crossing_point(record.crossing_point)
        else:
            self.wait(0.8)

        self.play(FadeOut(label_box), run_time=0.3)

    def result_color(self, crosses):
        if crosses:
            return self.visual.crossing_color

        return self.visual.non_crossing_color

    def result_text(self, crosses):
        if crosses:
            return "є перетин"

        return "немає перетину"

    def highlight_crossing_point(self, crossing_point):
        point = Dot(
            crossing_point,
            radius=0.07,
            color=self.visual.intersection_color,
        )
        point.set_z_index(25)

        ring = Circle(
            radius=0.18,
            color=self.visual.intersection_color,
            stroke_width=3,
        )
        ring.move_to(crossing_point)
        ring.set_z_index(25)

        self.play(
            GrowFromCenter(point),
            Create(ring),
            run_time=0.4,
        )
        self.wait(0.65)

        self.play(
            Indicate(ring, color=self.visual.intersection_color),
            run_time=0.7,
        )
        self.play(
            FadeOut(point),
            FadeOut(ring),
            run_time=0.25,
        )

    def register_visible_throw(self, record, counts):
        self.visible_needles.add(record.needle)
        counts.add_throw(record.crosses)

    def play_visible_throw_series(self, stats, counts):
        for record in self.visible_records[2:]:
            self.play(
                FadeIn(record.needle, shift=DOWN * 0.20),
                run_time=self.visual.fast_drop_time,
            )

            self.register_visible_throw(record, counts)
            new_stats = self.factory.stats_box(
                counts.total,
                counts.crossing,
            )

            self.play(Transform(stats, new_stats), run_time=0.24)

        self.wait(0.4)

    def play_many_random_throws(self, stats):
        self.play_small_sample_note()
        self.play_repeat_note()

        for batch, batch_spec in zip(
            self.many_batches,
            self.experiment.batch_specs,
        ):
            self.play_many_batch(batch)
            self.update_stats_after_batch(stats, batch_spec)

    def play_small_sample_note(self):
        text = Text("Мала вибірка шумна.", font_size=30, color=WHITE)
        text_box = self.factory.center_box(text, min_width=4.8)

        self.play(FadeIn(text_box), run_time=0.45)
        self.wait(1.35)
        self.play(FadeOut(text_box), run_time=0.35)

    def play_repeat_note(self):
        text = Text(
            "Тепер повторимо випадково багато разів.",
            font_size=30,
            color=WHITE,
        )
        text_box = self.factory.center_box(text, min_width=6.1)

        self.play(FadeIn(text_box), run_time=0.45)
        self.wait(1.0)

        self.play(
            FadeOut(text_box),
            self.visible_needles.animate.set_opacity(0.36),
            run_time=0.55,
        )

    def play_many_batch(self, batch):
        self.play(
            AnimationGroup(
                *[
                    FadeIn(needle, shift=DOWN * 0.08)
                    for needle in batch
                ],
                lag_ratio=0.02,
            ),
            run_time=0.85,
        )

    def update_stats_after_batch(self, stats, batch_spec):
        new_stats = self.factory.stats_box(
            batch_spec.total_after,
            batch_spec.crossing_after,
        )

        self.play(Transform(stats, new_stats), run_time=0.65)
        self.bring_to_front(stats)
        self.wait(0.35)

    def play_final_result(self):
        final_result_box = self.create_final_result_box()

        self.play(FadeIn(final_result_box), run_time=0.6)
        self.wait(3.1)

        self.final_result_box = final_result_box

    def create_final_result_box(self):
        final_probability = (
            self.experiment.final_crossing_count
            / self.experiment.final_total_count
        )

        result = VGroup(
            Text(
                "Після багатьох випадкових кидків:",
                font_size=27,
                color=WHITE,
            ),
            MathTex(
                "N",
                "=",
                str(self.experiment.final_total_count),
                r"\qquad",
                "K",
                "=",
                str(self.experiment.final_crossing_count),
                font_size=34,
                color=WHITE,
            ),
            MathTex(
                r"P_{\mathrm{exp}}",
                "=",
                r"\frac{K}{N}",
                r"\approx",
                f"{self.factory.decimal_text(final_probability)}\\ldots",
                font_size=36,
                color=WHITE,
            ),
        )
        result[1][4].set_color(self.visual.crossing_color)
        result[1][6].set_color(self.visual.crossing_color)
        result.arrange(DOWN, buff=0.18)

        return self.factory.center_box(result, min_width=6.7)

    def play_pi_tease(self, stats):
        dim_layer = self.create_dim_layer()

        self.play(
            FadeOut(self.final_result_box),
            FadeIn(dim_layer),
            run_time=0.6,
        )

        row1, row2, row3, pi_row = self.create_pi_rows()
        self.write_pi_rows(row1, row2, row3, pi_row)
        self.highlight_matching_values(row3, pi_row)

        eq_start = self.transform_rows_to_pi_relation(
            row1,
            row2,
            row3,
            pi_row,
        )
        eq_mid = self.simplify_pi_relation(eq_start)
        eq_result = self.solve_for_probability(eq_mid)

        final_group = self.show_final_questions(eq_result)
        self.fade_out_everything(stats, dim_layer, final_group)

    def create_dim_layer(self):
        dim_layer = Rectangle(
            width=14.5,
            height=8.3,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=0.65,
            stroke_opacity=0,
        )
        dim_layer.set_z_index(40)

        return dim_layer

    def create_pi_rows(self):
        row1 = self.factory.aligned_formula_row(
            r"P_{\mathrm{exp}}",
            r"=\frac{K}{N}",
            r"\approx",
            r"0.63662\ldots",
            y=1.65,
        )
        row2 = self.factory.aligned_formula_row(
            r"\frac{1}{P_{\mathrm{exp}}}",
            r"=\frac{N}{K}",
            r"\approx",
            r"1.57079\ldots",
            y=0.55,
        )
        row3 = self.factory.aligned_formula_row(
            r"\frac{2}{P_{\mathrm{exp}}}",
            r"=\frac{2N}{K}",
            r"\approx",
            r"3.14159\ldots",
            y=-0.55,
        )
        pi_row = self.factory.aligned_value_row(
            r"\pi",
            r"\approx",
            r"3.14159\ldots",
            y=-1.65,
        )
        pi_row[0].set_color(RED)

        formula_rows = VGroup(row1, row2, row3, pi_row)
        formula_rows.move_to(ORIGIN)
        formula_rows.set_z_index(45)

        return row1, row2, row3, pi_row

    def write_pi_rows(self, *rows):
        for row in rows:
            self.play(Write(row), run_time=0.95)
            self.wait(0.55)

    def highlight_matching_values(self, row3, pi_row):
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

        self.value_highlights = VGroup(row3_highlight, pi_highlight)
        self.value_highlights.set_z_index(46)

        self.play(
            Create(row3_highlight),
            Create(pi_highlight),
            run_time=0.85,
        )
        self.wait(1.15)

    def transform_rows_to_pi_relation(self, row1, row2, row3, pi_row):
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
            FadeOut(self.value_highlights),
            ReplacementTransform(row3, eq_start),
            run_time=0.9,
        )
        self.wait(0.85)

        return eq_start

    def simplify_pi_relation(self, eq_start):
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

        return eq_mid

    def solve_for_probability(self, eq_mid):
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

        return eq_result

    def show_final_questions(self, eq_result):
        eq_result.generate_target()
        eq_result.target.move_to(UP * 0.75)

        left_question = self.create_left_final_question()
        right_question = self.create_right_final_question()
        proof_prompt = self.create_proof_prompt()

        final_group = VGroup(
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

        return final_group

    def create_left_final_question(self):
        question = VGroup(
            Text("Звідки тут", font_size=32, color=WHITE),
            MathTex(r"\pi", font_size=40, color=RED),
            Text("?", font_size=32, color=WHITE),
        )
        question.arrange(RIGHT, buff=0.12)
        question.move_to(LEFT * 2.85 + DOWN * 0.75)
        question.set_z_index(48)

        return question

    def create_right_final_question(self):
        question = VGroup(
            Text("А якщо", font_size=32, color=WHITE),
            MathTex("l", "<", "d", font_size=40, color=WHITE),
            Text("?", font_size=32, color=WHITE),
        )
        question.arrange(RIGHT, buff=0.12)
        question.move_to(RIGHT * 2.85 + DOWN * 0.75)
        question.set_z_index(48)

        return question

    def create_proof_prompt(self):
        proof_prompt = Text(
            "Тепер потрібне доведення.",
            font_size=34,
            color=WHITE,
        )
        proof_prompt.move_to(DOWN * 2.0)
        proof_prompt.set_z_index(48)

        return proof_prompt

    def fade_out_everything(self, stats, dim_layer, final_group):
        self.play(
            FadeOut(final_group),
            FadeOut(dim_layer),
            FadeOut(stats),
            FadeOut(self.visible_needles),
            *[FadeOut(batch) for batch in self.many_batches],
            FadeOut(self.lines),
            FadeOut(self.title),
            run_time=0.85,
        )
        self.wait(0.4)
