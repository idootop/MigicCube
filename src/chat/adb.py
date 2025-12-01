"""
ADB 工具模块
提供与 Android 设备交互的功能
"""

import re
import subprocess
import time
from dataclasses import dataclass
from typing import Callable


@dataclass
class AsrMessage:
    """语音识别消息"""

    id: str
    text: str
    raw: str


class AdbHelper:
    """ADB 辅助类"""

    def __init__(
        self,
        server_device: str = "",
        client_device: str = "",
    ):
        self.server_device = server_device
        self.client_device = client_device

    def clear_logcat(self):
        """清除 logcat 日志"""
        subprocess.run(
            ["adb", "-s", self.server_device, "logcat", "-c"],
            capture_output=True,
        )

    def listen_asr(self, callback: Callable[[AsrMessage], bool]):
        """
        监听语音识别输出

        Args:
            callback: 回调函数，接收 AsrMessage，返回 True 继续监听，False 停止
        """
        self.clear_logcat()

        process = subprocess.Popen(
            ["adb", "-s", self.server_device, "logcat"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        pattern = re.compile(r"onAsrFinal:([a-f0-9]+),(.+)$")

        try:
            assert process.stdout is not None
            for line in process.stdout:
                if "onAsrFinal" in line:
                    match = pattern.search(line)
                    if match:
                        msg = AsrMessage(
                            id=match.group(1),
                            text=match.group(2).strip(),
                            raw=line.strip(),
                        )
                        if not callback(msg):
                            break
        finally:
            process.terminate()
            process.wait()

    def take_photo(self, output_path: str = "temp/photo.jpg") -> bool:
        """
        使用客户端设备拍照并保存到本地

        Args:
            output_path: 本地保存路径

        Returns:
            是否成功
        """
        try:
            # 发送拍照广播
            subprocess.run(
                [
                    "adb",
                    "-s",
                    self.client_device,
                    "shell",
                    "am",
                    "broadcast",
                    "-a",
                    "android.intent.action.lumi.TAKE_PHOTO",
                ],
                capture_output=True,
                check=True,
            )

            # 等待拍照完成
            time.sleep(1.5)

            # 获取图片到本地
            result = subprocess.run(
                [
                    "adb",
                    "-s",
                    self.client_device,
                    "shell",
                    "cat /storage/emulated/0/DCIM/XiaoAi/*.jpg",
                ],
                capture_output=True,
            )

            if result.returncode == 0 and result.stdout:
                with open(output_path, "wb") as f:
                    f.write(result.stdout)
                return True
            return False

        except subprocess.CalledProcessError:
            return False
