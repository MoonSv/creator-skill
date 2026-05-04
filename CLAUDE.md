# Creator Skill - 小红书内容创作助手

基于小红书实时数据分析生成发布建议的 Claude Code Plugin。

## 项目结构

```
creator-skill/
├── .claude-plugin/plugin.json          # Plugin 注册配置
├── install.sh                          # 一键安装脚本
├── scripts/setup.sh                    # 环境依赖安装
├── skills/creator-skill/
│   ├── SKILL.md                        # 主 Skill 指令
│   ├── scripts/generate-cover.py       # 封面头图生成（Pillow, 4模板）
│   ├── references/html-format.md       # HTML 占位符与片段格式参考
│   └── assets/report.html              # HTML 报告模板
├── fonts/                              # 备用中文字体
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
