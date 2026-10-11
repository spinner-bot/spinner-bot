"""Build bilingual animated invitation cards for the profile README."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def card(mobile: bool, static: bool = False) -> str:
    width, height = (390, 520) if mobile else (1200, 360)
    radius = 16 if mobile else 20
    title_x, title_y = (34, 68) if mobile else (76, 101)
    line_y = 89 if mobile else 126
    line_end = 356 if mobile else 684
    route = (
        "M48 474 C103 474 109 448 157 434 S232 389 266 377 S312 339 339 329"
        if mobile else
        "M784 291 C846 291 849 248 905 232 S978 188 1018 166 S1080 113 1117 76"
    )
    ghost = (
        "M70 493 C140 476 180 471 217 441 S290 397 347 378"
        if mobile else
        "M788 316 C870 312 903 297 959 264 S1060 208 1140 187"
    )
    end_x, end_y = (339, 329) if mobile else (1117, 76)
    nodes = (
        ((48, 474), (157, 434), (266, 377), (339, 329)) if mobile else
        ((784, 291), (905, 232), (1018, 166), (1117, 76))
    )
    nodes_svg = "\n".join(
        f'<circle class="waypoint" cx="{x}" cy="{y}" r="{4 if mobile else 5}"/>'
        for x, y in nodes[:-1]
    )
    copy = (
        '''<text class="body-en" x="34" y="137">Have an idea, a question, or a</text>
    <text class="body-en" x="34" y="164">project in mind?</text>
    <text class="body-en" x="34" y="208">Let's exchange perspectives and</text>
    <text class="body-en" x="34" y="235">build what's next.</text>
    <path class="copy-rule" d="M34 258H356"/>
    <text class="body-zh" x="34" y="288">有想法、问题，或正在酝酿的项目吗？</text>
    <text class="body-zh" x="34" y="317">欢迎交流观点，一起构建下一步的可能。</text>'''
        if mobile else
        '''<text class="body-en" x="76" y="183">Have an idea, a question, or a project in mind?</text>
    <text class="body-en" x="76" y="218">Let's exchange perspectives and build what's next.</text>
    <path class="copy-rule" d="M76 240H665"/>
    <text class="body-zh" x="76" y="275">有想法、问题，或正在酝酿的项目吗？</text>
    <text class="body-zh" x="76" y="311">欢迎交流观点，一起构建下一步的可能。</text>'''
    )
    arrow = (
        "M315 333L339 329L333 352" if mobile else "M1093 80L1117 76L1111 101"
    )
    sparks = (
        '''<path class="spark spark-a" d="M287 350l7 -9M303 365l9 -3M323 305l3 -11"/>
    <circle class="spark spark-b" cx="302" cy="319" r="2.5"/>'''
        if mobile else
        '''<path class="spark spark-a" d="M1038 106l6 -14M1062 129l12 -7M1126 120l5 -11"/>
    <circle class="spark spark-b" cx="1084" cy="71" r="3"/>'''
    )
    travelers = "" if static else f'''<circle class="traveler" r="{5 if mobile else 6}">
      <animateMotion dur="4.8s" repeatCount="indefinite" path="{route}"/>
    </circle>
    <circle class="traveler" r="{3 if mobile else 4}" opacity=".65">
      <animateMotion dur="4.8s" begin="2.4s" repeatCount="indefinite" path="{route}"/>
    </circle>'''
    arrival_animation = "none" if static else "arrival 3.2s ease-in-out infinite"
    spark_animation = "none" if static else "twinkle 2.7s ease-in-out infinite"
    second_spark_animation = "none" if static else "twinkle 2.7s ease-in-out 1.1s infinite"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="connect-title connect-desc">
  <title id="connect-title">Let's connect！</title>
  <desc id="connect-desc">A bilingual invitation to exchange ideas and build what comes next. Animated signals travel along an upward path.</desc>
  <style>
    text {{ font-family: Inter, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; }}
    .heading {{ fill: #effffc; font-size: {34 if mobile else 52}px; font-weight: 760; letter-spacing: -.025em; }}
    .body-en {{ fill: #d6eeec; font-size: {17 if mobile else 23}px; font-weight: 510; }}
    .body-zh {{ fill: #abc9ca; font-size: {16 if mobile else 21}px; }}
    .copy-rule {{ fill: none; stroke: #29454d; stroke-width: 1; }}
    .route-ghost {{ fill: none; stroke: #234b55; stroke-width: {2 if mobile else 3}; stroke-linecap: round; }}
    .route {{ fill: none; stroke: #3a8387; stroke-width: {8 if mobile else 10}; stroke-linecap: round; stroke-linejoin: round; }}
    .route-core {{ fill: none; stroke: #8debd9; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
    .arrow {{ fill: none; stroke: #a1f8e6; stroke-width: {5 if mobile else 6}; stroke-linecap: round; stroke-linejoin: round; }}
    .waypoint {{ fill: #abfceb; stroke: #0a2831; stroke-width: 2; }}
    .arrival {{ fill: #0a2831; stroke: #a1f8e6; stroke-width: 3; transform-box: fill-box; transform-origin: center; animation: {arrival_animation}; }}
    .traveler {{ fill: #d3fff4; stroke: #83efdf; stroke-width: 2; }}
    .spark {{ fill: none; stroke: #7ce7d4; stroke-width: 2; stroke-linecap: round; }}
    .spark-b {{ fill: #7ce7d4; stroke: none; }}
    .spark-a {{ animation: {spark_animation}; }}
    .spark-b {{ animation: {second_spark_animation}; }}
    @keyframes arrival {{ 50% {{ opacity: .5; transform: scale(1.35); }} }}
    @keyframes twinkle {{ 50% {{ opacity: .28; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .arrival, .spark {{ animation: none; }}
      .traveler {{ display: none; }}
    }}
  </style>
  <defs>
    <linearGradient id="background" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#061117"/><stop offset=".20" stop-color="#061117"/><stop offset=".48" stop-color="#07191d"/><stop offset=".70" stop-color="#0b2829"/><stop offset=".85" stop-color="#143b35"/><stop offset=".94" stop-color="#205445"/><stop offset="1" stop-color="#2b6b52"/></linearGradient>
    <linearGradient id="accent"><stop stop-color="#70efd5"/><stop offset="1" stop-color="#72c9ff"/></linearGradient>
    <pattern id="grid" width="{25 if mobile else 30}" height="{25 if mobile else 30}" patternUnits="userSpaceOnUse"><path d="M{25 if mobile else 30} 0H0V{25 if mobile else 30}" fill="none" stroke="#163039" stroke-width="1"/></pattern>
    <clipPath id="clip"><rect width="{width}" height="{height}" rx="{radius}"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{width}" height="{height}" fill="url(#background)"/>
    <rect width="{width}" height="{height}" fill="url(#grid)" opacity=".25"/>
    <path d="M{title_x} {line_y}H{line_end}" stroke="#29454d" stroke-width="1"/>
    <path d="M{title_x} {line_y}h{58 if mobile else 92}" stroke="url(#accent)" stroke-width="3" stroke-linecap="round"/>
    <text class="heading" x="{title_x}" y="{title_y}">Let's connect！</text>
    {copy}
    <path class="route-ghost" d="{ghost}"/>
    <path class="route" d="{route}"/>
    <path class="route-core" d="{route}"/>
    {nodes_svg}
    <circle class="arrival" cx="{end_x}" cy="{end_y}" r="{12 if mobile else 14}"/>
    <path class="arrow" d="{arrow}"/>
{travelers}
    {sparks}
  </g>
  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="{radius - .5}" fill="none" stroke="#29434c"/>
</svg>
'''


def main() -> None:
    ASSETS.joinpath("connect.svg").write_text(card(False), encoding="utf-8")
    ASSETS.joinpath("connect-mobile.svg").write_text(card(True), encoding="utf-8")
    ASSETS.joinpath("connect-still.svg").write_text(card(False, True), encoding="utf-8")
    ASSETS.joinpath("connect-mobile-still.svg").write_text(card(True, True), encoding="utf-8")


if __name__ == "__main__":
    main()
