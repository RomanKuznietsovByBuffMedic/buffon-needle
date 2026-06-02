"""Manim-сцена для експерименту з голкою Бюффона.

Файл один: так простіше швидко доробляти відео.

Рівні:
1. Tune-класи — тексти, розміри, паузи, координати.
2. Data objects — прості дані експерименту.
3. BuffonGeometry — геометрія.
4. BuffonMobjectFactory — створення Manim-об'єктів.
5. BuffonNeedleExperimentScene — режисура сцени.

Правило: спочатку змінюй тільки Tune-класи.
"""

from dataclasses import dataclass
from dataclasses import field
import math
import random

from manim import *


# ============================================================================
# ЗОНА НАЛАШТУВАНЬ
# ============================================================================
# Спочатку змінюй тільки цей блок.
# Один параметр — одне природне місце зміни.
#
# КАРТА НАЛАШТУВАНЬ
# BoardTune              — прямі, відстань d, довжина голки l
# GlobalStyleTune        — кольори, товщини, рамки
# TitleTune              — головна назва
# FloorIntroTune         — вступ: "нескінченна підлога..."
# LinesTune              — поява паралельних прямих
# DistanceMarkersTune    — стрілки й підпис d
# LengthConditionTune    — голка, l, d, l = d
# ResultTune             — підписи результату
# RandomThrowTune        — випадкова позиція та кут
# StatsTune              — правий блок N, K, P_exp
# VisibleThrowsTune      — перші видимі кидки
# ManyThrowsTune         — багато випадкових кидків
# FinalResultTune        — фінальний числовий результат
# PiTableTune            — таблиця P, 1/P, 2/P, π
# PiTeaseTune            — фінальна формула і питання
# ExperimentTune         — кидки, batches, фінальні N і K
#
# БЕЗПЕЧНО ЗМІНЮВАТИ
# - тексти;
# - font_size / *_size;
# - wait_after / *_wait;
# - *_time;
# - позиції на кшталт LEFT * 2 + UP * 1;
# - кольори;
# - кількість видимих кидків і batch-кидків.
#
# ОБЕРЕЖНО ЗМІНЮВАТИ
# - line_spacing, line_count, line_length;
# - random_x_range, random_y_range, random_angle_range;
# - final_total_count, final_crossing_count.
#
# НЕ ЧІПАТИ БЕЗ ПОТРЕБИ
# - BuffonGeometry.crossing_data_from_endpoints;
# - BuffonGeometry._crossing_point;
# - TransformMatchingTex-послідовності у блоці з π.
# ============================================================================


@dataclass(frozen=True)
class BoardTune:
    """Геометрія дошки.

    Прямі, відстань між ними й довжина голки.
    """

    line_spacing: float = 1.5
    line_count: int = 5
    line_length: float = 12.0

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
class GlobalStyleTune:
    """Загальні кольори й візуальні сталі."""

    line_color: object = BLUE
    neutral_needle_color: object = WHITE
    crossing_color: object = GREEN
    non_crossing_color: object = RED
    needle_outline_color: object = GRAY
    intersection_color: object = YELLOW
    pi_color: object = RED

    text_box_fill_opacity: float = 0.8
    text_box_corner_radius: float = 0.1
    text_box_buff: float = 0.3

    needle_width: int = 4
    needle_outline_width: int = 6


@dataclass(frozen=True)
class TitleTune:
    text: str = "Експеримент з голкою Бюффона"
    font_size: int = 36
    write_time: float = 1.6
    wait_after: float = 0.8


@dataclass(frozen=True)
class FloorIntroTune:
    title: str = "Нескінченна підлога, на якій"
    subtitle: str = "рівновіддалені паралельні прямі"
    title_size: int = 30
    subtitle_size: int = 30
    line_gap: float = 0.15
    box_min_width: float = 6.5
    fade_in_time: float = 0.75
    wait_after: float = 1.5
    fade_out_time: float = 0.5


@dataclass(frozen=True)
class LinesTune:
    create_time: float = 1.00
    wait_after: float = 0.5


@dataclass(frozen=True)
class DistanceMarkersTune:
    marker_xs: tuple = (-5.45, 5.45)
    arrow_buff: float = 0.1
    arrow_width: float = 2
    arrow_tip_ratio: float = 0.15
    label_tex: str = r"d"
    label_size: int = 30
    label_buff: float = 0.1
    create_time: float = 1
    wait_after: float = 1.5


@dataclass(frozen=True)
class LengthConditionTune:
    """Фрагмент про умову l = d.

    Зразкова голка вертикальна.
    Її довжина дорівнює відстані між прямими.
    Тому вона вміщується між сусідніми прямими.
    """

    font_size: int = 30

    # Прямі впорядковані знизу вгору.
    # між другою прямою зверху і верхньою прямою.
    line_pair_indexes: tuple = (-2, -1)
    needle_x: float = 0.00
    needle_fade_shift: object = field(
        default_factory=lambda: DOWN * 0.25,
    )

    needle_label_tex: str = r"l"
    needle_label_font_size: int = 34
    needle_label_buff: float = 0.2

    condition_title: str = "У цьому експерименті:"
    distance_text: str = "• відстань між сусідніми прямими"
    distance_label_tex: str = r"d"
    needle_text: str = "• довжина голки"
    needle_length_tex: str = r"l"
    condition_equation_tex: str = r"l = d"

    condition_math_font_size: int = 34
    condition_math_gap: float = 0.12
    condition_line_gap: float = 0.2
    condition_box_width: float = 8.7

    needle_fade_in_time: float = 1
    info_fade_in_time: float = 0.5
    wait_after: float = 2.5
    fade_out_time: float = 0.75
    pause_after: float = 0.5


@dataclass(frozen=True)
class ResultTune:
    crossing_text: str = "є перетин"
    no_crossing_text: str = "немає перетину"
    label_size: int = 30
    label_box_width: float = 3

    point_radius: float = 0.1
    ring_radius: float = 0.3
    ring_width: int = 3

    recolor_time: float = 0.5
    label_fade_in_time: float = 0.5
    marker_create_time: float = 0.5
    marker_wait: float = 0.5
    marker_indicate_time: float = 1
    marker_fade_out_time: float = 0.5
    no_crossing_wait: float = 1
    label_fade_out_time: float = 0.5


