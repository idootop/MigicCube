# RubiksCube

三阶魔方速解（CFOP）

![PLL](assets/cfop.jpg)

# TODO

- [x] 支持操作符: U(u), D(d), F(f), B(b), L(l), R(r), M, E, S, x, y, z 和逆时针(')、重复操作(U2')等
- [x] 完成魔方初始化、操作符映射与状态观测接口
- [x] 网页端支持预览魔方操作序列结果，回放解法步骤
- [x] 实现完整的 CFOP 三阶魔方速解算法（基于 [PyCube-Solver](https://github.com/saiakarsh193/PyCube-Solver)）
- [ ] 实现从视觉（图片/摄像头）输入提取魔方状态，自动生成解法步骤

# Motivation

借助小米 AI 眼镜等终端的摄像头画面，实现 AI 魔方速解。
