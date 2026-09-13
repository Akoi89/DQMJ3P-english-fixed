# Dragon Quest Monsters: Joker 3 Professional, fixed English build

This is the 2021 English fan translation of DQM Joker 3 Professional (3DS),
rebuilt with its defects fixed, released as two xdelta patches for the
Japanese game. The summary is `RELEASE_NOTES.md`. What was changed and how it was checked is in `BUILD_NOTES.md` (thirty-one builds, in dated sections) and the test route is `TESTING.md`.

## What you get

Two xdelta patches that produce the two CIAs from the Japanese game. The
CIAs themselves are not distributed; the table gives their sizes and hashes
so you can check what the patches produced.

| File | Size | SHA-256 |
|---|---:|---|
| `DQMJ3P-base-fixed-0.1.0.cia` | 1,596,036,096 | 8e2892f9e72ffa89c536d3d44c2041e5b42381873d8d7cd71363a36d6d0a204b |
| `DQMJ3P-update-fixed-3.4.0.cia` | 21,431,296 | ad65f6c8dbf57f0b1a8051ad39abef3500015651c0b9942cb5688948f7168d1c |
| `patches/DQMJ3P-base-fixed-0.1.0.xdelta` | 13,815,352 | 81368db97db57b0eb5ed257d5ed96392705d0b4575d8d8abd92c738a126fd1a0 |
| `patches/DQMJ3P-update-fixed-3.4.0.xdelta` | 3,366,223 | 50d6ae1b834a76e55dac5d62e4fa6cd2a7c11b070fcf465d2bcde6de670ccc86 |

Install the base first, then the update. Both are needed: the update carries
the Ver.1.3 content and the executable, including the keyboard fix.

## Applying the xdelta patches

The patches are made against the Japanese retail files AFTER they have been
decrypted with Batch CIA 3DS Decryptor (the standard tool; it turns the
game CIA into a decrypted `.cci` and the update CIA into a decrypted
`.cia`). Feed those two output files straight to xdelta; do not rebuild,
trim or re-pack them with anything else first. They must match these
exactly:

| Source | Size | SHA-256 |
|---|---:|---|
| Japanese base, decrypted `.cci` (title 00040000001ACB00, CTR-P-BDQJ) | 1,591,599,104 | 79078f60ebe030693efe3900b9e7d2d7d3e45888b2f1b8e97189ec5e0f744172 |
| Japanese Ver.1.3 update, decrypted `.cia` (title 0004000E001ACB00, v3.4.0) | 15,725,568 | ec75431825c48507dbba3a9fa6dea57fbb3ef36cf7c4fe1b8791314eb1dde4a1 |

The easy way: `patches/apply_patches.bat` with the two decrypted files as
its arguments (or drag both onto it). It uses the bundled `xdelta3.exe`
(3.2.0, Apache License 2.0) and writes the two CIAs next to the patches.

By hand, with xdelta3 (3.1 or newer; the patches carry no application
header, so you name both files yourself):

```
xdelta3 -d -B 1879048192 -s "<japanese base decrypted>.cci" DQMJ3P-base-fixed-0.1.0.xdelta DQMJ3P-base-fixed-0.1.0.cia
```

```
xdelta3 -d -B 268435456 -s "<japanese update decrypted>.cia" DQMJ3P-update-fixed-3.4.0.xdelta DQMJ3P-update-fixed-3.4.0.cia
```

The `-B` values are the source window sizes the patches were made with; the
base one needs about 1.8 GB of RAM while decoding. Check the output against
the SHA-256 table above. Both patches were verified to decode byte for byte
on the machine that made them.

Yes, the base patch turns a `.cci` into a `.cia`. That is deliberate: the
decryptor produces a `.cci` for game titles, and a `.cia` is what installs.

## What is fixed, in one paragraph each

