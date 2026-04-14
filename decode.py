#   decode.py 6-10-24
#   Note this will not run in the code editor and must be downloaded

from PIL import Image

CHARS_IN_A_ROW = 8
MAX_CHARS_IN_MSG = 20

try:
  im = Image.open("output.png") 
except:  
  print("ERROR: could not find output.png. Check it exists in the directory with your python files")
  exit()

block_size = 0
upper_pixel_row = 0
left_pixel_col = 0
detected = False
rgb_im = im.convert('RGB')
for i in range(0, rgb_im.height):
  for j in range(0, rgb_im.width):
    r,g,b = rgb_im.getpixel((j,i))
    if r > 200 and g < 100 and b < 100: 
      if not detected:
        upper_pixel_row = i 
        left_pixel_col = j
      block_size += 1
      detected = True
    if detected and r > 200 and g > 200 and b > 200:
      break

msg_width = left_pixel_col + block_size * CHARS_IN_A_ROW
msg_height = upper_pixel_row + block_size * MAX_CHARS_IN_MSG
if (msg_height > rgb_im.height):
  msg_height =  rgb_im.height

my_array = []
for letters in range(0, CHARS_IN_A_ROW*(MAX_CHARS_IN_MSG+1)):
  my_array.append(0)

pos=0
for i in range(upper_pixel_row, msg_height, block_size):
  mid_i = i + int(block_size/2)
  for j in range(left_pixel_col, msg_width, block_size):
    mid_j = j + int(block_size/2)
    if (mid_j < msg_width and mid_i < msg_height):
      r, g, b = rgb_im.getpixel((mid_j, mid_i))
      if r < 100 and g < 100 and b > 200:
        my_array[pos]=1
      pos = pos + 1

message_as_bits = ''
for bit in my_array:
  message_as_bits = message_as_bits + str(bit)

letter = 0
decoded = ''
for n in range(0, len(message_as_bits)):
  if n % 8 == 0:
    if letter != 0:
      decoded = decoded + chr(letter)
      letter = 0
    letter = int(message_as_bits[n]) * 128 + letter 
  elif n % 8 == 1:
    letter = int(message_as_bits[n]) * 64 + letter 
  elif n % 8 == 2:
    letter = int(message_as_bits[n]) * 32 + letter 
  elif n % 8 == 3:
    letter = int(message_as_bits[n]) * 16 + letter 
  elif n % 8 == 4:
    letter = int(message_as_bits[n]) * 8 + letter 
  elif n % 8 == 5:
    letter = int(message_as_bits[n]) * 4 + letter 
  elif n % 8 == 6:
    letter = int(message_as_bits[n]) * 2 + letter 
  elif n % 8 == 7:
    letter = int(message_as_bits[n]) * 1 + letter

print("Decoded:", decoded)

