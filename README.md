![Static Badge](https://img.shields.io/badge/3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15%20-blue?label=Python)
![Static Badge](https://img.shields.io/badge/Linux%20-red?label=OS)

> [!WARNING]
> This software is unfinished. Do not see it as the final product.

# Tode
A modern, highly customizable, terminal text editor. Familiar keybindings and future IDE-level features. Perfect for beginners!

<img width="1849" height="978" alt="image" src="https://github.com/user-attachments/assets/60d0a228-955e-4bb2-b42e-22eca8cd61fe" />

> The image above was made after running `tode .` inside the `Tode/` directory.

## Install
The easiest way is with [pipx](https://pipx.pypa.io) or [uv](https://docs.astral.sh/uv/), which install Tode in its own isolated environment so it can't clash with other Python packages:

```bash
pipx install git+https://github.com/IdaxDiosMiguez/Tode.git
```

or

```bash
uv tool install git+https://github.com/IdaxDiosMiguez/Tode.git
```

Once Tode is on PyPI, this will become `pipx install tode`.

## Usage

Start the editor with:

```bash
tode [PATH]
```
> [!TIP]
> Run `tode --help` to see all available options.


# Development

```bash
git https://github.com/IdaxDiosMiguez/Tode.git
cd Tode
python -m venv .venv
source .venv/bin/activate
pip install -e .
tode
```
