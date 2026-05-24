# Buffon's Needle

[Українська версія](README.uk.md)

Manim project for visualizing Buffon's needle experiment.

## Goal

This project is being built step by step to create a short mathematical animation about Buffon's needle experiment.

The experiment idea:

1. draw an infinite floor with equally spaced parallel lines;
2. throw random needles;
3. count how many needles intersect a line;
4. estimate the experimental probability

$$
P_{\mathrm{exp}} \approx \frac{K}{N}
$$

where:

- $N$ is the total number of thrown needles;
- $K$ is the number of needles that intersect a line;
- $P_{\mathrm{exp}}$ is the experimental probability of intersection.

For the special case $l=d$, the theoretical probability is

$$
P = \frac{2}{\pi}.
$$

The animation shows experimentally that

$$
\frac{2}{P_{\mathrm{exp}}} = \frac{2N}{K} \approx \pi,
$$

and then leads to

$$
P \approx \frac{2}{\pi}.
$$

## Current state

The project currently contains the main Manim scene for the experimental part of the video.

The scene:

- introduces an infinite floor with equally spaced parallel lines;
- draws long horizontal parallel lines that extend beyond the visible frame;
- shows the distance $d$ between neighboring lines;
- shows the special case $l=d$;
- demonstrates random needle throwing through random position and random angle;
- highlights whether a needle crosses a line;
- counts the total number of throws and crossings;
- shows a large simulated experiment;
- derives the visual relation between the experimental probability and $\pi$;
- ends with the transition question for the proof part.

## Main scene

The main scene is located in:

```text
buffon_scene.py
```

Scene class:

```text
BuffonNeedleExperimentScene
```

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
- `buffon_scene.py` — Manim scene for Buffon's needle experiment.
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

## Quick preview render

Use this command for a fast low-quality preview:

```bash
uv run manim -pql buffon_scene.py BuffonNeedleExperimentScene
```

Command options:

- `uv run` — run the command inside the project environment;
- `manim` — run Manim;
- `-p` — open the video after rendering;
- `-ql` — render in low quality for a fast preview;
- `buffon_scene.py` — file with the Manim scene;
- `BuffonNeedleExperimentScene` — scene class name.

## Final 4K render

Use this command for maximum quality:

```bash
uv run manim -qk buffon_scene.py BuffonNeedleExperimentScene
```

The rendered video will be saved in:

```text
media/videos/buffon_scene/2160p60/BuffonNeedleExperimentScene.mp4
```

## High-quality 1080p render

If 4K rendering is too slow, use:

```bash
uv run manim -qh buffon_scene.py BuffonNeedleExperimentScene
```

The rendered video will be saved in:

```text
media/videos/buffon_scene/1080p60/BuffonNeedleExperimentScene.mp4
```

## Generated files

Manim creates a `media/` folder automatically.

This folder contains generated videos and should not be committed to Git.

## What not to commit

Do not commit:

```text
.venv/
media/
__pycache__/
*.pyc
```

These files and folders should be listed in `.gitignore`.

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
git commit -m "Update README docs"
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
nothing to commit, working tree clean
```

## Next steps

1. Finish the experimental scene polish.
2. Render the scene in final quality.
3. Create the proof scene.
4. Connect the experiment and proof parts.
5. Add narration, sound, subtitles, and final editing.