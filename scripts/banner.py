from PIL import Image, ImageDraw, ImageFont
import os

# Configuración de pixel art
PIXEL = 10  # tamaño de cada pixel
W, H = 25, 12  # tamaño en "pixeles"
IMG_W, IMG_H = W*PIXEL, H*PIXEL

frames = []

# Fuente para mensaje final
font = ImageFont.load_default()

# Paleta simple
BG_COLOR = (0, 0, 50)      # azul oscuro
MUÑECO_COLOR = (0, 0, 0)   # negro
BALON_COLOR = (255, 165, 0) # naranja
PORTERIA_COLOR = (255, 255, 255) # blanca

# -----------------------------
# 1. Muñequito corriendo
# -----------------------------
for step in range(10):
    img = Image.new("RGB", (IMG_W, IMG_H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Balón fijo
    balon_pos = (15, 9)
    d.rectangle([balon_pos[0]*PIXEL, balon_pos[1]*PIXEL,
                 (balon_pos[0]+1)*PIXEL, (balon_pos[1]+1)*PIXEL], fill=BALON_COLOR)

    # Muñequito (bloques)
    muñeco_x = 1 + step
    muñeco_y = 9
    # cabeza
    d.rectangle([muñeco_x*PIXEL, (muñeco_y-1)*PIXEL,
                 (muñeco_x+1)*PIXEL, muñeco_y*PIXEL], fill=MUÑECO_COLOR)
    # cuerpo
    d.rectangle([muñeco_x*PIXEL, muñeco_y*PIXEL,
                 (muñeco_x+1)*PIXEL, (muñeco_y+1)*PIXEL], fill=MUÑECO_COLOR)
    # piernas alternando para simular correr
    if step %2 ==0:
        d.rectangle([muñeco_x*PIXEL, (muñeco_y+1)*PIXEL,
                     (muñeco_x+1)*PIXEL, (muñeco_y+2)*PIXEL], fill=MUÑECO_COLOR)
    else:
        d.rectangle([ (muñeco_x+1)*PIXEL, (muñeco_y+1)*PIXEL,
                      (muñeco_x+2)*PIXEL, (muñeco_y+2)*PIXEL], fill=MUÑECO_COLOR)

    frames.append(img)

# -----------------------------
# 2. Patea el balón
# -----------------------------
for step in range(5):
    img = Image.new("RGB", (IMG_W, IMG_H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Balón se mueve hacia la portería
    balon_x = 15 + step*2
    balon_y = 9
    d.rectangle([balon_x*PIXEL, balon_y*PIXEL,
                 (balon_x+1)*PIXEL, (balon_y+1)*PIXEL], fill=BALON_COLOR)

    # Muñequito está delante
    muñeco_x = 11
    muñeco_y = 9
    d.rectangle([muñeco_x*PIXEL, (muñeco_y-1)*PIXEL,
                 (muñeco_x+1)*PIXEL, muñeco_y*PIXEL], fill=MUÑECO_COLOR)
    d.rectangle([muñeco_x*PIXEL, muñeco_y*PIXEL,
                 (muñeco_x+1)*PIXEL, (muñeco_y+1)*PIXEL], fill=MUÑECO_COLOR)
    d.rectangle([muñeco_x*PIXEL, (muñeco_y+1)*PIXEL,
                 (muñeco_x+1)*PIXEL, (muñeco_y+2)*PIXEL], fill=MUÑECO_COLOR)

    # Portería
    port_x = 22
    port_y = 8
    d.rectangle([port_x*PIXEL, port_y*PIXEL,
                 (port_x+1)*PIXEL, (port_y+3)*PIXEL], fill=PORTERIA_COLOR)

    frames.append(img)

# -----------------------------
# 3. Gol y celebración
# -----------------------------
for step in range(6):
    img = Image.new("RGB", (IMG_W, IMG_H), BG_COLOR)
    d = ImageDraw.Draw(img)

    # Balón en portería
    d.rectangle([22*PIXEL, 9*PIXEL, 23*PIXEL, 10*PIXEL], fill=BALON_COLOR)

    # Muñequito celebrando (brazos arriba)
    muñeco_x = 11
    muñeco_y = 9
    # cabeza
    d.rectangle([muñeco_x*PIXEL, (muñeco_y-1)*PIXEL,
                 (muñeco_x+1)*PIXEL, muñeco_y*PIXEL], fill=MUÑECO_COLOR)
    # cuerpo
    d.rectangle([muñeco_x*PIXEL, muñeco_y*PIXEL,
                 (muñeco_x+1)*PIXEL, (muñeco_y+1)*PIXEL], fill=MUÑECO_COLOR)
    # piernas
    d.rectangle([muñeco_x*PIXEL, (muñeco_y+1)*PIXEL,
                 (muñeco_x+1)*PIXEL, (muñeco_y+2)*PIXEL], fill=MUÑECO_COLOR)
    # brazos arriba
    d.rectangle([ (muñeco_x-1)*PIXEL, (muñeco_y-1)*PIXEL,
                  muñeco_x*PIXEL, muñeco_y*PIXEL], fill=MUÑECO_COLOR)
    d.rectangle([ (muñeco_x+1)*PIXEL, (muñeco_y-1)*PIXEL,
                  (muñeco_x+2)*PIXEL, muñeco_y*PIXEL], fill=MUÑECO_COLOR)

    # Portería
    port_x = 22
    port_y = 8
    d.rectangle([port_x*PIXEL, port_y*PIXEL,
                 (port_x+1)*PIXEL, (port_y+3)*PIXEL], fill=PORTERIA_COLOR)

    frames.append(img)

# -----------------------------
# 4. Mensaje final (varios frames para que dure más)
# -----------------------------
for _ in range(15):  # dura más tiempo
    img = Image.new("RGB", (IMG_W, IMG_H), BG_COLOR)
    d = ImageDraw.Draw(img)
    msg = "¡Bienvenido a mi perfil!"
    bbox = d.textbbox((0,0), msg, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text(((IMG_W-w)/2, (IMG_H-h)/2), msg, fill=(255,255,255), font=font)
    frames.append(img)

# Crear carpeta de salida
os.makedirs("assets", exist_ok=True)

# Guardar GIF animado
frames[0].save(
    "assets/muneco_pixel.gif",
    save_all=True,
    append_images=frames[1:],
    duration=200,
    loop=0
)

print("¡GIF pixel art generado en assets/muneco_pixel.gif!")
