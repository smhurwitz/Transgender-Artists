import string

def array_to_string(array):
    list = ""
    for a in array: list += a + ", "
    return list[0:-2]

""" Simplifies a string by removing excess spaces, removing punctuating, and making lowercase. Useful for comparing
    info between RYM and Spotify where small differences may occur. """
def string_simplify(s): return s.strip().translate(str.maketrans('', '', string.punctuation)).lower()

""" Simplifies an array of strings by removing excess spaces, removing punctuating, and making lowercase. Useful for comparing
    info between RYM and Spotify where small differences may occur. """
def strings_simplify(s):
    if s == None: return None
    simplified=[]
    for unsimp in s:
        simplified.append(string_simplify(unsimp))
    return simplified

""" Reads a list of URLS from a file into an array."""
def read_urls(filename):
    text_file = open(filename, "r")
    lines = text_file.read().split("\n")
    if '' in lines: lines.remove('')
    text_file.close()

    # allows for commenting
    newlines = []
    for line in lines:
        if not line[0] == "#": newlines.append(line.split("#")[0])
    return newlines