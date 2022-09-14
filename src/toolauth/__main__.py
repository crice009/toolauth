"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Toolauth."""


if __name__ == "__main__":
    main(prog_name="toolauth")  # pragma: no cover
