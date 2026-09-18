# Dragon Quest Monsters: Joker 3 Professional, fixed English build

This is the 2021 English fan translation of DQM Joker 3 Professional (3DS), rebuilt with its defects fixed. It's released as two xdelta patches for the Japanese game. The translation is the Joker 3 Translation Team's; this build only fixes what was broken in it.

Where to look: `RELEASE_NOTES.md` is the short summary, `FIXES.md` lists every fix, `BUILD_NOTES.md` is the full record (fifty-one dated sections, up to the fifty-fourth build) and `TESTING.md` is the test route. `CODE_PATCH_NOTES.md` is for anyone porting the code patch to another language: the addresses, the traps and how they were actually found.

## What you get

Two xdelta patches that produce the two CIAs from the Japanese game. The CIAs themselves aren't distributed; the table gives their sizes and hashes so you can check what the patches produced.

| File | Size | SHA-256 |
|---|---:|---|
| `DQMJ3P-base-fixed-0.1.0.cia` | 1,596,015,616 | 8a8b585a70c8780f0bf18eb7bcf6f07fa93357856ffaf223de6c19a4140c24d2 |
| `DQMJ3P-update-fixed-3.4.0.cia` | 21,423,104 | 5deec263ed182da42a2c8213220b1c3aa35e10d40413fb1b028a8d904099c490 |
| `patches/DQMJ3P-base-fixed-0.1.0.xdelta` | 13,586,914 | 171ad8f8d9343a2d05cf81c3f9e175cfc7a6647a146194fdff08b3df11bca326 |
| `patches/DQMJ3P-update-fixed-3.4.0.xdelta` | 4,634,988 | d98e95b67936e1eea01333ea8eaec20ccd3e4cf2026ce73749e65ac020061e00 |

Install the base first, then the update. Both are needed: the update carries the Ver.1.3 content and the executable, including the keyboard fix.

## Applying the patches

The patches are made against the Japanese retail files AFTER they've been decrypted with Batch CIA 3DS Decryptor (the standard tool; it turns the game CIA into a decrypted `.cci` and the update CIA into a decrypted `.cia`). Feed those two output files straight to xdelta. Don't rebuild, trim or re-pack them with anything else first.

> **Dump both titles as encrypted CIAs and decrypt them on the PC.** If you're pulling them off a 3DS with GodMode9, dump each title to CIA with no decrypt and no trim option, copy those to your computer, and run the decryptor there. GodMode9's own decrypt hands you a file of the **right size** that isn't the same bytes, and the patch will refuse it. That has now caught several people, so a size matching the table below is not proof the file is right. On Linux, [rom-converto](https://github.com/DevYukine/rom-converto) does the same job: decrypt both CIAs, then convert the decrypted game CIA to a trimmed `.3ds`/`.cci`.

Your decrypted files won't have the same SHA-256 as mine, and that's fine. The decryptor writes random bytes into every file it makes (a card seed in the `.cci`, ticket bytes in the update `.cia`), and dumps from different places can carry different tickets. Since v2.4 the patches don't depend on any of that; v2.3 and earlier did, which is why the update patch failed with a checksum mismatch for some people. What has to match is the game itself, so check the sizes:

| Source | Title ID | Version | Size as a `.cia` | Size once decrypted |
|---|---|---|---:|---:|
| Japanese base (CTR-P-BDQJ) | 00040000001ACB00 | 0.1.0 (16) | 1,591,612,416 | 1,591,599,104 (`.cci`) |
| Japanese Ver.1.3 update (CTR-U-BDQJ) | 0004000E001ACB00 | 3.4.0 (3136) | 15,725,568 | 15,725,568 (`.cia`) |

Check the `.cia` sizes before you decrypt anything, since the decrypt takes a while and a wrong file can only fail at the end of it. The base is the one people get wrong. If yours isn't 1,591,612,416 bytes it's a repack, a cartridge dump or a build with the update already merged in, and no patch can bridge that. There's only one correct Japanese base and the numbers above are what hShop lists for it. On hShop and in most dump filenames it's listed as `ドラゴンクエストモンスターズ - Joker 3 PROFESSIONAL`, product code CTR-P-BDQJ. The game's own banner writes that as `ドラゴンクエストモンスターズ` on one line and `Joker 3 PROFESSIONAL` on the next; the hyphen is just how the dump tools flatten the line break.

