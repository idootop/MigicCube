"""
魔方核心功能测试
"""

from cube import Cube
from cube.cube import INITIAL_CUBE_STR


class TestCube:
    """魔方类测试"""

    def test_initial_state(self):
        """测试初始状态"""
        cube = Cube()
        assert cube.is_solved(), "新创建的魔方应该是已还原状态"

    def test_from_string(self):
        """测试从字符串创建魔方"""
        cube = Cube(INITIAL_CUBE_STR)
        assert cube.is_solved(), "从已还原状态字符串创建的魔方应该是已还原的"

    def test_string_representation(self):
        """测试字符串表示"""
        cube = Cube()
        state_str = str(cube)

        assert len(state_str) == 54, "状态字符串长度应该为54"
        assert all(c in "WYRGOB" for c in state_str), "所有字符都应该是有效的颜色字符"

        # 已还原状态应该有特定的模式
        assert state_str[:9] == "R" * 9, "FRONT面应该全是红色"
        assert state_str[9:18] == "B" * 9, "BACK面应该全是蓝色"
        assert state_str[18:27] == "G" * 9, "LEFT面应该全是绿色"
        assert state_str[27:36] == "Y" * 9, "RIGHT面应该全是黄色"
        assert state_str[36:45] == "W" * 9, "UP面应该全是白色"
        assert state_str[45:54] == "O" * 9, "DOWN面应该全是橙色"

    def test_complex_algorithm(self):
        """测试复杂算法"""
        cube = Cube()
        ops = "U2 x' M2' u l L2 R' F2 f' S2' b2 b U z S f b b"
        cube.moves(ops)
        assert str(cube) == "OOOOROBYYYBBGBBBBRGBGGGGOWBRYWWYRWYWYGGYWRRWYRRGROWOOW", (
            "魔方状态异常"
        )

    def test_solve(self):
        """测试解决魔方"""
        cube = Cube()
        cube.scramble()
        cube.solve()
        assert cube.is_solved(), "魔方应该已经解决"

