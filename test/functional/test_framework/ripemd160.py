#!/usr/bin/env python3
# Copyright (c) 2014-2020 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""In-tree RIPEMD-160 matching src/crypto/ripemd160.cpp.

Do not call OpenSSL via hashlib: Ubuntu 22.04's default provider omits RIPEMD160.
"""


def _rol(x, i):
    return ((x << i) | ((x & 0xffffffff) >> (32 - i))) & 0xffffffff


def _f1(x, y, z):
    return x ^ y ^ z


def _f2(x, y, z):
    return (x & y) | (~x & z)


def _f3(x, y, z):
    return (x | ~y) ^ z


def _f4(x, y, z):
    return (x & z) | (y & ~z)


def _f5(x, y, z):
    return x ^ (y | ~z)


def _round(a, b, c, d, e, f, x, k, r):
    a = (_rol((a + f + x + k) & 0xffffffff, r) + e) & 0xffffffff
    c = _rol(c, 10)
    return a, c


def _transform(s, chunk):
    def u32(i):
        return int.from_bytes(chunk[i:i + 4], "little")

    w = [u32(i) for i in range(0, 64, 4)]
    a1, b1, c1, d1, e1 = s
    a2, b2, c2, d2, e2 = s

    def r11(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f1(b, c, d), x, 0, r)

    def r21(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f2(b, c, d), x, 0x5A827999, r)

    def r31(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f3(b, c, d), x, 0x6ED9EBA1, r)

    def r41(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f4(b, c, d), x, 0x8F1BBCDC, r)

    def r51(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f5(b, c, d), x, 0xA953FD4E, r)

    def r12(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f5(b, c, d), x, 0x50A28BE6, r)

    def r22(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f4(b, c, d), x, 0x5C4DD124, r)

    def r32(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f3(b, c, d), x, 0x6D703EF3, r)

    def r42(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f2(b, c, d), x, 0x7A6D76E9, r)

    def r52(a, b, c, d, e, x, r):
        return _round(a, b, c, d, e, _f1(b, c, d), x, 0, r)

    # Direct translation of src/crypto/ripemd160.cpp Transform().
    a1, c1 = r11(a1, b1, c1, d1, e1, w[0], 11)
    a2, c2 = r12(a2, b2, c2, d2, e2, w[5], 8)
    e1, b1 = r11(e1, a1, b1, c1, d1, w[1], 14)
    e2, b2 = r12(e2, a2, b2, c2, d2, w[14], 9)
    d1, a1 = r11(d1, e1, a1, b1, c1, w[2], 15)
    d2, a2 = r12(d2, e2, a2, b2, c2, w[7], 9)
    c1, e1 = r11(c1, d1, e1, a1, b1, w[3], 12)
    c2, e2 = r12(c2, d2, e2, a2, b2, w[0], 11)
    b1, d1 = r11(b1, c1, d1, e1, a1, w[4], 5)
    b2, d2 = r12(b2, c2, d2, e2, a2, w[9], 13)
    a1, c1 = r11(a1, b1, c1, d1, e1, w[5], 8)
    a2, c2 = r12(a2, b2, c2, d2, e2, w[2], 15)
    e1, b1 = r11(e1, a1, b1, c1, d1, w[6], 7)
    e2, b2 = r12(e2, a2, b2, c2, d2, w[11], 15)
    d1, a1 = r11(d1, e1, a1, b1, c1, w[7], 9)
    d2, a2 = r12(d2, e2, a2, b2, c2, w[4], 5)
    c1, e1 = r11(c1, d1, e1, a1, b1, w[8], 11)
    c2, e2 = r12(c2, d2, e2, a2, b2, w[13], 7)
    b1, d1 = r11(b1, c1, d1, e1, a1, w[9], 13)
    b2, d2 = r12(b2, c2, d2, e2, a2, w[6], 7)
    a1, c1 = r11(a1, b1, c1, d1, e1, w[10], 14)
    a2, c2 = r12(a2, b2, c2, d2, e2, w[15], 8)
    e1, b1 = r11(e1, a1, b1, c1, d1, w[11], 15)
    e2, b2 = r12(e2, a2, b2, c2, d2, w[8], 11)
    d1, a1 = r11(d1, e1, a1, b1, c1, w[12], 6)
    d2, a2 = r12(d2, e2, a2, b2, c2, w[1], 14)
    c1, e1 = r11(c1, d1, e1, a1, b1, w[13], 7)
    c2, e2 = r12(c2, d2, e2, a2, b2, w[10], 14)
    b1, d1 = r11(b1, c1, d1, e1, a1, w[14], 9)
    b2, d2 = r12(b2, c2, d2, e2, a2, w[3], 12)
    a1, c1 = r11(a1, b1, c1, d1, e1, w[15], 8)
    a2, c2 = r12(a2, b2, c2, d2, e2, w[12], 6)

    e1, b1 = r21(e1, a1, b1, c1, d1, w[7], 7)
    e2, b2 = r22(e2, a2, b2, c2, d2, w[6], 9)
    d1, a1 = r21(d1, e1, a1, b1, c1, w[4], 6)
    d2, a2 = r22(d2, e2, a2, b2, c2, w[11], 13)
    c1, e1 = r21(c1, d1, e1, a1, b1, w[13], 8)
    c2, e2 = r22(c2, d2, e2, a2, b2, w[3], 15)
    b1, d1 = r21(b1, c1, d1, e1, a1, w[1], 13)
    b2, d2 = r22(b2, c2, d2, e2, a2, w[7], 7)
    a1, c1 = r21(a1, b1, c1, d1, e1, w[10], 11)
    a2, c2 = r22(a2, b2, c2, d2, e2, w[0], 12)
    e1, b1 = r21(e1, a1, b1, c1, d1, w[6], 9)
    e2, b2 = r22(e2, a2, b2, c2, d2, w[13], 8)
    d1, a1 = r21(d1, e1, a1, b1, c1, w[15], 7)
    d2, a2 = r22(d2, e2, a2, b2, c2, w[5], 9)
    c1, e1 = r21(c1, d1, e1, a1, b1, w[3], 15)
    c2, e2 = r22(c2, d2, e2, a2, b2, w[10], 11)
    b1, d1 = r21(b1, c1, d1, e1, a1, w[12], 7)
    b2, d2 = r22(b2, c2, d2, e2, a2, w[14], 7)
    a1, c1 = r21(a1, b1, c1, d1, e1, w[0], 12)
    a2, c2 = r22(a2, b2, c2, d2, e2, w[15], 7)
    e1, b1 = r21(e1, a1, b1, c1, d1, w[9], 15)
    e2, b2 = r22(e2, a2, b2, c2, d2, w[8], 12)
    d1, a1 = r21(d1, e1, a1, b1, c1, w[5], 9)
    d2, a2 = r22(d2, e2, a2, b2, c2, w[12], 7)
    c1, e1 = r21(c1, d1, e1, a1, b1, w[2], 11)
    c2, e2 = r22(c2, d2, e2, a2, b2, w[4], 6)
    b1, d1 = r21(b1, c1, d1, e1, a1, w[14], 7)
    b2, d2 = r22(b2, c2, d2, e2, a2, w[9], 15)
    a1, c1 = r21(a1, b1, c1, d1, e1, w[11], 13)
    a2, c2 = r22(a2, b2, c2, d2, e2, w[1], 13)
    e1, b1 = r21(e1, a1, b1, c1, d1, w[8], 12)
    e2, b2 = r22(e2, a2, b2, c2, d2, w[2], 11)

    d1, a1 = r31(d1, e1, a1, b1, c1, w[3], 11)
    d2, a2 = r32(d2, e2, a2, b2, c2, w[15], 9)
    c1, e1 = r31(c1, d1, e1, a1, b1, w[10], 13)
    c2, e2 = r32(c2, d2, e2, a2, b2, w[5], 7)
    b1, d1 = r31(b1, c1, d1, e1, a1, w[14], 6)
    b2, d2 = r32(b2, c2, d2, e2, a2, w[1], 15)
    a1, c1 = r31(a1, b1, c1, d1, e1, w[4], 7)
    a2, c2 = r32(a2, b2, c2, d2, e2, w[3], 11)
    e1, b1 = r31(e1, a1, b1, c1, d1, w[9], 14)
    e2, b2 = r32(e2, a2, b2, c2, d2, w[7], 8)
    d1, a1 = r31(d1, e1, a1, b1, c1, w[15], 9)
    d2, a2 = r32(d2, e2, a2, b2, c2, w[14], 6)
    c1, e1 = r31(c1, d1, e1, a1, b1, w[8], 13)
    c2, e2 = r32(c2, d2, e2, a2, b2, w[6], 6)
    b1, d1 = r31(b1, c1, d1, e1, a1, w[1], 15)
    b2, d2 = r32(b2, c2, d2, e2, a2, w[9], 14)
    a1, c1 = r31(a1, b1, c1, d1, e1, w[2], 14)
    a2, c2 = r32(a2, b2, c2, d2, e2, w[11], 12)
    e1, b1 = r31(e1, a1, b1, c1, d1, w[7], 8)
    e2, b2 = r32(e2, a2, b2, c2, d2, w[8], 13)
    d1, a1 = r31(d1, e1, a1, b1, c1, w[0], 13)
    d2, a2 = r32(d2, e2, a2, b2, c2, w[12], 5)
    c1, e1 = r31(c1, d1, e1, a1, b1, w[6], 6)
    c2, e2 = r32(c2, d2, e2, a2, b2, w[2], 14)
    b1, d1 = r31(b1, c1, d1, e1, a1, w[13], 5)
    b2, d2 = r32(b2, c2, d2, e2, a2, w[10], 13)
    a1, c1 = r31(a1, b1, c1, d1, e1, w[11], 12)
    a2, c2 = r32(a2, b2, c2, d2, e2, w[0], 13)
    e1, b1 = r31(e1, a1, b1, c1, d1, w[5], 7)
    e2, b2 = r32(e2, a2, b2, c2, d2, w[4], 7)
    d1, a1 = r31(d1, e1, a1, b1, c1, w[12], 5)
    d2, a2 = r32(d2, e2, a2, b2, c2, w[13], 5)

    c1, e1 = r41(c1, d1, e1, a1, b1, w[1], 11)
    c2, e2 = r42(c2, d2, e2, a2, b2, w[8], 15)
    b1, d1 = r41(b1, c1, d1, e1, a1, w[9], 12)
    b2, d2 = r42(b2, c2, d2, e2, a2, w[6], 5)
    a1, c1 = r41(a1, b1, c1, d1, e1, w[11], 14)
    a2, c2 = r42(a2, b2, c2, d2, e2, w[4], 8)
    e1, b1 = r41(e1, a1, b1, c1, d1, w[10], 15)
    e2, b2 = r42(e2, a2, b2, c2, d2, w[1], 11)
    d1, a1 = r41(d1, e1, a1, b1, c1, w[0], 14)
    d2, a2 = r42(d2, e2, a2, b2, c2, w[3], 14)
    c1, e1 = r41(c1, d1, e1, a1, b1, w[8], 15)
    c2, e2 = r42(c2, d2, e2, a2, b2, w[11], 14)
    b1, d1 = r41(b1, c1, d1, e1, a1, w[12], 9)
    b2, d2 = r42(b2, c2, d2, e2, a2, w[15], 6)
    a1, c1 = r41(a1, b1, c1, d1, e1, w[4], 8)
    a2, c2 = r42(a2, b2, c2, d2, e2, w[0], 14)
    e1, b1 = r41(e1, a1, b1, c1, d1, w[13], 9)
    e2, b2 = r42(e2, a2, b2, c2, d2, w[5], 6)
    d1, a1 = r41(d1, e1, a1, b1, c1, w[3], 14)
    d2, a2 = r42(d2, e2, a2, b2, c2, w[12], 9)
    c1, e1 = r41(c1, d1, e1, a1, b1, w[7], 5)
    c2, e2 = r42(c2, d2, e2, a2, b2, w[2], 12)
    b1, d1 = r41(b1, c1, d1, e1, a1, w[15], 6)
    b2, d2 = r42(b2, c2, d2, e2, a2, w[13], 9)
    a1, c1 = r41(a1, b1, c1, d1, e1, w[14], 8)
    a2, c2 = r42(a2, b2, c2, d2, e2, w[9], 12)
    e1, b1 = r41(e1, a1, b1, c1, d1, w[5], 6)
    e2, b2 = r42(e2, a2, b2, c2, d2, w[7], 5)
    d1, a1 = r41(d1, e1, a1, b1, c1, w[6], 5)
    d2, a2 = r42(d2, e2, a2, b2, c2, w[10], 15)
    c1, e1 = r41(c1, d1, e1, a1, b1, w[2], 12)
    c2, e2 = r42(c2, d2, e2, a2, b2, w[14], 8)

    b1, d1 = r51(b1, c1, d1, e1, a1, w[4], 9)
    b2, d2 = r52(b2, c2, d2, e2, a2, w[12], 8)
    a1, c1 = r51(a1, b1, c1, d1, e1, w[0], 15)
    a2, c2 = r52(a2, b2, c2, d2, e2, w[15], 5)
    e1, b1 = r51(e1, a1, b1, c1, d1, w[5], 5)
    e2, b2 = r52(e2, a2, b2, c2, d2, w[10], 12)
    d1, a1 = r51(d1, e1, a1, b1, c1, w[9], 11)
    d2, a2 = r52(d2, e2, a2, b2, c2, w[4], 9)
    c1, e1 = r51(c1, d1, e1, a1, b1, w[7], 6)
    c2, e2 = r52(c2, d2, e2, a2, b2, w[1], 12)
    b1, d1 = r51(b1, c1, d1, e1, a1, w[12], 8)
    b2, d2 = r52(b2, c2, d2, e2, a2, w[5], 5)
    a1, c1 = r51(a1, b1, c1, d1, e1, w[2], 13)
    a2, c2 = r52(a2, b2, c2, d2, e2, w[8], 14)
    e1, b1 = r51(e1, a1, b1, c1, d1, w[10], 12)
    e2, b2 = r52(e2, a2, b2, c2, d2, w[7], 6)
    d1, a1 = r51(d1, e1, a1, b1, c1, w[14], 5)
    d2, a2 = r52(d2, e2, a2, b2, c2, w[6], 8)
    c1, e1 = r51(c1, d1, e1, a1, b1, w[1], 12)
    c2, e2 = r52(c2, d2, e2, a2, b2, w[2], 13)
    b1, d1 = r51(b1, c1, d1, e1, a1, w[3], 13)
    b2, d2 = r52(b2, c2, d2, e2, a2, w[13], 6)
    a1, c1 = r51(a1, b1, c1, d1, e1, w[8], 14)
    a2, c2 = r52(a2, b2, c2, d2, e2, w[14], 5)
    e1, b1 = r51(e1, a1, b1, c1, d1, w[11], 11)
    e2, b2 = r52(e2, a2, b2, c2, d2, w[0], 15)
    d1, a1 = r51(d1, e1, a1, b1, c1, w[6], 8)
    d2, a2 = r52(d2, e2, a2, b2, c2, w[3], 13)
    c1, e1 = r51(c1, d1, e1, a1, b1, w[15], 5)
    c2, e2 = r52(c2, d2, e2, a2, b2, w[9], 11)
    b1, d1 = r51(b1, c1, d1, e1, a1, w[13], 6)
    b2, d2 = r52(b2, c2, d2, e2, a2, w[11], 11)

    t = s[0]
    s[0] = (s[1] + c1 + d2) & 0xffffffff
    s[1] = (s[2] + d1 + e2) & 0xffffffff
    s[2] = (s[3] + e1 + a2) & 0xffffffff
    s[3] = (s[4] + a1 + b2) & 0xffffffff
    s[4] = (t + b1 + c2) & 0xffffffff
    return s


def ripemd160(msg):
    """Return the 20-byte RIPEMD-160 digest of msg (bytes)."""
    if not isinstance(msg, (bytes, bytearray)):
        raise TypeError("msg must be bytes")
    s = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    msg = bytes(msg)
    length = len(msg)
    for off in range(0, length - (length % 64), 64):
        s = _transform(s, msg[off:off + 64])
    pad = bytearray(msg[length - (length % 64):])
    pad.append(0x80)
    pad.extend(b"\x00" * ((119 - (length % 64)) % 64))
    pad.extend((length << 3).to_bytes(8, "little"))
    for off in range(0, len(pad), 64):
        s = _transform(s, pad[off:off + 64])
    return b"".join(v.to_bytes(4, "little") for v in s)
