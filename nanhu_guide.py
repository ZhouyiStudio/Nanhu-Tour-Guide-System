#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嘉兴南湖导游程序
Nanhu Tour Guide System
"""

import sys
import os
import time
import json

# ========== 数据层 ==========

SCENIC_SPOTS = [
    {
        "id": 1,
        "name": "南湖红船（中共一大会址）",
        "category": "红色文化",
        "rating": "★★★★★",
        "duration": "30分钟",
        "desc": "南湖红船位于南湖湖心岛南侧，是中国共产党第一次全国代表大会最后一天会议的会址。"
                 "1921年7月30日晚，中共一大因遭法租界巡捕袭扰，被迫中断。"
                 "8月初，代表们转移到嘉兴南湖，在一艘游船上继续举行会议，宣告中国共产党诞生。"
                 "这艘游船因而被称为\"南湖红船\"，是中国共产党的\"母亲船\"。",
        "history": "1921年8月初，中共一大代表们从上海转移到嘉兴南湖，"
                    "在游船上通过了《中国共产党纲领》和《关于当前实际工作的决议》，"
                    "选举产生了中央领导机构，庄严宣告了中国共产党的诞生。",
        "tips": "建议上午参观，光线好，适合拍照留念。红船现为国家级文物保护单位。"
    },
    {
        "id": 2,
        "name": "南湖革命纪念馆",
        "category": "红色文化",
        "rating": "★★★★★",
        "duration": "1.5小时",
        "desc": "南湖革命纪念馆是展示中国共产党创建历史的专题纪念馆，"
                 "位于嘉兴市南湖路旁。纪念馆建筑庄重大气，"
                 "展厅面积约8000平方米，通过大量历史文物、图片、"
                 "场景复原和多媒体展示，全面呈现了中共创建的历史背景和过程。",
        "history": "南湖革命纪念馆1959年10月1日正式成立，"
                    "1990年和2011年两次扩建。"
                    "现馆舍于2011年建党90周年之际建成开放。"
                    "馆藏文物数千件，其中国家一级文物数十件。",
        "tips": "免费参观，需携带身份证。周一闭馆，建议预留充足时间。"
    },
    {
        "id": 3,
        "name": "湖心岛",
        "category": "自然景观",
        "rating": "★★★★☆",
        "duration": "1小时",
        "desc": "湖心岛是南湖中最大的岛屿，面积约8亩。"
                 "岛上绿树成荫，亭台楼阁错落有致，"
                 "以烟雨楼最为著名。"
                 "登岛可乘画舫游览，沿途欣赏南湖秀美的湖光水色。",
        "history": "湖心岛自古就是嘉兴名胜。唐代已有建筑，"
                    "明代大修，清康熙、乾隆多次南巡至此。"
                    "烟雨楼因唐代杜牧诗\u201c南朝四百八十寺，多少楼台烟雨中\u201d而得名。",
        "tips": "需乘船上岛，船票含在景区门票内。岛上蚊虫较多，夏季注意防护。"
    },
    {
        "id": 4,
        "name": "烟雨楼",
        "category": "人文古迹",
        "rating": "★★★★★",
        "duration": "40分钟",
        "desc": "烟雨楼位于湖心岛南端，是南湖的标志性建筑。"
                 "楼高约20米，三层重檐，飞檐翘角，气势恢宏。"
                 "登楼远眺，南湖全景尽收眼底，"
                 "细雨蒙蒙时更显\"烟雨朦胧\"的诗情画意。",
        "history": "烟雨楼始建于五代后晋时期（公元936-947年），"
                    "原在嘉兴城西南湖畔。明嘉靖年间移建至湖心岛。"
                    "清代康熙、乾隆皇帝多次登临并题诗。"
                    "1921年中共一大代表也曾登楼游览。",
        "tips": "烟雨楼是南湖最佳观景点，雨后初晴时景色最美。"
    },
    {
        "id": 5,
        "name": "南湖天地",
        "category": "休闲商业",
        "rating": "★★★★☆",
        "duration": "2小时",
        "desc": "南湖天地是集餐饮、购物、文化体验于一体的滨水商业街区，"
                 "沿南湖而建，建筑风格融合了传统江南水乡和现代设计元素。"
                 "这里汇集了众多嘉兴特色餐饮和文创商店，"
                 "是游客休憩、品尝美食的好去处。",
        "history": "南湖天地于2021年开业，是嘉兴城市更新的重点项目，"
                    "旨在打造南湖景区周边的高品质文旅商业配套。",
        "tips": "傍晚时分灯光亮起，氛围最佳。推荐品尝嘉兴粽子等当地美食。"
    },
    {
        "id": 6,
        "name": "壕股塔",
        "category": "人文古迹",
        "rating": "★★★★☆",
        "duration": "30分钟",
        "desc": "壕股塔位于南湖西岸，是一座七层八角砖塔，"
                 "高约45米。塔身古朴典雅，登塔可俯瞰南湖全景及嘉兴城市风貌。"
                 "塔周边环境清幽，绿树环绕。",
        "history": "壕股塔始建于宋代，历代多次修缮。"
                    "塔名\"壕股\"源于其位于古城壕（护城河）之滨。"
                    "现塔为现代重建，保留了宋代建筑风格。",
        "tips": "登塔需另购票，体力消耗较大但景色值得。"
    },
    {
        "id": 7,
        "name": "揽秀园",
        "category": "园林景观",
        "rating": "★★★★☆",
        "duration": "45分钟",
        "desc": "揽秀园是一座典型的江南古典园林，"
                 "园内亭台楼阁、小桥流水、假山奇石相映成趣。"
                 "园名\"揽秀\"意为揽取南湖秀色，"
                 "是南湖景区中感受江南园林艺术的绝佳去处。",
        "history": "揽秀园建于20世纪80年代，"
                    "虽然是现代建造，但严格遵循了江南古典园林的造园技法，"
                    "被誉为\"浙北园林之冠\"。",
        "tips": "园内曲径通幽，适合慢慢游览拍照。"
    },
    {
        "id": 8,
        "name": "南湖渔村",
        "category": "民俗文化",
        "rating": "★★★☆☆",
        "duration": "1小时",
        "desc": "南湖渔村是一个展示嘉兴水乡渔文化的民俗景点，"
                 "这里有传统的渔家民居、渔具展示和水上作业演示，"
                 "可以体验南湖渔民的传统生活方式。",
        "history": "南湖自古以来就是重要的淡水渔场，"
                    "渔村文化是南湖人文的重要组成部分。"
                    "南湖渔村景区是对这一传统文化的保护性展示。",
        "tips": "可以品尝到新鲜的南湖鱼鲜，体验渔民生活。"
    }
]

ROUTES = [
    {
        "id": "A",
        "name": "红色经典之旅（半日游）",
        "duration": "3-4小时",
        "spots": [1, 2, 3, 4],
        "desc": "以红色文化为主题，参观中共一大会址红船和南湖革命纪念馆，"
                "感受中国共产党的光辉起点，同时游览湖心岛和烟雨楼。",
        "schedule": [
            "南湖革命纪念馆（1.5小时）→ 乘船前往湖心岛（10分钟）",
            "湖心岛/烟雨楼（1小时）→ 瞻仰南湖红船（30分钟）→ 乘船返回"
        ]
    },
    {
        "id": "B",
        "name": "全景深度游（一日游）",
        "duration": "6-8小时",
        "spots": [1, 2, 3, 4, 5, 6, 7],
        "desc": "全面游览南湖主要景点，涵盖红色文化、自然景观和人文古迹，"
                "适合时间充裕的游客。",
        "schedule": [
            "上午：南湖革命纪念馆（1.5小时）→ 乘船至湖心岛",
            "中午：湖心岛/烟雨楼/红船（1.5小时）→ 返回用餐",
            "下午：揽秀园（45分钟）→ 壕股塔（30分钟）→ 南湖天地（自由活动）"
        ]
    },
    {
        "id": "C",
        "name": "休闲亲子游（半日游）",
        "duration": "3-4小时",
        "spots": [3, 4, 5, 7],
        "desc": "轻松休闲路线，以自然风光和休闲娱乐为主，"
                "适合家庭出游。",
        "schedule": [
            "乘船至湖心岛（1小时游览）→ 烟雨楼观景",
            "揽秀园（45分钟）→ 南湖天地（美食购物）"
        ]
    },
    {
        "id": "D",
        "name": "文化寻踪之旅（一日游）",
        "duration": "6-8小时",
        "spots": [1, 2, 3, 4, 6, 7, 8],
        "desc": "深度体验南湖的历史文化，从红色文化到古迹探访，"
                "再到民俗体验，全方位感受南湖的文化底蕴。",
        "schedule": [
            "上午：南湖革命纪念馆（1.5小时）→ 红船瞻仰（30分钟）",
            "中午：湖心岛/烟雨楼（1小时）→ 午餐",
            "下午：揽秀园（45分钟）→ 壕股塔（30分钟）→ 南湖渔村（1小时）"
        ]
    }
]

FOOD_RECOMMENDATIONS = [
    {
        "name": "嘉兴粽子",
        "specialty": "五芳斋粽子",
        "desc": "嘉兴粽子是浙江嘉兴的特色传统名点，以五芳斋最为著名。"
                "选用上等糯米、猪后腿肉、咸蛋黄等原料，"
                "用箬叶包裹，经长时间蒸煮而成，香气扑鼻，软糯可口。",
        "where": "五芳斋总店（南湖天地店、建国路总店）"
    },
    {
        "name": "南湖菱",
        "specialty": "南湖无角菱",
        "desc": "南湖菱是嘉兴南湖的特产，以其无角（圆角）而闻名。"
                "菱肉洁白如玉，生食脆甜多汁，熟食粉糯香甜，"
                "是南湖最具代表性的时令美食。",
        "where": "南湖景区周边特产店、南湖天地"
    },
    {
        "name": "文虎酱鸭",
        "specialty": "嘉兴酱鸭",
        "desc": "文虎酱鸭是嘉兴的传统名菜，选用优质麻鸭，"
                "以秘制酱料腌渍后文火慢炖而成。"
                "成品色泽酱红，肉质紧实，酱香浓郁。",
        "where": "文虎酱鸭专卖店（南湖路店）"
    },
    {
        "name": "南湖鱼鲜",
        "specialty": "南湖白鱼、南湖河虾",
        "desc": "南湖水质优良，盛产多种淡水鱼鲜。"
                "白鱼肉质鲜嫩，河虾清甜弹牙。"
                "清蒸白鱼、盐水河虾是最地道的吃法。",
        "where": "南湖渔村、南湖天地各餐馆"
    }
]

TRANSPORT_INFO = {
    "external": {
        "高铁": [
            "嘉兴南站（推荐）- 距南湖景区约6公里，打车15分钟",
            "嘉兴站 - 距南湖景区约3公里，打车8分钟"
        ],
        "自驾": [
            "沪昆高速（G60）→ 嘉兴出口 → 南湖景区，上海出发约1.5小时",
            "常台高速（G15W）→ 嘉兴出口 → 南湖景区"
        ],
        "大巴": [
            "嘉兴汽车客运中心 → 换乘公交或打车至南湖景区"
        ],
        "飞机": [
            "杭州萧山国际机场 → 乘机场大巴至嘉兴（约1.5小时）",
            "上海虹桥机场 → 转高铁至嘉兴（约30分钟）"
        ]
    },
    "internal": {
        "公交": [
            "1路、5路、8路、28路等可达南湖景区",
            "南湖景区内部有观光车（10元/人）"
        ],
        "游船": [
            "会景园码头 → 湖心岛（往返船票含景区门票内）",
            "南湖夜游船（夏季开放，需另购票）"
        ],
        "步行": [
            "南湖景区主要景点集中在核心区域，步行游览最为惬意",
            "环湖步道全长约4.5公里，步行一圈约1小时"
        ]
    }
}

TICKET_INFO = {
    "门票": "南湖景区：免费开放（部分景点需购票）",
    "联票": "南湖景区联票：60元/人（含湖心岛船票、壕股塔）",
    "红船": "红船瞻仰：免费（需预约）",
    "纪念馆": "南湖革命纪念馆：免费（凭身份证领票）",
    "开放时间": "南湖景区：08:00-17:00（夏季至17:30）",
    "预约方式": "微信公众号「南湖景区」预约，或现场扫码预约"
}


# ========== 工具函数 ==========

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """打印程序标题"""
    banner = (
        "\n"
        "  +====================================================+\n"
        "  |                                                    |\n"
        "  |      ~~  嘉兴 . 南湖导游系统   ~~                 |\n"
        "  |     Nanhu Tour Guide System                        |\n"
        "  |                                                    |\n"
        "  |   轻烟拂渚，微风欲来                              |\n"
        "  |   -- 红色起点 . 江南明珠                          |\n"
        "  |                                                    |\n"
        "  +====================================================+\n"
    )
    print(banner)


def print_separator(char="─", length=56):
    """打印分隔线"""
    print(f"  {char * length}")


def print_menu_title(title):
    """打印菜单标题"""
    print()
    print(f"  📌 {title}")
    print_separator()


def print_info(label, value):
    """打印信息项"""
    print(f"  📍 {label}：{value}")


def wait_for_enter():
    """等待用户按回车继续"""
    input("\n  ⏎ 按回车键继续...")


def print_subtitle(text):
    """打印小标题"""
    print(f"\n  ┌─ {text} ─────────────────────────────┐")


def print_text(text, indent=True):
    """打印文本，自动换行"""
    prefix = "  " if indent else ""
    print(f"{prefix}{text}")


# ========== 功能模块 ==========

def show_spot_detail(spot):
    """显示单个景点详情"""
    clear_screen()
    print_banner()
    print()
    print(f"  🏛️  【{spot['name']}】")
    print_separator("═")
    print_info("类别", spot["category"])
    print_info("评分", spot["rating"])
    print_info("建议游览时长", spot["duration"])
    print()
    print_subtitle("景点介绍")
    print_text(spot["desc"])
    print()
    print_subtitle("历史背景")
    print_text(spot["history"])
    print()
    print_subtitle("游览小贴士")
    print_text(spot["tips"])


def list_all_spots():
    """列出所有景点"""
    clear_screen()
    print_banner()
    print_menu_title("南湖景点一览")
    
    # 按类别分组
    categories = {}
    for spot in SCENIC_SPOTS:
        cat = spot["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(spot)
    
    for cat, spots in categories.items():
        print(f"\n  ▸ {cat}")
        for spot in spots:
            print(f"    [{spot['id']}] {spot['name']}  {spot['rating']}")
    
    print()
    print_separator()
    
    while True:
        try:
            choice = input("  请输入景点编号查看详情（0返回主菜单）：")
            if choice == "0":
                return
            spot_id = int(choice)
            spot = next((s for s in SCENIC_SPOTS if s["id"] == spot_id), None)
            if spot:
                show_spot_detail(spot)
                wait_for_enter()
            else:
                print("  ❌ 无效编号，请重新输入。")
                continue
        except ValueError:
            print("  ❌ 请输入数字编号。")
            continue


def search_spots():
    """搜索景点"""
    clear_screen()
    print_banner()
    print_menu_title("🔍 搜索景点")
    
    keyword = input("  请输入关键词（名称/类别/描述）：").strip()
    if not keyword:
        print("  未输入关键词。")
        wait_for_enter()
        return
    
    results = []
    for spot in SCENIC_SPOTS:
        if (keyword in spot["name"] or 
            keyword in spot["category"] or 
            keyword in spot["desc"]):
            results.append(spot)
    
    if not results:
        print(f"\n  未找到包含{keyword}的景点。")
        wait_for_enter()
        return
    
    print(f"\n  找到 {len(results)} 个相关景点：")
    for spot in results:
        print(f"  [{spot['id']}] {spot['name']} - {spot['category']}")
        print(f"        {spot['desc'][:50]}...")
    
    print()
    while True:
        try:
            choice = input("  输入编号查看详情（0返回）：")
            if choice == "0":
                return
            spot_id = int(choice)
            spot = next((s for s in results if s["id"] == spot_id), None)
            if spot:
                show_spot_detail(spot)
                wait_for_enter()
                return
            else:
                print("  ❌ 无效编号。")
        except ValueError:
            print("  ❌ 请输入数字。")


def show_routes():
    """显示推荐路线"""
    clear_screen()
    print_banner()
    print_menu_title("🗺️ 推荐游览路线")
    
    for route in ROUTES:
        print(f"\n  ┌─ 路线{route['id']}：{route['name']}")
        print(f"  ├ 时长：{route['duration']}")
        print(f"  ├ 概述：{route['desc']}")
        print(f"  ├ 包含景点：", end="")
        spot_names = []
        for sid in route["spots"]:
            spot = next(s for s in SCENIC_SPOTS if s["id"] == sid)
            spot_names.append(spot["name"])
        print("、".join(spot_names))
        print(f"  └ 行程安排：")
        for step in route["schedule"]:
            print(f"      • {step}")
    
    wait_for_enter()


def show_transport():
    """显示交通信息"""
    clear_screen()
    print_banner()
    print_menu_title("🚗 交通指南")
    
    print("\n  ── 外部交通 ──")
    for mode, details in TRANSPORT_INFO["external"].items():
        print(f"\n  ▸ {mode}")
        for d in details:
            print(f"    • {d}")
    
    print("\n  ── 内部交通 ──")
    for mode, details in TRANSPORT_INFO["internal"].items():
        print(f"\n  ▸ {mode}")
        for d in details:
            print(f"    • {d}")
    
    wait_for_enter()


def show_food():
    """显示美食推荐"""
    clear_screen()
    print_banner()
    print_menu_title("🍜 嘉兴美食推荐")
    
    for food in FOOD_RECOMMENDATIONS:
        print(f"\n  ─── {food['name']} ───")
        print(f"  招牌：{food['specialty']}")
        print(f"  介绍：{food['desc']}")
        print(f"  推荐去处：{food['where']}")
    
    wait_for_enter()


def show_ticket():
    """显示门票信息"""
    clear_screen()
    print_banner()
    print_menu_title("🎫 门票及开放信息")
    
    for key, val in TICKET_INFO.items():
        print_info(key, val)
    
    print()
    print("  📌 温馨提示：")
    print("  • 建议提前在微信公众号「南湖景区」预约门票")
    print("  • 节假日游客较多，建议错峰出行")
    print("  • 景区内禁止无人机飞行（经批准除外）")
    print("  • 注意保护文物，请勿触摸红船及馆藏文物")
    
    wait_for_enter()


def show_weather_tips():
    """显示游览建议"""
    clear_screen()
    print_banner()
    print_menu_title("🌤️ 最佳游览时间及建议")
    
    tips_content = [
        ("最佳季节", "3-5月、9-11月，气温适宜，景色最美"),
        ("春季", "春暖花开，烟雨朦胧，最能感受烟雨楼的意境"),
        ("夏季", "荷花盛开，但天气炎热，注意防暑防晒"),
        ("秋季", "天高气爽，适合户外游览和摄影"),
        ("冬季", "游客较少，可安静品味历史文化"),
        ("建议时段", "上午8:00-11:00 或 下午15:00-17:00"),
        ("穿着建议", "舒适步行鞋，夏季防晒，春秋备外套"),
        ("携带物品", "身份证（纪念馆需凭身份证领票）、水、相机")
    ]
    
    for title, content in tips_content:
        print_info(title, content)
    
    wait_for_enter()


def show_history():
    """显示红色历史"""
    clear_screen()
    print_banner()
    print_menu_title("🚩 南湖红色历史")
    
    history_content = """
  中共一大与南湖红船
  ═════════════════════════════════════

  1921年7月23日，中国共产党第一次全国代表大会在上海
  法租界望志路106号（今兴业路76号）秘密开幕。

  7月30日晚，会议遭法租界巡捕袭扰，被迫中断。
  代表们决定转移，李达夫人王会悟建议到嘉兴南湖继续开会。

  8月初，代表们分两批抵达嘉兴：
  • 毛泽东、董必武、陈潭秋等乘早班火车先到
  • 其余代表乘后班火车抵达

  王会悟在南湖预订了一艘画舫（游船），
  代表们以游湖为掩护，在船上继续会议。

  会议通过了《中国共产党纲领》和《关于当前实际工作的决议》，
  选举陈独秀为中央局书记，宣告中国共产党正式成立。

  这艘画舫被称为"南湖红船"，
  成为中国革命源头的象征。

  ★ 红船精神：
    开天辟地、敢为人先的首创精神
    坚定理想、百折不挠的奋斗精神
    立党为公、忠诚为民的奉献精神
