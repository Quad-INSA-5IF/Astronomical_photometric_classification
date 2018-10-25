from typing import List, Callable, TypeVar

T = TypeVar('T')


def read_csv(file_path: str, has_header: bool, transform: Callable[[List[str]], T]) -> List[T]:
    csv_file = open(file_path, "r")

    if has_header:
        csv_file.readline()

    result = []
    for line in csv_file:
        parts = list(line.strip().split(','))
        obj = transform(parts)
        result.append(obj)

    return result