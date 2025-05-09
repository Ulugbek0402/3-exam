from file_manager import read


def generate_id(filename: str) -> int:
    data = read(filename=filename)
    if len(data) == 0:
        return 1
    else:
        return int(data[-1][0]) + 1

