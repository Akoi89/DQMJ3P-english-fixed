#!/usr/bin/env python3
"""Build optional online/Enhanced IPS overlays for English Fixed v2.21.

Input is a decompressed update .code, either Japanese Ver.1.3 or English
Fixed v2.21. The overlays do not contain the translation; install both English
Fixed CIAs first. Python 3.9+ and the standard library are enough.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import online_patch as online
import enhanced_patch as enhanced

ROOT = Path(__file__).resolve().parent.parent
CODE_SIZE = 8_159_232
SUPPORTED_MD5 = {
    "566939cd4b5260b4d5265fde9a69462a": "Japanese Ver.1.3",
    "9a7a188b6c050ecdf7ca0f65c57cd6cb": "English Fixed v2.21",
}
VARIANTS = {
    "3ds": "code_online_3ds.ips",
    "azahar": "code_online_azahar.ips",
    "enhanced": "code_online_enhanced.ips",
}
LABELS = {
    0x76C83C: "SIL base URL",
    0x76A0C4: "SpotPass base URL",
    0x7711AA: "NAT check host 1, ASCII",
    0x7711C5: "NAT check host 2, ASCII",
    0x7791DE: "NAT check host 1, UTF-16LE",
    0x779214: "NAT check host 2, UTF-16LE",
    0x4B5878: "Featured communities: send an empty ID list",
    0x356F90: "NEX: skip NASC authentication request",
    0x3572A4: "NEX: skip NASC event wait",
    0x3572C0: "NEX: skip NASC result read",
    0x42D088: "NEX server locator and player token",
    0x356B58: "Call the derived player-password routine",
    0x6B9A60: "Player-password routine and SIL token stub",
    0x56CB48: "SIL: do not queue a NASC/NEX login",
    0x56CB90: "SIL: do not wait for the NEX login flag",
    0x56CBC4: "SIL: write the derived player token",
    0x2CA944: "Grand Prix: bypass the NEX-session check",
    0x288044: "Wi-Fi Square connection state 7: advance to state 10",
    0x2880AC: "Wi-Fi Square connection state 8: advance to state 10",
    0x339EC4: "Gift discs: bypass the NEX-connected check",
    0x1CA434: "Coin shop: bypass the NEX-connected check",
    0x222DE4: "Present Codes: bypass the NEX-connected check",
    0x503E88: "Azahar: enable lazy POST data for an empty body",
    0x503E8C: "Azahar: do not skip the empty POST setup",
    0x6D5F8C: "Azahar: one-byte empty POST entry",
    0x504290: "Azahar: use a 4 KiB response-header buffer",
    0x504294: "Azahar: store the response-header buffer size",
    0x3AA3B4: "Azahar: call the replay upload-size stub",
    0x6B9B60: "Azahar: replay size plus multipart-header allowance",
    0x0050F0: "Enhanced: render every frame in double-speed battles",
    0x005460: "Enhanced: call the larger device-heap stub",
    0x116420: "Enhanced: animate distant monsters every tick",
    0x201584: "Enhanced: scale field-object activation distance (s16)",
    0x201844: "Enhanced: scale field-object activation distance (s0)",
    0x2018D8: "Enhanced: scale field-object activation distance (s0)",
    0x0D96A0: "Enhanced: scale fade distances",
    0x5ECB4C: "Enhanced: keep the higher-detail map tiles longer",
    0x6B9810: "Enhanced: fade, LOD, activation, group and heap stubs",
}
for slot, _ in enhanced.GROUP_DISTANCE_SLOTS:
    LABELS[slot - 0x100000] = "Enhanced: monster-group distance vtable slot"


def check_code(code):
    digest = hashlib.md5(code).hexdigest()
    if len(code) != CODE_SIZE or digest not in SUPPORTED_MD5:
        raise ValueError("Unsupported .code: need decompressed Japanese Ver.1.3 "
                         "or English Fixed v2.21 (see CODE_PATCH_NOTES.md)")
    return SUPPORTED_MD5[digest]


def validate_records(code, records):
    end = 0
    for offset, payload in sorted(records):
        if not payload or offset < end or offset + len(payload) > len(code):
            raise ValueError(f"Overlapping or out-of-range IPS record at {offset:#x}")
        if offset not in LABELS:
            raise ValueError(f"Undocumented IPS record at {offset:#x}")
        end = offset + len(payload)


def build_variants(code, server, nat_server):
    check_code(code)
    common = [
        online.slot_record(code, online.SIL_URL, f"http://{server}:8381/00300701/"),
        online.slot_record(code, online.SPOTPASS_URL,
                           f"http://{server}:8380/p01/nsa/H7btVjYWs7p5dGj6"),
        online.code_record(code, online.FEATURED_ALL_SITE),
    ]
    common += online.nex_player_records(code, f"{server}:45000")
    common += [online.code_record(code, site) for site in online.SKIP_NASC
               if site[0] not in (online.NEX_LOGIN_JOB_START, online.SIL_TOKEN_SITE)]
    common += online.nncs_records(code, f"{server},{nat_server}")
    emulator = common + [online.code_record(code, site) for site in online.AZAHAR_FIXES]
    emulator += online.azahar_upload_records(code)
    graphics = []
    for va, new, old in enhanced.build_patches():
        before = struct.pack(f"<{len(old)}I", *old)
        after = struct.pack(f"<{len(new)}I", *new)
        graphics.append(online.code_record(code, (va - 0x100000, before, after)))
    variants = {"3ds": common, "azahar": emulator, "enhanced": emulator + graphics}
    for records in variants.values():
        validate_records(code, records)
    return {name: sorted(records) for name, records in variants.items()}


def make_outputs(code, server, nat_server):
    variants = build_variants(code, server, nat_server)
    outputs = {VARIANTS[name]: online.write_ips(records)
               for name, records in variants.items()}
    # Include every byte written, even unchanged bytes inside an instruction or
    # string slot. A port must reserve the whole record, not only its byte diff.
    records = {}
    for variant, entries in variants.items():
        for offset, payload in entries:
            if offset not in records:
                records[offset] = {
                    "offset": f"0x{offset:06x}", "va": f"0x{offset + 0x100000:06x}",
                    "size": len(payload), "purpose": LABELS[offset],
                    "before": code[offset:offset + len(payload)].hex(),
                    "after": payload.hex(), "variants": [],
                }
            elif records[offset]["after"] != payload.hex():
                raise ValueError(f"Variant record mismatch at {offset:#x}")
            records[offset]["variants"].append(variant)
    manifest = {
        "address_base": "0x100000", "code_size": CODE_SIZE,
        "supported_md5": SUPPORTED_MD5,
        "server": server, "nat_server": nat_server,
        "patches": {name: {
            "file": VARIANTS[name], "records": len(entries),
            "size": len(outputs[VARIANTS[name]]),
            "sha256": hashlib.sha256(outputs[VARIANTS[name]]).hexdigest(),
        } for name, entries in variants.items()},
        "records": [records[offset] for offset in sorted(records)],
    }
    outputs["patch_manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    outputs["SHA256SUMS"] = "".join(
        f"{hashlib.sha256(outputs[name]).hexdigest()}  {name}\n"
        for name in VARIANTS.values()).encode()
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code", type=Path, required=True, help="decompressed update .code")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "patches" / "optional")
    parser.add_argument("--server", default="188.245.46.173", help="SIL/SpotPass/NEX and first NAT host")
    parser.add_argument("--nat-server", default="78.47.138.100", help="second, different NAT host")
    parser.add_argument("--check", action="store_true", help="compare existing outputs without writing")
    args = parser.parse_args()
    try:
        code = args.code.read_bytes()
        source = check_code(code)
        outputs, manifest = make_outputs(code, args.server, args.nat_server)
        for name in outputs:
            if args.code.resolve() == (args.out_dir / name).resolve():
                raise ValueError("Input and output paths must differ")
        if args.check:
            for name, data in outputs.items():
                if (args.out_dir / name).read_bytes() != data:
                    raise ValueError(f"{name}: differs from the reproducible build")
        else:
            args.out_dir.mkdir(parents=True, exist_ok=True)
            for name, data in outputs.items():
                (args.out_dir / name).write_bytes(data)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{'Verified' if args.check else 'Built'} from {source}")
    for name, patch in manifest["patches"].items():
        print(f'{name}: {patch["records"]} records, {patch["size"]} bytes; {patch["sha256"]}')


if __name__ == "__main__":
    main()
