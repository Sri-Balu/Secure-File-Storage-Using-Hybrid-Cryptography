from __future__ import absolute_import, unicode_literals
from steganography.steganography import Steganography

# hide text to image
path = "./nature.jpg"
output_path = "./output.jpg"
text = 'The quick brown fox jumps over the lazy dog.'

# convert the text to hexadecimal format
# hex_text = ' '.join([hex(ord(c))[2:].upper() for c in text]).strip()

Steganography.encode(path, output_path, text)

# read secret text from image
secret_text = Steganography.decode(output_path)

# convert the hexadecimal format back to text
# secret_text = ''.join(chr(int(secret_text[i:i+2], 16)) for i in range(0, len(secret_text), 2))

print(secret_text)