@dataclass(frozen=True)
class RandomThrowTune:
    info_title: str = "Кожен кидок випадковий:"
    info_position_text: str = "• випадковий центр"
    info_angle_text: str = "• випадковий кут"
    info_title_size: int = 30
    info_detail_size: int = 30
    info_gap: float = 0.2
    info_box_width: float = 5
    info_fade_in_time: float = 0.5
    info_wait: float = 1

    dot_radius: float = 0.1
    dot_color: object = WHITE
    dot_path_points: tuple = field(
        default_factory=lambda: (
            LEFT * 4.60 + UP * 0.40,
            RIGHT * 2.80 + DOWN * 1.10,
            LEFT * 1.30 + DOWN * 2.00,
        ),
    )
    dot_fade_in_time: float = 0.5
    dot_move_time: float = 1
    dot_wait: float = 0.5

    preview_opacity: float = 0.75
    preview_fade_time: float = 0.5
    angle_sequence: tuple = (PI / 3, -PI / 5)
    angle_rotate_time: float = 1
    replace_time: float = 0.5


@dataclass(frozen=True)
class StatsTune:
    title: str = "Експеримент"
    total_tex: str = "N"
    crossing_tex: str = "K"
    probability_tex: str = r"P_{\mathrm{exp}}"
    title_size: int = 30
    count_size: int = 30
    probability_size: int = 30

    box_width: float = 3.5
    box_height: float = 2
    box_center: object = field(
        default_factory=lambda: RIGHT * 4.5 + UP * 1.8,
    )
    box_opacity: float = 0.75
    content_gap: float = 0.1
    content_shift: object = field(
        default_factory=lambda: RIGHT * 0.2 + DOWN * 0.15,
    )

    fade_in_time: float = 0.5
    wait_after: float = 0.5
    update_time: float = 0.5

@dataclass(frozen=True)
class VisibleThrowsTune:
    fade_in_shift: object = field(default_factory=lambda: DOWN * 0.20)
    fade_in_time: float = 0.5
    wait_after_all: float = 0.5

    small_sample_text: str = "Мала вибірка дає нестабільний результат."
    small_sample_size: int = 30
    small_sample_box_width: float = 6.5
    small_sample_fade_in_time: float = 0.5
    small_sample_wait: float = 1.5
    small_sample_fade_out_time: float = 0.5


@dataclass(frozen=True)
class ManyThrowsTune:
    repeat_text: str = (
        "Тепер повторимо експеримент "
        "багато разів."
    )
    repeat_text_size: int = 30
    repeat_box_width: float = 6
    repeat_fade_in_time: float = 0.5
    repeat_wait: float = 1.5

    old_needles_opacity: float = 0.36
    old_needles_dim_time: float = 0.55
    batch_fade_shift: object = field(default_factory=lambda: DOWN * 0.08)
    batch_fade_in_time: float = 0.85
    batch_lag_ratio: float = 0.02
    batch_stats_update_time: float = 0.65
    batch_wait: float = 0.35


@dataclass(frozen=True)
class FinalResultTune:
    title: str = "Після багатьох випадкових кидків:"
    title_size: int = 27
    count_size: int = 34
    probability_size: int = 36
    box_width: float = 6.70
    content_gap: float = 0.18
    fade_in_time: float = 0.60
    wait_after: float = 3.10


@dataclass(frozen=True)
class FormulaRowTune:
    left_tex: str
    middle_tex: str
    sign_tex: str
    value_tex: str
    y: float


@dataclass(frozen=True)
class PiTableTune:
    row_1: FormulaRowTune = FormulaRowTune(
        r"P_{\mathrm{exp}}",
        r"=\frac{K}{N}",
        r"\approx",
        r"0.63662\ldots",
        1.65,
    )
    row_2: FormulaRowTune = FormulaRowTune(
        r"\frac{1}{P_{\mathrm{exp}}}",
        r"=\frac{N}{K}",
        r"\approx",
        r"1.57079\ldots",
        0.55,
    )
    row_3: FormulaRowTune = FormulaRowTune(
        r"\frac{2}{P_{\mathrm{exp}}}",
        r"=\frac{2N}{K}",
        r"\approx",
        r"3.14159\ldots",
        -0.55,
    )
    pi_left_tex: str = r"\pi"
    pi_sign_tex: str = r"\approx"
    pi_value_tex: str = r"3.14159\ldots"
    pi_y: float = -1.65

    font_size: int = 34
    sign_x: float = 1.55
    middle_buff: float = 0.26
    left_buff: float = 0.28
    value_buff: float = 0.22
    center: object = field(default_factory=lambda: ORIGIN)

    write_time: float = 2
    wait_after_row: float = 1

    highlight_buff: float = 0.10
    highlight_width: int = 3
    highlight_create_time: float = 0.85
    highlight_wait: float = 1.15


@dataclass(frozen=True)
class PiTeaseTune:
    dim_opacity: float = 0.65
    dim_fade_in_time: float = 0.60

    start_equation_parts: tuple = (
        r"\frac{2}{P_{\mathrm{exp}}}",
        "=",
        r"\frac{2N}{K}",
        r"\approx",
        r"\pi",
    )
    middle_equation_parts: tuple = (
        r"\frac{2}{P_{\mathrm{exp}}}",
        r"\approx",
        r"\pi",
    )
    result_equation_parts: tuple = (
        r"P_{\mathrm{exp}}",
        r"\approx",
        r"\frac{2}{",
        r"\pi",
        "}",
    )
    equation_pos: object = field(default_factory=lambda: UP * 0.85)
    equation_target_pos: object = field(default_factory=lambda: UP * 0.75)
    large_formula_size: int = 44
    middle_formula_size: int = 46
    result_formula_size: int = 50
    transform_time: float = 0.90
    equation_wait: float = 0.85
    middle_equation_wait: float = 0.75
    result_equation_wait: float = 0.90

    left_question_text_1: str = "Звідки тут"
    left_question_tex: str = r"\pi"
    left_question_text_2: str = "?"
    left_question_pos: object = field(
        default_factory=lambda: LEFT * 2.85 + DOWN * 0.75,
    )

    right_question_text_1: str = "А якщо"
    right_question_tex_parts: tuple = ("l", "<", "d")
    right_question_text_2: str = "?"
    right_question_pos: object = field(
        default_factory=lambda: RIGHT * 2.85 + DOWN * 0.75,
    )

    question_text_size: int = 32
    question_tex_size: int = 40
    question_gap: float = 0.12
    proof_text: str = "Тепер потрібне доведення."
    proof_text_size: int = 34
    proof_pos: object = field(default_factory=lambda: DOWN * 2.00)

    questions_fade_in_time: float = 0.85
    questions_wait: float = 2.60
    final_fade_out_time: float = 0.85
    end_wait: float = 0.40


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


