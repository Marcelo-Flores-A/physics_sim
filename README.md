# physics_sim

This repo contains a 2D physics simulator that is used to carry out experiments.
It is built with [Python Arcade](https://api.arcade.academy/). A ball falls under
gravity, bounces off the window borders, and spins. You tilt a bar to steer it.

## Features

- **Gravity and motion.** Velocity and position are integrated every frame, at a
  120 Hz update rate.
- **Border collisions.** The ball bounces off the floor and walls. Energy loss
  comes from elasticity, and surface friction slows it down.
- **Rotation.** The ball spins, and its angular speed changes when it touches a
  surface.
- **Circle vs. rotated rectangle collisions.** The ball collides with a bar that
  you control and can tilt to any angle. The collision uses a local-space
  closest-point test and reflects the ball's velocity off the collision normal.
- **Menus.** A main menu, a simulation screen and an options screen.

## Requirements

- Python 3.10 or newer
- [Arcade](https://pypi.org/project/arcade/) 3.x (listed in `requirements.txt`).
  Pillow, which is used to draw the two-colour ball texture, is installed
  automatically with Arcade.

## Installation

Clone the repository and create a virtual environment:

```bash
git clone <repo-url> physics_sim
cd physics_sim
python -m venv .venv
```

Activate the environment:

| Shell                  | Command                         |
| ---------------------- | ------------------------------- |
| Windows (PowerShell)   | `.venv\Scripts\Activate.ps1`    |
| Windows (cmd)          | `.venv\Scripts\activate.bat`    |
| macOS / Linux          | `source .venv/bin/activate`     |

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the simulation

The modules in `arcade_starter/` import each other as top-level modules
(`from physics import ...`). Run `main.py` as a script, not as a package:

```bash
cd arcade_starter
python main.py
```

Running `python arcade_starter/main.py` from the repo root also works.
`python -m arcade_starter.main` does **not**.

## Controls

### Main menu

| Key                  | Action                     |
| -------------------- | -------------------------- |
| `↑` / `W`            | Move selection up          |
| `↓` / `S`            | Move selection down        |
| `Enter` / left click | Select the highlighted item |
| `F11`                | Toggle fullscreen          |
| `Esc`                | Quit                       |

### Simulation

| Key   | Action                                           |
| ----- | ------------------------------------------------ |
| `A`   | Tilt the bar counter-clockwise (hold)            |
| `D`   | Tilt the bar clockwise (hold)                    |
| `R`   | Reset the ball and bar to their starting positions |
| `F11` | Toggle fullscreen                                |
| `Esc` | Return to the main menu                          |

When a simulation starts or is reset, the ball is dropped from the top centre of
the window with a small horizontal velocity. The bar sits level near the bottom.

### Options

The options screen shows information only. Press `Esc` to return to the menu.

## Configuration

To change the simulation parameters, edit `arcade_starter/constants.py`. The
options screen can't change them yet.

| Constant                        | Default    | Description                                       |
| ------------------------------- | ---------- | ------------------------------------------------- |
| `BALL_RADIUS`                   | `16`       | Ball radius (px)                                  |
| `OBJECT_INITIAL_SPEED_X`        | `100.0`    | Ball's horizontal speed on start/reset (px/s)     |
| `OBJECT_INITIAL_ANGULAR_SPEED`  | `500.0`    | Ball's spin on start/reset (deg/s)                |
| `GRAVITY`                       | `-980.0`   | Vertical acceleration (px/s²)                     |
| `OBJECT_MASS`                   | `1.0`      | Ball mass                                         |
| `OBJECT_ELASTICITY`             | `0.5`      | Fraction of speed kept after a bounce (0–1)       |
| `FRICTION_COEFFICIENT`          | `0.1`      | Friction applied when touching floor/walls        |
| `BAR_WIDTH` / `BAR_HEIGHT`      | `700` / `16` | Bar size (px)                                   |
| `BAR_SPEED`                     | `400.0`    | Bar tilt speed (deg/s)                            |
| `BAR_POSITION_Y`                | `200`      | Bar's vertical position (px)                      |
| `WIDTH` / `HEIGHT`              | `960` / `540` | Initial window size (px)                       |
| `TITLE`                         | `"Arcade Starter - Experiments"` | Window title                |

## Project structure

```
physics_sim/
├── arcade_starter/
│   ├── main.py         # Entry point: window, game states (menu/simulation/options), input routing
│   ├── simulation.py   # Creates the sprites, owns the simulation state, draws the HUD
│   ├── physics.py      # PhysicsObject, PlayerController and PhysicsEngine (integration + collisions)
│   └── constants.py    # Tunable physics, display and state constants
├── assets/             # Placeholder folders for fonts, images and sounds (currently empty)
├── requirements.txt
└── README.md
```

## How it works

1. `App` in `main.py` is the Arcade window. It calls `on_update` at 120 Hz and
   only advances the physics while the simulation screen is active.
2. `PhysicsSimulation.update()` calls `PhysicsEngine.update()` and passes in the
   keys currently held down.
3. On each update, `PhysicsEngine` does the following:
   - Resolves border collisions for the ball: bounce, friction and spin.
   - Checks whether the ball overlaps the bar. If it does,
     `handle_sprite_collision` moves the ball into the bar's rotated frame,
     finds the contact normal, reflects the velocity, applies elasticity and
     pushes the ball out of the bar.
   - Otherwise, it integrates the ball's motion and applies the bar's tilt input.

## Known limitations

- The options screen shows fixed text. Its values don't come from
  `constants.py`, so they can be out of sync with the actual settings.
- The bar can only tilt. It doesn't move sideways and doesn't collide with the
  window borders yet.
- Resizing the window updates the simulation bounds, but the HUD and menu are
  still positioned for the default 960×540 size.
