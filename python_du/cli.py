from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .renderer import RenderConfig, render_tree
from .scanner import scan


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python-du",
        description="Disk usage analyzer — scan a directory and print a visual size map.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="directory to scan (default: current directory)",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        default=4,
        help="maximum depth to display (default: 4)",
    )
    parser.add_argument(
        "-m",
        "--min-percent",
        type=float,
        default=0.5,
        help="hide entries smaller than this percentage (default: 0.5)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable colored output",
    )
    parser.add_argument(
        "--sort-alpha",
        action="store_true",
        help="sort entries alphabetically instead of by size",
    )
    parser.add_argument(
        "--scan-depth",
        type=int,
        default=None,
        help="maximum directory depth to scan (default: unlimited)",
    )
    parser.add_argument(
        "-L",
        "--follow-symlinks",
        action="store_true",
        help="follow symbolic links",
    )

    args = parser.parse_args(argv)
    target = Path(args.path)

    if not target.exists():
        print(f"python-du: error: '{target}' does not exist", file=sys.stderr)
        sys.exit(1)
    if not target.is_dir():
        print(f"python-du: error: '{target}' is not a directory", file=sys.stderr)
        sys.exit(1)

    tree = scan(target, max_depth=args.scan_depth, follow_symlinks=args.follow_symlinks)

    config = RenderConfig(
        max_depth=args.max_depth,
        min_percent=args.min_percent,
        use_color=not args.no_color and sys.stdout.isatty(),
        sort_by_size=not args.sort_alpha,
    )

    print(render_tree(tree, config))


if __name__ == "__main__":
    main()