@dataclass(frozen=True)
class ExperimentTune:
    final_total_count: int = 50_000
    final_crossing_count: int = 31_831

    random_x_range: tuple = (-5.25, 5.15)
    random_y_range: tuple = (-2.55, 2.55)
    random_angle_range: tuple = (-PI / 2.15, PI / 2.15)

    visible_throws: tuple = field(
        default_factory=lambda: (
            ThrowSpec(LEFT * 4.30 + UP * 2.23, PI / 10),
            ThrowSpec(LEFT * 2.20 + UP * 1.25, -PI / 2.7),
            ThrowSpec(RIGHT * 0.50 + DOWN * 0.35, PI / 4.0),
            ThrowSpec(RIGHT * 3.20 + UP * 0.25, -PI / 3.0),
            ThrowSpec(LEFT * 4.70 + DOWN * 1.15, PI / 8.0),
            ThrowSpec(RIGHT * 2.00 + DOWN * 2.18, -PI / 6.0),
            ThrowSpec(LEFT * 0.70 + UP * 2.62, PI / 2.9),
            ThrowSpec(RIGHT * 4.60 + DOWN * 0.55, -PI / 5.5),
            ThrowSpec(LEFT * 3.30 + DOWN * 2.30, PI / 3.6),
            ThrowSpec(RIGHT * 0.10 + UP * 0.28, -PI / 8.0),
            ThrowSpec(LEFT * 1.60 + DOWN * 0.90, PI / 2.8),
            ThrowSpec(RIGHT * 1 + UP * 2, -PI / 7.0),
        ),
    )

    batch_specs: tuple = field(
        default_factory=lambda: (
            BatchSpec(11, 14, 0.21, 100, 64),
            BatchSpec(22, 16, 0.19, 1_000, 637),
            BatchSpec(33, 18, 0.17, 5_000, 3_183),
            BatchSpec(44, 22, 0.15, 50_000, 31_831),
        ),
    )


@dataclass(frozen=True)
class SceneTune:
    board: BoardTune = field(default_factory=BoardTune)
    style: GlobalStyleTune = field(default_factory=GlobalStyleTune)
    title: TitleTune = field(default_factory=TitleTune)
    floor: FloorIntroTune = field(default_factory=FloorIntroTune)
    lines: LinesTune = field(default_factory=LinesTune)
    distance: DistanceMarkersTune = field(
        default_factory=DistanceMarkersTune,
    )
    length: LengthConditionTune = field(
        default_factory=LengthConditionTune,
    )
    random_throw: RandomThrowTune = field(default_factory=RandomThrowTune)
    result: ResultTune = field(default_factory=ResultTune)
    stats: StatsTune = field(default_factory=StatsTune)
    visible: VisibleThrowsTune = field(default_factory=VisibleThrowsTune)
    many: ManyThrowsTune = field(default_factory=ManyThrowsTune)
    final: FinalResultTune = field(default_factory=FinalResultTune)
    pi_table: PiTableTune = field(default_factory=PiTableTune)
    pi_tease: PiTeaseTune = field(default_factory=PiTeaseTune)
    experiment: ExperimentTune = field(default_factory=ExperimentTune)


# ============================================================================
# DATA OBJECTS
# ============================================================================


@dataclass
class ExperimentCounts:
    total: int = 0
    crossing: int = 0

    def add_throw(self, crosses):
        self.total += 1

        if crosses:
            self.crossing += 1


@dataclass(frozen=True)
class NeedleRecord:
    needle: object
    crosses: bool
    crossing_point: object
    midpoint: object
    angle: float


# ============================================================================
# GEOMETRY
# ============================================================================


class BuffonGeometry:
    """Геометрія: прямі, кінці голки, перетини."""

    HORIZONTAL_EPSILON = 1e-9

    def __init__(self, board):
        self.board = board
        self._line_ys = self._create_line_ys()

    def line_ys(self):
        return self._line_ys

    def needle_endpoints(self, midpoint, angle):
        direction = self._needle_direction(angle)
        half_length = self.board.half_needle_length

        start = midpoint - half_length * direction
        end = midpoint + half_length * direction

        return start, end

    def crossing_data_from_endpoints(self, start, end):
        y_start = start[1]
        y_end = end[1]

        if self._is_horizontal(y_start, y_end):
            return False, None

        lower_y = min(y_start, y_end)
        upper_y = max(y_start, y_end)

        for line_y in self._line_ys:
            if self._contains_line_y(lower_y, line_y, upper_y):
                point = self._crossing_point(start, end, line_y)

                return True, point

        return False, None

    def random_throw_specs(
        self,
        seed,
        count,
        x_range,
        y_range,
        angle_range,
    ):
        rng = random.Random(seed)

        return tuple(
            self._random_throw_spec(
                rng,
                x_range,
                y_range,
                angle_range,
            )
            for _ in range(count)
        )

    def _create_line_ys(self):
        offset = self.board.center_offset
        spacing = self.board.line_spacing

        return tuple(
            (index - offset) * spacing
            for index in range(self.board.line_count)
        )

    def _needle_direction(self, angle):
        x_part = RIGHT * math.cos(angle)
        y_part = UP * math.sin(angle)

        return x_part + y_part

    def _is_horizontal(self, y_start, y_end):
        return abs(y_end - y_start) < self.HORIZONTAL_EPSILON

    def _contains_line_y(self, lower_y, line_y, upper_y):
        return lower_y <= line_y <= upper_y

    def _crossing_point(self, start, end, line_y):
        t = self._vertical_position_ratio(start, end, line_y)
        x = self._interpolate_x(start, end, t)

        return RIGHT * x + UP * line_y

    def _vertical_position_ratio(self, start, end, line_y):
        return (line_y - start[1]) / (end[1] - start[1])

    def _interpolate_x(self, start, end, t):
        return start[0] + t * (end[0] - start[0])

    def _random_throw_spec(
        self,
        rng,
        x_range,
        y_range,
        angle_range,
    ):
        midpoint = self._random_midpoint(rng, x_range, y_range)
        angle = self._random_angle(rng, angle_range)

        return ThrowSpec(midpoint, angle)

    def _random_midpoint(self, rng, x_range, y_range):
        x = rng.uniform(*x_range)
        y = rng.uniform(*y_range)

        return RIGHT * x + UP * y

    def _random_angle(self, rng, angle_range):
        return rng.uniform(*angle_range)


