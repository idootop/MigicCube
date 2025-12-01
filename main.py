#!/usr/bin/env python3


import sys

from cube import Cube


def solve_cube(state: str):
    # 验证输入
    if len(state) != 54:
        print(f"❌ 错误: 魔方状态字符串长度应该为54，当前长度为{len(state)}")
        return

    valid_colors = set("RBGYWOX")  # 增加 X 作为可能的未知颜色占位符
    invalid_chars = set(state.upper()) - valid_colors
    if invalid_chars:
        print(f"❌ 错误: 包含无效字符: {', '.join(invalid_chars)}")
        print("   有效字符: R(红), B(蓝), G(绿), Y(黄), W(白), O(橙)")
        return

    try:
        print("=" * 60)
        print("🎲 开始求解魔方...")
        print("=" * 60)

        # 创建魔方实例
        cube = Cube(state)

        # 可视化初始状态
        print("\n📊 初始魔方状态:")
        cube.visualize()

        # 检查是否已还原
        if cube.is_solved():
            print("✅ 魔方已经是还原状态，无需求解！")
            return

        # 求解魔方
        solution = cube.solve()

        # 可视化还原后的状态
        print("\n📊 还原后魔方状态:")
        cube.visualize()

        # 验证是否成功还原
        if cube.is_solved():
            # 打印解决方案
            solution.print()
            solution.print_ops()
        else:
            print("⚠️  魔方未完全还原，可能存在问题")

    except Exception as e:
        print(f"❌ 求解过程出错: {e}")
        import traceback

        traceback.print_exc()


def main():
    """主函数"""
    if len(sys.argv) < 2:
        # 如果没有提供参数，使用默认示例
        print("""
魔方求解脚本

用法:
    python main.py <魔方状态字符串>

示例:
    python main.py "ggybgrrrybwwborgybbowyrygbyyyoowgrrrwwrgywowgbbooboogw"

魔方状态字符串格式:
    54个字符，表示6个面的颜色，每个面9个块
    颜色字符: R(红), B(蓝), G(绿), Y(黄), W(白), O(橙)
    顺序: FRONT(9) + LEFT(9) + RIGHT(9) + UP(9) + DOWN(9) + BACK(9)
""")
        exit(1)

    # 开始求解
    state = sys.argv[1]
    solve_cube(state)


if __name__ == "__main__":
    main()


# uv run main.py "wbrybygryywbbwoyowwgorywbyygrbboorrgogobrggwbwwoggyror"
