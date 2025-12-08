<div align="center">

<img src="assets/logo.png" width="300" />
<p align="center">使用小米 AI 眼镜，在 <strong>20 步</strong>内还原任何三阶魔方。</p>

</div>

## 项目简介

本项目通过小米 AI 眼镜识别魔方，并在 1 秒钟内给出最优解法（20 步以内），然后使用 3D 动画演示每一步转动，让解魔方变得前所未有的简单有趣。

## 演示视频

![Demo](assets/demo.gif)

## 核心功能

- **📷 智能识别**：自动调用小米 AI 眼镜拍照，利用 Yolo11 + OpenCV 识别魔方状态。
- **⚡️ 快速还原**：使用 Kociemba 两阶段求解法，在 1 秒内给出最优解法（20 步以内）。
- **🎲 3D 演示**：在网页上以逼真的 3D 动画形式，逐步演示如何转动魔方的每一个面。
- **🔊 语音引导**：支持通过语音实时交互，获得每一步的操作提示（小米 AI 眼镜没有屏幕）。

## 技术细节

![Yolo](assets/yolo.webp)

> [!IMPORTANT]
> 注意，以下操作基于 ADB 调试模式，但小米 AI 眼镜默认并未开启此功能，所以你可能无法复现本项目。

首先，我们通过 ADB 获取到小米 AI 眼镜上的画面和语音交互记录（[相关代码](src/chat/adb.py)）。

获取到画面后，我们先用目标检测模型（基于 [YOLO11m](https://docs.ultralytics.com/tasks/detect)）识别魔方位置（[相关代码](src/vision/predict.py)｜[模型下载](https://github.com/idootop/MigicCube/releases/tag/model)）。

然后使用 OpenCV 进行透视变换矫正画面，并识别出魔方每个面的色块颜色（[相关代码](src/vision/image.py)）。

接着使用 [Kociemba](https://github.com/hkociemba/RubiksCube-TwophaseSolver) 两阶段求解法，在 1 秒内给出 20 步以内的最优解法（[相关代码](src/cube/kociemba.py)｜[修剪表下载](https://github.com/idootop/MigicCube/releases/tag/kociemba)）。

最后将解法同步到网页端，并使用 [Roofig](https://github.com/larspetrus/Roofpig) 展示 3D 魔方动画即可（[相关代码](src/web/index.html)）。

## 更新历史

- [x] 支持操作符: U(u), D(d), F(f), B(b), L(l), R(r), M, E, S, x, y, z 和逆时针(')、重复操作(U2')等
- [x] 完成魔方初始化、操作符映射与状态观测接口
- [x] 网页端支持预览魔方操作序列结果，回放解法步骤
- [x] 实现完整的 CFOP 三阶魔方速解算法（基于 [PyCube-Solver](https://github.com/saiakarsh193/PyCube-Solver)）
- [x] 使用 Kociemba 方法求解魔方（压缩到 20 步以内）
- [x] 实现小米 AI 眼镜文字对话实时监听和拍照获取图像 POC
- [x] 实现 Yolo11 魔方识别模型相关数据收集、处理、训练、推理全流程
- [x] 实现从视觉（图片/摄像头）输入提取魔方状态，自动生成解法步骤
- [x] 优化交互流程（支持语音交互、拍照键和音量增减事件监听）
- [x] 支持实时预览魔方状态和上一步、下一步、重置操作
- [x] 实现 TTS 语音提示和语音交互流程

## License

MIT License © 2025-PRESENT [Del Wang](https://del.wang)
