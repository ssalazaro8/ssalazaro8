from PIL import Image, ImageDraw, ImageFont
import os

PIX = 10
W, H = 25, 12
IMG_W, IMG_H = W*PIX, H*PIX
frames = []

font = ImageFont.load_default()

BG = (0, 0, 50)
MUÑECO = (0, 0, 0)
BALON = (255, 165, 0)
PORTERIA = (255, 255, 255)

# -----------------------------
# 1. Corriendo (15 frames)
# -----------------------------
for step in range(15):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)

    # Balón fijo
    d.rectangle([15*PIX, 9*PIX, 16*PIX, 10*PIX], fill=BALON)

    # Muñequito
    x = 1 + step
    y = 9
    d.rectangle([x*PIX, (y-1)*PIX, (x+1)*PIX, y*PIX], fill=MUÑECO)  # cabeza
    d.rectangle([x*PIX, y*PIX, (x+1)*PIX, (y+1)*PIX], fill=MUÑECO)   # cuerpo
    if step % 2 == 0:
        d.rectangle([x*PIX, (y+1)*PIX, (x+1)*PIX, (y+2)*PIX], fill=MUÑECO)
    else:
        d.rectangle([(x+1)*PIX, (y+1)*PIX, (x+2)*PIX, (y+2)*PIX], fill=MUÑECO)

    frames.append(img)

# -----------------------------
# 2. Pateando (10 frames)
# -----------------------------
for step in range(10):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)

    # Balón en movimiento
    balon_x = 15 + step*2
    d.rectangle([balon_x*PIX, 9*PIX, (balon_x+1)*PIX, 10*PIX], fill=BALON)

    # Muñequito frente al balón
    d.rectangle([11*PIX, 8*PIX, 12*PIX, 9*PIX], fill=MUÑECO)  # cabeza
    d.rectangle([11*PIX, 9*PIX, 12*PIX, 10*PIX], fill=MUÑECO) # cuerpo
    d.rectangle([11*PIX, 10*PIX, 12*PIX, 11*PIX], fill=MUÑECO) # piernas

    # Portería
    for i in range(3):
        d.rectangle([22*PIX, (8+i)*PIX, 23*PIX, (9+i)*PIX], fill=PORTERIA)

    frames.append(img)

# -----------------------------
# 3. Gol y celebración (6 frames)
# -----------------------------
for step in range(6):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)

    # Balón dentro de la portería
    d.rectangle([22*PIX, 9*PIX, 23*PIX, 10*PIX], fill=BALON)

    # Muñequito celebrando
    d.rectangle([11*PIX, 7*PIX, 12*PIX, 8*PIX], fill=MUÑECO)  # cabeza
    d.rectangle([11*PIX, 8*PIX, 12*PIX, 9*PIX], fill=MUÑECO)  # cuerpo
    d.rectangle([11*PIX, 9*PIX, 12*PIX, 10*PIX], fill=MUÑECO) # piernas
    # brazos arriba
    d.rectangle([10*PIX, 7*PIX, 11*PIX, 8*PIX], fill=MUÑECO)
    d.rectangle([12*PIX, 7*PIX, 13*PIX, 8*PIX], fill=MUÑECO)

    # Portería con malla moviéndose
    offset = (-1)**step
    for i in range(3):
        d.rectangle([22*PIX, (8+i)*PIX, 23*PIX, (9+i)*PIX], fill=PORTERIA)
        d.rectangle([22*PIX+offset, (8+i)*PIX, 23*PIX+offset, (9+i)*PIX], fill=PORTERIA)

    frames.append(img)

# -----------------------------
# 4. Mensaje final (15 frames)
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
    "assets/muneco_pixel_final.gif",
    save_all=True,
    append_images=frames[1:],
    duration=150,
    loop=0
)
print("¡GIF pixel art final generado en assets/muneco_pixel_final.gif!")
