# HTML 报告占位符与片段格式参考

本文档定义了 `assets/report.html` 模板中所有占位符的含义和填充格式。

## 占位符清单

| 占位符 | 内容 | 示例 |
|--------|------|------|
| `{{TOPIC}}` | 用户主题 | 北京五一手帐集市 |
| `{{GENERATED_TIME}}` | 报告生成时间 | 2026-05-04 13:30 |
| `{{COMPETITION_SCORE}}` | 竞争度评分 | 7.2/10 |
| `{{COMPETITION_LEVEL}}` | 竞争等级 | 中等偏高 |
| `{{BEST_TIME}}` | 建议发布时间 | 周五 18:00 |
| `{{AVG_ENGAGEMENT}}` | 平均互动量 | 2,345 |
| `{{TOTAL_POSTS}}` | 分析帖子总数 | 66 |
| `{{KEYWORDS_TAGS}}` | 关键词标签 HTML | 见下方 |
| `{{HOT_POSTS_CARDS}}` | 帖子卡片 HTML | 见下方 |
| `{{HOT_PATTERNS}}` | 爆款模式总结 HTML | 段落文本 |
| `{{CHART_DATA_JSON}}` | Chart.js 图表数据 | 见下方 |
| `{{KOL_TABLE_ROWS}}` | 博主表格行 HTML | 见下方 |
| `{{KOL_STRATEGIES}}` | 博主策略 HTML | 段落文本 |
| `{{COVER_IMAGE}}` | 封面图 img 标签 | base64 img |
| `{{COVER_REASON}}` | 封面选择理由 | 段落文本 |
| `{{GENERATED_COVERS}}` | 生成封面预览 HTML | 见下方 |
| `{{IMAGE_SEQUENCE}}` | 图片序列 HTML | 见下方 |
| `{{EXCLUDED_IMAGES}}` | 未推荐图片 HTML | 段落文本 |
| `{{TITLE_SUGGESTIONS}}` | 标题建议 HTML | 见下方 |
| `{{CONTENT_TEMPLATE}}` | 正文模板 | 纯文本 |
| `{{HASHTAGS}}` | 话题标签 HTML | 见下方 |
| `{{TIMING_ADVICE}}` | 发布时间建议 | 段落文本 |
| `{{VIRAL_FACTORS}}` | 爆火因素 HTML | 段落文本 |
| `{{DIFFERENTIATION}}` | 差异化建议 HTML | 段落文本 |
| `{{RISK_WARNINGS}}` | 风险提示 HTML | 段落文本 |

## HTML 片段格式

### 关键词标签

```html
<span class="tag bg-red-100 text-red-700">关键词</span>
```

### 帖子卡片

帖子标题应包裹在链接中，点击跳转到小红书原帖（`https://www.xiaohongshu.com/explore/{{note_id}}`）：

```html
<div class="card bg-gray-50 rounded-lg p-4 cursor-pointer" onclick="this.querySelector('.detail').classList.toggle('hidden')">
    <div class="flex justify-between items-center">
        <div class="flex-1">
            <h4 class="font-medium text-gray-800">
                <a href="https://www.xiaohongshu.com/explore/{{note_id}}" target="_blank" class="hover:text-red-500">{{帖子标题}}</a>
            </h4>
            <p class="text-xs text-gray-500 mt-1">@{{作者}} · 点赞 {{点赞数}} · 收藏 {{收藏数}} · 评论 {{评论数}}</p>
        </div>
    </div>
    <div class="detail hidden mt-3 text-sm text-gray-600 border-t pt-3">{{帖子正文摘要}}</div>
</div>
```

### 标题建议（含复制按钮）

```html
<div class="flex items-center justify-between bg-gray-50 rounded-lg px-4 py-3">
    <span class="text-gray-800">{{标题文字}}</span>
    <button class="copy-btn text-xs px-3 py-1 bg-red-100 text-red-600 rounded-full hover:bg-red-200" onclick="copyText('{{标题文字}}', this)">复制</button>
</div>
```

### 话题标签（点击复制）

```html
<span class="tag bg-red-100 text-red-700 cursor-pointer" onclick="copyText('#{{标签名}}', this)">#{{标签名}}</span>
```

### 博主表格行

```html
<tr>
    <td class="px-4 py-3"><a href="https://www.xiaohongshu.com/user/profile/{{user_id}}" target="_blank" class="text-gray-800 hover:text-red-500">@{{博主名}}</a></td>
    <td class="px-4 py-3 text-right">{{粉丝数}}</td>
    <td class="px-4 py-3 text-right">{{互动率}}%</td>
    <td class="px-4 py-3"><span class="tag bg-gray-100 text-gray-600">{{风格标签}}</span></td>
</tr>
```

### 图片序列

```html
<div class="relative">
    <img src="data:image/jpeg;base64,{{BASE64_DATA}}" class="w-full rounded-lg" />
    <span class="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">{{序号}}</span>
    <p class="text-xs text-gray-500 mt-1">{{简评}}</p>
</div>
```

### 生成的封面预览

```html
<div>
    <img src="data:image/jpeg;base64,{{BASE64_DATA}}" class="w-full rounded-lg" />
    <p class="text-xs text-gray-500 mt-1 text-center">{{模板名称}}</p>
</div>
```

## 图片内嵌方式

将图片转为 base64 内嵌到 HTML 中：

```bash
base64 -i "{{图片路径}}" | tr -d '\n'
```

在 HTML 中使用：

```html
<img src="data:image/jpeg;base64,{{BASE64_DATA}}" class="w-full rounded-lg" />
```

对于 PNG 图片使用 `data:image/png;base64,...`。

## Chart.js 数据格式

`{{CHART_DATA_JSON}}` 应替换为以下结构的 JSON：

```json
{
    "labels": ["帖子1标题缩写", "帖子2标题缩写"],
    "likes": [1234, 5678],
    "collects": [234, 567],
    "comments": [45, 89]
}
```

labels 中的标题控制在 8 个字以内，过长则截断加 `...`。
