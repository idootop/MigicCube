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
        """重置魔方到初始状态"""
        self.faces = [
            [[Color.YELLOW] * 3 for _ in range(3)],  # UP
            [[Color.WHITE] * 3 for _ in range(3)],  # DOWN
            [[Color.RED] * 3 for _ in range(3)],  # FRONT
            [[Color.ORANGE] * 3 for _ in range(3)],  # BACK
            [[Color.BLUE] * 3 for _ in range(3)],  # LEFT
            [[Color.GREEN] * 3 for _ in range(3)],  # RIGHT
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

        # 旋转次数映射表：根据 times 和 clockwise 计算实际旋转次数
        def get_turn_counts(times: int, clockwise: bool) -> tuple[int, int]:
            """
            获取主层和中层的旋转次数
            返回: (主层次数, 中层次数)
            """
            if not clockwise:
                times = -times

            if times == -2:
                return (2, 2)
            elif times == -1:
                return (3, 1)
            elif times == 1:
                return (1, 3)
            elif times == 2:
                return (2, 2)
            else:
                t = times % 4
                if t == 0:
                    return (0, 0)
                elif t == 3:
                    return (3, 1)
                else:
                    return (t, 4 - t if t < 4 else 0)

        t1, t2 = get_turn_counts(times, clockwise)

        if t1 == 0:
            return

        # 处理整体旋转
        if move == "x":
            # x = R + M' + L'
            self._repeat_move("R", t1)
            self._repeat_move("M", t2)
            self._repeat_move("L", t2)
        elif move == "y":
            # y = U + E' + D'
            self._repeat_move("U", t1)
            self._repeat_move("E", t2)
            self._repeat_move("D", t2)
        elif move == "z":
            # z = F + S + B'
            self._repeat_move("F", t1)
            self._repeat_move("S", t1)
            self._repeat_move("B", t2)
        # 处理双层操作
        elif move in "udlrfb":
            layer_map = {
                "r": ("R", "M", t1, t2),  # r = R + M'
                "l": ("L", "M", t1, t1),  # l = L + M
                "u": ("U", "E", t1, t2),  # u = U + E'
                "d": ("D", "E", t1, t1),  # d = D + E
                "f": ("F", "S", t1, t1),  # f = F + S
                "b": ("B", "S", t1, t2),  # b = B + S'
            }
            outer, middle, outer_times, middle_times = layer_map[move]

            self._repeat_move(outer, outer_times)
            self._repeat_move(middle, middle_times)
        # 处理基本操作和中层操作
        else:
            actual_times = times * 3 if not clockwise else times
            self._repeat_move(move, actual_times)

    def _repeat_move(self, move: str, times: int):
        """重复执行基本操作指定次数"""
        for _ in range(times % 4):
            self._execute_basic_move(move)

    def _execute_basic_move(self, move: str):
        """执行单次基本操作"""
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
        elif move == "M":
            self._rotate_M()
        elif move == "E":
            self._rotate_E()
        elif move == "S":
            self._rotate_S()
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
        moves = [m.value for m in Move]
        moves = random.choices(moves, k=moves_count)
        self.apply_moves(moves)
        return " ".join(moves)

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

    def _rotate_U(self):
        """上面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.UP)
        # 旋转相邻的边
        front_face = [self.faces[Face.FRONT.value][0][i] for i in range(3)]
        right_face = [self.faces[Face.RIGHT.value][0][i] for i in range(3)]
        back_face = [self.faces[Face.BACK.value][0][i] for i in range(3)]
        left_face = [self.faces[Face.LEFT.value][0][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.FRONT.value][0][i] = right_face[i]
            self.faces[Face.RIGHT.value][0][i] = back_face[i]
            self.faces[Face.BACK.value][0][i] = left_face[i]
            self.faces[Face.LEFT.value][0][i] = front_face[i]

    def _rotate_D(self):
        """下面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.DOWN)
        # 旋转相邻的边
        front_face = [self.faces[Face.FRONT.value][2][i] for i in range(3)]
        left_face = [self.faces[Face.LEFT.value][2][i] for i in range(3)]
        back_face = [self.faces[Face.BACK.value][2][i] for i in range(3)]
        right_face = [self.faces[Face.RIGHT.value][2][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.FRONT.value][2][i] = left_face[i]
            self.faces[Face.LEFT.value][2][i] = back_face[i]
            self.faces[Face.BACK.value][2][i] = right_face[i]
            self.faces[Face.RIGHT.value][2][i] = front_face[i]

    def _rotate_F(self):
        """前面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.FRONT)
        # 旋转相邻的边
        up_face = [self.faces[Face.UP.value][2][i] for i in range(3)]
        left_face = [self.faces[Face.LEFT.value][i][2] for i in range(3)]
        down_face = [self.faces[Face.DOWN.value][0][i] for i in range(3)]
        right_face = [self.faces[Face.RIGHT.value][i][0] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][2][i] = left_face[2 - i]
            self.faces[Face.LEFT.value][i][2] = down_face[i]
            self.faces[Face.DOWN.value][0][i] = right_face[2 - i]
            self.faces[Face.RIGHT.value][i][0] = up_face[i]

    def _rotate_B(self):
        """后面顺时针旋转90度"""
        # 旋转面
        self._rotate_face_clockwise(Face.BACK)
        # 旋转相邻的边
        left_face = [self.faces[Face.LEFT.value][i][0] for i in range(3)]
        up_face = [self.faces[Face.UP.value][0][i] for i in range(3)]
        right_face = [self.faces[Face.RIGHT.value][i][2] for i in range(3)]
        down_face = [self.faces[Face.DOWN.value][2][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.LEFT.value][2 - i][0] = up_face[i]
            self.faces[Face.DOWN.value][2][i] = left_face[i]
            self.faces[Face.RIGHT.value][2 - i][2] = down_face[i]
            self.faces[Face.UP.value][0][i] = right_face[i]

    def _rotate_L(self):
        """左面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.LEFT)
        # 旋转相邻的边
        up_face = [self.faces[Face.UP.value][i][0] for i in range(3)]
        back_face = [self.faces[Face.BACK.value][i][2] for i in range(3)]
        down_face = [self.faces[Face.DOWN.value][i][0] for i in range(3)]
        front_face = [self.faces[Face.FRONT.value][i][0] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][i][0] = back_face[2 - i]
            self.faces[Face.BACK.value][i][2] = down_face[2 - i]
            self.faces[Face.DOWN.value][i][0] = front_face[i]
            self.faces[Face.FRONT.value][i][0] = up_face[i]

    def _rotate_R(self):
        """右面顺时针旋转90度"""
        self._rotate_face_clockwise(Face.RIGHT)
        # 旋转相邻的边
        up_face = [self.faces[Face.UP.value][i][2] for i in range(3)]
        front_face = [self.faces[Face.FRONT.value][i][2] for i in range(3)]
        down_face = [self.faces[Face.DOWN.value][i][2] for i in range(3)]
        back_face = [self.faces[Face.BACK.value][i][0] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][i][2] = front_face[i]
            self.faces[Face.FRONT.value][i][2] = down_face[i]
            self.faces[Face.DOWN.value][i][2] = back_face[2 - i]
            self.faces[Face.BACK.value][i][0] = up_face[2 - i]

    def _rotate_M(self):
        """中间层M（与L同向）顺时针旋转90度"""
        # M层是左右之间的中间层，与L同向
        up_face = [self.faces[Face.UP.value][i][1] for i in range(3)]
        back_face = [self.faces[Face.BACK.value][i][1] for i in range(3)]
        down_face = [self.faces[Face.DOWN.value][i][1] for i in range(3)]
        front_face = [self.faces[Face.FRONT.value][i][1] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][i][1] = back_face[2 - i]
            self.faces[Face.BACK.value][i][1] = down_face[2 - i]
            self.faces[Face.DOWN.value][i][1] = front_face[i]
            self.faces[Face.FRONT.value][i][1] = up_face[i]

    def _rotate_E(self):
        """中间层E（与D同向）顺时针旋转90度"""
        # E层是上下之间的中间层，与D同向
        front_face = [self.faces[Face.FRONT.value][1][i] for i in range(3)]
        left_face = [self.faces[Face.LEFT.value][1][i] for i in range(3)]
        back_face = [self.faces[Face.BACK.value][1][i] for i in range(3)]
        right_face = [self.faces[Face.RIGHT.value][1][i] for i in range(3)]
        for i in range(3):
            self.faces[Face.FRONT.value][1][i] = left_face[i]
            self.faces[Face.LEFT.value][1][i] = back_face[i]
            self.faces[Face.BACK.value][1][i] = right_face[i]
            self.faces[Face.RIGHT.value][1][i] = front_face[i]

    def _rotate_S(self):
        """中间层S（与F同向）顺时针旋转90度"""
        # S层是前后之间的中间层，与F同向
        up_face = [self.faces[Face.UP.value][1][i] for i in range(3)]
        left_face = [self.faces[Face.LEFT.value][i][1] for i in range(3)]
        down_face = [self.faces[Face.DOWN.value][1][i] for i in range(3)]
        right_face = [self.faces[Face.RIGHT.value][i][1] for i in range(3)]
        for i in range(3):
            self.faces[Face.UP.value][1][i] = left_face[2 - i]
            self.faces[Face.LEFT.value][i][1] = down_face[i]
            self.faces[Face.DOWN.value][1][i] = right_face[2 - i]
            self.faces[Face.RIGHT.value][i][1] = up_face[i]
