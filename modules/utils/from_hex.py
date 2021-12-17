def from_hex(hex : str) -> tuple:
    
    hex_code = hex.strip('#')
    
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))