---
name: creator-skill
description: 小红书内容创作助手 - 基于实时数据生成完整发布建议。当用户提到发小红书、写笔记、内容创作、标题优化、封面制作、探店分享、好物推荐、穿搭分享，或提到图片文件夹想做社交媒体发布，甚至只是说"帮我分析下这个话题在小红书怎么发"，都应该触发。涉及 Xiaohongshu / Little Red Book / XHS / RED 的任何内容规划都适用。即使用户没有明确说"小红书"，只要意图是中文社交媒体图文内容创作，也优先考虑触发。
version: 1.0.0
---

# Creator Skill - 小红书内容创作助手

根据用户提供的主题和本地图片，分析小红书实时数据，生成一份自包含的交互式 HTML 发布建议报告。

## Phase 0: 环境检查

静默执行，不打扰用户：

```bash
export PATH="$HOME/.local/bin:$PATH" && which xhs && xhs status
```

如果 xhs 未安装或未登录，只说一句 `请先运行 ./install.sh 完成安装（项目目录下）`，然后停止。一切正常则直接进入下一步。

## Phase 1: 理解用户意图

从用户消息中直接提取**主题**和**图片路径**。不要逐个追问——如果两项都缺，合并成一次提问：

> 告诉我你想发的主题和图片文件夹路径，例如：「北京五一手帐集市，图片在 ~/Photos/shouzhan/」

其他信息（目标受众、账号定位等）全部自动推断。

## Phase 2: 小红书数据采集

### 为什么要限速

xhs-cli 调用的是小红书的内部接口。频繁请求会触发风控系统——轻则弹验证码打断采集，重则需要重新登录甚至封号。所以每次请求之间随机等待 3-5 秒，单次运行总请求控制在 30 次以内。

### 安全红线

- 只做读取操作。因为 xhs-cli 的写操作（like/comment/post）一旦被检测到自动化行为，账号会被立即限流甚至永久封禁，所以绝不执行任何写操作。
- 任何命令返回错误或提示验证码，立即停止全部采集并告知用户。不要重试——重试只会加重风控。
- 使用计数器跟踪请求数量，确保 ≤ 30。

### 采集步骤

每次 xhs 命令之间执行：`sleep $((RANDOM % 3 + 3))`

#### 2.1 搜索热门帖子
```bash
xhs search "{{主题}}" --sort popularity
```

#### 2.2 搜索最新帖子
```bash
xhs search "{{主题}}" --sort time
```

#### 2.3 扩展关键词搜索（1-2次）
根据主题拆分相关关键词补充搜索。例如主题"北京五一hello手帐集市"可搜索"手帐集市""hello手帐"。
```bash
xhs search "{{相关关键词}}" --sort popularity
```

#### 2.4 读取 Top 帖子详情（5-8个）
从搜索结果中选互动最高的帖子。必须使用搜索结果返回的完整 URL（含 xsec_token），因为小红书用这个 token 做防盗链校验，自行拼接 note_id 会 403。
```bash
xhs read {{note_url}}
```

#### 2.5 读取评论（3-5个帖子）
```bash
xhs comments {{note_url}} --limit 20
```

#### 2.6 博主信息（3-5个）
```bash
xhs user {{user_id}}
```

#### 2.7 热门趋势（如有余量）
```bash
xhs hot
```

## Phase 3: 数据分析

基于采集数据分析：

1. **爆款特征**：标题模式（句式、emoji、数字列表）、内容结构（开头hook、正文节奏、互动引导）、图片数量和风格、标签策略
2. **博主画像**：粉丝量级分层、互动率（总互动/粉丝数）、内容风格、发布频率
3. **互动分布**：点赞/收藏/评论的中位数和最高值，哪类内容收藏高（干货型）vs 点赞高（情绪型）vs 评论高（争议型）
4. **时效性**：当前热度阶段、是否还有发布窗口
5. **差异化机会**：现有内容的共性 vs 缺失的角度

## Phase 4: 图片分析

查找用户文件夹内所有图片：

```bash
find {{图片文件夹}} -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.heic" -o -iname "*.webp" \) | sort
```

HEIC 文件需要先转换为 JPEG 才能用 Read 工具查看（macOS 可用 `sips -s format jpeg -Z 1200`）。

对每张图片用 Read 工具查看，评估：内容相关性、视觉质量、小红书审美适配度（明亮/精致/有氛围感）、封面潜力、叙事位置。

**输出决策：**
- 推荐发布图片（排好顺序，6-9 张最佳），每张给出选用理由
- 最佳封面图 + 详细理由
- 不推荐的图片 + 排除理由
- 超过 20 张图片时，优先分析画质最好的前 15 张

## Phase 5: 封面头图生成

基于 Phase 3 的竞品分析选择模板：

| 内容类型 | 模板 | 风格 |
|----------|------|------|
| 教程/攻略/干货 | `bold_text` | 大字报风（底部大字+渐变遮罩） |
| 生活方式/穿搭/美食 | `magazine` | 杂志风（顶部白色条带+标题） |
| 日常/心情/记录 | `minimal` | 简约清新（中央卡片式标题） |
| 对比/测评 | `split` | 上图下文（上2/3图+下1/3文字区） |

生成所有模板供用户选择：
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/scripts/generate-cover.py "{{封面图路径}}" "{{推荐标题}}" --all-templates
```

或指定模板：
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/scripts/generate-cover.py "{{封面图路径}}" "{{推荐标题}}" --template {{模板名}} --subtitle "{{副标题}}"
```

## Phase 6: 生成内容建议

1. **标题候选**（3-5个）：参考爆款模式，融入热门关键词，每个说明设计思路
2. **正文结构**：开头 hook（前两行决定展开）→ 正文要点 → 互动引导语（问句收尾），300-800 字
3. **话题标签**（8-15个）：3-5个大流量通用 + 3-5个精准主题 + 2-3个长尾
4. **发布时间**：基于该类内容互动高峰（通常工作日 18:00-22:00，周末 10:00-12:00/20:00-22:00）

## Phase 7: 生成 HTML 报告

读取报告模板：
```bash
Read ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/assets/report.html
```

读取占位符和 HTML 片段格式参考：
```bash
Read ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/references/html-format.md
```

按照 `html-format.md` 中的说明，将所有分析数据填充到模板的占位符中。图片以 base64 内嵌确保自包含：

```bash
base64 -i "{{图片路径}}" | tr -d '\n'
```

单张图片超过 2MB 时，先压缩到 800px 宽度再嵌入。

## Phase 8: 输出报告

保存到：
```
${CLAUDE_PLUGIN_ROOT}/output/report_{{主题简称}}_{{日期}}.html
```

在浏览器中打开：
```bash
open "${CLAUDE_PLUGIN_ROOT}/output/report_{{文件名}}.html"
```

告知用户报告已生成，并提供核心建议摘要（3-5句话）。
