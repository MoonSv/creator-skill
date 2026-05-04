# 模式 B: 帖子诊断 — 执行指令

## 输入

用户提供：
- 一个小红书帖子 URL（如 `https://www.xiaohongshu.com/explore/xxx`）
- 或者描述自己的某条帖子（需要引导用户提供 URL 或通过 `xhs my-notes` 找到）

如果用户只说"帮我看看我的帖子"但没给链接，用 `xhs my-notes` 列出最近的帖子让用户选。

## 采集步骤（≤20 次请求）

每次 xhs 命令之间：`sleep $((RANDOM % 3 + 3))`

### B.1 读取目标帖子
```bash
xhs read {{帖子URL}}
```
提取：标题、正文、图片数量、点赞/收藏/评论数、发布时间、话题标签、作者 user_id。

### B.2 读取帖子评论
```bash
xhs comments {{帖子URL}} --limit 20
```
分析评论情绪和反馈方向。

### B.3 获取发帖者信息
```bash
xhs user {{user_id}}
```
了解账号量级（粉丝数决定了数据预期基准——1000粉和10万粉的"好数据"标准完全不同）。

### B.4 提取关键词并搜索竞品
从帖子标题和标签中提取 2-3 个核心关键词。

```bash
xhs search "{{关键词1}}" --sort popular
```
```bash
xhs search "{{关键词2}}" --sort popular
```
```bash
xhs search "{{关键词}}" --sort latest
```

### B.5 读取竞品帖子详情（3-5个）
从搜索结果中选互动最高的帖子：
```bash
xhs read {{竞品URL}}
```

### B.6 读取竞品评论（2-3个）
```bash
xhs comments {{竞品URL}} --limit 20
```

## 分析框架

### 1. 数据健康度评分

计算以下指标并与同主题竞品对比：

- **绝对数据**：点赞、收藏、评论各多少
- **收藏/点赞比**：>0.5 干货价值高，0.2-0.5 正常，<0.1 缺乏收藏动机
- **评论/点赞比**：>0.1 互动性强，<0.03 缺乏讨论点
- **百分位排名**：在搜索到的同主题帖子中，该帖子的互动数据处于什么水平
- **账号量级基准**：基于粉丝数估算合理的互动数据范围

### 2. 标题诊断

与 Top 3 竞品标题逐项对比：
- 关键词覆盖：是否包含用户会搜索的高频词
- 句式：疑问句/感叹句/数字列表 哪种效果好
- 长度：该领域最佳标题长度区间
- Emoji：竞品用了多少、哪些位置
- 搜索 SEO：标题中的关键词在搜索结果中排名如何

### 3. 内容诊断

- **开头 Hook**：前两行是否有吸引力（竞品怎么写的）
- **正文结构**：信息密度、段落节奏、是否有干货/情绪价值
- **互动引导**：结尾是否有问句、投票、征集等引导评论的设计
- **内容长度**：与竞品对比是否在最佳区间
- **图片数量和质量**：与竞品对比

### 4. 标签诊断

- 标签数量是否在最佳区间（8-15个）
- 是否覆盖了大流量通用标签
- 是否有精准的长尾标签
- 竞品用了哪些标签是你没用的

### 5. 时机诊断

- 发布时间是否在互动高峰（工作日18-22点、周末10-12/20-22点）
- 该话题的时效性：发布时是在热度上升期还是下降期
- 是否有同期热点抢走了流量

### 6. 竞品差距分析（核心）

对 Top 3 竞品逐项对比，输出结构化表格：

| 维度 | 你的帖子 | 竞品1 | 竞品2 | 竞品3 |
|------|---------|-------|-------|-------|
| 标题 | ... | ... | ... | ... |
| 互动数据 | ... | ... | ... | ... |
| 内容结构 | ... | ... | ... | ... |
| 标签策略 | ... | ... | ... | ... |

明确指出"他们做了什么你没做"，找出最大的 1-3 个差距因素。

## 输出建议

分三个层次：
1. **立即可改**（如果帖子还能编辑）：优化标题、补充标签、修改互动引导语
2. **下次改进**：封面策略、内容结构、发布时间、图片选择
3. **数据预期**：基于同量级账号 + 同主题，给出合理的互动数据范围（"你的粉丝量级下，这个主题的正常互动量是 X-Y"）

## HTML 报告生成

读取模板：
```
Read ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/assets/report-diagnosis.html
```

### 占位符清单

