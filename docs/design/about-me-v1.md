# About Me 区块设计记录

日期：2026-10-11。此版将 About Me 放在动画封面之后。首轮采用 HTML 双栏表格，网页实测显示为白色默认表格，和封面深色视觉不一致。根据截图反馈，改为自带背景的独立 SVG 卡片：桌面左右双栏，窄屏上下排列。

## 内容与顺序

- 标题：`ABOUT ME 关于我`，英语在前，中间以空格连接。
- 左栏为用户提供的英文原文，右栏为中文原文；两栏保持相同的语义顺序，不改写正文。
- 栏目眉题分别标为 `PROFILE` 与 `个人简介`，不出现序号或语言名称标签。

## 视觉实现

- `assets/about-me.svg` 自带深色渐变背景、细边框、栏目线和中心轨道，网页亮色或暗色主题下外观一致。
- `assets/about-me-mobile.svg` 在窄屏布局中先完整显示英文，再显示中文，保留英语在前的顺序。
- README 使用 `<picture>` 按屏幕宽度选择桌面或窄屏构图。
- 图卡中的正文保持静态；完整双语正文同时写入 `<img alt>`，图片加载失败时仍可获取内容。
- 首轮表格方案用到的 `archive/legacy-assets/about-rule.svg`、`archive/legacy-assets/about-divider.svg` 和预览截图已归档，作为迭代资料。
- `scripts/preview_about_me.py` 生成当前卡片的桌面与窄屏预览；`previews/about-me-v2.png` 和 `previews/about-me-mobile-v2.png` 为本轮成稿。
- 初稿预览 `archive/design-history/previews/about-me-v1.png` 与 `archive/design-history/previews/about-me-mobile-v1.png` 保留 HTML 表格在网页主题背景下的效果，记录此次修订原因。

## 已知取舍

SVG 内的正文不是可选择文本；替代文本提供完整双语内容。桌面与窄屏分别使用两种 SVG 构图，避免窄屏双栏挤压正文。
