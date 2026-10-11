"""Build continuous timeline and Current Focus SVG layouts."""

from dataclasses import dataclass
from pathlib import Path
import re
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


@dataclass(frozen=True)
class Event:
    season_en: str
    year: str
    title_en: str
    title_zh: str
    body_en: str
    body_zh: str


EVENTS = (
    Event(
        "AUTUMN", "2025",
        "Programming Foundations & First Builds", "编程基础与工程起步",
        "Began undergraduate study at Hohai University, establishing a foundation in computing and intelligent technologies. C/C++ programming and team software projects developed my ability to translate problems into working implementations.",
        "进入河海大学，开启计算机与智能技术领域的系统学习。通过 C/C++ 编程和团队软件项目建立实现基础，逐步形成从问题分析到代码落地的工程思维。",
    ),
    Event(
        "SPRING", "2026",
        "Machine Learning & Research Practice", "机器学习与研究实践",
        "Developed a broad foundation in machine learning and deep learning through model implementation and experimentation. Joined a research team to investigate specific machine learning algorithm optimization problems, extending my focus from learning algorithms to research questions, methodological design, and empirical analysis.",
        "系统拓展机器学习与深度学习知识，通过模型实现和实验建立对核心方法的理解。进入研究团队，开始探索具体的机器学习算法优化问题，将关注点从算法学习推进到研究问题、方法设计与实证分析。",
    ),
    Event(
        "SUMMER", "2026",
        "Multimodal Intelligence & Policy Distillation", "多模态智能与策略蒸馏",
        "Extended my research focus to multimodal large language models and Online Policy Distillation (OPD). With access to advanced computing resources, I independently pursued Vision-OPD reproduction and follow-up experiments, testing methodological hypotheses, analyzing performance gaps, and investigating the possibilities and limitations of model capability transfer.",
        "将研究重心拓展至多模态大语言模型与在线策略蒸馏（Online Policy Distillation, OPD）。借助高水平计算资源，独立开展 Vision-OPD 复现与后续方案探索，通过实验检验方法假设、分析性能差距，并进一步理解模型能力迁移的技术路径与局限。",
    ),
    Event(
        "AUTUMN", "2026",
        "Model Architectures & Emerging Directions", "模型架构与前沿探索",
        "Expanded into tabular learning and alternative model architectures, exploring TabPFN, gradient-boosted trees, and FT-Transformer, while investigating the mechanisms and potential applications of emerging approaches such as JEV. Continuing to identify promising research questions and technical opportunities.",
        "将探索范围延伸至表格学习与新型模型架构，研究 TabPFN、梯度提升树和 FT-Transformer 等方法，并关注 JEV 等新兴方向的机制与应用潜力。持续拓展技术视野，寻找具有研究价值的问题与切入点。",
    ),
)


FOCUS = (
    ("Multimodal Intelligence & Policy Distillation", "多模态智能与策略蒸馏"),
    ("Tabular Learning & Model Architectures", "表格学习与模型架构"),
    ("Model Capability Transfer & Learning Mechanisms", "模型能力迁移与学习机制"),
    ("AI-Driven Software Engineering & Open-Source Building", "AI 驱动的软件工程与开源构建"),
)


def approx_width(value: str, size: float) -> float:
    width = 0.0
    for char in value:
        if ord(char) > 127:
            width += 1.0 if "\u4e00" <= char <= "\u9fff" or char in "，。；（）《》" else 0.58
        elif char in " il.,:;!'|":
            width += 0.28
        elif char in "MW@":
            width += 0.86
        elif char.isupper():
            width += 0.67
        elif char == " ":
            width += 0.32
        else:
            width += 0.53
    return width * size


