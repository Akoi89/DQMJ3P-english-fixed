# Dragon Quest Monsters: Joker 3 Professional, fixed English build

The 2021 English fan translation of DQM Joker 3 Professional (3DS), rebuilt with its defects fixed. Released as two xdelta patches for the Japanese game. The translation is the Joker 3 Translation Team's; this build only fixes what was broken in it.

- `RELEASE_NOTES.md` - what each version fixed
- `FIXES.md` - every fix in detail, grouped by what you'd notice
- `TESTING.md` - the test route, and what nobody has checked yet
- `BUILD_NOTES.md` - the full record
- `CODE_PATCH_NOTES.md` - addresses and traps, for anyone porting the code patch to another language

## What you get

Two xdelta patches that produce the two CIAs from the Japanese game. The CIAs aren't distributed; the table lets you check what the patches produced.

| File | Size | SHA-256 |
|---|---:|---|
| `DQMJ3P-base-fixed-0.1.0.cia` | 1,596,032,000 | 526c784b94e9a7519adf1babfa7325851efa6eb1358830dbb4e5af8ad4333436 |
| `DQMJ3P-update-fixed-3.4.0.cia` | 21,427,200 | 5c1f39991fd3aa4bce7e2605214b5960fc3784d93961e11c76759fbae5d76974 |
| `patches/DQMJ3P-base-fixed-0.1.0.xdelta` | 13,623,736 | 5ff6591a84e56722e577532801776e1a79d847c91577b188b783171995972b74 |
| `patches/DQMJ3P-update-fixed-3.4.0.xdelta` | 4,960,393 | 6e77da022944e13df20a3056a6f6e19954e4081fbab76b2a311d34f4f0e386b1 |

Install **both CIAs**, the base first and then the update. The update carries the Ver.1.3 content and the executable, including the keyboard fix; the base carries the rest of the game's data. With only one of them installed you get a mix of old and new text.

**Back up your save before updating from an older build.** Installing a new build over the old one keeps your save, so there's no need to delete the game first, and deleting it in FBI or the Home Menu can take the save with it. On a 3DS, Checkpoint or JKSM makes the backup. In Azahar or Citra, right click the game, pick Open Save Data Location, and copy that folder somewhere safe.

## Applying the patches

> **Dump both titles as encrypted CIAs and decrypt them on the PC.**
> - With GodMode9, dump each title to CIA with **no decrypt and no trim**, copy them to your computer, and decrypt there. Where GodMode9 offers **Build CIA (legit)** and **Build CIA (standard)**, pick **legit**: standard decrypts while it builds.
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

