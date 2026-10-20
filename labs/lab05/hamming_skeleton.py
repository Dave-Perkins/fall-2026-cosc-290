"""
Hamming single-error correction using XOR specifically for 11 bit messages.

Our array (called a "block") has 16 bits, numbered 0 to 15 in binary.
  - Positions 1, 2, 4 and 8 (the powers of two) hold the four parity bits.
  - Position 0 holds one more parity bit covering the whole block.
  - The other 11 positions hold the message, in order.

The trick: XOR together the positions of every 1 bit in the block.  The
parity bits are chosen so that this comes out to 0.  If one bit is flipped,
the XOR comes out to the position of the flipped bit.  If that is 0, the
flipped bit was position 0 itself, which the overall parity bit reveals.

Usage:
    python3 hamming.py encode 10110011010        (11 message bits -> 16-bit block)
    python3 hamming.py decode 0110100110110010   (16-bit block -> fix error, recover message)

Fill in the four functions marked TODO.  main() is finished.
"""

import sys

# In preparation for extending this code to handle messages of other lengths:
BLOCK_SIZE = 16
PARITY_POSITIONS = [1, 2, 4, 8]
DATA_POSITIONS = [i for i in range(1, BLOCK_SIZE) if i not in PARITY_POSITIONS]
MESSAGE_SIZE = len(DATA_POSITIONS)   

def syndrome(block):
    """ XOR together the positions of all the 1 bits.  0 means no error. """
    pass

def overall_parity(block):
    """ XOR of every bit in the block: 0 if there is an even number of 1s. """
    pass

def encode(message):
    """ Build a 16-bit block from an 11-bit message. """
    block = [0] * BLOCK_SIZE
    pass

def decode(block):
    """
    Fix at most one flipped bit, then return (corrected block, message,
    position of the flipped bit or None).
    """
    block = list(block)   # work on a copy
    pass

# ---------------------------------------------------------------------------
# Command-line interface (no need to edit below this line)
# ---------------------------------------------------------------------------

def bits_from_string(s, expected_length):
    if len(s) != expected_length or any(c not in "01" for c in s):
        print(f"error: expected {expected_length} bits of 0 and 1, got {s!r}")
        sys.exit(1)
    return [int(c) for c in s]

def bits_to_string(bits):
    return "".join(str(b) for b in bits)

def show_grid(block, mark=None):
    """Print the block as a 4 x 4 grid, positions 0-3 on the first row."""
    for row in range(4):
        cells = []
        for col in range(4):
            position = 4 * row + col
            cell = str(block[position])
            if position == mark:
                cell = "[" + cell + "]"
            else:
                cell = " " + cell + " "
            cells.append(cell)
        print("   " + "".join(cells))

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("encode", "decode"):
        print("usage: python3 hamming.py encode <11 bits>")
        print("       python3 hamming.py decode <16 bits>")
        sys.exit(1)
    command, bit_string = sys.argv[1], sys.argv[2]

    if command == "encode":
        message = bits_from_string(bit_string, MESSAGE_SIZE)
        block = encode(message)
        print("message:", bits_to_string(message))
        print("block:  ", bits_to_string(block))
        show_grid(block)
    else:
        received = bits_from_string(bit_string, BLOCK_SIZE)
        block, message, flipped = decode(received)
        print("received: ", bits_to_string(received))
        if flipped is None:
            print("no error detected")
        else:
            print(f"error at position {flipped}, flipped it back")
        print("corrected:", bits_to_string(block))
        show_grid(block, mark=flipped)
        print("message:  ", bits_to_string(message))

main()
