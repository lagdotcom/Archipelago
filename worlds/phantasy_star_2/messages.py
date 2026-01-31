game_tokens = {
    " ": 0x00,
    "0": 0x01,
    "1": 0x02,
    "2": 0x03,
    "3": 0x04,
    "4": 0x05,
    "5": 0x06,
    "6": 0x07,
    "7": 0x08,
    "8": 0x09,
    "9": 0x0A,
    "A": 0x0B,
    "B": 0x0C,
    "C": 0x0D,
    "D": 0x0E,
    "E": 0x0F,
    "F": 0x10,
    "G": 0x11,
    "H": 0x12,
    "I": 0x13,
    "J": 0x14,
    "K": 0x15,
    "L": 0x16,
    "M": 0x17,
    "N": 0x18,
    "O": 0x19,
    "P": 0x1A,
    "Q": 0x1B,
    "R": 0x1C,
    "S": 0x1D,
    "T": 0x1E,
    "U": 0x1F,
    "V": 0x20,
    "W": 0x21,
    "X": 0x22,
    "Y": 0x23,
    "Z": 0x24,
    "a": 0x25,
    "b": 0x26,
    "c": 0x27,
    "d": 0x28,
    "e": 0x29,
    "f": 0x2A,
    "g": 0x2B,
    "h": 0x2C,
    "i": 0x2D,
    "j": 0x2E,
    "k": 0x2F,
    "l": 0x30,
    "m": 0x31,
    "n": 0x32,
    "o": 0x33,
    "p": 0x34,
    "q": 0x35,
    "r": 0x36,
    "s": 0x37,
    "t": 0x38,
    "u": 0x39,
    "v": 0x3A,
    "w": 0x3B,
    "x": 0x3C,
    "y": 0x3D,
    "z": 0x3E,
    ",": 0x3F,
    ".": 0x40,
    ";": 0x41,
    '"': 0x42,
    "?": 0x43,
    "!": 0x44,
    "'": 0x45,
    "-": 0x46,
    "·": 0x47,
    "/": 0x48,
    "⯆": 0x49,
    ":": 0x77,
    "@CH1": 0xBB,
    "@CH2": 0xBC,
    "@ENEMY": 0xBD,
    "@TECH": 0xBE,
    "@ITEM": 0xBF,
    "@VALUE": 0xC0,
    "<NL>": 0xC1,
    "<CLR>": 0xC2,
    "<WAIT>": 0xC3,
    "<END>": 0xC4,
    "<WIN>": 0xC5,
    "<END2>": 0xC6,
    "<END3>": 0xC7,
}

window_tokens = {
    " ": 0x26,
    "A": 0x27,
    "B": 0x28,
    "C": 0x29,
    "D": 0x2A,
    "E": 0x2B,
    "F": 0x2C,
    "G": 0x2D,
    "H": 0x2E,
    "I": 0x2F,
    "J": 0x30,
    "K": 0x31,
    "L": 0x32,
    "M": 0x33,
    "N": 0x34,
    "O": 0x35,
    "P": 0x36,
    "Q": 0x37,
    "R": 0x38,
    "S": 0x39,
    "T": 0x3A,
    "U": 0x3B,
    "V": 0x3C,
    "W": 0x3D,
    "X": 0x3E,
    "Y": 0x3F,
    "Z": 0x40,
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
    ",": 0x5B,
    ".": 0x5C,
    ";": 0x5D,
    '"': 0x5E,
    "?": 0x5F,
    "!": 0x60,
    "'": 0x61,
    "-": 0x62,
    "·": 0x63,
    "/": 0x64,
    "⯆": 0x65,
    "0": 0x76,
    "1": 0x77,
    "2": 0x78,
    "3": 0x79,
    "4": 0x7A,
    "5": 0x7B,
    "6": 0x7C,
    "7": 0x7D,
    "8": 0x7E,
    "9": 0x7F,
    "▀": 0xB9,
    "▄": 0xBE,
}


