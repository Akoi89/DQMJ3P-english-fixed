# The code patch, for anyone porting it to another translation

Written for Lurpigi, whose font fix this build uses and credits, and for
anyone else patching Dragon Quest Monsters: Joker 3 Professional into a
language other than English.

The text work in this project does not transfer, because it is English. The
code patch does, because every fix below is about buffer sizes and a default
tab index, not about words. If your translation has longer names than the
Japanese, you will hit the same walls we did.

Everything here was measured on the running game. Where a number appears, it
came from a debugger or a byte comparison, not from reading a disassembly and
guessing. That distinction cost us several days, and section 5 is the reason.

## 1. Which executable, and the trap that will cost you an evening

This title ships as two CIAs: a base title and an update, `0004000E001ACB00`.
The update's ExeFS `.code` is what actually runs. It is stored BLZ-compressed
(exheader flag byte 0x0D, bit 0).

The trap: on Azahar or Citra, an ExeFS code override for this game has to go
under the **base** title id,
`AzaharPlus/load/mods/00040000001ACB00/exefs/code.bin`, even though the
update's code is the code that runs. Putting it under the update's title id
does nothing at all, silently. We lost an evening to that.

Useful constants for the update's code:

* Decompressed size 8,159,232 bytes, md5 `566939cd4b5260b4d5265fde9a69462a`
  before any patching.
* Virtual address = file offset in the decompressed code + `0x100000`.
* The compressed `.code` as shipped is 4,477,028 bytes. The ExeFS entry after
  `.code` starts at data offset `0x445200`, so there are only about 400 bytes
  of slack. Our patched code compresses 28 bytes larger, to 4,477,056, which leaves
  384 bytes spare. Check yours rather than assume.
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

`0x22f818` has thirteen other callers that also pass 21. We placed some of
them and left the rest: their screens were never identified, so an action
name may still cut at 18 somewhere we did not find. If you go looking, a
one-shot breakpoint logger that records the caller address per screen is the
fastest way to map them.

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

117 changed words in the update's executable, md5 `49ff105d`. Known and not
fixed: the Library monster lists still cut at 10, because a row builder uses a
16-character buffer in which the family icon costs 5 units rather than 1. We
judged that one not worth the risk for the gain.

The base title's executable is untouched.

## 7. Licensing, so it is not a question

Nothing here is claimed as ours to license. The offsets are facts about
someone else's binary. Use them however you like, with no attribution
required. If it helps your players, that is the point.
