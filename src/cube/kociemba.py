import twophase.solver as sv

# 固定的颜色到面映射 (基于初始还原状态的定义)
# FRONT=红, LEFT=蓝, RIGHT=绿, UP=黄, DOWN=白, BACK=橙
COLOR_TO_FACE = {
    "R": "F",  # 红 -> Front
    "B": "L",  # 蓝 -> Left
    "G": "R",  # 绿 -> Right
    "Y": "U",  # 黄 -> Up
    "W": "D",  # 白 -> Down
    "O": "B",  # 橙 -> Back
}

# 标准的中心块颜色 (物理面 -> 应有的中心块颜色)
STANDARD_CENTERS = {
    "F": "R",  # FRONT 应该是红色中心
    "L": "B",  # LEFT 应该是蓝色中心
    "R": "G",  # RIGHT 应该是绿色中心
    "U": "Y",  # UP 应该是黄色中心
    "D": "W",  # DOWN 应该是白色中心
    "B": "O",  # BACK 应该是橙色中心
}

# 每个物理面的中心块位置 (每面第5个格子，索引4)
# 物理面顺序: FRONT(0), LEFT(1), RIGHT(2), UP(3), DOWN(4), BACK(5)
PHYSICAL_CENTER_POSITIONS = {
    "F": 0 * 9 + 4,  # FRONT 中心: 索引 4
    "L": 1 * 9 + 4,  # LEFT 中心: 索引 13
    "R": 2 * 9 + 4,  # RIGHT 中心: 索引 22
    "U": 3 * 9 + 4,  # UP 中心: 索引 31
    "D": 4 * 9 + 4,  # DOWN 中心: 索引 40
    "B": 5 * 9 + 4,  # BACK 中心: 索引 49
}

# 当前 cube_state 的面顺序到 URFDLB 顺序的映射
FACE_ORDER_MAP = {
    "U": 3,  # UP 在当前顺序的索引 3 (位置 27-35)
    "R": 2,  # RIGHT 在当前顺序的索引 2 (位置 18-26)
    "F": 0,  # FRONT 在当前顺序的索引 0 (位置 0-8)
    "D": 4,  # DOWN 在当前顺序的索引 4 (位置 36-44)
    "L": 1,  # LEFT 在当前顺序的索引 1 (位置 9-17)
    "B": 5,  # BACK 在当前顺序的索引 5 (位置 45-53)
}


def check_centers_standard(cube_state: str) -> bool:
    """检查中心块是否在标准位置"""
    for face, pos in PHYSICAL_CENTER_POSITIONS.items():
        if cube_state[pos] != STANDARD_CENTERS[face]:
            return False
    return True


def kociemba_solve(cube_state: str):
    """
    Kociemba 方法求解魔方

    cube_state: 54 字符的魔方状态字符串，顺序为 FRONT, LEFT, RIGHT, UP, DOWN, BACK
                颜色使用 R(红), B(蓝), G(绿), Y(黄), W(白), O(橙)

    注意: Kociemba 算法只支持标准操作 (U, R, F, D, L, B)，不支持改变中心块的操作。
          如果中心块不在标准位置，返回的解法会还原到"每面同色"状态，但可能不是初始还原状态。
    """
    # 检查中心块是否在标准位置
    centers_standard = check_centers_standard(cube_state)
    if not centers_standard:
        return None

    # 重新排列面的顺序: 从 FRONT,LEFT,RIGHT,UP,DOWN,BACK 到 U,R,F,D,L,B
    reordered = ""
    for face in "URFDLB":
        face_idx = FACE_ORDER_MAP[face]
        start = face_idx * 9
        end = start + 9
        reordered += cube_state[start:end]

    # 颜色映射: 使用固定映射转换为 URFDLB 面标识
    kociemba_state = "".join([COLOR_TO_FACE[c] for c in reordered])

    # 调用 Kociemba 求解
    solutions = sv.solve(kociemba_state, 20, 1)
    if "Error" in solutions:
        return None

    # 移除最后的步数统计 (如 "(17f)")
    solutions = " ".join(solutions.split(" ")[:-1])
    if not solutions:
        return ""

    # 转换格式: "U1 R3 F2" -> "UR'F2" (不带空格，兼容 Move.from_core)
    # Kociemba 格式: 1=顺时针90°, 2=180°, 3=逆时针90°
    converted = []
    for move in solutions.split():
        face = move[0]
        count = move[1] if len(move) > 1 else "1"
        if count == "1":
            converted.append(face)
        elif count == "2":
            converted.append(f"{face}2")
        elif count == "3":
            converted.append(f"{face}'")
    return "".join(converted)
