# Dragon Quest Monsters: Joker 3 Professional, English fixed build

A rebuild of the 2021 English fan translation (3DS, Ver.1.3) with its mistakes fixed. The translation is the Joker 3 Translation Team's; this only fixes what was broken in it. Every change is scripted and reproduced from the two 2021 CIAs.

## What this build fixes

- **Two crashes and five stuck prompts.** A broken font crashed the game at a cutscene. Five yes/no questions closed before you could answer, and two of those locked you out of the later Speed Road races.
- **Text that said the wrong thing.** Every translated line was read against the Japanese. A few thousand said something else and are corrected: bestiary entries with the story backwards, spells listing the wrong element, directions that sent you the wrong way, menu buttons labelled the opposite of what they do.
- **Spelling, and one name for one thing.** Just over a thousand spelling and wrong-word slips. Monsters, skills, items and places are now called the same thing in dialogue, menus and tables, and monster names match the ones the series uses.
- **Text that didn't fit its box.** The game won't shrink text or move a word to the next line. Too wide, and it chops the line off partway through a word; one line too many, and the extra is drawn outside the box on top of whatever's there. Fixed across descriptions, warnings and conversations.
- **Names cut short.** In menus, in the Library, on the naming keyboard, and under wild monsters in battle, where 438 species used to show nothing at all.
- **Japanese that was never translated.** 167 lines, plus menus, tips, textures and signs.

`FIXES.md` has a paragraph on each. `BUILD_NOTES.md` is the full record.

## Version history

Newest first.

- **v2.11** - your name no longer runs into the next word, the roaming boss prompts read as sentences, and the mist skill sets and gravity spells held back from v2.10 are renamed.
- **v2.10** - names checked against the series. About fifty spells, skills, traits and one monster now use the name the official English releases use, and the Courage skill set is Cleric again.
- **v2.9** - nine labels in the menus were too wide for their box, so the game cut them off partway through a word. The race screen showed "Hors" and "Accel" instead of Horsepower and Acceleration. They are abbreviated to fit now, and the Wi-Fi ranking label that said "Score" says "W/L", which is what the Japanese means.
- **v2.8.1** - the top player title was one letter too long to draw, so it showed as "Legendary Scou". It's now "Legend Master".
- **v2.8** - four Library descriptions named monsters that aren't in the game. Thirteen skill pages, three warnings and the Fondude rescue speeches didn't fit their boxes. The build now measures every line against its box and won't finish if one doesn't fit.
- **v2.7** - 49 Library descriptions spilled a line out over the row below. Two monsters got the names the Joker 2 Professional translation uses, and the fusion list shows "etc." again when a monster has more recipes than it can list.
- **v2.6.1** - fixes a crash v2.6 introduced in the naming keyboard. If you installed v2.6, replace it.
- **v2.6** - wild monsters have their names back in battle, and scouting one stops asking you to retype it.
- **v2.5** - 356 monster names changed to the ones the series uses, and dialogue lines that include your name are measured with the name in them.
- **v2.4** - the patches were rebuilt so any correctly decrypted dump works, not just mine.
- **v2.3** - the meaning pass finished, and the game says the same thing the same way everywhere.
- **v2.2** - the interface text, a second read of the meaning pass, and the partner's lines.
- **v2.1** - the leftovers from v2.0's meaning pass.
- **v2.0** - the meaning pass. Earlier versions fixed how the English reads; this one fixed what it says. 1,573 lines corrected.
- **v1.9** - the Ride Fuse screen, and one name for fusion instead of five.
- **v1.8** - the skill-point hint stops cutting names at 10 letters.
- **v1.7** - the rest of the screens that cut action names at 18.
- **v1.6** - one spell name, and one column that cut names short.
- **v1.5** - the last of the help lists that didn't match their skill.
- **v1.4** - sixteen help lines that named the wrong thing, and names that now agree across skill, book and help line.
- **v1.3.1** - one corrected sentence in `FIXES.md`. Patches identical to v1.3.
- **v1.3** - three more panels stopped cutting names at 14 characters.
- **v1.2** - thirty skill books named after the skill they teach, not the 2021 "Xguard" name.
- **v1.1** - monster names no longer cut at 10 in the Library, and the rename keyboard takes 11 characters instead of 8.
- **v1.0.1** - documents only, after a fact audit. Patches identical to v1.0.
- **v1.0** - first release.

## Not fixed, known

- A monster's stored name holds 11 characters, so a longer species name is still cut when you obtain or rename it. That field is part of the save format. Names already cut to 8 in an existing save stay until renamed.
- Online content (the Wi-Fi Square shop, download monsters and events, StreetPass and SpotPass exclusives, the transfers) is outside this patch. [Anthony's plugin](https://github.com/Anthcny144/DQMJ3P-unobtainable-content) restores it. Every address it uses still holds the stock instructions in this build, so the two should coexist, but they haven't been run together.

## Files

Two xdelta patches, one for the Japanese base and one for the Japanese Ver.1.3 update. They apply to the decrypted Japanese retail files and produce the two CIAs you install. Sizes, hashes, the source files expected and the exact commands are in `README.md`. Install the base first, then the update; both are needed.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project). This rebuild starts from the 2021-05-30 Professional patch posted on the woodus.com forum, which used the team's text without their full consent, so the team is credited as the authors of every line it didn't write. The font fix is Lurpigi's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English. A number of these fixes began as Retho's reports on Discord, including the monster name this release corrects and the skill set whose name sent me back to check every other one against the official releases. The click by click instructions in the README, and the Linux route beside them, are oho's.

The fixes were made with Claude (Anthropic) doing the reading, measuring and scripting, with every wording decision reviewed and every change checked against the shipped files.