**The crash.** The original patch ships a broken font that crashes the game
at a cutscene. Both CIAs carry the corrected font (from Lurpigi's Italian
project), which matches the Japanese font layout and loses no glyph. On
top of that, the four glyphs the Japanese Ver.1.3 update added to its
fonts (three kanji and the crystal icon) are appended to both fonts, and
the crystal icon is back in the three strings that show it; the 2021 patch
had replaced it with a character no font has. Every character used by
every string in the build now exists in both fonts.

**The text.** 167 untranslated strings translated; every dialogue page and description re-broken between words at its box (the engine wraps by character); the corrupted name-entry
keyboard restored; factual errors, wrong numbers and spelling fixed; names
made consistent with each other (skill book names now match the skill they
teach, guard and break traits are told apart, the Crack ranks follow the
same ladder as every other family, the card-suit monsters have their suits
back); 54 player titles shortened to the 14-character cap the game
enforces (and nine more corrected); and the hand line breaks that the original update files had lost
put back, so descriptions no longer split words at the box edge.

**The graphics.** 101 UI textures and 60 layout text panes that the original
patch left in Japanese are English, plus the boot notice and the home
screen title.

**The tables.** The resistance values, sort-mode headers and family rows that overprinted, clipped or mistranslated are fixed.

**The squeezed labels.** 135 layout text panes (the AGI and INT stat
labels, the bestiary's "Items" pill, map place names, StreetPass counters)
carried a minus 2 px letter spacing tuned for the wide Japanese font; on the
English font it ran narrow letters into each other ("Iems"). The spacing is
zero now.

**The help layer, read in full.** Every item, skill, trait and action
description, monster trivia entry, title description and menu help string
(3,570 of them) was proofread: 301 spelling, agreement and wording slips
fixed, skill names in help lists aligned with the skill table, and the
family names in title descriptions aligned with the monster table.

**The Helpful Tips.** The 89 tip titles lost their category prefix so they
fit the game's 20 character title limit (58 were cut mid-word), eight were
shortened further, and 36 slips in the tip bodies are fixed. The setting
is "Break World" everywhere (twelve lines said "Broken World"), the three
event names carry no apostrophe (Riders Cup, Masters GP, Challengers GP),
and the Fondude family is spelled the way the bestiary spells it.

**The map marker.** The Silent Meadows navi map showed "NOW_PRINTING" on
its destination marker. That was this rebuild's own doing: the layout pane
carries a hidden message ID after its text, and an earlier text-pane edit
dropped it. The ID is back, the pane reads "Wood Park", and the writer no
longer drops such IDs.

**The prompts.** Every line's control codes were compared with the
Japanese line's. Five yes/no prompts had lost their prompt code, among
them the Rank ★★ and ★★★ Speed Road prompts, which closed before a choice
could be made and locked players out of the later races; one had the code
in the wrong place, one had a spurious one, and a few system lines carried
the wrong window style. All mirror the Japanese now.

**The keyboard.** The name-entry keyboard opens on the Latin "Aa" tab
instead of hiragana. This is a three-word patch to the update's executable.

**Item names.** Every item list, the item info window and the equip lists
cut item names at 14 characters ("Strong Medicin"); 584 of the 1,079
names are longer. Three 16-character buffers in the update's executable
are raised to 32 (thirteen words changed), so names draw in full. The
reactor's two analyze panes cut them at 10 the same way; that buffer is
raised too (four more words).

**Monster names.** The Library's monster lists cut species names at 10
characters ("Metal Slim"; 495 of the 1,024 names are longer) because one
row builder formats each name into a 16-character buffer behind a
five-unit family icon; that buffer is now 38 characters (32 visible; the
longest name is 24). The Manage Monsters header cut the monster's own name
at 10 through a 12-character buffer, now 32. The rename keyboard took 8
characters while a default name holds 11, so opening Change Name on a
monster with a long name and pressing OK cut it to 8; the keyboard now
takes 11, its four handlers copy 11, and the two copies that carry a
parent's name into a synthesized monster's record keep 11 instead of 10.
Twenty-seven words in the update's executable, found with a live debugger
and each seen on screen.

**The quest and hint text, checked against the Japanese.** After the Shiny Sap hint turned out to point at the wrong kind of chest, every quest instruction, hint, tutorial, signpost, shop and NPC guidance line (1,007 of them) was read beside its Japanese with one question: is it true? 125 lines said something the Japanese does not (a place, a direction, a container, a quantity, a condition, or what the player is told to do) and now say what the Japanese says. Three names the dialogue used are now the names the tables use (Δ Slime, Don Mole, Darkiron Bastille), and the two mine puzzle hints say clockwise and counterclockwise.

**The dialogue, read in full.** Every NPC line, cutscene line, quest and shop line (5,697 strings) was proofread the way the help layer was: 595 spelling, agreement, wrong-word and stray-token slips fixed, the names the dialogue spelled two ways aligned with the game's own tables (Nochoro, Tiko, Lenate, Theresa, Mt. Elpis, Undead Garden and a dozen more), and sixteen lines the 2021 text had garbled put right from the Japanese, among them the cryogenic-sleep records, the boulder line in the crystal caves, the red and yellow mushrooms that both said pink, and the dying underling who now addresses his two bats instead of claiming to be one.

**The menus, read in full.** The last layer: every menu prompt, tutorial pop-up, battle event line, Speed Road and race string, reactor readout, diary entry and network screen (1,614 strings). 122 slips fixed, the terms the menus spelled several ways settled (Present Code, G-Cup, Network Coins, Wi-Fi Square, and SpotPass and StreetPass spelled Nintendo's way everywhere, dialogue included), and ten lines corrected from the Japanese, among them two Speed Road attacks labelled ranged that are close-range, three that said one slime drops where all of them do, and a garbled diary line about the ship remains.

**The page layout.** Every dialogue page was measured against the same page of the Japanese. In 64 lines the page-break code was wrapped in spaces or glued to the text where the Japanese breaks the line, which left a stray space or a blank line at the top of the next page; a few pages opened with an empty line; 26 pages ran to a third line because a short line had been broken by hand; one line had two Japanese pages on one. All are back in the Japanese shape, with no wording changed. Five more pages whose English simply had too many words for two lines were shortened, and one prompt that was not a sentence was retranslated. The Bastille's remodeling machine, named nine ways in the 2021 text, has the two names the Japanese gives it; the Snapped family is named by its table names; and the chapter 7 hint, which said the opposite of the Japanese, is retranslated.

## Not fixed, known

See "Tier 3" in `TESTING.md`: a few screens nobody has checked yet. If you find something, note the exact text and the screen.

A monster's stored name holds 11 characters, so a species name longer
than that ("Metal Pearl Slime") is still cut to 11 when the monster is
obtained or renamed; the record field is 24 bytes and changing it would
change the save format. Names already cut to 8 in an existing save stay
as they are until renamed.

Online-only content (the Wi-Fi Square shop, the download monsters and
events, StreetPass and SpotPass exclusives, the transfers) is not this
patch's business. Anthony's plugin at
https://github.com/Anthcny144/DQMJ3P-unobtainable-content restores it on a
modded 3DS with the Luma plugin loader or on Azahar. Its README asks for a
game whose code is untouched; this build changes forty-seven words of the
update's code (the keyboard tab, the name buffers, the keyboard limit). I
checked the five Ver.1.3 code addresses the plugin hooks, and the four
words it probes to recognise the version, against this build's executable:
all nine still hold the stock instructions, so the two should coexist. I
have not run them together.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project), as compiled and released for Professional by Eiz on the woodus.com forum (the 2021-05-30 build). Eiz's own thread records that the Professional text came from that team without their full consent, so this rebuild credits the team as the authors of every line it did not write, and Eiz for the patch it started from. The font fix is Lurpigi's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English. This rebuild only fixes what was broken; it does not claim the translation.
