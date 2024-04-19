
from hackmud_sim.colour.rgb  import Colour
from hackmud_sim.colour.data import HACKMUD_PALETTE, HARDLINE_PALETTE, CLEAR

print("| Colour code | Hex value | Hardline value | Closest |")
print("| ----------- | --------- | -------------- | ------- |")

for colour in HARDLINE_PALETTE:
    
    hm, hd = HACKMUD_PALETTE[colour], HARDLINE_PALETTE[colour]
    
    diff = hd.colour_to_pallete(list(HACKMUD_PALETTE.values()))
    
    print(f"| {colour}           | {hm.get_escape_code()}{hm.hex_code}{CLEAR}   | {hd.get_escape_code()}{hd.hex_code}{CLEAR}        | {diff.get_escape_code()}{list(HACKMUD_PALETTE.keys())[[i.hex_code for i in HACKMUD_PALETTE.values()].index(diff.hex_code)]}{CLEAR}       |")