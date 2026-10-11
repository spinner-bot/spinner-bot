"""Build the two self-contained SVG layouts for the bilingual research timeline."""

from dataclasses import dataclass
from pathlib import Path
import re
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


@dataclass(frozen=True)
class Event:
    season_en: str
    season_zh: str
    year: str
    title_en: str
    title_zh: str
    body_en: str
    body_zh: str


EVENTS = (
    Event(
        "AUTUMN", "秋", "2025",
        "Programming Foundations & First Builds", "编程基础与工程起步",
        "Began undergraduate study at Hohai University, establishing a foundation in computing and intelligent technologies. C/C++ programming and team software projects developed my ability to translate problems into working implementations.",
        "进入河海大学，开启计算机与智能技术领域的系统学习。通过 C/C++ 编程和团队软件项目建立实现基础，逐步形成从问题分析到代码落地的工程思维。",
    ),
    Event(
        "SPRING", "春", "2026",
        "Machine Learning & Research Practice", "机器学习与研究实践",
        "Developed a broad foundation in machine learning and deep learning through model implementation and experimentation. Joined a research team to investigate specific machine learning algorithm optimization problems, extending my focus from learning algorithms to research questions, methodological design, and empirical analysis.",
        "系统拓展机器学习与深度学习知识，通过模型实现和实验建立对核心方法的理解。进入研究团队，开始探索具体的机器学习算法优化问题，将关注点从算法学习推进到研究问题、方法设计与实证分析。",
    ),
    Event(
        "SUMMER", "夏", "2026",
        "Multimodal Intelligence & Policy Distillation", "多模态智能与策略蒸馏",
        "Extended my research focus to multimodal large language models and Online Policy Distillation (OPD). With access to advanced computing resources, I independently pursued Vision-OPD reproduction and follow-up experiments, testing methodological hypotheses, analyzing performance gaps, and investigating the possibilities and limitations of model capability transfer.",
        "将研究重心拓展至多模态大语言模型与在线策略蒸馏（Online Policy Distillation, OPD）。借助高水平计算资源，独立开展 Vision-OPD 复现与后续方案探索，通过实验检验方法假设、分析性能差距，并进一步理解模型能力迁移的技术路径与局限。",
    ),
    Event(
        "AUTUMN", "秋", "2026",
        "Model Architectures & Emerging Directions", "模型架构与前沿探索",
        "Expanded into tabular learning and alternative model architectures, exploring TabPFN, gradient-boosted trees, and FT-Transformer, while investigating the mechanisms and potential applications of emerging approaches such as JEV. Continuing to identify promising research questions and technical opportunities.",
        "将探索范围延伸至表格学习与新型模型架构，研究 TabPFN、梯度提升树和 FT-Transformer 等方法，并关注 JEV 等新兴方向的机制与应用潜力。持续拓展技术视野，寻找具有研究价值的问题与切入点。",
    ),
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
        text(x + width - pad, date_y, event.season_zh, "date-zh", 'text-anchor="end"'),
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
      .track { fill: none; stroke: #3b7c80; stroke-width: 2; }
      .date { fill: #76efd8; font-size: DATE_SIZEpx; font-weight: 700; letter-spacing: .12em; }
      .date-zh { fill: #9ad9dd; font-size: DATE_ZH_SIZEpx; font-weight: 650; }
      .title-en { fill: #f0fcfb; font-size: TITLE_EN_SIZEpx; font-weight: 700; }
      .title-zh { fill: #c9e6e5; font-size: TITLE_ZH_SIZEpx; font-weight: 650; }
      .body-en { fill: #b7cacc; font-size: BODY_EN_SIZEpx; }
      .body-zh { fill: #b7cacc; font-size: BODY_ZH_SIZEpx; }
      .year { fill: #e8fffa; font-size: YEAR_SIZEpx; font-weight: 760; letter-spacing: .09em; }
    </style>"""
    sizes = (11, 12, 15, 16, 14, 14, 14) if mobile else (13, 14, 19, 19, 17, 17, 17)
    for key, size in zip(("DATE_SIZE", "DATE_ZH_SIZE", "TITLE_EN_SIZE", "TITLE_ZH_SIZE", "BODY_EN_SIZE", "BODY_ZH_SIZE", "YEAR_SIZE"), sizes):
        styles = styles.replace(key, str(size))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="timeline-desc">
  <title id="timeline-desc">Bilingual research timeline, 2025 to 2026 / 2025 至 2026 年研究时间线</title>
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


def year_marker(x: int, y: int, width: int = 110) -> str:
    return "\n".join((
        f'<rect x="{x - width // 2}" y="{y - 20}" width="{width}" height="40" rx="20" fill="#13313a" stroke="#60c8bd"/>',
        text(x, y + 6, "2026", "year", 'text-anchor="middle"'),
    ))


def desktop() -> str:
    left_x, right_x, card_width = 60, 680, 460
    first_y = 68
    first, first_height = card(EVENTS[0], left_x, first_y, card_width, False)
    crossing_y = first_y + first_height + 70
    pieces = [first]
    nodes = [(540, first_y + 38, 520)]
    current_y = crossing_y + 70
    for event in EVENTS[1:]:
        drawing, height = card(event, right_x, current_y, card_width, False)
        pieces.append(drawing)
        nodes.append((660, current_y + 38, 680))
        current_y += height + 26
    total_height = current_y + 12
    tracks = [
        f'<path class="track" d="M540 28V{crossing_y - 20} Q540 {crossing_y} 560 {crossing_y} H640 Q660 {crossing_y} 660 {crossing_y + 20} V{total_height - 29}"/>',
        f'<path d="M560 {crossing_y}H640" stroke="#70efd5" stroke-width="3"/>',
    ]
    for index, (node_x, node_y, card_edge) in enumerate(nodes):
        tracks.extend((
            f'<path class="hairline" d="M{min(node_x, card_edge)} {node_y}H{max(node_x, card_edge)}"/>',
            f'<circle cx="{node_x}" cy="{node_y}" r="{7 if index == 0 else 6}" fill="#0b1f27" stroke="#71ecd7" stroke-width="2"/>',
            f'<circle cx="{node_x}" cy="{node_y}" r="2" fill="#71ecd7"/>',
        ))
    content = "\n".join(tracks + pieces + [year_marker(600, crossing_y - 31, 88)])
    return shell(1200, total_height, False, content)


def mobile() -> str:
    x, card_width = 43, 323
    current_y = 44
    pieces = []
    nodes = []
    crossing_y = 0
    for index, event in enumerate(EVENTS):
        if index == 1:
            crossing_y = current_y + 28
            current_y = crossing_y + 48
        drawing, height = card(event, x, current_y, card_width, True)
        pieces.append(drawing)
        nodes.append(current_y + 32)
        current_y += height + 26
    total_height = current_y + 12
    tracks = [
        f'<path class="track" d="M23 24V{total_height - 29}"/>',
        f'<path d="M23 {crossing_y}H366" stroke="#70efd5" stroke-width="2" opacity=".65"/>',
    ]
    for node_y in nodes:
        tracks.extend((
            f'<path class="hairline" d="M23 {node_y}H43"/>',
            f'<circle cx="23" cy="{node_y}" r="5" fill="#0b1f27" stroke="#71ecd7" stroke-width="2"/>',
        ))
    content = "\n".join(tracks + pieces + [year_marker(194, crossing_y, 88)])
    return shell(390, total_height, True, content)


def main() -> None:
    ASSETS.joinpath("timeline.svg").write_text(desktop(), encoding="utf-8")
    ASSETS.joinpath("timeline-mobile.svg").write_text(mobile(), encoding="utf-8")


if __name__ == "__main__":
    main()
