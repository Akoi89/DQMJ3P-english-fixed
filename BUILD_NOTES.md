# The rebuilt CIAs

First built 2026-09-08; the thirtieth and latest build is dated 2026-09-13. Output is in `FIXED_BUILD/` at the project root, alongside a copy of these notes and the test plan.

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
