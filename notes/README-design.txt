═══════════════════════════════════════════════════════════
README v2 结构设计笔记
主题：Cyberpunk Neon Terminal（赛博朋克霓虹终端）
创建：2026-08-11
状态：初稿，待迭代
═══════════════════════════════════════════════════════════

【可用资产】（assets/ ═══════════════════════════════
  已存在且质量 OK 的 SVG，直接复用：
  ├── neon-header.svg       头部横幅（带网格、扫描线、粒子动画）
  ├── status-bar.svg        状态条（绿色脉冲点 + 终端信息行）
  ├── section-research.svg   🔬 RESEARCH FOCUS / 研究方向（青色）
  ├── section-arsenal.svg    技术武库（绿色，样式应与其他 section 一致）
  ├── section-projects.svg  🚀 FEATURED PROJECTS / 精选项目（紫色）
  ├── section-stats.svg      统计面板（样式一致）
  ├── section-arcade.svg     贡献街机（样式一致）
  ├── section-connect.svg    联系方式（样式一致）
  ├── section-char-sheet.svg 角色面板（样式一致）
  └── footer-rift.svg       页脚（中继线 + 钻石脉冲）

  配色体系（从 SVG 提取）：
  - 主文字：终端命令行 #00ff88 绿
  - 板块标题：各自主题色（青/紫/绿）
  - 中文副标题：#888888 灰
  - 背景：#0D1117
  - 结构："> 命令行提示" + "EMOJI TITLE" + "/ 中文标题"

【用户信息】
  姓名：ZHANG RUIHAN / 张锐寒
  昵称：浪兮
  GitHub：spinner-bot
  学校：河海大学 · 人工智能与自动化学院
  实验室：HHU DIG Lab (Data Intelligence & Governance) 数智治域实验室
  团队：2025 URT 本科生科研团队
  地点：江苏 南京 江宁
  语言：Python, C, C++, HTML, 即将 Java
  方向：AI/NLP/CV / 游戏开发 / 数学可视化 / 自动化工具

【项目信息】（12 个原创 + 1 个 Fork）
  EffiLife (Python)        — "浪兮效率，高效生活"
  IllusionaryNook (C++)     — "3D open-world sandbox game, high freedom"
  auto-ssh (Python)         — SSH 自动化工具
  Concept-UrbanChain (Python)— 概念系统 / 算法实验沙箱
  sphere-dreamweave (C++)   — "Beauty of Mathematics in Code"
  Pixel-Roamer (Python)     — 10 年前设计的游戏，现在实现
  mind-map (C)              — 自动扫描思路生成 .mind 文件
  AI-lab-2nd-generation (Python) — NLP/CV/AI 学习笔记与代码
  BouncingBall-SurvivalDash (C++) — C++ 入门小游戏
  fundamentals-forge (HTML) — "My adventure in fundamentals"
  AI-lab (Python) [归档]
  img2Russellvec (Python) [Fork] — AI 图像情绪识别

【全局规则】
  - 居中布局：<div align="center">
  - 板块之间：<br/> 留白分隔
  - 蛇形图：保持现有配置，放到 CONTRIBUTION ARCADE 板块

【板块结构】（从上到下，仅 2 个板块）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 打字机动画
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  内容：两句交替
    EN: "Building systems that see, read, and understand."
    CN: 「构建能看、能读、能理解的智能系统」
  实现：https://git.io/typing-svg 或 readme-typing-svg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. CONTRIBUTION ARCADE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  内容：
    - 🐍 蛇形动画（已有，保持 picture 标签暗色/亮色切换）
  实现：直接复用当前 README 中的 <picture> 标签

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【待确认】
  □ 打字动画文案是否 OK？

【待实现】
  ☑ 蛇形动画
  ☐ 打字机动画
