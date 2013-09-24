import struct

stentry = struct.Struct('!IIxxxx') # offset, length, 4 byte for extension
sthead = struct.Struct('!IIIq') # version, size, flags
