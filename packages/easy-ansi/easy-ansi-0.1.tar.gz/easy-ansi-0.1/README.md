# Easy ANSI

Easy ANSI is a terminal framework API to give you an easy way to use colors,
cursor control movements, and line/box drawing. It is not meant as a
replacement to more full-featured frameworks
(such as [curses](https://docs.python.org/3/library/curses.html)
or [urwid](https://urwid.org/)),
but as a tool to quickly create nice-looking screens in your terminal window.
You can even create animations with the cursor controls.

You can find demo programs [here](https://gitlab.com/joeysbytes/easy-ansi/-/tree/master/demos).

## Table of Contents

* [Requirements](#requirements)
* [General Usage](#general-usage)
* [Quick Reference](#quick-reference)
  * [Screen Commands](#screen-commands)
  * [Cursor Commands](#cursor-commands)
  * [Standard Colors](#standard-colors)
  * [Attributes](#attributes)
  * [256 Color Palette](#256-color-palette)
  * [RGB Color Palette](#rgb-color-palette)
  * [Drawing Lines and Boxes](#drawing-lines-and-boxes)
* [Color Reference](#color-reference)
  * [Standard Color Reference](standard-color-reference)

## Requirements

* This library is not dependent on any operating system, but instead is
dependent on the capabilities of the terminal you use.
* The Windows command prompt and PowerShell prompt do not support ANSI
codes (as of this writing), and thus are not supported. You will find
that terminal programs for Windows work well (Cygwin, Git Bash, PuTTY, etc).

## General Usage

* All ANSI sequences come as either a command or a code (string). For
example, to clear the screen, you can call the *clear()* method, but
if you want to store the command to clear the screen, call the
*clear_code()* method instead.
* Certain ANSI sequences may not work as expected when combined with other
ANSI sequences. For example, mixing color palettes on the same line does
not work well. You should always visually check your application.
* Certain terminal settings can change the behavior of certain ANSI codes.
For example, many terminal emulators will display bright text as bold.
You will have to experiment with your terminal settings for best results.

## Quick Reference

### Screen Commands

```python
from easyansi import screen
```

| Method | Description | Parameters |
| --- | --- | --- |
| clear() | Clear the screen and move the cursor to 0, 0 | |
| clear_line(row) | Clear the line at the given row. The cursor will move to the beginning of the row cleared. | **row:** The row number to clear. |
| get_size() | Return the size of the terminal. If the system cannot determine the size of the terminal, a default size of 80 columns by 24 rows is returned. | |
| prnt(text) | A convenience method to print output to the screen without an ending newline character. | **text:** The text to output to the screen. |

### Cursor Commands

```python
from easyansi import cursor
```

| Method | Description | Parameters |
| --- | --- | --- |
| locate(x, y) | Move the cursor to the x, y coordinates given. The upper-left corner is 0, 0. | **x:** column<br />**y:** row |
| down(rows) | Move the cursor down a certain number of rows (default = 1). | **rows:** The number of rows to move the cursor down. |
| up(rows) | Move the cursor up a certain number of rows (default = 1). | **rows:** The number of rows to move the cursor up. |
| left(cols) | Move the cursor left a certain number of columns (default = 1). | **cols:** The number of columns to move the cursor left. |
| right(cols) | Move the cursor right a certain number of columns (default = 1). | **cols:** The number of columns to move the cursor right. |
| hide() | Hide the cursor. | |
| show() | Show the cursor. | |

### Standard Colors

See the color reference below.

```python
from easyansi import colors
```

| Method | Description | Parameters |
| --- | --- | --- |
| color(fg, bg) | Set the foreground and/or background color from the 16-color palette. | **fg:** Foreground color index.<br />**bg:** Background color index. |
| default(fg, bg) | Set the foreground and/or background color to the terminal default. | **fg:** Foreground color 0 (false) or 1 (true).<br />**bg:** Background color 0 (false) or 1 (true). |
| reset() | Reset the colors and attributes to terminal defaults. | |

### Attributes

```python
from easyansi import attributes
```

| Method | Description | Parameters |
| --- | --- | --- |
| normal()<br />bright()<br />dim() | Set the text intensity to one of normal, bright, or dim.<br />**NOTE:** Bright is often used to bold text. | |
| italic()<br />italic_off() | Set italic text on or off. | |
| underline()<br />underline_off() | Set underline text on or off. | |
| reverse()<br />reverse_off() | Set reverse text on or off. | |
| strikethrough()<br />strikethrough_off() | Set strike-through text on or off. | |
| blink()<br />blink_off() | Set blinking text on or off. | |
| conceal()<br />conceal_off() | Set concealed (hidden) text on or off.<br />**WARNING:** Do NOT use this for password or other sensitive fields. Your text is still available to be copied from the terminal. | |
| reset() | Reset the colors and attributes to terminal defaults. | |

### 256 Color Palette

See the color reference below.

```python
from easyansi import colors_256
```

| Method | Description | Parameters |
| --- | --- | --- |
| color(fg, bg) | Set the foreground and/or background color from the 256-color palette. | **fg:** Foreground color index.<br />**bg:** Background color index. |
| default(fg, bg) | Set the foreground and/or background color to the terminal default. | **fg:** Foreground color 0 (false) or 1 (true).<br />**bg:** Background color 0 (false) or 1 (true). |
| reset() | Reset the colors and attributes to terminal defaults. | |

### RGB Color Palette

```python
from easyansi import colors_rgb
```

| Method | Description | Parameters |
| --- | --- | --- |
| color(r, g, b, bg_r, bg_g, bg_b) | Set the foreground and/or background color to the provided RGB values. | **r:** The foreground red value (0-255).<br />**g:** The foreground green value (0-255).<br />**b:** The foreground blue value (0-255).<br />**bg_r:** The background red value (0-255).<br />**bg_g:** The background green value (0-255).<br />**bg_b:** The background blue value (0-255). |
| reset() | Reset the colors and attributes to terminal defaults. | |

### Drawing Lines and Boxes

```python
from easyansi.drawing import single
from easyansi.drawing import double
from easyansi.drawing import keyboard
```

| Drawing Style | Description |
| --- | --- |
| single | Single line drawing characters.
| double | Double line drawing characters.
| keyboard | Line drawing characters only from keyboard characters.

```python
from easyansi import drawing
```

| Method | Description | Parameters |
| --- | --- | --- |
| hline(length, char, style) | Draw a horizontal line to a given length, optionally composed of the given char(s) or of a given style. | **length:** Total length of the line.<br />**char:** The character(s) to use to build the line.<br />**style:** The line style to use to build the line. char will override the style. |
| vline(length, char, style) | Draw a vertical line to a given length, optionally composed of the given char(s) or of a given style. | **length:** Total length of the line.<br />**char:** The character(s) to use to build the line.<br />**style:** The line style to use to build the line. char will override the style. |
| box(width, height, style, top, bottom, left, right, top_left, top_right, bottom_left, bottom_right, top_bottom, left_right, all_corners, all_sides, all_chars) | Draw a box. Only width and height is required. This utilizes the hline and vline methods internally. | **width:** Width of the box<br />**height:** Height of the box.<br />**style:** The line style to use<br />**top:** The character(s) to use for the top line.<br />**bottom:** The character(s) to use for the bottom line.<br />**left:** The character(s) to use for the left line.<br />**right:** The character(s) to use for the right line.<br />**top_left:** The character to use for the top left corner.<br />**top_right:** The character to use for the top right corner.<br />**bottom_left:** The character to use for the bottom left corner.<br />**bottom_right:** The character to use for the bottom_right corner.<br />**top_bottom:** The character(s) to use for the top and bottom lines.<br />**left_right:** The character(s) to use for the left and right lines.<br />**all_corners:** The character to use for all the corners.<br />**all_sides:** The character(s) to use for all sides.<br />**all_chars:** The character to use for all drawing of the box. |

## Color Reference

### Standard Color Reference

| Color Index | Color Name |
| --- | --- |
| 0 | BLACK |
| 1 | RED |
| 2 | GREEN |
| 3 | YELLOW |
| 4 | BLUE |
| 5 | MAGENTA |
| 6 | CYAN |
| 7 | WHITE |
| 8 | BRIGHT_BLACK |
| 9 | BRIGHT_RED |
| 10 | BRIGHT_GREEN |
| 11 | BRIGHT_YELLOW |
| 12 | BRIGHT_BLUE |
| 13 | BRIGHT_MAGENTA |
| 14 | BRIGHT_CYAN |
| 15 | BRIGHT_WHITE |

![Screenshot of standard colors](./docs/images/color_chart.png)
