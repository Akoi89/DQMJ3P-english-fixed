"""Build a Luma3DS / Azahar code.ips that redirects DQMJ3P's Square Enix servers.

Luma (and Azahar) load ONE code.ips per title, so this tool can merge the records of an
existing patch (e.g. the Italian fan translation) with the URL replacements.

usage (python -I):
  make_url_patch.py --code code.bin --sil-url http://example.org/00300701/ \
      [--infra-url http://example.org/infra/] [--spotpass-url http://example.org:8380/p01/nsa/H7btVjYWs7p5dGj6] \
      [--nex-auth 127.0.0.1:45000 --nex-password PW] [--skip-nasc] [--skip-frd] [--azahar] [--azahar-hle-boss]
      [--nncs 127.0.0.1,127.0.0.2] [--pid-offset 1] [--spotpass-break]
      [--merge other/code.ips] -o code.ips

Install: SD:/luma/titles/00040000001ACB00/code.ips  (3DS, "Enable game patching" on)
         <Azahar user dir>/load/mods/00040000001ACB00/exefs/code.ips
"""
import argparse
import struct
import sys

# String slots in code.bin v1.3 (file offsets = VA - 0x100000), verified in Ghidra.
SIL_URL = (0x76C83C, b"https://dqm32ds.sil2.square-enix.com/00300701/")
INFRA_URL = (0x7BF6D4, b"http://wi-fi.infralib.square-enix.com/")
# SpotPass (BOSS) base URL; tasks are "%s/%s" with "<TASK>/<file>" (re/notes/spotpass_boss.md).
SPOTPASS_URL = (0x76A0C4, b"https://npdl.cdn.nintendowifi.net/p01/nsa/H7btVjYWs7p5dGj6")
# --nncs HOST1,HOST2: NAT check servers (server/nncs). Pia's NatTraverser (FUN_004c8130) uses the
# ASCII pair, the NEX core (FUN_004692d8) the UTF-16 pair.
NNCS_ASCII = [(0x7711AA, b"nncs1.app.nintendowifi.net"), (0x7711C5, b"nncs2.app.nintendowifi.net")]
NNCS_UTF16 = [(0x7791DE, "nncs1.app.nintendowifi.net".encode("utf-16-le")),
              (0x779214, "nncs2.app.nintendowifi.net".encode("utf-16-le"))]

