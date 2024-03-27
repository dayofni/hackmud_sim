
import re

from json   import loads
from re     import findall, finditer, sub
from random import choice

from hackmud_sim.colour.data import CLEAR, COLOUR_MODE, HACKMUD_PALETTE

def parse_hackmud_codes(text: str, mode=COLOUR_MODE, clear=CLEAR) -> str:
    
    """
    Parses a hackmud-formatted string using colour format `$text`.
    
    Returns a string with ANSI colours in mode `mode`. If not set, uses default in `settings.json`.
    """
    
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
            colour = HACKMUD_PALETTE[text[c+1]]
            out += colour.get_escape_code(mode=mode)
            continue
        
        out += character
    
    return out

def parse_script_names(text: str, mode=COLOUR_MODE, clear=CLEAR) -> str:
    
    COLOUR_SCRIPT = HACKMUD_PALETTE["2"].get_escape_code(mode=mode)
    COLOUR_AUTHOR = HACKMUD_PALETTE["C"].get_escape_code(mode=mode)
    COLOUR_TRUST  = HACKMUD_PALETTE["5"].get_escape_code(mode=mode)
    
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

def parse_gc(text: str, mode=COLOUR_MODE, clear=CLEAR) -> str:
    
    # Find GC strings (9Q 7T 199B 254M 740K 991) GC
    
    COLOUR_NUM = HACKMUD_PALETTE["B"].get_escape_code(mode=mode)
    COLOUR_GC_DENOM = {
        "K": HACKMUD_PALETTE["N"].get_escape_code(mode=mode),
        "M": HACKMUD_PALETTE["L"].get_escape_code(mode=mode),
        "B": HACKMUD_PALETTE["J"].get_escape_code(mode=mode),
        "T": HACKMUD_PALETTE["T"].get_escape_code(mode=mode),
        "Q": HACKMUD_PALETTE["D"].get_escape_code(mode=mode)
    }
    COLOUR_GC  = HACKMUD_PALETTE["C"].get_escape_code(mode=mode)
    
    
    gc_strs = findall(r"(?:\d+[QTBMK])*\d*GC\b", text)
    
    for gc_str in gc_strs.copy():
        
        new = COLOUR_NUM + gc_str
        
        for denom, colour in COLOUR_GC_DENOM.items():
            new = new.replace(denom, colour + denom + COLOUR_NUM)
        
        new = new.replace("GC", COLOUR_GC + "GC" + clear)

        text = text.replace(gc_str, new)
    
    return text

def parse_sector(text: str, mode=COLOUR_MODE, clear=CLEAR):
    
    GREEK_LETTERS = "ALPHA|BETA|GAMMA|DELTA|EPSILON|ZETA|ETA|THETA|IOTA|KAPPA|LAMBDA|MU|NU|XI|OMICRON|PI|RHO|SIGMA|TAU|UPSILON|PHI|CHI|PSI|OMEGA"
    BLANK = HACKMUD_PALETTE["C"].get_escape_code(mode=mode)
    
    AXIOMS = {
        "DATA":   HACKMUD_PALETTE["q"].get_escape_code(mode=mode),
        "KIN":    HACKMUD_PALETTE["M"].get_escape_code(mode=mode),
        "FORM":   HACKMUD_PALETTE["l"].get_escape_code(mode=mode),
        "VOID":   HACKMUD_PALETTE["H"].get_escape_code(mode=mode),
        "CHAOS":  HACKMUD_PALETTE["D"].get_escape_code(mode=mode),
        "CHOICE": HACKMUD_PALETTE["5"].get_escape_code(mode=mode),
        "LAW":    HACKMUD_PALETTE["q"].get_escape_code(mode=mode),
        "WILD":   HACKMUD_PALETTE["Y"].get_escape_code(mode=mode)
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

def parse_args(text: str, mode=COLOUR_MODE, clear=CLEAR):
    
    # Stolen outright from dtr (like most things) and her hackmud-render project. (https://github.com/hackmud-dtr/hackmud-render)
    
    ARCANE_MAGIC = re.compile(r'((?:(?:"(?:[^"\n]|\.)+")|(?:[a-zA-z_]\w*))[\t ]{0,2}):([\t ]{0,2}(?:(?:true)|(?:false)|(?:null)|(?:"(?:[^"\n]|\.)*")|(?:-?\d+\.?\d*)|\{|\[|#s\.[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*))')
    
    COLOUR_KEY = HACKMUD_PALETTE["N"].get_escape_code(mode=mode)
    COLOUR_VAL = HACKMUD_PALETTE["V"].get_escape_code(mode=mode)
    
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

def parse_misc(text: str, mode=COLOUR_MODE, clear=CLEAR, user_colours={}):
    
    # usernames and :::TRUST COMMUNICATION:::
    # dates
    # @([a-z_][a-z0-9_]*)
    # :::TRUST COMMUNICATION:::
    
    COLOUR_TRUST = HACKMUD_PALETTE["D"].get_escape_code(mode=mode)
    COLOUR_YEAR  = HACKMUD_PALETTE["A"].get_escape_code(mode=mode)
    COLOUR_AD    = HACKMUD_PALETTE["B"].get_escape_code(mode=mode)
    COLOUR_DAY   = HACKMUD_PALETTE["L"].get_escape_code(mode=mode)
    COLOUR_D     = HACKMUD_PALETTE["C"].get_escape_code(mode=mode)
    
    text = text.replace(":::TRUST COMMUNICATION:::", COLOUR_TRUST + ":::TRUST COMMUNICATION:::" + clear)
    
    users = list(set(findall(r"@([a-z_][a-z0-9_]*)", text)))
    
    for user in users:
        
        if user not in user_colours:
            colour = HACKMUD_PALETTE[choice("JKMWLB")].get_escape_code(mode=mode)
        else:
            colour = user_colours[colour]
        
        text = text.replace(f"@{user}", f"{COLOUR_D}@{colour}{user}{clear}")
    
    text = sub(r"([0-9]{1,4})AD D([0-9]{1,3})", rf"{COLOUR_YEAR}\1{COLOUR_AD}AD {COLOUR_D}D{COLOUR_DAY}\2{clear}", text)
    
    return text
    
def parse_hackmud_string(text: str, mode=COLOUR_MODE) -> str:
    
    # Need to include:
    # -> scripts
    # -> colour codes
    # -> GC strings
    # -> :::TRUST COMMUNICATION:::
    # -> @user
    # -> args
    
    clear = HACKMUD_PALETTE["S"].get_escape_code(mode=mode)
    
    funcs = [
        parse_args, 
        parse_script_names,
        parse_hackmud_codes,
        parse_sector,
        parse_gc,
        parse_misc
    ]
    
    for parser in funcs:
        text = parser(text, mode=mode, clear=clear)
    
    return clear + text + CLEAR
