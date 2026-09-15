# Dragon Quest Monsters: Joker 3 Professional, fixed English build

This is the 2021 English fan translation of DQM Joker 3 Professional (3DS), rebuilt with its defects fixed. It's released as two xdelta patches for the Japanese game. The translation is the Joker 3 Translation Team's; this build only fixes what was broken in it.

Where to look: `RELEASE_NOTES.md` is the short summary, `FIXES.md` lists every fix, `BUILD_NOTES.md` is the full record (thirty-one builds, in dated sections) and `TESTING.md` is the test route.

## What you get

Two xdelta patches that produce the two CIAs from the Japanese game. The CIAs themselves aren't distributed; the table gives their sizes and hashes so you can check what the patches produced.

| File | Size | SHA-256 |
|---|---:|---|
| `DQMJ3P-base-fixed-0.1.0.cia` | 1,596,023,808 | fcf1ddb69e2539e07e5fb13e0ac66882cd1897fbee68e32bda64aab3d019523d |
| `DQMJ3P-update-fixed-3.4.0.cia` | 21,427,200 | 7111661e573e1451efbf5ba8de5ed21ff8a7b0e893a7291323acca57fffc8a9e |
| `patches/DQMJ3P-base-fixed-0.1.0.xdelta` | 13,681,372 | 41851206f76218d2273b5adeb9c3e8fb03fa6bf9026854b9bb0768bdc6a923f6 |
| `patches/DQMJ3P-update-fixed-3.4.0.xdelta` | 5,682,177 | fe4e858d7550f0a5a0fb1899c418a23ab1f795630200fec8fb1f50449bdd7ce7 |

Install the base first, then the update. Both are needed: the update carries the Ver.1.3 content and the executable, including the keyboard fix.

## Applying the patches

The patches are made against the Japanese retail files AFTER they've been decrypted with Batch CIA 3DS Decryptor (the standard tool; it turns the game CIA into a decrypted `.cci` and the update CIA into a decrypted `.cia`). Feed those two output files straight to xdelta. Don't rebuild, trim or re-pack them with anything else first. They must match these exactly:

| Source | Size | SHA-256 |
|---|---:|---|
| Japanese base, decrypted `.cci` (title 00040000001ACB00, CTR-P-BDQJ) | 1,591,599,104 | 79078f60ebe030693efe3900b9e7d2d7d3e45888b2f1b8e97189ec5e0f744172 |
| Japanese Ver.1.3 update, decrypted `.cia` (title 0004000E001ACB00, v3.4.0) | 15,725,568 | ec75431825c48507dbba3a9fa6dea57fbb3ef36cf7c4fe1b8791314eb1dde4a1 |

The easy way: run `patches/apply_patches.bat` with the two decrypted files as its arguments, or drag both onto it. It uses the bundled `xdelta3.exe` (3.2.0, Apache License 2.0) and writes the two CIAs next to the patches.

By hand, with xdelta3 (3.1 or newer; the patches carry no application header, so you name both files yourself):

```
xdelta3 -d -B 1879048192 -s "<japanese base decrypted>.cci" DQMJ3P-base-fixed-0.1.0.xdelta DQMJ3P-base-fixed-0.1.0.cia
```

```
xdelta3 -d -B 268435456 -s "<japanese update decrypted>.cia" DQMJ3P-update-fixed-3.4.0.xdelta DQMJ3P-update-fixed-3.4.0.cia
```

The `-B` values are the source window sizes the patches were made with; the base one needs about 1.8 GB of RAM while decoding. Check the output against the SHA-256 table above. Both patches were verified to decode byte for byte on the machine that made them.

Yes, the base patch turns a `.cci` into a `.cia`. That's deliberate: the decryptor produces a `.cci` for game titles, and a `.cia` is what installs.

## What's fixed

The short version. `FIXES.md` has a paragraph on each.

The crash is gone. The 2021 patch shipped a broken font that crashed the game for some players at The Core, the cutscene after the Break Archdemon boss; both CIAs now carry the corrected font from Lurpigi's Italian project, with the four glyphs the Ver.1.3 update added (three kanji and the crystal icon) appended, so every character the text uses exists in both fonts. The chest and transfer crashes people reported in 2021 were already fixed in Eiz's 2021-05-30 build, which is what this starts from.

