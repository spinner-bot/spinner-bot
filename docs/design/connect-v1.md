# Let's connect！邀请卡

日期：2026-10-11。接在时间线／Current Focus 画布后、贪吃蛇动画前，作为 README 的收尾邀请。英文在前，中文在后；标题按用户指定为 `Let's connect！`，不加中文标题。邀请语：

> Have an idea, a question, or a project in mind? Let's exchange perspectives and build what's next.
>
> 有想法、问题，或正在酝酿的项目吗？欢迎交流观点，一起构建下一步的可能。

沿用封面和时间线的深青黑、细网格、薄荷青与浅蓝强调、圆角边框。背景顶部约 20% 固定为原来的 `#061117`，从该位置往下才开始变色；纵向颜色变化采用非匀速节点，先极轻、后逐段加速转向同一色系的浅绿。用一条向右上方延伸的信号轨迹、流动光点、节点呼吸与小型闪烁线表示“连接”和向前探索。文字保持静止，不用色相切换或大幅弹跳。桌面与手机使用各自的 SVG，独立自带背景，以适应 GitHub 明暗主题。

README 图片模式下，浏览器对 SVG 内部的 `prefers-reduced-motion` 响应可能不稳定。因此额外生成无旅行光点、无闪烁和呼吸动画的 `connect-still.svg`、`connect-mobile-still.svg`，并通过 `<picture>` 媒体条件显式选择。静态画面仍保留完整邀请语和上升轨迹。

验收：四张 SVG 均通过 XML 解析；桌面与手机图片预览文字、轨迹和渐变无溢出。使用浏览器的减少动态效果设置加载 README 同结构的 `<picture>` 时，实际选中了手机版静态 SVG，间隔 1.5 秒的两帧截图完全一致。

生成脚本为 `scripts/build_connect.py`，预览脚本为 `scripts/preview_connect.py`。第一版过程图保存在 `previews/connect-desktop-v1.png`、`previews/connect-mobile-v1.png`、`previews/connect-mobile-motion-v1.png`（晚 1.5 秒的动画帧）、`previews/connect-reduced-motion-v1.png`。
