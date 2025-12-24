#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "click >=8.3.1, <8.4",
#   "dycw-utilities >=0.172.3, <0.173",
#   "pytest-xdist >=3.8.0, <3.9",
#   "rich >=14.2.0, <14.3",
#   "typed-settings[attrs, click] >=25.3.0, <25.4",
# ]
# ///
from __future__ import annotations

from logging import getLogger

from click import command
from rich.pretty import pretty_repr
from typed_settings import EnvLoader, click_options, option, settings
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

_LOGGER = getLogger(__name__)


@settings
class Settings:
    dummy: bool = option(default=False, help="Dummy flag")


@command(**CONTEXT_SETTINGS)
@click_options(Settings, [EnvLoader("")], show_envvars_in_help=True)
def main(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=_LOGGER)
    _LOGGER.info(
        strip_and_dedent("""
            Running with settings:
            %s
        """),
        pretty_repr(settings),
    )


if __name__ == "__main__":
    main()