# --skip-nasc: SilAuthJob_Update (0x66cacc) logs in to NEX (NASC LOGIN) and asks NASC for a
# service token (SVCLOC) before talking to SIL; Pretendo answers both with error 110 while the
# game is not registered there. Skip them so the job goes straight to SIL register/login with an
# all-zero token (our SIL server does not verify it). Test builds only.
# The friends-server login that comes first (frd Login, job 0x66ed9c) works on Pretendo with Nimbus.
ARM_NOP = bytes.fromhex("00f020e3")
# --skip-frd: also pretend the frd login succeeded. Without a real login the next frd calls fail
# (Azahar 2026-10-26: error 006-0000 right after AC connect), so this is only a debugging aid.
SKIP_FRD = [  # (file offset, original, replacement)
    # frd job state 0: bne 0x66ee54 -> b 0x66eee4 (success path: flags |= 4, then state 2)
    (0x56EDE0, bytes.fromhex("1b00001a"), bytes.fromhex("3f0000ea")),
    # NgsFacade_LoginAsync_impl: frd HasLoggedIn (FUN_0052c610) == 0 -> beq error. With --nex-auth
    # the NEX login needs nothing else from frd (second test emulator: Pretendo refuses a second
    # session of the same friends account, 002-0121).
    (0x3BB860, bytes.fromhex("0d00000a"), ARM_NOP),
]
# --azahar: work around two Azahar http:C bugs hit by sil_HttpWorker (0x603a10).
# 1. A POST without post data is never sent (BeginRequest leaves it pending until
#    NotifyFinishSendPostData, which refuses contexts without data), so SIL requests with an empty
#    body (nuser/getnonce) time out after 60 s. The worker only enables lazy/chunked post data when
#    the body is non-empty: force it on. The SDK's SendPostDataRaw rejects a NULL/0-length buffer,
#    so the dummy entry used for an empty list ({next, data, alt, size} at 0x7d5f8c, only read
#    there) is made to send one 0x00 byte; the server treats b"\0" as empty. The request digest
#    only covers the real entries, so it is unchanged.
# 2. GetResponseData (all headers) reports min(real size, buffer size) instead of the real size, so
#    the worker's size probe with a 1-byte buffer allocates 1 byte, X-Sil-Digest is never found
#    and every file/* response is rejected (-304, "Download non riuscito"). Replace the probe's
#    error check with a fixed 4 KiB header buffer size; the second call still checks its result.
AZAHAR_FIXES = [
    (0x503E88, bytes.fromhex("0090a003"), ARM_NOP),  # moveq r9,#0
    (0x503E8C, bytes.fromhex("0e00000a"), ARM_NOP),  # beq (skip SetLazyPostDataSetting)
    (0x6D5F8C, bytes(16), bytes.fromhex("00000000" "8c5f7d00" "00000000" "01000000")),
    (0x504290, bytes.fromhex("020110e3"), bytes.fromhex("010aa0e3")),  # tst r0,#0x80000000 -> mov r0,#0x1000
    (0x504294, bytes.fromhex("2000001a"), bytes.fromhex("140084e5")),  # bne error -> str r0,[r4,#0x14]
]
# --azahar-hle-boss: only for Azahar with the HLE BOSS service (no "required online LLE modules"),
# which never downloads tasks and always reports task state 0 while the game waits for 6 ("done")
# before reading NsData (gift discs FUN_00370e94, coin shop FUN_002c9a54). The NsData then come
# from files in the BOSS extdata (re/tools/spotpass_azahar.py). With the real boss module (LLE) use
# --spotpass-url instead.
AZAHAR_HLE_BOSS = [
    (0x58212C, bytes.fromhex("000051e30900a003"), bytes.fromhex("0600a0e31eff2fe1")),  # boss_vfn_68212c: mov r0,#6; bx lr
]
# --nex-auth HOST:PORT + --nex-password PW: real NEX login on our server (server/nex in DEV mode)
# without NASC. The login job asks frd for the NASC game authentication (FUN_00456f50), waits for
# frd's event (FUN_0045724c), then FUN_00456ab4 reads the result with FUN_0052d088 (+0 result 1,
# +4 HTTP 200, +8 char host[32], +0x28 u16 port, +0x30 char token[256]) and the NEX password with
# FUN_0052c674 (32 bytes) before connecting to the authentication server. Skip the frd request and
# wait, and replace both getters: fixed locator, dummy token (DEV server accepts any) and password.
NEX_LOGIN_SKIP_FRD = [
    (0x356F90, bytes.fromhex("8c5803eb"), bytes.fromhex("0000a0e3")),  # bl frd game auth -> mov r0,#0
    (0x3572A4, bytes.fromhex("240000ef"), bytes.fromhex("0000a0e3")),  # svc WaitSynchronization -> mov r0,#0
    (0x3572C0, bytes.fromhex("fe5603eb"), bytes.fromhex("0000a0e3")),  # bl frd last result -> mov r0,#0
]
# --pid-offset N: add N to the principal ID the game reads from frd (GetMyFriendKey wrapper
# 0x52d464, used through FUN_0052c888 by the NEX login and the battle scenes). Lets a second
# emulator with the same friends account log in to our NEX server as another player (DEV mode).
# The wrapper copies cmdbuf[2..5] to the FriendKey; reorder it to make room for the add.
PID_OFFSET_SITE = 0x42D48C
PID_OFFSET_ORIGINAL = bytes.fromhex("080084e2" "0e0090e8" "140094e5" "0c0085e5")  # add r0,r4,#8; ldm r0,{r1-r3}; ldr r0,[r4,#0x14]; str r0,[r5,#0xc]
# --spotpass-break: the game registers BREAK01-03 (field events: stealth box, sky map monster,
# StreetPass assassin) at boot as background tasks (FUN_002277d8: every 24 h, 21 runs) and never
# starts them; the BOSS module runs them on its own schedule (sleep mode on a console), which never
# happens in Azahar. StartTaskImmediate on those scheduled tasks fails in Azahar (0xD8A0A018, no
# HTTP): the BOSS module asks ac:u GetConnectingLocation (0x0014), which Azahar does not implement.
# Foreground tasks skip that check, but the SDK allows only the id "FGONLYT" for them (0x522fa8).
# So when the plaza connect screen (0x5e) reaches state 10 (AC connected; 0x3880f8, also the
# --skip-nasc path) call a routine in the text page padding that downloads the three BREAK files
# one after the other the way the coin shop downloads its table (FUN_00681ec8): Unregister FGONLYT,
# build the URL "<base>/BREAKxx/<file>", RegisterImmediateTask (0x52174c), StartTaskImmediate
# (0x521a74), then sleep 50 ms steps (max 10 s) until GetTaskState (0x521cc8) is 6 (done) or an
# error. The game finds the NsData by data type, not by task id. The BOSS manager
# (0x227398 / 0x682a8c) is created only if none is alive.
BREAK_HOOK = 0x2880F8  # mov r0,#0xa
BREAK_CAVE = 0x6B9900  # zero filled up to the page end 0x7ba000; 0x6b9810-0x6b98f3 is used by code_enhanced.ips
BREAK_FILES = (0x86A140, 0x86A120, 0x86A100)  # "BREAK01/BossStealthBox.bin", "BREAK03/...", "BREAK02/..."
# --azahar: replay uploads. Azahar's http:C sends chunked post data sorted by content, so the 32 KiB
# pieces of a replay arrive shuffled. The HTTP ring buffer size limits a piece, so size it for the
# whole upload: FUN_004aa380 passes it to the HTTP client (+0x58) from the request's +0x18, replace
# that with the data size (+0x20) plus room for the multipart headers.
UPLOAD_SIZE_SITE = (0x3AA3B4, bytes.fromhex("181095e5"))  # ldr r1,[r5,#0x18]
UPLOAD_SIZE_CAVE = 0x6B9B60  # after the --nex-player-password routine
# With --nex-auth: "Comunita' in Evidenza" (FUN_005b5774) sends FindCommunityByGatheringId with
# the gathering ids saved from StreetPass (bl FUN_0023d168, which only copies them). Skip the copy:
# the empty list makes our server answer with every community (server/nex/.../featured.go). A
# stale saved id would look like a search by community code, which must stay exact.
FEATURED_ALL_SITE = (0x4B5878, bytes.fromhex("3a1ef2eb"), ARM_NOP)  # bl FUN_0023d168 -> nop
# --nex-player-password: instead of a shared password, NEX uses the first 8 bytes of
# MD5(salt + friends password) in hex, also sent as the LoginEx token so the server can store it
# on the first login. The friends password (frd:u GetMyPassword, 16 characters) is the player's
# Pretendo NEX password and never leaves the console. MD5: the SIL digest functions.
# The same value fills the SIL token buffer where the game would ask NASC for a service token
# (SilAuthJob_Update case 1: token still empty), so SIL can bind the friend code to the player.
PLAYER_CAVE = 0x6B9A60  # after the --spotpass-break routine
PLAYER_SALT = b"DQMJ3P-Online-v1"
PLAYER_PASSWORD_CALL = (0x356B58, bytes.fromhex("c55603eb"))  # bl FUN_0052c674 in FUN_00456ab4
SIL_TOKEN_SITE = 0x56CBC4  # case 1: beq (token empty -> silAuthRequestAuthToken)
SIL_TOKEN_BUFFER = 0x8CFF54
NEX_LOGIN_JOB_START = 0x56C4EC  # NexLoginJob_Start, faked by --skip-nasc unless --nex-auth
NEX_AUTH_DATA = 0x42D088  # FUN_0052d088 body (0x74 bytes)
NEX_PASSWORD = 0x42C674   # FUN_0052c674 body (0x78 bytes)
SKIP_NASC = [
    (0x56CB48, bytes.fromhex("7afcff0b"), ARM_NOP),  # case 0: bleq 0x66bd38 (queue NEX login)
    (0x56CB90, bytes.fromhex("ba00000a"), ARM_NOP),  # case 1: beq (wait for NEX logged-in flag 0x10)
    (0x56CBC4, bytes.fromhex("0d00000a"), ARM_NOP),  # case 1: beq (token empty -> silAuthRequestAuthToken)
    # The Wi-Fi plaza connection (also from the rankings desk) logs in to NEX through other paths
    # (Azahar: 002-0110). NexLoginJob_Start (0x66c4ec) -> "mov r0,#0; bx lr": report success without
    # NASC. NEX features (battles, communities) stay unusable, SIL does not need them.
    (NEX_LOGIN_JOB_START, bytes.fromhex("f0402de90040a0e1"), bytes.fromhex("0000a0e31eff2fe1")),
    # Ranking Battle connect screen (FUN_003ca8cc): after connecting it requires a live NEX session
    # (FUN_00445fb8 -> NgsFacade state 0x10001), else closes the menu silently. Skip that check.
    (0x2CA944, bytes.fromhex("1900000a"), ARM_NOP),  # beq 0x3ca9b0
    # The plaza's generic connect screen (0x5e, update function 0x3879ac, state in +0x68): states 2/3
    # bring up the AC connection, state 7 (8) then runs a network login task (+0x80 / +0x84) that
    # fails without NEX and is reported through FUN_005f3b74 (006-0000). The AC connection is what
    # the BOSS module needs for gift discs and the coin shop stock, so take the success path
    # (state 10) whatever the task result is.
    (0x288044, bytes.fromhex("800094e5"), bytes.fromhex("2b0000ea")),  # state 7: b 0x3880f8
    (0x2880AC, bytes.fromhex("840094e5"), bytes.fromhex("110000ea")),  # state 8: b 0x3880f8
    # After screen 0x5e the gift disc menu (FUN_00439e58), the coin shop (FUN_002ca3b8) and the
    # present code menu (FUN_00322d70, SIL login in state 8 first) only go on if FUN_00445fb8 (NEX
    # connected) says so: force it at those calls.
    (0x339EC4, bytes.fromhex("3b3000eb"), bytes.fromhex("0100a0e3")),  # gift: bl -> mov r0,#1
    (0x1CA434, bytes.fromhex("dfee05eb"), bytes.fromhex("0100a0e3")),  # coin shop: bl -> mov r0,#1
    (0x222DE4, bytes.fromhex("738c04eb"), bytes.fromhex("0100a0e3")),  # present code: bl -> mov r0,#1
]


