# SUBMISSION REPORT — news-image-20261122

**Status: PREPARED — NOT SUBMITTED**

- **Competition:** news-image-20261122 — "Sum up 22 November's world news in one image"
- **Repo:** https://github.com/salikamarlisa3-cell/global-edition-news-image-20261122
- **Commit:** `(see below — filled after push)`
- **Entry:** `entry.png`, exactly 1024×1024, deterministic (two runs byte-identical,
  sha256 `e13dcd479a8a8a569c59d2e90422db18387be6d3ce264797ad3d6e6aaca1b8bb`,
  182,599 bytes)
- **Prepared:** 2026-11-22 (build session, ~09:24–10:00 WIB)
- **Deadline:** 2026-11-24 07:00 WIB (2026-11-24T00:00:00Z)

## What the poster contains

- **56 stories, 7 regions** (8 stories per region: North America, Latin America,
  Europe, Middle East, Africa, Asia, Oceania), every story published or reported
  in the 22 Nov 2026 news cycle with its outlet tag on the page.
- **3 lead stories:** Iran strikes US bases in Bahrain; World Court finds Myanmar
  guilty of Rohingya genocide; Peru quake 6.7 rattles the Andes.
- **Dot-matrix world map** with 7 numbered region pins + region key.
- **16 illustrated panels** (3 leads + 13 feature tiles) drawn from the day's stories.
- **UTC timeline** (6 timed events, WIB), **by-the-numbers** strip (6 stats),
  **weather strip** (day highs/lows for 7 cities, Open-Meteo forecast for 22 Nov) +
  **"left out & why"** date-check box.
- **SOURCES.md** in the repo lists every story with outlet, date and
  verification URL. Just Security Early Edition for 22 Nov was not published
  (weekday-only; latest 20 Nov), so stories were verified against Reuters, AP,
  BBC, Al Jazeera, AFP, DW, RNZ, The Guardian and the wires.

## Verification performed

- `entry.png` opened and visually inspected: no clipping, no overlap, all
  56 story lines, map pins, timeline, numbers and weather strips legible.
- Defects found and fixed: (1) story #41 outlet "DEMOCRACY NOW!" overflowed
  its column by ~25px — fixed by right-aligning outlet tags and widening the
  headline margin; (2) feature-tile caption "Mlambo-Ngcu…" truncated —
  shortened to "Mlambo".
- Determinism: generator run twice; both outputs byte-identical
  (sha256 `e13dcd479a8a8a569c59d2e90422db18387be6d3ce264797ad3d6e6aaca1b8bb`).
- Generator `main.py` written fresh in this session (no code copied from
  earlier news-image entries); only the pattern was reused.
- Repo is public with MIT LICENSE (SPDX line), `.makefun/owner.json`,
  README with the 3 live make.fun badges, and repo About/description set.

## Next step (NOT done by this session)

This entry is **prepared, not submitted**. Submission needs the user's paste
of the build prompt into the 'make.fun — Ruang Build' side chat before the
**2026-11-24 07:00 WIB** deadline; the news-image kit cannot write a
transcript bundle for a subagent session.
