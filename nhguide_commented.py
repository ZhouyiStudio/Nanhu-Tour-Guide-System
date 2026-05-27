#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# 文件名： nhguide_commented.py  (带注释的教学版)
# 说明：   嘉兴南湖导游系统（GUI 桌面版）
#          使用 Tkinter 构建图形界面，支持分类展示、图片浏览、
#          AI 问答、语音朗读等功能
# ============================================================
# UI Design By PyMe--我用 Python 创世界
# https://www.py-me.com/

# -------- 导入所需库 --------
import tkinter as tk            # Tkinter：Python 标准 GUI 库，用于创建窗口和控件
import json                     # JSON 处理：序列化和反序列化数据
import threading                # 多线程：避免网络请求阻塞界面
import os                       # 操作系统接口：路径操作、文件判断等
import base64                   # Base64 编码：图片转码用
import io                       # 内存文件操作：图片处理缓存
import sys                      # 系统接口：获取脚本路径、判断是否打包
from tkinter import scrolledtext, filedialog, messagebox  # Tkinter 增强组件
from PIL import Image, ImageTk  # Pillow 库：处理各种图片格式并转为 Tkinter 可用的 PhotoImage

# -------- 环境变量加载 --------
# 自动加载 .env 文件（支持 exe 同目录或当前目录）
try:
    from dotenv import load_dotenv   # 从 .env 文件加载环境变量
    # 先找 exe/脚本所在目录，再找当前工作目录
    基础路径 = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    load_dotenv(os.path.join(基础路径, '.env'))
    load_dotenv('.env')  # 也尝试工作目录
except ImportError:
    pass  # 如果没有安装 python-dotenv 库，跳过环境变量加载

# -------- DeepSeek AI 配置 --------
# 安全：API Key 从环境变量 DeepSeek_API密钥 读取
api密钥 = os.environ.get("DeepSeek_API密钥", "")
if not api密钥:
    print("⚠ 警告：环境变量 DeepSeek_API密钥 未设置，AI 问答功能将不可用。")
    print("  请创建 .env 文件并写入 DeepSeek_API密钥=你的key")
接口地址 = "https://api.deepseek.com/chat/completions"   # DeepSeek API 端点
模型名 = "deepseek-chat"                                 # 使用的 AI 模型名称

# -------- 分类内容数据 --------
# 各功能分类下展示的文本条目（景点导览、游览路线、红色历史等）
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

# -------- 图片路径与映射 --------
# PyInstaller 打包后资源路径处理
if getattr(sys, 'frozen', False):         # 检测是否在 PyInstaller 打包后的 exe 中运行
    基础路径 = sys._MEIPASS                # 打包后的临时解压路径
else:
    基础路径 = os.path.dirname(__file__)   # 脚本所在目录
图片路径 = os.path.join(基础路径, "assets", "images")  # 图片资源文件夹路径

# 每个景点名称对应的图片文件名列表
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

# 每个分类对应的图片文件名列表
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

# 每张图片对应的说明文字
分类图说 = {
    "景点导览": ["南湖红船", "烟雨楼", "壕股塔", "革命纪念馆", "小瀛洲",
                "揽秀园", "会景园", "端午祭坛"],
    "游览路线": ["南湖红船", "烟雨楼", "革命纪念馆"],
    "红色历史": ["南湖红船", "会景园入口"],
    "交通指南": ["会景园", "壕股塔远眺"],
    "门票信息": ["革命纪念馆", "壕股塔"],
}

# ============================================================
# 函数：问问ai —— 调用 DeepSeek API 进行智能对话
# 参数：
#   历史消息   - 对话历史列表（包含 system/user/assistant 消息）
#   ai响应成功 - 回调函数，AI 回复成功时调用
#   ai响应失败 - 回调函数，API 请求失败时调用
# 功能：在后台线程中发送 HTTP 请求，不阻塞界面
# ============================================================
def 问问ai(历史消息, ai响应成功, ai响应失败):
    """
    调用 DeepSeek API 进行 AI 对话
    使用后台线程发送请求，避免阻塞 GUI 界面
    """
    def 发送请求():
        """实际发送 HTTP 请求的函数（在子线程中执行）"""
        try:
            import urllib.request  # 导入 URL 请求库
            
            # 构造请求数据：JSON 格式的 API 参数
            请求数据 = json.dumps({               # 序列化为 JSON 字符串
                "model": 模型名,                  # 模型名称
                "messages": 历史消息,              # 对话历史
                "stream": False,                   # 不使用流式输出
                "temperature": 0.7,                # 生成温度（0-2，越高越随机）
                "max_tokens": 1024,                # 最大生成 token 数
            }).encode("utf-8")                     # 编码为 UTF-8 字节流
            
            # 构造 HTTP 请求对象
            请求对象 = urllib.request.Request(
                接口地址,                          # API 端点 URL
                data=请求数据,                     # POST 请求体
                headers={
                    "Content-Type": "application/json",    # 内容类型
                    "Authorization": f"Bearer {api密钥}",  # 认证头（Bearer Token）
                },
                method="POST",                     # HTTP 方法
            )
            
            # 发送请求并获取响应（超时30秒）
            with urllib.request.urlopen(请求对象, timeout=30) as 响应对象:
                响应体 = json.loads(响应对象.read().decode("utf-8"))  # 解析 JSON 响应
                回复 = 响应体["choices"][0]["message"]["content"]   # 提取 AI 回复文本
                ai响应成功(回复)                   # 调用成功回调函数
        
        except Exception as e:
            ai响应失败(str(e))                    # 调用失败回调函数，传入错误信息
    
    # 在新线程中执行请求（daemon=True 表示主线程退出时自动结束）
    threading.Thread(target=发送请求, daemon=True).start()