def read_ips(data):
    if data[:5] != b"PATCH":
        raise ValueError("not an IPS file")
    records, i = [], 5
    while data[i:i + 3] != b"EOF":
        off = int.from_bytes(data[i:i + 3], "big")
        size = int.from_bytes(data[i + 3:i + 5], "big")
        i += 5
        if size == 0:  # RLE record
            count = int.from_bytes(data[i:i + 2], "big")
            records.append((off, bytes([data[i + 2]]) * count))
            i += 3
        else:
            records.append((off, data[i:i + size]))
            i += size
    return records


def write_ips(records):
    out = bytearray(b"PATCH")
    for off, payload in records:
        if off == 0x454F46:  # "EOF" as an offset would end the patch early
            raise ValueError("record at offset 0x454F46 is not representable")
        for start in range(0, len(payload), 0xFFFF):
            chunk = payload[start:start + 0xFFFF]
            out += (off + start).to_bytes(3, "big") + len(chunk).to_bytes(2, "big") + chunk
    return bytes(out + b"EOF")


def slot_record(code, slot, new_url):
    off, original = slot
    if code[off:off + len(original)] != original:
        sys.exit(f"code.bin does not contain {original!r} at {off:#x}: wrong version (needs v1.3)")
    # The slot is the original string plus its NUL; padding up to the next string is unknown,
    # so never write past the original terminator.
    new = new_url.encode()
    if len(new) > len(original):
        sys.exit(f"{new_url!r} is {len(new)} bytes, max {len(original)} for this slot")
    return off, new + b"\0" * (len(original) + 1 - len(new))


