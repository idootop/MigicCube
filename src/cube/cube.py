"""
三阶魔方类
"""

import random
from typing import Optional

from .typing import Color, Face, Move


class Cube:
    """三阶魔方类"""

    def __init__(self, state: Optional[list[list[list[Color]]]] = None):
        """
        初始化魔方

        Args:
            state: 6x3x3的颜色数组，如果为None则初始化为已还原状态
        """
        if state is None:
            self.reset()
        else:
            self.faces = state

    def reset(self):
        self.faces = [
            [[Color.YELLOW] * 3 for _ in range(3)],
            [[Color.WHITE] * 3 for _ in range(3)],
            [[Color.RED] * 3 for _ in range(3)],
            [[Color.ORANGE] * 3 for _ in range(3)],
            [[Color.BLUE] * 3 for _ in range(3)],
            [[Color.GREEN] * 3 for _ in range(3)],
        ]
        return self

    def get_face(self, face: Face) -> list[list[Color]]:
        """获取指定面的颜色矩阵"""
        return [row[:] for row in self.faces[face.value]]

    def set_face(self, face: Face, colors: list[list[Color]]):
        """设置指定面的颜色矩阵"""
        self.faces[face.value] = [row[:] for row in colors]

    def copy(self) -> "Cube":
        """创建魔方的深拷贝"""
        new_faces = [[[color for color in row] for row in face] for face in self.faces]
        return Cube(new_faces)

    def is_solved(self) -> bool:
        """检查魔方是否已还原"""
        for face_idx in range(6):
            face = self.faces[face_idx]
            first_color = face[0][0]
            for row in face:
                for color in row:
                    if color != first_color:
                        return False
        return True

    def apply_move(self, op: str | Move):
        """
        应用一个转动操作

        支持的操作格式：
        - 基本操作：U, D, F, B, L, R（顺时针90度）
        - 逆时针：U', D', F', B', L', R'（逆时针90度）
        - 双层：u, d, f, b, l, r（外两层一起转）
        - 中层：M, E, S（中间层单独转）
        - 整体旋转：x, y, z（整个魔方旋转）
        - 多次旋转：U2, U2', u3等（可指定次数）

        Args:
            op: 转动操作字符串或Move枚举
        """
        move, times, clockwise = Move.get_info(op)

        # 如果是逆时针，转换为顺时针3次
        if not clockwise:
            times = times * 3

        # 执行指定次数的旋转
        for _ in range(times):
            # 基本6面操作
            if move == "U":
                self._rotate_U()
            elif move == "D":
                self._rotate_D()
            elif move == "F":
                self._rotate_F()
            elif move == "B":
                self._rotate_B()
            elif move == "L":
                self._rotate_L()
            elif move == "R":
                self._rotate_R()
            # 双层操作（外两层）
            elif move == "u":
                self._rotate_U()
                self._rotate_E()
                self._rotate_E()
                self._rotate_E()  # E与U反向，所以转3次
            elif move == "d":
                self._rotate_D()
                self._rotate_E()
            elif move == "f":
                self._rotate_F()
                self._rotate_S()
            elif move == "b":
                self._rotate_B()
                self._rotate_S()
                self._rotate_S()
                self._rotate_S()  # S与B反向
            elif move == "l":
                self._rotate_L()
                self._rotate_M()
            elif move == "r":
                self._rotate_R()
                self._rotate_M()
                self._rotate_M()
                self._rotate_M()  # M与R反向
            # 中层操作
            elif move == "M":
                self._rotate_M()
            elif move == "E":
                self._rotate_E()
            elif move == "S":
                self._rotate_S()
            # 整体旋转
            elif move == "x":
                # x = R + M' + L'
                self._rotate_R()
                self._rotate_M()
                self._rotate_M()
                self._rotate_M()
                self._rotate_L()
                self._rotate_L()
                self._rotate_L()
            elif move == "y":
                # y = U + E' + D'
                self._rotate_U()
                self._rotate_E()
                self._rotate_E()
                self._rotate_E()
                self._rotate_D()
                self._rotate_D()
                self._rotate_D()
            elif move == "z":
                # z = F + S + B'
                self._rotate_F()
                self._rotate_S()
                self._rotate_B()
                self._rotate_B()
                self._rotate_B()
            else:
                raise ValueError(f"不支持的操作: {move}")

    def apply_moves(self, moves: str | list[str] | list[Move]):
        """应用一系列转动操作"""
        if isinstance(moves, str):
            moves = moves.split(" ")
        for move in moves:
            self.apply_move(move)
        return self

    def scramble(self, moves_count: int = 100):
        """打乱魔方"""
        moves = random.choices(list(Move), k=moves_count)
        self.apply_moves(moves)
        return self

    def __str__(self) -> str:
        """获取魔方状态的字符串表示"""
        # 按照标准顺序：上、下、前、后、左、右
        result = []
        for face in [Face.UP, Face.DOWN, Face.FRONT, Face.BACK, Face.LEFT, Face.RIGHT]:
            for row in self.faces[face.value]:
                result.append("".join(color.value for color in row))
        return "".join(result)

    @classmethod
    def from_string(cls, state_str: str) -> "Cube":
        """从字符串创建魔方状态"""
        if len(state_str) != 54:  # 6面 * 9块 = 54
            raise ValueError(f"状态字符串长度必须为54，当前为{len(state_str)}")

        color_map = {
            "W": Color.WHITE,
            "Y": Color.YELLOW,
            "R": Color.RED,
            "O": Color.ORANGE,
            "G": Color.GREEN,
            "B": Color.BLUE,
        }

        faces = []
        idx = 0
        for _ in range(6):
            face = []
            for _ in range(3):
                row = []
                for _ in range(3):
                    char = state_str[idx].upper()
                    if char not in color_map:
                        raise ValueError(f"无效的颜色字符: {char}")
                    row.append(color_map[char])
                    idx += 1
                face.append(row)
            faces.append(face)

        return cls(faces)

    def visualize(self):
        """
        按面打印魔方状态，标准展开图格式：
              上(U)
        左(L) 前(F) 右(R) 后(B)
              下(D)
        """
        # 获取各面数据
        up = self.faces[Face.UP.value]
        down = self.faces[Face.DOWN.value]
        front = self.faces[Face.FRONT.value]
        back = self.faces[Face.BACK.value]
        left = self.faces[Face.LEFT.value]
        right = self.faces[Face.RIGHT.value]

        # 使用全角空格保证对齐（中文字符是2个宽度）
        space = "      "  # 两个全角空格，对应6个字符宽度

        # 打印上面（U）- 居中显示
        print()
        print(f"{space}+-----+")
        for row in up:
            colors = " ".join(str(color) for color in row)
            print(f"{space}|{colors}|")

        # 打印中间一行：左(L) 前(F) 右(R) 后(B)
        print("+-----+-----+-----+-----+")
        for i in range(3):
            left_colors = " ".join(str(color) for color in left[i])
            front_colors = " ".join(str(color) for color in front[i])
            right_colors = " ".join(str(color) for color in right[i])
            back_colors = " ".join(str(color) for color in back[i])
            print(f"|{left_colors}|{front_colors}|{right_colors}|{back_colors}|")
        print("+-----+-----+-----+-----+")

        # 打印下面（D）- 居中显示
        for row in down:
            colors = " ".join(str(color) for color in row)
            print(f"{space}|{colors}|")
        print(f"{space}+-----+")
        print()

    def _rotate_face_clockwise(self, face: Face):
        """顺时针旋转一个面90度"""
        old_face = self.get_face(face)
        # 矩阵转置后每行反转 = 顺时针旋转90度
        new_face = [[old_face[2 - j][i] for j in range(3)] for i in range(3)]
        self.set_face(face, new_face)

    def _rotate_face_counterclockwise(self, face: Face):
        """逆时针旋转一个面90度"""
        # 逆时针 = 顺时针3次
        for _ in range(3):
            self._rotate_face_clockwise(face)

    def _rotate_U(self):
        """上面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.UP)
        # 旋转相邻的边
        temp = [self.faces[Face.FRONT.value][0][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.FRONT.value][0][i] = self.faces[Face.RIGHT.value][0][i]
            self.faces[Face.RIGHT.value][0][i] = self.faces[Face.BACK.value][0][i]
            self.faces[Face.BACK.value][0][i] = self.faces[Face.LEFT.value][0][i]
            self.faces[Face.LEFT.value][0][i] = temp[i]

    def _rotate_D(self):
        """下面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.DOWN)
        # 旋转相邻的边
        temp = [self.faces[Face.FRONT.value][2][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.FRONT.value][2][i] = self.faces[Face.LEFT.value][2][i]
            self.faces[Face.LEFT.value][2][i] = self.faces[Face.BACK.value][2][i]
            self.faces[Face.BACK.value][2][i] = self.faces[Face.RIGHT.value][2][i]
            self.faces[Face.RIGHT.value][2][i] = temp[i]

    def _rotate_F(self):
        """前面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.FRONT)
        # 旋转相邻的边
        temp = [self.faces[Face.UP.value][2][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][2][i] = self.faces[Face.LEFT.value][2 - i][2]
            self.faces[Face.LEFT.value][2 - i][2] = self.faces[Face.DOWN.value][0][i]
            self.faces[Face.DOWN.value][0][i] = self.faces[Face.RIGHT.value][2 - i][0]
            self.faces[Face.RIGHT.value][2 - i][0] = temp[i]

    def _rotate_B(self):
        """后面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.BACK)
        # 旋转相邻的边
        temp = [self.faces[Face.UP.value][0][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][0][i] = self.faces[Face.RIGHT.value][i][2]
            self.faces[Face.RIGHT.value][i][2] = self.faces[Face.DOWN.value][2][2 - i]
            self.faces[Face.DOWN.value][2][2 - i] = self.faces[Face.LEFT.value][i][0]
            self.faces[Face.LEFT.value][i][0] = temp[i]

    def _rotate_L(self):
        """左面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.LEFT)
        # 旋转相邻的边
        temp = [self.faces[Face.UP.value][i][0] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][i][0] = self.faces[Face.BACK.value][2 - i][2]
            self.faces[Face.BACK.value][2 - i][2] = self.faces[Face.DOWN.value][i][0]
            self.faces[Face.DOWN.value][i][0] = self.faces[Face.FRONT.value][i][0]
            self.faces[Face.FRONT.value][i][0] = temp[i]

    def _rotate_R(self):
        """右面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.RIGHT)
        # 旋转相邻的边
        temp = [self.faces[Face.UP.value][i][2] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][i][2] = self.faces[Face.FRONT.value][i][2]
            self.faces[Face.FRONT.value][i][2] = self.faces[Face.DOWN.value][i][2]
            self.faces[Face.DOWN.value][i][2] = self.faces[Face.BACK.value][2 - i][0]
            self.faces[Face.BACK.value][2 - i][0] = temp[i]

    def _rotate_M(self):
        """中间层M（与L同向）顺时针旋转90度"""
        # M层是左右之间的中间层，与L同向
        temp = [self.faces[Face.UP.value][i][1] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][i][1] = self.faces[Face.BACK.value][2 - i][1]
            self.faces[Face.BACK.value][2 - i][1] = self.faces[Face.DOWN.value][i][1]
            self.faces[Face.DOWN.value][i][1] = self.faces[Face.FRONT.value][i][1]
            self.faces[Face.FRONT.value][i][1] = temp[i]

    def _rotate_E(self):
        """中间层E（与D同向）顺时针旋转90度"""
        # E层是上下之间的中间层，与D同向
        temp = [self.faces[Face.FRONT.value][1][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.FRONT.value][1][i] = self.faces[Face.LEFT.value][1][i]
            self.faces[Face.LEFT.value][1][i] = self.faces[Face.BACK.value][1][i]
            self.faces[Face.BACK.value][1][i] = self.faces[Face.RIGHT.value][1][i]
            self.faces[Face.RIGHT.value][1][i] = temp[i]

    def _rotate_S(self):
        """中间层S（与F同向）顺时针旋转90度"""
        # S层是前后之间的中间层，与F同向
        temp = [self.faces[Face.UP.value][1][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][1][i] = self.faces[Face.LEFT.value][2 - i][1]
            self.faces[Face.LEFT.value][2 - i][1] = self.faces[Face.DOWN.value][1][i]
            self.faces[Face.DOWN.value][1][i] = self.faces[Face.RIGHT.value][2 - i][1]
            self.faces[Face.RIGHT.value][2 - i][1] = temp[i]
