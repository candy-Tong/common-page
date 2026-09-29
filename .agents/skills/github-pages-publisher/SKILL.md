---
name: github-pages-publisher
description: >-
  将静态网页安全发布到 GitHub Pages，并验证“仓库已写入 → Pages 构建成功 → 公网 URL 真正上线 → 页面内容版本一致”的完整链路。
  适用于用户要求“部署到 GitHub”“部署到 common-page”“给我公网地址”“更新 GitHub Pages 页面”等任务。
metadata:
  version: "1.0"
  updated: "2026-09-29"
---

# GitHub Pages 发布 Skill

## 目标

不要把“文件提交成功”误报成“网站已经上线”。

一个发布任务只有在以下四层分别确认后才算完成：

1. **源码层**：目标文件已经写入正确仓库和正确分支。
2. **构建层**：GitHub Pages 对应 commit 的构建 / deploy job 成功。
3. **公网层**：最终页面 URL 返回 HTTP 200，且资源路径正确。
4. **版本层**：公网页面确实是本次提交的版本，而不是 CDN / Pages 旧缓存。

如果任一层未确认，必须准确说明当前停在哪一层。

---

## 1. 先判断发布目标

优先复用用户已经指定或已存在的 Pages 仓库，不擅自新建仓库。

对于本仓库 `candy-Tong/common-page`：

- Pages 根地址：`https://candy-tong.github.io/common-page/`
- 默认分支：`main`
- Pages 来源：仓库根目录
- 每个独立项目放在：
  `<type>/<topic>/<project>/index.html`
- 不允许用单个项目覆盖根目录 `index.html`
- 必须保留 `.nojekyll`

如果用户没有指定仓库，但上下文明显是在延续 common-page 的研究页发布，默认继续使用 common-page，不重复询问。

如果是其他仓库，先读取：
- 仓库默认分支
- 现有目录结构
- Pages 配置 / workflow
- 项目级 `AGENTS.md` 或同类规则文件

---

## 2. 写入前先读取当前状态

在修改之前至少检查：

- 当前 branch / HEAD commit
- 目标路径是否已存在
- 根目录规则文件
- `sites.json` 或其他站点清单
- Pages workflow / deploy 配置
- 与目标目录同级的现有项目，避免覆盖

对于 common-page，还必须先读 `AGENTS.md`。

如果是研究型可视化页面，同时读取：
`.agents/skills/map-claims-and-evidence/SKILL.md`

这样可以确保发布流程不会破坏研究来源映射、案例覆盖与模拟数据标注。

---

## 3. 选择稳定的多级路径

路径原则：

- 全小写
- 使用短横线
- 目录以 `/` 结尾
- 不能包含 `//`
- 不重命名已有公开路径
- 每个项目拥有自己的 HTML / CSS / JS / 资源目录

示例：

`research/agents/claude-eval-hillclimb/`

对应公网地址：

`https://candy-tong.github.io/common-page/research/agents/claude-eval-hillclimb/`

不要把多个研究页都塞进根目录。

---

## 4. 注册站点清单

common-page 使用 `sites.json` 作为首页目录。

新增页面时必须“追加”一项，保留所有已有条目。

必填字段：

- `id`
- `title`
- `description`
- `category`
- `path`
- `date`
- `tags`

示例：

```json
{
  "id": "claude-eval-hillclimb",
  "title": "Claude 自动评估设计与 Hillclimbing",
  "description": "原文、官方工作流、实验结果、交互示例和方法边界。",
  "category": "研究 / AI AGENTS",
  "path": "research/agents/claude-eval-hillclimb/",
  "date": "2026-09-29",
  "tags": ["Claude", "Eval", "Hillclimb", "Agent"]
}
```

不要删除或重排无关项目，除非用户明确要求。

---

## 5. 静态页面发布约束

### 链接

- 项目内部资源优先使用相对路径。
- 不使用 `/assets/...` 这种会逃出 `/common-page/` 的绝对路径。
- 外部链接保留完整 URL。

### 内容

- 不提交 API key、token、cookie、私有工单、账号凭据或本机秘密。
- 模拟数据必须明确标注为模拟。
- 作者报告、源码事实、助手分析要分开。
- 不把本地测试结果写成线上真实模型结果。

### 交互

发布前检查：
- 桌面尺寸
- 手机尺寸
- 导航锚点
- 图谱缩放 / 点击
- 计算器
- 本地 CSS / JS / 图片资源

---

## 6. 提交 GitHub

用户明确要求“用 GitHub 部署”时，优先通过 GitHub connector 完成仓库写入。

推荐流程：

1. 读取最新 HEAD。
2. 创建或更新目标文件。
3. 更新 manifest / 站点清单。
4. 如果一次涉及多个文件，尽量形成一个语义清晰的 commit。
5. commit message 说明发布对象，例如：
   `Publish Claude eval hillclimbing research page`

