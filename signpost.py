# signpost.py

from PIL import Image, ImageDraw
from utils import cm_to_px, get_font, create_image, draw_rounded_rectangle, create_text_image, save_image
from constants import COLOR_DICT, DEFAULT_FONT_PATH, SIMHEI_FONT_PATH, NAME_DICT, PROV_DICT, BORDER_WIDTH_PX, DPI


def signpost_highway(typ, name):
    """绘制普通公路（国道、省道、县道及乡道）的路标。"""
    # 路标尺寸
    width_cm, height_cm = 30, 15
    background_color = COLOR_DICT.get(typ, (255, 255, 255))
    image, width_px, height_px = create_image(width_cm, height_cm, background_color)

    draw = ImageDraw.Draw(image)

    # 绘制圆角矩形边框
    border_color = (255, 255, 255) if typ == "1" else (0, 0, 0)
    left, top, right, bottom = draw_rounded_rectangle(
        draw, width_px, height_px, 29, 14, 1, border_color
    )

    # 设置字体
    font = get_font(DEFAULT_FONT_PATH, 250)

    # 计算缩放比例
    desired_width_px = cm_to_px(25)
    desired_height_px = cm_to_px(9)
    text_bbox = font.getbbox(name)
    scale_ratio_width = desired_width_px / (text_bbox[2] - text_bbox[0])
    scale_ratio_height = desired_height_px / (text_bbox[3] - text_bbox[1])

    # 创建并缩放文本图像
    text_image = create_text_image(
        name,
        font,
        border_color,
        scale_ratio_width,
        scale_ratio_height
    )
    text_x = (width_px - text_image.width) // 2
    text_y = (height_px - text_image.height) // 2 + 50
    image.paste(text_image, (text_x, text_y), text_image)

    # 文件命名
    if typ == "3":
        first_letter = name[0]
        suffix = {
            "X": "县道标志",
            "Y": "乡道标志"
        }.get(first_letter, "未知类型标志")
        filename = f"{name}{suffix}"
    else:
        filename = f"{name}{NAME_DICT.get(typ, '')}"

    filepath = input("请从资源管理器中粘贴文件夹路径：")
    save_image(image, filepath, filename)

