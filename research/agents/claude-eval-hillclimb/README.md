# Claude 自动评估与优化研究

原始材料：<https://claude.dev/blog/automating-eval-design-and-hillclimbing/>

页面路径：`research/agents/claude-eval-hillclimb/index.html`

GitHub Pages 路由：<https://candy-tong.github.io/common-page/research/agents/claude-eval-hillclimb/>

## 内容

应用层优化定位、build-eval/hillclimb 流程、三个六步教学模拟、作者原始两组实验、15 节点 SVG 论证图、噪声计算器和实践说明。来源、作者报告、本页分析与教学模拟分别标注。

所有页面样式和脚本内联，无第三方运行时、模型调用或输入上传。共享首页与旧项目保持不变。来源覆盖边界见 `source-map.json`。

## 核查

从仓库根目录执行：

```sh
python scripts/check.py
python .agents/skills/map-claims-and-evidence/scripts/check_coverage.py research/agents/claude-eval-hillclimb/source-map.json research/agents/claude-eval-hillclimb/index.html
```

来源检查允许已披露的部分源码阅读，不代表完整实现审计或内部实验复现。发布需分别核对 Pages 工作流、实际公网 HTTP 状态与内容版本；单次提交不是部署完成证明。
