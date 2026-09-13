# Dragon Quest Monsters: Joker 3 Professional, English fixed build

A rebuild of the 2021 English fan translation of DQM Joker 3 Professional (3DS, Ver.1.3) with its defects fixed. The translation is the Joker 3 Translation Team's, as released for Professional by Eiz in 2021; this build only fixes what was broken in it. Every change is scripted and reproduced from the two 2021 CIAs, and the whole record is in `BUILD_NOTES.md` (thirty builds, in dated sections).

## The fixes, in one paragraph each

**The crash.** The original patch shipped a broken font that crashed the game at a cutscene. Both CIAs carry the corrected font (from Lurpigi's Italian project), and the four glyphs the Japanese Ver.1.3 update added to its fonts (three kanji and the crystal icon) are appended to it, so every character the text uses exists in both fonts.

**Every text layer proofread.** The help layer (3,570 item, skill, trait, action, trivia and title strings), the quest and hint text (checked line by line against the Japanese), the dialogue (5,697 strings) and the menus and system text (1,614 strings) were each read in full. Just over a thousand spelling, agreement, wrong-word and stray-token slips are fixed (301 in the help layer, 595 in the dialogue, 122 in the menus, and the Helpful Tips), 167 untranslated strings are translated, and about 150 lines that said something the Japanese does not (a place, a direction, a container, a count, a condition, what the player is told to do) now say what the Japanese says.

**Names made consistent.** Monster, skill, item, place and character names are the same in dialogue, menus and tables (Nochoro, Tiko, Lenate, Theresa, Δ Slime, Don Mole, Darkiron Bastille, Mt. Elpis, Undead Garden, Wi-Fi Square, Present Code, G-Cup, SpotPass and StreetPass, and a dozen more). Skill book names match the skill they teach; the Crack ranks follow the same ladder as every other family; the card-suit monsters have their suits back.

**Layout.** Every dialogue page and description is re-broken between words at its box (the engine wraps by character), every page-break code sits where the Japanese puts it, no page needs a third line where the Japanese page has two, and 135 layout labels that ran letters together ("Iems") have their spacing fixed. 101 UI textures and 60 layout text panes the original left in Japanese are English.

**Prompts and codes.** Every line's control codes match the Japanese line's. Five yes/no prompts had lost their prompt code, among them the Rank ★★ and ★★★ Speed Road prompts, which closed before a choice could be made and locked players out of the later races.

**The executable.** Twenty words are changed in the update's executable: the name-entry keyboard opens on the Latin "Aa" tab, and item names are no longer cut at 14 characters in lists, the info window and the equip lists, nor at 10 on the reactor's analyze readout.

## Not fixed, known

Monster names in the Library list stop at 10 characters and in the party header at 8. The game stores a shortened copy of the name in the monster record when the monster is obtained, and the code that writes it has not been found; raising the display limits (tried, on screen) changes nothing.

Online-only content (the Wi-Fi Square shop, the download monsters and events, StreetPass and SpotPass exclusives, the transfers) is outside this patch. Anthony's plugin at https://github.com/Anthcny144/DQMJ3P-unobtainable-content restores it on a modded 3DS with the Luma plugin loader or on Azahar. Its five Ver.1.3 hook addresses hold the stock instructions in this build's executable, so the two should coexist, but they have not been run together.

## Files

Two xdelta patches, one for the Japanese base and one for the Japanese Ver.1.3 update, applied to the decrypted Japanese retail files; they produce the two CIAs to install. Sizes, hashes, the source files the patches expect and the exact xdelta commands are in `README.md`. Install the base first, then the update; both are needed.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project), as compiled and released for Professional by Eiz on the woodus.com forum (the 2021-05-30 build). Eiz's own thread records that the Professional text came from that team without their full consent, so this rebuild credits the team as the authors of every line it did not write, and Eiz for the patch it started from. The font fix is Lurpigi's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English. The fixes in this build were made with Claude (Anthropic) doing the reading, measuring and scripting, with every wording decision reviewed, and every change verified against the shipped files.
