"""
魔方对话服务核心模块
"""

import os
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Optional

from .adb import AdbHelper, AsrMessage
from .image import CubeImageProcessor


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
    solution_steps: list[str] = field(default_factory=list)
    current_step_index: int = 0

    def reset(self):
        """重置上下文"""
        self.state = DialogState.IDLE
        self.faces = []
        self.current_face_index = 0
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

    def __init__(
        self,
        adb_helper: Optional[AdbHelper] = None,
        image_processor: Optional[CubeImageProcessor] = None,
        notify_callback: Optional[Callable[[str], None]] = None,
        demo_mode: bool = False,
    ):
        self.adb = adb_helper or AdbHelper()
        self.image_processor = image_processor or CubeImageProcessor()
        self.context = DialogContext()
        self._notify = notify_callback or self._default_notify
        self._demo_mode = demo_mode

        # 确保 temp 目录存在
        os.makedirs("temp", exist_ok=True)

    def _default_notify(self, message: str):
        """默认通知方法（打印到控制台）"""
        print(f"🤖 助手: {message}")

    def notify(self, message: str):
        """通知用户"""
        self._notify(message)

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
        keywords = ["这是", "这个是", "这面是", "好了", "拍好了", "拍照", "收到"]
        return any(kw in text for kw in keywords)

    def _handle_cube_trigger(self):
        """处理魔方触发"""
        self.context.state = DialogState.WAITING_FACE
        self.context.faces = []
        self.context.current_face_index = 0

        current_face = self._get_current_face()
        self.notify(f"好的主人，让我先看下魔方的{current_face.chinese_name}是什么颜色")

    def _handle_face_confirmation(self, text: str):
        """处理面确认"""
        current_face = self._get_current_face()
        if not current_face:
            return

        # 拍照
        image_path = f"temp/cube_{current_face.name}.jpg"

        colors: str
        if self._demo_mode:
            # 演示模式下跳过拍照
            self.notify(f"[演示模式] 已获取{current_face.chinese_name}的颜色")
            colors = self.image_processor.get_placeholder_colors(current_face.name)
        else:
            self.notify(f"正在拍摄{current_face.chinese_name}...")

            success = self.adb.take_photo(image_path)
            if not success:
                self.notify("拍照失败，请重试")
                return

            # 从图片提取颜色（目前使用占位符）
            extracted = self.image_processor.extract_colors(image_path)
            if extracted is None:
                # 使用占位符颜色
                colors = self.image_processor.get_placeholder_colors(current_face.name)
            else:
                colors = extracted

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
            self.notify(f"收到，让我再看看魔方的{next_face.chinese_name}是什么颜色")
        else:
            self._start_solving()

    def _start_solving(self):
        """开始求解魔方"""
        self.context.state = DialogState.SOLVING

        # 组合魔方状态字符串
        # 顺序: FRONT(9) + LEFT(9) + RIGHT(9) + UP(9) + DOWN(9) + BACK(9)
        face_map = {face.name: face.colors for face in self.context.faces}

        cube_state = (
            face_map.get("front", "X" * 9)
            + face_map.get("left", "X" * 9)
            + face_map.get("right", "X" * 9)
            + face_map.get("up", "X" * 9)
            + face_map.get("down", "X" * 9)
            + face_map.get("back", "X" * 9)
        )

        try:
            from cube import Cube

            cube = Cube(cube_state)

            if cube.is_solved():
                self.notify("魔方已经是还原状态，无需求解！")
                self.context.reset()
                return

            solution = cube.solve()

            # 解析操作步骤
            moves = solution.ops.split(" ")
            self.context.solution_steps = moves
            self.context.current_step_index = 0
            self.context.state = DialogState.GUIDING

            self.notify(f"魔方已经解好了！一共需要 {len(moves)} 步")
            self._show_current_step()

        except Exception as e:
            self.notify(f"求解失败: {e}")
            self.context.reset()

    def _show_current_step(self):
        """显示当前步骤"""
        from cube.typing import Move

        if self.context.current_step_index >= len(self.context.solution_steps):
            self.context.reset()
            return

        step = self.context.current_step_index + 1
        total = len(self.context.solution_steps)
        move = self.context.solution_steps[self.context.current_step_index]
        desc = Move.description(move)

        self.notify(
            f"{desc}，{f'还剩{total - step}步' if total - step > 0 else '魔方已解'}"
        )

    def _handle_next_step(self):
        """处理下一步指令"""
        self.context.current_step_index += 1
        self._show_current_step()

    def _is_next_step_command(self, text: str) -> bool:
        """检查是否是下一步指令"""
        keywords = ["下一步", "下一个", "继续", "好了", "完成", "搞定"]
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
        self.notify('魔方助手已启动，说"魔方"开始...')

        try:
            self.adb.listen_asr(self.handle_message)
        except KeyboardInterrupt:
            self.notify("服务已停止")

    def demo_mode(self, interactive: bool = True):
        """
        演示模式（不需要 ADB 设备）
        模拟用户输入进行测试

        Args:
            interactive: 是否交互式（等待用户按回车）
        """
        # 启用演示模式标志
        self._demo_mode = True
        self.notify("进入演示模式...")

        # 模拟用户输入序列
        demo_inputs = [
            "帮我还原魔方",
            "这是前面",
            "这是上面",
            "这是下面",
            "这是左面",
            "这是右面",
            "这是后面",
        ]

        for text in demo_inputs:
            msg = AsrMessage(id="demo", text=text, raw=text)
            self._handle_message_internal(msg)

            if self.context.state == DialogState.GUIDING:
                break

        # 模拟用户逐步确认
        if self.context.state == DialogState.GUIDING:
            while self.context.current_step_index < len(self.context.solution_steps):
                if interactive:
                    try:
                        input("按回车继续下一步...")
                    except EOFError:
                        # 非交互模式下自动继续
                        pass
                msg = AsrMessage(id="demo", text="下一步", raw="下一步")
                self._handle_message_internal(msg)
