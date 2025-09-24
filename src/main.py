from src.core.config import DATA_DIR
from src.core.flags.format_flag import FormatFlag
from src.core.flags.output_paths_flag import OutputPathsFlag
from src.core.flags.sub_langs_flag import SubLangsFlag
from src.core.flags.write_link import WriteLinkFlag
from src.core.flags.write_subs_flag import WriteSubsFlag
from src.core.runner import YTDLPRunner

def main():
    runner = YTDLPRunner()
    runner.add_flag(FormatFlag("best"))
    runner.add_flag(OutputPathsFlag(DATA_DIR))
    runner.add_flag(WriteLinkFlag())
    runner.add_flag(WriteSubsFlag())
    runner.add_flag(SubLangsFlag(["en", "ja"]))

    def print_line(line):
        print(f"{line}")

    result = runner.run(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
               on_output=print_line)

    print(f"Finished with code {result['return_code']}")

if __name__ == '__main__':
    main()
