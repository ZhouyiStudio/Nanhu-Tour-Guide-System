#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#UI Design By PyMe--我用 Python 创世界
#https://www.py-me.com/

import tkinter as tk, json, threading, os, base64, io
from tkinter import scrolledtext, filedialog, messagebox
from PIL import Image, ImageTk


api密钥 = "sk-已删除_请使用环境变量DeepSeek_API密钥"#偷key的是gay
api地址 = "https://api.deepseek.com/chat/completions"
模型 = "deepseek-chat"

fl = {
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
IMG_DIR = os.path.join(os.path.dirname(__file__), "assets", "images")

SPOT_IMAGES = {
    "红船":   ["thumb_hongchuan.jpg", "thumb_hongchuan2.jpg"],
    "烟雨楼": ["thumb_yanyulou.jpg", "thumb_yanyulou2.jpg"],
    "壕股塔": ["placeholder_haoguta.jpg"],
    "纪念馆": ["thumb_gemingjinianguan.jpg", "thumb_gemingjinianguan2.jpg"],
    "小瀛洲": ["placeholder_xiaoyingzhou.jpg"],
    "揽秀园": ["placeholder_lanxiuyuan.jpg"],
    "会景园": ["placeholder_huijingyuan.jpg"],
    "端午祭坛": ["placeholder_duanwujitan.jpg"],
}

CATEGORY_IMAGES = {
    "景点导览": ["thumb_hongchuan.jpg", "thumb_yanyulou.jpg", "placeholder_haoguta.jpg",
                 "thumb_gemingjinianguan.jpg", "placeholder_xiaoyingzhou.jpg",
                 "placeholder_lanxiuyuan.jpg", "placeholder_huijingyuan.jpg",
                 "placeholder_duanwujitan.jpg"],
    "游览路线": ["thumb_hongchuan.jpg", "thumb_yanyulou.jpg", "thumb_gemingjinianguan.jpg"],
    "红色历史": ["thumb_hongchuan.jpg", "placeholder_huijingyuan.jpg"],
    "交通指南": ["placeholder_huijingyuan.jpg", "placeholder_haoguta.jpg"],
    "门票信息": ["thumb_gemingjinianguan.jpg", "placeholder_haoguta.jpg"],
}

CATEGORY_CAPTIONS = {
    "景点导览": ["南湖红船", "烟雨楼", "壕股塔", "革命纪念馆", "小瀛洲",
                "揽秀园", "会景园", "端午祭坛"],
    "游览路线": ["南湖红船", "烟雨楼", "革命纪念馆"],
    "红色历史": ["南湖红船", "会景园入口"],
    "交通指南": ["会景园", "壕股塔远眺"],
    "门票信息": ["革命纪念馆", "壕股塔"],
}


def 问问ai(messages, ai响应成功, ai响应失败):
    def 发送请求():
        try:
            import urllib.request

            data = json.dumps({
                "model": 模型,
                "messages": messages,
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 1024,
            }).encode("utf-8")

            req = urllib.request.Request(
                api地址,
                data=data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api密钥}",
                },
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                reply = body["choices"][0]["message"]["content"]
                ai响应成功(reply)

        except Exception as e:
            ai响应失败(str(e))

    threading.Thread(target=发送请求, daemon=True).start()


def 图片转base64(path, max_size=2048):
    """读取图片并转为 base64 data URI，超长边自动缩放到 max_size"""
    try:
        img = Image.open(path)
        # 转 RGB（兼容 PNG 透明通道）
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        w, h = img.size
        if max(w, h) > max_size:
            scale = max_size / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{b64}"
    except Exception:
        return None


