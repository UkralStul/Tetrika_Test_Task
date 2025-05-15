def merge_intervals(intervals):
    """Объединение пересекающихся интервалов"""
    intervals.sort()  # Сортируем интервалы по началу
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def intersect_intervals(intervals1, intervals2):
    """Нахождение пересечения двух списков интервалов"""
    i, j = 0, 0
    result = []
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]
        start = max(start1, start2)
        end = min(end1, end2)
        if start < end:  # Если пересекаются
            result.append([start, end])
        if end1 < end2:
            i += 1
        else:
            j += 1
    return result


def intervals_to_pairs(intervals):
    """Преобразование списка в пары [start, end]"""
    return [[intervals[i], intervals[i + 1]] for i in range(0, len(intervals), 2)]


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_intervals = intervals_to_pairs(intervals['lesson'])
    pupil_intervals = merge_intervals(intervals_to_pairs(intervals['pupil']))
    tutor_intervals = merge_intervals(intervals_to_pairs(intervals['tutor']))

    common_intervals = intersect_intervals(pupil_intervals, tutor_intervals)
    lesson_common_intervals = intersect_intervals(lesson_intervals, common_intervals)

    total_time = sum(end - start for start, end in lesson_common_intervals)
    return total_time


# Тесты
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117},
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513,
                             1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009,
                             1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773,
                             1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                             1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577},
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565},
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print("Все тесты пройдены!")
