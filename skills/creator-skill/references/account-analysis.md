# 模式 C: 账号分析 — 执行指令

## 输入

三种方式：
1. 博主主页 URL（如 `https://www.xiaohongshu.com/user/profile/xxx`）
2. user_id
3. "分析我的小红书账号"（用 `xhs whoami` + `xhs my-notes`）

## 采集步骤（≤25 次请求）

每次 xhs 命令之间：`sleep $((RANDOM % 3 + 3))`

### C.1 获取账号信息

如果分析自己：
```bash
xhs whoami
```

如果分析其他博主：
```bash
xhs user {{user_id}}
```

提取：昵称、粉丝数、关注数、获赞与收藏、简介、认证信息。

### C.2 获取帖子列表

如果分析自己：
```bash
xhs my-notes
xhs my-notes --page 1
```

如果分析其他博主：
```bash
xhs user-posts {{user_id}}
xhs user-posts {{user_id}} --cursor {{cursor}}
```

翻 2-3 页，获取近期 20-30 条帖子的列表数据（标题、互动数据摘要）。

### C.3 读取代表性帖子详情（8-10个）

从帖子列表中选取不同表现水平的帖子：
- 互动最高的 3 条（爆款）
- 中等表现的 3 条
- 互动最低的 2-3 条（低迷款）

```bash
xhs read {{note_url}}
```

这种选法是为了对比分析"什么样的内容表现好、什么样的差"。

### C.4 读取爆款帖子评论（2-3条）
```bash
xhs comments {{note_url}} --limit 20
```

### C.5 搜索同领域对标博主

从帖子内容中提取该博主的核心领域关键词：
```bash
xhs search-user "{{领域关键词}}"
```

### C.6 获取对标博主信息（2-3个）

选粉丝量级相近或略高一档的博主：
```bash
xhs user {{对标博主_user_id}}
xhs user-posts {{对标博主_user_id}}
```

## 分析框架

### 1. 账号基础画像

- **量级定位**：
  - < 1000 粉：素人起步期
  - 1000-1万：尾部博主成长期
  - 1万-10万：腰部博主发展期
  - 10万+：头部博主
- **获赞与收藏总量**
- **单帖平均互动**：总互动 / 帖子数
- **粉丝质量推断**：平均互动 / 粉丝数（>5% 优秀，2-5% 正常，<1% 可能有僵尸粉）

### 2. 内容表现分析

- **帖子数据分布**：用散点图展示每条帖子的互动量，标注爆款和低迷款
- **互动趋势**：近期帖子 vs 早期帖子的互动走势（上升/平稳/下降）
- **内容类型分布**：图文 vs 视频、主题分类（按标签聚类）
- **发布频率**：平均几天发一条、是否有规律
- **最佳发布时间**：表现好的帖子都是什么时候发的

### 3. 爆款复盘

**Top 3 帖子逐条分析**：
- 标题有什么特点
- 内容结构和切入角度
- 封面图风格
- 标签策略
- 发布时间
- 为什么这条能爆

**Bottom 3 帖子逐条分析**：
- 和爆款相比差在哪
- 是内容问题还是时机/运气问题

**爆款共性提炼**：找出 3-5 条规律（"你的爆款都有 X 特征"）

### 4. 标签和 SEO 分析

- 常用标签列表及使用频率
- 哪些标签出现在爆款中、哪些出现在低迷款中
- 推荐增加/减少的标签
- 标题关键词与搜索热度的匹配度

### 5. 对标博主对比

| 维度 | 该账号 | 对标A | 对标B |
|------|--------|-------|-------|
| 粉丝数 | | | |
| 帖子数 | | | |
| 平均互动 | | | |
| 互动率 | | | |
| 发布频率 | | | |
| 内容风格 | | | |

重点分析：差距最大的维度、对标博主可借鉴的策略。

### 6. 运营建议

**内容方向**：
- 应该多做什么类型的内容（基于爆款分析）
- 应该减少什么（基于低迷款分析）
- 建议尝试的新角度

**发布节奏**：
- 推荐发布频率
- 推荐发布时间

**增长策略**（基于当前量级）：
- 素人期：如何冷启动、选什么赛道
- 尾部：如何突破 1 万粉、需要调整什么
- 腰部：如何维持增长、是否该做矩阵
- 头部：如何变现、品牌合作策略

**短期行动清单**：最重要的 3-5 个行动项

## HTML 报告生成

