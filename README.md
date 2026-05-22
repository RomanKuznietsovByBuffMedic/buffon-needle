# Buffon Needle

Manim project for visualizing Buffon's needle experiment.

## Goal

This project is being built step by step to create a short mathematical animation about Buffon's needle experiment.

The experiment idea:

1. draw parallel lines;
2. throw random needles;
3. count how many needles intersect a line;
4. estimate the experimental probability

$$
P \approx \frac{M}{N}
$$

where:

- $N$ is the total number of thrown needles;
- $M$ is the number of needles that intersect a line;
- $P$ is the experimental probability of intersection.

Then use this probability to estimate $\pi$:

$$
\pi \approx \frac{2L}{dP}
$$

where:

- $L$ is the needle length;
- $d$ is the distance between neighboring parallel lines.

In the special case $L=d$:

$$
\pi \approx \frac{2N}{M}
$$

## Current state

The project currently contains the first Manim scene.

The scene:

- shows the title `Buffon's needle experiment`;
- draws several horizontal parallel lines;
- renders a basic Manim video;
- checks that the Manim setup works correctly.

Needles and intersection counting are not added yet.

## Project structure

```text
buffon-needle/
├── main.py
├── buffon_scene.py
├── README.md
├── README.uk.md
├── pyproject.toml
├── uv.lock
└── .gitignore
```

## Files

- `main.py` — basic Python test script.
- `buffon_scene.py` — Manim scene for the first part of the Buffon's needle animation.
- `pyproject.toml` — project configuration and dependencies.
- `uv.lock` — locked dependency versions.
- `README.uk.md` — Ukrainian version of this README.

## Requirements

The project uses:

- Python;
- uv;
- Manim.

Dependencies are managed with `uv`.

## Run the Python test

```bash
uv run python main.py
```

Expected output:

```text
Hello from buffon-needle!
```

## Run the Manim scene

```bash
uv run manim -pql buffon_scene.py ParallelLinesScene
```

Command options:

- `-p` — open the video after rendering;
- `-q l` — render in low quality for a fast preview;
- `buffon_scene.py` — file with the Manim scene;
- `ParallelLinesScene` — scene class name.

## Generated files

Manim creates a `media/` folder automatically.

This folder contains generated videos and should not be committed to Git.

## Git notes

Check the current project state:

```bash
git status
```

Add changed files:

```bash
git add README.md README.uk.md
```

Create a commit:

```bash
git commit -m "Update README files"
```

Push changes to GitHub:

```bash
git push
```

Check that everything is clean:

```bash
git status
```

Expected result:

```text
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

## Next steps

1. Understand the current `buffon_scene.py` code.
2. Replace manual line coordinates with coordinates based on the distance `d`.
3. Add one needle.
4. Check whether the needle intersects a line.
5. Add many random needles.
6. Count intersections.
7. Show $P \approx M/N$ and estimate $\pi$.
