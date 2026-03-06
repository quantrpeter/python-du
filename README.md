# python-du

A disk usage analyzer that scans a directory and prints a visual tree map of folder sizes — right in your terminal.

## Example

```
$ python-du /usr -d 2 -m 2
usr  [60.2 GB]

├── share                             27.4 GB ( 45.6%)  ▕█████████░░░░░░░░░░░▏
│   └── ollama                            22.6 GB ( 37.5%)  ▕███████░░░░░░░░░░░░░▏
│       └── .ollama                           22.6 GB ( 37.5%)  ▕███████░░░░░░░░░░░░░▏
├── lib                               26.4 GB ( 43.8%)  ▕████████░░░░░░░░░░░░▏
│   ├── x86_64-linux-gnu                  11.7 GB ( 19.3%)  ▕███░░░░░░░░░░░░░░░░░▏
│   ├── arm-none-eabi                      2.7 GB (  4.5%)  ▕░░░░░░░░░░░░░░░░░░░░▏
│   ├── jvm                                2.1 GB (  3.5%)  ▕░░░░░░░░░░░░░░░░░░░░▏
│   ├── dotnet                             1.5 GB (  2.5%)  ▕░░░░░░░░░░░░░░░░░░░░▏
│   └── apache-netbeans                    1.3 GB (  2.2%)  ▕░░░░░░░░░░░░░░░░░░░░▏
├── local                              3.8 GB (  6.3%)  ▕█░░░░░░░░░░░░░░░░░░░▏
│   └── lib                                3.2 GB (  5.3%)  ▕█░░░░░░░░░░░░░░░░░░░▏
├── bin                                1.4 GB (  2.4%)  ▕░░░░░░░░░░░░░░░░░░░░▏
│   └── <files>                            1.4 GB (  2.4%)  ▕░░░░░░░░░░░░░░░░░░░░▏
└── <files>                           33.7 KB (  0.0%)  ▕░░░░░░░░░░░░░░░░░░░░▏

Total: 60.2 GB  |  46966 directories, 390046 files
```

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
