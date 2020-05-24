import re
from collections import OrderedDict

# Strings come with a length prefix, and look like 4:spam.
# Integers go between start and end markers, so 7 would encode to i7e.
# Lists and dictionaries work in a similar way: l4:spami7ee represents ['spam', 7], while d4:spami7ee means {spam: 7}.

def tokenize(text):
    i = 0
    match = re.compile(b"([idel])|(\d+):|(-?\d+)").match
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield b"s"
            yield text[i:i + int(s)]
            i = i + int(s)
        else:
            yield s


def decode_item(next, token):
    if token == b"i":
        data = int(next())
        if next() != b"e":
            raise ValueError
    elif token == b"d" or token == b"l":
        data = []
        el = next()
        while el != b"e":
            data.append(decode_item(next, el))
            el = next()
        if token == b"d":
            data = OrderedDict(zip(data[0::2], data[1::2]))
    elif token == b"s":
        data = next()
    else:
        raise ValueError
    return data


def decode(text):
    try:
        tokenized_text = tokenize(text)
        data = decode_item(tokenized_text.__next__, tokenized_text.__next__())
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("Invalid bencode")
    ordered_dict = OrderedDict(data)
    return ordered_dict

