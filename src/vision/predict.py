from typing import Union

import numpy as np
import torch
from ultralytics import YOLO


class YOLOv11Predictor:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def predict(
        source: Union[str, np.ndarray],
        verbose: bool = False,
        conf_threshold=0.5,
        iou_threshold=0.5,
    ):
        """
        对图片进行预测

        Args:
            source: 图片路径(str)或图像数组(numpy.ndarray)
            verbose: 是否显示详细信息
            conf_threshold: 置信度阈值
            iou_threshold: IoU阈值
        """
        self = YOLOv11Predictor()

        results = self.model.predict(
            source=source,
            conf=conf_threshold,
            iou=iou_threshold,
            device=self.device,
            verbose=verbose,
        )

        if verbose:
            results[0].plot(show=True)

        return self._get_detection_info(results[0])

    def __init__(self, model_path="data/model.pt"):
        """初始化YOLO预测器"""

        # 检查设备
        if torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

        # 加载模型
        self.model = YOLO(model_path)
        self.model.to(self.device)

    def _get_detection_info(self, results):
        """获取检测结果的详细信息"""

        detections = []

        if results.boxes is not None:
            boxes = (
                results.boxes.xyxy.cpu().numpy().tolist()
            )  # 边界框坐标 [x1, y1, x2, y2]
            confidences = results.boxes.conf.cpu().numpy()  # 置信度
            class_ids = results.boxes.cls.cpu().numpy()  # 类别ID
            for i in range(len(boxes)):
                detection = {
                    "class_id": int(class_ids[i]),
                    "class_name": self.model.names[int(class_ids[i])],
                    "confidence": float(confidences[i]),
                    "bbox": boxes[i],  # [x1, y1, x2, y2]
                    "bbox_xywh": [  # 转换为 [x, y, width, height] 格式
                        boxes[i][0],
                        boxes[i][1],
                        boxes[i][2] - boxes[i][0],
                        boxes[i][3] - boxes[i][1],
                    ],
                }
                detections.append(detection)

        return detections


if __name__ == "__main__":
    detections = YOLOv11Predictor.predict("data/test.jpg", verbose=True)
    print("✅ done")
