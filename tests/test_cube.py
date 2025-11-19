"""
魔方核心功能测试
"""

import pytest

from cube import Cube


class TestCube:
    """魔方类测试"""

    def test_initial_state(self):
        """测试初始状态"""
        cube = Cube()
        assert cube.is_solved(), "新创建的魔方应该是已还原状态"

    def test_copy(self):
        """测试魔方拷贝"""
        cube1 = Cube()
        cube2 = cube1.copy()

        # 修改cube1不应该影响cube2
        cube1.apply_move("R")
        assert cube1.is_solved() == False, "cube1应该不再是还原状态"
        assert cube2.is_solved() == True, "cube2应该仍然是还原状态"

    def test_from_string(self):
        """测试从字符串创建魔方"""
        # 已还原状态的字符串表示（顺序：上、下、前、后、左、右）
        solved_state = "Y" * 9 + "W" * 9 + "R" * 9 + "O" * 9 + "B" * 9 + "G" * 9
        cube = Cube.from_string(solved_state)
        assert cube.is_solved(), "从已还原状态字符串创建的魔方应该是已还原的"

    def test_from_string_invalid_length(self):
        """测试无效长度的字符串"""
        with pytest.raises(ValueError, match="状态字符串长度必须为54"):
            Cube.from_string("WWW")

    def test_from_string_invalid_color(self):
        """测试无效颜色字符"""
        invalid_state = "X" * 54
        with pytest.raises(ValueError, match="无效的颜色字符"):
            Cube.from_string(invalid_state)

    def test_basic_moves(self):
        """测试基本转动操作"""
        cube = Cube()
        original_state = str(cube)

        # 测试所有基本面的顺时针旋转
        for face in ["U", "D", "F", "B", "L", "R"]:
            test_cube = Cube()
            test_cube.apply_move(face)
            assert str(test_cube) != original_state, f"{face} 应该改变魔方状态"

            # 旋转4次应该回到原状态
            test_cube.apply_move(face)
            test_cube.apply_move(face)
            test_cube.apply_move(face)
            assert str(test_cube) == original_state, f"{face} 旋转4次应该回到原状态"

    def test_counterclockwise_moves(self):
        """测试逆时针转动"""
        cube = Cube()
        original_state = str(cube)

        # 测试顺时针 + 逆时针 = 回到原状态
        for face in ["U", "D", "F", "B", "L", "R"]:
            test_cube = Cube()
            test_cube.apply_move(face)
            test_cube.apply_move(f"{face}'")
            assert str(test_cube) == original_state, f"{face} + {face}' 应该回到原状态"

    def test_double_moves(self):
        """测试180度旋转"""
        cube = Cube()
        original_state = str(cube)

        # U2 应该等于 U + U
        for face in ["U", "D", "F", "B", "L", "R"]:
            cube1 = Cube()
            cube2 = Cube()

            cube1.apply_move(f"{face}2")
            cube2.apply_move(face)
            cube2.apply_move(face)

            assert str(cube1) == str(cube2), f"{face}2 应该等于 {face} + {face}"

            # U2 + U2 应该回到原状态
            cube1.apply_move(f"{face}2")
            assert str(cube1) == original_state, f"{face}2 + {face}2 应该回到原状态"

    def test_double_layer_moves(self):
        """测试双层转动"""
        for face in ["u", "d", "f", "b", "l", "r"]:
            cube = Cube()
            original_state = str(cube)

            # 双层转动应该改变状态
            cube.apply_move(face)
            assert str(cube) != original_state, f"{face} 应该改变魔方状态"

            # 旋转4次应该回到原状态
            cube.apply_move(face)
            cube.apply_move(face)
            cube.apply_move(face)
            assert str(cube) == original_state, f"{face} 旋转4次应该回到原状态"

    def test_middle_layer_moves(self):
        """测试中层转动"""
        for middle in ["M", "E", "S"]:
            cube = Cube()
            original_state = str(cube)

            # 中层转动应该改变状态
            cube.apply_move(middle)
            assert str(cube) != original_state, f"{middle} 应该改变魔方状态"

            # 旋转4次应该回到原状态
            cube.apply_move(middle)
            cube.apply_move(middle)
            cube.apply_move(middle)
            assert str(cube) == original_state, f"{middle} 旋转4次应该回到原状态"

    def test_whole_cube_rotations(self):
        """测试整体旋转"""
        for rotation in ["x", "y", "z"]:
            cube = Cube()
            original_state = str(cube)

            # 整体旋转不应该改变已还原状态
            cube.apply_move(rotation)
            assert cube.is_solved(), f"{rotation} 不应该破坏已还原状态"

            # 旋转4次应该回到完全相同的状态
            cube.apply_move(rotation)
            cube.apply_move(rotation)
            cube.apply_move(rotation)
            assert str(cube) == original_state, f"{rotation} 旋转4次应该回到原状态"

    def test_custom_times(self):
        """测试自定义旋转次数"""
        cube1 = Cube()
        cube2 = Cube()

        # U3 应该等于 U'
        cube1.apply_move("U'")
        cube2.apply_move("U")
        cube2.apply_move("U")
        cube2.apply_move("U")
        assert str(cube1) == str(cube2), "U' 应该等于 U * 3"

        # U2' 应该等于 U2
        cube3 = Cube()
        cube4 = Cube()
        cube3.apply_move("U2'")
        cube4.apply_move("U2")
        assert str(cube3) == str(cube4), "U2' 应该等于 U2"

    def test_apply_moves_string(self):
        """测试应用空格分隔的转动序列"""
        cube = Cube()
        original_state = str(cube)

        # 应用一系列操作
        cube.apply_moves("R U R' U'")
        assert str(cube) != original_state, "应用转动序列后状态应该改变"

        # 应用逆操作序列应该回到原状态
        cube.apply_moves("U R U' R'")
        assert str(cube) == original_state, "应用逆操作序列应该回到原状态"

    def test_complex_algorithm(self):
        """测试复杂算法（Sexy Move）"""
        cube = Cube()
        original_state = str(cube)

        # Sexy Move: R U R' U' (执行6次回到原状态)
        for _ in range(6):
            cube.apply_moves("R U R' U'")

        assert str(cube) == original_state, "Sexy Move 执行6次应该回到原状态"

    def test_invalid_move(self):
        """测试无效操作"""
        cube = Cube()

        # 应该抛出异常
        with pytest.raises(ValueError, match="不支持的操作"):
            cube.apply_move("X")  # 大写X不存在（小写x是整体旋转）

    def test_string_representation(self):
        """测试字符串表示"""
        cube = Cube()
        state_str = str(cube)

        assert len(state_str) == 54, "状态字符串长度应该为54"
        assert all(c in "WYRGOB" for c in state_str), "所有字符都应该是有效的颜色字符"

        # 已还原状态应该有特定的模式
        assert state_str[:9] == "Y" * 9, "UP面应该全是黄色"
        assert state_str[9:18] == "W" * 9, "DOWN面应该全是白色"
        assert state_str[18:27] == "R" * 9, "FRONT面应该全是红色"
        assert state_str[27:36] == "O" * 9, "BACK面应该全是橙色"
        assert state_str[36:45] == "B" * 9, "LEFT面应该全是蓝色"
        assert state_str[45:54] == "G" * 9, "RIGHT面应该全是绿色"

    def test_complex_algorithm2(self):
        """测试复杂算法"""
        cube = Cube()
        moves = "U2 x' M2' u l L2 R' F2 f' S2' b2 b U z S f b b"
        cube.apply_moves(moves)
        assert str(cube) == "RYWWYRWYWYGGYWRRWYOOOOROBYYRRGROWOOWYBBGBBBBRGBGGGGOWB", (
            "魔方状态异常"
        )
