---
name: cover-generator
description: This skill should be used when the user asks to "生成封面", "制作小红书封面", "做封面头图", "cover image", or needs to create cover images for Xiaohongshu posts.
version: 1.0.0
---

# Cover Generator - 小红书封面头图生成

为小红书帖子生成高质量的封面头图。基于 Pillow 图像处理，支持多种模板风格。

## 前置依赖

```bash
python3 -c "import PIL" || pip3 install Pillow
```

## 使用方式

### 输入

1. **原图路径**：用作封面底图的图片文件
2. **标题文字**：要叠加在封面上的标题
3. **模板选择**（可自动推荐）：
   - `bold_text` - 大字报风格（底部大字+渐变遮罩，适合教程/攻略/干货）
   - `magazine` - 杂志排版（顶部白色条带+标题，适合生活方式/穿搭）
   - `minimal` - 简约清新（中央卡片式标题，适合日常记录/心情）
   - `split` - 上图下文（上2/3图+下1/3文字区，适合测评/对比）
4. **副标题**（可选）

### 执行

单模板生成：
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate-cover.py "{{图片路径}}" "{{标题}}" --template {{模板名}} --subtitle "{{副标题}}"
```

全模板对比生成：
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate-cover.py "{{图片路径}}" "{{标题}}" --all-templates
```

指定输出路径：
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/generate-cover.py "{{图片路径}}" "{{标题}}" --template bold_text -o "{{输出路径}}"
```

### 模板选择建议

基于内容类型自动推荐：

| 内容类型 | 推荐模板 | 理由 |
|----------|----------|------|
| 教程/攻略/干货 | `bold_text` | 大字醒目，信息传递直接 |
| 探店/生活/穿搭 | `magazine` | 精致高级感，突出氛围 |
| 日常/碎碎念/记录 | `minimal` | 简洁不抢戏，让图片说话 |
| 测评/对比/清单 | `split` | 图文分离，信息层次清晰 |

### 输出规格

- 尺寸：1080 x 1440 px（3:4 比例，小红书最佳显示比例）
- 格式：JPEG（quality=95）
- 字体：PingFang SC（macOS 系统自带）
- 输出位置：默认在原图同目录，文件名添加 `_cover_{{模板名}}` 后缀

### 标题文字建议

- 控制在 8-15 个汉字（太长会换行影响美观）
- 使用有冲击力的关键词
- 避免标点符号过多
- 可用竖线 `|` 或斜杠 `/` 分割关键信息

## 注意事项

- 如果图片比例与 3:4 差异大，会自动居中裁剪，注意主体不要被裁掉
- 深色底图用 `bold_text` 效果最佳（白字+渐变遮罩）
- 浅色/白色底图用 `magazine` 或 `split`（暗色文字更清晰）
- 生成后建议让用户预览确认，不满意可换模板或调整标题
