# constants.py

import getpass

# 分辨率和转换系数
DPI = 600
CM_TO_INCH = 2.54

# 边框宽度（点转像素）
BORDER_WIDTH_PT = 10
BORDER_WIDTH_PX = int(BORDER_WIDTH_PT * DPI / 72)

# 字体路径
USER_NAME = getpass.getuser()
FONT_DIR = f"C:/Users/{USER_NAME}/AppData/Local/Microsoft/Windows/Fonts/"
DEFAULT_FONT_PATH = f"{FONT_DIR}BywayEModified.ttf"
SIMHEI_FONT_PATH = "C:/Windows/Fonts/simhei.ttf"

# 颜色字典
COLOR_DICT = {
    "1": (255, 0, 0),      # 红色
    "2": (255, 255, 0),    # 黄色
    "3": (255, 255, 255)   # 白色
}

# 高速公路类型字典
NAME_DICT = {
    "1": "国道",
    "2": "省道"
}

# 省份缩写字典
PROV_DICT = {
    "国家高速": "国家",
    "北京": "京",
    "天津": "津",
    "上海": "沪",
    "重庆": "渝",
    "河北": "冀",
    "山西": "晋",
    "辽宁": "辽",
    "吉林": "吉",
    "黑龙江": "黑",
    "江苏": "苏",
    "浙江": "浙",
    "安徽": "皖",
    "福建": "闽",
    "江西": "赣",
    "山东": "鲁",
    "河南": "豫",
    "湖北": "鄂",
    "湖南": "湘",
    "广东": "粤",
    "广西": "桂",
    "海南": "琼",
    "四川": "川",
    "贵州": "贵",
    "云南": "滇",
    "西藏": "藏",
    "陕西": "陕",
    "甘肃": "甘",
    "青海": "青",
    "宁夏": "宁",
    "新疆": "新",
    "内蒙古": "蒙",
    "京津冀地区": "京津冀"
}