Which build of the decryptor you use makes no difference to this. The `.cci` it writes is a 16 KiB header followed by the CIA's two contents back to back with no padding, and both of those sizes are recorded inside the CIA, so the same `.cia` always comes out at the same length whatever tool you run.

Never done this before, or something already went wrong? [Step by step, if you're having trouble](#step-by-step-if-youre-having-trouble) walks through the whole process one click at a time. On Linux, see [On Linux](#on-linux) instead.

The easy way: run `patches/apply_patches.bat` with the two decrypted files as its arguments, or drag both onto it. It uses the bundled `xdelta3.exe` (3.2.0, Apache License 2.0) and writes the two CIAs next to the patches.

By hand, with xdelta3 (3.1 or newer; the patches carry no application header, so you name both files yourself):

```
xdelta3 -d -B 1879048192 -s "<japanese base decrypted>.cci" DQMJ3P-base-fixed-0.1.0.xdelta DQMJ3P-base-fixed-0.1.0.cia
```

```
xdelta3 -d -B 268435456 -s "<japanese update decrypted>.cia" DQMJ3P-update-fixed-3.4.0.xdelta DQMJ3P-update-fixed-3.4.0.cia
```

The `-B` values are the source window sizes the patches were made with; the base one needs about 2 GB of free RAM while decoding. Check the output against the SHA-256 table above. Both patches were checked to give exactly those CIAs from a fresh decrypt and from copies whose header bytes (card seed, certificates, ticket, TMD) were overwritten with random data. If you get a checksum mismatch now, the file isn't the Japanese Ver.1.3 update or base; please don't force it with `-n`, since that builds a CIA with the wrong bytes in it.

Yes, the base patch turns a `.cci` into a `.cia`. That's deliberate: the decryptor produces a `.cci` for game titles, and a `.cia` is what installs.

## Step by step, if you're having trouble

The section above is the short version for people who already dump and decrypt their own games. If any of it went wrong, or you've never done this before, here's the whole thing click by click.

Before you start: your two source files have to be **encrypted** CIA dumps of the Japanese originals that you decrypt on your PC with the tool below. Don't use GodMode9's own decrypt or trim option. That hands you a file of exactly the right size with different bytes inside, and re-running the PC decryptor on it doesn't fix it. A matching file size proves nothing, only the hash does. Nearly every "target window checksum mismatch" report so far has turned out to be this.

1. Get your encrypted game CIA and encrypted update CIA, both Japanese originals. The game is `ドラゴンクエストモンスターズ - Joker 3 PROFESSIONAL` (CTR-P-BDQJ) and the update is its Ver.1.3 patch (CTR-U-BDQJ).
2. Get Batch CIA 3DS Decryptor from [GBAtemp](https://gbatemp.net/download/batch-cia-3ds-decryptor.35098/download?version=35152).
3. Extract it to a new folder.
4. Put the two encrypted CIA files in there, rename the game to `game.cia` and the update to `update.cia`.
5. Run `Batch CIA 3DS Decryptor.bat`. It takes a while on the base.
6. You should now have `game-decrypted.cci` and `update (Patch)-decrypted.cia` in that folder.
7. Download [DQMJ3P-english-fixed-patches-v2.4.zip](https://github.com/Akoi89/DQMJ3P-english-fixed/releases/download/v2.4/DQMJ3P-english-fixed-patches-v2.4.zip) from the releases page.
8. Extract it to another new folder.
9. Copy `game-decrypted.cci` and `update (Patch)-decrypted.cia` into that patch folder.
10. Select both of them and drag them onto `apply_patches.bat`.
11. If this stops with a checksum mismatch, go back to how you dumped the CIAs. They need to be encrypted dumps decrypted on the PC, not decrypted or trimmed by GodMode9. Check the source sizes in the table above too.
12. You should now have `DQMJ3P-base-fixed-0.1.0.cia` and `DQMJ3P-update-fixed-3.4.0.cia`.
13. Copy both to your 3DS SD card.
14. Open FBI on your 3DS. If your 3DS was modded with the commonly recommended guide, you already have it.
15. Go to SD, then to whatever folder you copied the two fixed CIAs into.
16. Install the base first, then the update. Both are needed.

Thanks to oho, who wrote these steps out on Discord.

## On Linux

The walkthrough above leans on two Windows things, Batch CIA 3DS Decryptor and `apply_patches.bat`. Neither is special. All the patches need is the Japanese base decrypted to a `.cci` of exactly 1,591,599,104 bytes, the Japanese update decrypted to a `.cia` of exactly 15,725,568 bytes, and xdelta3. Getting there on Linux is the same job with different tools.

Dumping doesn't change: pull both titles off the 3DS with GodMode9 as **encrypted** CIAs, no decrypt option and no trim option, and copy them to your computer. Everything below happens on the PC.

1. Install xdelta3: `sudo apt install xdelta3` on Debian or Ubuntu, `sudo dnf install xdelta` on Fedora, `sudo pacman -S xdelta3` on Arch. Version 3.1 or newer.
2. Get [rom-converto](https://github.com/DevYukine/rom-converto/releases/latest), which does the decrypting. Grab the CLI build for your system, `chmod +x` it, rename it to `rom-converto` and put it somewhere on your `PATH`.
3. Decrypt both files:
   ```
   rom-converto ctr decrypt "<japanese base>.cia"
   rom-converto ctr decrypt "<japanese update>.cia"
   ```
4. Turn the decrypted base into a `.cci`, which is the form the base patch expects:
   ```
   rom-converto ctr convert "<decrypted base>.cia"
   ```
   Run `rom-converto ctr --help` if that doesn't match your build. Its flags have moved between releases and the help output is the authority, not this README.
5. Check the two sizes before you go any further. The base has to be **1,591,599,104** bytes as a `.cci` and the update **15,725,568** bytes as a `.cia`. If your `.cci` is larger, it's very likely padded out to a card size; the patch needs the untrimmed-but-unpadded layout, which is a 16 KiB header followed by the CIA's two contents back to back.
6. Apply both patches:
   ```
   xdelta3 -d -B 1879048192 -s "<japanese base decrypted>.cci" DQMJ3P-base-fixed-0.1.0.xdelta DQMJ3P-base-fixed-0.1.0.cia
   ```
   ```
   xdelta3 -d -B 268435456 -s "<japanese update decrypted>.cia" DQMJ3P-update-fixed-3.4.0.xdelta DQMJ3P-update-fixed-3.4.0.cia
   ```
   The base one wants about 2 GB of free RAM while it decodes.
7. Check what came out against the hash table near the top: `sha256sum DQMJ3P-base-fixed-0.1.0.cia DQMJ3P-update-fixed-3.4.0.cia`.
8. Copy both CIAs to the 3DS SD card, open FBI, and install the base first and then the update.

Fair warning on step 4: I've built and checked these patches on Windows, and nobody has yet reported back from the Linux route end to end, so that conversion step is the one I can't vouch for. The size in step 5 is what tells you whether it worked. If rom-converto won't give you a `.cci` of the right length, both Windows tools run under Wine, and that's the same code path everyone else is using.

## What's fixed

The short version. `FIXES.md` has a paragraph on each.

**Crashes and soft-locks**

- The crash at The Core, the cutscene after the Break Archdemon boss. Both CIAs carry Lurpigi's corrected font, with the four glyphs the Ver.1.3 update added (three kanji and the crystal icon) appended, so every character the text uses exists in both fonts. The chest and transfer crashes from 2021 were already fixed in the 2021-05-30 build, which this starts from.
- Five yes/no prompts that had lost their prompt code and closed before you could choose, among them the Rank ★★ and ★★★ Speed Road prompts (the second conduit in the Incarnus realm) that locked you out of the later races. Every line's control codes now match the Japanese line's.

**What the text says**

- Every translated string that differs from the Japanese, 12,563 of them, was read against the Japanese for meaning, and 1,573 that said something else are corrected. A second read of every line that passed caught 261 more, and the last rounds 192 more.
- Bestiary entries with their story backwards or invented, like the Liquid Metal King's.
- Descriptions that got the effect wrong: Sizz spells dealing "Fire" damage, a trait that claimed to increase Ice damage when it gives Ice resistance, nineteen counter traits with attacker and target swapped.
- Story and guidance lines that sent you the wrong way: Sancho telling the amnesiac hero "Try not to forget", a door that needs all three of Bundold's minions' keys turned into three doors, a village guide who dropped the instruction to find the Prison Key.
- Menu prompts that described the opposite of what the button does, the Gold Bank's Deposit and Pocket labels swapped, and 54 trophy conditions one short ("more than 100" for "100 or more").
- Every quest instruction, hint, signpost, shop and guidance line (1,007) checked for whether it's true: 125 now say what the Japanese says.
- 167 untranslated strings translated.

**Spelling and names**

- Every text layer proofread: the help text (3,570 strings), the dialogue (5,697), the menus (1,614) and the Helpful Tips. Just over a thousand spelling, agreement and wrong-word slips fixed.
- One name for one thing, spelled the same in dialogue, menus and tables: skill books named after the skill they teach, Moreheal instead of Fullheal where the Japanese means Moreheal, Terrorceratops and Tyrannoceratops no longer swapped, Ground Zero, the Demon Realm Gate, Madame Rummy.
- Fusion is "fuse" and "fusion" everywhere, where it had five English names.
- Species and family kept apart: the status screen called a species a "Type", the Library called it a "Family", and the community rules restricted by "species" when they restrict by family.
- The same Japanese line reads the same way everywhere: 168 interface strings, monster names and system lines settled, "Psyche Up" on both the menu and its panel, one-shot battle reflects marked "x1".

**Layout and graphics**

- Every dialogue page and description breaks between words at its box edge (the engine wraps by character), page-break codes sit where the Japanese puts them, and no page runs to a third line where the Japanese has two.
- 101 UI textures and 60 layout text panes that were still Japanese are English, plus the boot notice and the home screen title.
- 135 labels whose letters ran together ("Iems") have their spacing fixed.
- The resistance tables, sort-mode headers and family rows no longer overprint or clip.
- Numbers and names the game writes into a line no longer land glued to the text ("880Poi", "385Type", "I will grant youGold Ring.").

**Names that were cut off (117 words changed in the update's executable)**

- The name-entry keyboard opens on the Latin "Aa" tab.
- Item names aren't cut at 14 characters any more ("Strong Medicin").
- Monster names aren't cut at 10 in the Library or the Manage Monsters header ("Metal Slim").
- Skill and action names aren't cut at 14 on the status screen's Skill panel, the Library's Basic Info header and Library > Skill ("Wisdom Boost EX").
- Action names aren't cut at 18 in the Teaches list, Library > Abilities, a monster's skill pages, the Ride Fuse screen and the skill-point Info window ("Miracle of the Stars"), or at 10 in the hint under the skill-point counter ("Venom Breath").
- The rename keyboard takes 11 characters instead of 8, so renaming no longer shortens a name.
- A fused monster's name no longer carries a Japanese prefix.

## Not fixed, known

See "Tier 3" in `TESTING.md`: a few screens nobody has checked yet. If you find something, note the exact text and the screen.

A monster's stored name holds 11 characters, so a species name longer than that ("Metal Pearl Slime") is still cut to 11 when the monster is obtained or renamed. The record field is 24 bytes and changing it would change the save format. Names already cut to 8 in an existing save stay as they are until renamed.

Online-only content (the Wi-Fi Square shop, the download monsters and events, StreetPass and SpotPass exclusives, the transfers) isn't this patch's business. Anthony's plugin at https://github.com/Anthcny144/DQMJ3P-unobtainable-content restores it on a modded 3DS with the Luma plugin loader or on Azahar. Its README asks for a game whose code is untouched; this build changes one hundred and seventeen words of the update's code (the keyboard tab, the name buffers, the keyboard limit, one built-in prefix, one default greeting). I checked the five Ver.1.3 code addresses the plugin hooks, and the four words it probes to recognise the version, against this build's executable: all nine still hold the stock instructions, and none of the changed words is within 32 bytes of them, so the two should coexist. I haven't run them together.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project). This rebuild starts from the 2021-05-30 Professional patch posted on the woodus.com forum, which used the team's text without their full consent, so the team is credited as the authors of every line it didn't write. The font fix is Lurpigi's. The click by click walkthrough above is oho's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English.

The fixes were made with Claude (Anthropic) doing the reading, measuring and scripting. Every wording decision was reviewed and every change checked against the shipped files. This rebuild only fixes what was broken; it doesn't claim the translation.
