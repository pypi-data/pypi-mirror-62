# Multiselection

[![PyPI](https://img.shields.io/pypi/v/jupyter-multiselection)](https://pypi.org/project/jupyter-multiselection/)

This nbextension allows to select occurences of the selected text in the currently active cell.

## Installation

First, install `jupyter_multiselection` using pip:

    pip install jupyter-multiselection

Next, install the nbextension using jupyter:
    
    jupyter nbextension install --py jupyter_multiselection

Finally, enable the nbextension:

    jupyter nbextension enable multiselection/multiselection

## Usage

Select a word or section of text in edit mode and other occurences of the selection will be highlighted.

![Highlight](https://gitlab.com/chdudek/jupyter_multiselection/-/raw/master/multiselection1.gif)

Use the select next hotkey (default `Ctrl+m`) to select the next occurence of the selection. To select all occurences use the select all hotkey (default: 'Ctrl+Alt+m').

![Highlight](https://gitlab.com/chdudek/jupyter_multiselection/-/raw/master/multiselection2.gif)


## Options

- `highlight` - If `true`, all occurences of the selected word will be highlighted (default: `true`).
- `wrapcell` - If `true`, after the last occurence in the cell the next selection will start from the beginning (default: `true`).
- `nextHotkey` - Hotkey to select the next occurence (default: `Ctrl+m`).
- `allHotkey` - Hotkey to select all occurences (default: `Ctrl+Alt+m`).

## TODO

- [ ] Multiselection across all cells
- [ ] Split multi-line selection into multiple selections


## History

- @chdudek (Feb 29 2020): Inital release 
