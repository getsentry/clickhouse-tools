import click
import os
from typing import Any
import structlog



plugin_folder = os.path.dirname(__file__)


class ClickhouseToolsCLI(click.MultiCommand):
    def list_commands(self, ctx: Any) -> list[str]:
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                rv.append(filename[:-3].replace("_", "-"))
        rv.sort()
        return rv
    
    def get_command(self, ctx: Any, name: str) -> click.Command:
        actual_command_name = name.replace("-", "_")
        ns: dict[str, click.Command] = {}
        fn = os.path.join(plugin_folder, actual_command_name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns[actual_command_name]

@click.command(cls=ClickhouseToolsCLI)
def main() -> None:
    pass

