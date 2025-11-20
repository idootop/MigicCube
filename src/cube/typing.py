"""
三阶魔方核心数据结构
"""

from dataclasses import dataclass
from enum import Enum
from typing import Self

from .core.helper import parseFormula


class Color(Enum):
    """魔方颜色枚举"""

    @staticmethod
    def _process(colors: str, map: dict[str, str]) -> str:
        colors = colors.upper()
        colors_list = list(colors)
        for idx, color in enumerate(colors_list):
            colors_list[idx] = map.get(color, color)
        return "".join(colors_list)

    @staticmethod
    def to_core(colors: str) -> str:
        return Color._process(
            colors,
            {
                "W": "W",
                "Y": "Y",
                "B": "R",
                "R": "G",
                "G": "O",
                "O": "B",
            },
        )

    @staticmethod
    def from_core(colors: str) -> str:
        return Color._process(
            colors,
            {
                "W": "W",
                "Y": "Y",
                "B": "O",
                "O": "G",
                "G": "R",
                "R": "B",
            },
        )

    @staticmethod
    def to_chinese(colors: str) -> str:
        return Color._process(
            colors,
            {
                "Y": "黄",
                "W": "白",
                "R": "红",
                "O": "橙",
                "B": "蓝",
                "G": "绿",
            },
        )


class Face(Enum):
    """魔方面枚举"""

    FRONT = 0  # 前（红）
    LEFT = 1  # 左（蓝）
    RIGHT = 2  # 右（绿）
    UP = 3  # 上（黄）
    DOWN = 4  # 下（白）
    BACK = 5  # 后（橙）

    @staticmethod
    def str_to_core_cube(colors: str | None):
        if not colors:
            return None
        core_cube = [[["None" for _ in range(3)] for _ in range(3)] for _ in range(6)]
        colors_list = list(Color.to_core(colors))
        map = {
            "F": 0,
            "L": 3,
            "R": 1,
            "U": 5,
            "D": 4,
            "B": 2,
        }
        for idx, face in enumerate("FLRUDB"):
            for row in range(3):
                for col in range(3):
                    core_cube[map[face]][row][col] = colors_list[
                        idx * 9 + row * 3 + col
                    ]
        return core_cube

    @staticmethod
    def core_cube_to_str(cube: list[list[list[str]]]):
        colors_list = ["" for _ in range(54)]
        map = {
            "F": 0,
            "R": 1,
            "B": 2,
            "L": 3,
            "D": 4,
            "U": 5,
        }
        for idx, face in enumerate("FLRUDB"):
            for row in range(3):
                for col in range(3):
                    colors_list[idx * 9 + row * 3 + col] = cube[map[face]][row][col]
        return Color.from_core("".join(colors_list))


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
    def to_core(ops: str):
        return ops.replace(" ", "").replace("2'", "'2")

    @staticmethod
    def from_core(core_ops: str):
        ops_list = parseFormula(core_ops)
        for idx, op in enumerate(ops_list):
            ops_list[idx] = op if len(op) == 1 else op[0] + "'"
        merged_ops: list[str] = []
        for op in ops_list:
            if merged_ops and merged_ops[-1] == op:
                is_prime = "'" in op
                merged_ops[-1] = f"{op[0]}2" + ("'" if is_prime else "")
            else:
                merged_ops.append(op)
        return " ".join(merged_ops)

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
    def reverse_moves(ops: str):
        moves = ops.split(" ")
        moves.reverse()
        inverse_moves = [Move.reverse(m) for m in moves]
        return " ".join(inverse_moves)

    @staticmethod
    def description(op: str):
        prime = "'" in op
        double = "2次" if "2" in op else ""
        two_layer = "2层" if op[0] in "udfblr" else ""
        if op.upper().startswith("L"):
            return f"左{two_layer}{'上' if prime else '下'}{double}"
        elif op.upper().startswith("R"):
            return f"右{two_layer}{'下' if prime else '上'}{double}"
        elif op.upper().startswith("U"):
            return f"上{two_layer}{'右' if prime else '左'}{double}"
        elif op.upper().startswith("D"):
            return f"下{two_layer}{'左' if prime else '右'}{double}"
        elif op.upper().startswith("F"):
            return f"前{two_layer}{'右' if prime else '左'}{double}"
        elif op.upper().startswith("B"):
            return f"后{two_layer}{'左' if prime else '右'}{double}"
        elif op.startswith("M"):
            return f"竖中{'上' if prime else '下'}{double}"
        elif op.startswith("E"):
            return f"横中{'左' if prime else '右'}{double}"
        elif op.startswith("S"):
            return f"侧中{'右' if prime else '左'}{double}"
        elif op.startswith("x"):
            return f"整体{'下翻' if prime else '上翻'}{double}"
        elif op.startswith("y"):
            return f"整体{'右转' if prime else '左转'}{double}"
        elif op.startswith("z"):
            return f"整体侧{'右' if prime else '左'}{double}"
        return f"未知操作：{op}"


@dataclass
class Solution:
    align: str
    cross: str
    f2l: str
    oll: str
    pll: str

    @property
    def ops(self) -> str:
        full = f"{self.align}{self.cross}{self.f2l}{self.oll}{self.pll}"
        return Move.from_core(full)

    @property
    def reversed_ops(self) -> str:
        return Move.reverse_moves(self.ops)

    def print(self):
        print("\n✅ 魔方求解成功：\n")
        lines = [
            f"Align ({len(Move.from_core(self.align).split(' ')) or 0}步): {Move.from_core(self.align) or 'None'}",
            f"Cross ({len(Move.from_core(self.cross).split(' ')) or 0}步): {Move.from_core(self.cross) or 'None'}",
            f"F2L ({len(Move.from_core(self.f2l).split(' ')) or 0}步): {Move.from_core(self.f2l) or 'None'}",
            f"OLL ({len(Move.from_core(self.oll).split(' ')) or 0}步): {Move.from_core(self.oll) or 'None'}",
            f"PLL ({len(Move.from_core(self.pll).split(' ')) or 0}步): {Move.from_core(self.pll) or 'None'}",
            f"FULL ({len(self.ops.split(' ')) or 0}步): {self.ops}",
            f"REVERSED ({len(self.reversed_ops.split(' ')) or 0}步): {self.reversed_ops}",
        ]
        print("\n".join(lines))

    def print_ops(self):
        print("\n🔥 还原步骤：\n")
        moves = self.ops.split(" ")
        for idx, move in enumerate(moves):
            print(f"{idx + 1}. {Move.description(move)}")
            input("按回车继续...")
        print("\n✅ 还原完毕！")
