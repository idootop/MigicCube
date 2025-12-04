"""
魔方对话服务核心模块
"""

import os
import threading
from dataclasses import dataclass, field
from enum import Enum, auto
from time import sleep
from typing import Any, Optional

from cube import Cube
from cube.typing import Move, Solution
from utils.core import write_json
from vision.image import extract_colors

from .adb import AdbHelper, AsrMessage


class DialogState(Enum):
    """对话状态"""

    IDLE = auto()  # 空闲状态，等待用户触发
    WAITING_FACE = auto()  # 等待用户确认魔方面
    COLLECTING_FACES = auto()  # 收集魔方各面
    SOLVING = auto()  # 求解中
    GUIDING = auto()  # 指导用户操作


@dataclass
class CubeFaceData:
    """魔方面数据"""

    name: str  # 面名称
    chinese_name: str  # 中文名称
    colors: str = ""  # 颜色字符串 (9个字符)
    image_path: str = ""  # 图片路径


@dataclass
class DialogContext:
    """对话上下文"""

    state: DialogState = DialogState.IDLE

    # 魔方相关
    faces: list[CubeFaceData] = field(default_factory=list)
    current_face_index: int = 0

    # 求解相关
    solution: Solution | None = None
    current_step_index: int = 0
    solution_steps: list[str] = field(default_factory=list)

    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value
        if name == "current_step_index" and self.solution:
            write_json(
                "src/web/state.json",
                {
                    "step": value,
                    "ops": self.solution.ops,
                    "reversed_ops": self.solution.reversed_ops,
                },
            )
        elif name == "solution" and not value:
            # 清空状态
            write_json("src/web/state.json", "{}")

    def reset(self):
        """重置上下文"""
        self.state = DialogState.IDLE
        self.faces = []
        self.current_face_index = 0
        self.solution = None
        self.solution_steps = []
        self.current_step_index = 0


