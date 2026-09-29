# Common Page · 研究与交互网页

多个独立静态网页的统一托管仓库。每个项目使用自己的多级路径，不覆盖其他项目。

## 页面目录

| 页面 | 仓库内路径 |
| --- | --- |
| 网页总入口 | `index.html` |
| 谁来做判断？Jev × Claude 深度研究 | `research/agents/jev-claude/index.html` |

GitHub Pages 目标入口：`https://candy-tong.github.io/common-page/`。

本篇目标路径：`https://candy-tong.github.io/common-page/research/agents/jev-claude/`。

目标地址是否已上线，以 Pages 构建结果和实际 HTTP 访问为准；提交源码不等于发布完成。

## 新增网页

使用 `<类型>/<主题>/<项目>/index.html`，例如 `research/agents/jev-claude/`。页面专属资源放在自己的目录中，使用相对路径；更新根目录 `sites.json` 后，首页会自动收录。

请保留已有项目路径，不要将新项目覆盖到根首页。不得提交密钥、账户令牌、个人敏感信息或未获授权公开的内容。

## 本地检查

```sh
python scripts/check.py
python -m http.server 8000
```

研究页面保留原有来源、核查日期及模拟数据标记。模型调用演示是教学模拟，不调用真实模型 API，资料及价格不代表实时数据。