def nncs_records(code, hosts):
    names = hosts.split(",")
    if len(names) != 2 or names[0] == names[1]:
        sys.exit(f"--nncs {hosts!r}: expected two different hosts, HOST1,HOST2")
    records = [slot_record(code, slot, name) for slot, name in zip(NNCS_ASCII, names)]
    for (off, original), name in zip(NNCS_UTF16, names):
        if code[off:off + len(original)] != original:
            sys.exit(f"code.bin does not contain the UTF-16 nncs name at {off:#x}: wrong version (needs v1.3)")
        new = name.encode("utf-16-le")
        if len(new) > len(original):
            sys.exit(f"--nncs {name!r} is too long, max {len(original) // 2} characters")
        records.append((off, new + b"\0" * (len(original) + 2 - len(new))))
    return records


def code_record(code, site):
    off, original, new = site
    if code[off:off + len(original)] != original:
        sys.exit(f"code.bin does not contain {original.hex()} at {off:#x}: wrong version (needs v1.3)")
    return off, new


def arm(*words):
    return b"".join(struct.pack("<I", w) for w in words)


def nex_login_records(code, auth, password):
    """FUN_0052d088 -> fixed NASC result, FUN_0052c674 -> fixed NEX password (see NEX_LOGIN_SKIP_FRD)."""
    host, _, port = auth.rpartition(":")
    if not host or not port.isdigit() or not 0 < int(port) < 0x10000:
        sys.exit(f"--nex-auth {auth!r}: expected HOST:PORT")
    if len(host.encode()) > 15 or len(password.encode()) > 15:
        sys.exit("--nex-auth host and --nex-password must be at most 15 bytes")
    prologue = bytes.fromhex("70402de90050a0e1")  # push {r4,r5,r6,lr}; mov r5,r0
    for off in (NEX_AUTH_DATA, NEX_PASSWORD):
        if code[off:off + len(prologue)] != prologue:
            sys.exit(f"code.bin does not contain the expected function at {off:#x}: wrong version (needs v1.3)")
    auth_data = arm(
        0xE3A01001, 0xE5801000,  # mov r1,#1; str r1,[r0]          result = success
        0xE3A010C8, 0xE5801004,  # mov r1,#200; str r1,[r0,#4]     HTTP status
        0xE28F1028, 0xE891100E,  # adr r1,host; ldm r1,{r1-r3,r12}
        0xE5801008, 0xE580200C, 0xE5803010, 0xE580C014,  # host -> +8
        0xE59F1020, 0xE1C012B8,  # ldr r1,port; strh r1,[r0,#0x28]
        0xE3A01074, 0xE5801030,  # token "t" -> +0x30
        0xE3A00000, 0xE12FFF1E,  # return 0
    ) + host.encode().ljust(16, b"\0") + struct.pack("<I", int(port))
    password_data = arm(
        0xE3A01000, 0xE5801010, 0xE5801014, 0xE5801018, 0xE580101C,  # clear bytes 16..31
        0xE28F100C, 0xE891100E, 0xE880100E,  # adr r1,pw; ldm r1,{r1-r3,r12}; stm r0,{r1-r3,r12}
        0xE3A00000, 0xE12FFF1E,  # return 0
    ) + password.encode().ljust(16, b"\0")
    assert len(auth_data) <= 0x74 and len(password_data) <= 0x78
    return [code_record(code, site) for site in NEX_LOGIN_SKIP_FRD] + [
        (NEX_AUTH_DATA, auth_data), (NEX_PASSWORD, password_data)]