| 占位符 | 内容 |
|--------|------|
| `{{POST_TITLE}}` | 帖子标题 |
| `{{POST_URL}}` | 帖子链接 |
| `{{POST_AUTHOR}}` | 作者昵称 |
| `{{POST_TIME}}` | 发布时间 |
| `{{POST_LIKES}}` | 点赞数 |
| `{{POST_COLLECTS}}` | 收藏数 |
| `{{POST_COMMENTS}}` | 评论数 |
| `{{AUTHOR_FOLLOWERS}}` | 作者粉丝数 |
| `{{AUTHOR_LEVEL}}` | 账号量级（素人/尾部/腰部/头部） |
| `{{GENERATED_TIME}}` | 报告生成时间 |
| `{{HEALTH_SCORE}}` | 数据健康度评分（如 6.5/10） |
| `{{HEALTH_LEVEL}}` | 健康度等级（优秀/良好/一般/较差） |
| `{{COLLECT_LIKE_RATIO}}` | 收藏/点赞比 |
| `{{COMMENT_LIKE_RATIO}}` | 评论/点赞比 |
| `{{PERCENTILE_RANK}}` | 同主题百分位排名 |
| `{{RADAR_DATA_JSON}}` | 雷达图数据（标题/内容/封面/标签/时机 五维） |
| `{{COMPARISON_CHART_JSON}}` | 竞品对比柱状图数据 |
| `{{COMPETITOR_CARDS}}` | 竞品帖子卡片 HTML |
| `{{TITLE_DIAGNOSIS}}` | 标题诊断内容 HTML |
| `{{CONTENT_DIAGNOSIS}}` | 内容诊断内容 HTML |
| `{{TAG_DIAGNOSIS}}` | 标签诊断内容 HTML |
| `{{TIMING_DIAGNOSIS}}` | 时机诊断内容 HTML |
| `{{GAP_ANALYSIS}}` | 差距分析表格 HTML |
| `{{IMMEDIATE_ACTIONS}}` | 立即可改建议 HTML |
| `{{NEXT_IMPROVEMENTS}}` | 下次改进建议 HTML |
| `{{DATA_EXPECTATIONS}}` | 数据预期说明 |

### HTML 片段格式

诊断项卡片（每个诊断维度用一个）：
```html
<div class="bg-white rounded-lg p-4 border-l-4 {{BORDER_COLOR}}">
    <div class="flex items-center justify-between mb-2">
        <h4 class="font-semibold text-gray-800">{{诊断维度}}</h4>
        <span class="text-xs px-2 py-1 rounded-full {{BADGE_COLOR}}">{{评分标签}}</span>
    </div>
    <p class="text-sm text-gray-600 mb-2">{{问题描述}}</p>
    <div class="bg-gray-50 rounded p-3 text-sm">
        <p class="text-gray-500 mb-1">竞品做法：</p>
        <p class="text-gray-700">{{竞品做法}}</p>
    </div>
    <div class="mt-2 bg-green-50 rounded p-3 text-sm">
        <p class="text-green-600 font-medium">建议：{{改进建议}}</p>
    </div>
</div>
```

border/badge 颜色：
- 优秀：`border-green-500` / `bg-green-100 text-green-700`
- 良好：`border-blue-500` / `bg-blue-100 text-blue-700`
- 一般：`border-yellow-500` / `bg-yellow-100 text-yellow-700`
- 较差：`border-red-500` / `bg-red-100 text-red-700`

竞品对比卡片：
```html
<div class="card bg-gray-50 rounded-lg p-4">
    <h4 class="font-medium text-gray-800">
        <a href="https://www.xiaohongshu.com/explore/{{note_id}}" target="_blank" class="hover:text-red-500">{{帖子标题}}</a>
    </h4>
    <p class="text-xs text-gray-500 mt-1">@{{作者}} · 点赞 {{点赞数}} · 收藏 {{收藏数}} · 评论 {{评论数}}</p>
    <p class="text-sm text-gray-600 mt-2">{{为什么这条数据好的分析}}</p>
</div>
```

行动建议项：
```html
<div class="flex items-start gap-3 py-2">
    <span class="flex-shrink-0 w-6 h-6 rounded-full bg-red-100 text-red-600 flex items-center justify-center text-xs font-bold">{{序号}}</span>
    <div>
        <p class="text-sm font-medium text-gray-800">{{建议标题}}</p>
        <p class="text-xs text-gray-500 mt-1">{{具体操作说明}}</p>
    </div>
</div>
```

保存并打开：
```bash
open "${CLAUDE_PLUGIN_ROOT}/output/diagnosis_{{帖子标题缩写}}_{{日期}}.html"
```
