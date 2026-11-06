"""Emulator-only graphics patches for the Ver.1.3 update.

Ported from Lurpigi/DQMJ3P-IT-FanTranslation, scripts/build_enhanced_ips.py.
Addresses are virtual (file offset + 0x100000). build_patches returns
(address, replacement ARM words, expected ARM words). The first cave ends
at 0x7b98f4, before the online player-password and upload routines.
See CODE_PATCH_NOTES.md for the address map and platform restrictions.
"""
import struct

BASE = 0x100000

CAVE = 0x7B9810

CAVE_END = 0x7BA000

SET_DEVICE_MEMORY_SIZE = 0x1067F4

DEVICE_HEAP_SIZE_VAR = 0x8C0328

FADE_SCALE = 5.0

DEVICE_HEAP = 0x4700000

DEVICE_HEAP_ORIGINAL = 0x2700000

GROUP_DISTANCE_SLOTS = [
    (0x838104, 0x40DAE8),
    (0x8438BC, 0x58AD94),
    (0x831B4C, 0x3DB6C0),
    (0x834F48, 0x3F4680),
    (0x834ED0, 0x3F4440),
    (0x834FC0, 0x3F470C),
]

def branch(src, dst, link=False):
    return (0xEB000000 if link else 0xEA000000) | (((dst - src - 8) >> 2) & 0xFFFFFF)

def vldr_pc(opcode, src, target):
    offset = target - src - 8
    return opcode | (0x800000 if offset >= 0 else 0) | (abs(offset) >> 2)

def build_cave():
    # Fade, map LOD and field-object activation helpers.
    fade = CAVE
    words = [
        0xEC910A03,
        0xEDDF1A04,
        0xEE200A21,
        0xEE600AA1,
        0xE2800F49,
        0xEC800A03,
        0xE12FFF1E,
        struct.unpack("<I", struct.pack("<f", FADE_SCALE))[0],
    ]
    lod = CAVE + len(words) * 4
    words += [
        0xEE300A00,
        0xEE200A00,
        0xE12FFF1E,
    ]
    scale = CAVE + 7 * 4
    active_s16 = CAVE + len(words) * 4
    words += [
        0xED908A01,
        vldr_pc(0xED1F0A00, active_s16 + 4, scale),
        0xEE288A00,
        0xE12FFF1E,
    ]
    active_s0 = CAVE + len(words) * 4
    words += [
        0xED900A01,
        vldr_pc(0xED5F0A00, active_s0 + 4, scale),
        0xEE200A20,
        0xE12FFF1E,
    ]
    # Expand a spawner group only when the larger model heap is active.
    scale_group = CAVE + len(words) * 4
    words += [
        0xE59F100C,
        0xE5911000,
        0xE3510627,
        0x80800100,
        0xE12FFF1E,
        DEVICE_HEAP_SIZE_VAR,
    ]
    stubs = []
    for _, original in GROUP_DISTANCE_SLOTS:
        stub = CAVE + len(words) * 4
        stubs.append(stub)
        words += [
            0xE92D4008,
            branch(stub + 4, original, link=True),
            0xE8BD4008,
            branch(stub + 12, scale_group),
        ]
    # Try 71 MiB, then retry the stock 39 MiB if the allocation is refused.
    heap = CAVE + len(words) * 4
    words += [
        0xE92D4010,
        0xE1A04000,
        0xE3A00647,
        branch(heap + 12, SET_DEVICE_MEMORY_SIZE, link=True),
        0xE3500000,
        0xB1A00004,
        branch(heap + 24, SET_DEVICE_MEMORY_SIZE, link=True) & 0x0FFFFFFF | 0xB0000000,
        0xE8BD8010,
    ]
    return words, fade, lod, (active_s16, active_s0), stubs, heap

def build_patches():
    """Return (VA, new ARM words, expected ARM words), graphics only."""
    cave, fade, lod, (active_s16, active_s0), stubs, heap = build_cave()
    slots = [
        (slot, [stub], [original])
        for (slot, original), stub in zip(GROUP_DISTANCE_SLOTS, stubs)
    ]
    return slots + [

        (0x1050F0, [0x33A00000], [0x32200001]),

        (0x105460, [branch(0x105460, heap, link=True)], [0xEB0004E3]),

        (0x216420, [branch(0x216420, 0x216450)], [0x0A000006]),

        (0x301584, [branch(0x301584, active_s16, link=True)], [0xED908A01]),
        (0x301844, [branch(0x301844, active_s0, link=True)], [0xED900A01]),
        (0x3018D8, [branch(0x3018D8, active_s0, link=True)], [0xED900A01]),

        (0x1D96A0, [branch(0x1D96A0, fade)], [0xE8910 << 12 | 0x00E]),

        (0x6ECB4C, [branch(0x6ECB4C, lod, link=True)], [0xEE200A00]),
        (CAVE, cave, [0] * len(cave)),
    ]