# ============================================================================
# MOBJECT FACTORY
# ============================================================================


class BuffonMobjectFactory:
    """Створює Manim-об’єкти."""

    def __init__(self, board, style, geometry):
        self.board = board
        self.style = style
        self.geometry = geometry

    def decimal_text(self, value, digits=5):
        return f"{value:.{digits}f}".rstrip("0").rstrip(".")

    def center_box(self, content, min_width=0):
        content.move_to(ORIGIN)

        return self.text_box(content, min_width=min_width)

    def text_box(self, content, min_width=0, fill_opacity=None):
        opacity = self._box_opacity(fill_opacity)
        width = self._box_width(content, min_width)
        height = self._box_height(content)

        background = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=self.style.text_box_corner_radius,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=opacity,
            stroke_opacity=0,
        )
        background.move_to(content.get_center())

        box = VGroup(background, content)
        box.set_z_index(30)

        return box

    def lines(self):
        return VGroup(
            *[
                self._line_at_y(line_y)
                for line_y in self.geometry.line_ys()
            ],
        )

    def distance_markers(self, tune):
        markers = VGroup()
        line_ys = self.geometry.line_ys()

        for marker_x in tune.marker_xs:
            markers.add(
                *self._distance_markers_on_side(marker_x, line_ys, tune),
            )

        return markers

    def distance_marker(self, marker_x, lower_y, upper_y, tune):
        arrow = DoubleArrow(
            start=RIGHT * marker_x + UP * lower_y,
            end=RIGHT * marker_x + UP * upper_y,
            buff=tune.arrow_buff,
            color=WHITE,
            stroke_width=tune.arrow_width,
            max_tip_length_to_length_ratio=tune.arrow_tip_ratio,
        )

        label = MathTex(
            tune.label_tex,
            font_size=tune.label_size,
            color=WHITE,
        )
        label.next_to(
            arrow,
            self._label_side(marker_x),
            buff=tune.label_buff,
        )

        return VGroup(arrow, label)

    def needle(self, midpoint, angle, needle_color=None, opacity=1.0):
        start, end = self.geometry.needle_endpoints(midpoint, angle)
        crosses, crossing_point = self.geometry.crossing_data_from_endpoints(
            start,
            end,
        )
        color = self._resolved_needle_color(needle_color, crosses)

        needle = VGroup(
            self._needle_outline(start, end, opacity),
            self._needle_inner(start, end, color, opacity),
        )

        return needle, crosses, crossing_point

    def stats_box(self, total_count, crossing_count, tune):
        content = self._stats_content(total_count, crossing_count, tune)
        background = self._stats_background(tune)

        self._position_stats_content(content, background, tune)

        return VGroup(background, content)

    def intersection_marker(self, crossing_point, tune):
        point = Dot(
            crossing_point,
            radius=tune.point_radius,
            color=self.style.intersection_color,
        )
        ring = Circle(
            radius=tune.ring_radius,
            color=self.style.intersection_color,
            stroke_width=tune.ring_width,
        )
        ring.move_to(crossing_point)

        marker = VGroup(point, ring)
        marker.set_z_index(25)

        return marker

    def dim_layer(self, opacity):
        layer = Rectangle(
            width=14.5,
            height=8.3,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=opacity,
            stroke_opacity=0,
        )
        layer.set_z_index(40)

        return layer

    def aligned_formula_row(self, row_tune, table_tune):
        left = self._formula_part(row_tune.left_tex, table_tune.font_size)
        middle = self._formula_part(
            row_tune.middle_tex,
            table_tune.font_size,
        )
        sign = self._formula_part(row_tune.sign_tex, table_tune.font_size)
        value = self._formula_part(row_tune.value_tex, table_tune.font_size)

        self._arrange_formula_row(
            left,
            middle,
            sign,
            value,
            row_tune.y,
            table_tune,
        )

        row = VGroup(left, middle, sign, value)
        row.value_part = value

        return row

    def aligned_value_row(self, table_tune):
        left = self._formula_part(
            table_tune.pi_left_tex,
            table_tune.font_size,
        )
        sign = self._formula_part(
            table_tune.pi_sign_tex,
            table_tune.font_size,
        )
        value = self._formula_part(
            table_tune.pi_value_tex,
            table_tune.font_size,
        )

        sign.move_to(RIGHT * table_tune.sign_x + UP * table_tune.pi_y)
        left.next_to(sign, LEFT, buff=table_tune.left_buff)
        value.next_to(sign, RIGHT, buff=table_tune.value_buff)
        left.set_color(self.style.pi_color)

        row = VGroup(left, sign, value)
        row.value_part = value

        return row

    def _box_opacity(self, fill_opacity):
        if fill_opacity is None:
            return self.style.text_box_fill_opacity

        return fill_opacity

    def _box_width(self, content, min_width):
        width = content.width + 2 * self.style.text_box_buff

        return max(width, min_width)

    def _box_height(self, content):
        return content.height + 2 * self.style.text_box_buff

    def _line_at_y(self, line_y):
        return Line(
            start=LEFT * self.board.half_line_length + UP * line_y,
            end=RIGHT * self.board.half_line_length + UP * line_y,
            color=self.style.line_color,
        )

    def _distance_markers_on_side(self, marker_x, line_ys, tune):
        return [
            self.distance_marker(marker_x, lower_y, upper_y, tune)
            for lower_y, upper_y in zip(line_ys[:-1], line_ys[1:])
        ]

    def _label_side(self, marker_x):
        if marker_x < 0:
            return LEFT

        return RIGHT

    def _resolved_needle_color(self, needle_color, crosses):
        if needle_color is not None:
            return needle_color

        if crosses:
            return self.style.crossing_color

        return self.style.non_crossing_color

    def _needle_outline(self, start, end, opacity):
        line = Line(
            start=start,
            end=end,
            color=self.style.needle_outline_color,
            stroke_width=self.style.needle_outline_width,
        )
        line.set_opacity(opacity)

        return line

    def _needle_inner(self, start, end, color, opacity):
        line = Line(
            start=start,
            end=end,
            color=color,
            stroke_width=self.style.needle_width,
        )
        line.set_opacity(opacity)

        return line

    def _stats_content(self, total_count, crossing_count, tune):
        probability_text = self._probability_text(total_count, crossing_count)

        title = Text(tune.title, font_size=tune.title_size)
        total_row = self._count_row(tune.total_tex, total_count, tune)
        crossing_row = self._count_row(
            tune.crossing_tex,
            crossing_count,
            tune,
        )
        probability_row = self._probability_row(probability_text, tune)

        crossing_row[0].set_color(self.style.crossing_color)
        crossing_row[2].set_color(self.style.crossing_color)
        probability_row[3].set_color(self.style.crossing_color)

        content = VGroup(title, total_row, crossing_row, probability_row)
        content.arrange(DOWN, aligned_edge=LEFT, buff=tune.content_gap)
        content.set_z_index(21)

        return content

    def _probability_text(self, total_count, crossing_count):
        if total_count == 0:
            return "0"

        probability = crossing_count / total_count

        return self.decimal_text(probability, digits=5)

    def _count_row(self, label_tex, count, tune):
        return MathTex(
            label_tex,
            "=",
            str(count),
            font_size=tune.count_size,
            color=WHITE,
        )

    def _probability_row(self, probability_text, tune):
        return MathTex(
            tune.probability_tex,
            r"\approx",
            r"\frac{",
            tune.crossing_tex,
            r"}{",
            tune.total_tex,
            r"}",
            "=",
            probability_text,
            font_size=tune.probability_size,
            color=WHITE,
        )

    def _stats_background(self, tune):
        background = RoundedRectangle(
            width=tune.box_width,
            height=tune.box_height,
            corner_radius=self.style.text_box_corner_radius,
            color=BLACK,
            fill_color=BLACK,
            fill_opacity=tune.box_opacity,
            stroke_opacity=0,
        )
        background.move_to(tune.box_center)
        background.set_z_index(20)

        return background

    def _position_stats_content(self, content, background, tune):
        content.move_to(background.get_center())
        content.align_to(background, LEFT)
        content.align_to(background, UP)
        content.shift(tune.content_shift)

    def _formula_part(self, tex, font_size):
        return MathTex(tex, font_size=font_size, color=WHITE)

    def _arrange_formula_row(
        self,
        left,
        middle,
        sign,
        value,
        y,
        table_tune,
    ):
        sign.move_to(RIGHT * table_tune.sign_x + UP * y)
        middle.next_to(sign, LEFT, buff=table_tune.middle_buff)
        left.next_to(middle, LEFT, buff=table_tune.left_buff)
        value.next_to(sign, RIGHT, buff=table_tune.value_buff)


