from PIL import Image, ImageDraw, ImageFont
import os

PIX = 10  # tamaño de un "pixel"
W, H = 25, 12  # ancho y alto en pixels
IMG_W, IMG_H = W*PIX, H*PIX
frames = []

# Fuente para mensaje final
font = ImageFont.load_default()

# Colores
BG = (0, 0, 50)
MUÑECO = (0, 0, 0)
BALON = (255, 165, 0)
PORTERIA = (255, 255, 255)

# -----------------------------
# Fase 1: Muñequito corriendo
# -----------------------------
for step in range(10):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)

    # Balón fijo
    d.rectangle([15*PIX, 9*PIX, 16*PIX, 10*PIX], fill=BALON)

    # Muñequito
    x = 1 + step
    y = 9
    # cabeza
    d.rectangle([x*PIX, (y-1)*PIX, (x+1)*PIX, y*PIX], fill=MUÑECO)
    # cuerpo
    d.rectangle([x*PIX, y*PIX, (x+1)*PIX, (y+1)*PIX], fill=MUÑECO)
    # piernas alternando
    if step % 2 == 0:
        d.rectangle([x*PIX, (y+1)*PIX, (x+1)*PIX, (y+2)*PIX], fill=MUÑECO)
    else:
        d.rectangle([(x+1)*PIX, (y+1)*PIX, (x+2)*PIX, (y+2)*PIX], fill=MUÑECO)

    frames.append(img)

# -----------------------------
# Fase 2: Patea el balón
# -----------------------------
for step in range(5):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)

    # Balón se mueve
    balon_x = 15 + step*2
    d.rectangle([balon_x*PIX, 9*PIX, (balon_x+1)*PIX, 10*PIX], fill=BALON)

    # Muñequito delante
    d.rectangle([11*PIX, 8*PIX, 12*PIX, 9*PIX], fill=MUÑECO)  # cabeza
    d.rectangle([11*PIX, 9*PIX, 12*PIX, 10*PIX], fill=MUÑECO) # cuerpo
    d.rectangle([11*PIX, 10*PIX, 12*PIX, 11*PIX], fill=MUÑECO) # piernas

    # Portería
    for i in range(3):
        d.rectangle([22*PIX, (8+i)*PIX, 23*PIX, (9+i)*PIX], fill=PORTERIA)

    frames.append(img)

# -----------------------------
# Fase 3: Gol y portería animada
# -----------------------------
for step in range(6):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)

    # Balón en portería
    d.rectangle([22*PIX, 9*PIX, 23*PIX, 10*PIX], fill=BALON)

    # Muñequito celebrando
    d.rectangle([11*PIX, 7*PIX, 12*PIX, 8*PIX], fill=MUÑECO)  # cabeza
    d.rectangle([11*PIX, 8*PIX, 12*PIX, 9*PIX], fill=MUÑECO)  # cuerpo
    d.rectangle([11*PIX, 9*PIX, 12*PIX, 10*PIX], fill=MUÑECO) # piernas
    # brazos arriba
    d.rectangle([10*PIX, 7*PIX, 11*PIX, 8*PIX], fill=MUÑECO)
    d.rectangle([12*PIX, 7*PIX, 13*PIX, 8*PIX], fill=MUÑECO)

    # Portería
    for i in range(3):
        d.rectangle([22*PIX, (8+i)*PIX, 23*PIX, (9+i)*PIX], fill=PORTERIA)

    frames.append(img)

# -----------------------------
# Fase 4: Mensaje final prolongado
# -----------------------------
for _ in range(15):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)
    msg = "¡Bienvenido a mi perfil!"
    bbox = d.textbbox((0,0), msg, font=font)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text(((IMG_W-w)/2, (IMG_H-h)/2), msg, fill=(255,255,255), font=font)
    frames.append(img)

# Guardar GIF
os.makedirs("assets", exist_ok=True)
frames[0].save(
    "assets/muneco_pixel.gif",
    save_all=True,
    append_images=frames[1:],
    duration=200,
    loop=0
)
print("¡GIF pixel art generado en assets/muneco_pixel.gif!")
