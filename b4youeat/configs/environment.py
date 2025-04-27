import enum
import logging
import os
from typing import Final


log = logging.getLogger(__name__)

ENV_VAR: Final[str] = "PYENV"


@enum.unique
class Environment(enum.Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"


def _get_config_var(var_name: str, fallback: str) -> str:
    var = os.environ.get(var_name, None)

    if var is None:
        log.warning(f"{var_name} is not set, falling back to {fallback}.")
        return fallback.lower()

    var = var.lower()
    log.info(f"{var_name} is {var}")
    return var


# ----- Environment ----- #


def _get_environment() -> Environment:
    return Environment(_get_config_var(ENV_VAR, Environment.LOCAL.value))


ENVIRONMENT: Final[Environment] = _get_environment()


def is_prod_environment() -> bool:
    return (ENVIRONMENT == Environment.PROD)

