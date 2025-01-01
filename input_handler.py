# input_handler.py

from constants import PROV_DICT

def get_info():
    """获取用户输入的信息，确定绘制类型和参数。"""
    while True:
        print("绘制类型\n1：高速；2：普通公路")
        draw_typ = input("请输入绘制类型：")
        if draw_typ == "1":
            print("高速公路类型：\n1：非4位数编码；\n2：4位数编码（含角标）；\n3：4位数编码（无角标）")
            expwy_typ = input("请输入高速公路类型：")
            print(f"\n{list(PROV_DICT.keys())}")
            while True:
                zone_typ = input("请输入高速公路所在地区（仅限以上列表中的内容）：")
                if PROV_DICT.get(zone_typ) is not None:
                    break
                else:
                    print("输入有误，请重新输入！\n")
            if expwy_typ == "2":
                name_mainline = input("请输入主线编号：")
                name_cm = input("请输入角标：")
                info_list = [draw_typ, expwy_typ, PROV_DICT[zone_typ], name_mainline, name_cm]
            else:
                name = input("请输入高速公路编号：")
                info_list = [draw_typ, expwy_typ, PROV_DICT[zone_typ], name]
            break

        elif draw_typ == "2":
            while True:
                print("公路类型：\n1：国道；2：省道；3：县道及乡道")
                typ = input("请输入公路类型：")
                if typ in {"1", "2", "3"}:
                    name = input("请输入公路编号：")
                    info_list = [draw_typ, typ, name]
                    break
                else:
                    print("输入有误，请重新输入！\n")
            break

        else:
            print("输入有误，请重新输入！\n")

    return info_list