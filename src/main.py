from typing import List

from src.core.flags.base import BaseFlag
from src.core.runner import YTDLPRunner


class TestFormatFlag(BaseFlag):
    name = "format"

    def __init__(self, value: str = "best"):
        super().__init__(value, True)

    def validate(self):
        pass

    def to_args(self) -> List[str]:
        return ["--" + self.name, self.value]

def main():
    runner = YTDLPRunner()
    runner.add_flag(TestFormatFlag("best"))

    def print_line(line):
        print(f"{line}")

    result = runner.run(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
               on_output=print_line)

    print(f"Finished with code {result['return_code']}")

if __name__ == '__main__':
    main()
