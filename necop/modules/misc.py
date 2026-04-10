"""Miscellaneous methods"""

def dictarr_to_table(map: list):
    """Converts a array of dictionaries to a 2D array"""
    table = []

    for line in map:
        arr = []
        for value in line.values():
            arr.append(value)

        table.append(arr)
        
    return table
