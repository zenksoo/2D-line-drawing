import tomllib

class GridConfig:
    def __init__(self, width: int, height: int,
                 grid_size: int, color: int) -> None:
        self.w: int = width
        self.h: int = height
        self.grid_size: int = grid_size
        self.color: int = color

    @staticmethod
    def _from_file(file: str) -> "GridConfig":
        with open(file, 'rb') as f:
            config = tomllib.load(f)

        return GridConfig(**config["grid"])