def wrap(value: str, width: float, size: float, chinese: bool = False) -> list[str]:
    if chinese:
        tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9+./-]*|\s+|.", value)
        lines: list[str] = []
        current = ""
        for token in tokens:
            if token in "，。；：、！？）》" and current:
                current += token
            elif current and approx_width(current + token, size) > width - size:
                lines.append(current.strip())
                current = token.lstrip()
            else:
                current += token
        if current.strip():
            lines.append(current.strip())
        return lines

    lines = []
    current = ""
    for token in value.split():
        candidate = f"{current} {token}" if current else token
        if current and approx_width(candidate, size) > width:
            lines.append(current)
            current = token
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def text(x: float, y: float, value: str, class_name: str, extra: str = "") -> str:
    return f'<text class="{class_name}" x="{x:g}" y="{y:g}" {extra}>{escape(value)}</text>'


def lines_at(x: float, y: float, lines: list[str], class_name: str, step: int) -> list[str]:
    return [text(x, y + index * step, line, class_name) for index, line in enumerate(lines)]


def card(event: Event, x: int, y: int, width: int, mobile: bool) -> tuple[str, int]:
    pad = 21 if mobile else 27
    inner = width - 2 * pad
    title_size = 15 if mobile else 19
    body_en_size = 14 if mobile else 17
    body_zh_size = 14 if mobile else 17
    title_en = wrap(event.title_en, inner, title_size)
    title_zh = wrap(event.title_zh, inner, 16 if mobile else 19, True)
    body_en = wrap(event.body_en, inner, body_en_size)
    body_zh = wrap(event.body_zh, inner, body_zh_size, True)

    title_step = 22 if mobile else 27
    zh_title_step = 23 if mobile else 28
    en_step = 23 if mobile else 27
    zh_step = 25 if mobile else 29
    date_y = y + (37 if mobile else 43)
    en_title_y = date_y + (39 if mobile else 42)
    zh_title_y = en_title_y + len(title_en) * title_step + 4
    en_body_y = zh_title_y + len(title_zh) * zh_title_step + (22 if mobile else 26)
    last_en_y = en_body_y + (len(body_en) - 1) * en_step
    separator_y = last_en_y + (23 if mobile else 27)
    zh_body_y = separator_y + (27 if mobile else 32)
    last_zh_y = zh_body_y + (len(body_zh) - 1) * zh_step
    height = int(last_zh_y - y + (31 if mobile else 36))

    out = [
        f'<rect class="panel" x="{x}" y="{y}" width="{width}" height="{height}" rx="16"/>',
        f'<rect x="{x + pad}" y="{y + 24}" width="3" height="20" rx="1.5" fill="url(#accent)"/>',
        text(x + pad + 14, date_y, f"{event.season_en} {event.year}", "date"),
        f'<path class="hairline" d="M{x + pad} {date_y + 12}H{x + width - pad}"/>',
    ]
    out += lines_at(x + pad, en_title_y, title_en, "title-en", title_step)
    out += lines_at(x + pad, zh_title_y, title_zh, "title-zh", zh_title_step)
    out += lines_at(x + pad, en_body_y, body_en, "body-en", en_step)
    out.append(f'<path class="hairline" d="M{x + pad} {separator_y}H{x + width - pad}"/>')
    out += lines_at(x + pad, zh_body_y, body_zh, "body-zh", zh_step)
    out.append(f'<path d="M{x + pad} {y + height - 12}H{x + pad + 42}" stroke="url(#accent)" stroke-width="2"/>')
    return "\n".join(out), height


