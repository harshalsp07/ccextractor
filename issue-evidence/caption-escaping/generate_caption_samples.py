from pathlib import Path
import struct
out = Path(__file__).resolve().parent

def odd_parity(b):
    return b if b.bit_count() % 2 else b | 0x80

def group(ms, pairs):
    return struct.pack("<QH", ms, len(pairs)) + b"".join(
        bytes([4, odd_parity(a), odd_parity(b)]) for a, b in pairs)

for name, caption in [("plain", "HELLO WORLD"), ("markup", "<BOB> & HI")]:
    caption = caption.ljust((len(caption) + 1) // 2 * 2).encode("ascii")
    data = bytes.fromhex("ccccedcc00500001000000")
    data += group(0, [(0x14, 0x20), (0x14, 0x20), (0x14, 0x60)]
                  + list(zip(caption[::2], caption[1::2])))
    data += group(1000, [(0x14, 0x2f), (0x14, 0x2f)])
    data += group(3000, [(0x14, 0x2c), (0x14, 0x2c)])
    (out / (name + ".bin")).write_bytes(data)

print("Generated markup.bin and plain.bin")
