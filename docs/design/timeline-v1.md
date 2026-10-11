# 研究时间线设计记录

日期：2026-10-11。接在 About Me 后，不设板块标题。完整双语正文位于 `scripts/build_timeline.py`，由脚本生成 `assets/timeline.svg` 和 `assets/timeline-mobile.svg`。页面通过 `<picture>` 选择适合屏宽的布局。

- 英文在前，中文在后。每个节点只写一次年份；英文日期使用 `AUTUMN 2025` 等格式，中文日期只补充季节。
- 2025 节点在左，2026 节点在右。主轨道在年份变化处以两段圆角弯折横向过渡，中央悬浮 `2026` 标记，保留可见的横向轨迹。
- 窄屏改为单列节点，跨年以横向细线和悬浮年份标记表达，维持正文字号和阅读顺序。
- 春季英文补入 “specific machine learning algorithm optimization problems”；夏季英文补入 “With access to advanced computing resources”。
- 正文为静态 SVG 文本；卡片背景、轨道与细节不依赖 GitHub 的亮暗主题。正文数据保留在生成脚本中，后续可继续修改。
- `scripts/preview_timeline.py` 生成桌面和手机的预览截图，保存在 `previews/` 下。
