#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#UI Design By PyMe--我用 Python 创世界
#https://www.py-me.com/

import tkinter as tk, json, threading, os, base64, io, sys
from tkinter import scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk

# 自动加载 .env 文件（支持 exe 同目录或当前目录）
try:
    from dotenv import load_dotenv
    # 先找 exe/脚本所在目录，再找当前工作目录
    基础路径 = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    load_dotenv(os.path.join(基础路径, '.env'))
    load_dotenv('.env')  # 也尝试工作目录
except ImportError:
    pass


# 安全：API Key 从环境变量 DeepSeek_API密钥 读取
api密钥 = os.environ.get("DeepSeek_API密钥", "")
if not api密钥:
    print("⚠ 警告：环境变量 DeepSeek_API密钥 未设置，AI 问答功能将不可用。")
    print("  请创建 .env 文件并写入 DeepSeek_API密钥=你的key")
接口地址 = "https://api.deepseek.com/chat/completions"
模型名 = "deepseek-chat"

分类内容 = {
    "景点导览": [
        "南湖红船（中共一大会址）——停泊在湖心岛旁，1921年中共一大在此闭幕，被誉为「中国共产党母亲的船」。",
        "烟雨楼——位于湖心岛上，始建于五代，因唐代诗人杜牧「南朝四百八十寺，多少楼台烟雨中」而得名。登楼可俯瞰南湖全景。",
        "壕股塔——又称南湖塔，位于南湖西岸，七层八角，高68米，可登塔远眺南湖及嘉兴市区风光。",
        "南湖革命纪念馆——位于南湖南岸，展示中共一大历史与红船精神的现代化展馆，免费开放。",
        "小瀛洲——南湖中的小岛，绿树成荫，亭台楼阁错落有致，有「浙北园林之冠」的美誉。",
        "揽秀园——南湖西岸的古典园林，园内假山流水、回廊曲折，是赏景休憩的好去处。",
        "会景园——南湖南岸的入口广场，集散中心所在地，有大型牌坊和文化长廊。",
        "端午祭坛——位于南湖西南岸，展示嘉兴端午民俗文化，每年端午举办龙舟赛。",
    ],
    "游览路线": [
        "路线一（红色经典之旅）：会景园 → 乘船 → 湖心岛（红船+烟雨楼）→ 南湖革命纪念馆 → 揽秀园",
        "路线二（环湖全览）：会景园 → 揽秀园 → 小瀛洲 → 壕股塔 → 端午祭坛 → 南湖革命纪念馆 → 湖心岛",
        "路线三（休闲半日游）：会景园 → 乘船 → 湖心岛 → 烟雨楼 → 返回会景园",
        "路线四（深度文化游）：南湖革命纪念馆 → 壕股塔 → 揽秀园 → 小瀛洲 → 湖心岛（红船+烟雨楼）",
    ],
    "红色历史": [
        "1921年7月，中共一大在上海法租界召开，因遭巡捕搜查，会议被迫中断。",
        "代表们转移到嘉兴南湖，在湖心岛的游船上继续举行会议。",
        "会议通过了《中国共产党纲领》和《关于当前实际工作的决议》，选举了中央领导机构。",
        "这艘游船后来被命名为「南湖红船」，成为中国革命起点的象征。",
        "红船精神：开天辟地、敢为人先的首创精神；坚定理想、百折不挠的奋斗精神；立党为公、忠诚为民的奉献精神。",
    ],
    "交通指南": [
        "【外部交通】",
        "高铁：嘉兴南站下车，乘游8路公交车直达南湖景区（约40分钟）。",
        "火车：嘉兴站下车，乘1路/8路公交车至南湖景区（约15分钟）。",
        "自驾：导航至「南湖景区会景园」，周边有多个停车场。",
        "",
        "【内部交通】",
        "游船：会景园码头→湖心岛（往返），票价20元/人。",
        "步行：环湖步道全长约5公里，适合步行游览。",
        "观光车：环湖观光车，招手即停，全程约30分钟。",
    ],
    "门票信息": [
        "【南湖景区】免费开放（需实名预约）。",
        "【湖心岛（红船+烟雨楼）】门票60元/人，含往返游船。",
        "【南湖革命纪念馆】免费开放，凭身份证入馆。",
        "【壕股塔】登塔10元/人。",
        "开放时间：景区 08:00-17:00；纪念馆 09:00-16:30（周一闭馆）。",
        "预约方式：微信公众号实名预约，或现场扫码。",
    ],
}

