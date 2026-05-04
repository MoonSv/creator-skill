---
name: creator-skill
description: 小红书内容创作全能助手 - 三大功能：(1)发布建议：给主题+图片生成完整发布策略报告；(2)帖子诊断：分析已发布帖子的数据表现，对比竞品找出差距，给出改进建议；(3)账号分析：分析博主账号整体数据和内容表现，生成运营建议报告。当用户提到发小红书、写笔记、内容创作、帖子数据分析、流量诊断、转化率优化、账号分析、账号运营、涨粉策略、分析我的小红书、我的帖子数据怎么样、探店/好物/穿搭分享，或给出一个小红书帖子链接/用户主页链接让你分析时，都应触发。涉及 Xiaohongshu / XHS / RED / 小红书的任何内容创作、数据分析、运营优化需求都适用。
version: 2.0.0
---

# Creator Skill - 小红书内容创作助手

三大功能模式，统一输出自包含的交互式 HTML 报告。

## Phase 0: 环境检查（共用）

静默执行。不要尝试读取、输入或获取任何密码、钥匙串凭据、cookie 值。

```bash
export PATH="$HOME/.local/bin:$PATH" && which xhs
```

如果 xhs 未安装，说一句 `请先运行 ./install.sh 完成安装` 然后停止。

如果已安装，用一次搜索测试登录状态：

```bash
xhs search "测试" --sort time 2>&1 | head -5
```

返回正常结果说明已登录。如果返回错误，告知用户：

> 小红书未登录。请在终端运行 `xhs login` 扫码登录（建议使用小号）。

## Phase 1: 意图识别与路由

根据用户输入判断模式：

| 用户输入特征 | 模式 | 执行 |
|-------------|------|------|
| 提供主题 + 图片文件夹路径 | **A: 发布建议** | 继续下方 Phase 2-8 |
| 提供帖子 URL 或说"分析我的帖子/笔记" | **B: 帖子诊断** | 读取 `references/post-diagnosis.md` 并执行 |
| 提供用户主页 URL 或说"分析我的账号" | **C: 账号分析** | 读取 `references/account-analysis.md` 并执行 |

如果无法判断，问一次：

> 你想做什么？(1) 准备发一条新笔记 (2) 分析一条已发布的帖子数据 (3) 分析一个账号的整体表现

**模式 B 和 C 的完整指令在 references 文件中**，读取后按其中的步骤执行。以下是模式 A 的流程。

---

## 共用：安全红线

所有模式都遵守：

- 只做读取操作。xhs-cli 的写操作一旦被检测到自动化行为，账号会被限流甚至封禁。
- 每次 xhs 命令之间：`sleep $((RANDOM % 3 + 3))`。频繁请求会触发小红书风控。
- 任何命令返回错误或验证码，立即停止采集并告知用户。不要重试。
- 不要读取、请求或获取密码、cookie、钥匙串凭据。
- 使用计数器跟踪请求数量。模式A ≤ 30，模式B ≤ 20，模式C ≤ 25。

---

## 模式 A: 发布建议（主题 + 图片 → 报告）

### Phase 2: 理解用户意图

提取**主题**和**图片路径**。两项都缺时合并提问一次：

> 告诉我你想发的主题和图片文件夹路径，例如：「北京五一手帐集市，图片在 ~/Photos/shouzhan/」

### Phase 3: 数据采集

#### 3.1 搜索热门帖子
```bash
xhs search "{{主题}}" --sort popular
```

#### 3.2 搜索最新帖子
```bash
xhs search "{{主题}}" --sort latest
```

#### 3.3 扩展关键词搜索（1-2次）
```bash
xhs search "{{相关关键词}}" --sort popular
```

#### 3.4 读取 Top 帖子详情（5-8个）
必须使用搜索结果返回的完整 URL（含 xsec_token）。
```bash
xhs read {{note_url}}
```

#### 3.5 读取评论（3-5个帖子）
```bash
xhs comments {{note_url}} --limit 20
```

#### 3.6 博主信息（3-5个）
```bash
xhs user {{user_id}}
```

#### 3.7 热门趋势（如有余量）
```bash
xhs hot
```

### Phase 4: 数据分析

1. **爆款特征**：标题模式、内容结构、图片风格、标签策略
2. **博主画像**：粉丝分层、互动率、内容风格、发布频率
3. **互动分布**：收藏高（干货型）vs 点赞高（情绪型）vs 评论高（争议型）
4. **时效性**：热度阶段、发布窗口
5. **差异化机会**：共性 vs 缺失角度

### Phase 5: 图片分析

```bash
find {{图片文件夹}} -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.heic" -o -iname "*.webp" \) | sort
```

HEIC 先转 JPEG：`sips -s format jpeg -Z 1200`。用 Read 工具查看每张图片。

输出：推荐发布图片（6-9张排序）+ 封面图 + 排除理由。超过 20 张优先分析前 15 张。

### Phase 6: 封面头图生成

| 内容类型 | 模板 |
|----------|------|
| 教程/攻略/干货 | `bold_text` |
| 生活方式/穿搭/美食 | `magazine` |
| 日常/心情/记录 | `minimal` |
| 对比/测评 | `split` |

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/scripts/generate-cover.py "{{封面图}}" "{{标题}}" --all-templates
```

### Phase 7: 内容建议

1. **标题候选**（3-5个）+ 设计思路
2. **正文结构**：hook → 要点 → 互动引导，300-800字
3. **话题标签**（8-15个）：大流量 + 精准 + 长尾
4. **发布时间**：工作日 18-22点，周末 10-12/20-22点

### Phase 8: 生成 HTML 报告

读取模板和格式参考：
```
Read ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/assets/report.html
Read ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/references/html-format.md
```

图片 base64 内嵌。超过 2MB 先压缩到 800px 宽度。

保存并打开：
```bash
open "${CLAUDE_PLUGIN_ROOT}/output/report_{{主题简称}}_{{日期}}.html"
```
