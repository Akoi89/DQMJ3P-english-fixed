# Dragon Quest Monsters: Joker 3 Professional, fixed English build

The 2021 English fan translation of DQM Joker 3 Professional (3DS), rebuilt with its defects fixed. Released as two xdelta patches for the Japanese game. The translation is the Joker 3 Translation Team's; this build only fixes what was broken in it.

- `RELEASE_NOTES.md` - what each version fixed
- `FIXES.md` - a paragraph on every fix
- `TESTING.md` - the test route, and what nobody has checked yet
- `BUILD_NOTES.md` - the full record
- `CODE_PATCH_NOTES.md` - addresses and traps, for anyone porting the code patch to another language

## What you get

Two xdelta patches that produce the two CIAs from the Japanese game. The CIAs aren't distributed; the table lets you check what the patches produced.

| File | Size | SHA-256 |
|---|---:|---|
| `DQMJ3P-base-fixed-0.1.0.cia` | 1,596,015,616 | 8af7690a60ec150b8372bbc9abf555b5ba6629e55ccb8ee05ad130c8b7f76941 |
| `DQMJ3P-update-fixed-3.4.0.cia` | 21,423,104 | 5ac42726a8b45f1bc643abaa09c9e723e176168b65f331e82d7a642928378d35 |
| `patches/DQMJ3P-base-fixed-0.1.0.xdelta` | 13,663,804 | d962a10b9a165bba4300534507619a38562c952f228f0b0b9c69ee49e47a2d9a |
| `patches/DQMJ3P-update-fixed-3.4.0.xdelta` | 4,941,541 | 0a620055626c473ad079f6760ecb508ed8fc71f19c21d6e51ffe7b8a949c74db |

Install the base first, then the update. Both are needed: the update carries the Ver.1.3 content and the executable, including the keyboard fix.

## Applying the patches

> **Dump both titles as encrypted CIAs and decrypt them on the PC.**
> - With GodMode9, dump each title to CIA with **no decrypt and no trim**, copy them to your computer, and decrypt there.
> - GodMode9's own decrypt hands you a file of the **right size** that isn't the same bytes, and the patch will refuse it. A size matching the table is **not** proof the file is right.
> - That has now caught several people. Nearly every "target window checksum mismatch" report has turned out to be this.

Decrypt both with Batch CIA 3DS Decryptor, which gives you a `.cci` for the game and a `.cia` for the update. Feed those straight to xdelta. Don't rebuild, trim or re-pack them first. **Check the source sizes before decrypting**, since a wrong file can only fail at the end of a long decrypt:

| Source | Title ID | Version | Size as a `.cia` | Size once decrypted |
|---|---|---|---:|---:|
| Japanese base (CTR-P-BDQJ) | 00040000001ACB00 | 0.1.0 (16) | 1,591,612,416 | 1,591,599,104 (`.cci`) |
| Japanese Ver.1.3 update (CTR-U-BDQJ) | 0004000E001ACB00 | 3.4.0 (3136) | 15,725,568 | 15,725,568 (`.cia`) |

**The easy way:** drag both decrypted files onto `patches/apply_patches.bat`, or pass them as arguments. It uses the bundled `xdelta3.exe` (3.2.0, Apache License 2.0).

**By hand,** with xdelta3 3.1 or newer:

```
xdelta3 -d -B 1879048192 -s "<japanese base decrypted>.cci" DQMJ3P-base-fixed-0.1.0.xdelta DQMJ3P-base-fixed-0.1.0.cia
```

```
xdelta3 -d -B 268435456 -s "<japanese update decrypted>.cia" DQMJ3P-update-fixed-3.4.0.xdelta DQMJ3P-update-fixed-3.4.0.cia
```

The base one needs about 2 GB of free RAM. Check both outputs against the SHA-256 table above, then install **the base first, then the update**.

