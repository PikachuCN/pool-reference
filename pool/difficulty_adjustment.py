from typing import Tuple, List

from chia.util.ints import uint64


def get_new_difficulty(
    recent_partials: List[Tuple[uint64, uint64]],
    number_of_partials_target: int,
    time_target: int,
    current_difficulty: uint64,
    current_time: uint64,
    min_difficulty: uint64,
) -> uint64:
    """
        给定来自给定农民的最后 number_of_partials_target（或我们拥有的总部分），返回新的难度，如果我们不想更新，则返回相同的难度。
    """

    # 如果我们还没有处理任何部分，保持当前（默认）难度
    if len(recent_partials) == 0:
        return current_difficulty

    # 如果我们最近更新了难度，请不要再次更新
    if any(difficulty != current_difficulty for timestamp, difficulty in recent_partials):
        return current_difficulty

    # 如果我们自上次部分以来真的很慢，请降低难度
    last_timestamp = recent_partials[0][0]
    if current_time - last_timestamp > 3 * 3600:
        return max(min_difficulty, current_difficulty // 5)

    if current_time - last_timestamp > 3600:
        return max(min_difficulty, uint64(int(current_difficulty // 1.5)))

    # 如果我们在这个难度下没有足够的部分，请不要更新
    if len(recent_partials) < number_of_partials_target:
        return current_difficulty

    # 最后，这是正常耕作和缓慢（或没有）增长的标准情况，适应新的难度
    time_taken = uint64(recent_partials[0][0] - recent_partials[-1][0])
    new_difficulty = uint64(int(current_difficulty * time_target / time_taken))
    return max(min_difficulty, new_difficulty)
