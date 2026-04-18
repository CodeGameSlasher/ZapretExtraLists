from pathlib import Path
from dataclasses import dataclass


def get_all_content(path: Path) -> list[str]:
    return sorted({file.read_text().strip() for file in path.iterdir()})


@dataclass
class ValueList:
    directory: Path

    def __post_init__(self) -> None:
        self.domains: Path = self.directory.joinpath("domains")
        self.ips: Path = self.directory.joinpath("ips")


LISTS = ValueList(Path("exclude")), ValueList(Path("include"))

for value_list in LISTS:
    ips: list[str] = get_all_content(value_list.ips) if value_list.ips.exists() else []
    domains: list[str] = get_all_content(value_list.domains) if value_list.domains.exists() else []

    ips_path = value_list.directory.joinpath("ips.txt")
    if len(ips) > 0:
        ips_path.write_text("\n".join(ips))
    elif ips_path.exists():
        ips_path.unlink()

    domains_path = value_list.directory.joinpath("domains.txt")
    if len(domains) > 0:
        domains_path.write_text("\n".join(domains))
    elif domains_path.exists():
        domains_path.unlink()

    value_list.directory.joinpath("all.txt").write_text(
        "\n".join(sorted({*domains, *ips}))
    )