class ChatService:
    """对话服务"""

    # 魔方六个面的收集顺序
    FACE_ORDER = [
        CubeFaceData("front", "前面"),
        CubeFaceData("up", "上面"),
        CubeFaceData("down", "下面"),
        CubeFaceData("left", "左面"),
        CubeFaceData("right", "右面"),
        CubeFaceData("back", "后面"),
    ]

    def __init__(self, adb_helper: Optional[AdbHelper] = None, debug: bool = False):
        self.adb = adb_helper or AdbHelper()
        self.debug = debug
        self.context = DialogContext()
        self._cube_state: str | None = None

        # 确保 temp 目录存在
        os.makedirs("temp", exist_ok=True)

    def notify(self, message: str):
        """默认通知方法（打印到控制台）"""
        print(f"🤖 助手: {message}")
        self.adb.tts(message)

    def _get_current_face(self) -> Optional[CubeFaceData]:
        """获取当前需要收集的面"""
        if self.context.current_face_index < len(self.FACE_ORDER):
            return self.FACE_ORDER[self.context.current_face_index]
        return None

    def _get_next_face(self) -> Optional[CubeFaceData]:
        """获取下一个需要收集的面"""
        next_index = self.context.current_face_index + 1
        if next_index < len(self.FACE_ORDER):
            return self.FACE_ORDER[next_index]
        return None

    def _is_face_confirmation(self, text: str) -> bool:
        """检查是否是面确认指令"""
        keywords = ["这是", "好了", "继续", "好的", "拍照"]
        return any(kw in text for kw in keywords)

    def _handle_cube_trigger(self):
        """处理魔方触发"""
        self.context.state = DialogState.WAITING_FACE
        self.context.faces = []
        self.context.current_face_index = 0

        current_face = self._get_current_face()
        self.notify(f"好的主人，让我看下魔方{current_face.chinese_name}是什么颜色。")

    def _handle_face_confirmation(self, text: str):
        """处理面确认"""
        current_face = self._get_current_face()
        if not current_face:
            return

        # 拍照（语音指令触发时，比如：好了）
        if "拍照" not in text:
            self.adb.take_photo()
            return

        # 等待缩略图更新
        sleep(1)

        # 获取图片
        image_path = f"temp/cube_{current_face.name}.jpg"
        if not self.adb.save_photo(image_path):
            self.notify("获取图片失败，请重试")
            return

        # 从图片提取颜色
        colors = extract_colors(image_path)

        # 保存面数据
        face_data = CubeFaceData(
            name=current_face.name,
            chinese_name=current_face.chinese_name,
            colors=colors,
            image_path=image_path,
        )
        self.context.faces.append(face_data)
        self.context.current_face_index += 1

        # 检查是否收集完成
        next_face = self._get_current_face()
        if next_face:
            self.notify(f"好的，让我看看{next_face.chinese_name}是什么颜色。")
        else:
            self._start_solving()

    def _start_solving(self):
        """开始求解魔方"""
        self.context.state = DialogState.SOLVING

        # 组合魔方状态字符串
        # 顺序: FRONT(9) + LEFT(9) + RIGHT(9) + UP(9) + DOWN(9) + BACK(9)
        face_map = {face.name: face.colors for face in self.context.faces}

        cube_state = (
            self._cube_state
            if self._cube_state
            else (
                face_map.get("front", "X" * 9)
                + face_map.get("left", "X" * 9)
                + face_map.get("right", "X" * 9)
                + face_map.get("up", "X" * 9)
                + face_map.get("down", "X" * 9)
                + face_map.get("back", "X" * 9)
            )
        )

        try:
            cube = Cube(cube_state)

            if cube.is_solved():
                self.notify("魔方已经是还原状态，无需求解！")
                self.context.reset()
                return

            solution = cube.solve()

            # 解析操作步骤
            moves = solution.ops.split(" ")
            self.context.solution_steps = moves
            self.context.solution = solution
            self.context.current_step_index = 0
            self.context.state = DialogState.GUIDING

            self.notify(f"魔方已经解好了！一共需要 {len(moves)} 步")

        except Exception as e:
            self.notify(f"求解失败: {e}")
            self.context.reset()

    def _handle_next_step(self):
        """处理下一步指令"""
        total = len(self.context.solution_steps)
        step = self.context.current_step_index

        if step + 1 > total:
            return

        move = self.context.solution_steps[step]
        desc = Move.description(move)
        remaining_steps = total - 1 - step
        self.notify(f"{desc}。{'' if remaining_steps > 0 else '魔方已解。'}")
        self.context.current_step_index = step + 1

    def _handle_previous_step(self):
        """处理上一步指令"""
        step = self.context.current_step_index
        if step - 1 < -1:
            return

        self.notify("好了")
        self.context.current_step_index = step - 1

    def _is_next_step_command(self, text: str) -> bool:
        """检查是否是下一步指令"""
        keywords = ["下一步", "好了", "好的", "继续", "音量变大"]
        return any(kw in text for kw in keywords)

    def _is_previous_step_command(self, text: str) -> bool:
        """检查是否是上一步指令"""
        keywords = ["上一步", "音量变小"]
        return any(kw in text for kw in keywords)

    def _is_exit_command(self, text: str) -> bool:
        """检查是否是退出指令"""
        keywords = ["退出", "结束", "取消", "停止", "不玩了", "算了"]
        return any(kw in text for kw in keywords)

    def _is_cube_trigger(self, text: str) -> bool:
        """检查是否是魔方触发词"""
        return "魔方" in text

    def _handle_message_internal(self, message: AsrMessage) -> bool:
        """
        内部消息处理逻辑

        Args:
            message: 语音识别消息

        Returns:
            True 继续监听，False 停止
        """
        text = message.text
        print(f"👤 用户: {text}")

        # 检查退出指令
        if self._is_exit_command(text):
            self.notify("好的，已退出魔方助手")
            self.context.reset()
            return True  # 继续监听，只是重置状态

        # 根据当前状态处理
        if self.context.state == DialogState.IDLE:
            if self._is_cube_trigger(text):
                self._handle_cube_trigger()

        elif self.context.state == DialogState.WAITING_FACE:
            if self._is_face_confirmation(text):
                self._handle_face_confirmation(text)

        elif self.context.state == DialogState.GUIDING:
            if self._is_next_step_command(text):
                self._handle_next_step()
            elif self._is_previous_step_command(text):
                self._handle_previous_step()

        return True

    def handle_message(self, message: AsrMessage) -> bool:
        """
        处理语音消息（ADB 回调入口）

        Args:
            message: 语音识别消息

        Returns:
            True 继续监听，False 停止
        """
        return self._handle_message_internal(message)

    def start(self):
        """启动对话服务"""
        print('魔方助手已启动，请说"解魔方"开始...')

        if self.debug:
            self._cube_state = "WYBRRYGROGGRGBBYYOOBROGWWRBYBBOYOGBWYWGGWGBRWYWROOWRYO"
            self._start_solving()

        threads = []
        try:
            logcat_thread = threading.Thread(
                target=self.adb.logcat, args=(self.handle_message,)
            )
            volume_thread = threading.Thread(
                target=self.adb.listen_volume, args=(self.handle_message,)
            )
            threads.append(logcat_thread)
            threads.append(volume_thread)
            for thread in threads:
                thread.start()
        except KeyboardInterrupt:
            pass
        finally:
            for thread in threads:
                thread.join()