不要使用浏览器自动化去绕过已有 GitHub connector。

---

## 7. 构建成功不等于公网已验证

提交后找到与 **本次 commit SHA** 对应的 Pages workflow run。

必须确认：

- `head_sha == 本次 commit SHA`
- workflow status = `completed`
- conclusion = `success`
- deploy job = `success`

如果只看到旧 workflow 成功，不能算本次已发布。

如果 Pages 正在构建，就继续读取本次 workflow 状态；不要用旧版本 HTTP 200 代替。

---

## 8. 公网验证

构建成功后验证：

1. Pages 根目录 HTTP 200。
2. `sites.json` HTTP 200。
3. 目标多级路径 HTTP 200。
4. 页面引用的本地 CSS / JS / image 均 HTTP 200。
5. manifest 已包含本项目。

对于 common-page，可以复用 `.github/workflows/verify-pages.yml` 的校验逻辑。

如果自动 verify workflow 没有被本次 deploy 触发，可以：
- 检查 workflow 条件；
- 在不修改源码的情况下重新运行验证 job；
- 明确说明它验证的是当前线上内容。

---

## 9. 防止“200 但仍是旧页面”

HTTP 200 只说明“某个页面存在”。

对重要更新，还要进行版本一致性检查，至少满足一种：

- 页面包含当前 commit / version marker；
- 公网页面关键标题、段落或项目 ID 与本次构建一致；
- 对正文或构建产物计算内容 hash，并与部署 artifact / 本地测试文件比对；
- GitHub Pages artifact 明确来自本次 `head_sha`，再结合目标 URL 内容检查。

如果公网仍返回旧内容，不得说“已经更新完成”。

---

## 10. 发布完成后的用户回复

完成时尽量短，给用户最有用的三个东西：

1. **公网页面**
2. **源码目录 / commit**
3. **部署或验证记录**

推荐格式：

> 已通过 GitHub Pages 发布并验证：
>
> 页面：<public URL>
>
> 源码：<repository path>
>
> Commit：<sha>
>
> Pages 构建：success；公网目标路径：HTTP 200。

如果构建成功但公网内容还没更新，就明确写：
“源码和 Pages 构建已完成，但公网内容一致性尚未确认。”

---

## 11. common-page 专用发布清单

执行前：
- [ ] 读 `AGENTS.md`
- [ ] 读当前 `sites.json`
- [ ] 确认目标目录不覆盖已有项目
- [ ] 研究页时读 research skill

写入：
- [ ] `<type>/<topic>/<project>/index.html`
- [ ] 需要时放同目录 CSS / JS / assets
- [ ] 追加 `sites.json`
- [ ] 保留 `.nojekyll`

验证：
- [ ] `python scripts/check.py`（能运行本地副本时）
- [ ] 桌面与手机
- [ ] 交互
- [ ] Pages workflow 对应本次 commit
- [ ] 公网根页 HTTP 200
- [ ] 公网目标页 HTTP 200
- [ ] `sites.json` HTTP 200
- [ ] 内容版本一致

---

## 12. 常见错误

### 错误 A：commit 成功就回复“部署完成”
不通过。必须继续确认 Pages 构建和公网地址。

### 错误 B：只检查根域名
不通过。必须检查最终多级路径。

### 错误 C：拿旧版页面的 200 当本次上线
不通过。核对 workflow `head_sha` 和内容版本。

### 错误 D：覆盖 common-page 根 index
不通过。独立项目应放自己的多级目录。

### 错误 E：更新页面但忘了 sites.json
不通过。这样首页无法发现新项目。

### 错误 F：部署时顺便删除别的项目
不通过。发布任务默认只做增量变更。

### 错误 G：用 GitHub connector 已经能做的事改用浏览器登录
不通过。用户要求 GitHub workflow 时优先 connector。

---

## 13. 这次流程的回归案例

### R1：新研究页发布
输入：用户说“调研这个，并用 GitHub 部署”。
通过：
- 新建独立多级路径；
- 更新站点 manifest；
- 提交 main；
- Pages run 对应新 SHA 成功；
- 最终 URL HTTP 200；
- 回复公网地址。

### R2：页面文件存在，但 Pages 还在构建
不通过：立即回复“已部署完成”。
通过：区分“已提交”和“已上线”。

### R3：公网 URL 返回 200，但正文仍是旧版
不通过：只报告 200。
通过：核对当前 commit 的版本标记、关键内容或构建 artifact。

### R4：仓库已有多个站点
不通过：用新研究页覆盖根目录。
通过：保持根首页和旧项目不变，只新增路径与 manifest 项。

### R5：用户要求“用 GitHub 部署”
不通过：改用临时 Cloudflare tunnel 作为最终交付。
通过：以 GitHub Pages 作为正式公网地址；临时预览只能作为发布前检查手段。