# ============================================================
# 函数：图片转base64
# 将图片文件转换为 base64 编码的 data URI
# 参数：
#   文件名   - 图片文件路径
#   最大尺寸 - 长边最大像素（默认2048），超过则等比例缩放
# ============================================================
def 图片转base64(文件名, 最大尺寸=2048):
    """
    读取图片并转为 base64 data URI 格式
    超长边自动缩放到最大尺寸
    返回格式：data:image/jpeg;base64,XXXXXXXXX...
    失败返回 None
    """
    try:
        图片 = Image.open(文件名)                 # 打开图片文件
        # 转 RGB（兼容 PNG 透明通道）
        if 图片.mode in ("RGBA", "P"):            # 如果包含透明通道或调色板模式
            图片 = 图片.convert("RGB")            # 转换为 RGB 模式
        宽, 高 = 图片.size                        # 获取原始宽高
        if max(宽, 高) > 最大尺寸:                 # 如果长边超过最大限制
            缩放比例 = 最大尺寸 / max(宽, 高)      # 计算缩放比例
            图片 = 图片.resize((int(宽 * 缩放比例), int(高 * 缩放比例)), Image.LANCZOS)  # 等比缩放
        缓存 = io.BytesIO()                       # 创建内存字节缓存
        图片.save(缓存, format="JPEG", quality=85)  # 保存为 JPEG 格式到内存
        编码文本 = base64.b64encode(缓存.getvalue()).decode("utf-8")  # Base64 编码
        return f"data:image/jpeg;base64,{编码文本}"  # 返回 data URI
    except Exception:
        return None                                # 任何错误都返回 None


