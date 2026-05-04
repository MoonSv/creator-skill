# Creator Skill - 小红书内容创作助手

这是一个 Claude Code Plugin，帮助用户基于小红书实时数据分析生成优化的发布建议。

## 安装使用

### 方式1：本地安装（推荐）
```bash
# 克隆项目
git clone <repo-url> ~/Documents/creator-skill

# 注册为 Claude Code plugin
claude plugin add ~/Documents/creator-skill

# 安装依赖
bash scripts/setup.sh

# 登录小红书（建议用小号）
xhs login
```

### 方式2：手动注册
将本项目路径添加到 Claude Code 的 plugin 配置中。

## 使用方式

在 Claude Code 中直接说"我想发小红书"或描述你的发布主题，skill 会自动触发。

## 安全原则

- 只使用读取操作，绝不自动发帖/点赞/评论
- 请求间隔 3-5 秒，单次运行 ≤30 请求
- 建议使用小号进行数据采集
