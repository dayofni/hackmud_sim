from re   import findall, compile, finditer, sub
from math import sqrt
from json import loads

from random import choice

from os.path import join, dirname, realpath

CLEAR   = "\x1b[0m"
CORRUPT = "¡¢Á¤Ã¦§¨©ª"

#? Hex code and RGB conversion

def hex_to_rgb(hexcode: str) -> tuple[int, int, int]:
    
    """
    Get RGB values from hex colour code.
    
    Works with/without #. Ignores alpha.
    """
    
    if hexcode[0] == "#":
        hexcode = hexcode[1:]
    
    colours = [hexcode[:2], hexcode[2:4], hexcode[4:6]]    # Seperates out #RRGGBB to ["RR", "GG", "BB"]
    colours = [int(colour, base=16) for colour in colours] # Turns hexes to integers
    
    return tuple(colours)

def rgb_to_hex(rgb_values: tuple[int, int, int], add_hash=True) -> str:
    
    """
    Generate hex colour code from RGB colour code.
    """
    
    out = "#" if add_hash else ""
    
    for channel in rgb_values:
        str_hex = hex(channel)[2:]
        
        out += "0" * (2-len(str_hex)) + str_hex
        
    
    return out

#? Escape code handling

def get_escape_code(rgb: tuple[int, int, int], mode=None) -> str:
    
    red, green, blue = rgb
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    if mode == "truecolor":
        return f"\x1b[38;2;{red};{green};{blue}m" # Really easy conversion!
    
    elif mode == "256-colour":
        
        # Code borrowed from StackOverflow answer https://stackoverflow.com/a/26665998.
        # Adapted from JavaScript to Python.
        
        if (red == green and green == blue): # greyscale
            
            if red < 8:
                colour = 16 # Handling edgecases
            
            elif red > 248:
                colour = 231; # See above
                
            else:
                colour = round(((red - 8) / 247) * 24) + 232
        else:
            colour = 16 \
                + (36 * round(red / 255 * 5)) \
                + (6 * round(green / 255 * 5))  \
                + round(blue / 255 * 5);

        return f"\x1b[38;5;{colour}m" # Really easy conversion!

#? hackmud formatting

def parse_hackmud_codes(text: str, mode=None, clear=CLEAR) -> str:
    
    """
    Parses a hackmud-formatted string using colour format `$text`.
    
    Returns a string with ANSI colours in mode `mode`. If not set, uses default in `settings.json`.
    """
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    out = ""
    skip = False
    in_search = False
    
    for c, character in enumerate(text):
        
        if skip:
            skip = False
            continue
        
        if character == "`" and in_search:
            in_search = False
            out += clear
            continue
        
        elif character == "`" and c + 1 < len(text) and text[c+1].isalnum():
            skip = True
            in_search = True
            colour = SETTINGS["colours"][text[c+1]]
            out += get_escape_code(colour, mode=mode)
            continue
        
        out += character
    
    return out

def parse_script_names(text: str, mode=None, clear=CLEAR) -> str:
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    COLOUR_SCRIPT = get_escape_code(SETTINGS["colours"]["2"])
    COLOUR_AUTHOR = get_escape_code(SETTINGS["colours"]["C"])
    COLOUR_TRUST  = get_escape_code(SETTINGS["colours"]["5"])
    
    TRUST_USERS = [
        "accts",
        "autos",
        "binmat",
        "chats",
        "corps",
        "escrow",
        "gui",
        "kernel",
        "market",
        "risk",
        "scripts",
        "sys",
        "trust",
        "users"
    ]
    
    search = set(findall(r"\w+\.\w+", text))
    
    for scriptname in search:
        user, script = scriptname.split(".")
        
        if user in TRUST_USERS:
            author_code = COLOUR_TRUST
        else:
            author_code = COLOUR_AUTHOR
        
        new = f"{author_code}{user}{clear}.{COLOUR_SCRIPT}{script}{clear}"
        
        text = text.replace(scriptname, new)
    
    return text

