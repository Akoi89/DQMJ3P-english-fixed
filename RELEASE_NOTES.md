# Dragon Quest Monsters: Joker 3 Professional, English fixed build

A rebuild of the 2021 English fan translation of DQM Joker 3 Professional (3DS, Ver.1.3) with its defects fixed. The translation is the Joker 3 Translation Team's, as released for Professional by Eiz in 2021; this build only fixes what was broken in it. Every change is scripted and reproduced from the two 2021 CIAs. The whole record is in `BUILD_NOTES.md` (thirty-one builds, in dated sections) and the per-fix list is in `FIXES.md`.

## What's fixed

**The crash.** The original patch shipped a broken font that crashed the game for some players at The Core, the cutscene after the Break Archdemon boss. Both CIAs carry the corrected font (from Lurpigi's Italian project), with the four glyphs the Japanese Ver.1.3 update added (three kanji and the crystal icon) appended to it. Every character the text uses now exists in both fonts. The chest and transfer crashes reported in 2021 were already fixed in Eiz's 2021-05-30 build, which this starts from.

**The text.** Every layer was proofread: the help text (3,570 item, skill, trait, action, trivia and title strings), the quest and hint text (checked line by line against the Japanese), the dialogue (5,697 strings) and the menus (1,614 strings). Just over a thousand spelling, agreement, wrong-word and stray-token slips are fixed (301 in the help layer, 595 in the dialogue, 122 in the menus, and the Helpful Tips). 167 untranslated strings are translated. About 150 lines that said something the Japanese doesn't (a place, a direction, a container, a count, a condition, what you're told to do) now say what the Japanese says.

**Names.** Monster, skill, item, place and character names are the same in dialogue, menus and tables (Nochoro, Tiko, Lenate, Theresa, Δ Slime, Don Mole, Darkiron Bastille, Mt. Elpis, Undead Garden, Wi-Fi Square, Present Code, G-Cup, SpotPass and StreetPass, and a dozen more). Skill book names match the skill they teach, the Crack ranks follow the same ladder as every other family, and the card-suit monsters have their suits back.

**Layout.** Every dialogue page and description is re-broken between words at its box (the engine wraps by character). Every page-break code sits where the Japanese puts it, and no page needs a third line where the Japanese page has two. 135 layout labels that ran letters together ("Iems") have their spacing fixed. 101 UI textures and 60 layout text panes the original left in Japanese are English.

**Prompts.** Every line's control codes match the Japanese line's. Five yes/no prompts had lost their prompt code, among them the Rank ★★ and ★★★ Speed Road prompts (the second conduit in the Incarnus realm, where the yes/no box never appeared), which closed before you could choose and locked you out of the later races.

**The executable.** Forty-seven words are changed in the update's executable. The name-entry keyboard opens on the Latin "Aa" tab. Item names aren't cut at 14 characters in lists, the info window and the equip lists, nor at 10 on the reactor's analyze readout. The Library's monster lists and the Manage Monsters header don't cut monster names at 10 any more, and the rename keyboard takes 11 characters instead of 8, so renaming doesn't shorten a name (a stored name holds 11).

## Not fixed, known

A monster's stored name holds 11 characters, so a species name longer than that is still cut to 11 when the monster is obtained or renamed; the field is part of the save format. Names already cut to 8 in an existing save stay that way until renamed.

Online-only content (the Wi-Fi Square shop, the download monsters and events, StreetPass and SpotPass exclusives, the transfers) is outside this patch. Anthony's plugin at https://github.com/Anthcny144/DQMJ3P-unobtainable-content restores it on a modded 3DS with the Luma plugin loader or on Azahar. Its five Ver.1.3 hook addresses hold the stock instructions in this build's executable, so the two should coexist, but they haven't been run together.

## Files

Two xdelta patches, one for the Japanese base and one for the Japanese Ver.1.3 update, applied to the decrypted Japanese retail files; they produce the two CIAs to install. Sizes, hashes, the source files the patches expect and the exact xdelta commands are in `README.md`. Install the base first, then the update; both are needed.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project), as compiled and released for Professional by Eiz on the woodus.com forum (the 2021-05-30 build). Eiz's own thread records that the Professional text came from that team without their full consent, so this rebuild credits the team as the authors of every line it didn't write, and Eiz for the patch it started from. The font fix is Lurpigi's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English. The fixes were made with Claude (Anthropic) doing the reading, measuring and scripting, with every wording decision reviewed and every change checked against the shipped files.