Every text layer was proofread: the help text (3,570 strings), the quest and hint text (1,007 lines, each checked against the Japanese), the dialogue (5,697 strings) and the menus (1,614 strings). Just over a thousand spelling, agreement and wrong-word slips are fixed, 167 untranslated strings are translated, and about 150 lines that said something the Japanese doesn't now say what it says. Names are spelled the same way in dialogue, menus and tables.

Since v2.0 the meaning is checked too. Every translated string that differs from the Japanese, 12,563 of them (the bestiary, the trait, ability, item and help descriptions, the story and field dialogue, and the menus, tips, battle messages, diary and trophies), was read against the Japanese for what it says, and 1,573 that said something else are corrected: a bestiary entry with its story backwards, a trait that claimed to increase Ice damage when it gives Ice resistance, Sizz spells dealing "Fire" damage, Sancho telling the amnesiac hero "Try not to forget" where the Japanese tells him it's fine to leave the past forgotten, trophy conditions one short ("more than 100" for "100 or more"), menu prompts that described the opposite of what the button does.

Layout is back in the Japanese shape. Every dialogue page and description breaks between words at its box edge (the engine wraps by character), page-break codes sit where the Japanese puts them, and no page runs to a third line where the Japanese has two. 101 UI textures and 60 layout text panes that were still Japanese are English, and 135 labels that ran letters together ("Iems") have their spacing fixed.

Every line's control codes match the Japanese line's. Five yes/no prompts had lost their prompt code, among them the Rank ★★ and ★★★ Speed Road prompts (the second conduit in the Incarnus realm, where the yes/no box never appeared), which closed before you could choose and locked you out of the later races.

One hundred and eighteen words are changed in the update's executable. The name-entry keyboard opens on the Latin "Aa" tab. Item names aren't cut at 14 characters any more ("Strong Medicin"), monster names aren't cut at 10 in the Library or the Manage Monsters header ("Metal Slim"), and the rename keyboard takes 11 characters instead of 8, so renaming no longer shortens a name. Three more panels no longer cut at 14: the status screen's Skill panel ("Wisdom Boost EX"), the Library's Basic Info header ("Metal Pearl Slime") and the Monsters list under Library > Skill. The Teaches list of a skill set, under Allocate Skill Points and Library > Skill, no longer cuts action names at 18 ("Miracle of the Sta" for "Miracle of the Stars"), and neither do Library > Abilities and a monster's skill pages. The hint under the skill-point counter no longer cuts them at 10 ("Venom Brea" for "Venom Breath"), and the Ride Fuse screen (Fusion Info) and the skill-point Info window show whole names too.

## Not fixed, known

See "Tier 3" in `TESTING.md`: a few screens nobody has checked yet. If you find something, note the exact text and the screen.

A monster's stored name holds 11 characters, so a species name longer than that ("Metal Pearl Slime") is still cut to 11 when the monster is obtained or renamed. The record field is 24 bytes and changing it would change the save format. Names already cut to 8 in an existing save stay as they are until renamed.

Online-only content (the Wi-Fi Square shop, the download monsters and events, StreetPass and SpotPass exclusives, the transfers) isn't this patch's business. Anthony's plugin at https://github.com/Anthcny144/DQMJ3P-unobtainable-content restores it on a modded 3DS with the Luma plugin loader or on Azahar. Its README asks for a game whose code is untouched; this build changes one hundred and eighteen words of the update's code (the keyboard tab, the name buffers, the keyboard limit, one built-in prefix, one default greeting). I checked the five Ver.1.3 code addresses the plugin hooks, and the four words it probes to recognise the version, against this build's executable: all nine still hold the stock instructions, and none of the changed words is within 32 bytes of them, so the two should coexist. I haven't run them together.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project), as compiled and released for Professional by Eiz on the woodus.com forum (the 2021-05-30 build). Eiz's own thread records that the Professional text came from that team without their full consent, so this rebuild credits the team as the authors of every line it didn't write, and Eiz for the patch it started from. The font fix is Lurpigi's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English.

The fixes were made with Claude (Anthropic) doing the reading, measuring and scripting. Every wording decision was reviewed and every change checked against the shipped files. This rebuild only fixes what was broken; it doesn't claim the translation.