def nex_player_records(code, auth):
    """FUN_0052d088 -> fixed NASC result with the player password as token, and the call to
    FUN_0052c674 -> routine that turns the friends password into the player password."""
    host, _, port = auth.rpartition(":")
    if not host or not port.isdigit() or not 0 < int(port) < 0x10000:
        sys.exit(f"--nex-auth {auth!r}: expected HOST:PORT")
    if len(host.encode()) > 15:
        sys.exit("--nex-auth host must be at most 15 bytes")
    if code[NEX_AUTH_DATA:NEX_AUTH_DATA + 8] != bytes.fromhex("70402de90050a0e1"):
        sys.exit(f"code.bin does not contain the expected function at {NEX_AUTH_DATA:#x}: wrong version (needs v1.3)")
    routine = [
        0xE92D4070,  # +00 push {r4-r6,lr}
        0xE24DD090,  # +04 sub sp,sp,#0x90          MD5 context at sp, digest at sp+0x70
        0xE1A04000,  # +08 mov r4,r0
        None,        # +0c bl 0x52c674              friends password (frd:u GetMyPassword)
        0xE3500000,  # +10 cmp r0,#0
        None,        # +14 blt +74
        0xE5D40000,  # +18 ldrb r0,[r4]
        0xE3500000,  # +1c cmp r0,#0
        0x03E00000,  # +20 mvneq r0,#0              no password: fail, don't hash nothing
        None,        # +24 beq +74
        0xE1A0000D,  # +28 mov r0,sp
        None,        # +2c bl 0x1b24a0              MD5 init
        0xE1A0000D,  # +30 mov r0,sp
        0xE28F1078,  # +34 adr r1,salt
        0xE3A02010,  # +38 mov r2,#16
        None,        # +3c bl 0x3019f0              MD5 update
        0xE1A0000D,  # +40 mov r0,sp
        0xE1A01004,  # +44 mov r1,r4
        0xE3A02010,  # +48 mov r2,#16
        None,        # +4c bl 0x3019f0
        0xE1A0000D,  # +50 mov r0,sp
        0xE28D1070,  # +54 add r1,sp,#0x70
        None,        # +58 bl 0x1b2214              MD5 final
        None,        # +5c bl +7c                   digest to hex in r4
        0xE3A00000,  # +60 mov r0,#0
        0xE5840010, 0xE5840014, 0xE5840018, 0xE584001C,  # +64 clear bytes 16..31 of the buffer
        0xE28DD090,  # +74 add sp,sp,#0x90
        0xE8BD8070,  # +78 pop {r4-r6,pc}
        0xE28D1070,  # +7c add r1,sp,#0x70
        0xE1A00004,  # +80 mov r0,r4
        0xE3A02008,  # +84 mov r2,#8                8 digest bytes = 16 hex digits
        0xE28F3034,  # +88 adr r3,hex
        0xE4D15001,  # +8c loop: ldrb r5,[r1],#1
        0xE1A06225,  # +90 mov r6,r5,lsr #4
        0xE7D36006,  # +94 ldrb r6,[r3,r6]
        0xE4C06001,  # +98 strb r6,[r0],#1
        0xE205500F,  # +9c and r5,r5,#15
        0xE7D35005,  # +a0 ldrb r5,[r3,r5]
        0xE4C05001,  # +a4 strb r5,[r0],#1
        0xE2522001,  # +a8 subs r2,r2,#1
        None,        # +ac bne +8c
        0xE12FFF1E,  # +b0 bx lr
    ]
    calls = {0x0C: (0x52C674, 0xE, True), 0x14: (0x74, 0xB, False), 0x24: (0x74, 0x0, False),
             0x2C: (0x1B24A0, 0xE, True), 0x3C: (0x3019F0, 0xE, True), 0x4C: (0x3019F0, 0xE, True),
             0x58: (0x1B2214, 0xE, True), 0x5C: (0x7C, 0xE, True), 0xAC: (0x8C, 0x1, False)}
    for at, (dst, cond, link) in calls.items():
        dst = dst - 0x100000 if dst >= 0x100000 else PLAYER_CAVE + dst
        routine[at // 4] = branch(PLAYER_CAVE + at, dst, cond, link)
    body = arm(*routine) + PLAYER_SALT + b"0123456789abcdef"
    assert len(PLAYER_SALT) == 16 and len(routine) * 4 == 0xB4
    sil_token = PLAYER_CAVE + len(body)
    body += arm(
        0xE59F0000,                          # ldr r0,buffer
        branch(sil_token + 4, PLAYER_CAVE),  # b routine
        SIL_TOKEN_BUFFER,
    )
    if code[PLAYER_CAVE:PLAYER_CAVE + len(body)] != bytes(len(body)):
        sys.exit(f"code.bin has data at {PLAYER_CAVE:#x}: wrong version (needs v1.3)")
    assert PLAYER_CAVE + len(body) <= 0x6BA000
    auth_data = arm(
        0xE92D4010, 0xE1A04000,  # push {r4,lr}; mov r4,r0
        0xE3A01001, 0xE5801000,  # mov r1,#1; str r1,[r0]          result = success
        0xE3A010C8, 0xE5801004,  # mov r1,#200; str r1,[r0,#4]     HTTP status
        0xE28F1028, 0xE891100E,  # adr r1,host; ldm r1,{r1-r3,r12}
        0xE5801008, 0xE580200C, 0xE5803010, 0xE580C014,  # host -> +8
        0xE59F1020, 0xE1C012B8,  # ldr r1,port; strh r1,[r0,#0x28]
        0xE2840030,              # add r0,r4,#0x30                 token = player password
        branch(NEX_AUTH_DATA + 0x3C, PLAYER_CAVE, link=True),
        0xE3A00000, 0xE8BD8010,  # mov r0,#0; pop {r4,pc}
    ) + host.encode().ljust(16, b"\0") + struct.pack("<I", int(port))
    assert len(auth_data) <= 0x74
    call = arm(branch(PLAYER_PASSWORD_CALL[0], PLAYER_CAVE, link=True))
    return [code_record(code, site) for site in NEX_LOGIN_SKIP_FRD] + [
        (NEX_AUTH_DATA, auth_data), code_record(code, (*PLAYER_PASSWORD_CALL, call)), (PLAYER_CAVE, body),
        code_record(code, (SIL_TOKEN_SITE, bytes.fromhex("0d00000a"),
                           arm(branch(SIL_TOKEN_SITE, sil_token, cond=0x0, link=True))))]


def azahar_upload_records(code):
    cave = arm(
        0xE5951020,  # ldr r1,[r5,#0x20]
        0xE2811901,  # add r1,r1,#0x4000
        0xE12FFF1E,  # bx lr
    )
    if code[UPLOAD_SIZE_CAVE:UPLOAD_SIZE_CAVE + len(cave)] != bytes(len(cave)):
        sys.exit(f"code.bin has data at {UPLOAD_SIZE_CAVE:#x}: wrong version (needs v1.3)")
    call = arm(branch(UPLOAD_SIZE_SITE[0], UPLOAD_SIZE_CAVE, link=True))
    return [code_record(code, (*UPLOAD_SIZE_SITE, call)), (UPLOAD_SIZE_CAVE, cave)]


def pid_offset_record(code, offset):
    if not 0 < offset < 0x100:
        sys.exit("--pid-offset must be between 1 and 255")
    return code_record(code, (PID_OFFSET_SITE, PID_OFFSET_ORIGINAL, arm(
        0xE5940014, 0xE585000C,  # ldr r0,[r4,#0x14]; str r0,[r5,#0xc]   friend code high word
        0xE994000F,              # ldmib r4,{r0-r3}                    result, pid, pad, fc low
        0xE2811000 | offset,     # add r1,r1,#offset
    )))


def branch(src, dst, cond=0xE, link=False):
    """B/BL from file offset src to file offset dst (same 0x100000 base, so offsets work as VAs)."""
    return (cond << 28) | ((0xB if link else 0xA) << 24) | (((dst - src - 8) >> 2) & 0xFFFFFF)


def blx(src, dst):
    """BLX from ARM to a Thumb function at file offset dst."""
    offset = dst - src - 8
    return 0xFA000000 | (((offset >> 1) & 1) << 24) | ((offset >> 2) & 0xFFFFFF)


def spotpass_break_records(code):
    va = BREAK_CAVE + 0x100000
    # Stack: sp+0 5th argument, +8 Task (0x18), +0x20 TaskPolicy (0x20), +0x40 URL (0x200),
    # +0x240 TaskAction (0x7d8).
    routine = [
        0xE92D41F0,  # +000 push {r4-r8,lr}
        0xE24DDEA2,  # +004 sub sp,sp,#0xa20
        0xE59F7138,  # +008 ldr r7,=0x897894        BOSS manager pointer
        0xE5976000,  # +00c ldr r6,[r7]
        0xE3560000,  # +010 cmp r6,#0
        None,        # +014 bne +024
        None,        # +018 bl 0x227398            create the manager
        0xE3500000,  # +01c cmp r0,#0
        None,        # +020 beq +11c
        0xE5975000,  # +024 ldr r5,[r7]
        0xE28F40F8,  # +028 adr r4,files
        0xE5950000,  # +02c loop: ldr r0,[r5]
        0xE5902014,  # +030 ldr r2,[r0,#0x14]
        0xE1A00005,  # +034 mov r0,r5
        0xE28F10F8,  # +038 adr r1,"FGONLYT"
        0xE12FFF32,  # +03c blx r2                   Unregister (no-op if absent)
        0xE4948004,  # +040 ldr r8,[r4],#4
        0xE3580000,  # +044 cmp r8,#0
        None,        # +048 beq +114
        0xE5950000,  # +04c ldr r0,[r5]
        0xE5902050,  # +050 ldr r2,[r0,#0x50]
        0xE1A00005,  # +054 mov r0,r5
        0xE12FFF32,  # +058 blx r2                   base URL
        0xE1A02000,  # +05c mov r2,r0
        0xE1A03008,  # +060 mov r3,r8
        0xE28F10D4,  # +064 adr r1,"%s/%s"
        0xE28D0040,  # +068 add r0,sp,#0x40
        None,        # +06c blx 0x1028d4           sprintf (Thumb)
        0xE28D0008,  # +070 add r0,sp,#8
        None,        # +074 bl 0x520d7c            Task("FGONLYT")
        0xE28D0F90,  # +078 add r0,sp,#0x240
        None,        # +07c bl 0x521734            TaskAction ctor
        0xE28D0F90,  # +080 add r0,sp,#0x240
        0xE28D1040,  # +084 add r1,sp,#0x40
        None,        # +088 bl 0x521688            Initialize(url)
        0xE3500000,  # +08c cmp r0,#0
        None,        # +090 blt +02c
        0xE28D0020,  # +094 add r0,sp,#0x20
        None,        # +098 bl 0x521008            TaskPolicy ctor
        0xE28D0020,  # +09c add r0,sp,#0x20
        0xE3A01EE1,  # +0a0 mov r1,#0xe10
        0xE3A02001,  # +0a4 mov r2,#1
        None,        # +0a8 bl 0x520fd0            Initialize(1 h, 1 run)
        0xE28D0008,  # +0ac add r0,sp,#8
        0xE28D1F90,  # +0b0 add r1,sp,#0x240
        0xE28D2020,  # +0b4 add r2,sp,#0x20
        0xE3A03000,  # +0b8 mov r3,#0
        0xE58D3000,  # +0bc str r3,[sp]
        None,        # +0c0 bl 0x52174c            RegisterImmediateTask
        0xE3500000,  # +0c4 cmp r0,#0
        None,        # +0c8 blt +02c
        0xE28D0008,  # +0cc add r0,sp,#8
        None,        # +0d0 bl 0x521a74            StartTaskImmediate
        0xE3500000,  # +0d4 cmp r0,#0
        None,        # +0d8 blt +02c
        0xE3A070C8,  # +0dc mov r7,#200
        0xE59F0064,  # +0e0 wait: ldr r0,=50000000
        0xE3A01000,  # +0e4 mov r1,#0
        0xEF00000A,  # +0e8 svc 0xa                  SleepThread
        0xE28D0008,  # +0ec add r0,sp,#8
        0xE3A01000,  # +0f0 mov r1,#0
        0xE3A02000,  # +0f4 mov r2,#0
        0xE3A03000,  # +0f8 mov r3,#0
        None,        # +0fc bl 0x521cc8            GetState
        0xE3500006,  # +100 cmp r0,#6
        None,        # +104 bhs +02c               done (6) or error (7-9)
        0xE2577001,  # +108 subs r7,r7,#1
        None,        # +10c bne +0e0
        None,        # +110 b +02c
        0xE3560000,  # +114 cmp r6,#0
        None,        # +118 bleq 0x682a8c          destroy the manager we created
        0xE28DDEA2,  # +11c add sp,sp,#0xa20
        0xE3A0000A,  # +120 mov r0,#0xa              the replaced instruction
        0xE8BD81F0,  # +124 pop {r4-r8,pc}
        *BREAK_FILES, 0,              # +128 files
        *struct.unpack("<2I", b"FGONLYT\0"),  # +138
        *struct.unpack("<2I", b"%s/%s\0\0\0"),  # +140
        0x897894,                     # +148
        50000000,                     # +14c 50 ms
    ]
    calls = {0x014: (0x024, 0x1, False), 0x018: (0x227398, 0xE, True), 0x020: (0x11C, 0x0, False),
             0x048: (0x114, 0x0, False), 0x074: (0x520D7C, 0xE, True),
             0x07C: (0x521734, 0xE, True), 0x088: (0x521688, 0xE, True), 0x090: (0x02C, 0xB, False),
             0x098: (0x521008, 0xE, True), 0x0A8: (0x520FD0, 0xE, True), 0x0C0: (0x52174C, 0xE, True),
             0x0C8: (0x02C, 0xB, False), 0x0D0: (0x521A74, 0xE, True), 0x0D8: (0x02C, 0xB, False),
             0x0FC: (0x521CC8, 0xE, True), 0x104: (0x02C, 0x2, False), 0x10C: (0x0E0, 0x1, False),
             0x110: (0x02C, 0xE, False), 0x118: (0x682A8C, 0x0, True)}
    for at, (dst, cond, link) in calls.items():
        dst = dst - 0x100000 if dst >= 0x100000 else BREAK_CAVE + dst  # absolute VA or cave offset
        routine[at // 4] = branch(BREAK_CAVE + at, dst, cond, link)
    routine[0x6C // 4] = blx(BREAK_CAVE + 0x6C, 0x1028D4 - 0x100000)
    body = arm(*routine)
    if code[BREAK_CAVE:BREAK_CAVE + len(body)] != bytes(len(body)):
        sys.exit(f"code.bin has data at {BREAK_CAVE:#x}: wrong version (needs v1.3)")
    assert va + len(body) <= 0x7BA000
    hook = code_record(code, (BREAK_HOOK, bytes.fromhex("0a00a0e3"), arm(branch(BREAK_HOOK, BREAK_CAVE, link=True))))
    return [hook, (BREAK_CAVE, body)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--code", required=True, help="decompressed code.bin v1.3")
    ap.add_argument("--sil-url", required=True, help="replacement for the Square Enix SIL base URL (keep the trailing /)")
    ap.add_argument("--infra-url", help="replacement for wi-fi.infralib.square-enix.com")
    ap.add_argument("--spotpass-url",
                    help="replacement SpotPass base, e.g. http://host:8380/p01/nsa/H7btVjYWs7p5dGj6 (server/spotpass)")
    ap.add_argument("--azahar-hle-boss", action="store_true",
                    help="Azahar with the HLE BOSS service: report SpotPass tasks as done (data from spotpass_azahar.py)")
    ap.add_argument("--skip-nasc", action="store_true",
                    help="skip NEX login + NASC service token before SIL (test builds, game not on Pretendo)")
    ap.add_argument("--skip-frd", action="store_true", help="also fake the friends-server login (debugging only)")
    ap.add_argument("--nex-auth", metavar="HOST:PORT",
                    help="real NEX login on this authentication server without NASC")
    ap.add_argument("--nex-password", help="shared NEX password for --nex-auth (server in DEV mode)")
    ap.add_argument("--nex-player-password", action="store_true",
                    help="NEX password for --nex-auth derived from the friends password (normal server)")
    ap.add_argument("--azahar", action="store_true",
                    help="work around Azahar http:C bugs (empty POST, header size probe)")
    ap.add_argument("--nncs", metavar="HOST1,HOST2",
                    help="NAT check servers, e.g. 127.0.0.1,127.0.0.2 with server/nncs (local battles)")
    ap.add_argument("--pid-offset", type=int,
                    help="add N to the player's PID (second test emulator, same friends account)")
    ap.add_argument("--spotpass-break", action="store_true",
                    help="download the BREAK01-03 SpotPass files when the plaza connects (Azahar has no sleep mode)")
    ap.add_argument("--merge", action="append", default=[], help="existing code.ips to include")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    code = open(args.code, "rb").read()
    ours = [slot_record(code, SIL_URL, args.sil_url)]
    if args.infra_url:
        ours.append(slot_record(code, INFRA_URL, args.infra_url))
    if args.spotpass_url:
        ours.append(slot_record(code, SPOTPASS_URL, args.spotpass_url))
    if args.azahar_hle_boss:
        ours += [code_record(code, site) for site in AZAHAR_HLE_BOSS]
    if args.nex_password and args.nex_player_password:
        ap.error("--nex-password and --nex-player-password exclude each other")
    if bool(args.nex_auth) != bool(args.nex_password or args.nex_player_password):
        ap.error("--nex-auth needs --nex-password or --nex-player-password")
    if args.nex_player_password and not args.skip_nasc:
        ap.error("--nex-player-password needs --skip-nasc")
    if args.nex_auth:
        ours.append(code_record(code, FEATURED_ALL_SITE))
    if args.nex_player_password:
        ours += nex_player_records(code, args.nex_auth)
    elif args.nex_auth:
        ours += nex_login_records(code, args.nex_auth, args.nex_password)
    if args.skip_nasc:
        # with a real NEX login, NexLoginJob_Start must not be faked
        ours += [code_record(code, site) for site in SKIP_NASC
                 if not (args.nex_auth and site[0] == NEX_LOGIN_JOB_START)
                 and not (args.nex_player_password and site[0] == SIL_TOKEN_SITE)]
    if args.skip_frd:
        ours += [code_record(code, site) for site in SKIP_FRD]
    if args.azahar:
        ours += [code_record(code, site) for site in AZAHAR_FIXES] + azahar_upload_records(code)
    if args.nncs:
        ours += nncs_records(code, args.nncs)
    if args.pid_offset:
        ours.append(pid_offset_record(code, args.pid_offset))
    if args.spotpass_break:
        ours += spotpass_break_records(code)

    # records this tool wrote into a previously merged patch are replaced, not kept
    own_offsets = {SIL_URL[0], INFRA_URL[0], SPOTPASS_URL[0], NEX_AUTH_DATA, NEX_PASSWORD, PID_OFFSET_SITE, BREAK_HOOK, BREAK_CAVE,
                   PLAYER_PASSWORD_CALL[0], PLAYER_CAVE, UPLOAD_SIZE_SITE[0], UPLOAD_SIZE_CAVE, FEATURED_ALL_SITE[0]} | {
        off for off, _, _ in SKIP_NASC + SKIP_FRD + AZAHAR_FIXES + AZAHAR_HLE_BOSS + NEX_LOGIN_SKIP_FRD} | {
        off for off, _ in NNCS_ASCII + NNCS_UTF16}
    merged = []
    for path in args.merge:
        for off, payload in read_ips(open(path, "rb").read()):
            if off in own_offsets:
                continue
            for o, p in ours:
                if off < o + len(p) and o < off + len(payload):
                    sys.exit(f"{path}: record at {off:#x} overlaps our patch at {o:#x}")
            merged.append((off, payload))

    open(args.out, "wb").write(write_ips(merged + ours))
    print(f"wrote {args.out}: {len(merged)} merged records + {len(ours)} records of ours")


if __name__ == "__main__":
    main()
