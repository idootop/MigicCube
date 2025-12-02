import os

import cv2
import numpy as np

from cube.typing import Color
from vision.predict import YOLOv11Predictor


def find_cube_contour(image: np.ndarray):
    """
    定位魔方轮廓

    Args:
        image: 图像数组(numpy.ndarray)或图像路径(str)

    Returns:
        魔方轮廓的4个角点坐标，格式为 numpy 数组 shape=(4, 2)
        如果未检测到魔方，返回 None
    """
    detections = YOLOv11Predictor.predict(image)
    for detection in detections:
        if detection["class_name"] == "cube":
            # 将边界框 [x1, y1, x2, y2] 转换为4个角点的轮廓
            bbox = detection["bbox"]
            x1, y1, x2, y2 = bbox
            # 返回4个角点：左上、右上、右下、左下
            contour = np.array(
                [
                    [x1, y1],  # 左上
                    [x2, y1],  # 右上
                    [x2, y2],  # 右下
                    [x1, y2],  # 左下
                ],
                dtype=np.float32,
            )
            return contour
    return None


def perspective_correct(image: np.ndarray, contour):
    """透视矫正"""
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # 计算矩形的四个点
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # 左上角
    rect[2] = pts[np.argmax(s)]  # 右下角

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # 右上角
    rect[3] = pts[np.argmax(diff)]  # 左下角

    # 计算目标宽度和高度
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # 目标点
    dst = np.array(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
        dtype="float32",
    )

    # 计算透视变换矩阵并应用
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def get_cube_colors(image: np.ndarray):
    """
    获取魔方各色块颜色

    颜色识别基于HSV颜色空间：
    - 白色：低饱和度(S<=50)，高明度(V>=150)
    - 黄色：H在20-30之间，高饱和度
    - 橙色：H在5-20之间，高饱和度
    - 红色：H在0-5或170-180之间，高饱和度
    - 绿色：H在40-80之间
    - 蓝色：H在90-130之间
    """
    # 转换到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 分割成9个色块
    height, width = hsv.shape[:2]
    block_size = height // 3
    colors = []

    for row in range(3):
        for col in range(3):
            x, y = col * block_size, row * block_size
            roi = hsv[y : y + block_size, x : x + block_size]

            # 计算ROI的HSV中值
            hsv_median = cv2.medianBlur(roi, 5)
            h, s, v = cv2.split(hsv_median)
            h_med, s_med, v_med = (
                int(np.median(h)),
                int(np.median(s)),
                int(np.median(v)),
            )

            # 匹配颜色（按优先级顺序）
            matched_color = "X"

            # 首先检查白色（低饱和度，高明度）- 优先级最高
            if s_med <= 50 and v_med >= 150:
                matched_color = "W"
            # 然后检查其他颜色（需要足够的饱和度）
            elif s_med >= 50 and v_med >= 50:
                # 检查黄色（H在20-30之间）
                if 20 <= h_med <= 30:
                    matched_color = "Y"
                # 检查橙色（H在5-20之间，但要避免与红色混淆）
                elif 5 <= h_med < 20:
                    matched_color = "O"
                # 检查红色（H在0-5或170-180之间）
                elif (0 <= h_med < 5) or (170 <= h_med <= 180):
                    matched_color = "R"
                # 检查绿色（H在40-80之间）
                elif 40 <= h_med <= 80:
                    matched_color = "G"
                # 检查蓝色（H在90-130之间）
                elif 90 <= h_med <= 130:
                    matched_color = "B"

            colors.append(matched_color)

    return "".join(colors)


def recognize_cube(image: np.ndarray, verbose: bool = False):
    """
    识别魔方

    Args:
        image: 图像数组(numpy.ndarray)或图像路径(str)
        verbose: 是否显示详细信息

    Returns:
        魔方颜色字符串，格式为 "WYROGBX"
    """
    contour = find_cube_contour(image)
    if contour is None:
        print("未检测到魔方轮廓")
        return
    corrected = perspective_correct(image, contour)
    colors = get_cube_colors(corrected)

    if verbose:
        print("识别到的色块颜色:", colors)
        for i in range(3):
            for j in range(3):
                print(Color.to_chinese(colors[i * 3 + j]), end=" ")
            print()
        cv2.imshow("Recognized Cube", corrected)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return colors


def main():
    # 遍历 data/images 中的图片
    for file in os.listdir("data/images"):
        image = cv2.imread(f"data/images/{file}")
        recognize_cube(image, verbose=True)


if __name__ == "__main__":
    main()
