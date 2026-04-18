from pathlib import Path
from dataclasses import dataclass


class DirectoryNotFoundError(Exception):
    def __init__(self, directory: Path) -> None:
        super().__init__(f"Directory {directory} wasn't found!")


def get_all_content(path: Path) -> list[str]:
    return sorted({file.read_text().strip() for file in path.iterdir()})


@dataclass
class List:
    directory: Path

    def __post_init__(self) -> None:
        self.domains: Path = self.directory.joinpath("domains")
        self.ips: Path = self.directory.joinpath("ips")

        if not self.domains.is_dir():
            raise DirectoryNotFoundError(self.domains)
        if not self.ips.is_dir():
            raise DirectoryNotFoundError(self.ips)


LISTS = List(Path("exclude")), List(Path("include"))

for list in LISTS:
    domains = get_all_content(list.domains)
    list.directory.joinpath("domains.txt").write_text("\n".join(domains))
    ips = get_all_content(list.ips)
    list.directory.joinpath("ips.txt").write_text("\n".join(ips))

    list.directory.joinpath("all.txt").write_text('\n'.join(sorted({*domains, *ips})))