# ============================================================
# 类：主窗口 (GUI 核心类)
# 管理整个图形界面的布局和交互
# 包含左侧导航栏、中央内容区（文本 + 图片）、聊天面板
# ============================================================
class 主窗口:
    """南湖导游系统的主窗口类"""

    def __init__(self, 根窗口):
        """
        初始化主窗口
        参数：
            根窗口 - Tkinter 根窗口对象 (tk.Tk())
        功能：设置窗口属性、创建导航栏、文本区、图片面板、聊天面板
        """
        self.根窗口 = 根窗口                      # 保存根窗口引用
        self._朗读引擎 = None                     # 语音朗读引擎（延迟初始化）
        self._朗读中 = False                      # 标记是否正在朗读
        self._tts内联按钮 = []                    # 每个AI回复后的朗读按钮引用列表

        # ======== 窗口基本配置 ========
        根窗口.title("嘉兴南湖导游系统")           # 设置窗口标题
        根窗口.geometry("1024x620")               # 设置窗口默认大小（宽x高）
        根窗口.resizable(True, True)              # 允许用户调整窗口大小
        根窗口.minsize(860, 520)                  # 设置窗口最小尺寸

        # 主题颜色常量
        主题红 = "#C41E24"                        # 主色调：南湖红
        self.LIGHT = "#FFF5F0"                    # 浅色背景

        # ======== 创建主体布局容器 ========
        主体 = tk.Frame(根窗口)                   # 主框架容器
        主体.pack(fill=tk.BOTH, expand=True)      # 填充整个窗口
        
        # ======== 左侧导航栏 ========
        导航栏 = tk.Frame(主体, width=160, bg=主题红)  # 左侧导航框（宽160px）
        导航栏.pack(side=tk.LEFT, fill=tk.Y)      # 靠左对齐，纵向填满
        导航栏.pack_propagate(False)              # 固定宽度（子控件不改变父容器宽度）
        
        # 导航栏标题
        tk.Label(导航栏, text="南湖导游", font=("微软雅黑", 14, "bold"),
                 fg="white", bg=主题红, pady=12).pack(fill=tk.X)  # 白色加粗标题
        
        # 动态创建导航按钮，每个分类对应一个按钮
        for 分类键 in 分类内容:                   # 遍历所有分类
            按钮 = tk.Button(导航栏, text=分类键, font=("微软雅黑", 10),
                            fg="white", bg=主题红, activebackground="#8B0000",
                            activeforeground="white", relief=tk.FLAT,
                            bd=0, pady=6, cursor="hand2",
                            command=lambda n=分类键: self.展示(n))  # 点击调用展示方法
            按钮.pack(fill=tk.X)                  # 横向填满导航栏
        
        # 分隔线
        tk.Frame(导航栏, height=1, bg="#FFD4D4").pack(fill=tk.X, pady=4)
        
        # AI 问答按钮（特殊样式，更加突出）
        tk.Button(导航栏, text="AI问答", font=("微软雅黑", 10, "bold"),
                  fg="white", bg="#D4380D", activebackground="#8B2500",
                  activeforeground="white", relief=tk.RAISED,
                  bd=1, pady=6, cursor="hand2",
                  command=self.聊天).pack(fill=tk.X, padx=2)

        # ======== 内容区域（左侧文本 + 右侧图片） ========
        self.文本框架 = tk.Frame(主体)             # 文本+图片的容器框架
        
        # 左侧文本区容器
        文本容器 = tk.Frame(self.文本框架)
        文本容器.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # 靠左，填满剩余空间
        
        # 文本区顶部工具栏：标题 + 朗读按钮
        文本工具栏 = tk.Frame(文本容器, bg="#FFF5F0", height=30)  # 工具栏容器
        文本工具栏.pack(fill=tk.X)                # 横向填满
        文本工具栏.pack_propagate(False)           # 固定高度
        
        # 朗读当前介绍按钮
        self.文本朗读按钮 = tk.Button(文本工具栏, text="🔊 朗读介绍", font=("微软雅黑", 10),
                                      bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                      bd=0, padx=8, cursor="hand2",
                                      command=self.朗读当前介绍)  # 点击后朗读文本区内容
        self.文本朗读按钮.pack(side=tk.RIGHT, padx=(6, 2), pady=3)
        
        # 停止朗读按钮
        self.文本停止按钮 = tk.Button(文本工具栏, text="⏹ 停止", font=("微软雅黑", 10),
                                            bg="#FFD4D4", fg="#C41E24", relief=tk.FLAT,
                                            bd=0, padx=8, cursor="hand2",
                                            command=self.停止朗读)  # 点击停止朗读
        self.文本停止按钮.pack(side=tk.RIGHT, padx=2, pady=3)
        
        # 文本展示区域（带滚动条）
        self.文本区 = scrolledtext.ScrolledText(文本容器, font=("微软雅黑", 11),
                                              bg=self.LIGHT, fg="#333333",
                                              wrap=tk.WORD, bd=0, padx=15, pady=15)
                                              # wrap=tk.WORD 按单词换行
        self.文本区.pack(fill=tk.BOTH, expand=True)
        
        # ======== 右侧图片面板 ========
        self.图片面板 = tk.Frame(self.文本框架, width=220, bg="#F5F0EB")  # 右侧面板（宽220px）
        self.图片面板.pack(side=tk.RIGHT, fill=tk.Y)  # 靠右，纵向填满
        self.图片面板.pack_propagate(False)           # 固定宽度
        
        # 图片面板标题
        self.图片标题 = tk.Label(self.图片面板, text="景点图片",
                                        font=("微软雅黑", 10, "bold"),
                                        bg="#8B4513", fg="white", pady=4)
        self.图片标题.pack(fill=tk.X)                # 横向填满
        
        # 图片展示画布（可滚动）
        self.图片画布 = tk.Canvas(self.图片面板, bg="#F5F0EB",
                                    highlightthickness=0, width=210)  # 画布宽度210px
        self.图片滚动条 = tk.Scrollbar(self.图片面板, orient=tk.VERTICAL,
                                          command=self.图片画布.yview)  # 垂直滚动条
        self.图片可滚动区 = tk.Frame(self.图片画布, bg="#F5F0EB")     # 画布内的滚动区域
        
        # 当滚动区尺寸变化时更新画布的滚动范围
        self.图片可滚动区.bind("<Configure>",
                                 lambda e: self.图片画布.configure(scrollregion=self.图片画布.bbox("all")))
        self.图片画布.create_window((0, 0), window=self.图片可滚动区, anchor="nw", width=205)  # 将滚动区嵌入画布
        self.图片画布.configure(yscrollcommand=self.图片滚动条.set)  # 画布滚动时联动滚动条
        
        self.图片画布.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.图片滚动条.pack(side=tk.RIGHT, fill=tk.Y)

        # ======== 聊天面板 ========
        self.聊天面板 = tk.Frame(主体)               # 聊天面板容器
        
        # 聊天显示区域（只读，带滚动条）
        self.聊天显示 = scrolledtext.ScrolledText(
            self.聊天面板, font=("微软雅黑", 11),
            bg="white", fg="#333333",
            wrap=tk.WORD, bd=0, padx=12, pady=12,
        )
        self.聊天显示.pack(fill=tk.BOTH, expand=True)
        self.聊天显示.config(state=tk.DISABLED)      # 设为只读，禁止用户直接编辑
        
        # 聊天输入区域（输入框 + 按钮行）
        输入框架 = tk.Frame(self.聊天面板, bg="#F0F0F0", height=50)  # 底部输入栏
        输入框架.pack(fill=tk.X, side=tk.BOTTOM)     # 固定在底部
        输入框架.pack_propagate(False)               # 固定高度
        
        # 所选图片预览标签
        self.图片预览 = tk.Label(输入框架, bg="#F0F0F0",
                                          font=("微软雅黑", 8), fg="#666666",
                                          padx=4, pady=2)
        
        # 文本输入框
        self.输入框 = tk.Entry(输入框架, font=("微软雅黑", 11),
                              bd=1, relief=tk.SOLID)  # 单行输入框
        self.输入框.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 4), pady=8)
        self.输入框.bind("<Return>", lambda e: self.用户发送())  # 按回车键发送
        
        # 发送按钮
        self.发送按钮 = tk.Button(输入框架, text="发送", font=("微软雅黑", 10),
                                  bg="#C41E24", fg="white", relief=tk.FLAT,
                                  bd=0, padx=12, pady=2, cursor="hand2",
                                  command=self.用户发送)  # 点击发送消息
        self.发送按钮.pack(side=tk.RIGHT, padx=4, pady=8)
        
        # 朗读最后 AI 回复按钮
        self.聊天朗读按钮 = tk.Button(输入框架, text="🔊 朗读", font=("微软雅黑", 10),
                                         bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                                         bd=0, padx=8, pady=2, cursor="hand2",
                                         command=self.朗读最后回复)
        self.聊天朗读按钮.pack(side=tk.RIGHT, padx=(2, 0), pady=8)
        
        # 停止朗读按钮
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

        # ======== AI 对话历史（系统提示词） ========
        self.历史消息 = [
            {
                "role": "system",                  # 系统消息角色
                "content": (                       # 系统提示内容
                    "你是嘉兴南湖景区的智能导游助手。你熟悉南湖的所有景点、历史、交通、美食等信息。"
                    "请用中文友好地回答游客的问题，回答要简洁准确、有礼貌。"
                    "如果不知道答案，请如实说不知道，不要编造。"
                ),
            }
        ]

        # ======== 状态变量 ========
        # 缓存图片引用（防止被 GC 回收导致图片不显示）
        self.图片缓存 = []

        # 当前选择的发送图片路径
        self.发送图片路径 = None

    # -------- 方法：换掉 --------
    def 换掉(self, 框架):
        """
        切换显示的面板
        隐藏所有面板，然后显示指定的面板
        参数：
            框架 - 要显示的框架对象（文本框架或聊天面板）
        """
        for f in (self.文本框架, self.聊天面板):   # 遍历两个面板
            f.pack_forget()                        # 隐藏所有面板
        框架.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)  # 显示指定面板

    # -------- 方法：加载图片 --------
    def 加载图片(self, 文件名, 宽度=190, 高度=140):
        """
        加载并缩放图片，返回 Tkinter PhotoImage 对象
        参数：
            文件名 - 图片文件名（相对于图片路径）
            宽度   - 缩放宽度的目标值（默认190）
            高度   - 缩放高度的目标值（默认140）
        返回：PhotoImage 对象，加载失败返回 None
        """
        路径 = os.path.join(图片路径, 文件名)      # 拼接完整路径
        if not os.path.exists(路径):               # 如果文件不存在
            return None
        try:
            图片 = Image.open(路径)                # 用 Pillow 打开图片
            宽, 高 = 图片.size                     # 获取原始尺寸
            缩放比例 = min(宽度 / 宽, 高度 / 高)   # 计算缩放比例（保持宽高比）
            新宽, 新高 = int(宽 * 缩放比例), int(高 * 缩放比例)  # 计算缩放后尺寸
            图片 = 图片.resize((新宽, 新高), Image.LANCZOS)  # 高质量缩放
            return ImageTk.PhotoImage(图片)         # 转为 Tkinter 可用格式
        except Exception:
            return None

    # -------- 方法：加载大图 --------
    def 加载大图(self, 文件名, 最大尺寸=800):
        """
        加载完整分辨率图片（用于弹出大图窗口）
        图片缩放至最大尺寸范围内
        参数：
            文件名   - 图片文件名
            最大尺寸 - 长边最大像素（默认800）
        返回：PhotoImage 对象，失败返回 None
        """
        路径 = os.path.join(图片路径, 文件名)      # 拼接完整路径
        if not os.path.exists(路径):
            # 如果找不到 thumb_ 前缀的文件，尝试原图
            原文件名 = 文件名.replace("thumb_", "")  # 去掉缩略图前缀
            路径 = os.path.join(图片路径, 原文件名)
        if not os.path.exists(路径):
            return None
        try:
            图片 = Image.open(路径)                # 打开图片
            宽, 高 = 图片.size                     # 获取原始尺寸
            缩放比例 = min(最大尺寸 / 宽, 最大尺寸 / 高, 1.0)  # 计算缩放比（不超过原始大小）
            if 缩放比例 < 1.0:                     # 如果原始图片超过最大尺寸才缩放
                图片 = 图片.resize((int(宽 * 缩放比例), int(高 * 缩放比例)), Image.LANCZOS)
            return ImageTk.PhotoImage(图片)         # 转为 Tkinter 格式
        except Exception:
            return None

    # -------- 方法：清空图片面板 --------
    def 清空图片面板(self):
        """移除图片面板中所有子组件，清空图片缓存"""
        for 组件 in self.图片可滚动区.winfo_children():  # 遍历所有子组件
            组件.destroy()                              # 销毁子组件
        self.图片缓存.clear()                           # 清空缓存（释放内存）

    # -------- 方法：打开大图 --------
    def 打开大图(self, 文件名, 图说=""):
        """
        弹出新窗口显示大图
        参数：
            文件名 - 图片文件名
            图说   - 图片说明文字（可选）
        """
        照片 = self.加载大图(文件名)                  # 加载大图
        if 照片 is None:                              # 如果加载失败
            messagebox.showinfo("提示", "暂无高清图片")  # 显示提示信息
            return

        新窗口 = tk.Toplevel(self.根窗口)             # 创建新顶层窗口
        新窗口.title(f"南湖景点 — {图说}" if 图说 else "南湖景点")  # 设置窗口标题
        新窗口.configure(bg="#333333")                # 深色背景（突出图片）

        # 窗口大小跟随图片
        图宽 = 照片.width()                           # 图片宽度
        图高 = 照片.height()                          # 图片高度
        新窗口.geometry(f"{图宽 + 40}x{图高 + 80}")  # 窗口比图片稍大（边距）

        # 图片标签
        标签 = tk.Label(新窗口, image=照片, bg="#333333", cursor="hand2")
        标签.image = 照片                             # 保存引用，防止 GC 回收
        标签.pack(expand=True, padx=20, pady=(20, 5))

        # 标题（如果有说明文字）
        if 图说:
            tk.Label(新窗口, text=图说, font=("微软雅黑", 10),
                     bg="#333333", fg="white").pack(pady=(0, 10))

        # 点击任意位置关闭窗口
        新窗口.bind("<Button-1>", lambda e: 新窗口.destroy())
        标签.bind("<Button-1>", lambda e: 新窗口.destroy())

        # 按 ESC 键关闭窗口
        新窗口.bind("<Escape>", lambda e: 新窗口.destroy())
        新窗口.focus_set()                            # 让新窗口获取焦点

    # -------- 方法：显示图片组 --------
    def 显示图片组(self, 文件名列表, 图说列表=None):
        """
        在图片面板中显示一组图片（可点击放大）
        参数：
            文件名列表 - 图片文件名列表
            图说列表   - 对应的说明文字列表（可选）
        """
        self.清空图片面板()                            # 先清空旧图片
        for 序号, 文件名 in enumerate(文件名列表):     # 遍历文件名列表
            照片 = self.加载图片(文件名)               # 加载缩略图
            if 照片 is None:                           # 如果文件不存在则跳过
                continue
            self.图片缓存.append(照片)                 # 保存引用防止 GC

            容器 = tk.Frame(self.图片可滚动区, bg="#F5F0EB", padx=8, pady=4)
            容器.pack(fill=tk.X)                       # 每个图片放一个横向容器

            图说 = 图说列表[序号] if 图说列表 and 序号 < len(图说列表) else ""

            标签 = tk.Label(容器, image=照片, bg="#F5F0EB",
                           cursor="hand2", relief=tk.FLAT)
            标签.image = 照片                          # 保存引用
            标签.pack(pady=(4, 0))

            # 绑定点击放大 — 传入文件名和图说
            标签.bind("<Button-1>",
                     lambda e, fn=文件名, c=图说: self.打开大图(fn, c))

            if 图说:
                tk.Label(容器, text=图说, font=("微软雅黑", 8),
                         bg="#F5F0EB", fg="#666666", wraplength=190).pack()

            if 序号 < len(文件名列表) - 1:             # 图片之间加分隔线
                tk.Frame(容器, height=1, bg="#DDDDDD").pack(fill=tk.X, pady=4)

    # -------- 方法：展示 --------
    def 展示(self, 分类名):
        """
        在文本区域展示分类内容
        参数：
            分类名 - 要展示的分类键名
        """
        self.换掉(self.文本框架)                      # 切换到文本框架
        self.文本区.config(state=tk.NORMAL)            # 设置为可编辑（以便插入内容）
        self.文本区.delete(1.0, tk.END)               # 清空旧内容

        # 插入分类标题
        self.文本区.insert(tk.END, f"🏛 {分类名}\n\n", "title")
        self.文本区.tag_config("title", font=("微软雅黑", 16, "bold"),
                             foreground="#C41E24", spacing3=10)

        # 插入分类内容（每条记录单独一行）
        for 条目 in 分类内容[分类名]:
            self.文本区.insert(tk.END, f"  • {条目}\n\n", "content")
        self.文本区.tag_config("content", font=("微软雅黑", 10),
                             foreground="#333333", spacing1=4, spacing3=4)

        self.文本区.config(state=tk.DISABLED)          # 恢复只读
        self.展示分类图片(分类名)                      # 同步显示对应图片

    # -------- 方法：展示分类图片 --------
    def 展示分类图片(self, 分类名):
        """
        根据分类显示对应的图片
        参数：
            分类名 - 要显示的分类键名
        """
        if 分类名 in 分类图片:                         # 如果该分类有对应图片
            self.显示图片组(分类图片[分类名], 分类图说.get(分类名))  # 显示图片组

    # -------- 方法：显示景点图片 --------
    def 显示景点图片(self, 景点名):
        """
        根据景点名称显示对应图片
        参数：
            景点名 - 景点名称（需与景点图片字典中的键匹配）
        """
        if 景点名 in 景点图片:                         # 如果该景点有对应图片
            self.显示图片组(景点图片[景点名])           # 显示图片组

    # -------- 方法：聊天 --------
    def 聊天(self):
        """切换到聊天面板"""
        self.换掉(self.聊天面板)                      # 切换到聊天面板

    # -------- 方法：朗读_通用 --------
    def 朗读_通用(self, 文本, 完成回调=None):
        """
        使用 Windows SAPI5 语音引擎朗读文本（异步）
        参数：
            文本     - 要朗读的文字内容
            完成回调 - 朗读完成后调用的函数（可选）
        """
        try:
            import pyttsx3                            # 导入文本转语音库
            self._朗读引擎 = pyttsx3.init(driverName='sapi5')  # 初始化 SAPI5 引擎
            self._朗读引擎.setProperty('rate', 200)    # 设置语速（200词/分钟）
            self._朗读引擎.setProperty('volume', 1.0)  # 设置音量（最大）

            # 选择中文语音
            所有语音 = self._朗读引擎.getProperty('voices')  # 获取所有可用语音
            for 语音 in 所有语音:                     # 遍历查找中文语音
                if 'Chinese' in 语音.name or '中文' in 语音.name:
                    self._朗读引擎.setProperty('voice', 语音.id)  # 设置为中文语音
                    break

            self._朗读中 = True                       # 标记正在朗读

            def 朗读():
                """在子线程中执行朗读（不阻塞界面）"""
                self._朗读引擎.say(文本)              # 加入朗读队列
                self._朗读引擎.runAndWait()           # 等待朗读完成
                self._朗读中 = False                  # 标记朗读结束
                if 完成回调:
                    完成回调()                       # 执行完成回调

            threading.Thread(target=朗读, daemon=True).start()  # 启动朗读线程

        except Exception as e:
            self._朗读中 = False
            messagebox.showwarning("语音提示", f"语音朗读初始化失败：{e}")

    # -------- 方法：停止朗读 --------
    def 停止朗读(self):
        """停止当前正在进行的语音朗读"""
        try:
            if self._朗读引擎 and self._朗读中:       # 如果引擎存在且正在朗读
                self._朗读引擎.stop()                 # 停止朗读
            self._朗读中 = False                      # 更新状态
            self._重置内联按钮()                      # 恢复所有内联按钮
        except Exception:
            pass                                      # 忽略异常

    # -------- 方法：_重置内联按钮 --------
    def _重置内联按钮(self):
        """将所有内联朗读/停止按钮重置为「朗读」状态"""
        for 按钮 in self._tts内联按钮:                # 遍历所有内联按钮
            try:
                按钮.config(text="🔊 朗读", bg="#E8E8E8", fg="#333333")  # 恢复为朗读按钮样式
            except Exception:
                pass

    # -------- 方法：_添加内联朗读按钮 --------
    def _添加内联朗读按钮(self, 回复文本):
        """
        在 AI 回复内容后嵌入一个朗读/停止切换按钮
        参数：
            回复文本 - AI 回复的文字内容（朗读时使用）
        """
        self.聊天显示.config(state=tk.NORMAL)        # 临时启用编辑

        按钮框架 = tk.Frame(self.聊天显示, bg=self.LIGHT)
        朗读按钮 = tk.Button(按钮框架, text="🔊 朗读", font=("微软雅黑", 9),
                            bg="#E8E8E8", fg="#333333", relief=tk.FLAT,
                            bd=0, padx=6, pady=1, cursor="hand2",
                            activebackground="#D0D0D0")
        朗读按钮.pack(side=tk.LEFT, padx=(4, 0))

        # 记录按钮引用（以便后续重置）
        self._tts内联按钮.append(朗读按钮)

        def 切换朗读():
            """切换朗读/停止状态的内联函数"""
            if 朗读按钮.cget("text") == "🔊 朗读":   # 当前是「朗读」状态
                # 切换到停止状态 → 开始朗读
                朗读按钮.config(text="⏹ 停止", bg="#FFD4D4", fg="#C41E24")
                
                # 朗读完成后的回调：恢复按钮状态
                def 朗读完成():
                    try:
                        朗读按钮.config(text="🔊 朗读", bg="#E8E8E8", fg="#333333")
                    except Exception:
                        pass
                self.朗读_通用(回复文本, 朗读完成)    # 开始朗读
            else:                                      # 当前是「停止」状态
                # 单击停止 → 停止朗读
                self.停止朗读()                        # _重置内联按钮 会自动恢复所有按钮

        朗读按钮.config(command=切换朗读)              # 绑定点击事件

        # 在聊天显示中嵌入按钮
        self.聊天显示.window_create(tk.END, window=按钮框架)
        self.聊天显示.insert(tk.END, "\n")
        self.聊天显示.see(tk.END)                      # 滚动到底部
        self.聊天显示.config(state=tk.DISABLED)        # 恢复只读

    # -------- 方法：朗读当前介绍 --------
    def 朗读当前介绍(self):
        """朗读左侧文本区中的当前景点介绍内容"""
        全部文本 = self.文本区.get("1.0", tk.END).strip()  # 获取文本区全部内容
        if not 全部文本:
            messagebox.showinfo("提示", "当前没有景点介绍内容")
            return
        self.朗读_通用(全部文本)                       # 开始朗读

    # -------- 方法：朗读最后回复 --------
    def 朗读最后回复(self):
        """朗读聊天区中最后一条 AI 回复内容"""
        # 从聊天显示控件中提取最后一段 AI 回复
        全部文本 = self.聊天显示.get("1.0", tk.END).strip()
        if not 全部文本:
            messagebox.showinfo("提示", "没有可朗读的内容")
            return

        # 查找最后一段 【AI】 标记之后的内容
        位置 = 全部文本.rfind("【AI】")                # 从后往前找
        if 位置 != -1:
            回复文本 = 全部文本[位置 + 4:].strip()    # 提取【AI】之后的内容
            if 回复文本:
                self.朗读_通用(回复文本)
                return

        # 找不到 【AI】 时，朗读所有聊天内容（去掉标记符号）
        纯文本 = 全部文本.replace("【你】", "").replace("【AI】", "").replace("【系统】", "")
        if 纯文本.strip():
            self.朗读_通用(纯文本)
        else:
            messagebox.showinfo("提示", "暂无 AI 回复可朗读")

    # -------- 方法：选择图片 --------
    def 选择图片(self):
        """
        打开文件选择对话框选择图片
        选中后在输入框左侧显示缩略图预览
        """
        路径 = filedialog.askopenfilename(            # 打开文件选择器
            title="选择图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp")],
        )
        if not 路径:                                   # 如果用户取消了选择
            return
        self.发送图片路径 = 路径                       # 保存选中的路径

        # 显示预览缩略图
        try:
            图片 = Image.open(路径)
            图片.thumbnail((40, 40))                   # 缩放到40x40
            照片 = ImageTk.PhotoImage(图片)
            self.图片预览.configure(image=照片, text="")
            self.图片预览.image = 照片
            self.图片预览.pack(side=tk.LEFT, padx=(8, 0), pady=4)
        except Exception:
            # 如果图片加载失败，显示文本占位
            self.图片预览.configure(text="[图片]", image="")
            self.图片预览.pack(side=tk.LEFT, padx=(8, 0), pady=4)

    # -------- 方法：加一句 --------
    def 加一句(self, 文本, 标签):
        """
        在聊天显示区插入一条消息
        参数：
            文本 - 消息内容
            标签 - 文本样式标签（如 "user_msg"、"ai_msg" 等）
        """
        self.聊天显示.config(state=tk.NORMAL)          # 临时启用编辑
        self.聊天显示.insert(tk.END, 文本, 标签)      # 插入文本并应用样式
        self.聊天显示.see(tk.END)                      # 滚动到底部
        self.聊天显示.config(state=tk.DISABLED)        # 恢复只读

    # -------- 方法：加图片到聊天 --------
    def 加图片到聊天(self, 图片路径):
        """
        在聊天区域插入图片预览
        参数：
            图片路径 - 图片文件的完整路径
        """
        try:
            图片 = Image.open(图片路径)
            图片.thumbnail((200, 150))                 # 缩放到聊天区合适大小
            照片 = ImageTk.PhotoImage(图片)
            self.图片缓存.append(照片)                 # 保持引用防止 GC
            self.聊天显示.config(state=tk.NORMAL)
            self.聊天显示.image_create(tk.END, image=照片)  # 嵌入图片
            self.聊天显示.insert(tk.END, "\n")
            self.聊天显示.see(tk.END)
            self.聊天显示.config(state=tk.DISABLED)
        except Exception:
            pass                                       # 加载失败则静默跳过

    # -------- 方法：用户发送 --------
    def 用户发送(self):
        """
        处理用户发送消息
        获取输入框内容，显示用户消息和 AI 思考标记，
        调用 AI API，处理回复显示和朗读按钮嵌入
        """
        用户文本 = self.输入框.get().strip()           # 获取输入框文本
        有图片 = self.发送图片路径 is not None          # 检查是否选择了图片

        if not 用户文本 and not 有图片:                # 没有文本也没有图片则忽略
            return

        self.输入框.delete(0, tk.END)                  # 清空输入框
        self.发送按钮.config(state=tk.DISABLED)         # 禁用发送按钮（防止重复发送）
        self.图片按钮.config(state=tk.DISABLED)         # 禁用图片选择按钮

        # 在聊天区显示用户消息
        if 用户文本:
            self.加一句(f"\n【你】{用户文本}\n", "user_msg")

        # 如果有图片，显示在聊天区
        图片路径 = self.发送图片路径
        if 图片路径:
            self.加图片到聊天(图片路径)                # 插入图片预览
            self.发送图片路径 = None                   # 清除已发送的图片路径
            self.图片预览.pack_forget()                # 移除预览
            self.图片预览.configure(image="", text="")

        # 记录 AI 思考标记的位置（以便后续替换）
        思考位置 = self.聊天显示.index(tk.END)
        self.加一句("\n【AI】\n", "thinking")           # 显示 "AI 思考中..."
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

        # -------- 内部函数：AI 响应成功回调 --------
        def ai响应成功(回复):
            """AI 返回回复时的回调函数"""
            self.聊天显示.config(state=tk.NORMAL)
            self.聊天显示.delete(思考位置, tk.END)     # 删除 "思考中..." 标记
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
            self.发送按钮.config(state=tk.NORMAL)       # 恢复发送按钮
            self.图片按钮.config(state=tk.NORMAL)        # 恢复图片选择按钮

        # -------- 内部函数：AI 响应失败回调 --------
        def ai响应失败(错误):
            """AI 请求失败时的回调函数"""
            self.聊天显示.config(state=tk.NORMAL)
            self.聊天显示.delete(思考位置, tk.END)     # 删除 "思考中..." 标记
            self.聊天显示.config(state=tk.DISABLED)

            错误消息 = f"\n【系统】请求失败：{错误}\n\n"
            self.加一句(错误消息, "err_msg")
            self.聊天显示.tag_config("err_msg", foreground="#CC0000",
                                         font=("微软雅黑", 10))
            self.发送按钮.config(state=tk.NORMAL)       # 恢复发送按钮
            self.图片按钮.config(state=tk.NORMAL)        # 恢复图片选择按钮

        # 启动 AI 请求（在后台线程中执行）
        问问ai(请求消息, ai响应成功, ai响应失败)


# ============================================================
# 函数：启动
# 创建根窗口和主窗口实例，进入 Tkinter 主事件循环
# ============================================================
def 启动():
    """创建并启动 GUI 程序"""
    根窗口 = tk.Tk()                                  # 创建 Tkinter 根窗口
    app = 主窗口(根窗口)                               # 创建主窗口实例（构建整个界面）
    根窗口.mainloop()                                 # 进入主事件循环（阻塞，直到窗口关闭）


# -------- 程序入口 --------
if __name__ == "__main__":
    """
    脚本入口点
    当该脚本被直接运行时（而不是作为模块导入），启动程序
    """
    启动()
