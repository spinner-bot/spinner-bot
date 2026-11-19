# 贪吃蛇贡献图停更事件记录

| 项目 | 内容 |
| --- | --- |
| 发现时间 | 2026-11-19 |
| 影响范围 | 主页 README 的贪吃蛇贡献图（`spinner-bot/spinner-bot` → `output` 分支） |
| 停更时长 | 2026-10-11 02:56 UTC ~ 2026-11-19 14:06 UTC，约 39 天 |
| 失败运行次数 | 188 次（全部失败，无人察觉） |
| 根因 | 工作流里 `env: GITHUB_TOKEN: ${{ secrets.SNK_TOKEN }}` 的取值失效，空/无效 token 让动作在 1 秒内失败 |
| 状态 | 已修复并验证 |

---

## 1. 现象

2026-11-19 发现主页的贪吃蛇贡献图停留在 2026-10-11 的样子，之后一个多月没有任何变化。

## 2. 先排除"图片缓存"

这类问题最常见的假象是缓存，所以先查了**数据源本身**：

- README 引用的是 `https://raw.githubusercontent.com/spinner-bot/spinner-bot/output/github-contribution-grid-snake.svg`；
- 该 `output` 分支的最后一次提交是 `524806b`，时间 `2026-10-11T02:56:08Z`，提交信息 `Update snake animation [skip ci]`。

也就是说，**图片文件本身真的停在 10 月 11 日**，不是浏览器或 GitHub 图片代理（camo）的缓存问题。
继续往前查调度记录，`Generate Snake Animation` 工作流自 10 月 11 日之后每一次运行都是 `failure`。

## 3. 关键证据：失败发生在"第 1 秒"

对比两次运行的步骤耗时：

| 运行 | 步骤 | 耗时 |
| --- | --- | --- |
| 成功（2026-10-11 02:55Z） | `Generate snake SVG` | 正常执行 |
| 失败（2026-10-14 23:54Z） | `Checkout repository` | success 2s |
| 失败（2026-10-14 23:54Z） | `Generate snake SVG` | **failure，1 秒** |
| 失败（2026-10-14 23:54Z） | `Push SVGs to output branch` | skipped |

失败的第一步之前的步骤都成功，失败发生在真正调用 `Platane/snk/svg-only@v3` 的时候，而且**只用 1 秒**——脚本根本没跑起来，是动作一启动就报错退出。

## 4. 根因

`svg-only` 动作（`v3`，commit `d8f6715`）的 `dist/index.js` 里有这样一行：

```js
const githubToken = process.env.GITHUB_TOKEN ?? getInput("github_token");
```

- `getInput("github_token")` 的默认值是 `${{ github.token }}`，正常情况下**根本不需要**额外传 token；
- 但工作流在第 3 步写了 `env: GITHUB_TOKEN: ${{ secrets.SNK_TOKEN }}`；
- 一旦 `SNK_TOKEN` 这个 secret 不存在（值为空），表达式解析结果是**空字符串 `""`**；
- `??` 是"空值合并"，**只对 `null` / `undefined` 回退**，空字符串不会回退；
- 于是动作拿着一个空 token 去请求 GitHub API → 401 → 立刻 `setFailed` → 1 秒内失败。

### 为什么会在这个时间点开始坏

`SNK_TOKEN`（一个 `read:user` 的 PAT）是 2026-09-10 的提交 `663c581` 加进来的，目的是把私有仓库的贡献也算进去。
9 月 10 日到 10 月 11 日之间它一直有效，所以能正常出图；**10 月 11 日前后这个 secret 消失或变成空值**
（PAT 过期后被删、或仓库 secret 被清理），工作流从此每次都拿空 token。

> 依据：最终方案 `secrets.SNK_TOKEN || secrets.GITHUB_TOKEN` 能立刻恢复正常，说明 `SNK_TOKEN` 当前解析结果确实为假值（空）。

