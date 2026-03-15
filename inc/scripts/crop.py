import sys
from PIL import Image

# Acceder a los argumentos
src_file = sys.argv[1]
dst_file = sys.argv[2]
x1 = int(sys.argv[3])
y1 = int(sys.argv[4])
x2 = int(sys.argv[5])
y2 = int(sys.argv[6])

# Abrir la imagen
im = Image.open(src_file)

# Recortar la imagen
cropped_im = im.crop((x1, y1, x2, y2))

# Guardar la imagen recortada
cropped_im.save(dst_file)
