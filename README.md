# 嘉兴南湖导游系统 🏛

基于 Python Tkinter 的南湖景区智能导游桌面应用，支持景点导览、AI 问答、语音朗读、图片查看等功能。

## 功能

- **景点导览** — 景点介绍、游览路线、红色历史、交通指南、门票信息
- **AI 问答** — 接入 DeepSeek Chat 大模型，智能回答游客问题
- **语音朗读** — Windows TTS 中文朗读，支持停止
- **图片查看** — 景点图片缩略图展示，点击放大查看
- **图片问答** — 发送图片给 AI，识别景点或获取相关信息

## 运行

```bash
pip install pillow pyttsx3
python nhguide.py
```

## 截图

![主界面](assets/images/thumb_yanyulou.jpg)

## 技术栈

- Python 3 + Tkinter
- DeepSeek API
- Pillow（图片处理）
- pyttsx3（语音朗读）

## 数据来源

南湖景区公开旅游信息。