读取模板：
```
Read ${CLAUDE_PLUGIN_ROOT}/skills/creator-skill/assets/report-account.html
```

### 占位符清单

| 占位符 | 内容 |
|--------|------|
| `{{ACCOUNT_NAME}}` | 账号昵称 |
| `{{ACCOUNT_ID}}` | user_id |
| `{{ACCOUNT_URL}}` | 主页链接 |
| `{{FOLLOWERS}}` | 粉丝数 |
| `{{FOLLOWING}}` | 关注数 |
| `{{TOTAL_LIKES}}` | 获赞与收藏总量 |
| `{{TOTAL_POSTS}}` | 帖子总数 |
| `{{ACCOUNT_LEVEL}}` | 量级定位 |
| `{{ACCOUNT_BIO}}` | 简介 |
| `{{GENERATED_TIME}}` | 报告生成时间 |
| `{{AVG_ENGAGEMENT}}` | 单帖平均互动 |
| `{{ENGAGEMENT_RATE}}` | 互动率 |
| `{{POST_FREQUENCY}}` | 发布频率 |
| `{{TREND_LABEL}}` | 趋势标签（上升/平稳/下降） |
| `{{SCATTER_DATA_JSON}}` | 帖子散点图数据 |
| `{{TREND_DATA_JSON}}` | 互动趋势折线图数据 |
| `{{PIE_DATA_JSON}}` | 内容类型饼图数据 |
| `{{TOP_POSTS_CARDS}}` | 爆款帖子分析卡片 HTML |
| `{{BOTTOM_POSTS_CARDS}}` | 低迷帖子分析卡片 HTML |
| `{{VIRAL_PATTERNS}}` | 爆款共性提炼 HTML |
| `{{TAG_ANALYSIS}}` | 标签分析 HTML |
| `{{BENCHMARK_TABLE}}` | 对标博主对比表格 HTML |
| `{{BENCHMARK_STRATEGIES}}` | 可借鉴策略 HTML |
| `{{CONTENT_ADVICE}}` | 内容方向建议 HTML |
| `{{RHYTHM_ADVICE}}` | 发布节奏建议 HTML |
| `{{GROWTH_STRATEGY}}` | 增长策略 HTML |
| `{{ACTION_ITEMS}}` | 短期行动清单 HTML |

### HTML 片段格式

帖子分析卡片（爆款/低迷通用）：
```html
<div class="card bg-gray-50 rounded-lg p-4">
    <div class="flex justify-between items-start">
        <div class="flex-1">
            <h4 class="font-medium text-gray-800">
                <a href="https://www.xiaohongshu.com/explore/{{note_id}}" target="_blank" class="hover:text-red-500">{{帖子标题}}</a>
            </h4>
            <p class="text-xs text-gray-500 mt-1">点赞 {{点赞}} · 收藏 {{收藏}} · 评论 {{评论}} · {{发布时间}}</p>
        </div>
        <span class="text-xs px-2 py-1 rounded-full {{BADGE_COLOR}}">{{标签：爆款/中等/低迷}}</span>
    </div>
    <p class="text-sm text-gray-600 mt-2">{{分析说明}}</p>
</div>
```

对标博主表格行：
```html
<tr>
    <td class="px-4 py-3 font-medium">
        <a href="https://www.xiaohongshu.com/user/profile/{{user_id}}" target="_blank" class="text-gray-800 hover:text-red-500">@{{昵称}}</a>
    </td>
    <td class="px-4 py-3 text-right">{{粉丝数}}</td>
    <td class="px-4 py-3 text-right">{{帖子数}}</td>
    <td class="px-4 py-3 text-right">{{平均互动}}</td>
    <td class="px-4 py-3 text-right">{{互动率}}</td>
    <td class="px-4 py-3">{{内容风格标签}}</td>
</tr>
```

行动项：
```html
<div class="flex items-start gap-3 py-3 border-b border-gray-100">
    <span class="flex-shrink-0 w-7 h-7 rounded-full bg-red-500 text-white flex items-center justify-center text-xs font-bold">{{序号}}</span>
    <div>
        <p class="font-medium text-gray-800">{{行动标题}}</p>
        <p class="text-sm text-gray-500 mt-1">{{具体说明}}</p>
    </div>
</div>
```

保存并打开：
```bash
open "${CLAUDE_PLUGIN_ROOT}/output/account_{{昵称}}_{{日期}}.html"
```