def parse_gc(text: str, mode=None, clear=CLEAR) -> str:
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    # Find GC strings (9Q 7T 199B 254M 740K 991) GC
    
    COLOUR_NUM = get_escape_code(SETTINGS["colours"]["B"], mode=mode)
    COLOUR_GC  = get_escape_code(SETTINGS["colours"]["C"], mode=mode)
    COLOUR_K   = get_escape_code(SETTINGS["colours"]["N"], mode=mode)
    COLOUR_M   = get_escape_code(SETTINGS["colours"]["L"], mode=mode)
    COLOUR_B   = get_escape_code(SETTINGS["colours"]["J"], mode=mode)
    COLOUR_T   = get_escape_code(SETTINGS["colours"]["T"], mode=mode)
    COLOUR_Q   = get_escape_code(SETTINGS["colours"]["D"], mode=mode)
    
    gc_strs = findall(r"(?:\d+[QTBMK])*\d*GC\b", text)
    
    for gc_str in gc_strs.copy():
        
        new = COLOUR_NUM + gc_str \
            .replace("Q", COLOUR_Q + "Q" + COLOUR_NUM) \
            .replace("T", COLOUR_T + "T" + COLOUR_NUM) \
            .replace("B", COLOUR_B + "B" + COLOUR_NUM) \
            .replace("M", COLOUR_M + "M" + COLOUR_NUM) \
            .replace("K", COLOUR_K + "K" + COLOUR_NUM) \
            .replace("GC", COLOUR_GC + "GC" + clear)

        text = text.replace(gc_str, new)
    
    return text

def parse_sector(text: str, mode=None, clear=CLEAR):
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    GREEK_LETTERS = "ALPHA|BETA|GAMMA|DELTA|EPSILON|ZETA|ETA|THETA|IOTA|KAPPA|LAMBDA|MU|NU|XI|OMICRON|PI|RHO|SIGMA|TAU|UPSILON|PHI|CHI|PSI|OMEGA"
    BLANK = get_escape_code(SETTINGS["colours"]["C"], mode=mode)
    
    AXIOMS = {
        "DATA":   get_escape_code(SETTINGS["colours"]["q"], mode=mode),
        "KIN":    get_escape_code(SETTINGS["colours"]["M"], mode=mode),
        "FORM":   get_escape_code(SETTINGS["colours"]["l"], mode=mode),
        "VOID":   get_escape_code(SETTINGS["colours"]["H"], mode=mode),
        "CHAOS":  get_escape_code(SETTINGS["colours"]["D"], mode=mode),
        "CHOICE": get_escape_code(SETTINGS["colours"]["5"], mode=mode),
        "LAW":    get_escape_code(SETTINGS["colours"]["q"], mode=mode),
        "WILD":   get_escape_code(SETTINGS["colours"]["Y"], mode=mode)
    }
    
    sectors = findall(r"(?:%s)_(?:%s)_\d"%("|".join(AXIOMS.keys()), GREEK_LETTERS), text) + findall(r"(?:SPC|NGC|VNP|HJG|K)_\d{4}", text)
    
    for sector in sectors:
        
        colour = BLANK
        
        for axiom in AXIOMS:
            
            if axiom in sector:
                colour = AXIOMS[axiom]
                break
        
        text = text.replace(sector, colour + sector + clear)
    
    return text

def replace(old, start, end, new):
    return old[:start] + new + old[end:]

