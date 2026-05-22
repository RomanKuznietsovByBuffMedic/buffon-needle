# Buffon Needle Manim

[Українська версія](README.uk.md)

This is a Manim project for creating a mathematical video about Buffon's needle problem.

The goal of the project is to visualize:

- random needle drops;
- intersections with parallel lines;
- the experimental estimate of \(\pi\);
- the probability formula behind Buffon's needle.

## Project status

This project is currently in the setup and experimentation stage.

## Requirements

System dependencies:

- Python
- uv
- ffmpeg
- cairo
- pango

On Arch Linux:

```bash
sudo pacman -S --needed python uv ffmpeg cairo pango
```

## Setup

After cloning the repository, run:

```bash
uv sync
```

This creates or updates the local virtual environment `.venv` and installs the dependencies from `uv.lock`.

## Render

Example test render:

```bash
uv run manim -pql main.py TestCircle
```

Options:

```text
-p   open preview after rendering
-q l low quality, fast render
```

## Project structure

```text
buffon-needle/
├─ .venv/              # local virtual environment, not committed
├─ .vscode/            # VS Code project settings
├─ main.py             # Manim scenes
├─ pyproject.toml      # project metadata and dependencies
├─ uv.lock             # locked dependency versions
├─ README.md           # English project description
├─ README.uk.md        # Ukrainian project description
└─ media/              # rendered videos, not committed
```

## Notes

Do not commit:

```text
.venv/
media/
*.mp4
```

The repository should contain source code, configuration files, and dependency lock files only.