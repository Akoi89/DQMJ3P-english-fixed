# The rebuilt CIAs

First built 2026-09-08; the thirty-first and latest build is dated 2026-09-13. Output is in `FIXED_BUILD/` at the project root, alongside a copy of these notes and the test plan.

| File | Size | Title | Version |
|---|---|---|---|
| `DQMJ3P-base-fixed-0.1.0.cia` | 1522 MB | `00040000001ACB00` | 0.1.0 |
| `DQMJ3P-update-fixed-3.4.0.cia` | 20.4 MB | `0004000E001ACB00` | 3.4.0 |

**The crash fix is included.** Both CIAs carry Lurpigi's corrected
`break_font_L.bffnt`, md5 `66add92a51eb6a865070d2949981a61e` (819,828 bytes: Lurpigi's font with the four glyphs the twentieth build appended; before that build the packed font was `4fe77591a49b87f5c72f76000b78979d`), read back out of the packed files to
confirm it: 17x21 cells, three 512x1024 sheets, A4, which is the Japanese layout. Both builds got
slightly smaller because the correct font is 819 KB against the broken one's 2.1 MB.

The menu font `break_font.bffnt` is deliberately left as the English patch shipped it. The Italian
project's version is redrawn artwork with identical layout and identical glyph coverage, so taking
it would change how English text looks for no benefit.

Built with your own `TGAA 1-2/testimony_pipeline/build.py`. Both original CIAs carry plaintext
RomFS, so each took the safe path: splice the new RomFS into the NCCH in place and repair the hash
chain, never `3dstool -c -t cxi`. Every TMD hash was recomputed and re-verified by the tool, and I
re-verified both independently afterwards with `ncch.verify`.

**One version note.** The original base CIA's filename says v0.1.0 but its TMD said 0.0.0. The
rebuild is stamped 0.1.0, so it installs cleanly over the original and is distinguishable from it.
If you would rather it matched the original exactly, that is a three minute rebuild.

## Verified from the packed file, not the working tree

The point of this section is that these numbers come from text extracted back out of the finished
CIA, not from the directory I edited.

**Update CIA:** 22 message files, **12,659 of 12,659 strings identical** to the intended build.
Every spot check reads correctly out of the packed file: the bestiary entries, `Moreheal`, the
`Sleep` and `Stasis` skill trees, `Volcanic Fragment`, `Brass`, the rewritten trophy, and Great
King Vearn's line. No `Centre`, no `……`, and the only Japanese left is the two icon-glyph strings.

**Base CIA:** 950 message files, **26,803 of 26,803 strings identical**. Read straight out of the
packed file, the name-entry keyboard is `きぎ` again with no `Round` or `Breath` on the kanji page,
the map reads `The Mole Hole - B4`, the race tutorial gives its real instruction, and the counter
word is correctly blank. No `Centre`, no `……`, three kana strings left and all three are icon
glyphs inside English text.

## What is in these builds

| Change | Count |
|---|---:|
| Strings that had no English at all, now written | 167 |
| Corrupted name-entry keyboard restored | 2 |
| Factual errors corrected | 16 strings, 35 edits |
| Name collisions resolved | 21 renames |
| Spelling corrections | 277 |
| Japanese ellipses normalised to `...` | 422 |
| Centre standardised to Center | 103 |
| Regressions reverted to Joker 3 wording | 5 |
| Brash renamed to Brass | 7 |

Verification of the merged base-plus-update result: 3 strings still flag as untranslated and all
three are English text containing icon glyphs; 2 strings are blank and both are the Japanese
counter words the Joker 3 patch also blanks; 6 format specifiers changed and all six now match the
Japanese exactly; no live name collision remains in any name table.

## What is NOT in these builds

- Anything for the plain Joker 3 patch. This work is Professional only.
- The 395 duplicate files in the RomFS. Left alone deliberately; removing them changes the layout
  for no functional gain.

## Install

`FONT_FIX/` is now redundant if you install these CIAs, since the font is inside them. It is still
useful for one thing: dropping it on the **original** 2021 patch to confirm the crash fix works on
its own, separately from any of my text changes.

Same as any CIA: install both, base first. If you already have the 2021 patch installed, these
install over it. **Back up your save first.** Nothing here should touch save format, but that is an
assumption, not a measurement.

Then follow `TESTING.md`. Tier 1 is about ten minutes and covers the flagship fixes. The cutscene
the woodus thread names as the crash point is the regression test for the font.

## If something is wrong

The whole build regenerates from the two original 2021 CIAs with one command,
run from `_audit/`:

```
python rebuild.py build_repro
```

It extracts both CIAs, adds Lurpigi's font (md5 checked), runs every pass in the
order they were first run, and then compares the result with `build/` file for
file and byte for byte. As of 2026-09-11 all 14,082 files match. Once a rebuild
matches, `build/` can be replaced with it, and the CIAs packed from it with
`build.py`, then `smdhfix.py`, then `verify_pack.py`.

A change means a new step in `rebuild.py`, never a hand edit to `build/`. The
one time that rule was broken (a one-off command normalising "Divine Beast" to
"Incarnus") is exactly what the byte for byte check caught; that step is now
`incarnus.py`.

## Second build, 2026-09-09: the graphics layer

The first build translated the message files. This one adds the two layers that
no `.mes` audit can see.

| Change | Count |
|---|---:|
| UI label textures redrawn in the game font | 83 placements, 51 distinct |
| Textures taken from the French patch, where they drew English | 18 placements, 15 distinct |
| Text panes inside the layouts, rewritten | 60 |
| Layout archives rewritten | 53 of 362 |
| Message strings the earlier passes missed | 4 |

Three of those four are blanked rather than translated: the engine concatenates
them around a number, and the Joker 3 English patch blanks the same three labels.
An earlier draft translated them as "Left", "Times" and "etc.", which would have
put the word on the wrong side of the number.

The four missed strings came out of a kana scan that excluded the Japanese
keyboard tables and the single character icon glyphs. Three were entries in the
fragment table in `LayoutMessage.mes`, which was otherwise fully translated, and
one was a line of cutscene dialogue in demo980. That scan now returns zero.

The fifteen French files were checked before use: every one matches ours exactly
in width, height, format and byte length, so nothing in the layout had to move.
Two more were rejected. The French drew COPPER on the copper coin banners, but
the Japanese is ブロンズ and our own text says "Bronze Network Coin", so using
their file would have contradicted the text we ship.

### Verified from the packed CIAs, not the working tree

Both RomFS images were extracted back out of the finished CIAs and checked
there.

- **Base:** all 101 changed textures and all 60 changed panes present and
  correct. All 362 archives parse and all 3,938 textures decode. The font is
  still Lurpigi's fixed `break_font_L.bffnt` (md5
  `66add92a51eb6a865070d2949981a61e` since the twentieth build's four added glyphs). Zero untranslated strings outside the
  keyboard tables.
- **Update:** the three repaired fragments read `Left`, `Times` and `etc.`
  straight out of the packed file.

Four null tests pass on the applied tree: messages 972 of 972, archives 362 of
362, layouts 399 of 399, and every changed texture decodes.

### The boot notice, and a term normalised

The second review approved translating the boot notice rather than leaving it or
replacing it with credits. It is split across two textures per screen, 320x240
on the lower and 384x60 on the upper, with the Japanese running straight over
the seam, so `texpanel.py` lays the text out on a joined canvas and cuts it back
into tiles at their original byte lengths.

The body is set in the game's own font, which was the right choice by
measurement rather than taste: the Japanese lines are 12 px tall on a 17 px
pitch and the game font matches both. The heading is 29 px, more than twice what
that font draws, so it is set in a system face at the measured height with the
warning triangle and the red rules left untouched.

神獣 was also normalised. The script said Incarnus 350 times and Incarnii 266,
but four places said Divine Beast or Holy Beast. All are now Incarnus.

### 395 duplicated message files, and what that changed

The Professional patch ships 395 message files twice, once under
`Script/Field/...` and once under `Field/...`. Counting the event directories
across every build settles which is real:

| Build | `Field/Event` | `Script/Field/Event` |
|---|---:|---:|
| Japanese retail, base | 0 | 153 |
| Japanese retail, update | 0 | 7 |
| Joker 3, Japanese | 0 | 90 |
| Joker 3, English patch | 0 | 90 |
| **Professional, English patch** | **115** | 153 |

The `Field/` copies exist in no Japanese release and in no other patch, so the
game cannot be loading them. Seven strings across four files had drifted apart
between the two copies, one of them a two character stub against 209 characters
on the live side. `dedupe.py` copies the live text over the dead copy rather
than deleting 395 files on an inference, so whichever one the engine reaches it
reads the same thing.

This also corrects an earlier claim here. The line of cutscene dialogue reported
as untranslated was in one of these dead copies; the live copy was already
translated. Three of those four missed strings were real, not four.

### The eight display banners, and the title

`banners.py` finishes the last of the graphics. These are the ones the plain
font substitution flattens, so each has its own recipe: the fill, the outline
and the glow are sampled off the Japanese being replaced, and the geometry is
measured per banner and written down rather than guessed.

Two of them span more than one texture. The title banner is 320 px cut into 256
and 64, so it is laid out joined and cut back, the same way the boot notice is.

The two coin banners keep the French artwork and repaint only the metal word,
because the French drew that art in English already and only COPPER was wrong.
Sampling their own gradient off the letters beside it means BRONZE carries the
same orange ramp and the same outline.

Nothing baked into a Layout texture is in Japanese any more.

### The home screen and save data title

Both SMDH files had an English slot reading `DQMJOKER3 PRO` for the short and
the long name, where the Japanese slot carries a proper two line title. Both now
read `DQM Joker 3 PRO` and `Dragon Quest Monsters / Joker 3 PROFESSIONAL`, and
every Latin script slot is filled so the title reads correctly whatever the
console is set to. The Japanese and CJK slots are untouched. The update keeps
its `Ver.1.3`, taken from its own Japanese slot rather than typed in.

The save data icon rides the normal RomFS build. The home screen icon lives in
the ExeFS, so `smdhfix.py` patches it after the CIA is built and repairs the two
hashes that covers: the icon's own SHA-256 in the ExeFS header, which is stored
backwards, and the ExeFS superblock hash in the NCCH. **That step has to be
re-run after any rebuild**, because `build.py` starts again from the shell CIA.
The hash chain is checked before the patch, after it, and once more read back
out of the finished file.

## Fourth build, 2026-09-10: spelling regressions undone

A change audit read the packed CIAs against the 2021 patch and found 20 places
where our spelling pass made the text worse: it picked the most common word
one letter away rather than the right one (`usless` became `unless`), saw only
half of hyphenated words (`trans-dimensional` became `trains-dimensional`), and
flattened deliberate accents and Spanish. `_audit/spellfix.py` puts all 20
right and settles two lines whose meaning had flipped, checked against the
Japanese. Details in `AUDIT_FINDINGS.md` at the project root.

Checked out of the packed files: every RomFS file identical to its build tree,
all 45 fixes present (33 in the base title, 12 in the update), and compared
with the previous build only the 29 intended message files differ. Home screen
titles unchanged.

The from scratch recipe under "If something is wrong" above is out of date. It
stops at `round4.py` and leaves out the later passes, so rebuild from the
`_audit/build/` trees, which match the shipped CIAs byte for byte, until it is
rewritten.

## Fifth build, 2026-09-10: player titles

Playing a clean New Game showed the status screen cutting the player title
`Paradise Resident` to `Paradise Resid`. The field has room for it; the game
stops at 14 characters. 54 of the 236 titles were longer than that, every one
inherited from the 2021 patch. All 54 now fit, from review rounds 6 and 6B.

Checking the new names against the whole table caught three sets where a
shortened title would have duplicated another, and a ranking the Japanese
climbs (champion, emperor, overlord) that the English had flattened. The same
pass fixed seven inherited title errors that were never cut off: four typos,
`Ground` for "grand", a coined word standing in for "mapper", and
`Lost Traveler` for a title that means a traveler who never loses their way. `_audit/titles.py` applies it; 63 titles change (54 shortened to the cap, nine corrected).

Only the base title changes. The update CIA is byte for byte the previous one.

## Sixth build, 2026-09-11: wrong numbers in the help text, and a grammar fix

Every number in the ability, trait, skill and item descriptions was compared with
the Japanese. Five descriptions were simply wrong, all inherited from the 2021
patch: four traits said all four stats rise "by N levels" where the Japanese
says N of your stats go up, and one item sent you to the "first" Speed Road
instead of the third. Two more had dropped an exact figure the Japanese gives
("doubles", "5%"). All reviewed and fixed by `_audit/helpfix.py`. English lines
that state a figure the Japanese never mentions were left alone on review: they
may come from game data, and nothing in the text says they are wrong.

`_audit/articles.py` fixes two places that read "a Incarnus".

Both CIAs change this time. The build now comes from `_audit/rebuild.py`, which
reproduces the build tree from the original 2021 CIAs byte for byte.

## Seventh build, 2026-09-11: names (review rounds 8 and 8B)

227 names change, in 405 places across the seven name tables, and every
description that mentions one is carried along: 432 description labels. The
Japanese decides each mention, so a word that only looks like a name is left
alone. Among them: the attack traits (ブレイク) are now "X Break" and "X Break+",
kept apart from the defence traits (ガード) "X Ward"; the monster family titles
are "Slime Novice" through "Slime Legend"; the ときどき and growth traits follow
the same plain-for-small, "+"-for-full rule; the item and map names flagged in
round 8 are fixed. Applied by `_audit/rename8.py` from `_audit/names_r8.json`
(made by `mk_r8_renames.py`), the last step of `rebuild.py`.

Checks: rename8.py was written by the builder from `_audit/SPEC_rename8.md` and
accepted by the refuter after one rework; `residual8.py`, written separately,
finds no old name left in any of 727 mentions the Japanese backs; rebuild from
the 2021 CIAs matches `build/` byte for byte; no title over 14 characters; no
new name shared by two Japanese names. Against the sixth build only message
files changed: base 14 files and 466 labels, update 9 files and 371 labels.

Installed 2026-09-11 about 19:45 with `_audit/install_one.ps1` (base, then
update). `_audit/checkinstall.py` hashed all four installed .app files against
the TMD and the CIA bytes: all match.

## Eighth build, 2026-09-11 night: names that disagreed with each other (round 9)

An independent audit of the seventh build found no defect in what had been
applied, but did find text naming one skill or trait two different ways.
Review round 9 (`GEMINI_DQMJ3PRO_ROUND9.md`) approved every section:

| Change | Count |
|---|---:|
| Crack skill ranks put on the same plain / + / SP / EX ladder as the other nine families (round 4 of this project had made them Expert / Master) | 2 |
| Traits that shared a name with a different trait: 背水の陣 "Do-or-Die", ムラっ気 "Erratic" | 2 |
| Trainee class skills named "Trainee " + the base class (Wizard, Fighter, Barnstormer) | 3 |
| The card-suit monsters restored: Hawkhart Queen, Cluboon Jack, in the skill and monster tables | 4 |
| "Vearn, the Beholder" in one form everywhere | 1 |
| Skill books named after the skill they teach ("Quake Ward Book", not "Groundguard Book") | 115 |
| Skill book help lines that quoted a skill by a name not in the skill table, plus one missing "EX" | 13 |
| Mentions carried into descriptions and dialogue on Japanese evidence | 10 labels |

Applied by `_audit/round9.py` (built from `_audit/SPEC_round9.md`, refuter
accepted) from `_audit/names_r9.json` and `_audit/help_r9.json`, the last step
of `rebuild.py`. It reuses `rename8.py`'s algorithm, so every carried mention
is decided by the Japanese of the same line. Rebuild from the 2021 CIAs
matches `build/` byte for byte. Both CIAs change. Against the seventh build,
only message files differ: base 8 files and 144 labels, update 7 files and
145 labels, all accounted for by the table above. `verify_pack` OK on both,
home screen titles unchanged.

Two tools were also fixed to print on a plain console (`rebuild.py`,
`smdhfix.py`); neither change touches what is written.

## Ninth build, 2026-09-11 late night: line breaks restored, and the family table

Playing the eighth build showed two things the files could not.

**The update files had lost every hand line break.** The 2021 team broke
each description by hand in the base title (the Slime entry is four lines of
about 160 px), but their update title carries the same texts with every break
replaced by a space, and the update copy is the one the game shows. The engine
wraps by character, so words split at the box edge ("pleasa / nt"). Measured:
2,872 update labels in six description files, and 4,984 across all 22 update
message files, are exactly their base text flattened.

`_audit/unflatten.py` (from `_audit/SPEC_unflatten.md`, refuter accepted
after one rework) puts them back, and it is a whitespace-only change by
construction: every write is refused unless the text with whitespace
collapsed is identical before and after.

| Step | Count |
|---|---:|
| Update labels given back their base line breaks, 15 files | 4,984 |
| Bestiary entries re-wrapped by word at the measured 182 px box (base breaks ran to 213 px) | 142 |
| Bestiary entries left with the 2021 breaks | 595 |
| Help strings nobody had ever broken, word-wrapped at 234 px (Feat 4, Item 45, Action 4, Help 2) | 55 |
| Distinct labels changed, all in the update title | 5,155 |

Box widths come from the layout files (`tb_trivia_01` 182 x 72 in
`lib_monster.arc`; 234 x 72 in `lib_common.arc`), and the font measure was
calibrated against the screen: a line the game broke at 180 px measures 180.
52 bestiary entries come out at five lines in a four-line box; the Japanese
has one such entry. Whether the fifth line shows needs a look on screen.
`SkillHelpMessage` is a list, one ability per line, and was only restored,
never wrapped. Ideographic spaces (U+3000, 43 of them) are preserved.

**The Library family table clipped.** Round 5 had restored "Slime Family"
through "??? Family" on a width estimate of 62 px in a 75 px cell; on screen
the cell holds 70 px and five of the nine clipped ("Dragon Famil", "Undead
Fami"). The column header already reads "Family", so round 10 dropped the
word from the nine cells (`latefixes.py`); the widest is now 49 px.

Rebuild from the 2021 CIAs matches `build/` byte for byte with both steps in
`rebuild.py`. Only the update title's message files and both titles'
`LayoutMessage.mes` change against the eighth build.

## Tenth build, 2026-09-12: the name-entry keyboard opens on the Latin tab

Same base CIA as the ninth build. Only the update CIA changes, and only its
executable: the RomFS is byte-identical to the ninth build.

The keyboard used to open on the hiragana tab, and every player of an
English patch has to press X five times before typing a name. The keyboard's
open routine in the executable passes a hardcoded page index of 0. Static
reverse engineering of the update title's code (`_audit/KEYBOARD_TAB_RE.md`)
found that call, proved from the game's own seven-entry tab tables that the
"Aa" page is index 5, and found two spare no-op words in the page builder to
keep the keyboard's two page-index fields in step, so the tab highlight and
the X cycling agree with the page shown. Three 32-bit words change in
8,159,232 bytes of code. Tested first through the emulator's mod folder,
which substitutes the code without touching a CIA: the one-word version
opened the Latin page under a hiragana highlight, the three-word version
opens it with Aa highlighted and X cycles correctly.

`_audit/codepatch.py` (from `_audit/SPEC_codepatch.md`, refuter accepted)
applies it at pack time to the update CIA, after `smdhfix.py`: it
decompresses the ExeFS `.code` with 3dstool, whose BLZ compressor reproduces
Nintendo's compressed bytes exactly, patches the three words, recompresses
(4,477,028 to 4,477,036 bytes, inside the 4,477,440 allocation before the
icon), rewrites the entry and repairs the per-file and superblock hashes, and
reads the result back. A rerun says "already patched" and changes nothing.

Verified from the packed file: the only bytes that differ from the ninth
build's update CIA are the superblock hash, one entry-size byte, the `.code`
hash and the `.code` data; the exheader, its hash, the RomFS fields, the icon
and content 1 are unchanged; the decompressed code differs from the ninth
build's in exactly nine bytes at the three offsets.

## Eleventh build, 2026-09-12: event dialogue wrapped at the window, two number fragments

Playing the tenth build showed the field dialogue window splitting words at
its edge ("don't think I won't re / sist you"). The description files had
been put right in the ninth build, but the event dialogue was never
hand-broken in English at all: each page is one long line, and the engine
wraps by character at the 346 px message window
(`common/message_window.arc`, `tb_message_window`, 346 x 44, two lines).
The Japanese dialogue is hand-broken into two lines per page and its widest
line measures about 345 px.

`_audit/wrapdialogue.py` (from `_audit/SPEC_wrapdialogue.md`, refuter
accepted after two reworks) word-wraps every over-width line at 346 px in
the event dialogue folders (`Script/Field/` and the patch's dead `Field/`
copies), in both titles. Pages are split at every page-break control tag,
including the 127 that sit mid-line, and the space beside such a tag is
charged to the line it sits on; control codes are kept whole; every write
is whitespace-only by a hard check.

| Change | Count |
|---|---:|
| Dialogue labels rewrapped (both titles, both folder copies) | 3,370 |
| Lines that were wider than the window, now broken between words | 3,917 |
| Render lines still over 346 px after the pass | 0 |
| Pages that end up over two lines (the engine pages through them; 18 unique were already so) | 35 unique |

Two fragments the engine draws straight after a number gained a leading
space (`latefixes.py`): the level-up panel read "5skill points!" and the
skill screen "2SP unlocks:"; they now read "5 skill points!" and "2 SP
unlocks:". Whether the engine honours a leading space is checked on screen.

Left alone on purpose: 27 over-width lines in five `Message/` files whose
boxes have not been measured (StealthBox, NameMessage, Information,
MenuMessage, ReactorFnd).

Rebuild from the 2021 CIAs matches `build/` byte for byte with the new step
last in `rebuild.py`. Both CIAs change (message files only); the update
CIA also carries the keyboard patch from the tenth build via `codepatch.py`.

## Twelfth build, 2026-09-12: round 11 and the Helpful Tips re-flow

The eleventh build was packed and verified but never installed; this one
supersedes it and adds two steps.

**Round 11** (`GEMINI_DQMJ3PRO_ROUND11.md`, approved in full; applied by
`_audit/round11.py`, refuter accepted): 51 labels.

| Change | Count |
|---|---:|
| Resistance values that overprinted each other in their 26 px cell: Vuln, Norm, Res., Half, Res+, Null, Heal, Refl (two copies of the table, base and update) | 21 |
| "Essence Drain" row label that wrapped in its 66 px cell, now "Ess. Drain" | 2 |
| Sort-mode headers: Type (was "ID"), Obtained, Equipped, Retrieval, Race, Demons, Undead | 14 |
| Family rows on the bestiary Mix lines: Demon, Undead, and "Break" for ブレイク系 (was "Boss") | 6 |
| The 種類 counter after a count ("12Type"), now " Types" with a leading space | 2 |
| Three dialogue typos: "safe... you", a doubled "suddenly", "Resistance" capitalised (base, two copies of each file) | 6 |

The typo fixes run before the dialogue wrap in the recipe, because they
match the unwrapped 2021 lines.

**Helpful Tips re-flowed** (`_audit/tipsflow.py`, refuter accepted): the
2021 team hand-broke the tip bodies at whatever width they liked, some at
half the 378 px box. 88 of the 90 bodies are re-flowed at the box width,
paragraphs separated by a blank line as the Japanese does; 2 that would
exceed the ten-line box with the gaps keep their 2021 breaks. Whitespace-only
by a hard check. Eight lines land at exactly 378 px.

Rebuild from the 2021 CIAs with both steps replaces `build/` this time (the
typo fixes cannot be applied on top of already-wrapped text), and the pack
chain runs from the new trees.

## Thirteenth build, 2026-09-12: one label back from the twelfth

The twelfth build was installed and checked on screen: the resistance
table fits (Vuln / Norm / Res. / Half / Res+ / Null / Heal / Refl, "Ess.
Drain"), the item list header reads "Type" in type-sort mode, and the
sort, family and typo changes are in. One of round 11's choices did not
survive the screen: the 種類 counter on the Library's Collection overview
sits in a unit pane a few characters wide, and " Types" wrapped its last
letter onto a stray line ("5 Type" / "s"). It is blank in this build, the
second of the two options the review offered, so the overview reads
"12  2.2%" under a column header that already names the category, the same
treatment the six counters in round 5 got. Nothing else changes: against
the twelfth build only `LayoutMessage.mes` differs, one label, in each
title. Rebuild from the 2021 CIAs replaces `build/` as before; the pack
chain, keyboard patch, verification and xdelta patches are all redone.

## Fourteenth build, 2026-09-12: the squeezed labels were never a font bug

The "capital I collision" (AGI, INT, "Iems") that was parked as a font
mystery is a layout setting. The `txt1` panes that draw those labels carry
a character spacing of -2.0 px, which the Japanese designers used to tighten
their wide font in small pill buttons. Nintendo's layout library adds that
number to every glyph advance, and on the English font (capital I advances
4 px) a -2 leaves the next letter on top of it. A zoom of the 2026-09-11
bestiary capture shows the whole word "Items" squeezed from 27 px to 19 px,
which is exactly five letters at -2. The fonts themselves were re-checked
and are clean: same metrics in every copy, one cmap entry per letter, no
kerning block.

`_audit/charspace.py` (spec `SPEC_charspace.md`; builder Sonnet, refuter
Opus ACCEPT with no must-fixes) sets every negative charSpace to 0.0: 135
panes in 14 base archives, 129 of them at -2.0 and 6 at -1.0 (the medal
counters). The update title has no such pane, so only the base CIA and the
base xdelta change; the update CIA and its patch are byte for byte the
thirteenth build's. The edit is 141 bytes across the 14 archives, all
inside the float slots, and every layout still rewrites byte-identical
under the null test. Three panes with positive spacing (staff roll, one
button) are left as they were. Rebuild from the 2021 CIAs with the new
last step replaces `build/`; pack, keyboard patch, verification, install
(checkinstall OK) and both xdelta patches redone.

Not yet seen on screen after this build: the status screen's AGI/INT
labels and the bestiary "Items" pill.

## Fifteenth build, 2026-09-12: round 12, the Helpful Tips titles

The tips list cut 58 of its 89 titles mid-word ("Monster Mast"). The game
keeps at most 20 characters of a title (one screenshot, plus the longest
Japanese title being exactly 20; not read from the code), and the
【Category】 prefix the 2021 team carried over from the Japanese took 6 to
11 of them. Reviewed as `GEMINI_DQMJ3PRO_ROUND12.md` and approved in
full: the prefix is dropped from every title, and the eight that were
still over 20 without it are shortened (Active & Standby, More on Fusion,
Masters GP, Great Riders Cup, Removing GUEST Marks, Below the Break,
Riding Monsters 2, Partner Battle Rides). Three typos in tip bodies go
with it: "leveling up, This" gets its period, "the will be able to
pickup" becomes "they will be able to pick up", and "what item's" loses
its apostrophe.

`_audit/round12.py` (refuter Opus ACCEPT) runs before the tips re-flow so
the body fixes see the 2021 lines; it keeps the 2021 line breaks inside a
match and writes the paragraph break after "yourself." explicitly, because
the fixed line is 209 px, 1 px over the re-flow's short-line rule. 91
labels change in `Message/Information.mes`, nothing else in either title;
the update CIA and its patch are byte for byte the thirteenth build's.
Rebuild from the 2021 CIAs replaces `build/`; pack, keyboard patch,
verification, install (checkinstall OK) and both xdelta patches redone.

Not yet seen on screen after this build: the tips list titles, and the
fourteenth build's AGI/INT labels.

## Sixteenth build, 2026-09-12: round 13, the tip bodies and three consistency fixes

Reading the tips on screen turned up "guage" and "it the grand stage", so
all 89 tip bodies were read through. Reviewed as `GEMINI_DQMJ3PRO_ROUND13.md`
and approved in full: 33 spelling, agreement and missing-word fixes in 26
tips; "Broken World" unified to "Break World" (the Japanese is
ブレイクワールド in every one of the 12 lines); the three event names lose
their apostrophe, matching the Japanese katakana and the round 12 titles
(the refuter found two plural-possessive forms, "Riders' Cup" and
"Challengers' GP", that the review's counts had missed; they fall under the
same approved rule and are included); and 16 "Fondue" mentions in the Wood
Park recolouring dialogue become "Fondude", the family name the bestiary
uses.

`_audit/round13.py` runs after round11.py and before the dialogue wrap and
the tips re-flow, so its substring fixes see the 2021 lines; a match that
straddles a hand line break keeps the break. 109 labels change in the base
title and 38 in the update (the Ver.1.3 dialogue carries the event names
too). Rebuild from the 2021 CIAs replaces `build/`; pack, keyboard patch,
verification and both xdelta patches redone. Install pending: the chain
found an emulator running and left the installed titles alone.

## Seventeenth build, 2026-09-12: the NOW_PRINTING map marker, found and fixed

The Silent Meadows navi map drew "NOW_PRINTING" on its destination
marker. It had been parked as an engine fallback inherited from the game.
It was ours. A BFLYT text pane can carry, after its default text, an
ASCII message ID (the offset at +44 of the text-box fields points at it);
the game fills the pane from that label in LayoutMessage.mes. The marker
pane `tb_plc_H01` in `NaviMap/H00_00.arc` carries "PlaceName_H01_00",
which our LayoutMessage translates as "Wood Park". When the second build
wrote the English default text into that pane, `lyttext.replace` grew the
section and dropped everything after the text, so the ID offset pointed
at padding; the game looked up an empty label and drew its fallback. One
more pane had the same damage, the round counter in the battle window
(`tb_smogcount_round`, ID "round"). The 2021 patch's layouts have no such
damage (507 valid IDs, none dangling), and the Japanese game does not
show the placeholder.

Two changes: `lyttext.replace` keeps whatever follows the text slot and
shifts the ID offset when it grows a section, and a last step
`_audit/lytid.py` restores any ID that differs from the Ver.1.3 Japanese
layout (the reference for both titles, since the 2021 patch built its
base layouts from the Ver.1.3 files). The refuter (Opus) caught that the
first draft compared against the 1.0 Japanese layouts, which would have
pointed eight name-entry tabs at labels our message file does not have;
against the right reference exactly two panes change. Only those two
archives differ from the sixteenth build; the update CIA and its patch are
unchanged. Rebuild from the 2021 CIAs replaces `build/`; pack, keyboard
patch, verification, install (checkinstall OK) and the base xdelta redone.

Seen on screen 2026-09-12: the Silent Meadows marker reads "Wood Park".

## Eighteenth build, 2026-09-12: round 14, the sizing sample's 22 slips

To size the text that had never been read through, 200 strings were drawn
at random (100 dialogue, 100 help) and read for objective errors: 12 of
the dialogue strings and 8 of the help strings had one. The 22 slips found
that way were reviewed as `GEMINI_DQMJ3PRO_ROUND14.md` and approved in
full, together with the decision to proofread the whole help layer next
(3,570 strings; that pass is round 15, out for review). `_audit/round14.py`
applies the 22 as substring fixes before the dialogue wrap, keeping the
2021 line breaks; one fix also drops a stray Japanese bracket and a
leftover script token that sat on its own line. The refuter caught that
the token's removal first left "He" alone on a line; fixed. 36 labels
change in the base title and 12 in the update. Rebuild, pack, keyboard
patch, verification, install (checkinstall OK) and both xdelta patches
redone.

## Nineteenth build, 2026-09-12: round 15, the help layer proofread

Round 14 chose the help layer. Seven proofreaders (Opus) read all 3,570
strings under one brief (objective errors only; style, register and the
skill-name lists left alone) and returned 325 rows; each row was matched
against the shipped text of both titles, 19 were already fixed by earlier
rounds and 5 dropped after checking, leaving 301, reviewed as
`GEMINI_DQMJ3PRO_ROUND15.md` and approved in full with eight consistency
rules: attack elements read Light and Ice; "Woosh Ward" and "-flurry" as
the skill table spells them; "Tension Passer", "MP Drain Ward+" and
"Poisonous Prod" as the table names them; family names in title
descriptions follow the monster table (Demon, Undead), and three titles
that said "Nature Family" against a Japanese 悪魔系 read "Demon Family";
Tension moves say "by 2 levels" / "by 4 levels"; five more stray Japanese
brackets go; the misspelt but consistent skill names stay as the 2021
team's names. The same family-name rule is also applied to the two
coupling-search filters "Find only Devil Family." and "... Zombie Family
results." (found by the refuter; not in the review's literal scope, same
rule).

`_audit/round15.py` applies the rows and the rules before the dialogue
wrap. The refuter's first pass caught two real defects: an overlap rewrite
that could strip single letters (HelpMessage1002) and an "already applied"
shortcut that skipped rows whose corrected text is shorter than the
original; both fixed and re-verified (0 unexpected labels over 39,462).
342 labels change in the base title and 333 in the update. Rebuild, pack,
keyboard patch, verification and both xdelta patches redone; install
pending, the chain found an emulator running.

## Twentieth build, 2026-09-12: the crystal icon glyph, and a check of every character

A Discord thread about chest crashes prompted a check of every character
in every shipped string against both fonts. All resolve except one: the
Japanese Ver.1.3 update added four glyphs to its fonts (巫, 翔, 裔 and the
crystal icon 鴒) and the 2021 team, whose fonts lacked them, replaced the
icon with "♦", which exists in no font, so the icon drew as glyph 0 in
"Not enough [icon]." and in front of crystal items. `_audit/fontglyph.py`
(spec `SPEC_fontglyph.md`, builder Sonnet, refuter Opus ACCEPT with an
independent parse of the output) appends the four cells from the Japanese
update fonts to both of our fonts (3,842 to 3,846 glyphs, one CMAP block
added, every original glyph byte-identical), and `round16.py` puts 鴒 back
in the three labels. The fonts were tried through the emulator's mod
folder first: boot, save load, menus and lists render as before. The
chest crashes themselves are the 2021-05-30 changelog's "fix crash when
opening some chests"; our base is that release. Both titles change;
rebuild, pack, keyboard patch, verification, install (checkinstall OK) and
both xdelta patches redone.

## Twenty-first build, 2026-09-12: the lost yes/no prompts (round 17a)

The Woodus thread and the Discord were read for bug reports. Most predate
the 2021-05-30 release (chest and transfer crashes, machine-translated
brackets) or are the cutscene font crash already fixed. One survived: a
2021 report that the second Speed Road conduit's dialogue "closes out
before you get the chance" to choose yes or no, locking the later races.
A comparison of every English line's control codes with the Japanese
line's found the cause: the prompt code (01 0102, which ends 403 Japanese
lines) was missing from the Rank ★★ and ★★★ prompts and from three SD
extra-data prompts; one line kept it mid-text so its prompt fired early;
one line had a spurious one; three system lines (and a fourth copy of one)
carried a different window-style code. `_audit/round17.py` mirrors the
Japanese codes on those labels, 28 label writes over the two titles and
the dead Field copy, no visible word changed. Refuter (Opus) REWORK once
for a sixth lost prompt it found and for two inaccurate docstring claims,
then ACCEPT. Format specifiers were compared the same way: 0 differences.
The wording items from the same scan are round 17b, out for review. Both
titles change; rebuild, pack, keyboard patch, verification, install
(checkinstall OK) and both xdelta patches redone (the base patch was
re-encoded once with the documented source window, which changed nothing).

## Twenty-second build, 2026-09-12: round 17b (the Collab Battle reward, the Shiny Sap hint)

Reviewed as `GEMINI_DQMJ3PRO_ROUND17.md` and approved in full. The four
Collab Battle reward lines (A01_02, AROMA_2GO_MSG_900 to 903) had their
content shifted by one label in the 2021 English, the ticket line was
missing and a speech line was drawn in the system window; they are
rebuilt to the Japanese sequence with the Japanese control codes, and the
2021 team's reward-offer sentence goes back to line 900's second page,
where the Japanese has it (the refuter noticed it would otherwise vanish).
The ticket is "Collab Ticket" and every "Colab" is "Collab" (8 mentions).
The Shiny Sap hint (accessory quest 8) said "stealth boxex" where the
Japanese, and the dragon-quest.jp guide, say the black treasure chests
high above the Silent Meadows; both hint labels are corrected, plus
"aquired" and "the Grim Tundra" in the same set. The 27 dropped player-name
inserts stay as the 2021 team left them. `_audit/round18.py`, refuter
ACCEPT. Both titles change; rebuild, pack, keyboard patch, verification,
install (checkinstall OK) and both xdelta patches redone.

## Twenty-third build, 2026-09-12: item names no longer cut at 14

A session on an end-game save (378 hours, nearly every item) showed the
Items list cutting names at 14 characters: "Strong Medicin", "Super Seed
of", "Jumbo Oomph Po"; 584 of 1,079 item names are longer. The cause is
the family the earlier name-cap work mapped: item names are built into
fixed stack buffers, here three of 16 characters (icon, 14 visible, NUL)
in two shared wrappers and one screen function (`NAMECAP_RE.md` section
11, Opus). Unlike the monster caps, no stored field is involved, so
raising the buffers is enough. Thirteen words change in the update's
executable: the three sizes and the frame prologue, epilogues and one
scratch offset around them, to 32 characters. Tested first through the
emulator's mod folder on the end-game save: the item list, the item info
window and the equip lists draw full names ("Dirt Dragosphere"), and
monster nicknames are unchanged against an unpatched run. The refuter
(Opus) disassembled all three functions independently, confirmed every
prologue and epilogue is in the list and the alignment holds, and
accepted. `codepatch.py` carries the edits alongside the keyboard patch
and accepts a keyboard-only executable as a partial state. Only the
update title changes; the base CIA and its patch are the twenty-second
build's. Pack, keyboard and item patch, verification, install
(checkinstall OK) and the update xdelta redone.

## Twenty-fourth build, 2026-09-12: the quest and hint text checked against the Japanese

After the Shiny Sap hint (twenty-second build) turned out to describe the
wrong container, every quest instruction, hint, tutorial, signpost, shop
and NPC guidance line (1,007 labels, the Japanese beside the English) was
read by three Opus readers with one brief: facts only. They returned 128
rows; three were the Shiny Sap rows already fixed, and the remaining 125
all matched the shipped text (`_audit/proof_facts/consolidate.py`, which
matches across page breaks and full-width spaces). The reviewer approved
all 125 and the four consistency questions: "Broken Slime" to "Δ Slime"
(the bestiary's name for 凶スライム), "Don Clawleone" to "Don Mole",
"Black Iron Prison Tower" to "Darkiron Bastille", and the two mine
puzzle hints from "to the right" / "left" to "clockwise" /
"counterclockwise" (時計回り / 反時計回り). `round19.py` applies the rows
and the three names with a matcher that spans line breaks, page breaks
and highlight codes and keeps the matched separators in place; the three
names are matched the same way, so the six mentions split over a line
break are converted too (30 / 2 / 23 live mentions against the package's
contiguous count of 28 / 2 / 19), and a name that was split is joined
onto one line (the dialogue rewrap only breaks lines that overflow, so a
lone "Δ" would otherwise have stayed at a line end). One approved row
spelled "colour"; it ships as "color", the patch's spelling. The refuter
(Opus) reworked the first version (the globals missed names split over a
line break) and accepted the second after rerunning it on copies: 347
labels written, none outside the approved rows, the two hint labels and
the three names; a second run writes nothing; no old name left under the
loose matcher; the two help-layer labels that got a longer line still sit
inside the 346 px box. The join was added after that review and checked
by hand on the four split sites. Both titles change (base 277 labels,
update 70 against the twenty-third build). A first pack of this build
(without the join) was installed and replaced within the hour; the
shipped files are the second. Pack, keyboard and item patch,
verification, install (checkinstall OK both) and both xdeltas redone and
round-tripped.

The reviewer also offered an abbreviation script for the item names; it
is not needed, the twenty-third build's code patch draws them in full.

## Twenty-fifth build, 2026-09-12: the dialogue layer proofread

The last unread layer. Every NPC, cutscene, quest and shop line in the
Script/Field files (5,697 strings of 25 characters or more, the update's
copy of a file where it has one) went to eleven Opus readers in batches
of 518 with the help-layer brief from round 15: objective slips only.
They returned 605 rows; `_audit/proof_dlg/consolidate.py` matched every
one exactly once in the shipped text. Every string a reader flagged as
unsure, and every name the readers could not settle within one batch,
was then checked against the Japanese and the name-tag, monster, map,
item and reactor tables (`proof_dlg/jp_check.txt`, `reader_notes.md`).
That check set aside ten reader rows (two readers had gone against the
tables on Tiko and Nochoro, two had turned the Monster Battle GP into
the Masters GP, one had made the dying underling the wrong bat), added
eighteen whole-word sweeps (Nochoro, Tiko, Lenate, Theresa, Snapped-off,
Mt. Elpis, Anses's, East Polar Park, Undead Garden, Wormhole, Sea Map,
the Darkiron Bastille's power room, Monster Battle GP, Snapped-Dragon
for ダースガルマ, the cryogenic-sleep records, the boulder line, one
agreement slip) and sixteen Japanese-based fixes. The reviewer approved
all of it (595 rows, B1 to B18, C1 to C16).

`round20.py` got a new engine, because the first smoke test showed the
word-level matcher of rounds 13 to 19 dropping a highlight-off code and a
player-name insert when the corrected word touched them. The new one
works on a visible-text view (control pairs skipped, whitespace runs
collapsed, mapped back to the stored string), rewrites only the part of
a string that differs between old and new, and keeps every control pair
inside the rewritten span, each with the line break beside it. After the
edits, every changed page that would need a third line in the two-line
window is reflowed (its plain line breaks joined, the page wrapped
afresh at 346 px); ten such pages came from the edits and all ten fit
again, and the two that were over the limit in the 2021 text stay as
they were. Two labels are whole-label replacements with hand-placed
codes (the underling, and a line whose player-name insert sat between
two stray brackets; that one keeps the name on its own line and adds
the period the Japanese has, which the review package's row does not
show). The refuter (Opus) reworked the first version
(the two cases above plus an insertion that could land inside a
highlight) and accepted the second after rerunning it on copies: 1,517
labels written across both titles, a second run writes nothing, and no
label's sequence of control pairs differs from the shipped one.

Both titles change (1,310 labels in the base, 207 in the update against
the twenty-fourth build); the base CIA grows by one 4 KB block. One
older expectation had to move with the round: spellfix.py's fixed wording
for MASTERS_LOAD_SYSTEM_MSG_140 now says "Masters Road", the form the B
sweep gives it, so verify_pack.py's gate passes. Pack, keyboard and item
patch, verification, install (checkinstall OK both) and both xdeltas
redone and round-tripped.

## Twenty-sixth build, 2026-09-12: the analyze panes, and two items closed

The last two name caps from the item-name audit. The reactor's two analyze
lines (`tb_item_list_00` / `_01` in `reactor.arc`, 144 px each) cut item
names at 10 characters: one function builds both names into a 12-character
buffer at the top of its frame (`NAMECAP_RE.md` section 9, sites 5/6). Its
frame audit is the simplest of the family: no other stack offset is used,
one exit, a seven-register push, so the frame goes from 0x1c to 0x44 and
the two size words to 32 characters, four words in all. `codepatch.py`
carries them with the keyboard and item-list edits and accepts the
builds-23-to-25 executable as a partial state. The refuter (Opus)
re-disassembled the function and the name builder it calls and accepted.
This one is not seen on screen: the reactor does not open indoors and the
end-game save sits in the hub, so the check is left to play (TESTING.md
Tier 3); the same patch family was seen working on the item lists.

Closed without a change: the 16-character suffix buffer in the equip-slot
name path (section 11.1) holds the equip mark, which is the single letter
"E" in both titles' tables, so it cannot overflow.

README: a line in "Not fixed, known" points at Anthony's plugin for the
online-only content, with the note that it is a code plugin, not text,
and untested with this build.

Only the update title changes; the base CIA and its patch are the
twenty-fifth build's. Pack, keyboard and item and analyze patch,
verification, install (checkinstall OK) and the update xdelta redone.

## Twenty-seventh build, 2026-09-13: the menu and system layer proofread

The last layer nobody had read: every string in the Message files that
the help-layer round did not cover (1,614 strings of 25 characters or
more, 891 of them in MenuMessage: prompts, confirmations, the tutorial
pop-ups, battle event and result lines, the Speed Road and race text, the
reactor readouts, the diary, the network and transfer screens). Three
Opus readers with the round 15 brief returned 125 rows, all matched once
in the shipped text (`_audit/proof_menu/consolidate.py`). Every string a
reader flagged went against the Japanese, and every disputed term was
counted over the layer and, where it crosses layers, the dialogue. Three
reader rows were set aside (two went against the Japanese on Present
Code, one against a name tag), eleven sweeps added (Present Code for
プレゼントコード, the form the input pane already used; G-Cup; Lenate for the
two romanisations left in the menus; Carmasso; Wi-Fi Square; Network
Coins for 通信コイン; Bronze Coins; and SpotPass and StreetPass in Nintendo's
spelling over the menus and the dialogue both), and eleven Japanese-based
fixes: two Speed Road attacks labelled 【SHOT】 whose Japanese and whose
own list entry say close range, three attack descriptions that said one
slime drops where the Japanese says all, "Item Drop Rate up by 10x",
the Mega Body pop-up's missing verb, "ice floe" for 氷塊, the local-battle
prompt's missing "on the", a possessive, and the ship-remains line of the
Grim Tundra diary page, rewritten from ポーラパークのそばにある ストレンジャー号は
コアから切り離された 母船の一部だという. The reviewer approved all of it
(122 rows and the eleven C rows, B1 to B11).

`round21.py` is round 20's engine with two additions. Sweeps carry a
scope, so the two spellings also run over the dialogue files. And since
Message strings are never rewrapped by a later step, any changed line
that ends up more than 40 px wider than the widest line its own label
had, or wider than any line in its file, is re-broken at the label's old
width together with the rest of its paragraph. Four labels needed it:
the diary page, the Mega Body pop-up, the team-name error and a transfer
prompt whose fix had straddled a line break and would otherwise have
merged two list lines into one 352 px line (the refuter's catch, which
turned the file-wide check into a per-label one). No label ended wider
than those bounds or gained a line; the diary page lost one, the
intended merge of its rewritten sentence. Smoke test on
copies: 334 labels written across both titles, a second run writes
nothing, no label's sequence of control pairs changed.

Both titles change (213 labels in the base, 121 in the update against
the twenty-sixth build). Pack, keyboard, item and analyze patch,
verification, install (checkinstall OK both) and both xdeltas redone and
round-tripped.

After the build, the last name cap was tried and closed without a
change. The Library list's 10-character monster names come from a row
cache filled from the monster record; the documented one-word patch
(NAMECAP_RE.md 10.2) raises the copy limit to 11, and an RE pass
(NAMECAP_RE_12.md, Opus) found a second 10-character limit upstream, in
the loop that fills the record's lineage sub-entries from the stored
name. With both limits raised to 11 through the emulator's mod folder
the rows still drew ten characters ("Shell Slim"), so the stored name
itself is already cut when the monster is obtained, by a writer that
remains unlocated. No byte patch helps; the README's known-issues list
says so. Nothing shipped from this.

## Twenty-eighth build, 2026-09-13: the page layout of the dialogue

A measurement, not a reading. Every page of every dialogue label was
rendered with the game font and compared with the same page of the
Japanese Ver.1.3 text: 26 labels had a page that needed three lines
where the Japanese page has two, and 64 labels had the page-break code
mid-line (glued to a sentence, wrapped in spaces, or followed by a stray
space), which the engine draws as a leading space or a blank line at
the top of the next page. `round22.py` puts the Japanese shape back by
rule. Each page-break code takes the line-break flanks of the same code
in the Japanese label (its own line in almost every label; glued to the
closing punctuation in about twenty, where the Japanese writes it so;
193 label instances changed over the two copies in the rebuild, where
the step runs before the rewrap). Leading blank lines
the Japanese page lacks are dropped (three labels, seven instances).
Pages that outrun the Japanese page are rejoined and re-broken by width
when the words fit two lines (26 pages; a line that opens with an arrow,
a bullet, a heading, a window code or a page code is never joined, and
pages the Japanese draws on three or more lines, the results panels and
the operating-instructions board, are left alone). One label is split at
the Japanese page boundary. A write is refused if a visible word would
change or a control pair would be lost or reordered. The refuter (Opus)
sent the first version back (it forced every code onto its own line,
against the Japanese in 22 labels, and its counts were wrong) and
checked the second against the Japanese flank by flank. Five pages still
need a third line because their English is longer than two lines can
hold, and one line is a mistranslation; those six are with the reviewer
as round 22 section E and are not in this build.

Two experiments preceded the round. A three-line test line pushed
through the emulator's RomFS mod folder never reached the screen, nor
did a test change to a menu string, so that folder does not layer over
this title's RomFS once the update is installed (the executable override
does, as the item-name test showed); the mod folder is not a usable test
path for text. And the message window's text pane measures 44 px for a
21 px font, two lines; the Japanese game ships a few three-line pages in
it, so a third line is drawn rather than clipped, which is why the five
leftovers are a review question and not a defect.

Both titles change (144 labels in the base, 52 in the update against
the twenty-seventh build). Pack, keyboard, item and analyze patch,
verification, install (checkinstall OK both) and both xdeltas redone
and round-tripped.

## Twenty-ninth build, 2026-09-13: the six pages that needed words (round 22 section E)

The reviewer approved all six. `round23.py` rewrites each label whole,
with hand-placed line breaks and page codes, matched on its visible text
so it applies before or after the rewrap: the Darkonium line and the
Bundold gate record shortened to two lines; the medal collector's speech
split into the three Japanese pages with a shorter reward line; the
Demon King's Room signpost arrow shortened to one line; the resurrection
monologue given the page break its second window code implied; and the
Estark apparatus prompt, whose English was not a sentence, retranslated
and split into the two Japanese pages ("%ls and the 4 magatama are
inside." / "Insert %ls into the remnants?"). Every new line measures
under 346 px and no page has a third line. With this, no dialogue page
in either title needs more lines than its Japanese page, except the
panels the Japanese draws on three or more lines.

Only the base title's files hold five of the six labels; the medal
collector's is in both. Pack, keyboard, item and analyze patch,
verification, install (checkinstall OK both) and both xdeltas redone
and round-tripped.

## Thirtieth build, 2026-09-13: the machine's name, the Snapped family, one chapter hint

The two inconsistencies the proofreaders had flagged that no table could
settle, checked against the Japanese and put to the reviewer as round
24; all fifteen rows approved. The machine in the Darkiron Bastille has
two Japanese names, the full ブレイク化改造装置 (once ブレイクモンスター改造装置)
and the short 改造装置; the 2021 English rendered it nine ways. It is
"Break Remodeling Device" wherever the Japanese uses the full name and
"Remodeling Device" wherever it uses the short one (nine lines; the
Estark remnants' 製造装置, "production apparatus", is a different word and
stays). Four lines said just "Snapped" where the Japanese names
Snapped-off (ガルビルス) or Snapped-Almighty (ガルマザード), the tables'
names; one wrote "Dr. Snapped" with a period the tables lack. And the
chapter 7 hint said the boss had revived his minions where the Japanese
says the player has beaten them and reached the boss; retranslated.
`round24.py` applies the rows with the round 20 engine and the round 21
width rule for the one bestiary entry, and round 20's page reflow for the
three lines a longer name would have pushed to a third line (the refuter's
catch). Both titles change (29 labels in the base, 2 in the update: the
bestiary entry and the chapter hint). Pack, keyboard,
item and analyze patch, verification, install (checkinstall OK both) and
both xdeltas redone and round-tripped.

## Thirty-first build, 2026-09-13: the monster-name caps, settled with a live debugger

The 27th build's note said the Library rows and the party header were cut
by a stored copy of the name whose writer could not be found. That was
wrong, and the emulator's GDB stub showed why. A write watchpoint on a
monster record's name field, breakpoints on the name builders, and a few
pokes (`_audit/NAMECAP_LIVE.md`) gave the real picture: the record holds
11 characters and the capture-time writer stores 11 (the user's own save
still carries the tails of 11-letter defaults behind the 2-letter names
they gave their monsters); the Library lists cut at 10 because their row
builder formats each name into a 16-character buffer behind a family icon
that is five units long, not one (the static chain blamed for it, 0x25f3f4,
never runs on that screen); the Manage Monsters header cut at 10 through
the 12-character buffer the static pass had found and dismissed; and names
ended at 8 only after a rename, because the keyboard took 8 characters,
pre-filled the name cut to 8, and OK wrote it back. Each site was patched
in memory first and looked at on screen before it went into
`codepatch.py`: 27 more words in the update's executable (the Library row
buffer to 38 characters with its frame grown, the header buffer and the
three member-list prompt buffers to 32 with their frames, the keyboard
limit and slot counts to 11, the four rename handlers and the two lineage
copies to 11). The refuter re-ran the byte and frame checks (ACCEPT); a
clean boot with the new code showed an 11-letter rename kept in full,
"Slamen Dark, the Reaper" whole in its Library row, and an 11-letter
player name stored in its 24-byte save field. Anthony's plugin's hook and
probe words are untouched. Only the update's executable changes; both CIAs
are repacked as usual, the xdeltas regenerated and round-tripped.

## Thirty-second build, 2026-09-14: the text findings from the v1.1 rig sweep (round 25)

A menu-by-menu pass over v1.1 on the emulator (`_audit/RIG_SWEEP_2026-09-13.md`)
confirmed nine of the TESTING.md Tier 3 rows on screen and turned up six
things nobody had seen. The four text ones went to Gemini as round 25 and
were approved as recommended; the two code ones (three more 14-character
panels) wait for a live-debugger round after the RHDN posting and are
listed under "Not fixed, known" meanwhile.

`_audit/round25.py` (round 24's engine, 42 rows in
`_audit/proof_terms/round25.tsv`, refuter ACCEPT on a dry run) writes 74
labels: the thirty skill books that had kept the 2021 "Xguard" stem
through round 9 (their help lines wrote the skill in kana, so round 9's
stem test never saw them) now carry the English skill table's name plus
"Book", trailing spaces and one lowercase "book" gone; the five
HabitatMessage strings that read "as Map", "as Fiery Volcano" and so on
(Japanese ワールドマップなど) read "World Map etc."; the six "Point Zero"
occurrences in five strings (the diary twice, the Zoom list's rooftop
entry, the Z00_00 wormhole prompt and its record) read "Ground Zero" like
the other 23; and "Heavens Thunder" gets its apostrophe. No new item name
collides with an existing one; the longest, "Quake & Gravity Ward EX
Book", measures 149 units against the 138 of "Essence Drain Ward SP Book"
the bag already drew whole. Both CIAs change (HabitatMessage, DiaryMessage
and RulerPointMessage are base-only files); the executable is the 31st
build's. Pack, verification, install and both xdeltas redone.

## Thirty-third build, 2026-09-14: the last three 14-character panels

Round 25 section A, which Gemini approved as a code round after the RHDN
posting. Three panels cut names at exactly 14 characters: the status
screen's Skill panel, the Library's Basic Info header and the Monsters
list under Library > Skill. Two hypotheses died first, both worth
recording. It is not the layouts: across all 362 Layout archives and 2,730
text panes only 17 allocate between 13 and 17 characters and none is on
these screens, and the panes that hold these names allocate nothing at all
(`_audit/panesweep.py`). And it is not the six name-builder callers that
pass a 16-character buffer: breakpoints on all six never fired while the
Library header was rebuilt, though the header did rebuild.

The cause is two sibling builders, 0x2317d8 and 0x231410, the only two
members of the name-builder family whose printf max is 15. Each formats
`u"%ls%ls"`, a one-unit icon plus the name, into a 16-character stack
buffer; 16 units less the terminator less the icon leaves exactly 14. That
one shared shape is why three unrelated screens cut at the same place.
Thirteen words change: each buffer grows to 32 characters (30 visible,
against a longest species name and a longest skill name that are both 24), each
frame grows to hold it, and the locals above each buffer move up. Both
functions have a single exit and nothing else touches a stack offset above
the buffer in either.

One word is easy to miss and cost a boot. 0x2317d8 has a second path that
sits past its own `pop`: when the name object is null it zero-fills the
buffer with a loop of eight turns writing four bytes each, then branches
back into the common tail. Left at eight with a 64-byte buffer it hands
the tail 32 bytes of uninitialised stack, and the game black-screens on
the boot logos, because that path runs before the title. A disassembly
that stops at the first `pop` never shows it.

Each panel was checked on screen through the mod folder on the end-game
save before the build: "Wisdom Boost EX" and "Mystic Juliante" whole in
the Skill panel, "Metal Pearl Slime" whole in the Library header, "Metal
King Slime" whole in the Monsters list. Anthony's plugin's five hook words
and four version probes are byte-identical in the new executable. Only the
update title changes; the base CIA and its patch are the thirty-second
build's. Pack, verification, install and the update xdelta redone.

## Thirty-fourth build, 2026-09-14: seven skill books round 25 missed (round 26)

The thirty-third build was never released on its own; this build adds seven
book renames to it and is what v1.3 ships. Round 25's list of books came
from a stem test for "guard", so books whose 2021 names never had that
stem slipped past. Each is now named after the skill it teaches, spelled
as the English skill table spells it, plus " Book": the rule Gemini
approved as round 25 C-i. "SPD Ward EX Book", "INT Ward EX Book" and "MP
Ward EX Book" become "Slow Ward EX Book", "Wisdom Ward EX Book" and "MP
Drain Ward EX Book". The four Mist SP books become "Red Mister SP Book",
"White Mister SP Book" (it also read "BOOK" with a trailing space),
"Netherworld Mister SP Book" (it read "Underwold Mist SP Book") and
"Sublime Mister SP Book" (it read "Clear Skies Mist SP Book"), matching
their base books, which round 9 had already renamed.

`_audit/round26.py` is round 25's script with only its table changed
(`_audit/proof_terms/round26.tsv`, 7 rows, 14 label writes across both
trees, refuter reviewed). None of the new names collides with another
item, and the widest, "Netherworld Mister SP Book", measures 132 units
against the 149 of "Quake & Gravity Ward EX Book", which the bag draws
whole.

Held back for a ruling, not changed: "Black Mist SP Book", because the
skill table names its skill "Black Mister+" while every sibling SP rank
reads "... Mister SP" and the book's own help line says "Black Mister SP",
so the table entry is probably the slip; and six stat "Up SP" books, whose
help lines name the rank-3 skill while the Japanese rank maps to "... Boost
EX". Both need a wording decision, not a mechanical rename. The first
review of this round caught that two names had been taken from help lines
instead of the skill table; the table, which the rule names, is what the
final seven follow.

ItemMessage.mes lives in both titles, so both CIAs change and both
patches are regenerated. The executable is the thirty-third build's. Pack,
verification, install and both xdeltas redone.

## Thirty-fifth build, 2026-09-14: the books and mist names held back from round 26 (round 27)

Round 26 held back two things for a ruling, and measuring them turned up
two more. All four went to Gemini as round 27 and were approved as
recommended; this build adds them to the thirty-fourth and is what v1.3
ships.

A. The skill table named every mist skill set's SP rank "... Mister SP"
except one, "Black Mister+", the only place that string occurs. It is now
"Black Mister SP", and its book "Black Mister SP Book"; the book's help
line already said "Black Mister SP".

B. Each stat has four books; the Japanese ranks アップ１, ２, ３, ＳＰ are
Boost, Boost+, Boost SP and Boost EX in the English skill table. The six
fourth-rank books were still "X Up SP Book", and their help lines named the
third-rank skill, which a different book already teaches, while the
Japanese help lines name the fourth. They now read "HP Boost EX Book",
"MP Boost EX Book", "Attack Boost EX Book", "Defense Boost EX Book", "Speed
Boost EX Book" and "Wisdom Boost EX Book", with help lines to match.

C. The spell 青天の霧 is "Sublime Mist" in the action table and its skill
set "Sublime Mister", but the 2021 name "Blue" survived in eight labels:
the second of its two trait labels ("Chance Blue Mister"), the SP book's
help line, and the skill lists of six help texts. The SP book's help text
carried it twice, its Skill line and its list, and both are changed. "Blue
Mist" no longer occurs anywhere in either title. "Chance Underworld
Mister" stays, as ruled: every mist trait is named after the spell it
casts, and 冥界の霧 is "Underworld Fog" in 31 strings of each title.

D. "Shepard's Book" is "Shepherd's Book" (羊飼い; the skill is "Shepherd").

`_audit/round27.py`, round 25's engine with the table
`_audit/proof_terms/round27.tsv` (24 rows, 23 labels in each title),
refuter reviewed. No new book name collides with another item and the
widest, "Defense Boost EX Book", measures 112 units. The build chain script
was derived from the last one by renaming its log numbers; a blind
replacement would also have rewritten the update patch's xdelta window
(268435456), so the replacement is now targeted and the window checked.
Both CIAs change; the executable is the thirty-third build's. Pack,
verification, install and both xdeltas redone.

## Thirty-sixth build, 2026-09-14: help lines that named the wrong thing (round 28)

A check of every skill book's help text, "Skill: X" against the English
skill table, found sixteen mismatches after v1.3. They went to Gemini as
round 28 with the Pusugon spelling, and were approved as recommended with
two additions: the Vearn, the Beholder list says "Swelling Strike" for
パイルハンマー, as the action table does, and ＪＥＳＴＥＲ should follow its
species, "Jester". The second addendum is held back, see below.

A. The seven Ver.1.3 Dai collab books (IH1079 to IH1085) listed several
skills to a line, because the 2021 text was one flat line and the rebuild
re-broke it like prose. `_audit/round28a.py` rewrites each list one item
per line, cut at the Japanese item boundaries without changing a word
except "Pile Driver" in IH1080. Each list is ten lines, the most any of
the other 532 book help texts has, and the widest line is 120 units
against 147 for the widest line already shown in that window.

B to E, `_audit/round28.py` (round 25's engine, `_audit/proof_terms/
round28.tsv`, 17 rows, 16 labels in each title): four help lines say
Blunt Ward and Sap Ward; the recovery SP skills lose their plus and their
books follow ("Cure-All SP Book", "Purifier SP Book", "Mage's Aid SP
Book"); ＪＯＫＥＲ's book, help line and trivia say "Wildcard", and the same
trivia sentence names ＪＥＳＴＥＲ by its species name, "Jester"; "Pusugon the
Monstrous", and its book "Pusugon the Monstrous Book", which overrules
round 9's leave list for that one label as the verdict says. Refuter
reviewed.

Held back from the verdict: ＪＥＳＴＥＲ's skill, book and help line stay
"JESTER". "Jester" is already the English name of another skill, the
遊び人 class skill taught by "Goof-off's Book" (help line "Skill: Jester"),
and the review package had not said so; renaming would give two skills one
name. It goes back to Gemini with that fact.

Found while checking this round and NOT changed (outside what was ruled):
"Pile Driver" still names パイルハンマー in ten more help texts of the
update (five book, five skill-set), "Attack Ward+" and "Defense Ward+"
name 攻撃力ガード＋ and 守備力ガード＋ in 34 more, and the seven collab skill sets' own help texts (SkillHelp0579 to
0585) are each still one flat line. They are the next round.

Both CIAs change; the executable is the thirty-third build's. Pack,
verification, install and both xdeltas redone.

## Thirty-seventh build, 2026-09-14: the rest of those help lists (round 29)

Checking round 28 turned up the same defects in strings it had not
listed. They went to Gemini as round 29 and were approved as recommended.

A. The JESTER question from round 28: no change. ＪＥＳＴＥＲ's skill and
book stay "JESTER", because "Jester" is the 遊び人 class skill (and its
spell "Jester's Jig"); the capitals tell the two apart.

B. The seven collab skill sets' own help texts (SkillHelp0579 to 0585,
shown in synthesis under Inherited Skills > Info) were each one flat line
in English against
ten lines in Japanese. `_audit/round29a.py` (round28a.py aimed at
SkillHelpMessage.mes) rewrites each one item per line at the Japanese item
boundaries. One word changes: SkillHelp0580 "Pile Driver" becomes
"Swelling Strike". Held back: the verdict also asked for the Brass list's
"Fullheal" to become "Moreheal" (the Japanese is ベホイマ), but the same
"Fullheal" for ベホイマ is in 22 more help texts the package had not
listed, and changing one would make the game less consistent, not more.
All 23 go back to Gemini together. Each list is ten lines, the most
any other skill-set help text has, and the widest line is 111 units
against 120 for the widest line those texts already show. On screen
(2026-09-14) the text turned out to live in synthesis, Inherited Skills,
Info (Y) on a skill set; Library > Skill and Allocate Skill Points draw
their lists from the skill table instead. A ten-line list (Muspell) fits
that box with its tenth line whole. The collab lists themselves were not
seen there: the test save has no stored monster carrying one.

C and D. `_audit/round29.py` (round 25's engine, `_audit/proof_terms/
round29.tsv`, 43 rows, 43 labels in each title): "Pile Driver" becomes
"Swelling Strike" in nine more help texts, the action table's name for
パイルハンマー, and "Attack Ward+" / "Defense Ward+" become "Blunt Ward+" /
"Sap Ward+" in 34 help-list lines, the skill table's names for 攻撃力ガード＋
and 守備力ガード＋. The new names are shorter, so no line grows. None of the
three old names is left in either title. Refuter reviewed.

Both CIAs change; the executable is the thirty-third build's. Pack,
verification, install and both xdeltas redone.

## Thirty-eighth build, 2026-09-15: Moreheal, and the 18-character Teaches column (round 30)

Round 30 went to Gemini with the one word held back from round 29 and a
name cap found while checking v1.5. Both approved as recommended.

A. `_audit/round30.py` (round 25's engine, `_audit/proof_terms/
round30_A.tsv`, 23 rows): "Fullheal" becomes "Moreheal" in 23 help lists
of the update (ten book help texts, thirteen skill-set help texts) and the
same 22 of the base title (SkillHelp0584, Brass, is update-only). In every
one the "Fullheal" line stands where the Japanese line reads ベホイマ, and
the action table names ベホイマ "Moreheal" (A065) and ベホマ "Fullheal"
(A602), which stays. "Moreheal" measures 44 px against 36; no label's
widest line changes. The only "Fullheal" left in either title is A602.
Refuter reviewed.

B. A skill set's Teaches list, the top screen of Allocate Skill Points and
of Library > Skill, cut every action name at 18 characters. The row
builder at 0x3bd0b4 handed the icon+name formatter 0x22f818 a stack
buffer of 21 characters: two icon codes, 18 letters, the NUL. Five words
in `codepatch.py` grow its frame 0x48 -> 0x88, move the buffer into the
new space at sp+0x48 and raise the capacity to 32 characters; the longest
real action name is 23. Found with a read watchpoint on a stored name and
a stack walk; seen whole on screen from a fresh boot. Eleven action names
were affected; "Essence Drain Ward+", counted as a twelfth in the review
package, is a trait, and trait rows skip that buffer. The formatter has
thirteen other callers that also pass 21; they draw other screens, were
not identified, and are unchanged. The record is `_audit/NAMECAP_18_LIVE.md`.
The executable now has sixty-five changed words (md5 e8fa730f...).

Seen on the shipped CIAs from a fresh boot on the end-game save:
Gome-chan's Teaches list under Allocate Skill Points shows "Giga
Essence Extractor" and "Miracle of the Stars" whole, and Wild SP Book's
help list reads "Moreheal".

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Thirty-ninth build, 2026-09-15: the other screens that cut action names at 18

The icon+name formatter behind v1.6's Teaches fix (0x22f818) has thirteen
other callers, and every one handed it a 21-character buffer. A screen
hunt on the end-game save, one-shot breakpoints on all thirteen
(`_audit/hitlog.py`) while walking the menus, a battle, the field ability
menu and the Library, placed five of them:

| Function | Screen | Cut in v1.6 |
|---|---|---|
| 0x429a5c | Library > Abilities rows | yes ("Combustive Rending", "A Dark, Cold, Plac") |
| 0x3be878 | a monster's skill pages (status screen, battle Swap) | yes ("Giga Essence Extra", "Miracle of the Sta") |
| 0x5f8ad8 | Info header in the field ability menu | not seen (field spells are short) |
| 0x5f88fc | the field ability menu's list | not seen |
| 0x57a348 | the chosen-ability row above Use / Cancel | not seen |

Each buffer becomes 32 characters and each frame grows to hold it, the
same fix as 0x3bd0b4: 21 words in `codepatch.py`, 86 in all (md5
c11419c5...). The last three only ever show field-usable spells; they are
fixed anyway because the change is small and the field-usable list was not
checked against every long name. Refuter reviewed. Seen whole on screen
from a fresh boot; a battle and the field menu ran normally.

Not capped, checked on screen: the battle Orders list, its Info window and
the action banner. Not placed, unchanged: 0x22fa68, 0x385dd4, 0x385f00,
0x38616c, 0x3c1394, 0x3c1584, 0x3de964 and 0x426fec; the strings near
them suggest online, StreetPass, Ride Fuse and pop-up screens, but nearby
strings misled twice during the hunt. `_audit/NAMECAP_18_LIVE.md` has the
record.

No text changed. Only the update CIA changes; the base CIA and its xdelta
are byte-identical to v1.6's.

## Fortieth build, 2026-09-15: the skill-point hint, and round 31

A last pass on the unplaced callers of the icon+name formatter (StreetPass
Battle from the title screen; a skill book used on a party monster, then
Allocate Skill Points) placed one more, and it was the worst of them. The
line under the skill-point counter ("Learns:" or "NN SP unlocks:") cut
every ability name at 10 letters. The name wrapper 0x22fa1c formats into a
21-character buffer, and this caller asks for coloured icons, whose colour
codes take 10 of the 21. Five words in `codepatch.py` give it a 40-
character buffer (29 letters after the icons) in a frame grown to hold
it; 91 words in all (md5 141afb82...). Refuter reviewed; seen whole on
screen from a fresh boot, and the "has learned" pop-ups still work.
`_audit/NAMECAP_18_LIVE.md` has the record, including the seven callers
still unplaced (online, StreetPass match-ups, Ride Fuse and one more).

Round 31 (`_audit/round31.py`, `_audit/proof_terms/round31.tsv`), Gemini
verdict A-i, B-i: A634 (闇獄凍滅斬) "A Dark, Cold, Place..." becomes "A
Dark, Cold Place...", keeping the 2021 phrase without the comma before the
noun; I0230 (破毒のおまもり) "Amulet of Clensing" becomes "Amulet of
Cleansing". Both labels in both titles, nothing else names them. Refuter
reviewed.

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-first build, 2026-09-15: Ride Fuse, and one name for it (rounds 32 and 33)

The last hunt for the short name buffer reached the Ride Fuse screen. Ride
Fuse needs no special pair: in battle, Ride on one party monster, then Ride
on the other with Nochorin, and the command unlocks; its Fusion Info screen
has its own builders. Four callers of the icon+name formatter were placed:
0x3de884 (the Unify Ability line), 0x385bb4 and 0x385f68 (the ability
pages), 0x426ed0 (the Info window in Allocate Skill Points); a fifth,
0x385e6c, has no callers at all. Each buffer stays where it is and its
frame grows to hold 64 bytes, capacity 21 -> 32: 16 words. Refuter
reviewed; seen whole on screen. Only the two StreetPass match-up callers
(0x3c1394, 0x3c1584) were never reached; they need data from another
console, and are unchanged. `_audit/NAMECAP_18_LIVE.md` has the record.

Round 32 (Gemini verdict A-i, B-i, C-i). A: `_audit/round32.py` and
`_audit/proof_terms/round32.tsv`, 36 rows, plus `_audit/round32a.py` for
one tutorial page rewritten whole so its sentences keep their lines: 合体
is "fuse" / "fusion" everywhere, "Ride Fuse" stays the battle command; the
Fusion Info labels, the AI and stay-fused settings, the battle banner, the
three help titles, the AI help page, six tutorial pages and three event
lines (the Full Charge monument hint, and the Scout-Q #2 message, which now
names the trait 合体上手 by its name, "Fusion Expert"), 36 labels in the
base title and 27 in the update. B: the Ride menu's "Ride with Nochorin." /
"Dismount with Nochorin." become "Nochorin Rides" / "Nochorin Dismounts".
C: a fused monster's name was built from a format string in the
executable, u"合体%ls", so Fusion Info and everything else that prints it
showed "合体Qu"; three words make it u"%ls", and one more raises the name's
capacity from 10 to 11 letters, the full length of a monster name.
Refuter reviewed.

A scan of the executable for other built-in Japanese found five strings.
"チュートリアル" and "ヒント" are referenced by nothing, "不明" sits in a
table of battle-script paths as a fallback, and "プレゼント" belongs to the
Present Code screens; they are left. The fifth, "よろしくおねがいします!",
is the default StreetPass profile comment.

Round 33 (Gemini verdict A-i, B-i, C-i, D-ii, E-i). A: seven words in
`codepatch.py` make that default comment "Hello there!", the most its
twelve-character slot holds. B to D: `_audit/round33.py` and
`_audit/proof_terms/round33.tsv`: HelpMessage4100 to 4102 (合体モンスターの
種族名) say "Fused monster's family" instead of "Sort by monster family
type" (they were not seen on screen; the Attempt Fusion result shows no
family page); the Liquid Metal King's bestiary entry follows the Japanese
(its drops become countless Liquid Metal Slimes; it is proud of its
stamina, 体力) in four lines; the event line that sums up Full Charge says
"You learned Full Charge, Ride Fuse and Attempt Fusion!". E: 合体解除 stays
"Split". The executable now has 118 changed words (md5 49ff105d...).
Refuter reviewed.

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-second build, 2026-09-15: the meaning pass (rounds 34 to 39)

Every translated string that differs from the Japanese was compared with
it for meaning, in four layers: the bestiary (737), the other descriptions
(2,725: traits, abilities, skill trees, help, items), the story and field
dialogue (6,367) and the other text in Message/ (2,734). A first reader
flagged possible errors per batch of 50 (`_audit/meaning/SPEC.md`); a
second judged each flag with the scene or list in view and drafted the
correction, measured against its box with the game font
(`_audit/meaning_fit.py`, `_audit/meaning_dlg.py`). Two scripts checked
what readers miss: every skill-tree and skill-book line against the
ability and trait tables (`_audit/meaning_skilltree.py`), and every name
the Japanese uses against the English (`_audit/meaning_names.py`).

Rounds 34 (bestiary, 251), 35 (descriptions, 211, and the skill-list
names), 36 (monster names against the Dragon Quest Wiki), 37 (dialogue,
695 plus 74 identical copies) and 38 (the rest, 416 plus 11 copies) went
to Gemini and were approved, with seven wording tweaks. Round 36: the
patch's names are official for most monsters that have one; サウルスロード
and バザックス had each other's (Terrorceratops and Tyrannoceratops) and
are swapped back; グランエスターク is Gran Estark everywhere; the other
fan names stay.

Round 39 applies all of it: `_audit/meaning_round39.py` turns the approved
drafts and the name passes into exact whole-label rewrites for both trees
(`_audit/proof_terms/round39.jsonl`, 3,864 rows), and `_audit/round39.py`
writes a label only if it still holds its expected text. It runs after
tipsflow.py; wrapdialogue.py and tipsflow.py then run again. Dialogue is
wrapped in the generator with the player's name measured at 11 wide
letters, so the second wrap changes nothing and no rewritten line exceeds
the 346 px window. Identical lines drafted twice take one wording. The
name passes: skill lists use the table names (360 lines); 魔界 is Demon
Realm where the Japanese has it (冥界, the netherworld, stays); Network
Coins where it has 通信コイン; the disc keywords Land / Sea / Sky where it
has 陸神討伐の and its siblings; Sirloin Bites / Voucher, Sea Map Fragment,
Incarnus' Stone, Phantomount, Unfinished Shrine, Malroth. Refuter reviewed
five times (four reworks: names split across a line break, name width in
the wrap, a skill-book stat line, a page-break newline, 魔界 variants,
spacing at colour codes). `verify_pack.py` now accepts a label round 39
rewrote whole if its old misspelling is gone (two bestiary entries no
longer use the fixed phrase at all). Labels changed against v1.9: 2,728 in
the base title, 1,136 in the update. The executable is unchanged (118
words, md5 49ff105d...).

Seen on screen, shipped build, fresh boot on the test save: the Slime's
bestiary entry, Ultra Body and Dizzying Body, the Material+ skill tree,
Helpful Tips 3 and 5, and the tactic list's "Don't use Abilities". Not
seen: story dialogue, trophies, the diary, the StreetPass prompts.

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-third build, 2026-09-15: the meaning pass's leftovers (round 40)

Round 40 (Gemini: A-i, B-i, C-i, D-i, E-i). `_audit/meaning_round40.py`
writes `_audit/proof_terms/round40.jsonl` (83 rows) against the finished
v2.0 text and `_audit/round40.py` applies it right after round 39 (same
exact-text guard). A: 魔界の門 is the Demon Realm Gate in every label whose
Japanese has it, in any case and as "phantom door" too; DEMO_910_MSG_002
(page 1 has only 門), DEMO_921_MSG_017 (魔界への扉) and DEMO_923_MSG_002
(門) are worded from their Japanese. B: the speaker tag NAME_TAG_DEODORA
is Madame Rummy (official in Dragon Quest Monsters: Joker, where デオドラン島
is Palaish Isle). C: the かしこさガード / 賢さガード trees and books are Dumb
Ward, Dumb Ward SP, Dumb Ward EX. D: PartnerNotyorinBattleInfoTitle01/02
take the order names; seen whole on the Nochorin Ally page. E: six lines
(DEMO_312_MSG_050, DEMO_323_MSG_090, DEMO_210_MSG_070, D02_35 GUIDE_MSG_001,
I01_01 NPC_GOST_REC, IH1013). Word swaps keep their line's own layout while
it fits (the warp prompts keep two lines). Refuter reviewed twice (one
rework: the gate pass was case-sensitive). Labels changed against v2.0: 69
in the base title, 14 in the update. The executable is unchanged.

Seen on screen, shipped build: the Nochorin Ally page, Library > Summary
(Fiery Volcano and Demon Realm, including the 《Demon Realm》 header) and
the ward trees under Library > Skill.

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-fourth build, 2026-09-15: the UI labels, a second look, the partner lines (round 41)

Round 41 (Gemini: A-i, A2 by the screen, B-i, C1-i, C3-i, C4-i, the C rows,
D-i). `_audit/meaning_round41.py` writes `_audit/proof_terms/round41.jsonl`
(406 rows) against the finished v2.1 text and `_audit/round41.py` applies it
right after round 40 (same exact-text guard). A: 83 UI labels, 2 copies (the
LayoutMessage buttons, headers and explainers, status, location, area,
habitat, disc and trophy words; 2,279 strings read). A2: the model viewer's
rotation labels stay as shipped (seen on the rig: pushing the circle pad
left turns the model's face to the viewer's left; the Japanese names the
same turn from the model's side), and 人目 is "P". B: 65 corrections from
a 600-line recall sample of the lines the v2.0 pass had passed, and 9
identical copies. C: 9 hand-drafted consistency rows; C1 ＪＯＫＥＲ is
Wildcard (9 labels by the word pass); C3 SPD is AGI (28 labels); C4 the
"slightly" of the all-enemy stat items stays. D: 28 partner lines. Three
drafts were narrowed to their panes ("Foe #1/#2" in a 36 px pane, " Mon."
after a count) and one line break moved so a swapped name fits. Refuter
reviewed twice (one rework: the word passes missed "SPDgain", a half-width
JOKER and ActionHelp308, and two tips lost their blank line). Labels changed
against v2.1: 275 in the base title, 131 in the update. The executable is
unchanged.

Seen on screen: on the shipped v2.1 build, the model viewer's rotation
labels (the A2 ruling); on the shipped forty-fourth build, "Foe #1" and
"Foe #2" whole on the bestiary page and the list header "Unlocked".

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-fifth build, 2026-09-15: the second read (round 42)

Round 42 (Gemini: A-i, B-i, C-i), ruled E-ii in round 41: every line the
first meaning pass had passed (9,727, the recall sample left out) read again
for medium and high errors only, then judged and drafted with the scene or
list in view. `_audit/meaning_round42.py` writes
`_audit/proof_terms/round42.jsonl` (546 rows) against the forty-fourth
build's text and `_audit/round42.py` applies it right after round 41 (same
exact-text guard). 261 corrections (121 dialogue, 34 descriptions, 106 system),
13 high, and 2 identical copies. IH0848 had no draft text and takes two
word fixes on its list (Fizz for ザバ, INT for かしこさ); seven Information
tips drafted as flat text are split back into their shipped paragraphs.
Refuter reviewed. Labels changed against the forty-fourth build: 386 in the
base title, 160 in the update. The executable is unchanged. The
forty-fourth build (round 41) was not released on its own.

Seen on screen, shipped forty-fifth build: Helpful Tips 7 (Monster
Recovery), its two paragraphs and the restored "HP and MP".

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-sixth build, 2026-09-15: loose ends before v2.2 (round 43)

Round 43 (Gemini: A-ii, B-i, C-i, C2-i, D-i, E-i, F-i, G-i, H-ii, I
approved). `_audit/meaning_round43.py` writes `_audit/proof_terms/round43.jsonl`
(73 rows, 34 strings) against the forty-fifth build's text and
`_audit/round43.py` applies it right after round 42 (same exact-text
guard). A: 思い出の戦い is "Battle Memories" (10 strings, the menu labels
included). B: 本屋 is "the Book Shop" (19). C: the Fighting Spirit tip.
D: DEMO_901_MSG_001_2. E: BattleEventMessage580. F: TICO_SUMMON_042.
G: Scout-Q #8 (1). H-ii: nine lines whose opening control code differs
from the Japanese are left for an emulator check (round 44). Refuter
reviewed. Labels changed against the forty-fifth build: 41 in the base
title, 32 in the update. The executable is unchanged. The forty-fourth and
forty-fifth builds were not released on their own: v2.2 is this build.

Seen on screen, shipped forty-sixth build: Helpful Tips "70. Manage
Favorites" and 74 (Training), its two paragraphs.

Both CIAs change. Pack, verification, install and both xdeltas redone.

## Forty-ninth build, 2026-09-16: rounds 44 to 51, the last of the meaning pass and the name consistency sweep

This build carries eight rounds. The forty-seventh and forty-eighth builds
(rounds 44 to 47) were packed and verified but never released on their own,
so v2.3 is this build and the eight rounds ship together.

Round 44 (Gemini: A-i, B-i, C-i, D-i, E-i) is a pass over control codes and
characters rather than wording. Eighteen field lines whose opening speaker
code did not match the Japanese are mirrored to it; those have not been seen
on screen, because the lines sit behind specific NPCs a test save could not
reach. Twelve strings of literal Japanese punctuation that renders on screen,
a corner bracket, an ideographic full stop, full-width brackets, are swapped
for their ASCII equivalents. Fifty-three strings carrying an oversized
ideographic space where a normal space belongs are narrowed. Four more lines
naming the Book Shop or its bookseller are brought in line with round 43.
85 distinct labels, 152 sites, 184 rows across both trees.

Round 45 (Gemini: A-i, B-i, C-i) is the 265 labels the meaning pass had
flagged but no earlier round had changed, read by six drafters in scene.
Twelve high severity lines had misled the player about the story or about
what to do: a boss's altar of sacrifice rewritten as kneeling before a "new
master", a door needing all three of Bundold's minions' keys turned into
three separate doors each needing one, a village guide's line dropping the
instruction to find the Prison Key. 110 medium severity lines soften, drop or
invent a smaller fact elsewhere. The model viewer's rotation labels, which two
drafters argued over on the text alone, are left as they are, because round 41
had already settled them by looking at the screen. 141 labels, 257 sites,
294 rows.

Round 46 (Gemini: B-i, C-i) finishes the meaning pass: the last 193 low
severity flags, read leaning toward keep because they had already been called
minor, plus six lines folded in from outside that pool so one fact does not
end up worded two ways. Five medium fixes and 51 low severity shades of
meaning, among them six Incarnus Altar location labels that now all read the
same way rather than one of the six carrying the fix. 51 labels, 103 sites,
112 rows.

Round 47 (Gemini: A-i, C-i, B settled by A, D-ii) is the reflect family in the
battle messages. Ten one-shot reflect effects are marked "x1" so they read
differently on screen from the kind that lasts, matching a distinction the
status list already makes. Seven "wore off" lines take the form round 43 had
settled for that file. D-ii is a ruling not to act: the Scout-Q quiz's two
askers are written with different voices in the Japanese and are left alone in
English, because a player only ever meets one of them and telling the two
apart would mean inventing fifty lines of dialogue. 17 labels, 17 sites,
34 rows.

Round 48 (Gemini: A-i) is the mirror of round 47: 87 Japanese strings in the
menus, help text and item and trait descriptions that carried two different
English wordings with no speaker to excuse it, one wording chosen per group by
four drafters. A trait's evasion bonus no longer reads "really easy" where the
Japanese carries no intensifier; an item that is a scroll in nine other item
names stops being called "documents" in the one label that still had it; and
"during a match" is dropped from two settings lines that had invented it.
133 labels, 133 sites, 261 rows.

Round 49 (Gemini: A-i, B-i, with B-ii settled as Shadow Noble, Rhapthorne,
Malroth and Orgodemir) is what round 48's own twelve-character floor had
hidden underneath it: the short interface strings, monster names and skill
names. 133 labels were judged legitimately different by context, ATK in a
narrow stat column against Attack as a battle command, and kept with a stated
reason; 36 more are unified. The round's own finding is that the monster table
lists 89 Japanese species names at two ids each, 77 of which already carry the
same English at both, so the 12 that did not are drift rather than intent.
Those were settled by which English form the shipped game actually uses more
often, with four pairs left to Gemini where no measurement pointed either way.
36 labels, 36 sites, 67 rows.

Round 50 (Gemini: A-i, B-i) corrects an over-application of round 47's D-ii
ruling by me. Of the 117 groups D-ii had waved through on the grounds that a
different character can justify a different wording, sixteen turned out to be
narration and examine text where nobody is speaking, so the excuse does not
hold. All sixteen groups are unified. B-i settles the battle tactic round 49
had pulled out: "Psyche Up" on both the menu and the panel, since the shorter
Japanese term is rendered "Psyche Up" in twelve other strings against "Tension
Gather" in this one label alone, and its sibling tactic already agrees across
both screens. 29 labels, 83 sites, 96 rows.

Round 51 carries no Gemini package and needed no new ruling. It exists so that
round 49's own casing decision does not create a split. Round 49 had settled,
measured tree-wide, that this game writes "Max HP" and "Max MP" rather than
"MAX" (628 against 4, and 857 against 3) and changed four battle messages to
match. Five labels carrying the same Japanese as those four sat outside round
49's pool: the two status list entries for the same two effects, and three
item help lines. Left alone, the battle log would have read "Max HP Down"
while the status screen read "MAX HP Down" for the identical effect. 5 labels,
5 sites, 8 rows.

Across the eight rounds 492 distinct labels change over 780 file-and-label
sites and 1,056 rows. The rows run higher than the labels because they count
the base and update trees separately and because the game ships duplicate
Field/ and Script/Field/ copies of the field scripts; five labels are rewritten
by two different rounds, which is why the per-round label counts add to 497
rather than 492. By tree: 489 labels over 777 sites in the base title, 269
over 269 in the update.

The chain's own byte diff against the forty-eighth build, which already held
rounds 44 to 47, reports 255 labels changed in the base title and 177 in the
update; that figure covers rounds 48 to 51 only, and is a different
measurement from the label counts above.

Every round applied with 0 problems, and wrapdialogue planned 0 writes
afterwards, which is what confirms the two strings round 50 writes out
literally are not re-wrapped and re-glued. verify_pack verdict OK on both
trees, xdelta round-trip OK on both patches.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  029c1ebf2d65c54657f6f7e2c4e384e3ff5e71dc917acdf20c0ec70b89368095
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  c795f16f7b60439cc4cf7233dad0aadef03fc3b7cea1abaa80b7e36b0242a2fb
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,787,425  5f8ca48fdd68871d8f10f604090615a1fd7eb738a3a8b0949195b686b65c3608
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            5,681,736  1c21222c15d835ba903235e27e4dcca45dc50dd10998b2b61288d56efab1ad60

The executable is unchanged, and its changed-word count is corrected here: 117
words differ, not the 118 the earlier sections of this file and the README
carried. 118 is the number of rows in the patch table, one of which writes a
value the code already held. The md5 49ff105d is unaffected. Both CIAs change, so pack,
verification and both xdeltas were redone.

## Fiftieth build, 2026-09-16: a species is not a family (round 52)

Round 52 (Gemini: A-i, B-i, C-i, D-i, on GEMINI_DQMJ3PRO_ROUND52B.md). v2.3
had not been published when this was found, so it ships inside v2.3 rather
than as a release of its own.

This game keeps two separate ideas that the English had tangled. There are
nine monster families, MK1001 to MK1009, Slime, Dragon, Beast, Nature, Demon,
Undead, Material, Break and ???, each written in Japanese with the same
suffix. There are 1,024 species in MonsterKindMessage.mes. Japanese uses one
word for the family and a different word for the species. Sixteen labels used
the wrong one: the status screen, the rules panel and the Reactor's analysis
called a species a "Type"; the Library heading, the fusion panel and three
fusion help lines called it a "Family"; and the community rules error said it
restricted entry by "species" when the Japanese restricts by family.

Two pieces of evidence settle it, either sufficient alone. HelpMessage1129
carries both Japanese words in one rule and the 2021 patch rendered them
correctly and distinctly, which is why that string is deliberately left
untouched. And the Manage Favorites milestone says "over 20" of the species
word, which is an ordinary target for species and impossible for families.

Also left alone: MenuMessageSameKind, which already read "the same species",
and the three labels whose Japanese is a third word again and correctly read
"Type", one of which round 49 filled from blank.

Two of the rewritten lines could not take the longer word in their existing
line breaks, so they are re-wrapped and measured rather than left to overflow:
the free-battle warning in a 140 px box and the Manage Favorites milestone in
a 168 px box. wrapdialogue planned 0 writes after the round, which confirms
nothing was re-broken behind them.

One label to watch on screen: the rules panel label goes to 36 px where its
Japanese was 30 px, the only string in the round wider than the Japanese its
pane was built for. The fit checker passes it, but the checker measures the
label and not the pane, so it is listed in TESTING rather than called verified.

Round 52 alone: 16 labels, 16 sites, 31 rows (base 16, upd 15). Across rounds
44 to 52 v2.3 now changes 506 distinct labels over 795 sites and 1,087 rows;
7 labels are rewritten by two rounds, so the per-round counts sum to 513
rather than 506. By tree: 503 labels over 792 sites in the base title, 283
over 283 in the update.

A first package for this round, GEMINI_DQMJ3PRO_ROUND52.md, asked the question
with the two words the wrong way round and was ruled on that framing. It is
kept as the record and none of it is applied; the corrected package is
GEMINI_DQMJ3PRO_ROUND52B.md.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  829f3cf8bc43bdf4b71a911d4e8ace7bd7d67f10298382d8208ff46911b93bf6
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  df3403080c649a9722dbadcc427ee99239bbfa9d7a9d1fba29da79ca97674aef
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,787,564  48dcc88c67cdec077a1ae31496fe28a7eeb7963dec561a5562df9ccb216223c8
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            5,681,755  5f388458d32c7ff5dd0fb30ad8ee663d87776d56905ecbcd38d042688b9793f8

The executable is unchanged at 117 words. Both CIAs change, so pack,
verification and both xdeltas were redone.

## Fifty-first build, 2026-09-16: undo one thing round 49 got wrong (round 53)

Round 53 is a regression fix, not a new ruling, and it was found by playing
the build rather than by any check in the toolchain.

Round 49 found one layout label blank in English where Japanese retail has
text, and filled it with "Type". That slot is a counter suffix rather than a
heading: Japanese writes "385 of these kinds" as one run, and English puts a
bare number there. The game concatenates its own runtime number straight onto
our string with no separator, so the Library Collection page came out reading
"385Type", "308Type", "52Type" in seven places. The 2021 patch was right to
leave the label blank, and round 53 puts it back.

Nothing static could have caught this. Both halves are individually correct
and the join only exists at draw time, so the width checker never sees the
number sitting in front of our text. Every other round from 39 to 52 was
checked for the same shape: this is the only blank any of them filled.

The two sibling labels carrying the same Japanese, in the sort menu, are
standalone options where "Type" is the right English and are untouched.

Because one of round 49's 36 unified labels is reverted, the settled short
string count in the release text moves from 169 to 168.

Round 53 alone: 1 label, 2 rows, one per tree. Across rounds 44 to 53 v2.3
changes 505 distinct labels over 794 sites and 1,089 rows, counting net change
per label so a label put back to its shipped value is not counted as changed.

Still present and NOT fixed here, seen on the same screen: the Speed Road
totals read "880Poi/nt", because the point counter suffix ships as "Point"
while its sibling ships as "pt". That one is a 2021 defect rather than ours
and is a wording choice, so it goes to review rather than into this build.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  41817cb1ccf03b65954e2909e8a6c943d04e9c17cb2991b31761d6cbda4c4c01
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  20d975e8f8a73753509a74dc91f73d9dee64868a5e52d5d6e8bca01dde727969
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,774,164  000670fa93d4520d0b3b8360ce8f605aa7aebb347ff2970b717d82d77acce42e
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            5,681,761  2af07ccf6eb4fe37fd06d775be53a37feda97e0afc02aa025b263edb9b53097b

The executable is unchanged at 117 words. Both CIAs change, so pack,
verification and both xdeltas were redone.

## Fifty-second build, 2026-09-16: two counters (round 54)

Round 54 (Gemini: A-i, B-i). Neither defect is ours. Both have been in the
English patch since 2021, and both were found by playing the fifty-first build
on the same Library screens that exposed our own round 49 regression.

A. Library > Speed Road rendered "880Poi" with "nt" pushed onto the next line.
The game writes its runtime number and then the label immediately after it,
with no separator, and "Point" came to 42 px with the number where the field
was built for the Japanese at 33 px. The game already answers this itself:
there are three labels for this counter, and the third, on the race screen,
already shipped "pt" with its Japanese being literally "pt" rather than a
Japanese counter. So "pt" follows the title's own convention instead of
inventing a house style, and lands at 28 px. That third label is untouched,
and the generator asserts it still reads "pt" in both trees.

B. Library > Records counted "# Stealth Box's Found", an apostrophe in a
plural. It reads "# Stealth Boxes Found". A tree-wide sweep confirmed it was
the only label of that shape rather than the first of many.

Left alone on purpose: the Records page mixes "# of Wins" with "# Victories",
and the Japanese varies between its two counter forms in the same way, so the
English is arguably following it. Sixteen labels, cosmetic, not worth a sweep.

Round 54 alone: 3 labels, 6 rows. Across rounds 44 to 54 v2.3 changes 508
distinct labels over 797 sites and 1,095 rows, counting net change per label
so a label put back to its shipped value is not counted as changed.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  d6c89cf0abe76de186d7147c13930589bff10944436c582a2a9d2f02b8bbca12
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  4416c1b7c9a04e97e027929c8173376beae453a42946959a6dc4f106ac9a22a5
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,774,099  383b00c700ea3f2a50f00e9f55e88df662c22487b6e82a36c9124b3848a8126f
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            5,681,767  a05e2537c90316b6d1bb984683e73c6187ba6235e60465c3dd2a3b4cfa184fab

The executable is unchanged at 117 words. Both CIAs change, so pack,
verification and both xdeltas were redone.

## Fifty-third build, 2026-09-16: a number and its unit (round 55)

Round 55 (Gemini: A-i). One label, and the sweep behind it is the reason it
exists at all.

The partner's Go Scout menu listed its errands as "5min", "15min", "30min".
The engine writes the number and our unit lands straight against it. That is
the same shape as two defects already dealt with in this release, one of ours
reverted in round 53 and one of the 2021 patch's fixed in round 54, but unlike
those two this one fitted and did not overflow, so it was a question of style
rather than a defect and went to review rather than being settled here. It now
reads "5 min".

A correction to the evidence, because the first version of this section had it
wrong. "30 min" is 31 px and the Japanese it replaces is 27 px, so the English
here is 4 px WIDER than the Japanese footprint, not narrower. An earlier draft
of this section said 33 px, which is the point counter from the round 54
section above and belongs to a different field. The ruling is unaffected: the
review package carried the correct 27 px and the decision was taken knowing
the English would be wider. What makes it safe is the pane rather than the
Japanese: the value is right aligned in a 120 px box and was seen on screen
with a wide gap before it.

Two sweeps stand behind it, because the one label was never the point.

The first covers strings where one of our own format slots touches a letter
with no separator. It was run with a 40 character limit and only over the
Message tree, and the section as first written claimed it covered everything,
which it did not. Re-run without either restriction: 70 distinct labels tree
wide, of which 60 are a unit or marker the Japanese writes flush too ("%lsG"
for gold, "Lv%ls", "x%ls" for a quantity, "%lsW %lsL" for a record) and are
left alone. The limit hid two real defects, which round 56 fixes.

The second covers the shape that actually produced all three instances, and
which no static check can see: the label holds no slot at all, and the engine
writes a number in front of it at draw time. Nothing in the string says so.
The best available proxy is a label whose entire Japanese is a bare counter,
one of the characters that only ever follows a numeral, against an English
word. Five exist. Two are the point labels round 54 fixed. Two are sort menu
options that are standalone rather than appended. The fifth already ships with
a LEADING SPACE and renders correctly, which is what settles the question: the
2021 patch had already solved this once, and round 55 is finishing a standard
it set rather than importing a new one.

The proxy is a filter and not a proof. All three real instances were found by
playing the game, and a label whose Japanese is not a bare counter could still
be appended to something.

Round 55 alone: 1 label, 2 rows. Across rounds 44 to 55 v2.3 changes 509
distinct labels over 798 sites and 1,097 rows, counting net change per label
so a label put back to its shipped value is not counted as changed.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  0fe1cdcbd29ce066c636a6f87667539cddc35c789ed184ea8c3157f5188557e3
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  f9128ee5c654b3d4e9c87f7c6cd8f285b53d54f3569383cc2d470541056a36f3
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,774,081  8b55f093c4be8fe240799aef8ebb2a5f9f6b993a7be835562465e411fbadf9e2
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            5,681,704  89bcb651561384c120891e52cd42f3aff80bdcfffa713bc5cdd9a46b6cc6d060

The executable is unchanged at 117 words. Both CIAs change, so pack,
verification and both xdeltas were redone.

## Fifty-fourth build, 2026-09-16: two words that ran into a name (round 56)

No ruling. These are missing spaces producing broken English rather than
wording calls, and both have been in the patch since 2021.

A disc prompt read "Use" with the disc name jammed onto it, so a player saw
"UseSunken Ruins Lv3 and freely roam within the disc world?". And Don Mogura,
handing over a reward, said "I will grant youGold Ring." In both the engine
writes the name where our sentence leaves a slot, and the space in front of
that slot was missing.

How they were found is the point. The round 55 sweep claimed to cover every
string where one of our slots touches a letter. It did not: it capped strings
at 40 characters and walked only the Message tree, and both of these are
longer than 40 characters, one of them in a field script. A reviewer refused
to accept the figure that sweep produced, which is what sent me back to run it
properly. Without that, both would have shipped in a release whose own notes
boast about fixing this exact class of defect.

Re-run over the whole tree with no cap: 70 labels where one of our slots
touches a letter. 60 are a unit or marker the Japanese writes flush too and
are left alone. These two are the only places in the whole tree where a WORD
runs into the value, which a second independent sweep confirmed. An earlier
draft split the remainder into "eight pure slot joins and two"; that split
is not reproducible from the rule as stated and has been dropped rather
than defended.

Both new strings are derived from the tree's own bytes by a targeted replace
rather than typed out, because both carry speaker and colour codes where a
transcription slip would be invisible. Neither goes through the drafting
helper, which re-derives whitespace around control codes from the original and
would have silently dropped the very space being added; that failure mode cost
this project a rebuild at round 50. wrapdialogue planned 0 writes afterwards,
which is the check that the spaces survived.

Round 56 alone: 2 labels over 3 sites, 4 rows. (2 label names; one of
them exists in the Script/Field and Field copies of the same field script,
and the other in both trees. An earlier draft of this line said "3 labels",
which counted sites, not labels.) Across rounds 44 to 56 v2.3 changes 510
distinct labels over 799 sites and 1,101 rows, counting net change per label
so a label put back to its shipped value is not counted as changed.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  8a8b585a70c8780f0bf18eb7bcf6f07fa93357856ffaf223de6c19a4140c24d2
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  5deec263ed182da42a2c8213220b1c3aa35e10d40413fb1b028a8d904099c490
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,774,026  1097e174bdefa4677169770753d660d28394d779e52df14de607b1ccfdbf2bb4
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            5,681,789  eafd370cd41bc06e331e229a4f037ca388be3a666a7acf0307991a0684e2f310

The executable is unchanged at 117 words. Both CIAs change, so pack,
verification and both xdeltas were redone.

## Fifty-fifth build, 2026-09-18: the player's name has a width, and the names are the series' own (round 57)

Three things, all measured rather than argued, and one of them is a bug in the
tool that was supposed to prevent exactly this.

**The player's name was measured as zero pixels.** `wrapdialogue.py` strips
every control pair before measuring, and the name token `\x01\u0201` is a
control pair. So every dialogue line carrying the name was wrapped one
name-width short, and at runtime the engine chopped it mid-word at the box
edge. Reported on Discord by isanthraxbayad, whose name is `Jesus`: the line
`Hmmm... [NAME] and Ace. You have both done an excellent job, as usual.`
measures 320 px empty and 347 px with the name, one pixel over the 346 px box.
695 deduplicated pages carry the token, and none of them was over the box with
an empty name, which is the proof that the measurement was the fault and not
the text.

The fix is `--name-reserve=adaptive`: each page is charged the widest reserve
it can take without gaining a rendered line. Three things had to be right, and
two of them were wrong first.

  1. The name holds 11 characters and the widest enterable glyph is `W` at
     11 px, so the worst case is 121 px. An earlier note assumed `M` at 8 px
     and would have reserved 88, which is 33 px short.
  2. The ceiling is the box, `LINES_PER_PAGE = 2`, not the page's current line
     count. Using the current count meant a one-line page could never become
     two, which silently refused to fix the reported line.
  3. `wrap_page` re-wrapped each existing line where it stood, so a page
     already broken in two could never rebalance: charging the name overflowed
     line 1, which split into a third line, and the search rejected the
     reserve. It now re-flows the whole page when keeping the existing breaks
     fails, and only then, so hand-placed breaks survive where they can. This
     one change took the failures from 104 pages to 2.

Measured on the built trees with `_audit/verify_namefit.py`, which counts the
lines as the file breaks them rather than re-wrapping them (an earlier version
re-wrapped, and reported the fix as having changed nothing):

| name substituted | v2.4 | v2.5 |
|---|---:|---:|
| 5 ordinary letters | 54 | 0 |
| 5 widest letters | 99 | 0 |
| 8 widest letters | 136 | 0 |
| 11 widest letters | 233 | 2 |

The two left (`DEMO_034_MSG_110`, `MSG_DEMO123_AFTER_KING`) take 114 px, ten
widest letters. Christopher is 56 px, Bartholomew 62, Maximillian 50, and even
eleven capital Ms is 88; only eleven capital Ws overflows them. Left alone.

**The monster names are the series' names now.** The authority is this game's
own bestiary list on the Dragon Quest Wiki, at the user's instruction: a name
not on that page does not go in the game. `bestiary_map.py` builds the pairs
from that page's own links, 709 of them. It has to read both `|japanese =` and
`|Japanese name =`; reading only the first silently dropped 91 monsters,
including Zoma, Estark and Pruslas. `mk_names_r57.py` then writes
`names_r57.json` and `rename57.py` applies it with `rename8.py`'s engine, which
only rewrites a mention in body text where the Japanese of that same label
proves which name is meant.

363 monster names changed. Eight were skipped as capitalisation churn, so
`She-Slime` is not rewritten as `She-slime`. 152 monsters have no entry on that
page and keep the name the 2021 translation gave them, which is unavoidable.
Four had been crossed with a different monster entirely: `Cavorting Column` is
the series name for ミステリピラー while ours is ミステリードール, which is Pocus
Poppet, and `Killer Wave` belongs to マッドウェーブ while ours is キラーウェーブ,
Thriller Wave. Barracuda and Quayhorse were the same mistake.

**The traits, and a reporter who was right about the word and wrong about the
target.** The report asked for "ward to crafty". Crafty is the series' English
for the katakana BREAK, not for GUARD: the wiki's "Crafty Breather" is break
breath. Measured in the shipped build, 42 traits are BREAK and were called
"... Break", and 58 are GUARD and were called "... Ward". So the 42 became
Crafty and the 58 were left, which is the opposite of what was asked for and
what the Japanese supports. Doing as asked would have introduced the defect.

**One more string.** `zenmetu` in `LayoutMessage.mes` read "Defeat All". The
Japanese 全滅する is intransitive, and the button is how you give up a boss
fight, so the English read as close to the opposite of what it does. It says
"Give up".

Scope of the rebuild against v2.4: 274 files differ in the base and 13 in the
update, nothing missing and nothing extra. Every one is a `.mes` under
`Message/`, `Script/Field/` or the `Field/` duplicate copies. No layout
archive, texture or executable byte changed, so nothing in this build can move
a pane.

Packed with `build.py`, then `smdhfix.py`, then `codepatch.py` on the update,
then `verify_pack.py`: base 13,955 files identical to its tree, update 127
identical, both verdict OK. The xdeltas were regenerated with
`build_xdelta_tolerant.py` and each proved four ways, against the real source,
two copies with the volatile bytes re-randomised and one with the whole scrub
area randomised.

## Fifty-sixth build, 2026-09-19: the wild monsters' names in battle (GitHub issue #1)

Reported on GitHub by are-gar about an hour before v2.5 went up, and older
than any of this: some monsters have no name in battle, only the letter that
marks one of a pair. The report was right, and the 2021 patch did it too.
Nobody had ever looked at a battle screen with a long-named monster in it.

**Where a battle name comes from.** A monster record is 0xf0 bytes and its
display name is a 24-byte field at +4, eleven UTF-16 characters and a
terminator, with the species id immediately after it at +0x1c. The battle
window's name panes (`battle_windows.bflyt`, `tb_mnsname_N_MM`) and the enemy
Status header draw that field, not the species table. Two writers fill it when
wild monsters spawn, `0x1d068c` for one record and `0x1d1a70` for a range, and
both measured the species name and, if it would not fit, skipped the copy and
left the field empty. Japanese species names fit. 438 of our 880 don't, so
every one of those drew nothing. The duplicate labeler `0x1d003c` then appends
`suffixA` to `suffixH` from `LayoutMessage.mes` to each record whose name
matches another's, and skipped for the same reason; empty plus "A" is "A",
which is exactly what the report's screenshots show.

**The fix, 36 words in the update's executable.** The two spawn writers copy
the first eleven characters and terminate, through the ARM `memcpy` at
`0x301a9c` that the labeler already calls. The labeler's length skip becomes a
nop and both its `wcscat` calls go to a thirteen-word routine written into the
two dead exception paths inside that same function, `0x1d00e4` to `0x1d011c`,
each of which sits behind a branch that cannot be taken: walk the name to its
end or to character nine, whichever comes first, then copy the suffix. The
eight suffix strings gain a leading space (round 58, both trees), so a pair
reads "Slime A" and a long pair "Halberdsa A", and nine plus two plus the
terminator is the twelve the field holds.

**Six of those words are a second pass, and the screen is what caught it.**
The cut keeps exactly nine characters, and 63 of the 880 species names have a
space as their ninth. A pair of them therefore rendered with two spaces,
"Mandrake  A", which reads as a typo rather than a label. The routine now backs
up over one trailing space before it appends the suffix, so it is "Mandrake A"
and "Deep Sea A" while "Halberdsa A" is untouched. The three extra words that
needed came from retiring the guard pair at `0x1d0100`, which the review had
already proved is always taken: the branch that fed it (`0x1d00e0`) now goes
straight to its destination, the region becomes fifteen contiguous words, and
the loop no longer needs its jump-over. The trim reads the halfword before the
field only if a name were empty, and no species name in the shipped data is
(144 are "-", the shortest real one is three characters), so the loop always
advances at least once first. Seen on the rebuilt discs: three Mandrakes
read "Mandrake A", "Mandrake B" and "Mandrake C", one space each
(`_audit/tex/rig_userthere2w.png`), where the first pass had read
"Mandrake  A" (`rig_usertherew.png`). That screen also answered the one
question the pair captures could not: a third of a kind is lettered C.

Two more writers of the same field turned up in the survey that followed, both
for StreetPass opponents (`0x291f88` and `0x29388c`), both formatting with a
24-character bound into a field that holds 24 bytes. A long name there would
have run over the species id. Their bound is twelve now. Nobody can reach that
screen since the service closed, but the words cost nothing.

**One more, from a question asked while testing.** The naming keyboard after a
scout pre-filled two letters of the species name, "Ja" for a Jailcat. That is
the keyboard's own mode-3 path in `menu/name.arc`'s init, `mov r1,#2` at
`0x22ad9c`, where every other mode pre-fills its whole initial text. It passes
zero now, which makes the callee use the name's own length, clamped to the
keyboard's slot count, so a scouted Demon-at-arms is offered "Demon-at-ar". The
first attempt passed eleven instead and crashed the game; the fifty-seventh
build section below is that story.

**How it was measured.** Azahar's GDB stub on the shipped v2.5 update code,
with write watchpoints on an enemy record's name field. Two Halberdsaurus read
"A" and "B" (`_audit/tex/rig_bn32_s.png`). With the words poked into memory
they read "HalberdsauA" and "HalberdsauB" under the ten-character cut used
during the hunt (`rig_bn58w_s.png`), a Jailcat pair read "JailcatA" and
"JailcatB" (`rig_bn56w_s.png`), and a scouted Demon-at-arms was offered
"Demon-at-ar" (`rig_bn119w_s.png`) with no letter in the caught record, which
is the check that a letter never follows a monster you keep. The space and the
nine-character cut were settled after those captures, so they are first seen on
the built CIA. Seen there from a fresh boot on the built CIAs: a wild pair south of the Wood Park zoom point reads "Halberdsa A" and "Halberdsa B", with the space, under a "Round 1" header in English (`_audit/tex/rig_battle_halberdsa_finalw.png`).

Every battle-start path was traced to one enemy-team builder, `0x1d0cdc`,
which calls both fixed writers: the wild path reaches it through `0x2f4f1c`
and the scripted one through a vtable slot at `0x81dd88`, so boss fights take
the same route. A survey of all 45 callers of the species-name getter found no
other writer of a record's name besides capture, which was already bounded at
eleven, and the two StreetPass ones.

Two traps for whoever reads this code next. `0x15b068` looks unreferenced and
is not: `0x15b064` falls through into it, and using it as a cave black-screened
the game. And there is no free padding at the end of the text segment; code
runs to `0x7b7458` of a `0x7b8000` segment and the tail is not zeroes. That is
why the new routine lives inside the function it serves.

Eleven pairs of species are identical for their first eleven characters (Great
Sabrecat and Great Sabrecub, Killing Machine and Killing Machine Light, Metal
Slime and Metal Slime Knight, and eight more), so a mixed group of those is
lettered as though they were the same species. That is the letter doing its
job rather than a defect: without it the two would print the same name and
there would be no way to tell which is which, and the Status page still gives
the full species name.

An independent review of the words re-derived every old byte, decoded every
new one, traced the thirteen-word routine by hand, scanned the whole image for
any other branch into it and reproduced the patched md5. It returned no
must-fix on the code. One note worth keeping: the copy takes a fixed 22 bytes,
so for a short name it reads past that name's terminator into the message data
behind it. That is a read, never a write, and the terminator written at
character eleven means nothing after the name is ever drawn or compared.

Both CIAs change. The code words are in the update, and round 58's eight
suffix strings are in both trees, so `LayoutMessage.mes` differs in each: eight
labels per CIA and nothing else. The executable is 153 words, md5
`cd5828a5`. That build crashed on the naming keyboard and was replaced the
same night; the fifty-seventh build section below is the fix, and its md5 is
`f6b40eef`.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,019,712  55584e1db1cd40189cc7f0c63a3202ff131b3edd781d66a8c2443e5e31fbdd93
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  746430cdf3050b846d117d0d0779ffdae6182ba1a1fcd6bfc1735a16f5aa76ff
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,656,705  77cdd2816b879942d3c5e5c7f66e76a6f70c99848f5489d3ff9b7ba14b9fca70
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            4,727,396  020ffec19abd0e1e643d41d70782103740d86aabd45adaa509d99226b65e6a94

## Fifty-seventh build, 2026-09-19: the naming keyboard crashed the game (v2.6.1)

Reported within the hour by famicom, on hardware, with a photograph of the
crash screen: fusing a monster killed the game when the name entry screen
opened, and it reproduced on other fusions too. This one was mine, introduced
by the fifty-sixth build, and it is worth writing down properly because the
mistake was avoidable and the evidence that would have caught it was in the
same screenful of disassembly as the change.

**What the crash was.** The exception screen said prefetch abort on svcBreak,
which is a deliberate panic rather than a wild jump, so something in the game
chose to stop. The keyboard fills its slots by asking `0x3212ec` for character
i of the initial text, once per slot, and that function bounds-checks:

    00321340  cmp  r0, r6          ; the string's length against the index asked for
    00321344  bhs  #0x321360       ; in range, carry on
    00321348  ldr  r2, [pc, ...]   ; otherwise the assert message
    0032135c  blx  #0x2ff628       ; and abort

The fifty-sixth build passed a literal eleven as the number of slots to fill,
so the keyboard asked for characters 0 to 10 of whatever name it was given. Any
name shorter than eleven characters therefore asked for a character that does
not exist and hit that abort. A fused monster's name is short. So is nearly
every monster you scout.

**Why testing missed it.** The one screen it was tested on was a scouted
Demon-at-arms, thirteen characters, where every index from 0 to 10 happens to
exist. A Slime would have crashed instantly. That is the whole lesson: the case
that was checked was the case that could not fail, and the shortest input is
the one a length change has to be tried on.

**The fix, one word.** `0x22ad9c` passes zero instead of eleven. The callee
treats zero as "use the initial text's own length":

    0022b2dc  cmp  r1, #0
    0022b2e8  beq  #0x22b318
    0022b318  ldr  r0, [r4, #0x64]    ; the initial-text object
    0022b320  ldr  r5, [r0, #-4]      ; its real length
    0022b324  b    #0x22b2ec          ; and on into the usual clamp to the slot count

so the count is the smaller of the name's length and the slots, and can never
name a character that is not there. Zero is also exactly what every other
keyboard mode passes, at `0x22acc0`, four instructions above the line the
fifty-sixth build edited. The correct value was on screen at the time.

The advertised behaviour does not change: the whole species name is still
pre-filled, up to the eleven slots. The executable is still 153 words; one of
them has a different value. md5 `f6b40eef`.

Only the update changes. Checked on the rig before this was released, on a
short species name and a long one, which is the check the fifty-sixth build
should have had.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,019,712  55584e1db1cd40189cc7f0c63a3202ff131b3edd781d66a8c2443e5e31fbdd93
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  af585a81651a0a625d930733984ede57933e673c411249d3d6adfa070d187067
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,656,678  a375431094bafb2e16662fb860286d978a5110e3f8cd4186515879faa218a542
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            4,941,761  d2448699b15b7b221109f4bf2229a266e4b6bd06b0cbda656cd4901a75fecaeb

## Fifty-eighth build, 2026-09-19: the Library descriptions did not fit (v2.7)

Three things, all reported or prompted by Retho on Discord in one afternoon.

**The names.** v2.5 renamed ヒヒュドラード to "Hihyudorado" and 邪獣ヒヒュルデ to
"Evil Beast Hihyurude", taking both from dragon-quest.org, which carries only a
romanisation for these because Joker 2 Professional was never officially
localised. The Joker 2 Professional fan translation has its own English names,
and reading its name table (`_audit/j2pro_names.py`, which decodes the ROM's own
text encoding) gives "Baboodread" and "Baboorood". "Baboodread" is what the 2021
J3 patch already used, so v2.5 replaced an established name with a
transliteration. Both go back, and 邪獣ヒヒュルデ is "Beastly Baboorood", keeping
the 邪獣 prefix that Joker 2 has no name for. Fourteen labels move, not two: the
skill-set header in ItemHelpMessage, the speaker name tag, the Library
description that names the earlier form, and a note in the demo917 script.
`SkillMessage.mes` SkillName0341 still read "Baboodread" all along, which v2.5
missed, so this also puts the monster and the skill named after it back in
agreement.

Checked against the same table: six more names we changed and J2 Professional
also uses are all defensible, each backed by this game's own wiki bestiary
(Lord of the Dragovians, Picuda, Quayhorse, Leonyx the Divine Battler, Wyrmhole
Dragon, Bishop Ladja). The cross-check found nothing else.

**The Fusion panel's "etc.".** LayoutMessage's `nado` (など) was blank. The
Library's Fusion panel uses it to say a monster has more recipes than the two it
shows, so blanking it deleted the only sign those recipes exist. It was blanked
on purpose, in `latefixes.py`, but as part of the wrong group: `ato` and
`kaisuu` are particles the engine wraps around a number where English word order
cannot follow, and this one is not that. It reads "etc." now. Seen on the rig on
Golem, whose panel now reads Discombombulator, Lantern Soldier, etc.

**The descriptions that did not fit.** 49 of the 737 Library descriptions
overflowed their box, and it had been shipping since v2.5.

The box is the pane `tb_trivia_01` in `lib_monster_trivia.bflyt`: 182 px wide,
four lines of 18. Both limits are hard, and the way they interact is the part
worth writing down. The game does not word wrap and does not shrink text to fit.
It hard cuts at the pane width in the middle of a word. On Bishop Ladja's page a
stored line rendered as "Slon the Rook and Kon the Knight at h" and then
"is command" on the line below, splitting "his". So a stored line over 182 px
silently costs an extra rendered line, and the fifth line is drawn BELOW the
box, over the "Foe #1" row.

That also calibrates the measuring: a line of 182 px fitted and one of 184 px
did not, so `wrapdialogue.measure` is exact for this font.

Why it happened: `rewrap.py` is the pass that wraps this file, and it was never
wired into `rebuild.py`. It ran once by hand, at 216 px, and only touched
strings with no line break at all, so everything the meaning and rename passes
rewrote afterwards was never re-wrapped. 37 entries ran to five lines and 12 had
a line too wide. The base tree was worse: 114 of its descriptions were still
single unbroken runs.

8 of the 49 fit once re-wrapped. The other 41 needed shorter English, and that
is mostly our own doing: these were strings the 2021 patch left untranslated, so
we wrote them, and wrote them long. Every rewrite was measured before it was
accepted. Several turned out to be corrections as well: 0375 had invented
"camouflaged by its onyx frame" and "a night stroll" that are not in the
Japanese, 0538 had fur "corrupted and bloodied" where the Japanese says dyed the
colour of darkness, and 0785 had a demon lord making a "super villain" where the
Japanese says he built a force to defeat the hero. Five wording calls went to
Gemini, which agreed with all five and improved two; the package and the verdict
are `GEMINI_DQMJ3PRO_TRIVIA_FIT.md`.

The fix that matters for next time is `trivfit.py`, which wraps every
description at the real width and exits non-zero listing anything that still
needs a fifth line. It is wired into `rebuild.py`, so this class of defect stops
the build instead of shipping.

The executable is untouched at 153 words, md5 `f6b40eef`.

A correction while checking this build: these notes had said 154 words since
the fifty-sixth build. codepatch.py has 154 entries, but the one at `0x7747a8`
writes the bytes that are already there, so only 153 words actually differ from
the Japanese original. The count had been taken from the length of the list
instead of from the built file. The md5 is unaffected and no binary changes.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  9866cf3cacd6e399ca55d97e3024a574d278aadd37e41c416b043cc4b819570a
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  668f331004408ad5ff6252ab82946171f66bdde6b65cd239e863090287ff6628
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,671,156  b3604207dd6d49d11dc383efae3c7f684bceff355d31cc1543b1ca1f5fd9e7ae
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            4,941,486  c5756cbab3d2b332fbf828c46c6b75da9085c24861c94a0a7ffd05e5f1510a09

## Fifty-ninth build, 2026-09-19: names that are in no name table, and a guard (v2.8)

v2.7 shipped and then two audits were run against the published CIAs rather than
against a working tree. Everything below came out of those, plus one refuter
pass over a new tool. Nothing here was reported by a player.

**Three descriptions named monsters that do not exist.** `MonsterTrivia0786`,
`0840` and `0875` spoke of "Slamen Rider", "Slamen Dark" and "Slamen Rider
Girl". None of those is a name in this game. The Japanese is スライダーヒーロー,
which is `MK0785` Ultra Slime, 死神スライダーク, which is `MK0786` Nemeslime, and
スライダーガール, which is `MK0840` Slider Girl, so the name table settles it and
there was no wording call to make. Two are the 2021 wording. `0840` is ours and
went backwards: `rename57.py` had corrected it, and the v2.7 rewrite put the old
name back.

It survived v2.7 because the check for it was a grep for the two-word phrase
"Slamen Rider" in text that is stored hard wrapped, so every occurrence split
across a line break was invisible. A scan of both shipped CIAs with the line
breaks collapsed finds three, which is the three fixed, and nothing else
anywhere in the game.

**Text that the screen cannot hold.** The 3DS top screen is 400 px and the
engine neither wraps nor shrinks, so anything past that edge is not drawn.
`MenuMessageLoadNotVersionWarning`, the warning about starting a new game over
a save, was one stored line of 478 px; `rewrap.py` has had a rule for that exact
label since it was written, 235 px over three lines, and the rule never ran
because `rewrap.py` was never wired into `rebuild.py`. Same root cause as the
bestiary overflow in the fifty-eighth build. `TakeOverDataCheatMonster_Whale`
was 639 px and `CaughtOut_Crack` 416 px; each has a twin string that says the
same thing and is broken correctly, so each is broken the same way as its twin.

**The Fondude speeches.** All seven rescue speeches are drawn in the field
dialogue window, 346 px by two lines, but they live in
`Message/StealthBoxMessage.mes` and `wrapdialogue.py` only ever looked at the
field script, so nothing had ever measured them. One page was stored as a single
482 px line. They are re-wrapped, the words untouched. The scope was not simply
widened to everything carrying a page-break tag, because ten of those labels are
the diary, which is drawn in a 378 by 180 pane and fits it today; widening would
have broken the diary.

Five field dialogue pages also ran to a third line, which is drawn below the
window, including one that left a lone "a" on a line of its own. None needed
shorter English. `wrapdialogue.py` keeps an authored line break and wraps under
it, which is right for script broken on purpose and useless when the break
itself is the problem. A page is only reflowed when the retail Japanese page for
the same label fits two lines, which is what keeps the pass off the six pages
that are long in Japanese too and are therefore drawn somewhere else.

**The skill and trait pages, found by a refuter.** The new guard described below
was written to check, among other things, the Library's skill and trait boxes.
Its first draft counted a stored line wider than a box as costing an extra
rendered row that a four line box could absorb, and so reported both files
clean. It cannot be absorbed: the cut in the middle of the word is the defect.
With the width test restored, thirteen entries in `FeatHelpMessage.mes` and
`ActionHelpMessage.mes` are over their 234 px box, up to 256 px. All thirteen
fit once re-wrapped, so no English is rewritten. The same mistake is why the
audit itself had called those two files clean.

That the box is 234 px is not a guess. The pane declares it, and every entry in
both files measures at or under 234 px in the retail Japanese font except the
`_Short` labels, which run to 303 px. A label whose retail Japanese does not fit
the box is not drawn in that box, so the twelve `_Short` labels are left alone.

**The guard.** `_audit/boxfit.py` is what `trivfit.py` was for one pane. It
measures every label in every message file and field script against the 400 px
screen, and the three boxes the audit resolved to their message file, and exits
non-zero. It runs last in `rebuild.py`, so this class of defect stops the build.
It deliberately does not guard the 36 single-line label panes or the 33 ItemHelp
labels: nobody has shown the engine clips those at all, and retail Japanese
itself overflows 21 of them, so guarding them would fail the build on something
that is not a defect. On this build it reports 32,365 labels checked, 0 over the
screen and 0 over a pane.

**The rest of the name sweep.** The Slider family was found by reading one
description. Sweeping all 737 for capitalised words that match no name in any
of the game's tables returns 58 phrases, 54 of which are fine: plurals of real
names (Exploads, Tuskateers, Nochoros), series lore (Rhapthorne, Loto, Dai) and
place names. Two more looked wrong and are not: "Exploads" is the correct plural
of `MK0409` Expload, and `0272`'s "Galba" and "Golba" are two different monsters,
ガルバ and ゴルバ. One was wrong: `MonsterTrivia0465` called him "Negel", where the
monster is `MK0465` 冥獣王ネルゲル, "Nelgel the Netherfiend", printed two lines above
on the same page, and the Japanese line does not name him at all. Two others are
spacing and case rather than naming: `0273` wrote "Blueeater" and "Redeater" as
one word each where the Japanese has two, and `0906` wrote "Dermlin island".
`0374`, `0433` and `0536` also ended without a full stop, `0374` on a comma,
where all three Japanese lines end with 。

**One spelling.** `MonsterTrivia0538` read "colour", which v2.7 introduced and
which was the only British spelling in a file whose descriptions use color 23
times, armor 14, favor 6 and rumor 18. The monster names stay British, which is
official Dragon Quest style.

The executable is untouched at 153 words, md5 `f6b40eef`.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  07a815e950fb4d6c071b11001b3e97f8ab88200746c8123de466dc363b406041
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  b35eab67669da9bf97fa7f2fc22854c525962b3dae55a2d9620c6c6be00bc54e
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,641,125  e5a88b9f50e1cceb1e8c93ca330e97d68eb8b60df401d65e8d881387157ec2f7
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            4,941,287  9b93aadb5012b1f276282212ba12740425ee5303056935f3db791cc37019056a

## Sixtieth build, 2026-09-19: the one title that did not fit (v2.8.1)

Found by looking at the game rather than by measuring it, which is the part
worth keeping.

The main menu status panel draws the player's title, and on the emulator it read
"Legendary Scou". The Library's own Title list, a completely different panel,
read "Legendary Scou" as well. Two unrelated panels cutting at the same point is
what rules out any one pane's width being the cause.

`TrophyName.mes` holds 256 titles and exactly one of them is longer than 14
characters: `TrophyName006` "Legendary Scout", at 15 characters and 80 px. The
other half of the proof is in the same list: `TrophyName005` "Monster Doctor" is
14 characters and 74 px and is drawn complete three rows above the cut one.

What is NOT settled, and is written down here rather than guessed at: whether
the cut is a 14-character cap of the kind `NAMECAP_14_LIVE.md` documents in
three other panels, or a pixel clip somewhere between 76 and 79 px. Both fit
every observation, because no title in the game is 14 characters or fewer AND
wider than 74 px, so no string exists that could tell the two apart. It does not
change the fix: a replacement inside both limits is safe under either
explanation, and "Monster Doctor" shows that 14 characters at 74 px is inside
both.

The title is now "Legend Master", 13 characters and 71 px. The Japanese is
伝説のマスター, literally the legendary master, and the title belongs to a family
that already reads Fledgling, Able Master, Skilled Master, Grand Master and
Monster Doctor. All thirteen occurrences change together, including the four
StreetPass strings that name it in prose, so the game does not call it two
things. Every affected line gets narrower, and the pass asserts that for each
one before writing.

A note on the method. The box-fit audit mapped 698 text panes through the
message-ID tail each one carries, and this pane carries none, so the audit could
never have seen it. Measuring everything that can be measured is not the same as
having looked.

This build also repairs the documents. The docs pass that wrote the fifty-ninth
build's notes had a faulty "already applied" check: it asked whether the marker
was still present, and the marker sits inside the replacement, so running the
pass twice inserted its block twice. v2.8 shipped with one RELEASE_NOTES
paragraph and four TESTING rows duplicated. Both are collapsed here and the
check now asks only whether the replacement is already present.

The executable is untouched at 153 words, md5 `f6b40eef`.

  DQMJ3P-base-fixed-0.1.0.cia                     1,596,015,616  8af7690a60ec150b8372bbc9abf555b5ba6629e55ccb8ee05ad130c8b7f76941
  DQMJ3P-update-fixed-3.4.0.cia                      21,423,104  5ac42726a8b45f1bc643abaa09c9e723e176168b65f331e82d7a642928378d35
  patches/DQMJ3P-base-fixed-0.1.0.xdelta             13,663,804  d962a10b9a165bba4300534507619a38562c952f228f0b0b9c69ee49e47a2d9a
  patches/DQMJ3P-update-fixed-3.4.0.xdelta            4,941,541  0a620055626c473ad079f6760ecb508ed8fc71f19c21d6e51ffe7b8a949c74db