def shell(width: int, height: int, mobile: bool, content: str) -> str:
    radius = 16 if mobile else 20
    pattern = 25 if mobile else 30
    styles = """<style>
      text { font-family: Inter, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; }
      .panel { fill: #0a1b23; stroke: #2a4850; stroke-width: 1; }
      .hairline { fill: none; stroke: #29454d; stroke-width: 1; }
      .track { fill: none; stroke: #28636d; stroke-width: TRACK_SIZEpx; stroke-linecap: round; stroke-linejoin: round; }
      .track-core { fill: none; stroke: #76e9d3; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; opacity: .75; }
      .node-halo { fill: #72ead2; opacity: .17; }
      .node-ring { fill: #0a2630; stroke: #a5ffec; stroke-width: 3; }
      .node-core { fill: #8ff8e1; }
      .date { fill: #76efd8; font-size: DATE_SIZEpx; font-weight: 700; letter-spacing: .12em; }
      .title-en { fill: #f0fcfb; font-size: TITLE_EN_SIZEpx; font-weight: 700; }
      .title-zh { fill: #c9e6e5; font-size: TITLE_ZH_SIZEpx; font-weight: 650; }
      .body-en { fill: #b7cacc; font-size: BODY_EN_SIZEpx; }
      .body-zh { fill: #b7cacc; font-size: BODY_ZH_SIZEpx; }
      .year { fill: #e8fffa; font-size: YEAR_SIZEpx; font-weight: 760; letter-spacing: .09em; }
      .timeline-heading { fill: #effffc; font-size: TIMELINE_HEADING_SIZEpx; font-weight: 750; letter-spacing: .015em; }
      .focus-heading { fill: #effffc; font-size: FOCUS_HEADING_SIZEpx; font-weight: 760; letter-spacing: .02em; }
      .focus-row { fill: #0b2029; stroke: #2a4850; stroke-width: 1; }
      .focus-en { fill: #e5f7f4; font-size: FOCUS_EN_SIZEpx; font-weight: 650; }
      .focus-zh { fill: #a9c7c8; font-size: FOCUS_ZH_SIZEpx; }
    </style>"""
    sizes = (11, 15, 16, 14, 14, 14, 22, 19, 15, 14) if mobile else (13, 19, 19, 17, 17, 17, 26, 25, 20, 18)
    for key, size in zip(("DATE_SIZE", "TITLE_EN_SIZE", "TITLE_ZH_SIZE", "BODY_EN_SIZE", "BODY_ZH_SIZE", "YEAR_SIZE", "TRACK_SIZE", "FOCUS_HEADING_SIZE", "FOCUS_EN_SIZE", "FOCUS_ZH_SIZE"), sizes):
        styles = styles.replace(key, str(size))
    styles = styles.replace("TIMELINE_HEADING_SIZE", "19" if mobile else "30")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="timeline-desc">
  <title id="timeline-desc">Bilingual research timeline and current focus / 研究时间线与当前关注</title>
  {styles}
  <defs>
    <linearGradient id="background" x2="1" y2="1"><stop stop-color="#061117"/><stop offset=".62" stop-color="#081b23"/><stop offset="1" stop-color="#0b222d"/></linearGradient>
    <linearGradient id="accent"><stop stop-color="#70efd5"/><stop offset="1" stop-color="#72c9ff"/></linearGradient>
    <pattern id="grid" width="{pattern}" height="{pattern}" patternUnits="userSpaceOnUse"><path d="M{pattern} 0H0V{pattern}" fill="none" stroke="#163039" stroke-width="1"/></pattern>
    <clipPath id="clip"><rect width="{width}" height="{height}" rx="{radius}"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{width}" height="{height}" fill="url(#background)"/>
    <rect width="{width}" height="{height}" fill="url(#grid)" opacity=".25"/>
    {content}
  </g>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="{radius - .5}" fill="none" stroke="#29434c"/>
</svg>
'''


def year_marker(x: int, y: int, width: int = 110, mobile: bool = False) -> str:
    height = 50 if mobile else 56
    return "\n".join((
        f'<rect x="{x - width // 2}" y="{y - height // 2}" width="{width}" height="{height}" rx="{height // 2}" fill="#10313a" stroke="#9af5df" stroke-width="2"/>',
        text(x, y + 6, "2026", "year", 'text-anchor="middle"'),
    ))


def timeline_heading(mobile: bool) -> str:
    track_x = 27 if mobile else 56
    title_x = 54 if mobile else 112
    node_y = 51 if mobile else 66
    baseline = 58 if mobile else 78
    underline_y = 76 if mobile else 100
    title_width = 232 if mobile else 365
    halo_radius = 17 if mobile else 25
    ring_radius = 12 if mobile else 17
    return "\n".join((
        f'<path d="M{track_x + ring_radius} {node_y}H{title_x - 7}" stroke="url(#accent)" stroke-width="2" stroke-linecap="round"/>',
        f'<circle class="node-halo" cx="{track_x}" cy="{node_y}" r="{halo_radius}"/>',
        f'<circle class="node-ring" cx="{track_x}" cy="{node_y}" r="{ring_radius}"/>',
        f'<circle class="node-core" cx="{track_x}" cy="{node_y}" r="{4 if mobile else 5}"/>',
        text(title_x, baseline, "My Adventure in AI & CS", "timeline-heading"),
        f'<path d="M{title_x} {underline_y}H{title_x + title_width}" stroke="#31535b" stroke-width="1"/>',
        f'<path d="M{title_x} {underline_y}H{title_x + (40 if mobile else 58)}" stroke="url(#accent)" stroke-width="2"/>',
    ))


def ellipsis(x: int, y: int, mobile: bool) -> str:
    steps = (24, 20, 20) if mobile else (32, 27, 27)
    radii = (6, 5, 4) if mobile else (8, 7, 6)
    opacity = (1, .78, .56)
    dots = []
    current = y
    for step, radius, alpha in zip(steps, radii, opacity):
        current += step
        dots.append(f'<circle cx="{x}" cy="{current}" r="{radius}" fill="#91f5df" opacity="{alpha}"/>')
    return "\n".join(dots)


def focus_section(start_y: int, mobile: bool) -> tuple[str, int]:
    center = 195 if mobile else 600
    heading_y = start_y + (27 if mobile else 31)
    underline_half = 88 if mobile else 126
    output = [
        text(center, heading_y, "CURRENT FOCUS 当前关注", "focus-heading", 'text-anchor="middle"'),
        f'<path d="M{center - underline_half} {heading_y + 19}H{center + underline_half}" stroke="#31535b" stroke-width="1"/>',
        f'<path d="M{center - 35} {heading_y + 19}H{center + 35}" stroke="url(#accent)" stroke-width="2"/>',
    ]

    row_y = start_y + (74 if mobile else 81)
    row_x, row_width = (33, 324) if mobile else (155, 890)
    for english, chinese in FOCUS:
        if mobile:
            en_lines = wrap(english, row_width - 64, 15)
            zh_lines = wrap(chinese, row_width - 64, 14, True)
            en_y = row_y + 34
            zh_y = en_y + len(en_lines) * 22 + 12
            row_height = zh_y - row_y + (len(zh_lines) - 1) * 24 + 27
            text_x = row_x + 38
            output.append(f'<rect class="focus-row" x="{row_x}" y="{row_y}" width="{row_width}" height="{row_height}" rx="14"/>')
            output.append(f'<rect x="{row_x + 19}" y="{row_y + 22}" width="3" height="{row_height - 44}" rx="1.5" fill="url(#accent)"/>')
            output += lines_at(text_x, en_y, en_lines, "focus-en", 22)
            output += lines_at(text_x, zh_y, zh_lines, "focus-zh", 24)
            row_y += row_height + 13
        else:
            row_height = 100
            text_x = row_x + 40
            output.extend((
                f'<rect class="focus-row" x="{row_x}" y="{row_y}" width="{row_width}" height="{row_height}" rx="14"/>',
                f'<rect x="{row_x + 21}" y="{row_y + 23}" width="3" height="54" rx="1.5" fill="url(#accent)"/>',
                text(text_x, row_y + 42, english, "focus-en"),
                text(text_x, row_y + 73, chinese, "focus-zh"),
            ))
            row_y += row_height + 15
    return "\n".join(output), row_y + 26


def desktop() -> str:
    card_x, card_width = 112, 976
    left_track, right_track = 56, 1144
    first_y = 133
    first, first_height = card(EVENTS[0], card_x, first_y, card_width, False)
    crossing_y = first_y + first_height + 76
    pieces = [first]
    nodes = [(left_track, first_y + 38, card_x)]
    current_y = crossing_y + 76
    for event in EVENTS[1:]:
        drawing, height = card(event, card_x, current_y, card_width, False)
        pieces.append(drawing)
        nodes.append((right_track, current_y + 38, card_x + card_width))
        current_y += height + 30
    tail_start = current_y + 25
    tip_y = tail_start + 556
    focus_drawing, total_height = focus_section(tail_start + 692, False)
    route = (
        f"M{left_track} 66V{crossing_y - 120} Q{left_track} {crossing_y} 176 {crossing_y} "
        f"H1024 Q{right_track} {crossing_y} {right_track} {crossing_y + 120} "
        f"V{tail_start} Q{right_track} {tail_start + 90} 1066 {tail_start + 135} "
        f"L678 {tail_start + 359} Q600 {tail_start + 404} 600 {tail_start + 494} V{tip_y}"
    )
    tracks = [f'<path class="track" d="{route}"/>', f'<path class="track-core" d="{route}"/>']
    for node_x, node_y, card_edge in nodes:
        tracks.extend((
            f'<path class="hairline" d="M{min(node_x, card_edge)} {node_y}H{max(node_x, card_edge)}"/>',
            f'<circle class="node-halo" cx="{node_x}" cy="{node_y}" r="26"/>',
            f'<circle class="node-ring" cx="{node_x}" cy="{node_y}" r="19"/>',
            f'<circle class="node-core" cx="{node_x}" cy="{node_y}" r="6"/>',
        ))
    content = "\n".join(tracks + [timeline_heading(False)] + pieces + [year_marker(600, crossing_y, 96), ellipsis(600, tip_y, False), focus_drawing])
    return shell(1200, total_height, False, content)


def mobile() -> str:
    card_x, card_width = 54, 282
    left_track, right_track = 27, 363
    current_y = 105
    pieces = []
    nodes = []
    crossing_y = 0
    for index, event in enumerate(EVENTS):
        if index == 1:
            crossing_y = current_y + 36
            current_y = crossing_y + 60
        drawing, height = card(event, card_x, current_y, card_width, True)
        pieces.append(drawing)
        nodes.append((left_track if index == 0 else right_track, current_y + 32, card_x if index == 0 else card_x + card_width))
        current_y += height + 26
    tail_start = current_y + 24
    tip_y = tail_start + 274
    focus_drawing, total_height = focus_section(tail_start + 380, True)
    route = (
        f"M{left_track} 51V{crossing_y - 70} Q{left_track} {crossing_y} 97 {crossing_y} "
        f"H293 Q{right_track} {crossing_y} {right_track} {crossing_y + 70} "
        f"V{tail_start} Q{right_track} {tail_start + 58} 315 {tail_start + 86} "
        f"L243 {tail_start + 128} Q195 {tail_start + 156} 195 {tail_start + 214} V{tip_y}"
    )
    tracks = [f'<path class="track" d="{route}"/>', f'<path class="track-core" d="{route}"/>']
    for node_x, node_y, card_edge in nodes:
        tracks.extend((
            f'<path class="hairline" d="M{min(node_x, card_edge)} {node_y}H{max(node_x, card_edge)}"/>',
            f'<circle class="node-halo" cx="{node_x}" cy="{node_y}" r="20"/>',
            f'<circle class="node-ring" cx="{node_x}" cy="{node_y}" r="16"/>',
            f'<circle class="node-core" cx="{node_x}" cy="{node_y}" r="5"/>',
        ))
    content = "\n".join(tracks + [timeline_heading(True)] + pieces + [year_marker(195, crossing_y, 88, True), ellipsis(195, tip_y, True), focus_drawing])
    return shell(390, total_height, True, content)


def main() -> None:
    ASSETS.joinpath("timeline.svg").write_text(desktop(), encoding="utf-8")
    ASSETS.joinpath("timeline-mobile.svg").write_text(mobile(), encoding="utf-8")


if __name__ == "__main__":
    main()
