import MCP23017


chips = {}
chips[1] = MCP23017(0x20, {'A': 17})#, 'B': 0x00})
chips[2] = MCP23017(0x21, {'A': 27})#, 'B': 0x00})

for chip in chips:
  for i in range(0x1B):
    byte = chip.read(i)
    print("0b{0:b}".format(byte))