miscellaneous_messages = [
    "Oh no! This satellite is<NL>headed straight for<NL>Palm! There's no time!<NL>What should I do???<WIN>",
    "It was that same dream<NL>again.<WIN>",
    "<CLR>Help!!!<END3>",
    "<CLR>.....?!<END3>",
    "<CLR>Did I disturb you?<NL>I'm Tyler,a space<NL>pirate. I left Palm<NL>long ago; life under the<WAIT>Mother Brain was not to<NL>my liking. You were<NL>being held by Gaila,<NL>right? It's good for<WAIT>",
    "you that I happened to<NL>be close by. Your<NL>friends are also being<NL>revived right now; they<WAIT>should awake any moment.<END>",
    "It was terrible...this<NL>is all that is left of<NL>Palm.<END>",
    "One planet was<NL>destroyed. Who knows<NL>what happened to Algo,<NL>I don't know what to<WAIT>say.<NL>According to the news,<NL>you and your friends are<NL>criminals charged with<WAIT>destroying the Mother<NL>Brain. But I don't<WAIT>",
    "believe you could have<NL>done that, could you?<NL>Anyway, I'll take you<NL>to Paseo. I've already<WAIT>got your belongings<NL>loaded.<NL>Ah, I remember now! You<NL>were heading for<WAIT>",
    "Dezo. I have heard<NL>that there is someone<NL>there who can do things<NL>the Mother Brain can't.<WAIT>But he might be of a<NL>criminal nature! You<NL>never can tell! Well,<NL>until we meet again!<END>",
    "You finally made it.<NL>I'm Lutz, the last<NL>telemental on Algo.<NL>You seem surprised that<WAIT>I know your name. Don't<NL>you remember? This is<NL>the second time we have<NL>met. I saved you from<WAIT>death after an accident<NL>on a spacetrip with your<NL>",
    "parents when you were<NL>10.<WAIT>What woke me was Alis'<NL>scream. So you are the<NL>last descendant of Alis<NL>who fought to protect<WAIT>Algo. Beautiful Alis,<NL>",
    "the symbol of Algo, was<NL>fighting the dark force<NL>in that dream. The dark<WAIT>force was trying to<NL>destroy Algo, but in<NL>the end was itself<NL>destroyed.<END>",
    "But that doesn't mean<NL>that there is no longer<NL>anyone trying to destroy<NL>Algo. You,@CH1, must<WAIT>arm yourself for battle.<NL>One valuable item is the<NL>aeroprism--it will let<NL>you see that which<WAIT>",
    "cannot be seen. Also<NL>arm yourself with Nei's<NL>weapons. Prepare<NL>yourself, and then I<WAIT>will tell you about the<NL>enemy's plans.<END>",
    "Ha,ha,ha,ha,ha!<NL>This is Pandora's box!<NL>It contains all that is<NL>evil, all that you call<WAIT>the dark force! This is<NL>a present from our world<NL>to all of you! Take it!<END3>",
    "@CH1, are you brave<NL>enough to do battle with<NL>the powers of evil?<WIN>",
    "In that case, I'll send<NL>you on your way with my<NL>prayers.<NL>Oh, god of Algo, bless<WAIT>this party with courage<NL>and strength.<END>",
    "Remove the Nei-sword<NL>from this box.<END>",
]


def translate_message(msg: str, translation_table: dict[str, int] = game_tokens):
    tokens: list[int] = []
    accumulator = ""
    for ch in msg:
        accumulator += ch
        if accumulator in translation_table:
            tokens.append(translation_table[accumulator])
            accumulator = ""
    if accumulator:
        raise Exception(f"could not encode, remaining: {accumulator}")
    return bytes(tokens)


def translate_block(block: list[str], translation_table: dict[str, int] = game_tokens):
    sizes = [len(block)]
    body = b""
    for message in block[:-1]:
        encoded = translate_message(message, translation_table)
        if len(encoded) > 0x255:
            raise Exception("message too long")
        sizes.append(len(encoded))
        body += encoded
    body += translate_message(block[-1], translation_table)
    return bytes(sizes) + body


# def dump_hex(start: int, data: bytes):
#     print("------ x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 xa xb xc xd xe xf", end=" ")
#     i = start
#     offset = i % 16
#     if offset != 0:
#         print("\n%06x " % (i - offset) + "   " * offset, end="")
#     for b in data:
#         if i % 16 == 0:
#             print("\n%06x" % i, end=" ")
#         i += 1
#         print("%02x" % b, end=" ")
#     print()
