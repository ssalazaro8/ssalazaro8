from PIL import Image, ImageDraw, ImageFont
import os

# -----------------------------
# Configuración
# -----------------------------
PIX = 10
W, H = 30, 12
IMG_W, IMG_H = W*PIX, H*PIX
frames = []

font = ImageFont.load_default()

BG = (0, 100, 200)      # fondo cielo
CAR = (255, 0, 0)       # auto rojo
WHEEL = (0, 0, 0)       # ruedas negras
FLAG = (255, 255, 0)    # bandera amarilla
TEXT_COLOR = (0, 0, 0)  # texto negro

# -----------------------------
# Animación del auto (20 frames)
# -----------------------------
for step in range(20):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)
    
    # Auto
    car_x = 2 + step
    car_y = 8
    # Cuerpo
    d.rectangle([car_x*PIX, (car_y-2)*PIX, (car_x+4)*PIX, car_y*PIX], fill=CAR)
    # Ruedas alternadas para simular movimiento
    if step % 2 == 0:
        d.rectangle([car_x*PIX, car_y*PIX, (car_x+1)*PIX, (car_y+1)*PIX], fill=WHEEL)
        d.rectangle([(car_x+3)*PIX, car_y*PIX, (car_x+4)*PIX, (car_y+1)*PIX], fill=WHEEL)
    else:
        d.rectangle([ (car_x+0.5)*PIX, car_y*PIX, (car_x+1.5)*PIX, (car_y+1)*PIX], fill=WHEEL)
        d.rectangle([ (car_x+2.5)*PIX, car_y*PIX, (car_x+3.5)*PIX, (car_y+1)*PIX], fill=WHEEL)
    
    # Bandera
    flag_x = (car_x+4)*PIX
    flag_y = (car_y-3)*PIX
    d.rectangle([flag_x, flag_y, flag_x+PIX*4, flag_y+PIX*2], fill=FLAG)
    # Texto dentro de la bandera
    msg = "¡Bienvenido!"
    d.text((flag_x+2, flag_y), msg, fill=TEXT_COLOR, font=font)
    
    frames.append(img)

# -----------------------------
# Guardar GIF
# -----------------------------
os.makedirs("assets", exist_ok=True)
frames[0].save(
    "assets/auto_pixel.gif",
    save_all=True,
    append_images=frames[1:],
    duration=150,  # ms por frame
    loop=0
)

print("¡GIF pixel art del auto generado en assets/auto_pixel.gif!")
