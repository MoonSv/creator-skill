#!/usr/bin/env python3
"""
小红书封面头图生成器
支持4种模板风格，自动裁剪为3:4比例(1080x1440)，叠加中文标题
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
except ImportError:
    print("错误: 请先安装 Pillow: pip3 install Pillow")
    sys.exit(1)


# 小红书推荐尺寸
COVER_WIDTH = 1080
COVER_HEIGHT = 1440

# macOS 中文字体路径（按优先级）
FONT_PATHS = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def find_font(bold=False):
    """查找可用的中文字体"""
    for path in FONT_PATHS:
        if Path(path).exists():
            return path
    # 备用：项目内字体目录
    project_fonts = Path(__file__).parent.parent / "fonts"
    for f in project_fonts.glob("*.ttf"):
        return str(f)
    for f in project_fonts.glob("*.ttc"):
        return str(f)
    return None


def load_font(size, bold=False):
    """加载指定大小的字体"""
    font_path = find_font(bold)
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def crop_to_ratio(img, target_w, target_h):
    """智能裁剪图片到目标比例，保持中心区域"""
    orig_w, orig_h = img.size
    target_ratio = target_w / target_h
    orig_ratio = orig_w / orig_h

    if orig_ratio > target_ratio:
        new_w = int(orig_h * target_ratio)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
    elif orig_ratio < target_ratio:
        new_h = int(orig_w / target_ratio)
        top = (orig_h - new_h) // 2
        img = img.crop((0, top, orig_w, top + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


def draw_text_with_stroke(draw, position, text, font, fill, stroke_width=3, stroke_fill="black"):
    """绘制带描边的文字"""
    x, y = position
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text(position, text, font=font, fill=fill)


def wrap_text(text, font, max_width, draw):
    """将文本换行以适应最大宽度"""
    lines = []
    current_line = ""
    for char in text:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] > max_width:
            if current_line:
                lines.append(current_line)
            current_line = char
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines


def template_bold_text(img, title, subtitle=""):
    """大字报风格 - 适合教程、攻略、干货"""
    draw = ImageDraw.Draw(img)

    # 底部渐变遮罩
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(img.height // 2, img.height):
        alpha = int(200 * (y - img.height // 2) / (img.height // 2))
        overlay_draw.rectangle([(0, y), (img.width, y + 1)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 主标题 - 大号白字
    font_size = 88
    font = load_font(font_size, bold=True)
    max_width = img.width - 120
    lines = wrap_text(title, font, max_width, draw)

    # 计算起始Y位置（底部对齐）
    line_height = font_size + 20
    total_height = len(lines) * line_height
    start_y = img.height - total_height - 160

    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw_text_with_stroke(draw, (60, y), line, font, fill="white", stroke_width=2)

    # 副标题
    if subtitle:
        sub_font = load_font(36)
        sub_y = start_y + total_height + 20
        draw_text_with_stroke(draw, (60, sub_y), subtitle, sub_font, fill="#FFD700", stroke_width=1)

    return img


def template_magazine(img, title, subtitle=""):
    """杂志排版风格 - 适合生活方式、穿搭"""
    # 轻微提亮
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.05)

    draw = ImageDraw.Draw(img)

    # 顶部半透明白色条带
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    bar_height = 280
    overlay_draw.rectangle([(0, 0), (img.width, bar_height)], fill=(255, 255, 255, 200))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 标题在白色条带内
    font = load_font(64, bold=True)
    max_width = img.width - 100
    lines = wrap_text(title, font, max_width, draw)

    line_height = 80
    total_height = len(lines) * line_height
    start_y = (bar_height - total_height) // 2

    for i, line in enumerate(lines):
        y = start_y + i * line_height
        draw.text((50, y), line, font=font, fill="#1a1a1a")

    # 底部装饰线
    if subtitle:
        sub_font = load_font(30)
        draw.text((50, bar_height - 50), subtitle, font=sub_font, fill="#666666")

    # 左侧装饰线
    draw.rectangle([(30, 20), (36, bar_height - 20)], fill="#FF2442")

    return img


def template_minimal(img, title, subtitle=""):
    """简约清新风格 - 适合日常记录"""
    # 整体提亮
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.08)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.95)

    draw = ImageDraw.Draw(img)

    # 中央圆角矩形卡片
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    card_margin = 80
    card_top = img.height // 2 - 120
    card_bottom = img.height // 2 + 180
    overlay_draw.rounded_rectangle(
        [(card_margin, card_top), (img.width - card_margin, card_bottom)],
        radius=20,
        fill=(255, 255, 255, 220),
    )
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 标题居中
    font = load_font(52, bold=True)
    max_width = img.width - card_margin * 2 - 60
    lines = wrap_text(title, font, max_width, draw)

    line_height = 68
    total_height = len(lines) * line_height
    start_y = card_top + (card_bottom - card_top - total_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img.width - text_width) // 2
        y = start_y + i * line_height
        draw.text((x, y), line, font=font, fill="#333333")

    return img


def template_split(img, title, subtitle=""):
    """上图下文分割风格 - 适合对比、测评"""
    # 上2/3图片，下1/3纯色文字区
    split_y = int(img.height * 0.65)

    # 图片区域保持原样
    result = img.copy()
    draw = ImageDraw.Draw(result)

    # 下方白色区域
    draw.rectangle([(0, split_y), (img.width, img.height)], fill="#FFFFFF")

    # 分割线装饰
    draw.rectangle([(0, split_y), (img.width, split_y + 4)], fill="#FF2442")

    # 标题
    font = load_font(60, bold=True)
    max_width = img.width - 120
    lines = wrap_text(title, font, max_width, draw)

    text_area_height = img.height - split_y - 4
    line_height = 76
    total_height = len(lines) * line_height
    start_y = split_y + (text_area_height - total_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img.width - text_width) // 2
        y = start_y + i * line_height
        draw.text((x, y), line, font=font, fill="#1a1a1a")

    # 副标题
    if subtitle:
        sub_font = load_font(28)
        bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_width = bbox[2] - bbox[0]
        draw.text(
            ((img.width - sub_width) // 2, start_y + total_height + 10),
            subtitle,
            font=sub_font,
            fill="#999999",
        )

    return result


TEMPLATES = {
    "bold_text": template_bold_text,
    "magazine": template_magazine,
    "minimal": template_minimal,
    "split": template_split,
}


def generate_cover(image_path, title, template="bold_text", subtitle="", output_path=None):
    """
    生成封面图

    Args:
        image_path: 原图路径
        title: 封面标题文字
        template: 模板名称 (bold_text/magazine/minimal/split)
        subtitle: 副标题（可选）
        output_path: 输出路径（默认在原图同目录生成）
    """
    img = Image.open(image_path)

    # 裁剪为3:4
    img = crop_to_ratio(img, COVER_WIDTH, COVER_HEIGHT)

    # 应用模板
    template_fn = TEMPLATES.get(template, template_bold_text)
    result = template_fn(img, title, subtitle)

    # 确定输出路径
    if output_path is None:
        src = Path(image_path)
        output_path = src.parent / f"{src.stem}_cover_{template}{src.suffix}"

    # 保存
    if result.mode == "RGBA":
        result = result.convert("RGB")
    result.save(str(output_path), quality=95)
    print(f"✓ 封面已生成: {output_path}")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(description="小红书封面头图生成器")
    parser.add_argument("image", help="原图路径")
    parser.add_argument("title", help="封面标题")
    parser.add_argument(
        "--template",
        choices=list(TEMPLATES.keys()),
        default="bold_text",
        help="模板风格 (default: bold_text)",
    )
    parser.add_argument("--subtitle", default="", help="副标题")
    parser.add_argument("--output", "-o", help="输出路径")
    parser.add_argument(
        "--all-templates",
        action="store_true",
        help="用所有模板各生成一张",
    )

    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"错误: 图片不存在: {args.image}")
        sys.exit(1)

    if args.all_templates:
        for name in TEMPLATES:
            src = Path(args.image)
            out = src.parent / f"{src.stem}_cover_{name}.jpg"
            generate_cover(args.image, args.title, name, args.subtitle, out)
    else:
        generate_cover(args.image, args.title, args.template, args.subtitle, args.output)


if __name__ == "__main__":
    main()
