# main.py

"""
作者: Bilibili @JesseSong15
AI创作声明：本代码在开发过程中运用了 ChatGPT o1 的辅助。
"""


from input_handler import get_info
from signpost import signpost_highway, signpost_expwy_nocm, signpost_expwy_cm

def main():
    """主程序循环，处理用户输入并绘制路标。"""
    info_list = get_info()
    if info_list[0] == "1":
        if info_list[1] != "2":
            # 非4位数编码或无角标
            signpost_expwy_nocm(info_list[1], info_list[2], info_list[3])
        else:
            # 4位数编码含角标
            signpost_expwy_cm(info_list[1], info_list[2], info_list[3], info_list[4])
    else:
        signpost_highway(info_list[1], info_list[2])

if __name__ == "__main__":
    main()