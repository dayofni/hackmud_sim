
from hackmud_sim.colour.rgb import Colour

COLOUR_MODE = "truecolor" # options: "truecolor", "256-colour"

CLEAR   = "\x1b[0m"    # Clear ANSI colour code

HACKMUD_PALETTE = {    # All hackmud colours and their respective codes
    "0": Colour(hex_code="#CACACA"),
    "1": Colour(hex_code="#FFFFFF"),
    "2": Colour(hex_code="#1EFF00"),
    "3": Colour(hex_code="#0070DD"),
    "4": Colour(hex_code="#B035EE"),
    "5": Colour(hex_code="#FF8000"),
    "6": Colour(hex_code="#FF8000"),
    "7": Colour(hex_code="#FF8000"),
    "8": Colour(hex_code="#FF8000"),
    "9": Colour(hex_code="#FF8000"),
    "a": Colour(hex_code="#000000"),
    "b": Colour(hex_code="#3F3F3F"),
    "c": Colour(hex_code="#676767"),
    "d": Colour(hex_code="#7D0000"),
    "e": Colour(hex_code="#8E3434"),
    "f": Colour(hex_code="#A34F00"),
    "g": Colour(hex_code="#725437"),
    "h": Colour(hex_code="#A88600"),
    "i": Colour(hex_code="#B2934A"),
    "j": Colour(hex_code="#939500"),
    "k": Colour(hex_code="#495225"),
    "l": Colour(hex_code="#299400"),
    "m": Colour(hex_code="#23381B"),
    "n": Colour(hex_code="#00535B"),
    "o": Colour(hex_code="#324A4C"),
    "p": Colour(hex_code="#0073A6"),
    "q": Colour(hex_code="#385A6C"),
    "r": Colour(hex_code="#010067"),
    "s": Colour(hex_code="#507AA1"),
    "t": Colour(hex_code="#601C81"),
    "u": Colour(hex_code="#43314C"),
    "v": Colour(hex_code="#8C0069"),
    "w": Colour(hex_code="#973984"),
    "x": Colour(hex_code="#880024"),
    "y": Colour(hex_code="#762E4A"),
    "z": Colour(hex_code="#101215"),
    "A": Colour(hex_code="#FFFFFF"),
    "B": Colour(hex_code="#CACACA"),
    "C": Colour(hex_code="#9B9B9B"),
    "D": Colour(hex_code="#FF0000"),
    "E": Colour(hex_code="#FF8383"),
    "F": Colour(hex_code="#FF8000"),
    "G": Colour(hex_code="#F3AA6F"),
    "H": Colour(hex_code="#FBC803"),
    "I": Colour(hex_code="#FFD863"),
    "J": Colour(hex_code="#FFF404"),
    "K": Colour(hex_code="#F3F998"),
    "L": Colour(hex_code="#1EFF00"),
    "M": Colour(hex_code="#B3FF9B"),
    "N": Colour(hex_code="#00FFFF"),
    "O": Colour(hex_code="#8FE6FF"),
    "P": Colour(hex_code="#0070DD"),
    "Q": Colour(hex_code="#A4E3FF"),
    "R": Colour(hex_code="#0000FF"),
    "S": Colour(hex_code="#7AB2F4"),
    "T": Colour(hex_code="#B035EE"),
    "U": Colour(hex_code="#E6C4FF"),
    "V": Colour(hex_code="#FF00EC"),
    "W": Colour(hex_code="#FF96E0"),
    "X": Colour(hex_code="#FF0070"),
    "Y": Colour(hex_code="#FF6A98"),
    "Z": Colour(hex_code="#0C112B")
}

TEST_STRING = """
`DR``HA``FI``LN``PB``TO``VW`

trust.script
user.script

9Q7T199B254M740K991GC

VOID_LAMBDA_2 KIN_THETA_7

scripts.get_level {name: "trust.sentience"}
dayofni.toybox    {script: "recon", args: {name: "trust.sentience"}}

:::TRUST COMMUNICATION::: 2024AD D100: sentience @dayofni is hereby an enemy of trust
"""