# 景点图片映射
# PyInstaller 打包后资源路径
if getattr(sys, 'frozen', False):
    基础路径 = sys._MEIPASS
else:
    基础路径 = os.path.dirname(__file__)
图片路径 = os.path.join(基础路径, "assets", "images")

景点图片 = {
    "红船":   ["thumb_hongchuan.jpg", "thumb_hongchuan2.jpg"],
    "烟雨楼": ["thumb_yanyulou.jpg", "thumb_yanyulou2.jpg"],
    "壕股塔": ["placeholder_haoguta.jpg"],
    "纪念馆": ["thumb_gemingjinianguan.jpg", "thumb_gemingjinianguan2.jpg"],
    "小瀛洲": ["placeholder_xiaoyingzhou.jpg"],
    "揽秀园": ["placeholder_lanxiuyuan.jpg"],
    "会景园": ["placeholder_huijingyuan.jpg"],
    "端午祭坛": ["placeholder_duanwujitan.jpg"],
}

分类图片 = {
    "景点导览": ["thumb_hongchuan.jpg", "thumb_yanyulou.jpg", "placeholder_haoguta.jpg",
                 "thumb_gemingjinianguan.jpg", "placeholder_xiaoyingzhou.jpg",
                 "placeholder_lanxiuyuan.jpg", "placeholder_huijingyuan.jpg",
                 "placeholder_duanwujitan.jpg"],
    "游览路线": ["thumb_hongchuan.jpg", "thumb_yanyulou.jpg", "thumb_gemingjinianguan.jpg"],
    "红色历史": ["thumb_hongchuan.jpg", "placeholder_huijingyuan.jpg"],
    "交通指南": ["placeholder_huijingyuan.jpg", "placeholder_haoguta.jpg"],
    "门票信息": ["thumb_gemingjinianguan.jpg", "placeholder_haoguta.jpg"],
}

分类图说 = {
    "景点导览": ["南湖红船", "烟雨楼", "壕股塔", "革命纪念馆", "小瀛洲",
                "揽秀园", "会景园", "端午祭坛"],
    "游览路线": ["南湖红船", "烟雨楼", "革命纪念馆"],
    "红色历史": ["南湖红船", "会景园入口"],
    "交通指南": ["会景园", "壕股塔远眺"],
    "门票信息": ["革命纪念馆", "壕股塔"],
}


def 问问ai(历史消息, ai响应成功, ai响应失败):
    def 发送请求():
        try:
            import urllib.request

            请求数据 = json.dumps({
                "model": 模型名,
                "messages": 历史消息,
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 1024,
            }).encode("utf-8")

            请求对象 = urllib.request.Request(
                接口地址,
                data=请求数据,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api密钥}",
                },
                method="POST",
            )

            with urllib.request.urlopen(请求对象, timeout=30) as 响应对象:
                响应体 = json.loads(响应对象.read().decode("utf-8"))
                回复 = 响应体["choices"][0]["message"]["content"]
                ai响应成功(回复)

        except Exception as e:
            ai响应失败(str(e))

    threading.Thread(target=发送请求, daemon=True).start()


