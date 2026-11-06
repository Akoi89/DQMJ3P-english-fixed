# Optional IPS address map

Generated from `patch_manifest.json`. Offsets address the decompressed update `.code`;
VA = offset + `0x100000`. Ends are exclusive. Reserve every byte of each record.
The complete before/after byte strings, including the longer routines and strings,
are in the manifest. All words and byte strings below are little-endian as stored.

| Offset | VA | End offset | Bytes | Variants | Before -> after | Purpose |
|---|---|---|---:|---|---|---|
| `0x0050f0` | `0x1050f0` | `0x0050f4` | 4 | enhanced | `01002032` -> `0000a033` | Enhanced: render every frame in double-speed battles |
| `0x005460` | `0x105460` | `0x005464` | 4 | enhanced | `e30400eb` -> `1bd11aeb` | Enhanced: call the larger device-heap stub |
| `0x0d96a0` | `0x1d96a0` | `0x0d96a4` | 4 | enhanced | `0e0091e8` -> `5a8017ea` | Enhanced: scale fade distances |
| `0x116420` | `0x216420` | `0x116424` | 4 | enhanced | `0600000a` -> `0a0000ea` | Enhanced: animate distant monsters every tick |
| `0x1ca434` | `0x2ca434` | `0x1ca438` | 4 | 3ds, azahar, enhanced | `dfee05eb` -> `0100a0e3` | Coin shop: bypass the NEX-connected check |
| `0x201584` | `0x301584` | `0x201588` | 4 | enhanced | `018a90ed` -> `ace012eb` | Enhanced: scale field-object activation distance (s16) |
| `0x201844` | `0x301844` | `0x201848` | 4 | enhanced | `010a90ed` -> `00e012eb` | Enhanced: scale field-object activation distance (s0) |
| `0x2018d8` | `0x3018d8` | `0x2018dc` | 4 | enhanced | `010a90ed` -> `dbdf12eb` | Enhanced: scale field-object activation distance (s0) |
| `0x222de4` | `0x322de4` | `0x222de8` | 4 | 3ds, azahar, enhanced | `738c04eb` -> `0100a0e3` | Present Codes: bypass the NEX-connected check |
| `0x288044` | `0x388044` | `0x288048` | 4 | 3ds, azahar, enhanced | `800094e5` -> `2b0000ea` | Wi-Fi Square connection state 7: advance to state 10 |
| `0x2880ac` | `0x3880ac` | `0x2880b0` | 4 | 3ds, azahar, enhanced | `840094e5` -> `110000ea` | Wi-Fi Square connection state 8: advance to state 10 |
| `0x2ca944` | `0x3ca944` | `0x2ca948` | 4 | 3ds, azahar, enhanced | `1900000a` -> `00f020e3` | Grand Prix: bypass the NEX-session check |
| `0x339ec4` | `0x439ec4` | `0x339ec8` | 4 | 3ds, azahar, enhanced | `3b3000eb` -> `0100a0e3` | Gift discs: bypass the NEX-connected check |
| `0x356b58` | `0x456b58` | `0x356b5c` | 4 | 3ds, azahar, enhanced | `c55603eb` -> `c08b0deb` | Call the derived player-password routine |
| `0x356f90` | `0x456f90` | `0x356f94` | 4 | 3ds, azahar, enhanced | `8c5803eb` -> `0000a0e3` | NEX: skip NASC authentication request |
| `0x3572a4` | `0x4572a4` | `0x3572a8` | 4 | 3ds, azahar, enhanced | `240000ef` -> `0000a0e3` | NEX: skip NASC event wait |
| `0x3572c0` | `0x4572c0` | `0x3572c4` | 4 | 3ds, azahar, enhanced | `fe5603eb` -> `0000a0e3` | NEX: skip NASC result read |
| `0x3aa3b4` | `0x4aa3b4` | `0x3aa3b8` | 4 | azahar, enhanced | `181095e5` -> `e93d0ceb` | Azahar: call the replay upload-size stub |
| `0x42d088` | `0x52d088` | `0x42d0e4` | 92 | 3ds, azahar, enhanced | Full bytes in manifest | NEX server locator and player token |
| `0x4b5878` | `0x5b5878` | `0x4b587c` | 4 | 3ds, azahar, enhanced | `3a1ef2eb` -> `00f020e3` | Featured communities: send an empty ID list |
| `0x503e88` | `0x603e88` | `0x503e8c` | 4 | azahar, enhanced | `0090a003` -> `00f020e3` | Azahar: enable lazy POST data for an empty body |
| `0x503e8c` | `0x603e8c` | `0x503e90` | 4 | azahar, enhanced | `0e00000a` -> `00f020e3` | Azahar: do not skip the empty POST setup |
| `0x504290` | `0x604290` | `0x504294` | 4 | azahar, enhanced | `020110e3` -> `010aa0e3` | Azahar: use a 4 KiB response-header buffer |
| `0x504294` | `0x604294` | `0x504298` | 4 | azahar, enhanced | `2000001a` -> `140084e5` | Azahar: store the response-header buffer size |
| `0x56cb48` | `0x66cb48` | `0x56cb4c` | 4 | 3ds, azahar, enhanced | `7afcff0b` -> `00f020e3` | SIL: do not queue a NASC/NEX login |
| `0x56cb90` | `0x66cb90` | `0x56cb94` | 4 | 3ds, azahar, enhanced | `ba00000a` -> `00f020e3` | SIL: do not wait for the NEX login flag |
| `0x56cbc4` | `0x66cbc4` | `0x56cbc8` | 4 | 3ds, azahar, enhanced | `0d00000a` -> `da33050b` | SIL: write the derived player token |
| `0x5ecb4c` | `0x6ecb4c` | `0x5ecb50` | 4 | enhanced | `000a20ee` -> `373303eb` | Enhanced: keep the higher-detail map tiles longer |
| `0x6b9810` | `0x7b9810` | `0x6b98f4` | 228 | enhanced | Full bytes in manifest | Enhanced: fade, LOD, activation, group and heap stubs |
| `0x6b9a60` | `0x7b9a60` | `0x6b9b40` | 224 | 3ds, azahar, enhanced | Full bytes in manifest | Player-password routine and SIL token stub |
| `0x6b9b60` | `0x7b9b60` | `0x6b9b6c` | 12 | azahar, enhanced | `000000000000000000000000` -> `201095e5011981e21eff2fe1` | Azahar: replay size plus multipart-header allowance |
| `0x6d5f8c` | `0x7d5f8c` | `0x6d5f9c` | 16 | azahar, enhanced | `00000000000000000000000000000000` -> `000000008c5f7d000000000001000000` | Azahar: one-byte empty POST entry |
| `0x731b4c` | `0x831b4c` | `0x731b50` | 4 | enhanced | `c0b63d00` -> `94987b00` | Enhanced: monster-group distance vtable slot |
| `0x734ed0` | `0x834ed0` | `0x734ed4` | 4 | enhanced | `40443f00` -> `b4987b00` | Enhanced: monster-group distance vtable slot |
| `0x734f48` | `0x834f48` | `0x734f4c` | 4 | enhanced | `80463f00` -> `a4987b00` | Enhanced: monster-group distance vtable slot |
| `0x734fc0` | `0x834fc0` | `0x734fc4` | 4 | enhanced | `0c473f00` -> `c4987b00` | Enhanced: monster-group distance vtable slot |
| `0x738104` | `0x838104` | `0x738108` | 4 | enhanced | `e8da4000` -> `74987b00` | Enhanced: monster-group distance vtable slot |
| `0x7438bc` | `0x8438bc` | `0x7438c0` | 4 | enhanced | `94ad5800` -> `84987b00` | Enhanced: monster-group distance vtable slot |
| `0x76a0c4` | `0x86a0c4` | `0x76a0ff` | 59 | 3ds, azahar, enhanced | Full bytes in manifest | SpotPass base URL |
| `0x76c83c` | `0x86c83c` | `0x76c86b` | 47 | 3ds, azahar, enhanced | Full bytes in manifest | SIL base URL |
| `0x7711aa` | `0x8711aa` | `0x7711c5` | 27 | 3ds, azahar, enhanced | Full bytes in manifest | NAT check host 1, ASCII |
| `0x7711c5` | `0x8711c5` | `0x7711e0` | 27 | 3ds, azahar, enhanced | Full bytes in manifest | NAT check host 2, ASCII |
| `0x7791de` | `0x8791de` | `0x779214` | 54 | 3ds, azahar, enhanced | Full bytes in manifest | NAT check host 1, UTF-16LE |
| `0x779214` | `0x879214` | `0x77924a` | 54 | 3ds, azahar, enhanced | Full bytes in manifest | NAT check host 2, UTF-16LE |
