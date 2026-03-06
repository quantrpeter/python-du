from __future__ import annotations

import shutil
from dataclasses import dataclass

from .scanner import DirNode

BLOCK_CHARS = " ░▒▓█"
BAR_COLORS = {
    "red": "\033[91m",
    "yellow": "\033[93m",
    "green": "\033[92m",
    "cyan": "\033[96m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "white": "\033[97m",
}
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"

PALETTE = ["blue", "cyan", "green", "yellow", "magenta", "red"]

TREE_PIPE = "│   "
TREE_TEE = "├── "
TREE_BEND = "└── "
TREE_BLANK = "    "


def format_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(size) < 1024:
            if unit == "B":
                return f"{size} B"
            return f"{size:.1f} {unit}"
        size /= 1024  # type: ignore[assignment]
    return f"{size:.1f} PB"


@dataclass
class RenderConfig:
    max_depth: int = 4
    min_percent: float = 0.5
    bar_width: int | None = None  # auto-detect from terminal
    use_color: bool = True
    sort_by_size: bool = True
    show_percent: bool = True


def render_tree(root: DirNode, config: RenderConfig | None = None) -> str:
    cfg = config or RenderConfig()
    term_width = shutil.get_terminal_size((80, 24)).columns
    bar_width = cfg.bar_width or max(20, min(50, term_width - 60))
    lines: list[str] = []

    total = root.total_size or 1
    label_col = (cfg.max_depth + 1) * 4 + 24

    header = f"{BOLD}{root.name}{RESET}" if cfg.use_color else root.name
    lines.append(f"{header}  [{format_size(root.total_size)}]")
    lines.append("")

    _render_node(root, lines, cfg, bar_width, total, prefix="", depth=0, color_idx=0, label_col=label_col)

    lines.append("")
    lines.append(_summary_line(root, cfg))
    return "\n".join(lines)


def _render_node(
    node: DirNode,
    lines: list[str],
    cfg: RenderConfig,
    bar_width: int,
    root_total: int,
    prefix: str,
    depth: int,
    color_idx: int,
    label_col: int,
) -> None:
    children = node.children
    if cfg.sort_by_size:
        children = sorted(children, key=lambda c: c.total_size, reverse=True)

    own_files_size = node.own_size
    entries: list[tuple[str, int, int, DirNode | None]] = []
    for child in children:
        pct = (child.total_size / root_total * 100) if root_total else 0
        if pct >= cfg.min_percent or depth < 1:
            entries.append((child.name, child.total_size, _count_files(child), child))

    if own_files_size > 0:
        pct = (own_files_size / root_total * 100) if root_total else 0
        if pct >= cfg.min_percent or depth < 1:
            entries.append(("<files>", own_files_size, node.file_count, None))

    for i, (name, size, fcount, child_node) in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = TREE_BEND if is_last else TREE_TEE
        child_prefix = TREE_BLANK if is_last else TREE_PIPE

        pct = (size / root_total * 100) if root_total else 0
        bar = _make_bar(pct, bar_width, PALETTE[(color_idx + i) % len(PALETTE)], cfg.use_color)

        size_str = format_size(size)
        pct_str = f" ({pct:5.1f}%)" if cfg.show_percent else ""
        files_str = f" [{fcount:,} {'file' if fcount == 1 else 'files'}]" if fcount else ""

        if cfg.use_color and child_node is None:
            name_str = f"{DIM}{name}{RESET}"
        else:
            name_str = name

        visible_len = len(prefix) + len(connector) + len(name)
        padding = max(1, label_col - visible_len)
        lines.append(f"{prefix}{connector}{name_str}{' ' * padding}{size_str:>10s}{pct_str}  {bar}{files_str}")

        if child_node and depth < cfg.max_depth:
            _render_node(
                child_node,
                lines,
                cfg,
                bar_width,
                root_total,
                prefix=prefix + child_prefix,
                depth=depth + 1,
                color_idx=color_idx + i,
                label_col=label_col,
            )


def _make_bar(pct: float, width: int, color: str, use_color: bool) -> str:
    filled = int(pct / 100 * width)
    filled = max(0, min(filled, width))

    if use_color:
        c = BAR_COLORS.get(color, "")
        bar = f"{c}{'█' * filled}{RESET}{'░' * (width - filled)}"
    else:
        bar = "█" * filled + "░" * (width - filled)
    return f"▕{bar}▏"


def _summary_line(root: DirNode, cfg: RenderConfig) -> str:
    total_files = _count_files(root)
    total_dirs = _count_dirs(root)
    size_str = format_size(root.total_size)
    summary = f"Total: {size_str}  |  {total_dirs} directories, {total_files} files"
    if cfg.use_color:
        return f"{DIM}{summary}{RESET}"
    return summary


def _count_files(node: DirNode) -> int:
    return node.file_count + sum(_count_files(c) for c in node.children)


def _count_dirs(node: DirNode) -> int:
    return len(node.children) + sum(_count_dirs(c) for c in node.children)
