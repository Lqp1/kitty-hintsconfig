kitty-hintsconfig
=================

# Summary

Helps you build a centralized config for [kitty](https://sw.kovidgoyal.net/kitty/) regarding markers and hints.

There are two lists of items:
- A list of regular expressions and marker number for markers.
- A list of regular expressions and actions for hints.

Goal was mainly to be able to handle many hints or markers using only one
mapping.

# Setup

Clone this project; easiest is to clone in kitty config folder:
```
cd ~/.config/kitty
git clone https://github.com/Lqp1/kitty-hintsconfig
```
Prior to its usage, install all dependencies:
```
pip install --user -r requirements.txt
```

## Markers

Marker regular expressions are case insensitive.
You may need to set the colors for the 3 markers slot as you wish in your kitty
configuration:
```
mark1_background green
mark2_background orange
mark3_background red
```

To use this tool to read markers, you can setup a mapping to toggle its usage:
```
map f1 toggle_marker function kitty-hintsconfig/kitty-hintsconfig.py
```

For each marker, you should define a `regexp` which is Python regexp, and a
`marker` which is the marker number you want to associate.

## Hints

Hints regular expressions are case sensitive.

You'll need to add a mapping to open this script:
```
map ctrl+shift+o kitten hints --customize-processing ~/.config/kitty/kitty-hintsconfig/kitty-hintsconfig.py
```

For each hint, you should define a `regexp` which is Python regexp, and an
action which can either be:
- `link`: to open a link in your browser
- `process`: to spawn a process

For the action, `{}` will be substituted by the first group defined in the
regexp.

# Config

There is a built in default config, which can be used for testing. For actual
usage, create a `~/.config/kitty/hints.yaml` file to make your own config. There
is an example at the top of this repository.