def signpost_expwy_nocm(expwy_typ, zone_typ, name):
    """绘制不含角标的高速公路编号路标。"""
    width_cm = 15 if expwy_typ == "1" else 20
    height_cm = 15
    image, width_px, height_px = create_image(width_cm, height_cm, (117, 186, 42))
    draw = ImageDraw.Draw(image)

    # 绘制圆角矩形边框
    left, top, right, bottom = draw_rounded_rectangle(
        draw, width_px, height_px, width_cm - 1, height_cm - 1, 1, (255, 255, 255)
    )

    # 填充颜色
    if zone_typ == "国家":
        fill_color = (230, 31, 25)
        fill_color_zone = (255, 255, 255)
    else:
        fill_color = (255, 255, 0)
        fill_color_zone = (0, 0, 0)

    # 绘制顶部矩形和椭圆
    toprect_width_px_1 = cm_to_px(width_cm - 1 - BORDER_WIDTH_PX * 2.54 / DPI)
    toprect_height_px_1 = cm_to_px(3.25)
    toprect_width_px_2 = cm_to_px(width_cm - 2)
    toprect_height_px_2 = cm_to_px(1)
    topelli_radius = toprect_width_px_1 - toprect_width_px_2

    left_1 = left + BORDER_WIDTH_PX
    top_1 = top + cm_to_px(1)
    right_1 = left + toprect_width_px_1
    bottom_1 = top + toprect_height_px_1

    left_2 = left + cm_to_px(1)
    top_2 = top + BORDER_WIDTH_PX
    right_2 = left + toprect_width_px_2
    bottom_2 = top + toprect_height_px_2

    right_3 = left_1 + 2 * topelli_radius
    bottom_3 = top_2 + 2 * topelli_radius
    left_4 = right_1 - 2 * topelli_radius
    bottom_4 = top_2 + 2 * topelli_radius

    draw.rectangle([left_1, top_1, right_1, bottom_1], fill=fill_color)
    draw.rectangle([left_2, top_2, right_2, bottom_2], fill=fill_color)
    draw.ellipse([left_1, top_2, right_3, bottom_3], fill=fill_color)
    draw.ellipse([left_4, top_2, right_1, bottom_4], fill=fill_color)

    # 设置高速编号字体
    font_mainline = get_font(DEFAULT_FONT_PATH, 150)
    text_bbox = font_mainline.getbbox(name)
    scale_ratio_width = min(cm_to_px(width_cm - 2.5) / (text_bbox[2] - text_bbox[0]), 1)
    scale_ratio_height = cm_to_px(6) / (text_bbox[3] - text_bbox[1])

    # 创建并缩放文本图像
    text_image = create_text_image(
        name,
        font_mainline,
        (255, 255, 255),
        scale_ratio_width,
        scale_ratio_height
    )
    text_x = (width_px - text_image.width) // 2
    text_y = (height_px - text_image.height) // 2
    image.paste(text_image, (text_x, text_y), text_image)
    print("高速公路编号绘制完成")

    ##### 处理国家高速/省级高速标志 #####
    font_zone = get_font(SIMHEI_FONT_PATH, 40)
    zone_text = f"{zone_typ}高速"
    space_px = cm_to_px(300 / 72 * DPI)  # 将空间从pt转换为px
    total_width = sum([font_zone.getbbox(c)[2] - font_zone.getbbox(c)[0] for c in zone_text]) + space_px * (len(zone_text) - 1)
    left_edge = (width_px - total_width) // 2
    top_edge = top + (cm_to_px(3.25) - BORDER_WIDTH_PX) // 2

    for char in zone_text:
        char_bbox = font_zone.getbbox(char)
        char_width = char_bbox[2] - char_bbox[0]
        char_height = char_bbox[3] - char_bbox[1]
        draw.text((left_edge, top_edge + BORDER_WIDTH_PX - char_height // 2), char, font=font_zone, fill=fill_color_zone)
        left_edge += char_width + space_px

    ##### 处理高速公路名 #####
    expwy_name = input("请输入高速公路中文名称：")
    font_name = get_font(SIMHEI_FONT_PATH, 60)
    space_px_name = cm_to_px(50 / 72 * DPI)
    char_list = list(expwy_name)
    total_width = sum([font_name.getbbox(c)[2] - font_name.getbbox(c)[0] for c in char_list]) + space_px_name * (len(char_list) - 1)
    text_height = max([font_name.getbbox(c)[3] - font_name.getbbox(c)[1] for c in char_list])

    scale_ratio_width_name = min(cm_to_px(width_cm - 3) / total_width, 1)
    scale_ratio_height_name = 1

    temp_image = Image.new("RGBA", (total_width + 4, text_height + 4), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    current_x = 2
    for c in char_list:
        temp_draw.text((current_x, 2), c, font=font_name, fill=(255, 255, 255))
        current_x += font_name.getbbox(c)[2] - font_name.getbbox(c)[0] + space_px_name

    text_image_name = temp_image.resize(
        (int(temp_image.width * scale_ratio_width_name), int(temp_image.height * scale_ratio_height_name)),
        Image.LANCZOS
    )
    text_x_name = (width_px - text_image_name.width) // 2
    text_y_name = height_px - cm_to_px(1) - text_height - BORDER_WIDTH_PX
    image.paste(text_image_name, (text_x_name, text_y_name), text_image_name)
    print("高速公路名称绘制完成")

    filepath = input("请从资源管理器中粘贴文件夹路径：")
    filename = f"{zone_typ}高速{name}标志"
    save_image(image, filepath, filename)

def signpost_expwy_cm(expwy_typ, zone_typ, name_mainline, name_cm):
    """绘制含有角标的高速公路编号路标。"""
    width_cm, height_cm = 20, 15
    image, width_px, height_px = create_image(width_cm, height_cm, (117, 186, 42))
    draw = ImageDraw.Draw(image)

    # 绘制圆角矩形边框
    left, top, right, bottom = draw_rounded_rectangle(
        draw, width_px, height_px, width_cm - 1, height_cm - 1, 1, (255, 255, 255)
    )

    # 填充颜色
    if zone_typ == "国家":
        fill_color = (230, 31, 25)
        fill_color_zone = (255, 255, 255)
    else:
        fill_color = (255, 255, 0)
        fill_color_zone = (0, 0, 0)

    # 绘制顶部矩形和椭圆
    toprect_width_px_1 = cm_to_px(width_cm - 1 - BORDER_WIDTH_PX * 2.54 / DPI)
    toprect_height_px_1 = cm_to_px(3.25)
    toprect_width_px_2 = cm_to_px(width_cm - 2)
    toprect_height_px_2 = cm_to_px(1)
    topelli_radius = toprect_width_px_1 - toprect_width_px_2

    left_1 = left + BORDER_WIDTH_PX
    top_1 = top + cm_to_px(1)
    right_1 = left + toprect_width_px_1
    bottom_1 = top + toprect_height_px_1

    left_2 = left + cm_to_px(1)
    top_2 = top + BORDER_WIDTH_PX
    right_2 = left + toprect_width_px_2
    bottom_2 = top + toprect_height_px_2

    right_3 = left_1 + 2 * topelli_radius
    bottom_3 = top_2 + 2 * topelli_radius
    left_4 = right_1 - 2 * topelli_radius
    bottom_4 = top_2 + 2 * topelli_radius

    draw.rectangle([left_1, top_1, right_1, bottom_1], fill=fill_color)
    draw.rectangle([left_2, top_2, right_2, bottom_2], fill=fill_color)
    draw.ellipse([left_1, top_2, right_3, bottom_3], fill=fill_color)
    draw.ellipse([left_4, top_2, right_1, bottom_4], fill=fill_color)

    # 设置高速编号字体
    font_mainline = get_font(DEFAULT_FONT_PATH, 150)
    font_cm = get_font(DEFAULT_FONT_PATH, 75)  # 150pt / 2
    text_bbox_mainline = font_mainline.getbbox(name_mainline)
    text_bbox_cm = font_cm.getbbox(name_cm)
    text_width_mainline = text_bbox_mainline[2] - text_bbox_mainline[0]
    text_width_cm = text_bbox_cm[2] - text_bbox_cm[0]
    text_height = text_bbox_mainline[3] - text_bbox_mainline[1]

    # 计算缩放比例
    desired_width_px = cm_to_px(20 - 2.5)
    scale_ratio_width = min(desired_width_px / (text_width_mainline + text_width_cm), 1)
    scale_ratio_height = cm_to_px(6) / text_height

    # 创建并缩放文本图像
    temp_image = Image.new("RGBA", (text_width_mainline + text_width_cm + 4, text_height + 4), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    temp_draw.text((2, 2), name_mainline, font=font_mainline, fill=(255, 255, 255))
    temp_draw.text((2 + text_width_mainline, 2 + text_height - (text_bbox_cm[3] - text_bbox_cm[1])), name_cm, font=font_cm, fill=(255, 255, 255))

    text_image = temp_image.resize(
        (int(temp_image.width * scale_ratio_width), int(temp_image.height * scale_ratio_height)),
        Image.LANCZOS
    )
    text_x = (width_px - text_image.width) // 2
    text_y = (height_px - text_image.height) // 2
    image.paste(text_image, (text_x, text_y), text_image)

    ##### 处理国家高速/省级高速标志 #####
    font_zone = get_font(SIMHEI_FONT_PATH, 40)
    zone_text = f"{zone_typ}高速"
    space_px = cm_to_px(300 / 72 * DPI)  # 将空间从pt转换为px
    total_width = sum([font_zone.getbbox(c)[2] - font_zone.getbbox(c)[0] for c in zone_text]) + space_px * (len(zone_text) - 1)
    left_edge = (width_px - total_width) // 2
    top_edge = top + (cm_to_px(3.25) - BORDER_WIDTH_PX) // 2

    for char in zone_text:
        char_bbox = font_zone.getbbox(char)
        char_width = char_bbox[2] - char_bbox[0]
        char_height = char_bbox[3] - char_bbox[1]
        draw.text((left_edge, top_edge + BORDER_WIDTH_PX - char_height // 2), char, font=font_zone, fill=fill_color_zone)
        left_edge += char_width + space_px

    ##### 处理高速公路名 #####
    expwy_name = input("请输入高速公路中文名称：")
    font_name = get_font(SIMHEI_FONT_PATH, 60)
    space_px_name = cm_to_px(50 / 72 * DPI)
    char_list = list(expwy_name)
    total_width = sum([font_name.getbbox(c)[2] - font_name.getbbox(c)[0] for c in char_list]) + space_px_name * (len(char_list) - 1)
    text_height = max([font_name.getbbox(c)[3] - font_name.getbbox(c)[1] for c in char_list])

    scale_ratio_width_name = min(cm_to_px(20 - 3) / total_width, 1)
    scale_ratio_height_name = 1

    temp_image = Image.new("RGBA", (total_width + 4, text_height + 4), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    current_x = 2
    for c in char_list:
        temp_draw.text((current_x, 2), c, font=font_name, fill=(255, 255, 255))
        current_x += font_name.getbbox(c)[2] - font_name.getbbox(c)[0] + space_px_name

    text_image_name = temp_image.resize(
        (int(temp_image.width * scale_ratio_width_name), int(temp_image.height * scale_ratio_height_name)),
        Image.LANCZOS
    )
    text_x_name = (width_px - text_image_name.width) // 2
    text_y_name = height_px - cm_to_px(1) - text_height - BORDER_WIDTH_PX
    image.paste(text_image_name, (text_x_name, text_y_name), text_image_name)

    filepath = input("请从资源管理器中粘贴文件夹路径：")
    filename = f"{zone_typ}高速{name_mainline}{name_cm}标志"
    save_image(image, filepath, filename)