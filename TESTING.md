# Test route for the fixed DQMJ3 Professional build

Written for the tenth build (2026-09-12) and kept current through the thirty-eighth (2026-09-15). Earlier versions of this file
described the first build only. Nothing here needs a full playthrough; the
tiers are ordered so the checks that prove the most come first.

**Back up your save before any of this.** Nothing in the build touches the
save format, but that is an assumption, not a measurement.

## Already proven on screen, so you do not have to check it

Seen on the emulator during the builds, from a clean New Game each time:

- Boots from the title screen through name entry, character creation, the
  whole opening, the first hub and the field menu. No crash.
- The name-entry keyboard opens on the Latin "Aa" tab with Aa highlighted,
  and X cycles the tabs correctly (tenth build).
- The keyboard's kanji page reads correctly (the original patch's corrupted
  keys, "Round" and "Breath", are gone), and the hiragana page is intact.
- Character creation is fully English.
- The status screen shows a shortened player title fitting its box.
- The Library opens after the first scout; the Skill and Trait lists show the
  renamed entries ("MP Drain Ward+", "Stat Break+").
- Battle prompts, "Round 1", the title banner and the name-entry footers,
  which are redrawn textures and layout text, all render in English.

## Tier 1: the things nobody has seen yet, ten minutes after the first scout

Open the Library from the menu (bottom-left icon of the grid).

| Check | Where | Looking for |
|---|---|---|
| Family table | Library > Monster, top screen | nine family names ("Slime", "Dragon" ...) each fitting its cell; no letter wrapped under the table |
| Bestiary text | Library > Monster > any monster, second page (R) | four lines broken between words, no word split at the edge like "pleasa / nt" |
| A long entry | same, for a monster whose entry runs to five lines (52 do; the Slime does not) | whether a fifth line is visible or cut. Either answer is useful |
| Trait info box | Library > Traits > All > any trait | text broken between words, not mid-word |
| Item help | Library > Items, or the bag menu | same |

## Tier 2: the round 9 names, first shop and first skill books

| Check | Where | Looking for |
|---|---|---|
| Skill books in a shop | any item shop that sells books | names read "<skill> Book" matching the skill list: "Quake Ward Book", "HP Boost SP Book" |
| A book's help line | select a book | "Skill: X" names a skill that exists in the skill list |
| Crack family | any monster with the Crack skill set, skill list | Crack, Crack+, Crack SP, Crack EX |
| Trainee skills | a monster with a trainee class skill | "Trainee Warrior", "Trainee Wizard", "Trainee Fighter" ... |
| Card suits | the three card monsters in the Library | Diamagon Ace, Hawkhart Queen, Cluboon Jack |

## Tier 3: still open from earlier builds

