# The code patch, for anyone porting it to another translation

Written for Lurpigi, whose font fix this build uses and credits, and for
anyone else patching Dragon Quest Monsters: Joker 3 Professional into a
language other than English.

The text work in this project does not transfer, because it is English. The
code patch does, because every fix below is about buffer sizes and a default
tab index, not about words. If your translation has longer names than the
Japanese, you will hit the same walls I did.

Everything here was measured on the running game. Where a number appears, it
came from a debugger or a byte comparison, not from reading a disassembly and
guessing. That distinction cost me several days, and section 5 is the reason.

## 1. Which executable, and the trap that will cost you an evening

This title ships as two CIAs: a base title and an update, `0004000E001ACB00`.
The update's ExeFS `.code` is what actually runs. It is stored BLZ-compressed
(exheader flag byte 0x0D, bit 0).

The trap: on Azahar or Citra, an ExeFS code override for this game has to go
under the **base** title id,
`AzaharPlus/load/mods/00040000001ACB00/exefs/code.bin`, even though the
update's code is the code that runs. Putting it under the update's title id
does nothing at all, silently. I lost an evening to that.

Useful constants for the update's code:

* Decompressed size 8,159,232 bytes, md5 `566939cd4b5260b4d5265fde9a69462a`
  before any patching.
* Virtual address = file offset in the decompressed code + `0x100000`.
* The compressed `.code` as shipped is 4,477,028 bytes. The ExeFS entry after
  `.code` starts at data offset `0x445200`, so there are only about 400 bytes
  of slack. My patched code compresses 20 bytes larger, to 4,477,048, which
  leaves 392 bytes spare. Check yours rather than assume.
* 3dstool round-trips the compression exactly: recompressing the untouched
  decompressed code reproduces the shipped bytes byte for byte. That is worth
  verifying once on your own copy before you trust a rebuild.

## 2. The name-entry keyboard opens on the Latin tab (3 words)

Without this, every player of a Latin-alphabet patch presses X five times
before typing a name. Three words, at file offsets in the decompressed code:

| offset | old | new |
|---|---|---|
| `0x0012aca0` | `00 10 A0 E3` | `05 10 A0 E3` |
| `0x0012b0f0` | `00 F0 20 E3` | `90 A0 84 E5` |
| `0x0012b0f4` | `00 F0 20 E3` | `88 A0 84 E5` |

The keyboard keeps two page-index fields and they must agree, or the tab
highlight and the page you are shown come apart. The second and third words
are what keep them in step.

## 3. The 14-character panels (13 words)

Three unrelated screens all cut names at exactly 14: the Library Basic Info
header, Library > Skill's "Monsters" list, and the status screen's Skill
panel. One shared shape causes all three. Two builders format `u"%ls%ls"`,
a one-unit icon plus the name, into a 16-character stack buffer with the
wrapper's max set to 15. Sixteen units, minus the NUL, minus the icon, is
fourteen visible characters.

| builder | buffer | draws |
|---|---|---|
| `0x2317d8` | sp+0x30, 16 chars, frame 0x60 | Library Basic Info header; Library > Skill "Monsters" |
| `0x231410` | sp+8, 16 chars, frame 0x4c | status screen Skill panel |

Both buffers grow to 32 characters and both frames grow to hold them:

* `0x2317d8`: `sub sp,#0x60`->`#0x80`, `mov r8,#0x10`->`#0x20`,
  `moveq r1,#8`->`#0x10`, `mov r2,#0xf`->`#0x1f`,
  `add r2,sp,#0x50`->`#0x70`, `add sp,#0x60`->`#0x80`.
* `0x231410`: `sub sp,#0x4c`->`#0x6c`, `mov r7,#0x10`->`#0x20`,
  `add r0,sp,#0x28`->`#0x48`, `add r2,sp,#0x28`->`#0x48`,
  `mov r2,#0xf`->`#0x1f`, `add r2,sp,#0x48`->`#0x68`,
  `add sp,#0x4c`->`#0x6c`.

**The word that is easy to miss, and it black-screens the game.** `0x2317d8`
has a second path for a null name object, which zero-fills the buffer and
then branches back into the common tail. Two addresses, and they are not the
same one, which is worth spelling out because the loop is easy to find and
the count is not:

* the loop body sits at `0x2318a8`, past the function's own `add sp` at
  `0x2318a0`, storing a halfword at a time.
* the COUNT is set far earlier, at `0x231808`, `moveq r1,#8`: eight turns
  writing 4 bytes each, 32 bytes, the old buffer size. That is the word you
  have to change, to `#0x10`.

Leave the count at 8 with a 64-byte buffer and the tail gets 32 bytes of
uninitialised stack. The game dies on the boot logos, because that path runs
before the title screen. A disassembly that stops at the first `pop` will not
show you the loop at all.

## 4. Two more caps of the same family

* **The Teaches list cut action names at 18.** The row builder `0x3bd0b4`
  handed the icon-and-name formatter `0x22f818` a 21-character buffer: two
  icon codes, eighteen letters, the NUL. Five words grow that frame
  `0x48`->`0x88`, move the buffer to sp+0x48 and raise the capacity to 32.
  The longest real action name is 23 characters.
* **The skill-point hint cut ability names at 10.** The wrapper `0x22fa1c`
  formats into a 21-character buffer, and this caller asks for *coloured*
  icons, whose colour codes eat 10 of the 21. Five words give it a
  40-character buffer in a grown frame.

