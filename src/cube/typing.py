"""
三阶魔方核心数据结构
"""

from enum import Enum
from typing import Self


class Color(Enum):
    """魔方颜色枚举"""

    YELLOW = "Y"  # 黄色（上）
    WHITE = "W"  # 白色（下）
    RED = "R"  # 红色（前）
    ORANGE = "O"  # 橙色（后）
    BLUE = "B"  # 蓝色（左）
    GREEN = "G"  # 绿色（右）

    def __str__(self):
        color_map = {
            "Y": "黄",
            "W": "白",
            "R": "红",
            "O": "橙",
            "B": "蓝",
            "G": "绿",
        }
        return color_map[self.value]


class Face(Enum):
    """魔方面枚举"""

    UP = 0  # 上（白）
    DOWN = 1  # 下（黄）
    FRONT = 2  # 前（红）
    BACK = 3  # 后（橙）
    LEFT = 4  # 左（绿）
    RIGHT = 5  # 右（蓝）


class Move(Enum):
    """
    魔方转动操作
    [face][times][direction]
    face: 转动面, 上、下、前、后、左、右
    times: 转动次数, 90度、180度
    direction: 转动方向, 顺时针或逆时针
    """

    # 外层 1 层
    U = "U"  # 上
    D = "D"  # 下
    F = "F"  # 前
    B = "B"  # 后
    L = "L"  # 左
    R = "R"  # 右
    # 外层 2 层
    u = "u"  # 上 2 层
    d = "d"  # 下 2 层
    f = "f"  # 前 2 层
    b = "b"  # 后 2 层
    l = "l"  # 左 2 层
    r = "r"  # 右 2 层
    # 中间 1 层
    M = "M"  # 左中
    E = "E"  # 底中
    S = "S"  # 前中
    # 整体 3 层
    x = "x"  # X 轴
    y = "y"  # Y 轴
    z = "z"  # Z 轴

    @staticmethod
    def reverse(op: str | Self):
        if isinstance(op, Move):
            op = op.value
        if "'" in op:
            return op.replace("'", "")
        if "2" in op:
            return op  # 180度转动逆操作还是180度
        return op + "'"

    @staticmethod
    def reverse_moves(moves: str | list[str] | list[Self]):
        if isinstance(moves, str):
            moves = moves.split(" ")
        inverse_moves = [Move.reverse(m) for m in moves]
        return " ".join(inverse_moves)

    @staticmethod
    def get_info(op: str | Self):
        if isinstance(op, Move):
            op = op.value
        times = 1
        move = op[0]
        clockwise = "'" not in op
        op_times = op.replace("'", "")
        if len(op_times) > 1:
            times = int(op_times[-1])
        return move, times, clockwise

    @staticmethod
    def get_description(op: str | Self) -> str:
        move, times, clockwise = Move.get_info(op)
        move_map = {
            "U": "上面",
            "D": "下面",
            "F": "前面",
            "B": "后面",
            "L": "左边",
            "R": "右边",
            "M": "左中",
            "E": "下中",
            "S": "前中",
            "x": "X轴",
            "y": "Y轴",
            "z": "Z轴",
        }
        two_layer = move in ["u", "d", "f", "b", "l", "r"]
        move_key = move.upper() if two_layer else move
        description = move_map[move_key]
        if two_layer:
            description += "2层"
        if not clockwise:
            description += "逆时针"
        if times > 1:
            description += f"旋转{times}次"
        return description
