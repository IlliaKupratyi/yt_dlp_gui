from typing import List

from src.core.config import DATA_DIR
from src.core.flags.base import BaseFlag
from src.core.flags.output_paths_flag import OutputPathsFlag
from src.core.runner import YTDLPRunner


class TestFormatFlag(BaseFlag):
    name = "format"

    def __init__(self, value: str = "best"):
        super().__init__(value, True)

    def _validate(self):
        pass

    def to_args(self) -> List[str]:
        return ["--" + self.name, self.value]

def main():
    runner = YTDLPRunner()
    runner.add_flag(TestFormatFlag("best"))
    runner.add_flag(OutputPathsFlag(DATA_DIR))

    def print_line(line):
        print(f"{line}")

    result = runner.run(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
               on_output=print_line)

    print(f"Finished with code {result['return_code']}")

if __name__ == '__main__':
    main()