# ============================================================================
# SCENE
# ============================================================================


class BuffonNeedleExperimentScene(Scene):
    def construct(self):
        # Construct — головний сценарний метод Manim.
        # Збираємо залежності та запускаємо відео.
        self.tune = SceneTune()
        self.board = self.tune.board
        self.style = self.tune.style
        self.geometry = BuffonGeometry(self.board)
        self.factory = BuffonMobjectFactory(
            self.board,
            self.style,
            self.geometry,
        )

        self.title = self.create_title()
        self.lines = self.factory.lines()
        self.distance_markers = self.factory.distance_markers(
            self.tune.distance,
        )
        self.visible_needles = VGroup()
        self.visible_records = self.create_visible_records()
        self.many_batches = self.create_many_batches()

        self.play_title()
        self.play_floor_intro()
        self.play_parallel_lines()
        self.play_distance_markers()
        self.play_length_condition()
        self.play_experiment()

    def play_experiment(self):
        # Основний експеримент: від кидків до π.
        # до появи π та запиту на доведення.
        counts = ExperimentCounts()
        stats = self.play_first_two_throws(counts)

        self.play_visible_throw_series(stats, counts)
        self.play_many_random_throws(stats)
        self.play_final_result()
        self.play_pi_hook(stats)

    def play_title(self):
        tune = self.tune.title

        self.play(Write(self.title), run_time=tune.write_time)
        self.wait(tune.wait_after)

    def play_floor_intro(self):
        tune = self.tune.floor
        box = self.create_floor_intro_box()

        self.play(FadeIn(box), run_time=tune.fade_in_time)
        self.wait(tune.wait_after)
        self.play(FadeOut(box), run_time=tune.fade_out_time)

    def play_parallel_lines(self):
        tune = self.tune.lines

        self.play(
            AnimationGroup(
                *[Create(line) for line in self.lines],
                lag_ratio=0,
            ),
            run_time=tune.create_time,
        )
        self.wait(tune.wait_after)

    def play_distance_markers(self):
        tune = self.tune.distance

        self.play(
            AnimationGroup(
                *[Create(marker) for marker in self.distance_markers],
                lag_ratio=0,
            ),
            run_time=tune.create_time,
        )
        self.wait(tune.wait_after)

    def play_length_condition(self):
        tune = self.tune.length
        sample_needle = self.create_length_condition_needle()
        needle_label = self.create_length_condition_label(sample_needle)
        condition_box = self.create_length_condition_box()

        self.play(
            FadeIn(sample_needle),
            FadeIn(needle_label),
            run_time=tune.needle_fade_in_time,
        )

        self.play(
            FadeIn(condition_box),
            run_time=tune.info_fade_in_time,
        )

        self.wait(tune.wait_after)

        self.play(
            FadeOut(needle_label),
            FadeOut(condition_box),
            FadeOut(sample_needle),
            FadeOut(self.distance_markers),
            run_time=tune.fade_out_time,
        )
        self.wait(tune.pause_after)

    def play_first_two_throws(self, counts):
        first_record = self.visible_records[0]
        second_record = self.visible_records[1]

        self.play_random_throw(first_record, show_info_text=True)
        self.show_result(first_record)
        counts.add_throw(first_record.crosses)

        self.play_random_throw(second_record, show_info_text=False)
        self.show_result(second_record)
        counts.add_throw(second_record.crosses)

        return self.show_initial_stats(counts)

    def play_visible_throw_series(self, stats, counts):
        tune = self.tune.visible

        for record in self.visible_records[2:]:
            self.show_fast_throw(record, counts, stats)

        self.wait(tune.wait_after_all)
        self.play_small_sample_message()

    def play_many_random_throws(self, stats):
        tune = self.tune.many
        repeat_box = self.create_repeat_box()

        self.play(FadeIn(repeat_box), run_time=tune.repeat_fade_in_time)
        self.wait(tune.repeat_wait)
        self.play(
            FadeOut(repeat_box),
            self.visible_needles.animate.set_opacity(
                tune.old_needles_opacity,
            ),
            run_time=tune.old_needles_dim_time,
        )
        self.play_batches(stats)

    def play_final_result(self):
        tune = self.tune.final
        final_box = self.create_final_result_box()

        self.play(FadeIn(final_box), run_time=tune.fade_in_time)
        self.wait(tune.wait_after)

        self.final_result_box = final_box

    def play_pi_hook(self, stats):
        tune = self.tune.pi_tease
        dim_layer = self.factory.dim_layer(tune.dim_opacity)

        self.play(
            FadeOut(self.final_result_box),
            FadeIn(dim_layer),
            run_time=tune.dim_fade_in_time,
        )

        rows = self.play_pi_table()
        eq_result = self.play_pi_equation_sequence(rows)
        final_group = self.play_final_questions(eq_result)

        self.wait(tune.questions_wait)
        self.play_scene_fade_out(final_group, dim_layer, stats)

    def create_title(self):
        tune = self.tune.title
        title = Text(tune.text, font_size=tune.font_size)
        title.to_edge(UP)

        return title

    def create_floor_intro_box(self):
        tune = self.tune.floor
        content = VGroup(
            Text(tune.title, font_size=tune.title_size, color=WHITE),
            Text(
                tune.subtitle,
                font_size=tune.subtitle_size,
                color=WHITE,
            ),
        )
        content.arrange(DOWN, buff=tune.line_gap)

        return self.factory.center_box(content, min_width=tune.box_min_width)

    def create_length_condition_needle(self):
        tune = self.tune.length
        midpoint = self.length_condition_midpoint()

        needle, _, _ = self.factory.needle(
            midpoint,
            PI / 2,
            needle_color=self.style.neutral_needle_color,
        )

        return needle

    def create_length_condition_label(self, needle):
        tune = self.tune.length
        label = MathTex(
            tune.needle_label_tex,
            font_size=tune.needle_label_font_size,
            color=WHITE,
        )
        label.next_to(
            needle,
            RIGHT,
            buff=tune.needle_label_buff,
        )

        return label

    def create_length_condition_box(self):
        tune = self.tune.length
        title = Text(
            tune.condition_title,
            font_size=tune.font_size,
            color=WHITE,
        )
        distance_row = self.create_text_math_row(
            tune.distance_text,
            tune.distance_label_tex,
            tune.font_size,
        )
        needle_row = self.create_text_math_row(
            tune.needle_text,
            tune.needle_length_tex,
            tune.font_size,
        )
        equation_row = self.create_text_math_row(
            "•",
            tune.condition_equation_tex,
            tune.font_size,
        )

        content = VGroup(
            title,
            distance_row,
            needle_row,
            equation_row,
        )
        content.arrange(
            DOWN,
            buff=tune.condition_line_gap,
        )

        return self.factory.center_box(
            content,
            min_width=tune.condition_box_width,
        )

    def create_text_math_row(self, text, tex, font_size):
        tune = self.tune.length
        text_part = Text(
            text,
            font_size=font_size,
            color=WHITE,
        )
        math_part = MathTex(
            tex,
            font_size=tune.condition_math_font_size,
            color=WHITE,
        )

        row = VGroup(text_part, math_part)
        row.arrange(RIGHT, buff=tune.condition_math_gap)

        return row

    def length_condition_midpoint(self):
        tune = self.tune.length
        lower_y, upper_y = self.length_condition_line_pair()
        middle_y = (lower_y + upper_y) / 2

        return RIGHT * tune.needle_x + UP * middle_y

    def length_condition_line_pair(self):
        tune = self.tune.length
        lower_index, upper_index = tune.line_pair_indexes
        line_ys = self.geometry.line_ys()

        return line_ys[lower_index], line_ys[upper_index]

    def create_visible_records(self):
        records = []

        for index, spec in enumerate(self.tune.experiment.visible_throws):
            needle, crosses, crossing_point = self.factory.needle(
                spec.midpoint,
                spec.angle,
                needle_color=self.visible_throw_color(index),
            )
            records.append(
                NeedleRecord(
                    needle=needle,
                    crosses=crosses,
                    crossing_point=crossing_point,
                    midpoint=spec.midpoint,
                    angle=spec.angle,
                ),
            )

        return tuple(records)

    def create_many_batches(self):
        return tuple(
            self.create_many_batch(batch_spec)
            for batch_spec in self.tune.experiment.batch_specs
        )

    def create_many_batch(self, batch_spec):
        batch = VGroup()
        throw_specs = self.geometry.random_throw_specs(
            batch_spec.seed,
            batch_spec.count,
            self.tune.experiment.random_x_range,
            self.tune.experiment.random_y_range,
            self.tune.experiment.random_angle_range,
        )

        for spec in throw_specs:
            needle, _, _ = self.factory.needle(
                spec.midpoint,
                spec.angle,
                opacity=batch_spec.opacity,
            )
            batch.add(needle)

        return batch

    def visible_throw_color(self, index):
        if index < 2:
            return self.style.neutral_needle_color

        return None

    def show_initial_stats(self, counts):
        tune = self.tune.stats
        stats = self.factory.stats_box(counts.total, counts.crossing, tune)

        self.play(FadeIn(stats), run_time=tune.fade_in_time)
        self.wait(tune.wait_after)

        return stats

    def show_fast_throw(self, record, counts, stats):
        tune = self.tune.visible

        self.play(
            FadeIn(record.needle, shift=tune.fade_in_shift),
            run_time=tune.fade_in_time,
        )
        self.visible_needles.add(record.needle)
        counts.add_throw(record.crosses)
        self.update_stats(stats, counts)

    def update_stats(self, stats, counts):
        tune = self.tune.stats
        new_stats = self.factory.stats_box(counts.total, counts.crossing, tune)

        self.play(Transform(stats, new_stats), run_time=tune.update_time)

    def play_random_throw(self, record, show_info_text=False):
        info_box = self.show_random_info_if_needed(show_info_text)

        self.play_random_position_dot(record.midpoint)
        preview = self.play_random_angle_preview(record.midpoint, record.angle)
        self.replace_preview_with_needle(preview, record, info_box)
        self.visible_needles.add(record.needle)

    def show_random_info_if_needed(self, show_info_text):
        if not show_info_text:
            return None

        tune = self.tune.random_throw
        info_box = self.create_random_info_box()

        self.play(FadeIn(info_box), run_time=tune.info_fade_in_time)
        self.wait(tune.info_wait)

        return info_box

    def create_random_info_box(self):
        tune = self.tune.random_throw
        content = VGroup(
            Text(tune.info_title, font_size=tune.info_title_size),
            Text(
                tune.info_position_text,
                font_size=tune.info_detail_size,
            ),
            Text(tune.info_angle_text, font_size=tune.info_detail_size),
        )
        content.set_color(WHITE)
        content.arrange(DOWN, buff=tune.info_gap)

        return self.factory.center_box(content, min_width=tune.info_box_width)

    def play_random_position_dot(self, final_midpoint):
        tune = self.tune.random_throw
        points = list(tune.dot_path_points) + [final_midpoint]
        dot = Dot(points[0], radius=tune.dot_radius, color=tune.dot_color)
        dot.set_z_index(25)

        self.play(FadeIn(dot), run_time=tune.dot_fade_in_time)

        for point in points[1:]:
            self.play(dot.animate.move_to(point), run_time=tune.dot_move_time)

        self.wait(tune.dot_wait)
        self.random_dot = dot

    def play_random_angle_preview(self, midpoint, final_angle):
        tune = self.tune.random_throw
        preview, _, _ = self.factory.needle(
            midpoint,
            0,
            needle_color=self.style.neutral_needle_color,
            opacity=tune.preview_opacity,
        )
        preview.set_z_index(12)

        self.play(
            FadeOut(self.random_dot),
            FadeIn(preview),
            run_time=tune.preview_fade_time,
        )
        self.rotate_preview_to_final_angle(preview, midpoint, final_angle)

        return preview

    def rotate_preview_to_final_angle(self, preview, midpoint, final_angle):
        tune = self.tune.random_throw
        current_angle = 0
        angle_sequence = list(tune.angle_sequence) + [final_angle]

        for target_angle in angle_sequence:
            self.play(
                Rotate(
                    preview,
                    angle=target_angle - current_angle,
                    about_point=midpoint,
                ),
                run_time=tune.angle_rotate_time,
            )
            current_angle = target_angle

    def replace_preview_with_needle(self, preview, record, info_box):
        tune = self.tune.random_throw
        record.needle.set_z_index(12)

        animations = [ReplacementTransform(preview, record.needle)]

        if info_box is not None:
            animations.append(FadeOut(info_box))

        self.play(*animations, run_time=tune.replace_time)

    def show_result(self, record):
        tune = self.tune.result
        result_color = self.result_color(record.crosses)
        label_box = self.create_result_label_box(record.crosses, result_color)

        self.play(
            record.needle[1].animate.set_color(result_color),
            run_time=tune.recolor_time,
        )
        self.play(FadeIn(label_box), run_time=tune.label_fade_in_time)

        if record.crosses:
            self.show_crossing_marker(record.crossing_point)
        else:
            self.wait(tune.no_crossing_wait)

        self.play(FadeOut(label_box), run_time=tune.label_fade_out_time)

    def create_result_label_box(self, crosses, color):
        tune = self.tune.result
        text = tune.crossing_text if crosses else tune.no_crossing_text
        label = Text(text, font_size=tune.label_size, color=color)

        return self.factory.center_box(label, min_width=tune.label_box_width)

    def show_crossing_marker(self, crossing_point):
        tune = self.tune.result
        marker = self.factory.intersection_marker(crossing_point, tune)
        point, ring = marker

        self.play(
            GrowFromCenter(point),
            Create(ring),
            run_time=tune.marker_create_time,
        )
        self.wait(tune.marker_wait)
        self.play(
            Indicate(ring, color=self.style.intersection_color),
            run_time=tune.marker_indicate_time,
        )
        self.play(
            FadeOut(point),
            FadeOut(ring),
            run_time=tune.marker_fade_out_time,
        )

    def play_small_sample_message(self):
        tune = self.tune.visible
        text = Text(
            tune.small_sample_text,
            font_size=tune.small_sample_size,
            color=WHITE,
        )
        box = self.factory.center_box(
            text,
            min_width=tune.small_sample_box_width,
        )

        self.play(FadeIn(box), run_time=tune.small_sample_fade_in_time)
        self.wait(tune.small_sample_wait)
        self.play(FadeOut(box), run_time=tune.small_sample_fade_out_time)

    def create_repeat_box(self):
        tune = self.tune.many
        text = Text(
            tune.repeat_text,
            font_size=tune.repeat_text_size,
            color=WHITE,
        )

        return self.factory.center_box(text, min_width=tune.repeat_box_width)

    def play_batches(self, stats):
        tune = self.tune.many

        for batch, batch_spec in zip(
            self.many_batches,
            self.tune.experiment.batch_specs,
        ):
            self.play(
                AnimationGroup(
                    *[
                        FadeIn(needle, shift=tune.batch_fade_shift)
                        for needle in batch
                    ],
                    lag_ratio=tune.batch_lag_ratio,
                ),
                run_time=tune.batch_fade_in_time,
            )
            self.update_stats_after_batch(stats, batch_spec)
            self.wait(tune.batch_wait)

    def update_stats_after_batch(self, stats, batch_spec):
        tune = self.tune.many
        stats_tune = self.tune.stats
        new_stats = self.factory.stats_box(
            batch_spec.total_after,
            batch_spec.crossing_after,
            stats_tune,
        )

        self.play(
            Transform(stats, new_stats),
            run_time=tune.batch_stats_update_time,
        )
        self.bring_to_front(stats)

    def create_final_result_box(self):
        tune = self.tune.final
        final_p_text = self.final_probability_text()
        content = VGroup(
            Text(tune.title, font_size=tune.title_size, color=WHITE),
            self.create_final_count_row(),
            self.create_final_probability_row(final_p_text),
        )
        content.arrange(DOWN, buff=tune.content_gap)

        return self.factory.center_box(content, min_width=tune.box_width)

    def create_final_count_row(self):
        exp = self.tune.experiment
        stats = self.tune.stats

        row = MathTex(
            stats.total_tex,
            "=",
            str(exp.final_total_count),
            r"\qquad",
            stats.crossing_tex,
            "=",
            str(exp.final_crossing_count),
            font_size=self.tune.final.count_size,
            color=WHITE,
        )
        row[4].set_color(self.style.crossing_color)
        row[6].set_color(self.style.crossing_color)

        return row

    def create_final_probability_row(self, final_p_text):
        stats = self.tune.stats

        return MathTex(
            stats.probability_tex,
            "=",
            r"\frac{K}{N}",
            r"\approx",
            f"{final_p_text}\\ldots",
            font_size=self.tune.final.probability_size,
            color=WHITE,
        )

    def play_pi_table(self):
        tune = self.tune.pi_table
        rows = self.create_pi_rows()

        for row in rows:
            self.play(Write(row), run_time=tune.write_time)
            self.wait(tune.wait_after_row)

        return rows

    def create_pi_rows(self):
        tune = self.tune.pi_table
        rows = VGroup(
            self.factory.aligned_formula_row(tune.row_1, tune),
            self.factory.aligned_formula_row(tune.row_2, tune),
            self.factory.aligned_formula_row(tune.row_3, tune),
            self.factory.aligned_value_row(tune),
        )
        rows.move_to(tune.center)
        rows.set_z_index(45)

        return rows

    def play_pi_equation_sequence(self, rows):
        row1, row2, row3, pi_row = rows
        highlights = self.create_pi_highlights(row3, pi_row)

        self.show_pi_highlights(highlights)
        eq_start = self.compress_pi_table(rows, row3, highlights)
        eq_mid = self.transform_to_middle_pi_equation(eq_start)

        return self.transform_to_probability_equation(eq_mid)

    def create_pi_highlights(self, row3, pi_row):
        tune = self.tune.pi_table
        row3_highlight = SurroundingRectangle(
            row3.value_part,
            color=YELLOW,
            buff=tune.highlight_buff,
            stroke_width=tune.highlight_width,
        )
        pi_highlight = SurroundingRectangle(
            pi_row.value_part,
            color=YELLOW,
            buff=tune.highlight_buff,
            stroke_width=tune.highlight_width,
        )
        highlights = VGroup(row3_highlight, pi_highlight)
        highlights.set_z_index(46)

        return highlights

    def show_pi_highlights(self, highlights):
        tune = self.tune.pi_table

        self.play(
            Create(highlights[0]),
            Create(highlights[1]),
            run_time=tune.highlight_create_time,
        )
        self.wait(tune.highlight_wait)

    def compress_pi_table(self, rows, row3, highlights):
        tune = self.tune.pi_tease
        row1, row2, _, pi_row = rows
        eq_start = self.create_pi_start_equation()

        self.play(
            FadeOut(row1),
            FadeOut(row2),
            FadeOut(pi_row),
            FadeOut(highlights),
            ReplacementTransform(row3, eq_start),
            run_time=tune.transform_time,
        )
        self.wait(tune.equation_wait)

        return eq_start

    def create_pi_start_equation(self):
        tune = self.tune.pi_tease
        equation = MathTex(
            *tune.start_equation_parts,
            font_size=tune.large_formula_size,
            color=WHITE,
        )
        equation[4].set_color(self.style.pi_color)
        equation.move_to(tune.equation_pos)
        equation.set_z_index(47)

        return equation

    def transform_to_middle_pi_equation(self, eq_start):
        tune = self.tune.pi_tease
        eq_mid = self.create_pi_middle_equation()

        self.play(
            TransformMatchingTex(eq_start, eq_mid),
            run_time=tune.transform_time,
        )
        self.wait(tune.middle_equation_wait)

        return eq_mid

    def create_pi_middle_equation(self):
        tune = self.tune.pi_tease
        equation = MathTex(
            *tune.middle_equation_parts,
            font_size=tune.middle_formula_size,
            color=WHITE,
        )
        equation[2].set_color(self.style.pi_color)
        equation.move_to(tune.equation_pos)
        equation.set_z_index(47)

        return equation

    def transform_to_probability_equation(self, eq_mid):
        tune = self.tune.pi_tease
        eq_result = self.create_probability_result_equation()

        self.play(
            TransformMatchingTex(eq_mid, eq_result),
            run_time=tune.transform_time,
        )
        self.wait(tune.result_equation_wait)

        return eq_result

    def create_probability_result_equation(self):
        tune = self.tune.pi_tease
        equation = MathTex(
            *tune.result_equation_parts,
            font_size=tune.result_formula_size,
            color=WHITE,
        )
        equation[3].set_color(self.style.pi_color)
        equation.move_to(tune.equation_pos)
        equation.set_z_index(47)

        return equation

    def play_final_questions(self, eq_result):
        tune = self.tune.pi_tease
        eq_result.generate_target()
        eq_result.target.move_to(tune.equation_target_pos)

        left_question = self.create_left_question()
        right_question = self.create_right_question()
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
            run_time=tune.questions_fade_in_time,
        )

        return final_group

    def create_left_question(self):
        tune = self.tune.pi_tease
        question = VGroup(
            Text(
                tune.left_question_text_1,
                font_size=tune.question_text_size,
                color=WHITE,
            ),
            MathTex(
                tune.left_question_tex,
                font_size=tune.question_tex_size,
                color=self.style.pi_color,
            ),
            Text(
                tune.left_question_text_2,
                font_size=tune.question_text_size,
                color=WHITE,
            ),
        )
        question.arrange(RIGHT, buff=tune.question_gap)
        question.move_to(tune.left_question_pos)
        question.set_z_index(48)

        return question

    def create_right_question(self):
        tune = self.tune.pi_tease
        question = VGroup(
            Text(
                tune.right_question_text_1,
                font_size=tune.question_text_size,
                color=WHITE,
            ),
            MathTex(
                *tune.right_question_tex_parts,
                font_size=tune.question_tex_size,
                color=WHITE,
            ),
            Text(
                tune.right_question_text_2,
                font_size=tune.question_text_size,
                color=WHITE,
            ),
        )
        question.arrange(RIGHT, buff=tune.question_gap)
        question.move_to(tune.right_question_pos)
        question.set_z_index(48)

        return question

    def create_proof_prompt(self):
        tune = self.tune.pi_tease
        prompt = Text(
            tune.proof_text,
            font_size=tune.proof_text_size,
            color=WHITE,
        )
        prompt.move_to(tune.proof_pos)
        prompt.set_z_index(48)

        return prompt

    def play_scene_fade_out(self, final_group, dim_layer, stats):
        tune = self.tune.pi_tease

        self.play(
            FadeOut(final_group),
            FadeOut(dim_layer),
            FadeOut(stats),
            FadeOut(self.visible_needles),
            *[FadeOut(batch) for batch in self.many_batches],
            FadeOut(self.lines),
            FadeOut(self.title),
            run_time=tune.final_fade_out_time,
        )
        self.wait(tune.end_wait)

    def result_color(self, crosses):
        if crosses:
            return self.style.crossing_color

        return self.style.non_crossing_color

    def final_probability(self):
        exp = self.tune.experiment

        return exp.final_crossing_count / exp.final_total_count

    def final_probability_text(self):
        return self.factory.decimal_text(self.final_probability(), digits=5)
