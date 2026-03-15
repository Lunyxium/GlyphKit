<p align="center">
  <img src="glyphkit.ico" alt="GlyphKit" width="300">
</p>
<h1 align="center">GlyphKit</h1>

<p align="center">
  A tiny, always-on-top Unicode palette for Windows.<br>
  Click a glyph. It's in your clipboard. Or already pasted.
</p>

<p align="center">
  <a href="https://github.com/Lunyxium/glyphkit/releases/latest"><img src="https://img.shields.io/github/v/release/Lunyxium/glyphkit?style=flat-square&color=2dd4bf" alt="Release"></a>
  <img src="https://img.shields.io/badge/platform-Windows%2011-0078D4?style=flat-square" alt="Windows 11">
  <img src="https://img.shields.io/github/license/Lunyxium/glyphkit?style=flat-square&_t=1" alt="License"> 
  <img src="https://img.shields.io/badge/dependencies-zero-2dd4bf?style=flat-square" alt="Zero dependencies">
</p>

<p align="center">
  Part of the <a href="https://github.com/stars/Lunyxium/lists/tools">Lunyxium Tools</a> collection.
</p>

---

<p align="center">
  <img src="media/glyphkit_app.gif" alt="GlyphKit in action" width="720">
</p>

## Why

Writing a formula that needs `∑` or `∂`? A doc where `½` looks cleaner than `1/2`, or `→` beats `-->`?  
Greek letters for a proof, `≈` instead of `~=`, currency symbols, arrows, fractions?

You know the drill: open the Windows character map. Lose focus. Scroll. Squint. Click. Copy. Alt-tab back. Paste. Repeat. For every single glyph.

Or you google it. Three tabs later you're reading the Wikipedia article on the Greek alphabet.

The floating touch keyboard and other tools exists, sure. Great for emoji. Finding `∑` or `⊕`? Thin coverage, cluttered layout, scrolling for days, it still steals focus or closes every time. Built for touchscreens, not your workflow.

*GlyphKit exists because that gap shouldn't be there.* It floats, never steals your cursor, puts every symbol one click away. In AUTO mode it even pastes for you – click `∞` and it lands right in your text field – while the tool stays available to you on top of your window for as long as you need it.

## Features

### Always there, never in the way

<p align="center">
  <img src="media/glyphkit_screenshot_full.png" alt="GlyphKit window" width="720">
</p>

GlyphKit stays on top of all your windows but never takes focus. Click a character and your cursor stays exactly where it was. The window doesn't appear in the taskbar, fades to near-transparent when you're not using it, and remembers its position between sessions.

Toggle it on and off from anywhere with **Ctrl + Alt + G**. Close it with **Esc** when focused.

### 433 characters across 13 categories

Math, arrows, Greek, logic, sets, comparison, geometry, subscripts, superscripts, box-drawing, fractions, currency, and miscellaneous symbols. All searchable by name.

### 4 copy modes

Cycle through them in the title bar:

| Mode     | What it does                                               |
| -------- | ---------------------------------------------------------- |
| **COPY** | Copies the character to your clipboard                     |
| **AUTO** | Copies and instantly pastes into whatever you're typing in |
| **HTML** | Copies the HTML entity, e.g. `&#x00BD;`                    |
| **U+**   | Copies the Unicode codepoint, e.g. `U+00BD`                |

<p align="center">
  <img src="media/glyphkit_screenshot_mode.png" alt="Copy modes" width="720">
</p>

<p align="center">
  <img src="media/glyphkit_screenshot_status.png" alt="Status bar confirmation" width="520">
</p>

### Favorites

Right-click any character to add it to your Favorites tab. Build your own shortlist of the glyphs you actually use. Remove them one by one with the delete toggle.

<p align="center">
  <img src="media/glyphkit_screenshot_favorites.png" alt="Favorites tab" width="720">
</p>

### Recently Used

Your last 24 unique characters are tracked automatically. No setup, just use the app. Clear the list when you want a fresh start.

### Search

Start typing in the search bar to filter across all categories by character name. Finds `arrow` or `alpha` or `fraction` instantly. The names of any glyphs are always shown in the status bar – so you can look for them even faster via the search.

<p align="center">
  <img src="media/glyphkit_screenshot_search.png" alt="Search for alpha" width="720">
</p>

### Remembers your setup

Window position, copy mode, favorites, and recents all survive restarts. Config lives next to the executable as a simple JSON file.

## Installation

### Portable (recommended)

1. Download **GlyphKit.exe** from the [latest release](https://github.com/Lunyxium/glyphkit/releases/latest)
2. Put it anywhere you like  
   *(note: if you put it in a read-only folder like C:\Program Files\ it won't save your settings or history)*
3. Run it

Windows might prompt a security pop-up, code & everything is right here if you want to check before allowing it.

Single file. No installer. No Python required. No admin rights. Just works.

<details>
<summary><strong>Run from source</strong></summary>

Requires Python 3.10+ on Windows.

```powershell
git clone https://github.com/Lunyxium/glyphkit.git
cd glyphkit
python run.pyw
```

Or just double-click `run.pyw`.

</details>

<details>
<summary><strong>Build the exe yourself</strong></summary>

```powershell
pip install pyinstaller
pyinstaller --onefile --noconsole --icon=glyphkit.ico --add-data "glyphkit.ico;." --name=GlyphKit run.pyw
```

Output: `dist/GlyphKit.exe` (~11 MB)

</details>

## Built with

Python, tkinter, and the Win32 API via ctypes. Zero external dependencies, runs entirely on Python's standard library.

~1200 lines of code across 3 files. Lightweight by design.

## License

MIT &mdash; [Matt Baeumli](https://github.com/Lunyxium) &mdash; 2026