class 主窗口:
    def __init__(self, root):
        self.root = root
        self._朗读引擎 = None
        self._朗读中 = False
        root.title("嘉兴南湖导游系统")
        root.geometry("1024x620")
        root.resizable(True, True)
        root.minsize(860, 520)

        RED = "#C41E24"
        LIGHT = "#FFF5F0"

        main = tk.Frame(root)
        main.pack(fill=tk.BOTH, expand=True)

        # ========== 左侧导航栏 ==========
        nav = tk.Frame(main, width=160, bg=RED)
        nav.pack(side=tk.LEFT, fill=tk.Y)
        nav.pack_propagate(False)

        tk.Label(nav, text="南湖导游", font=("微软雅黑", 14, "bold"),
                 fg="white", bg=RED, pady=12).pack(fill=tk.X)

        for name in fl:
            btn = tk.Button(nav, text=name, font=("微软雅黑", 10),
                            fg="white", bg=RED, activebackground="#8B0000",
                            activeforeground="white", relief=tk.FLAT,
                            bd=0, pady=6, cursor="hand2",
                            command=lambda n=name: self.展示(n))
            btn.pack(fill=tk.X)

        tk.Frame(nav, height=1, bg="#FFD4D4").pack(fill=tk.X, pady=4)

        tk.Button(nav, text="AI问答", font=("微软雅黑", 10, "bold"),
                  fg="white", bg="#D4380D", activebackground="#8B2500",
                  activeforeground="white", relief=tk.RAISED,
                  bd=1, pady=6, cursor="hand2",
                  command=self.聊天).pack(fill=tk.X, padx=2)

        # ========== 内容区域（左侧文本 + 右侧图片）==========
        self.text_frame = tk.Frame(main)

        # 左：文本区
        text_container = tk.Frame(self.text_frame)
        text_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 文本区顶部工具栏：标题 + 朗读按钮
        text_toolbar = tk.Frame(text_container, bg="#FFF5F0", height=30)
        text_toolbar.pack(fill=tk.X)
        text_toolbar.pack_propagate(False)

        self.text_tts_btn = tk.Button(text_toolbar, text="🔊 朗读介绍", font=("微软雅黑", 10),
                                      bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                      bd=0, padx=8, cursor="hand2",
                                      command=self.朗读当前介绍)
        self.text_tts_btn.pack(side=tk.RIGHT, padx=(6, 2), pady=3)
        self.text_tts_stop_btn = tk.Button(text_toolbar, text="⏹ 停止", font=("微软雅黑", 10),
                                           bg="#FFD4D4", fg="#C41E24", relief=tk.FLAT,
                                           bd=0, padx=8, cursor="hand2",
                                           command=self.停止朗读)
        self.text_tts_stop_btn.pack(side=tk.RIGHT, padx=2, pady=3)

        self.text = scrolledtext.ScrolledText(text_container, font=("微软雅黑", 11),
                                              bg=LIGHT, fg="#333333",
                                              wrap=tk.WORD, bd=0, padx=15, pady=15)
        self.text.pack(fill=tk.BOTH, expand=True)

        # 右：图片面板
        self.image_panel_frame = tk.Frame(self.text_frame, width=220, bg="#F5F0EB")
        self.image_panel_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_panel_frame.pack_propagate(False)

        # 图片标题
        self.img_title_label = tk.Label(self.image_panel_frame, text="景点图片",
                                        font=("微软雅黑", 10, "bold"),
                                        bg="#8B4513", fg="white", pady=4)
        self.img_title_label.pack(fill=tk.X)

        # 图片展示画布（可滚动）
        self.img_canvas = tk.Canvas(self.image_panel_frame, bg="#F5F0EB",
                                    highlightthickness=0, width=210)
        self.img_scrollbar = tk.Scrollbar(self.image_panel_frame, orient=tk.VERTICAL,
                                          command=self.img_canvas.yview)
        self.img_scrollable = tk.Frame(self.img_canvas, bg="#F5F0EB")

        self.img_scrollable.bind("<Configure>",
                                 lambda e: self.img_canvas.configure(scrollregion=self.img_canvas.bbox("all")))
        self.img_canvas.create_window((0, 0), window=self.img_scrollable, anchor="nw", width=205)
        self.img_canvas.configure(yscrollcommand=self.img_scrollbar.set)

        self.img_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.img_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ========== 聊天面板 ==========
        self.chat_frame = tk.Frame(main)
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, font=("微软雅黑", 11),
            bg="white", fg="#333333",
            wrap=tk.WORD, bd=0, padx=12, pady=12,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # 聊天输入区域（输入框 + 按钮行）
        input_frame = tk.Frame(self.chat_frame, bg="#F0F0F0", height=50)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM)
        input_frame.pack_propagate(False)

        # 所选图片预览标签
        self.img_preview_label = tk.Label(input_frame, bg="#F0F0F0",
                                          font=("微软雅黑", 8), fg="#666666",
                                          padx=4, pady=2)

        self.entry = tk.Entry(input_frame, font=("微软雅黑", 11),
                              bd=1, relief=tk.SOLID)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 4), pady=8)
        self.entry.bind("<Return>", lambda e: self.用户发送())

        self.send_btn = tk.Button(input_frame, text="发送", font=("微软雅黑", 10, "bold"),
                                  bg=RED, fg="white", activebackground="#8B0000",
                                  activeforeground="white", bd=0, padx=12, pady=2,
                                  cursor="hand2", command=self.用户发送)
        self.send_btn.pack(side=tk.RIGHT, padx=(4, 8), pady=8)

        # 朗读按钮
        self.tts_btn = tk.Button(input_frame, text="🔊 朗读", font=("微软雅黑", 10),
                                 bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                 bd=0, padx=8, pady=2, cursor="hand2",
                                 command=self.朗读最后回复)
        self.tts_btn.pack(side=tk.RIGHT, padx=(2, 0), pady=8)
        self.tts_stop_btn = tk.Button(input_frame, text="⏹ 停止", font=("微软雅黑", 10),
                                      bg="#FFD4D4", fg="#C41E24", relief=tk.FLAT,
                                      bd=0, padx=8, pady=2, cursor="hand2",
                                      command=self.停止朗读)
        self.tts_stop_btn.pack(side=tk.RIGHT, padx=2, pady=8)

        # 选择图片按钮
        self.img_btn = tk.Button(input_frame, text="🖼", font=("微软雅黑", 11),
                                 bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                 bd=0, padx=6, pady=2, cursor="hand2",
                                 command=self.选择图片)
        self.img_btn.pack(side=tk.RIGHT, padx=(4, 0), pady=8)

        self.messages = [
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
        self._image_refs = []

        # 当前选择的发送图片路径
        self.发送图片路径 = None

        self.展示("景点导览")

    def 换掉(self, frame):
        for f in (self.text_frame, self.chat_frame):
            f.pack_forget()
        frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def 加载图片(self, filename, width=190, height=140):
        """加载并缩放图片，返回 PhotoImage 对象"""
        path = os.path.join(IMG_DIR, filename)
        if not os.path.exists(path):
            return None
        try:
            img = Image.open(path)
            w, h = img.size
            scale = min(width / w, height / h)
            new_w, new_h = int(w * scale), int(h * scale)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def 加载大图(self, filename, max_size=800):
        """加载完整分辨率图片（用于弹出大图窗口），缩放至 max_size 内"""
        path = os.path.join(IMG_DIR, filename)
        if not os.path.exists(path):
            # 尝试非 thumb 版本
            real_name = filename.replace("thumb_", "")
            path = os.path.join(IMG_DIR, real_name)
        if not os.path.exists(path):
            return None
        try:
            img = Image.open(path)
            w, h = img.size
            scale = min(max_size / w, max_size / h, 1.0)
            if scale < 1.0:
                img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def 清空图片面板(self):
        for w in self.img_scrollable.winfo_children():
            w.destroy()
        self._image_refs.clear()

    def 打开大图(self, filename, caption=""):
        """弹出新窗口显示大图"""
        photo = self.加载大图(filename)
        if photo is None:
            messagebox.showinfo("提示", "暂无高清图片")
            return

        top = tk.Toplevel(self.root)
        top.title(f"南湖景点 — {caption}" if caption else "南湖景点")
        top.configure(bg="#333333")

        # 窗口大小跟随图片
        img_w = photo.width()
        img_h = photo.height()
        top.geometry(f"{img_w + 40}x{img_h + 80}")

        # 图片标签
        lbl = tk.Label(top, image=photo, bg="#333333", cursor="hand2")
        lbl.image = photo  # 防止 GC
        lbl.pack(expand=True, padx=20, pady=(20, 5))

        # 标题
        if caption:
            tk.Label(top, text=caption, font=("微软雅黑", 10),
                     bg="#333333", fg="white").pack(pady=(0, 10))

        # 点击关闭
        top.bind("<Button-1>", lambda e: top.destroy())
        lbl.bind("<Button-1>", lambda e: top.destroy())

        # 按 ESC 关闭
        top.bind("<Escape>", lambda e: top.destroy())
        top.focus_set()

    def 显示图片组(self, filenames, captions=None):
        """在图片面板中显示一组图片（可点击放大）"""
        self.清空图片面板()
        for i, fname in enumerate(filenames):
            photo = self.加载图片(fname)
            if photo is None:
                continue
            self._image_refs.append(photo)

            container = tk.Frame(self.img_scrollable, bg="#F5F0EB", padx=8, pady=4)
            container.pack(fill=tk.X)

            cap = captions[i] if captions and i < len(captions) else ""

            lbl = tk.Label(container, image=photo, bg="#F5F0EB",
                           cursor="hand2", relief=tk.FLAT)
            lbl.image = photo
            lbl.pack(pady=(4, 0))

            # 绑定点击放大 — 传入文件名和图说
            lbl.bind("<Button-1>",
                     lambda e, fn=fname, c=cap: self.打开大图(fn, c))

            if cap:
                tk.Label(container, text=cap, font=("微软雅黑", 8),
                         bg="#F5F0EB", fg="#666666", wraplength=190).pack()

            if i < len(filenames) - 1:
                tk.Frame(container, height=1, bg="#DDDDDD").pack(fill=tk.X, pady=4)

    def 展示(self, category):
        self.换掉(self.text_frame)
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)

        self.text.insert(tk.END, f"🏛 {category}\n\n", "title")
        self.text.tag_config("title", font=("微软雅黑", 16, "bold"),
                             foreground="#C41E24", spacing3=10)

        for item in fl[category]:
            if item.startswith("【"):
                self.text.insert(tk.END, f"\n{item}\n", "header")
                self.text.tag_config("header", font=("微软雅黑", 12, "bold"),
                                     foreground="#8B4513", spacing1=5)
            else:
                self.text.insert(tk.END, f"  {item}\n\n", "body")
                self.text.tag_config("body", font=("微软雅黑", 11),
                                     spacing1=3, spacing2=3)

        self.text.config(state=tk.DISABLED)
        self.展示分类图片(category)

    def 展示分类图片(self, category):
        if category in CATEGORY_IMAGES:
            caps = CATEGORY_CAPTIONS.get(category, [])
            self.显示图片组(CATEGORY_IMAGES[category], caps)

    def 显示景点图片(self, spot_name):
        for keyword, imgs in SPOT_IMAGES.items():
            if keyword in spot_name:
                self.显示图片组(imgs, [spot_name])
                return
        self.清空图片面板()
        tk.Label(self.img_scrollable, text="暂无图片",
                 font=("微软雅黑", 10), bg="#F5F0EB", fg="#999999",
                 pady=40).pack()

    def 聊天(self):
        self.换掉(self.chat_frame)
        self.entry.focus_set()

    def 朗读_通用(self, 文本):
        """底层朗读函数：用Windows中文语音朗读文本"""
        if not 文本 or not 文本.strip():
            return

        # 如果正在朗读，先停止
        self.停止朗读()

        import threading as _t

        def 朗读():
            try:
                import pyttsx3
                engine = pyttsx3.init()
                self._朗读引擎 = engine
                self._朗读中 = True
                engine.say(文本)
                engine.runAndWait()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("朗读失败", str(e)))
            finally:
                self._朗读中 = False
                self._朗读引擎 = None

        _t.Thread(target=朗读, daemon=True).start()

    def 停止朗读(self):
        """停止当前朗读"""
        self._朗读中 = False
        if self._朗读引擎 is not None:
            try:
                self._朗读引擎.stop()
            except Exception:
                pass
            self._朗读引擎 = None

    def 朗读当前介绍(self):
        """朗读左侧文本区的当前景点介绍内容"""
        全部文本 = self.text.get("1.0", tk.END).strip()
        if not 全部文本:
            messagebox.showinfo("提示", "当前没有景点介绍内容")
            return
        self.朗读_通用(全部文本)

    def 朗读最后回复(self):
        """朗读最后一条 AI 回复内容（使用 Windows 中文语音）"""
        # 从聊天显示控件中提取最后一段 AI 回复
        全部文本 = self.chat_display.get("1.0", tk.END).strip()
        if not 全部文本:
            messagebox.showinfo("提示", "没有可朗读的内容")
            return

        # 查找最后一段 【AI】 标记之后的内容
        idx = 全部文本.rfind("【AI】")
        if idx != -1:
            回复文本 = 全部文本[idx + 4:].strip()
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
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp")],
        )
        if not path:
            return
        self.发送图片路径 = path

        # 显示预览缩略图
        try:
            img = Image.open(path)
            img.thumbnail((40, 40))
            photo = ImageTk.PhotoImage(img)
            self.img_preview_label.configure(image=photo, text="")
            self.img_preview_label.image = photo
            self.img_preview_label.pack(side=tk.LEFT, padx=(8, 0), pady=4)
        except Exception:
            self.img_preview_label.configure(text="[图片]", image="")
            self.img_preview_label.pack(side=tk.LEFT, padx=(8, 0), pady=4)

    def 加一句(self, text, tag):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text, tag)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def 加图片到聊天(self, path):
        """在聊天区域插入图片预览"""
        try:
            img = Image.open(path)
            img.thumbnail((200, 150))
            photo = ImageTk.PhotoImage(img)
            self._image_refs.append(photo)  # 保持引用
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.image_create(tk.END, image=photo)
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
        except Exception:
            pass

    def 用户发送(self):
        user_text = self.entry.get().strip()
        has_image = self.发送图片路径 is not None

        if not user_text and not has_image:
            return

        self.entry.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED)
        self.img_btn.config(state=tk.DISABLED)

        # 在聊天区显示用户消息
        if user_text:
            self.加一句(f"\n【你】{user_text}\n", "user_msg")

        # 如果有图片，显示在聊天区
        img_path = self.发送图片路径
        if img_path:
            self.加图片到聊天(img_path)
            self.发送图片路径 = None
            self.img_preview_label.pack_forget()
            self.img_preview_label.configure(image="", text="")

        thinking_idx = self.chat_display.index(tk.END)
        self.加一句("\n【AI】\n", "thinking")
        self.chat_display.tag_config("thinking", foreground="#888888",
                                     font=("微软雅黑", 10, "italic"))

        # 构建消息体（DeepSeek 不支持图片多模态，有图片时只发文本）
        if has_image and img_path:
            # 只发文本，不加图片数据（API 不支持 image_url）
            text_to_send = user_text or "请介绍一下这张图片中的景点"
            request_messages = self.messages + [
                {"role": "user", "content": text_to_send}
            ]
        else:
            request_messages = self.messages + [
                {"role": "user", "content": user_text}
            ]

        def ai响应成功(reply):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(thinking_idx, tk.END)
            self.chat_display.config(state=tk.DISABLED)

            self.加一句(f"\n【AI】{reply}\n\n", "ai_msg")
            self.chat_display.tag_config("ai_msg", foreground="#333333",
                                         font=("微软雅黑", 10))
            # 只保存文本到历史（不存图片 base64，避免上下文膨胀）
            if user_text:
                self.messages.append({"role": "user", "content": user_text})
            else:
                self.messages.append({"role": "user", "content": "[用户发送了一张图片]"})
            self.send_btn.config(state=tk.NORMAL)
            self.img_btn.config(state=tk.NORMAL)

        def ai响应失败(err):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(thinking_idx, tk.END)
            self.chat_display.config(state=tk.DISABLED)

            err_msg = f"\n【系统】请求失败：{err}\n\n"
            self.加一句(err_msg, "err_msg")
            self.chat_display.tag_config("err_msg", foreground="#CC0000",
                                         font=("微软雅黑", 10))
            self.send_btn.config(state=tk.NORMAL)
            self.img_btn.config(state=tk.NORMAL)

        问问ai(request_messages, ai响应成功, ai响应失败)


def app():
    root = tk.Tk()
    app = 主窗口(root)
    root.mainloop()

if __name__ == "__main__":
    app()