def parse_args(text: str, mode=None, clear=CLEAR):
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    # Stolen outright from dtr (like most things) and her hackmud-render project. (https://github.com/hackmud-dtr/hackmud-render)
    
    ARCANE_MAGIC = compile(r'((?:(?:"(?:[^"\n]|\.)+")|(?:[a-zA-z_]\w*))[\t ]{0,2}):([\t ]{0,2}(?:(?:true)|(?:false)|(?:null)|(?:"(?:[^"\n]|\.)*")|(?:-?\d+\.?\d*)|\{|\[|#s\.[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*))')
    
    COLOUR_KEY = get_escape_code(SETTINGS["colours"]["N"], mode=mode)
    COLOUR_VAL = get_escape_code(SETTINGS["colours"]["V"], mode=mode)
    
    incr = 0
    
    for match in finditer(ARCANE_MAGIC, text):
        
        span = match.span()
        
        # Step 1: replace text
        
        new_segment = match.group()
        groups      = match.groups()
        
        new_segment = new_segment.replace(groups[0], COLOUR_KEY + groups[0] + clear)
        new_segment = new_segment.replace(groups[1], COLOUR_VAL + groups[1] + clear)
        
        text = replace(text, span[0] + incr, span[1] + incr, new_segment)
        incr += len(new_segment) - (span[1] - span[0])
        
    return text

def parse_misc(text: str, mode=None, clear=CLEAR, user_colours={}):
    
    # usernames and :::TRUST COMMUNICATION:::
    # dates
    # @([a-z_][a-z0-9_]*)
    # :::TRUST COMMUNICATION:::
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    COLOUR_TRUST = get_escape_code(SETTINGS["colours"]["D"], mode=mode)
    COLOUR_YEAR  = get_escape_code(SETTINGS["colours"]["A"], mode=mode)
    COLOUR_AD    = get_escape_code(SETTINGS["colours"]["B"], mode=mode)
    COLOUR_DAY   = get_escape_code(SETTINGS["colours"]["L"], mode=mode)
    COLOUR_D     = get_escape_code(SETTINGS["colours"]["C"], mode=mode)
    
    text = text.replace(":::TRUST COMMUNICATION:::", COLOUR_TRUST + ":::TRUST COMMUNICATION:::" + clear)
    
    users = list(set(findall(r"@([a-z_][a-z0-9_]*)", text)))
    
    for user in users:
        
        if user not in user_colours:
            colour = get_escape_code(SETTINGS["colours"][choice("JKMWLB")], mode=mode)
        else:
            colour = user_colours[colour]
        
        text = text.replace(f"@{user}", f"{COLOUR_D}@{colour}{user}{clear}")
    
    text = sub(r"([0-9]{1,4})AD D([0-9]{1,3})", rf"{COLOUR_YEAR}\1{COLOUR_AD}AD {COLOUR_D}D{COLOUR_DAY}\2{clear}", text)
    
    return text
    
def parse_hackmud_string(text: str, mode=None) -> str:
    
    # Need to include:
    # -> scripts
    # -> colour codes
    # -> GC strings
    # -> :::TRUST COMMUNICATION:::
    # -> @user
    # -> args
    
    if not mode:
        mode = SETTINGS["colour_mode"]
    
    clear = get_escape_code(SETTINGS["colours"]["S"], mode=mode)
    
    text = parse_args(text, mode=mode, clear=clear)
    text = parse_script_names(text, mode=mode, clear=clear)
    text = parse_hackmud_codes(text, mode=mode, clear=clear)
    text = parse_sector(text, mode=mode, clear=clear)
    text = parse_gc(text, mode=mode, clear=clear)
    text = parse_misc(text, mode=mode, clear=clear)
    
    return clear + text + CLEAR

#? misc colour scripts

def colour_to_pallete(rgb: tuple[int, int, int], pallete: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    
    pallete_dists = {}
    
    for comp_colour in pallete:
        
        # Distance. It's better to be (+10, +10, +10) rather than (+30, 0, 0)
        
        dist = lambda cha_a, cha_b: abs(cha_a ** 2 - cha_b ** 2)
        
        distances = [dist(*channel) for channel in zip(rgb, comp_colour)]
        
        pallete_dists[comp_colour] = sum(distances)
    
    return min(pallete_dists, key=lambda a: pallete_dists[a])

# Load colours from file, determine colour mode!

with open(join(dirname(realpath(__file__)), "settings.json")) as f: # opens up settings!
    SETTINGS = loads(f.read())["colour"]
    
    # change all colours to RGB values
    
    for colour, hexcode in SETTINGS["colours"].items():
        SETTINGS["colours"][colour] = hex_to_rgb(hexcode)