| Check | Where | Looking for |
|---|---|---|
| Trait list width | any long trait name in a list (longest shipped is 27 characters) | whether it clips |
| Colosseum "Battle" pane | Colosseum or Grand Prix screens | the word fits its 20 px pane |
| The 天敵 readout | the reactor | reads in English |
| Helpful Tips titles (fifteenth build) | the tips list | every title whole, none cut mid-word, no 【Category】 prefix |
| Small grey second values (not a defect) | Equip Compare's "after" column, the party screen's max HP/MP | this is the original game's design: the layout draws the max value at 80 % (MonStatus part, same in the Japanese file) and the code shrinks an unchanged compare value; a changed one is full size with an arrow |
| Map marker (seventeenth build) | the Silent Meadows navi map, the marker with the NEXT icon | its pill reads "Wood Park", not "NOW_PRINTING" |
| Item names (twenty-third build) | any item list, the item info window, Equip Accessories | full names, nothing cut at 14 characters; nothing wider than its row |
| Quest hints (twenty-fourth build) | the Silent Meadows scout-quest board, the Shiny Sap and mine puzzle hints | the hint names the same place, container and count as the Japanese; the mine hints say clockwise / counterclockwise |
| Dialogue (twenty-fifth build) | any town, the Aroma quest board, the crystal-cave boulders | no line runs past the box, no page needs a third line, no name insert or highlight looks out of place |
| Reactor analyze panes (twenty-sixth build, not yet seen on screen) | outdoors, reactor on, the two item lines in the analyze readout | item names longer than 10 characters drawn in full; nothing wider than its line |
| Menus (twenty-seventh build) | the Speed Road attack list and its descriptions, the diary, the Present Code screen, any network prompt | nothing runs past its box; the diary's Grim Tundra page reads whole; attack ranges match the list |
| Page layout (twenty-eighth build) | any multi-page dialogue, the Aroma contact call, the summoning shrine | no page opens with a blank line or a leading space; no page needs a third line except the results and instruction panels |
| Term fixes (thirtieth build) | the Darkiron Bastille dialogue, the Snapped family lines, the chapter 7 hint | "Break Remodeling Device" or "Remodeling Device" for the machine; Snapped-off / Snapped-Almighty by name; the chapter 7 hint says you beat the minions and reached the boss |
| Monster names (thirty-first build) | Library > Monster > any family; Manage Monsters, the header; Change Name on any monster | species names drawn whole in the rows ("Golden Pearl Slime"); an 11-letter name whole in the header; the keyboard shows 11 slots and keeps all 11 after OK |
| Books, habitats, Ground Zero (thirty-second build) | the bag's book pages; Library > Monster > Coalslime (habitat); the diary's chapter 7 and 8 pages and the Zoom list | "Gravity Ward SP Book", "Quake & Gravity Ward EX Book" whole in their rows; "Fiery Volcano etc." whole in the Habitat field; "Ground Zero", never "Point Zero" |
| Long names on three panels (thirty-third build) | a monster's Basic Info, the Skill panel on the right; Library > Monster > "Metal Pearl Slime", the header; Library > Skill > any skill, the Monsters list | "Wisdom Boost EX" and "Mystic Juliante" whole; "Metal Pearl Slime" whole in the header; "Metal King Slime" whole in the Monsters list |
| Fifteen more skill books, the Sublime mist (thirty-fifth build) | the bag's book pages; a book's info window; Library > Skill; a monster's traits | "Black / Red / White / Netherworld / Sublime Mister SP Book", "HP Boost EX Book" to "Wisdom Boost EX Book", "Shepherd's Book"; "Skill: HP Boost EX" in that book's help; "Black Mister SP" in the skill list; "Chance Sublime Mister", never "Blue" |
| Help lines and outliers (thirty-sixth build) | the info window of a Dai collab book (Kill-Vearn, Gome-chan, Brass); the bag's book pages; Library > Skill | one skill per line, nothing past the box; "Cure-All SP Book", "Wildcard Book", "Pusugon the Monstrous Book" whole; "Cure-All SP" in the skill list |
| Skill-set help lists (thirty-seventh build) | synthesis > Inherited Skills > Info (Y) on a Dai collab skill set (Great King Vearn, Gome-chan, Brass), which needs a parent that has one; any skill-set help with a Ward or Swelling Strike | one skill per line, nothing past the box; "Blunt Ward+", "Sap Ward+", "Swelling Strike", never "Attack Ward+", "Defense Ward+" or "Pile Driver" |
| Moreheal and the Teaches column (thirty-eighth build) | Allocate Skill Points or Library > Skill on a skill set that teaches a long action name (Gome-chan: Giga Essence Extractor, Miracle of the Stars); the help list of a set or book that teaches ベホイマ (Slime SP, Healer SP, Zoma's Book) | the whole name, clear of the SP numbers; "Moreheal", never "Fullheal", in those lists |
| Letter spacing (fourteenth build) | the status screen's AGI and INT labels, the bestiary second page's "Items" pill, a map place name, the StreetPass list | letters no longer run into each other; nothing now too wide for its pill |

## Tier 4: the Ver.1.3 content, where the new writing lives

39 of the newly translated strings are in the Dai crossover event chain
(A01_02). The Collab Battle at the Monster Arena covers most of them: the
announcement, the ticket prompt, the win and loss lines, and the Vearn,
Myst-Vearn, Great King Vearn and Chiu dialogue.

## If something is wrong

Note the screen, the exact text, and whether the box clips or wraps, and
take a screenshot (or a phone photo of the screen): where a line breaks or
a word is cut is far easier to diagnose from a picture than from a
description. Every
string in the build is traceable to a script step in `_audit/rebuild.py`,
so a wrong line is a one-line fix and a rebuild, never a hand edit.
