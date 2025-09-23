from typing import List

from src.core.flags.base import BaseFlag
from src.core.flags.format_list_flag import FormatListFlag
from src.core.runner import YTDLPRunner
from src.utils.format_lister import FormatLister


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
    # runner.add_flag(TestFormatFlag("best"))
    # runner.add_flag(OutputPathsFlag(DATA_DIR))
    format_lister = FormatLister()
    print(format_lister.get_formats("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    #def print_line(line):
     #   print(f"{line}")

    #result = runner.run(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
     #          on_output=print_line)

    #print(f"Finished with code {result['return_code']}")

if __name__ == '__main__':
    main()
