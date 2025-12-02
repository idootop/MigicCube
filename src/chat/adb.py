"""
ADB 工具模块
提供与 Android 设备交互的功能
"""

import re
import subprocess
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

    def listen_volume(self, on_message: Callable[[AsrMessage], bool]):
        """
        监听音量变化
        """
        process = subprocess.Popen(
            [
                "adb",
                "-s",
                self.server_device,
                "shell",
                "watch -n 1 'dumpsys audio | grep -i setStreamVolume | tail -n 1'",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        set_volume_pattern = re.compile(
            r"setStreamVolume\(stream:STREAM_MUSIC index:(\d+) flags:0x40 oldIndex:(\d+)\) from com.android.bluetooth"
        )

        last = ""
        try:
            assert process.stdout is not None
            for line in process.stdout:
                match = set_volume_pattern.search(line)
                if match:
                    index = int(match.group(1))
                    old_index = int(match.group(2))
                    if last and line.strip() != last:
                        volume_up = index > old_index
                        if index == old_index:
                            volume_up = index > 1
                        on_message(
                            AsrMessage(
                                id=f"volume_{'up' if volume_up else 'down'}",
                                text="音量变大" if volume_up else "音量变小",
                                raw=line.strip(),
                            )
                        )
                    last = line.strip()

        finally:
            process.terminate()
            process.wait()

    def logcat(self, on_message: Callable[[AsrMessage], bool]):
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

        asr_pattern = re.compile(r"onAsrFinal:([a-f0-9]+),(.+)$")
        take_photo_pattern = re.compile(r"Device-Sync: type: 18")

        try:
            assert process.stdout is not None
            for line in process.stdout:
                if "Device-Sync" in line:
                    match = take_photo_pattern.search(line)
                    if match:
                        on_message(
                            AsrMessage(id="take_photo", text="拍照", raw=line.strip())
                        )
                elif "onAsrFinal" in line:
                    match = asr_pattern.search(line)
                    if match:
                        msg = AsrMessage(
                            id=match.group(1),
                            text=match.group(2).strip(),
                            raw=line.strip(),
                        )
                        if not on_message(msg):
                            break
        finally:
            process.terminate()
            process.wait()

    def save_photo(self, output_path: str = "temp/photo.jpg") -> bool:
        """
        保存最新图片封面到本地
        """
        try:
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
            if result.stdout:
                with open(output_path, "wb") as f:
                    f.write(result.stdout)
                return True
            return False
        except Exception as e:
            print(f"保存图片失败: {e}")
            return False

    def take_photo(self) -> bool:
        """
        使用客户端设备拍照（拍照时需要确保不在唤醒状态）
        """
        try:
            # 发送拍照广播
            result = subprocess.run(
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
            return result.returncode == 0
        except Exception as e:
            print(f"拍照失败: {e}")
            return False