巧合的是，同一时间（10 月 11 日下午）正在为深色模式的蛇加背景色，当天的几次提交让工作流折腾了一番，最后又改回了原样——**文件内容其实没变，坏掉的不是 YAML，而是那个 secret。**

### 为什么没人发现

- 定时任务失败不会通知；
- 图片没更新时，浏览器会继续显示上一次成功加载的旧图，看起来"只是没更新"；
- 主页 README 一切正常，没有报错提示。

## 5. 对照实验

为了确认到底是哪一行导致的，在同一仓库做了三次对照（每次提交后立即触发运行）：

| 提交 | 该步骤的 `env` | 结果 |
| --- | --- | --- |
| `1f5b914` | 不传 `GITHUB_TOKEN`（走动作默认值） | ✅ success，耗时 6s |
| `62e51f6` | `GITHUB_TOKEN: ${{ secrets.SNK_TOKEN }}` | ❌ failure，耗时 1s |
| `ba325a3` | `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` | ✅ success |
| `eb46405` | `GITHUB_TOKEN: ${{ secrets.SNK_TOKEN \|\| secrets.GITHUB_TOKEN }}` | ✅ success（最终方案） |

结论明确：**问题就是 `SNK_TOKEN` 取到了空值**，换成任何非空 token 都能恢复。

## 6. 修复

`.github/workflows/snake.yml` 做了两处改动：

1. **token 取值加兜底**，PAT 有效时仍然优先使用（保留纳入私有贡献的能力），失效时自动退回内置 token：

   ```yaml
   env:
     GITHUB_TOKEN: ${{ secrets.SNK_TOKEN || secrets.GITHUB_TOKEN }}
   ```

2. **发布步骤改用 `crazy-max/ghaction-github-pages@v4`**，替换掉原来手写的
   `git checkout --orphan output` + `git rm -rf .` + `git push --force` 脚本。
   `--orphan` 与 `--force` 的组合本身比较脆弱，换成社区通用的发布动作更稳，
   也少一次 `actions/checkout`。

提交记录（小步提交）：

- `1f5b914` ci(snake): 简化为与另一账号一致的可靠流程
- `62e51f6` test(snake): 临时加回 env GITHUB_TOKEN，验证是否为失败原因
- `ba325a3` test(snake): 用内置 GITHUB_TOKEN 替换 SNK_TOKEN，进一步定位空值问题
- `eb46405` fix(snake): SNK_TOKEN 缺失时回退到内置 token

## 7. 验证

- 修复后的运行 `2026-11-19T14:09Z`（提交 `eb46405`）成功；此前 `1f5b914`、`ba325a3` 也已各自验证成功；
- `output` 分支更新到 `2a56a9f`，时间 `2026-11-19T14:09:35Z`；
- 新生成的 `github-contribution-grid-snake.svg` 已包含最近一个月的贡献数据。

GitHub 的图片代理通常几分钟内刷新；若浏览器仍显示旧图，强制刷新或换用无痕窗口即可。

## 8. 后续建议

1. **要不要恢复私有贡献**：如需包含私有仓库的贡献，到 Settings → Developer settings → Personal access tokens 重新生成一个带 `read:user` 的 PAT，
   存成仓库 secret `SNK_TOKEN` 即可，**不需要改工作流**（兜底表达式会自动优先使用它）。
2. **加失败告警**：定时任务静默失败是这次问题的最大教训。可考虑在失败时给工作流加一个通知步骤，或定期看一眼 Actions 页。
3. **提交保持小步**：这次的诊断过程本身也是靠四次小提交 + 每次立即运行来实现的，比一次性大改更容易定位。

## 附录：相关链接

- 工作流：`.github/workflows/snake.yml`
- 图片产物：`output` 分支的 `github-contribution-grid-snake.svg` / `-dark.svg`
- 上游动作：[Platane/snk](https://github.com/Platane/snk)
