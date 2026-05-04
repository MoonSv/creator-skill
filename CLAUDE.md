# Creator Skill - 小红书内容创作助手

基于小红书实时数据分析的 Claude Code Plugin，支持三大功能。

## 功能

| 模式 | 输入 | 输出 |
|------|------|------|
| **A: 发布建议** | 主题 + 图片文件夹 | 完整发布策略报告 |
| **B: 帖子诊断** | 帖子 URL | 数据诊断 + 竞品对比 + 改进建议 |
| **C: 账号分析** | 博主主页 URL 或"分析我的账号" | 账号数据分析 + 运营建议 |

## 项目结构

```
creator-skill/
├── .claude-plugin/plugin.json
├── install.sh
├── scripts/setup.sh
├── skills/creator-skill/
│   ├── SKILL.md                        # 主指令（路由 + 模式A）
│   ├── scripts/generate-cover.py       # 封面生成
│   ├── references/
│   │   ├── html-format.md              # 模式A HTML 格式
│   │   ├── post-diagnosis.md           # 模式B 帖子诊断指令
│   │   └── account-analysis.md         # 模式C 账号分析指令
│   └── assets/
│       ├── report.html                 # 模式A 报告模板
│       ├── report-diagnosis.html       # 模式B 报告模板
│       └── report-account.html         # 模式C 报告模板
└── output/                             # 生成的报告（gitignored）
```

## 安装

```bash
git clone https://github.com/MoonSv/creator-skill.git && cd creator-skill && ./install.sh
```

## 安全原则

- 只读操作，不发帖/点赞/评论
- 请求间隔 3-5 秒，单次运行 ≤30 请求
- 建议使用小号进行数据采集