Anything go wrong, or never done this before? [Step by step](#step-by-step-if-youre-having-trouble) below. On Linux, see [On Linux](#on-linux).

## Step by step, if you're having trouble

Never done this before, or something already went wrong? Start again from here. On Linux, see [On Linux](#on-linux) instead.

1. Get your **encrypted** game CIA and **encrypted** update CIA, both Japanese originals. The game is `ドラゴンクエストモンスターズ - Joker 3 PROFESSIONAL` (CTR-P-BDQJ), the update is its Ver.1.3 patch (CTR-U-BDQJ).
2. Get [Batch CIA 3DS Decryptor](https://gbatemp.net/download/batch-cia-3ds-decryptor.35098/download?version=35152) and extract it to a new folder.
3. Put the two CIAs in there. Rename the game to `game.cia` and the update to `update.cia`.
4. Run `Batch CIA 3DS Decryptor.bat`. It takes a while on the base.
5. You should now have `game-decrypted.cci` and `update (Patch)-decrypted.cia`.
6. Download the patches zip from the [latest release](https://github.com/Akoi89/DQMJ3P-english-fixed/releases/latest) and extract it to another new folder.
7. Copy the two decrypted files into the patch folder, select both, and drag them onto `apply_patches.bat`.
8. If it stops with a checksum mismatch, go back to **how you dumped**. They must be encrypted dumps decrypted on the PC, not decrypted or trimmed by GodMode9. Check the source sizes above too.
9. You should now have `DQMJ3P-base-fixed-0.1.0.cia` and `DQMJ3P-update-fixed-3.4.0.cia`. Copy both to your SD card.
10. Open FBI on your 3DS (you have it if you followed the usual modding guide), go to SD, and install **the base first, then the update**.
11. **Check the base really went on.** Start a battle and look at the top of the screen: it should say "Round 1". If it says ラウンド, or a monster's Info page shows an orange 固定 tag, only the update installed. Those screens live in the base game, so install the base CIA too.

Thanks to oho, who wrote these steps out on Discord.

### Why it usually goes wrong

- **The base is the file people get wrong.** If yours isn't 1,591,612,416 bytes it's a repack, a cartridge dump, or a build with the update already merged in, and no patch can bridge that. There is only one correct Japanese base.
- **Your decrypted files won't have the same SHA-256 as mine, and that's fine.** The decryptor writes random bytes into everything it makes (a card seed in the `.cci`, ticket bytes in the update `.cia`), and dumps from different places carry different tickets. Since v2.4 the patches don't depend on any of that. v2.3 and earlier did, which is why the update patch failed for some people.
- **Which build of the decryptor you use makes no difference.** Its `.cci` is a 16 KiB header followed by the CIA's two contents back to back with no padding, and both sizes are recorded inside the CIA, so the same `.cia` always comes out the same length whatever tool you run.
- **Don't force a mismatch with `-n`.** That builds a CIA with the wrong bytes in it. Both patches were proven to give exactly the CIAs in the table from a fresh decrypt and from copies whose header bytes (card seed, certificates, ticket, TMD) were overwritten with random data, so a mismatch means the source is wrong.
- **Yes, the base patch turns a `.cci` into a `.cia`.** That's deliberate: the decryptor produces a `.cci` for game titles, and a `.cia` is what installs.
- **Finding the right dump:** in most filenames it's `ドラゴンクエストモンスターズ - Joker 3 PROFESSIONAL`, product code CTR-P-BDQJ. The game's banner writes that on two lines; the hyphen is just how dump tools flatten the line break.

**On an emulator, if the names still look old after installing both CIAs:** right click the game in Azahar or Citra and pick Open Mods Location. A `romfs` folder in there overrides the game's data files with whatever it contains, and it beats anything you install as a CIA, so reinstalling will never help. Rename it to `romfs_off` and boot again. It replaces data files only, not the executable, so you can end up running this patch's code with the old translation's text: monster names appear in battle the way this build added them, but they're the old names. Found by Retho on Discord.

## On Linux

The walkthrough above leans on two Windows tools. Neither is special. All the patches need is the base decrypted to a `.cci` of exactly 1,591,599,104 bytes, the update decrypted to a `.cia` of exactly 15,725,568 bytes, and xdelta3.

Dumping doesn't change: pull both titles off the 3DS with GodMode9 as **encrypted** CIAs, no decrypt and no trim. Everything below happens on the PC.

1. Install xdelta3, version 3.1 or newer: `sudo apt install xdelta3` (Debian, Ubuntu), `sudo dnf install xdelta` (Fedora), `sudo pacman -S xdelta3` (Arch).
2. Get [rom-converto](https://github.com/DevYukine/rom-converto/releases/latest) for the decrypting. Grab the CLI build, `chmod +x` it, rename it to `rom-converto` and put it on your `PATH`.
3. Decrypt both:
   ```
   rom-converto ctr decrypt "<japanese base>.cia"
   rom-converto ctr decrypt "<japanese update>.cia"
   ```
4. Turn the decrypted base into a `.cci`, which is what the base patch expects:
   ```
   rom-converto ctr convert "<decrypted base>.cia"
   ```
   - **Turn trimming ON.** Without it the output is around 2.1 GB instead of 1,591,599,104 bytes.
   - Run `rom-converto ctr --help` if that doesn't match your build. Its flags move between releases and the help output is the authority, not this README.
   - oho walked this route on Fedora 44 and reproduced both hashes above, using the GUI AppImage build rather than the CLI, and had to tick the trim option there.
5. **Check both sizes before going further:** base `.cci` exactly 1,591,599,104, update `.cia` exactly 15,725,568. A larger `.cci` is very likely padded out to a card size; the patch needs the untrimmed-but-unpadded layout, a 16 KiB header followed by the CIA's two contents back to back.
6. Apply both patches with the same two xdelta3 commands as above. The base one wants about 2 GB of free RAM.
7. Check what came out: `sha256sum DQMJ3P-base-fixed-0.1.0.cia DQMJ3P-update-fixed-3.4.0.cia`.
8. Copy both to the SD card, open FBI, install the base first and then the update.

Fair warning on step 4: these patches were built and checked on Windows and nobody has reported back from the Linux route end to end, so the conversion step is the one I can't vouch for. The size in step 5 is what tells you whether it worked. If rom-converto won't give you a `.cci` of the right length, both Windows tools run under Wine, and that's the same code path everyone else uses.

## What's fixed

Crashes, soft-locks, text that said the wrong thing, spelling, names cut short in menus and battle, text that didn't fit its box, and Japanese that was never translated. `RELEASE_NOTES.md` has the summary and `FIXES.md` has a paragraph on each.

## Not fixed, known

- **Long monster names get shortened.** A stored name holds 11 characters, so "Metal Pearl Slime" is cut to 11 when you obtain or rename it. A wild one shows its first 11 in battle, or its first 9 plus " A" and " B" when two of a kind are on the field. The record field is 24 bytes; widening it would change the save format.
- **Names already in your save don't change.** The name is written onto the monster once, when you scout or fuse it, so monsters already in your party keep whatever your old build gave them. Only ones you get from now on use the corrected names. Names already cut to 8 stay until renamed.
- **Online content is out of scope:** the Wi-Fi Square shop, download monsters and events, StreetPass and SpotPass exclusives, the transfers. [Anthony's plugin](https://github.com/Anthcny144/DQMJ3P-unobtainable-content) restores it, on a modded 3DS with the Luma plugin loader or on Azahar.
  - It asks for a game whose code is untouched. This build changes 153 words of the update's code: the keyboard tab, the name buffers, the keyboard limits, one built-in prefix, one default greeting, and the routines that write a wild monster's name for battle.
  - I checked all nine addresses it uses (five hooks, four version probes). Every one still holds the stock instructions and the nearest changed word is over three kilobytes away, so the two should coexist. I haven't run them together.
- **Unchecked screens** are "Tier 3" in `TESTING.md`. Found something? Note the exact text and which screen, and tell me in the [issues tab](../../issues). Don't worry about whether it's already known. I'd much rather read the same report twice than miss one.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project). This rebuild starts from the 2021-05-30 Professional patch posted on the woodus.com forum, which used the team's text without their full consent, so the team is credited as the authors of every line it didn't write. The font fix is Lurpigi's. The click by click walkthrough is oho's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English.

The fixes were made with Claude (Anthropic) doing the reading, measuring and scripting. Every wording decision was reviewed and every change checked against the shipped files. This rebuild only fixes what was broken; it doesn't claim the translation.
