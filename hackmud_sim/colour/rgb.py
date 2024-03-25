
from typing import Optional


class Colour:
    
    def __init__(self, rgb: Optional[tuple[int, int, int]] = None, hex_code: Optional[str] = None) -> None:
        
        assert rgb or hex_code, "Must include one of the two to init a Colour: rgb or a hex-code (#FF0770)."
        
        if rgb:
            
            self.rgb = rgb
            
            self.hsv      = self.rgb_to_hsv(rgb)
            self.hex_code = self.rgb_to_hex(rgb)
        
        elif hex_code:
            
            self.hex_code = hex_code
            
            self.rgb = self.hex_to_rgb(rgb)
            self.hsv = self.rgb_to_hsv(self.rgb)

    def rgb_to_hex(self, rgb: tuple[int, int, int], add_hash: bool = True) -> str:
    
        out = "#" if add_hash else ""

        for channel in rgb:
            str_hex = hex(channel)[2:]
            out += "0" * (2-len(str_hex)) + str_hex # padding

        return out
    
    def hex_to_rgb(self, hex_code: str) -> tuple[int, int, int]:
        
        if hex_code[0] == "#":
            hex_code = hex_code[1:]

        colours = [hex_code[:2], hex_code[2:4], hex_code[4:6]] # Seperates out #RRGGBB to ["RR", "GG", "BB"]
        colours = [int(colour, base=16) for colour in colours] # Turns hexes to integers

        return tuple(colours)

    def colour_to_pallete(self, pallete: list["Colour"]) -> "Colour":

        pallete_dists = {}

        for comp_colour in pallete:

            # Distance. It's better to be (+10, +10, +10) rather than (+30, 0, 0)

            dist = lambda cha_a, cha_b: abs(cha_a ** 2 - cha_b ** 2)

            distances = [dist(*channel) for channel in zip(self.rgb, comp_colour.rgb)]

            pallete_dists[comp_colour] = sum(distances)

        return Colour(rgb=min(pallete_dists, key=lambda a: pallete_dists[a]))
    
    def get_escape_code(self, mode="truecolor") -> str:
    
        red, green, blue = self.rgb

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