1. Get your **encrypted** game CIA and **encrypted** update CIA, both Japanese originals. The game is `ドラゴンクエストモンスターズ - Joker 3 PROFESSIONAL` (CTR-P-BDQJ), the update is its Ver.1.3 patch (CTR-U-BDQJ). Already have both as `.cia` files? Check their sizes against the table above and carry on from step 2. Don't install them and build them again with GodMode9 first, since that is how a good file turns into a wrong one.
2. Get [Batch CIA 3DS Decryptor](https://gbatemp.net/download/batch-cia-3ds-decryptor.35098/download?version=35152) and extract it to a new folder.
3. Put the two CIAs in there. Rename the game to `game.cia` and the update to `update.cia`.
4. Run `Batch CIA 3DS Decryptor.bat`. It takes a while on the base.
5. You should now have `game-decrypted.cci` and `update (Patch)-decrypted.cia`.
6. Download the patches zip from the [latest release](https://github.com/Akoi89/DQMJ3P-english-fixed/releases/latest) and extract it to another new folder.
7. Copy the two decrypted files into the patch folder, select both, and drag them onto `apply_patches.bat`.
8. If it stops with a checksum mismatch, go back to **how you dumped**. They must be encrypted dumps decrypted on the PC, not decrypted or trimmed by GodMode9. Check the source sizes above too.
9. You should now have `DQMJ3P-base-fixed-0.1.0.cia` and `DQMJ3P-update-fixed-3.4.0.cia`. Copy both to your SD card.
10. Open FBI on your 3DS (you have it if you followed the usual modding guide), go to SD, and install **the base first, then the update**.
11. **Check both went on.** The title menu shows which versions you have: the small box above Continue says "EN 2.21" (the update patch) and the bottom right corner says "base EN 2.21" (the base patch). No corner line means the base didn't install, so install the base CIA too; "Ver.1.3" in the box means the update didn't. The two numbers should match. Builds before v2.12 show neither.

Thanks to oho, who wrote these steps out on Discord.

### Why it usually goes wrong

- **The base is the file people get wrong.** If yours isn't 1,591,612,416 bytes it's a repack, a cartridge dump, or a build with the update already merged in, and no patch can bridge that. There is only one correct Japanese base.
- **Your decrypted files won't have the same SHA-256 as mine, and that's fine.** The decryptor writes random bytes into everything it makes (a card seed in the `.cci`, ticket bytes in the update `.cia`), and dumps from different places carry different tickets. Since v2.4 the patches don't depend on any of that. v2.3 and earlier did, which is why the update patch failed for some people.
- **Which build of the decryptor you use makes no difference.** Its `.cci` is a 16 KiB header followed by the CIA's two contents back to back with no padding, and both sizes are recorded inside the CIA, so the same `.cia` always comes out the same length whatever tool you run.
- **Don't force a mismatch with `-n`.** That builds a CIA with the wrong bytes in it. Both patches were proven to give exactly the CIAs in the table from a fresh decrypt and from copies whose header bytes (card seed, certificates, ticket, TMD) were overwritten with random data, so a mismatch means the source is wrong.
- **Yes, the base patch turns a `.cci` into a `.cia`.** That's deliberate: the decryptor produces a `.cci` for game titles, and a `.cia` is what installs.
- **Finding the right dump:** in most filenames it's `ドラゴンクエストモンスターズ - Joker 3 PROFESSIONAL`, product code CTR-P-BDQJ. The game's banner writes that on two lines; the hyphen is just how dump tools flatten the line break.

**On an emulator, if the names still look old after installing both CIAs:** right click the game in Azahar or Citra and pick Open Mods Location. A `romfs` folder in there overrides the game's data files with whatever it contains, and it beats anything you install as a CIA, so reinstalling will never help. Rename it to `romfs_off` and boot again. It replaces data files only, not the executable, so you can end up running this patch's code with the old translation's text: monster names appear in battle the way this build added them, but they're the old names. Found by Retho on Discord.

**The same override exists elsewhere.** On Android, Azahar keeps it in its user folder under `load/mods/00040000001ACB00/`. On a real 3DS with Luma, it's `/luma/titles/00040000001ACB00/romfs` on the SD card, and Luma loads it whenever game patching is on. If an old translation's files are in either place, rename the folder the same way. The title menu tells you which is happening: if the box and the corner say this build's version but the text is still old, something is overriding it.

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
   - oho walked this route on Fedora 44 for v2.4 and reproduced that version's hashes, using the GUI AppImage build rather than the CLI, and had to tick the trim option there.
5. **Check both sizes before going further:** base `.cci` exactly 1,591,599,104, update `.cia` exactly 15,725,568. A larger `.cci` is very likely padded out to a card size; the patch needs the untrimmed-but-unpadded layout, a 16 KiB header followed by the CIA's two contents back to back.
6. Apply both patches with the same two xdelta3 commands as above. The base one wants about 2 GB of free RAM.
7. Check what came out: `sha256sum DQMJ3P-base-fixed-0.1.0.cia DQMJ3P-update-fixed-3.4.0.cia`.
8. Copy both to the SD card, open FBI, install the base first and then the update.

Fair warning on step 4: these patches were built and checked on Windows. The size in step 5 is what tells you whether it worked. If rom-converto won't give you a `.cci` of the right length, both Windows tools run under Wine, and that's the same code path everyone else uses.

## Optional online and Enhanced patches

The xdelta patches above still produce the same English Fixed v2.21 CIAs and
hashes. Once both are installed, you can add one of these small IPS files from
[`patches/optional`](patches/optional). They apply on top of the English update;
they do not contain the translation and do not replace either xdelta.

| File | Where it runs | What it adds |
|---|---|---|
| `code_online_3ds.ips` | A real 3DS with Luma | Connection to DQMJ3P Online's replacement servers |
| `code_online_azahar.ips` | Azahar | The same connection, plus Azahar HTTP and replay-upload fixes |
| `code_online_enhanced.ips` | Azahar, on a fast enough device | The Azahar online patch plus the Enhanced changes below |

**Pick one, rename it `code.ips`, and replace any older `code.ips`.** Luma and
Azahar load one IPS per title. Do not stack these files or use a raw `code.bin`
override from a different build: it can replace the English fixes. Removing the
optional IPS returns to the installed v2.21 code.

On a **3DS**, put the renamed 3DS file at
`SD:/luma/titles/00040000001ACB00/code.ips` and enable **Enable game patching**
in Luma's SELECT-at-boot menu. Use the 3DS file on a console. Both Azahar files
are emulator-only; the Enhanced version has crashed at startup on real hardware.

On **Azahar**, right click the game, choose **Open Mods Location**, and put the
renamed Azahar file in `exefs/code.ips`. The complete path is
`<Azahar user directory>/load/mods/00040000001ACB00/exefs/code.ips`.
Use the base title ID, even though the update supplies the executable. For
online play, install the online system modules (LLE) and set up your account
using the [Pretendo Azahar guide](https://pretendo.network/docs/install/citra).
For a console, use [Pretendo with Nimbus](https://pretendo.network/docs/install/3ds).
Android and other emulators have not been checked for these additions.

### What online means here

[DQMJ3P Online](https://github.com/Lurpigi/DQMJ3P-Online) runs the game servers.
Pretendo supplies the system friends login and the player's identity, used to
derive the credentials for the replacement servers. That login is also needed
for random battles, communities, G-Cup, Grand Prix and Present Codes with these
patches; "friends service" does not mean only Friend Battle. SpotPass files come
directly from the project's server. The game's system-login path is retained.

The online project's results, before this English integration:

| Feature | What has been checked |
|---|---|
| Free Battle and Ranked Wi-Fi Battle | Two Azahar instances, and 3DS against Azahar |
| Friend Battle | Implemented; a test with two mutually registered friend accounts is still needed |
| Community creation, official communities by language, featured communities, Community Challenge | Verified by the online project |
| G-Cup: weekly cups, rankings, replays and rewards | Verified by the online project |
| Grand Prix: Masters and Challenger, rankings and rewards | Verified by the online project |
| All 130 original Present Codes | Verified on the server |
| Gift discs and the Wi-Fi Square Network Coin shop | Verified by the online project |
| Field SpotPass events: hidden box, sky monster, StreetPass assassin | Only the hidden box has been seen working; these IPS files do not force background downloads on Azahar |

These builds point to the project's public test server, `188.245.46.173`, and
use `78.47.138.100` for the second NAT check. Availability depends on that
server. See the [online project's guide](https://github.com/Lurpigi/DQMJ3P-Online#readme)
for its current status. A VPN can stop Azahar from finding its local address;
disable it if connection or battle errors appear. The save confirmation can
stay up for about 30 seconds before entering the Square. Battles are direct
P2P, without a relay, so CGNAT or symmetric NAT may stop a match from starting.
After changing Pretendo accounts, a rejected NEX login may need the server
administrator to reset the ID's stored credential.

### What Enhanced changes

- Monsters, NPCs and field objects stay visible five times farther away.
- Distant monsters animate every tick instead of at a reduced update rate.
- Double-speed battles render at 60 fps. The rest of the game stays at 30 fps;
  forcing it to 60 would also double the game logic's speed.
- Higher-detail map tiles remain in use longer at LOD transitions.
- The device heap for models grows from 39 MiB to 71 MiB. New 3DS mode must be
  enabled in Azahar; the wider monster-group range depends on that allocation.

This asks more of the emulator. If it slows down, use `code_online_azahar.ips`
to keep online play without the graphics changes. Use neither Azahar file on a
real 3DS. The Enhanced work was tried on Azahar for PC in the Italian project;
this exact English combination still needs an in-game test.

All three overlays have been checked against the published v2.21 executable
fingerprint. They preserve its 174 changed words and have no overlapping IPS
records. That is a binary check, not a claim of a completed English play test.
[`CODE_PATCH_NOTES.md`](CODE_PATCH_NOTES.md#8-optional-online-and-enhanced-overlays)
has the addresses, source provenance and reproduction commands;
[`TESTING.md`](TESTING.md#optional-online-and-enhanced-overlays) lists what to try.

## What's fixed

Crashes, soft-locks, text that said the wrong thing, spelling, names cut short in menus and battle, text that didn't fit its box, and Japanese that was never translated. `RELEASE_NOTES.md` has the summary and `FIXES.md` has the detail.

## Not fixed, known

- **Long monster names get shortened.** A stored name holds 11 characters, so "Metal Pearl Slime" is cut to 11 when you obtain or rename it. A wild one shows its first 11 in battle, or its first 9 plus " A" and " B" when two of a kind are on the field. The main bosses fight under a short name that fits ("Bundold" rather than "Bundold, the Thief"), and most of them keep the full title in the Library. Some bosses are still cut, like the Insurgent Demons. The record field is 24 bytes; widening it would change the save format.
- **Names already in your save don't change.** The name is written onto the monster once, when you scout or fuse it, so monsters already in your party keep whatever your old build gave them. Only ones you get from now on use the corrected names. Names already cut to 8 stay until renamed.
- **Some discontinued content still needs a separate solution.** The optional online IPS files restore the services listed above; they do not unlock every StreetPass exclusive, transfer or download event. [Anthony's plugin](https://github.com/Anthcny144/DQMJ3P-unobtainable-content) unlocks content on a modded 3DS with the Luma plugin loader or on Azahar.
  - The plugin asks for untouched code. The installed v2.21 translation changes 174 words. The earlier check of its nine addresses (five hooks and four version probes) applies to the translation alone; it is not a compatibility test of these optional overlays.
  - Running the plugin together with the new online or Enhanced IPS has not been tested. Check them separately if anything goes wrong.
- **One label might not fit.** The local wireless battle counter uses the word "Battle" instead of a single character, so it might look cramped. I haven't seen it on screen yet, so a screenshot would settle it.
- **Text that lands against a number or a name the game prints.** The game writes some
  values in at the moment it draws the line, a monster's name, a count, a place. Where a
  translated line sits right up against one of those with no space, nothing in the
  toolchain can see it, because in the stored text the two halves are separate. Every one
  found so far was found by somebody playing. If a line reads like two things run together,
  that is this, and I want it.
- **Unchecked screens** are listed in `TESTING.md`, grouped by where they are in the game. Found something? Note the exact text and which screen, and post it in [the reports thread](https://github.com/Akoi89/DQMJ3P-english-fixed/issues/3). Don't worry about whether it's already known, I'd much rather read the same report twice than miss one.

## Credits

The translation is the Joker 3 Translation Team's work (team lead Z6n4; the GBAtemp Joker 3 project). This rebuild starts from the 2021-05-30 Professional patch posted on the woodus.com forum, which used the team's text without their full consent, so the team is credited as the authors of every line it didn't write. The font fix is Lurpigi's. The click by click walkthrough is oho's. Fifteen UI textures are reused from Team Incarnus's French patch where they had already drawn English. A number of these fixes began as Retho's reports on Discord, including Great Godbird's name and the skill set whose name sent me back to check every other one against the official releases.

The optional online and Enhanced overlays were contributed by Lurpigi, from the DQMJ3P Online and Italian fan-translation projects. Their added scripts, addresses and verification limits are documented separately below the translation's code notes.

The fixes were made with Claude (Anthropic) doing the reading, measuring and scripting. Every wording decision was reviewed and every change checked against the shipped files. This rebuild only fixes what was broken; it doesn't claim the translation.
