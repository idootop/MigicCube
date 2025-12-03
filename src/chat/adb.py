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
        tts_api: str = "",
    ):
        self.server_device = server_device
        self.client_device = client_device
        self.tts_api = tts_api

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

    def shell(
        self,
        command: str,
        device="client",
        error_message="调用失败",
        return_result=False,
    ):
        """
        调用客户端设备
        """
        try:
            result = subprocess.run(
                [
                    "adb",
                    "-s",
                    self.client_device if device == "client" else self.server_device,
                    "shell",
                    command,
                ],
                capture_output=True,
                check=True,
            )
            if return_result:
                return result
            return result.returncode == 0
        except Exception as e:
            print(f"{error_message}: {e}")
            if return_result:
                return None
            return False

    def save_photo(self, output_path: str = "temp/photo.jpg") -> bool:
        """
        保存最新图片封面到本地
        """
        result = self.shell(
            "cat /storage/emulated/0/DCIM/XiaoAi/*.jpg",
            error_message="保存图片失败",
            device="client",
            return_result=True,
        )
        if result and result.stdout:
            with open(output_path, "wb") as f:
                f.write(result.stdout)
            return True
        return False

    def take_photo(self) -> bool:
        return self.shell(
            "am broadcast -a android.intent.action.lumi.TAKE_PHOTO",
            error_message="拍照失败",
            device="client",
        )

    def play_audio(self, uri: str):
        # 使用第三方应用（https://github.com/mpv-android/mpv-android）播放音频
        return self.shell(
            f'am force-stop is.xyz.mpv && am start -a android.intent.action.VIEW -p is.xyz.mpv -t audio/* -d "{uri}"',
            error_message="播放失败",
            device="client",
        )

    def tts(self, text: str):
        if not self.tts_api:
            return
        return self.play_audio(f"{self.tts_api}?text={text}")
