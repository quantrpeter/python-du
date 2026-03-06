# python-du

A disk usage analyzer that scans a directory and prints a visual tree map of folder sizes — right in your terminal.

## Example

![](https://github.com/quantrpeter/python-du/blob/main/image/Screenshot%20from%202026-03-06%2011-31-47.png?raw=true)

## Installation

```bash
pip install -e .
```

```
pip uninstall python-du
```

## Usage

```bash
python-du [path] [options]
```

If no path is given, the current directory is scanned.

### Options

| Flag | Description |
|------|-------------|
| `-d`, `--max-depth N` | Maximum tree depth to display (default: 4) |
| `-m`, `--min-percent N` | Hide entries smaller than N% of total (default: 0.5) |
| `--no-color` | Disable colored output |
| `--sort-alpha` | Sort alphabetically instead of by size |
| `--scan-depth N` | Limit how deep the filesystem scan goes (default: unlimited) |
| `-L`, `--follow-symlinks` | Follow symbolic links |

### Examples

Scan the current directory with defaults:

```bash
python-du
```

Scan `/var/log` showing only entries above 5%, two levels deep:

```bash
python-du /var/log -d 2 -m 5
```

Pipe to a file (automatically disables color):

```bash
python-du /home > usage-report.txt
```

## Publishing to PyPI

```
pip install build twine
python -m build
twine upload dist/*
```

When prompted, use `__token__` as the username and your PyPI API token as the password.

To skip the prompt, create a `~/.pypirc` file:

```ini
[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

> **Note:** Bump the `version` in `pyproject.toml` before each upload — PyPI rejects duplicate version numbers.

## Requirements

- Python >= 3.9
- No external dependencies
