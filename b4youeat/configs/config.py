import configparser
import os
from pathlib import Path
from typing import Any, Final, Optional

from configs.environment import ENVIRONMENT, Environment

class ConfigError(Exception):
    pass


def _create_parser() -> configparser.ConfigParser:
    return configparser.ConfigParser(
        strict=True,
        empty_lines_in_values=False,
        delimiters=("="),
        interpolation=configparser.ExtendedInterpolation(),
    )


class TrendsConfig:
    def __init__(
        self,
        *,
        environment: Environment,
        config_parser: configparser.ConfigParser,
    ):
        self._environment = environment
        self._config_parser = config_parser
        self._section = config_parser.default_section

    def get_optional(self, key: str, fallback: Any = None) -> Optional[Any]:
        return self._config_parser.get(self._section, key, fallback=fallback)

    def get_str(self, key: str, fallback: Optional[str] = None) -> str:
        value: Optional[str] = self.get_optional(key, None)
        if value is not None:
            assert isinstance(value, str)
            return value
        elif fallback is not None:
            return fallback
        else:
            raise ConfigError(f"Config {key} is not set")

    def get_int(self, key: str, fallback: Optional[int] = None) -> int:
        value: Optional[int] = self.get_optional(key, None)
        if value is not None:
            assert isinstance(value, int)
            return value
        elif fallback is not None:
            return fallback
        else:
            raise ConfigError(f"Config {key} is not set")


def get_config(*, environment: Environment) -> TrendsConfig:
    root = Path(__file__).parent.resolve()

    config_files = [
        os.path.join(root, "config.ini"),
        os.path.join(root, f"config.{environment.value}.ini"),
    ]

    parser = _create_parser()

    files_parsed = 0

    for config_file in config_files:
        if not os.path.isfile(config_file):
            continue
        if parser.read(config_file):
            files_parsed += 1
        else:
            raise ConfigError(f"Failed to read config file {config_file}")

    if files_parsed == 0:
        raise ConfigError("No config files were parsed.")

    if len(parser.sections()) > 0:
        raise ConfigError("Config files cannot contain multiple sections.")

    return TrendsConfig(environment=environment, config_parser=parser)


CONFIG: Final[TrendsConfig] = get_config(environment=ENVIRONMENT)
