# 项目完整状态快照

**最后更新**：2026-08-05
**当前版本**：v2（已推送）

---

## 1. 仓库信息

| 项目 | 内容 |
|------|------|
| GitHub 用户名 | `spinner-bot` |
| 特殊仓库 | `spinner-bot/spinner-bot` |
| 本地路径 | `D:\资源夹\科研\通用\github\profile` |
| 远程 | `https://github.com/spinner-bot/spinner-bot.git` |
| 分支 | `main` |
| 页面地址 | https://github.com/spinner-bot |

---

## 2. 用户信息全览

| 维度 | 英文 | 中文 |
|------|------|------|
| 用户名 | spinner-bot | - |
| 昵称 | spinner-bot | 浪兮 |
| 本名 | Zhang Ruihan | 张锐寒 |
| 学校 | HHU (Hohai University) | 河海大学 |
| 学院 | School of AI & Automation | 人工智能与自动化学院 |
| 实验室 | DIG Lab (Data Intelligence & Governance) | 数智治域实验室 |
| 团队 | 2025 URT Undergraduate Research Team | 2025 URT 本科生科研团队 |
| 年级 | Freshman → Sophomore (2025.09 enrolled) | 大一暑假 → 即将大二 |
| 位置 | Nanjing, Jiangsu, China | 中国·江苏·南京 |

### 技术栈
- **已掌握**：Python（主力）, C, C++, HTML
- **学习中**：Java
- **AI/ML**：PyTorch, scikit-learn, OpenCV, HuggingFace
- **工具**：Git, Docker, Linux, VSCode

### 研究方向
- **多模态 OPD**（Multimodal OPD Research）
- AI 深度学习、NLP、CV

### 项目列表
1. Concept-UrbanChain (Python) — 城市计算概念系统
2. AI-lab-2nd-generation (Python) — AI 学习代码与笔记
3. Pixel-Roamer (Python) — 10年前设计的游戏
4. IllusionaryNook (C++) — 3D开放世界沙盒
5. sphere-dreamweave (C++) — 数学可视化
6. mind-map (C) — 思维导图自动生成
7. EffiLife (Python) — 效率工具
8. auto-ssh (Python) — SSH 自动化
9. BouncingBall-SurvivalDash (C++) — C++入门游戏
10. fundamentals-forge (HTML) — 基础学习记录
11. img2Russellvec (Python, Fork) — AI图像情绪识别

---

## 3. 用户需求完整记录

### 已确认
- [x] 中英双语，英语在前（**注意：最新指示改为纯英文**）
- [x] 动画过长时中英切换循环（通过 typing SVG 交替实现）
- [x] 风格：赛博朋克霓虹终端，炫酷、颜色夸张、冲击感强
- [x] **背景炫酷，文字清晰易读**（关键原则）
- [x] **沉浸式**：暗黑色块全覆盖，模块之间连续不孤立
- [ ] 纯英文（最新指示，尚未执行）

### 待定
- [ ] 联系方式（邮箱？）
- [ ] 最终内容文案（用户将提供内容文档）
- [ ] 蛇形动画 GitHub Actions 自动更新
- [ ] 3D 贡献墙

---

## 4. 设计规范

### 配色
| 用途 | 色值 |
|------|------|
| 背景 | #0D1117 |
| 霓虹绿 | #00ff88 |
| 霓虹洋红 | #ff00ff |
| 霓虹青 | #00ccff |
| 霓虹橙 | #ff6600 |

### 设计原则
1. **背景炫酷，文字干净** — SVG 负责视觉冲击，Markdown 保持可读性
2. **沉浸式连续感** — 暗黑背景贯穿，Section SVG 头图串联板块
3. **终端命令行主题** — 每个 section 头图带 `> command` 提示符
4. **多色霓虹交替** — 不同 section 用不同霓虹色区分

---

## 5. 文件结构

```
D:\资源夹\科研\通用\github\profile\
├── .gitignore              # 忽略 notes/
├── README.md               # 个人主页 Markdown（v2）
├── assets/
│   ├── neon-header.svg     # 顶部大横幅（绿+洋红+青霓虹）
│   ├── status-bar.svg      # 状态条（ONLINE 指示灯）
│   ├── section-char-sheet.svg   # 🎮 CHARACTER SHEET（洋红）
│   ├── section-research.svg     # 🔬 RESEARCH FOCUS（青）
│   ├── section-arsenal.svg      # ⚡ TECH ARSENAL（橙）
│   ├── section-projects.svg     # 🚀 FEATURED PROJECTS（洋红）
│   ├── section-stats.svg        # 📊 STATS CONSOLE（青）
│   ├── section-arcade.svg       # 🕹️ CONTRIBUTION ARCADE（绿）
│   ├── section-connect.svg      # 📡 CONNECT（洋红）
│   └── footer-rift.svg          # 页脚
└── notes/                  # 交流记录（gitignore）
    ├── 01-basic-info.md
    ├── 02-github-research.md
    ├── 03-design-v1.md
    ├── 04-project-status.md  ← 当前文件
    └── repos.json            # API 获取的仓库数据
```

---

## 6. README 板块结构（v2）

```
<div align="center">  ← 全局包裹
  neon-header.svg     ← 霓虹头部横幅
  status-bar.svg      ← 状态条
  访客计数器
  typing-svg          ← EN↔CN 交替打字动画
  section-char-sheet  ← 角色面板 + 当前任务（双列表格）
  section-research    ← 研究方向徽章
  section-arsenal     ← 技能图标 + 装备表格
  section-projects    ← 8个项目表格
  section-stats       ← GitHub 统计（stats, langs, streak, graph）
  section-arcade      ← 贡献图 + 蛇形动画
  section-connect     ← 联系徽章
  footer-rift.svg     ← 页脚
</div>
```

---

## 7. 待办事项

### 高优先级
- [ ] **改为纯英文**（用户最新指示）
- [ ] 等待用户提供内容文档，规范化文案

### 中优先级
- [ ] 配置 GitHub Actions 自动更新蛇形动画
- [ ] 添加邮箱等联系方式
- [ ] 进一步优化沉浸感（可能需要更复杂的 SVG 或 CSS）

### 低优先级
- [ ] 3D 贡献墙
- [ ] 更多动画效果
- [ ] Profile summary cards（类似学长的折叠面板）

---

## 8. 已知问题 & 用户反馈

| 反馈 | 状态 |
|------|------|
| "一块一块不好看" → 模块孤立 | ✅ v2 已修复：去掉了 `---`，添加了连续 SVG section 头图 |
| "文字不要 fancy，要好读" | ✅ v2 已采纳：正文保持标准 Markdown |
| 设计注释不应出现在 README | ✅ 已清理 HTML 注释 |
| 改为纯英文 | ❌ 尚未执行 |
| 整体效果仍不尽如人意 | ⚠️ 等待内容文档后重新打磨 |

---

## 9. Git 提交历史

```
07ffb72 v2: Immersive terminal — continuous dark theme, neon section headers
c2d5fba Merge: resolve conflict & clean design comments from README
6ac79f5 🚀 v1.0: Cyberpunk neon terminal profile README
```
