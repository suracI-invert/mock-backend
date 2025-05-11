def convert_level(level: int) -> str:
    match level:
        case 1:
            return "A1"
        case 2:
            return "A2"
        case 3:
            return "B1"
        case 4:
            return "B2"
        case 5:
            return "C1"
        case 6:
            return "C2"
        case _:
            raise ValueError(f"Invalid level {level}")
