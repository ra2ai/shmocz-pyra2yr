# pyra2yr

Python interface for ra2yrcpp.

## Installation

### Method 1: Install pre-built wheel using pip

Install a pre-built wheel:
```bash
pip install -U https://github.com/shmocz/pyra2yr/releases/download/v0.3.0/pyra2yr-0.3.0-py3-none-any.whl
```

### Method 2: Install with poetry

TODO

## Setup

Build the the following images with their default names from the repository root:

```bash
docker build -f docker/vnc.Dockerfile    -t shmocz/vnc:latest            ./
docker build -f docker/tunnel.Dockerfile -t shmocz/pycncnettunnel:latest ./
docker build -f docker/Dockerfile        -t shmocz/pyra2yr:latest        ./
```

Docker Compose is required to launch games. The launcher generates a separate `docker-compose.instance.yml` for each run.

Download and extract [ra2yrcpp](https://github.com/shmocz/ra2yrcpp/releases/download/latest/ra2yrcpp.zip) outside the game data folder. In the game configuration, set `dll_directory` to the folder that directly contains the extracted DLLs. Each game instance uses those DLLs in preference to same-named DLLs (case-insensitive) in the game data folder, without modifying any original game files.

If you are not using Syringe, patch `gamemd-spawn.exe` according to the [ra2yrcpp instructions](https://github.com/shmocz/ra2yrcpp#usage).

## Usage

See `pyra2yr/examples/basic_usage.py` files for example usage.

## Tests

In a suitable python environment, run:

```bash
python -m unittest
```

Various environment variables are accepted:

- `USE_SYRINGE` if defined, use Syringe instead of legacy spawner. Assumes `Syringe.exe` is in game data folder.
- `USE_X11` (Linux only) Use host X server instead of VNC by exposing `/tmp/.X11-unix` to container.
- `X11_SOCKET` (Linux only) is `USE_X11` is defined alternative path to X server socket.

> [!NOTE]
> Any value will enable a boolean setting, even values like `no`, `False` and `n`.

For example:

```bash
USE_SYRINGE=y USE_X11=y python -m unittest
```

Don't forget to modify `game_data_directory` in "pyra2yr/test_util.py" if your game data folder is not "../ra2yrcpp/maingame".
