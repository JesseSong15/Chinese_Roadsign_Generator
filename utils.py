# utils.py

from PIL import Image, ImageDraw, ImageFont
from constants import DPI, CM_TO_INCH, DEFAULT_FONT_PATH, SIMHEI_FONT_PATH, BORDER_WIDTH_PX


def cm_to_px(cm):
    """将厘米转换为像素。"""
    return int(cm * DPI / CM_TO_INCH)

def get_font(path, size_pt):
    """加载指定路径和大小的字体。"""
    size_px = int(size_pt * DPI / 72)
    return ImageFont.truetype(path, size_px)

def create_image(width_cm, height_cm, color):
    """创建指定尺寸和颜色的图片。"""
    width_px = cm_to_px(width_cm)
    height_px = cm_to_px(height_cm)
    return Image.new("RGB", (width_px, height_px), color), width_px, height_px

def draw_rounded_rectangle(draw, width_px, height_px, rect_width_cm, rect_height_cm, corner_radius_cm, outline_color):
    """绘制带圆角的矩形，并返回其位置坐标。"""
    rect_width_px = cm_to_px(rect_width_cm)
    rect_height_px = cm_to_px(rect_height_cm)
    corner_radius_px = cm_to_px(corner_radius_cm)

    left = (width_px - rect_width_px) // 2
    top = (height_px - rect_height_px) // 2
    right = left + rect_width_px
    bottom = top + rect_height_px

    draw.rounded_rectangle(
        [left, top, right, bottom],
        radius=corner_radius_px,
        outline=outline_color,
        width=BORDER_WIDTH_PX
    )
    return left, top, right, bottom

def create_text_image(text, font, fill_color, scale_ratio_width, scale_ratio_height, padding_pt=2):
    """创建并缩放文本图像，处理文本的绘制和缩放。"""
    padding_px = int(padding_pt * DPI / 72)
    text_bbox = font.getbbox(text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    temp_image = Image.new("RGBA", (text_width + 2 * padding_px, text_height + 2 * padding_px), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    temp_draw.text((padding_px, padding_px), text, font=font, fill=fill_color)

    scaled_width = int(temp_image.width * scale_ratio_width)
    scaled_height = int(temp_image.height * scale_ratio_height)
    return temp_image.resize((scaled_width, scaled_height), Image.LANCZOS)

def save_image(image, filepath, filename):
    """保存生成的图片，并打印保存信息。"""
    full_path = f"{filepath}\\{filename}.png"
    image.save(full_path, dpi=(DPI, DPI))
    print(f"\n{filename} 绘制完成，文件存储至 {filepath}。")