`0x22f818` has thirteen other callers that also pass 21. I placed some of
them and left the rest: their screens were never identified, so an action
name may still cut at 18 somewhere I did not find. If you go looking, a
one-shot breakpoint logger that records the caller address per screen is the
fastest way to map them.

## 4b. Wild monsters had no name in battle at all (36 words)

If your species names run past eleven characters, your wild monsters have no
name in battle. This one is worth checking in any translation of this game.

A monster record's display name is a 24-byte field at +4, eleven UTF-16
characters and a terminator, with the species id at +0x1c. The battle window's
`tb_mnsname_N_MM` panes and the enemy Status header draw that field. Two spawn
writers fill it and both skipped rather than cut:

| function | what it did | words |
|---|---|---|
| `0x1d068c` (one record) | `wcslen(name)+1 > 12 ? skip : wcscpy(rec+4, name)` | 7 at `0x1d06f0` |
| `0x1d1a70` (a range) | the same | 7 at `0x1d1adc` |

Each seven-word run becomes `mov r2,#0x16; mov r1,<name>; add r0,<rec>,#4;
bl 0x301a9c; mov r3,#0; strh r3,[<rec>,#0x1a]; nop`, where `0x301a9c` is the
ARM `memcpy` this file already uses. It copies a fixed 22 bytes, so a short
name is read past its terminator; that is a read of loaded text and the
terminator written at character eleven keeps the extra out of everything.

The duplicate labeler `0x1d003c` appends `LayoutMessage`'s `suffixA` to
`suffixH` with `wcscat` and skipped when the result would not fit. Its skip
(`bhi` at `0x1d02cc`) becomes a nop, both `blx wcscat` (`0x1d02fc` and
`0x1d0318`) become `bl 0x1d00e4`, and `0x1d00e4` to `0x1d011c`, which held the
function's two impossible-length exception throws, holds a routine that cuts
the name at nine characters and appends the suffix. Pair that with a space in
your suffix strings, or change the nine: it is `add r2,r0,#0x12` at
`0x1d00e4`, an immediate in bytes, two per character.

Trim a trailing space before you append, or names whose cut lands on a space
render with two of them ("Mandrake  A"). 63 of this game's 880 species do. The
three words for it came from retiring the guard pair at `0x1d0100`
(`cmp fp,sl; bls 0x1d0120`), which is always taken because `fp <= sl` is
established just above it, so the branch feeding it at `0x1d00e0` can go
straight to `0x1d0120` and the whole region becomes fifteen contiguous words.

Two StreetPass opponent writers (`0x292078` and `0x293960`) format into the
same 24-byte field with a 24-character bound, so a long name runs over the
species id. Both are twelve now.

The naming keyboard after a scout pre-fills two characters: `mov r1,#2` at
`0x22ad9c`, the mode-3 branch of `menu/name.arc`'s init. Pass **zero**, not a
bigger literal. Zero makes the callee read the initial text's own length and
clamp that to the slot count; a literal makes it ask for that many characters
whether they exist or not, and the per-character fetch at `0x3212ec` aborts on
a short name, which crashes the game on every fusion. I shipped that mistake
for about an hour. Zero is what every other mode passes, at `0x22acc0`.

Two things that cost a night. `0x15b068` looks unreferenced and is not,
because `0x15b064` falls through into it, and overwriting it black-screens the
game. And there is no free padding at the end of the text segment, which is
why the routine above had to go inside the function that needed it.

## 5. How these were actually found, which matters more than the addresses

Every one of these caps was first attributed to the wrong code by a static
read, and the live debugger corrected it every time.

The clearest case: the stored monster name holds 11 characters and the game
writes 11 at capture. Nothing truncates it in the record. The three cuts a
player sees are three separate display and input limits, and the lineage
chain a static pass had blamed turned out to serve a different screen
entirely, which is why raising it changed nothing on screen.

What worked: Azahar's GDB stub (`use_gdbstub=true`, port 24689), driven by a
small client for breakpoints, write watchpoints, memory reads and pokes. Put
a read watchpoint on a stored name, walk the stack, and the builder that is
actually drawing the panel names itself. One caution: the stub halts the game
whenever no client is attached, so keep an agent connected for the session.

And verify on a fresh boot rather than a save state. A save state will not
re-run the paths that build these panels, and the black-screen bug in section
3 only appears before the title screen.

## 6. Where this build stands

153 changed words in the update's executable, md5 `f6b40eef`. If you are
counting against codepatch.py, that file has 154 entries: the one at `0x7747a8`
writes the bytes already there and changes nothing, so the built file differs
from the Japanese original in 153 words. These notes said 154 until v2.7,
because the figure came from the length of the list rather than the artifact.
An earlier
version of this section said 117 words and listed the Library monster lists as
known and not fixed. Both were stale: that cap was fixed in the thirty-first
build by raising the row builder's 16-character buffer to 38 (`0x3435d4`,
with the frame grown to hold it), and the word count had not been updated
since. Nothing in the name family is known-broken now.

The base title's executable is untouched.

## 7. Licensing, so it is not a question

Nothing here is claimed as mine to license. The offsets are facts about
someone else's binary. Use them however you like, with no attribution
required. If it helps your players, that is the point.