"""
    print(history_content)
    wait_for_enter()


def show_about():
    """显示关于程序"""
    clear_screen()
    print_banner()
    print_menu_title("📱 关于本程序")
    print("""
  嘉兴南湖导游系统 v1.0
  Nanhu Tour Guide System

  功能特色：
  • 景点详细介绍与搜索
  • 多主题游览路线推荐
  • 红色历史文化展示
  • 交通、美食实用信息
  • 门票预约与开放时间

  开发语言：Python 3
  数据来源：南湖景区官方资料
  适用平台：Windows / macOS / Linux
  ____________________________________
  
  🌊 嘉兴南湖 —— 中国共产党的诞生地
  🚩 欢迎您前来感受红色文化，领略江南风光！
""")
    wait_for_enter()


def interactive_qa():
    """智能问答功能"""
    qa_data = {
        "红船在哪里": "红船位于南湖湖心岛南侧，需乘船上岛参观。",
        "怎么预约": "关注微信公众号「南湖景区」进行预约，或现场扫码预约。",
        "门票多少钱": "南湖景区免费开放，部分景点如湖心岛船票、壕股塔需购票，联票60元/人。",
        "开放时间": "南湖景区开放时间 08:00-17:00（夏季至17:30）。",
        "纪念馆开放时间": "南湖革命纪念馆 09:00-17:00（16:30停止入馆），周一闭馆。",
        "怎么去南湖": "高铁到嘉兴南站或嘉兴站，公交1路、5路、8路可达。自驾走沪昆高速。",
        "游览多久": "半日游3-4小时，一日游6-8小时。",
        "附近还有什么": "嘉兴还有月河历史街区、西塘古镇、乌镇等著名景点。",
        "红船精神": "红船精神：开天辟地、敢为人先的首创精神；坚定理想、百折不挠的奋斗精神；立党为公、忠诚为民的奉献精神。",
    }
    
    clear_screen()
    print_banner()
    print_menu_title("💬 智能问答")
    print("  你可以问我以下问题（输入关键词即可）：")
    print("  红船在哪里 / 怎么预约 / 门票多少钱 / 开放时间")
    print("  纪念馆开放时间 / 怎么去南湖 / 游览多久 / 红船精神")
    print("  附近还有什么 / 推荐路线")
    print()
    
    count = 0
    while count < 5:  # 最多连续问5次
        question = input("  ❓ 请输入问题（输入0退出问答）：").strip()
        if question == "0":
            break
        
        if not question:
            continue
        
        # 简单匹配
        answered = False
        for keyword, answer in qa_data.items():
            if any(kw in question for kw in keyword.split("、")):
                print(f"\n  💡 {answer}\n")
                answered = True
                break
        
        if not answered:
            print("\n  🤔 抱歉，我不太理解这个问题。请换个方式问问看。\n")
            print("  你也可以使用主菜单的功能查看详细信息。\n")
        
        count += 1


# ========== 主菜单 ==========

def main_menu():
    """显示主菜单"""
    menu_items = [
        ("1", "🏛️  景点导览", "查看所有景点详细介绍"),
        ("2", "🔍  搜索景点", "按关键词搜索景点"),
        ("3", "🗺️  游览路线", "推荐游览路线规划"),
        ("4", "🚩  红色历史", "中共一大与南湖红船历史"),
        ("5", "🚗  交通指南", "外部与内部交通信息"),
        ("6", "🍜  美食推荐", "嘉兴特色美食介绍"),
        ("7", "🎫  门票信息", "门票价格与开放时间"),
        ("8", "🌤️  游览建议", "最佳游览时间与贴士"),
        ("9", "💬  智能问答", "常见问题快速解答"),
        ("0", "📱  关于程序", "关于本导游系统"),
        ("q", "🚪  退出程序", "退出导游系统"),
    ]
    
    clear_screen()
    print_banner()
    print_menuTitle = lambda title: print(f"  📌 {title}") or print_separator()
    print_menuTitle("主菜单")
    
    for num, name, desc in menu_items:
        print(f"  [{num}] {name}")
        print(f"       {desc}")
    
    print()


def run():
    """程序主循环"""
    menu_actions = {
        "1": list_all_spots,
        "2": search_spots,
        "3": show_routes,
        "4": show_history,
        "5": show_transport,
        "6": show_food,
        "7": show_ticket,
        "8": show_weather_tips,
        "9": interactive_qa,
        "0": show_about,
    }
    
    while True:
        main_menu()
        choice = input("  ⚡ 请选择功能：").strip().lower()
        
        if choice == "q":
            clear_screen()
            print_banner()
            print("\n  🌟 感谢使用嘉兴南湖导游系统！")
            print("  🌟 祝您在南湖度过愉快时光！")
            print("  🌟 '烟雨南湖，红色记忆 —— 欢迎再来！'\n")
            sys.exit(0)
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("\n  ❌ 无效选择，请重新输入。")
            wait_for_enter()


# ========== 程序入口 ==========

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n  🌟 感谢使用嘉兴南湖导游系统！再见！\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  ❌ 程序出现错误：{e}")
        print("  请重启程序。")
        sys.exit(1)
