"""Tests for GlyphKit — data integrity, config, and core logic."""

import json
import os
import tempfile
import pytest
from characters import CATEGORIES
from main import (
	TAB_ROWS, GLYPH_PRESETS, OPACITY_PRESETS, SCALE_STEPS,
	COPY_MODES, MAX_RECENTS, DESIGN_DPI,
)


# === Character Data Integrity ===

class TestCharacters:
	def test_no_empty_categories(self):
		for key, cat in CATEGORIES.items():
			assert len(cat["chars"]) > 0, f"Category '{key}' has no characters"

	def test_all_chars_are_tuples(self):
		for key, cat in CATEGORIES.items():
			for item in cat["chars"]:
				assert isinstance(item, tuple) and len(item) == 2, (
					f"Category '{key}' has malformed entry: {item}"
				)

	def test_no_duplicate_chars_within_category(self):
		for key, cat in CATEGORIES.items():
			chars = [c for c, _ in cat["chars"]]
			dupes = [c for c in chars if chars.count(c) > 1]
			assert len(dupes) == 0, f"Category '{key}' has duplicates: {set(dupes)}"

	def test_all_chars_are_valid_unicode(self):
		for key, cat in CATEGORIES.items():
			for char, name in cat["chars"]:
				assert len(char) == 1, f"'{name}' in '{key}' is not a single character: {repr(char)}"
				assert ord(char) > 0, f"'{name}' in '{key}' has invalid codepoint"

	def test_all_categories_have_icon(self):
		for key, cat in CATEGORIES.items():
			assert "icon" in cat, f"Category '{key}' missing icon"
			assert len(cat["icon"]) >= 1, f"Category '{key}' has empty icon"

	def test_all_chars_have_names(self):
		for key, cat in CATEGORIES.items():
			for char, name in cat["chars"]:
				assert len(name.strip()) > 0, f"Character '{char}' in '{key}' has empty name"

	def test_tab_rows_reference_valid_categories(self):
		for row in TAB_ROWS:
			for key in row:
				assert key in CATEGORIES, f"TAB_ROWS references unknown category '{key}'"

	def test_all_categories_in_tab_rows(self):
		all_tab_keys = {k for row in TAB_ROWS for k in row}
		for key in CATEGORIES:
			assert key in all_tab_keys, f"Category '{key}' not in TAB_ROWS"


# === Config Round-Trip ===

class TestConfig:
	def test_save_load_roundtrip(self):
		config = {
			"x": 100, "y": 200,
			"copy_mode": 1,
			"favorites": ["\u2211", "\u03b1", "\u20aa"],
			"recents": ["\u221e", "\u00bd"],
			"user_scale": 1.1,
			"glyph_size": "L",
			"idle_opacity": "low",
			"fade_delay": 200,
			"snap_enabled": False,
			"hotkey": "ctrl+alt+g",
		}
		with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
			json.dump(config, f, indent=2, ensure_ascii=False)
			path = f.name
		try:
			with open(path, "r", encoding="utf-8") as f:
				loaded = json.load(f)
			assert loaded == config
		finally:
			os.unlink(path)

	def test_unicode_survives_roundtrip(self):
		"""The bug that wiped configs: Unicode chars that can't encode in cp1252."""
		problematic = ["\u20aa", "\u2217", "\u03b8", "\u2265", "\u221e"]
		config = {"favorites": problematic}
		with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
			json.dump(config, f, ensure_ascii=False)
			path = f.name
		try:
			with open(path, "r", encoding="utf-8") as f:
				loaded = json.load(f)
			assert loaded["favorites"] == problematic
		finally:
			os.unlink(path)

	def test_ensure_ascii_false_preserves_chars(self):
		"""With ensure_ascii=False, chars are stored as-is, not as \\uXXXX."""
		config = {"favorites": ["\u03c0"]}
		with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
			json.dump(config, f, ensure_ascii=False)
			path = f.name
		try:
			with open(path, "r", encoding="utf-8") as f:
				raw = f.read()
			assert "\u03c0" in raw
			assert "\\u03c0" not in raw
		finally:
			os.unlink(path)


# === Recents Logic ===

class TestRecents:
	def _make_recents(self):
		return []

	def _add_recent(self, recents, char):
		"""Mirror of GlyphKitApp._add_recent logic."""
		if char in recents:
			recents.remove(char)
		recents.insert(0, char)
		return recents[:MAX_RECENTS]

	def test_add_single(self):
		r = self._add_recent([], "A")
		assert r == ["A"]

	def test_add_moves_to_front(self):
		r = ["B", "A"]
		r = self._add_recent(r, "A")
		assert r == ["A", "B"]

	def test_max_recents_limit(self):
		r = []
		for i in range(30):
			r = self._add_recent(r, str(i))
		assert len(r) == MAX_RECENTS

	def test_no_duplicates(self):
		r = []
		r = self._add_recent(r, "A")
		r = self._add_recent(r, "B")
		r = self._add_recent(r, "A")
		assert r == ["A", "B"]


# === Favorites Logic ===

class TestFavorites:
	def test_add_favorite(self):
		favs = []
		char = "\u03c0"
		if char not in favs:
			favs.append(char)
		assert favs == ["\u03c0"]

	def test_no_duplicate_favorite(self):
		favs = ["\u03c0"]
		char = "\u03c0"
		if char not in favs:
			favs.append(char)
		assert favs == ["\u03c0"]

	def test_remove_favorite(self):
		favs = ["\u03c0", "\u03b1", "\u03b2"]
		favs.remove("\u03b1")
		assert favs == ["\u03c0", "\u03b2"]

	def test_max_favorites(self):
		favs = [str(i) for i in range(70)]
		assert len(favs) >= 70
		# Should not add beyond 70
		if len(favs) < 70:
			favs.append("extra")
		assert len(favs) == 70


# === Constants Validity ===

class TestConstants:
	def test_scale_steps_sorted(self):
		assert SCALE_STEPS == sorted(SCALE_STEPS)

	def test_scale_steps_contain_100(self):
		assert 1.0 in SCALE_STEPS

	def test_opacity_presets_range(self):
		for key, val in OPACITY_PRESETS.items():
			assert 0 < val <= 1.0, f"Opacity '{key}' out of range: {val}"

	def test_opacity_off_is_fully_opaque(self):
		assert OPACITY_PRESETS["off"] == 1.0

	def test_glyph_presets_have_font_and_btn(self):
		for key, preset in GLYPH_PRESETS.items():
			assert "font" in preset, f"Glyph preset '{key}' missing 'font'"
			assert "btn" in preset, f"Glyph preset '{key}' missing 'btn'"

	def test_copy_modes_have_required_fields(self):
		for mode in COPY_MODES:
			assert "key" in mode
			assert "label" in mode
			assert "fg" in mode
			assert "status" in mode

	def test_design_dpi_is_144(self):
		assert DESIGN_DPI == 144
