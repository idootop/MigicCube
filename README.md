# RubiksCube

使用小米 AI 眼镜，实现 AI 解魔方。

![Yolo](assets/yolo.webp)

# TODO

- [x] 支持操作符: U(u), D(d), F(f), B(b), L(l), R(r), M, E, S, x, y, z 和逆时针(')、重复操作(U2')等
- [x] 完成魔方初始化、操作符映射与状态观测接口
- [x] 网页端支持预览魔方操作序列结果，回放解法步骤
- [x] 实现完整的 CFOP 三阶魔方速解算法（基于 [PyCube-Solver](https://github.com/saiakarsh193/PyCube-Solver)）
- [x] 实现小米 AI 眼镜对话流程监听和拍照图像获取 poc
- [x] 实现 yolo-v11 魔方识别模型相关数据收集、处理、训练、推理全流程
- [ ] 实现从视觉（图片/摄像头）输入提取魔方状态，自动生成解法步骤
