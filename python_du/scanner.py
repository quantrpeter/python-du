from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DirNode:
    """Represents a directory and its computed disk usage."""

    path: Path
    own_size: int = 0  # size of files directly in this dir
    total_size: int = 0  # recursive total including children
    children: list[DirNode] = field(default_factory=list)
    file_count: int = 0
    error: str | None = None

    @property
    def name(self) -> str:
        return self.path.name or str(self.path)


def scan(root: Path, *, max_depth: int | None = None, follow_symlinks: bool = False) -> DirNode:
    """Walk *root* and return a tree of DirNode objects with computed sizes."""
    return _scan_dir(root.resolve(), depth=0, max_depth=max_depth, follow_symlinks=follow_symlinks)


def _scan_dir(
    path: Path,
    *,
    depth: int,
    max_depth: int | None,
    follow_symlinks: bool,
) -> DirNode:
    node = DirNode(path=path)

    try:
        entries = sorted(os.scandir(path), key=lambda e: e.name)
    except PermissionError:
        node.error = "permission denied"
        return node
    except OSError as exc:
        node.error = str(exc)
        return node

    for entry in entries:
        try:
            if entry.is_symlink() and not follow_symlinks:
                continue

            if entry.is_file(follow_symlinks=follow_symlinks):
                try:
                    node.own_size += entry.stat(follow_symlinks=follow_symlinks).st_size
                    node.file_count += 1
                except OSError:
                    pass

            elif entry.is_dir(follow_symlinks=follow_symlinks):
                if max_depth is not None and depth >= max_depth:
                    child = _shallow_size(Path(entry.path))
                else:
                    child = _scan_dir(
                        Path(entry.path),
                        depth=depth + 1,
                        max_depth=max_depth,
                        follow_symlinks=follow_symlinks,
                    )
                node.children.append(child)
        except OSError:
            pass

    node.total_size = node.own_size + sum(c.total_size for c in node.children)
    return node


def _shallow_size(path: Path) -> DirNode:
    """Get total size of a directory without building a child tree."""
    node = DirNode(path=path)
    total = 0
    fcount = 0
    try:
        for dirpath, _dirnames, filenames in os.walk(path):
            for fname in filenames:
                try:
                    total += os.path.getsize(os.path.join(dirpath, fname))
                    fcount += 1
                except OSError:
                    pass
    except PermissionError:
        node.error = "permission denied"
    node.own_size = total
    node.total_size = total
    node.file_count = fcount
    return node
