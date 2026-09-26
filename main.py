import re
import sys
from dataclasses import dataclass
from pathlib import Path


def contains_any(directory: Path) -> bool:
    if directory.exists():
        try:
            next(directory.iterdir())
            return True
        except StopIteration:
            pass

    return False


def natural_key(value: str):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", value)
    ]


def get_all_content(path: Path) -> list[str]:
    result: set[str] = set()

    for file in path.iterdir():
        content = sorted({*file.read_text().splitlines()}, key=natural_key)
        file.write_text("\n".join(content), encoding="utf-8", newline="\n")

        result |= {*content}

    return sorted(result, key=natural_key)


@dataclass
class ValueList:
    directory: Path

    def __post_init__(self) -> None:
        self.domains: Path = self.directory.joinpath("domains")
        self.ips: Path = self.directory.joinpath("ips")

    def exists(self) -> bool:
        return contains_any(self.domains) or contains_any(self.ips)


LISTS = []

for folder in Path.cwd().iterdir():
    data_list = ValueList(folder)

    if data_list.exists():
        LISTS.append(data_list)

for value_list in LISTS:
    ips: list[str] = (
        get_all_content(value_list.ips) if contains_any(value_list.ips) else []
    )
    domains: list[str] = (
        get_all_content(value_list.domains) if contains_any(value_list.domains) else []
    )

    ips_path = value_list.ips.with_suffix(".txt")
    domains_path = value_list.domains.with_suffix(".txt")
    if domains_path.exists():
        domains_path.unlink()
    if ips_path.exists():
        ips_path.unlink()

    if len(ips) + len(domains) == 0:
        print(f"List {value_list.directory.stem} is empty")
        sys.exit()

    if len(ips) > 0 and len(domains) > 0:
        domains_path.write_text("\n".join(domains), encoding="utf-8", newline="\n")
        ips_path.write_text("\n".join(ips), encoding="utf-8", newline="\n")

    value_list.directory.joinpath("all.txt").write_text(
        "\n".join(sorted({*domains, *ips}, key=natural_key)),
        encoding="utf-8",
        newline="\n",
    )