def 图片转base64(文件名, 最大尺寸=2048):
    """读取图片并转为 base64 data URI，超长边自动缩放到最大尺寸"""
    try:
        图片 = Image.open(文件名)
        # 转 RGB（兼容 PNG 透明通道）
        if 图片.mode in ("RGBA", "P"):
            图片 = 图片.convert("RGB")
        宽, 高 = 图片.size
        if max(宽, 高) > 最大尺寸:
            缩放比例 = 最大尺寸 / max(宽, 高)
            图片 = 图片.resize((int(宽 * 缩放比例), int(高 * 缩放比例)), Image.LANCZOS)
        缓存 = io.BytesIO()
        图片.save(缓存, format="JPEG", quality=85)
        编码文本 = base64.b64encode(缓存.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{编码文本}"
    except Exception:
        return None


class 主窗口:
    def __init__(self, 根窗口):
        self.根窗口 = 根窗口
        self._朗读引擎 = None
        self._朗读中 = False
        self._tts内联按钮 = []  # 每个AI回复后的朗读按钮引用列表
        根窗口.title("嘉兴南湖导游系统")
        根窗口.geometry("1024x620")
        根窗口.resizable(True, True)
        根窗口.minsize(860, 520)

        主题红 = "#C41E24"
        self.LIGHT = "#FFF5F0"

        主体 = tk.Frame(根窗口)
        主体.pack(fill=tk.BOTH, expand=True)

        # ========== 左侧导航栏 ==========
        导航栏 = tk.Frame(主体, width=160, bg=主题红)
        导航栏.pack(side=tk.LEFT, fill=tk.Y)
        导航栏.pack_propagate(False)

        tk.Label(导航栏, text="南湖导游", font=("微软雅黑", 14, "bold"),
                 fg="white", bg=主题红, pady=12).pack(fill=tk.X)

        for 分类键 in 分类内容:
            按钮 = tk.Button(导航栏, text=分类键, font=("微软雅黑", 10),
                            fg="white", bg=主题红, activebackground="#8B0000",
                            activeforeground="white", relief=tk.FLAT,
                            bd=0, pady=6, cursor="hand2",
                            command=lambda n=分类键: self.展示(n))
            按钮.pack(fill=tk.X)

        tk.Frame(导航栏, height=1, bg="#FFD4D4").pack(fill=tk.X, pady=4)

        tk.Button(导航栏, text="AI问答", font=("微软雅黑", 10, "bold"),
                  fg="white", bg="#D4380D", activebackground="#8B2500",
                  activeforeground="white", relief=tk.RAISED,
                  bd=1, pady=6, cursor="hand2",
                  command=self.聊天).pack(fill=tk.X, padx=2)

        # ========== 内容区域（左侧文本 + 右侧图片）==========
        self.文本框架 = tk.Frame(主体)

        # 左：文本区
        文本容器 = tk.Frame(self.文本框架)
        文本容器.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 文本区顶部工具栏：标题 + 朗读按钮
        文本工具栏 = tk.Frame(文本容器, bg="#FFF5F0", height=30)
        文本工具栏.pack(fill=tk.X)
        文本工具栏.pack_propagate(False)

        self.文本朗读按钮 = tk.Button(文本工具栏, text="🔊 朗读介绍", font=("微软雅黑", 10),
                                      bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                      bd=0, padx=8, cursor="hand2",
                                      command=self.朗读当前介绍)
        self.文本朗读按钮.pack(side=tk.RIGHT, padx=(6, 2), pady=3)
        self.文本停止按钮 = tk.Button(文本工具栏, text="⏹ 停止", font=("微软雅黑", 10),
                                            bg="#FFD4D4", fg="#C41E24", relief=tk.FLAT,
                                            bd=0, padx=8, cursor="hand2",
                                            command=self.停止朗读)
        self.文本停止按钮.pack(side=tk.RIGHT, padx=2, pady=3)

        self.文本区 = scrolledtext.ScrolledText(文本容器, font=("微软雅黑", 11),
                                              bg=self.LIGHT, fg="#333333",
                                              wrap=tk.WORD, bd=0, padx=15, pady=15)
        self.文本区.pack(fill=tk.BOTH, expand=True)

        # 右：图片面板
        self.图片面板 = tk.Frame(self.文本框架, width=220, bg="#F5F0EB")
        self.图片面板.pack(side=tk.RIGHT, fill=tk.Y)
        self.图片面板.pack_propagate(False)

        # 图片标题
        self.图片标题 = tk.Label(self.图片面板, text="景点图片",
                                        font=("微软雅黑", 10, "bold"),
                                        bg="#8B4513", fg="white", pady=4)
        self.图片标题.pack(fill=tk.X)

        # 图片展示画布（可滚动）
        self.图片画布 = tk.Canvas(self.图片面板, bg="#F5F0EB",
                                    highlightthickness=0, width=210)
        self.图片滚动条 = tk.Scrollbar(self.图片面板, orient=tk.VERTICAL,
                                          command=self.图片画布.yview)
        self.图片可滚动区 = tk.Frame(self.图片画布, bg="#F5F0EB")

        self.图片可滚动区.bind("<Configure>",
                                 lambda e: self.图片画布.configure(scrollregion=self.图片画布.bbox("all")))
        self.图片画布.create_window((0, 0), window=self.图片可滚动区, anchor="nw", width=205)
        self.图片画布.configure(yscrollcommand=self.图片滚动条.set)

        self.图片画布.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.图片滚动条.pack(side=tk.RIGHT, fill=tk.Y)

        # ========== 聊天面板 ==========
        self.聊天面板 = tk.Frame(主体)
        self.聊天显示 = scrolledtext.ScrolledText(
            self.聊天面板, font=("微软雅黑", 11),
            bg="white", fg="#333333",
            wrap=tk.WORD, bd=0, padx=12, pady=12,
        )
        self.聊天显示.pack(fill=tk.BOTH, expand=True)
        self.聊天显示.config(state=tk.DISABLED)

        # 聊天输入区域（输入框 + 按钮行）
        输入框架 = tk.Frame(self.聊天面板, bg="#F0F0F0", height=50)
        输入框架.pack(fill=tk.X, side=tk.BOTTOM)
        输入框架.pack_propagate(False)

        # 所选图片预览标签
        self.图片预览 = tk.Label(输入框架, bg="#F0F0F0",
                                          font=("微软雅黑", 8), fg="#666666",
                                          padx=4, pady=2)

        self.输入框 = tk.Entry(输入框架, font=("微软雅黑", 11),
                              bd=1, relief=tk.SOLID)
        self.输入框.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 4), pady=8)
        self.输入框.bind("<Return>", lambda e: self.用户发送())

        self.发送按钮 = tk.Button(输入框架, text="发送", font=("微软雅黑", 10, "bold"),
                                  bg=主题红, fg="white", activebackground="#8B0000",
                                  activeforeground="white", bd=0, padx=12, pady=2,
                                  cursor="hand2", command=self.用户发送)
        self.发送按钮.pack(side=tk.RIGHT, padx=(4, 8), pady=8)

        # 朗读按钮
        self.聊天朗读按钮 = tk.Button(输入框架, text="🔊 朗读", font=("微软雅黑", 10),
                                  bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                  bd=0, padx=8, pady=2, cursor="hand2",
                                  command=self.朗读最后回复)
        self.聊天朗读按钮.pack(side=tk.RIGHT, padx=(2, 0), pady=8)
        self.聊天停止按钮 = tk.Button(输入框架, text="⏹ 停止", font=("微软雅黑", 10),
                                       bg="#FFD4D4", fg="#C41E24", relief=tk.FLAT,
                                       bd=0, padx=8, pady=2, cursor="hand2",
                                       command=self.停止朗读)
        self.聊天停止按钮.pack(side=tk.RIGHT, padx=2, pady=8)

        # 选择图片按钮
        self.图片按钮 = tk.Button(输入框架, text="🖼", font=("微软雅黑", 11),
                                  bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                  bd=0, padx=6, pady=2, cursor="hand2",
                                  command=self.选择图片)
        self.图片按钮.pack(side=tk.RIGHT, padx=(4, 0), pady=8)

        self.历史消息 = [
            {
                "role": "system",
                "content": (
                    "你是嘉兴南湖景区的智能导游助手。你熟悉南湖的所有景点、历史、交通、美食等信息。"
                    "请用中文友好地回答游客的问题，回答要简洁准确、有礼貌。"
                    "如果不知道答案，请如实说不知道，不要编造。"
                ),
            }
        ]

        # 缓存图片引用（防止被 GC 回收）
        self.图片缓存 = []

        # 当前选择的发送图片路径
        self.发送图片路径 = None

        self.展示("景点导览")

    def 换掉(self, 框架):
        for f in (self.文本框架, self.聊天面板):
            f.pack_forget()
        框架.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def 加载图片(self, 文件名, 宽度=190, 高度=140):
        """加载并缩放图片，返回 PhotoImage 对象"""
        路径 = os.path.join(图片路径, 文件名)
        if not os.path.exists(路径):
            return None
        try:
            图片 = Image.open(路径)
            宽, 高 = 图片.size
            缩放比例 = min(宽度 / 宽, 高度 / 高)
            新宽, 新高 = int(宽 * 缩放比例), int(高 * 缩放比例)
            图片 = 图片.resize((新宽, 新高), Image.LANCZOS)
            return ImageTk.PhotoImage(图片)
        except Exception:
            return None

    def 加载大图(self, 文件名, 最大尺寸=800):
        """加载完整分辨率图片（用于弹出大图窗口），缩放至最大尺寸内"""
        路径 = os.path.join(图片路径, 文件名)
        if not os.path.exists(路径):
            # 尝试非 thumb 版本
            原文件名 = 文件名.replace("thumb_", "")
            路径 = os.path.join(图片路径, 原文件名)
        if not os.path.exists(路径):
            return None
        try:
            图片 = Image.open(路径)
            宽, 高 = 图片.size
            缩放比例 = min(最大尺寸 / 宽, 最大尺寸 / 高, 1.0)
            if 缩放比例 < 1.0:
                图片 = 图片.resize((int(宽 * 缩放比例), int(高 * 缩放比例)), Image.LANCZOS)
            return ImageTk.PhotoImage(图片)
        except Exception:
            return None

    def 清空图片面板(self):
        for 组件 in self.图片可滚动区.winfo_children():
            组件.destroy()
        self.图片缓存.clear()

    def 打开大图(self, 文件名, 图说=""):
        """弹出新窗口显示大图"""
        照片 = self.加载大图(文件名)
        if 照片 is None:
            messagebox.showinfo("提示", "暂无高清图片")
            return

        新窗口 = tk.Toplevel(self.根窗口)
        新窗口.title(f"南湖景点 — {图说}" if 图说 else "南湖景点")
        新窗口.configure(bg="#333333")

        # 窗口大小跟随图片
        图宽 = 照片.width()
        图高 = 照片.height()
        新窗口.geometry(f"{图宽 + 40}x{图高 + 80}")

        # 图片标签
        标签 = tk.Label(新窗口, image=照片, bg="#333333", cursor="hand2")
        标签.image = 照片  # 防止 GC
        标签.pack(expand=True, padx=20, pady=(20, 5))

        # 标题
        if 图说:
            tk.Label(新窗口, text=图说, font=("微软雅黑", 10),
                     bg="#333333", fg="white").pack(pady=(0, 10))

        # 点击关闭
        新窗口.bind("<Button-1>", lambda e: 新窗口.destroy())
        标签.bind("<Button-1>", lambda e: 新窗口.destroy())

        # 按 ESC 关闭
        新窗口.bind("<Escape>", lambda e: 新窗口.destroy())
        新窗口.focus_set()

    def 显示图片组(self, 文件名列表, 图说列表=None):
        """在图片面板中显示一组图片（可点击放大）"""
        self.清空图片面板()
        for 序号, 文件名 in enumerate(文件名列表):
            照片 = self.加载图片(文件名)
            if 照片 is None:
                continue
            self.图片缓存.append(照片)

            容器 = tk.Frame(self.图片可滚动区, bg="#F5F0EB", padx=8, pady=4)
            容器.pack(fill=tk.X)

            图说 = 图说列表[序号] if 图说列表 and 序号 < len(图说列表) else ""

            标签 = tk.Label(容器, image=照片, bg="#F5F0EB",
                           cursor="hand2", relief=tk.FLAT)
            标签.image = 照片
            标签.pack(pady=(4, 0))

            # 绑定点击放大 — 传入文件名和图说
            标签.bind("<Button-1>",
                     lambda e, fn=文件名, c=图说: self.打开大图(fn, c))

            if 图说:
                tk.Label(容器, text=图说, font=("微软雅黑", 8),
                         bg="#F5F0EB", fg="#666666", wraplength=190).pack()

            if 序号 < len(文件名列表) - 1:
                tk.Frame(容器, height=1, bg="#DDDDDD").pack(fill=tk.X, pady=4)

    def 展示(self, 分类名):
        self.换掉(self.文本框架)
        self.文本区.config(state=tk.NORMAL)
        self.文本区.delete(1.0, tk.END)

        self.文本区.insert(tk.END, f"🏛 {分类名}\n\n", "title")
        self.文本区.tag_config("title", font=("微软雅黑", 16, "bold"),
                             foreground="#C41E24", spacing3=10)

        for 条目 in 分类内容[分类名]:
            self.文本区.insert(tk.END, f"  • {条目}\n\n", "content")
        self.文本区.tag_config("content", font=("微软雅黑", 10),
                             foreground="#333333", spacing1=4, spacing3=4)

        self.文本区.config(state=tk.DISABLED)
        self.展示分类图片(分类名)

    def 展示分类图片(self, 分类名):
        """根据分类显示对应的图片"""
        if 分类名 in 分类图片:
            self.显示图片组(分类图片[分类名], 分类图说.get(分类名))

    def 显示景点图片(self, 景点名):
        """根据景点名显示对应图片"""
        if 景点名 in 景点图片:
            self.显示图片组(景点图片[景点名])

    def 聊天(self):
        self.换掉(self.聊天面板)

    def 朗读_通用(self, 文本, 完成回调=None):
        """使用 Windows SAPI5 朗读文本（异步）"""
        try:
            import pyttsx3
            self._朗读引擎 = pyttsx3.init(driverName='sapi5')
            self._朗读引擎.setProperty('rate', 200)
            self._朗读引擎.setProperty('volume', 1.0)

            # 选择中文语音
            所有语音 = self._朗读引擎.getProperty('voices')
            for 语音 in 所有语音:
                if 'Chinese' in 语音.name or '中文' in 语音.name:
                    self._朗读引擎.setProperty('voice', 语音.id)
                    break

            self._朗读中 = True

            def 朗读():
                self._朗读引擎.say(文本)
                self._朗读引擎.runAndWait()
                self._朗读中 = False
                if 完成回调:
                    完成回调()

            threading.Thread(target=朗读, daemon=True).start()

        except Exception as e:
            self._朗读中 = False
            messagebox.showwarning("语音提示", f"语音朗读初始化失败：{e}")

    def 停止朗读(self):
        """停止当前朗读"""
        try:
            if self._朗读引擎 and self._朗读中:
                self._朗读引擎.stop()
            self._朗读中 = False
            self._重置内联按钮()
        except Exception:
            pass

    def _重置内联按钮(self):
        """将所有内联朗读按钮重置为朗读状态"""
        for 按钮 in self._tts内联按钮:
            try:
                按钮.config(text="🔊 朗读", bg="#E8E8E8", fg="#333333")
            except Exception:
                pass

    def _添加内联朗读按钮(self, 回复文本):
        """在AI回复后嵌入一个朗读/停止切换按钮"""
        self.聊天显示.config(state=tk.NORMAL)

        按钮框架 = tk.Frame(self.聊天显示, bg=self.LIGHT)
        朗读按钮 = tk.Button(按钮框架, text="🔊 朗读", font=("微软雅黑", 9),
                            bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                            bd=0, padx=6, pady=1, cursor="hand2",
                            activebackground="#D0D0D0")
        朗读按钮.pack(side=tk.LEFT, padx=(4, 0))

        # 记录按钮引用
        self._tts内联按钮.append(朗读按钮)

        def 切换朗读():
            if 朗读按钮.cget("text") == "🔊 朗读":
                # 切换到停止状态 → 开始朗读
                朗读按钮.config(text="⏹ 停止", bg="#FFD4D4", fg="#C41E24")
                # 朗读完成后的回调：恢复按钮
                def 朗读完成():
                    try:
                        朗读按钮.config(text="🔊 朗读", bg="#E8E8E8", fg="#333333")
                    except Exception:
                        pass
                self.朗读_通用(回复文本, 朗读完成)
            else:
                # 单击停止 → 停止朗读
                self.停止朗读()
                # 停止朗读中的 _重置内联按钮 已经恢复所有按钮

        朗读按钮.config(command=切换朗读)

        self.聊天显示.window_create(tk.END, window=按钮框架)
        self.聊天显示.insert(tk.END, "\n")
        self.聊天显示.see(tk.END)
        self.聊天显示.config(state=tk.DISABLED)

    def 朗读当前介绍(self):
        """朗读左侧文本区的当前景点介绍内容"""
        全部文本 = self.文本区.get("1.0", tk.END).strip()
        if not 全部文本:
            messagebox.showinfo("提示", "当前没有景点介绍内容")
            return
        self.朗读_通用(全部文本)

    def 朗读最后回复(self):
        """朗读最后一条 AI 回复内容（使用 Windows 中文语音）"""
        # 从聊天显示控件中提取最后一段 AI 回复
        全部文本 = self.聊天显示.get("1.0", tk.END).strip()
        if not 全部文本:
            messagebox.showinfo("提示", "没有可朗读的内容")
            return

        # 查找最后一段 【AI】 标记之后的内容
        位置 = 全部文本.rfind("【AI】")
        if 位置 != -1:
            回复文本 = 全部文本[位置 + 4:].strip()
            if 回复文本:
                self.朗读_通用(回复文本)
                return

        # 找不到 【AI】 时，朗读所有聊天内容
        # 去掉标记符号，保留纯文本
        纯文本 = 全部文本.replace("【你】", "").replace("【AI】", "").replace("【系统】", "")
        if 纯文本.strip():
            self.朗读_通用(纯文本)
        else:
            messagebox.showinfo("提示", "暂无 AI 回复可朗读")

    def 选择图片(self):
        """打开文件选择对话框选择图片"""
        路径 = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp")],
        )
        if not 路径:
            return
        self.发送图片路径 = 路径

        # 显示预览缩略图
        try:
            图片 = Image.open(路径)
            图片.thumbnail((40, 40))
            照片 = ImageTk.PhotoImage(图片)
            self.图片预览.configure(image=照片, text="")
            self.图片预览.image = 照片
            self.图片预览.pack(side=tk.LEFT, padx=(8, 0), pady=4)
        except Exception:
            self.图片预览.configure(text="[图片]", image="")
            self.图片预览.pack(side=tk.LEFT, padx=(8, 0), pady=4)

    def 加一句(self, 文本, 标签):
        self.聊天显示.config(state=tk.NORMAL)
        self.聊天显示.insert(tk.END, 文本, 标签)
        self.聊天显示.see(tk.END)
        self.聊天显示.config(state=tk.DISABLED)

    def 加图片到聊天(self, 图片路径):
        """在聊天区域插入图片预览"""
        try:
            图片 = Image.open(图片路径)
            图片.thumbnail((200, 150))
            照片 = ImageTk.PhotoImage(图片)
            self.图片缓存.append(照片)  # 保持引用
            self.聊天显示.config(state=tk.NORMAL)
            self.聊天显示.image_create(tk.END, image=照片)
            self.聊天显示.insert(tk.END, "\n")
            self.聊天显示.see(tk.END)
            self.聊天显示.config(state=tk.DISABLED)
        except Exception:
            pass

    def 用户发送(self):
        用户文本 = self.输入框.get().strip()
        有图片 = self.发送图片路径 is not None

        if not 用户文本 and not 有图片:
            return

        self.输入框.delete(0, tk.END)
        self.发送按钮.config(state=tk.DISABLED)
        self.图片按钮.config(state=tk.DISABLED)

        # 在聊天区显示用户消息
        if 用户文本:
            self.加一句(f"\n【你】{用户文本}\n", "user_msg")

        # 如果有图片，显示在聊天区
        图片路径 = self.发送图片路径
        if 图片路径:
            self.加图片到聊天(图片路径)
            self.发送图片路径 = None
            self.图片预览.pack_forget()
            self.图片预览.configure(image="", text="")

        思考位置 = self.聊天显示.index(tk.END)
        self.加一句("\n【AI】\n", "thinking")
        self.聊天显示.tag_config("thinking", foreground="#888888",
                                     font=("微软雅黑", 10, "italic"))

        # 构建消息体（DeepSeek 不支持图片多模态，有图片时只发文本）
        if 有图片 and 图片路径:
            # 只发文本，不加图片数据（API 不支持 image_url）
            待发文本 = 用户文本 or "请介绍一下这张图片中的景点"
            请求消息 = self.历史消息 + [
                {"role": "user", "content": 待发文本}
            ]
        else:
            请求消息 = self.历史消息 + [
                {"role": "user", "content": 用户文本}
            ]

        def ai响应成功(回复):
            self.聊天显示.config(state=tk.NORMAL)
            self.聊天显示.delete(思考位置, tk.END)
            self.聊天显示.config(state=tk.DISABLED)

            self.加一句(f"\n【AI】{回复}\n\n", "ai_msg")
            self.聊天显示.tag_config("ai_msg", foreground="#333333",
                                         font=("微软雅黑", 10))
            # 在每个AI回复后添加朗读/停止按钮
            self._添加内联朗读按钮(回复)
            # 只保存文本到历史（不存图片 base64，避免上下文膨胀）
            if 用户文本:
                self.历史消息.append({"role": "user", "content": 用户文本})
            else:
                self.历史消息.append({"role": "user", "content": "[用户发送了一张图片]"})
            self.发送按钮.config(state=tk.NORMAL)
            self.图片按钮.config(state=tk.NORMAL)

        def ai响应失败(错误):
            self.聊天显示.config(state=tk.NORMAL)
            self.聊天显示.delete(思考位置, tk.END)
            self.聊天显示.config(state=tk.DISABLED)

            错误消息 = f"\n【系统】请求失败：{错误}\n\n"
            self.加一句(错误消息, "err_msg")
            self.聊天显示.tag_config("err_msg", foreground="#CC0000",
                                         font=("微软雅黑", 10))
            self.发送按钮.config(state=tk.NORMAL)
            self.图片按钮.config(state=tk.NORMAL)

        问问ai(请求消息, ai响应成功, ai响应失败)


def 启动():
    根窗口 = tk.Tk()
    app = 主窗口(根窗口)
    根窗口.mainloop()

if __name__ == "__main__":
    启动()
