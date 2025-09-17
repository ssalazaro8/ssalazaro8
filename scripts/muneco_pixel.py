from PIL import Image, ImageDraw, ImageFont
import os

# Configuración general
PIX = 10
W, H = 50, 20
IMG_W, IMG_H = W*PIX, H*PIX
frames = []

# Colores
BG = (135, 206, 235)        # cielo celeste
CAR = (220, 20, 60)         # rojo chimba
WHEEL = (20, 20, 20)        # ruedas negras
HIGHLIGHT = (255, 255, 255) # reflejo del carro
FLAG_BG = (255, 215, 0)     # amarillo bandera
TEXT_COLOR = (0, 0, 0)      # texto negro

# Fuente para el mensaje
font = ImageFont.load_default()

# Animación
for step in range(25):
    img = Image.new("RGB", (IMG_W, IMG_H), BG)
    d = ImageDraw.Draw(img)
    
    # Auto deportivo
    car_x = 2 + step
    car_y = 12
    # Cuerpo
    d.rectangle([car_x*PIX, (car_y-3)*PIX, (car_x+7)*PIX, car_y*PIX], fill=CAR)
    # Techo
    d.polygon([(car_x*PIX+2, (car_y-3)*PIX),
               (car_x*PIX+5, (car_y-3)*PIX),
               (car_x*PIX+6, (car_y-4)*PIX),
               (car_x*PIX+1, (car_y-4)*PIX)], fill=CAR)
    # Reflejo
    d.line([(car_x*PIX+1, (car_y-3)*PIX), (car_x*PIX+6, (car_y-3)*PIX)], fill=HIGHLIGHT)
    
    # Ruedas
    d.ellipse([(car_x*PIX+1, car_y*PIX), (car_x*PIX+2.5, car_y*PIX+1.5)], fill=WHEEL)
    d.ellipse([(car_x*PIX+5, car_y*PIX), (car_x*PIX+6.5, car_y*PIX+1.5)], fill=WHEEL)
    
    # Bandera bienvenida
    flag_x = (car_x+8)*PIX
    flag_y = (car_y-5)*PIX
    d.rectangle([flag_x, flag_y, flag_x+PIX*12, flag_y+PIX*3], fill=FLAG_BG)
    msg = "¡Bienvenido a mi perfil!"
    d.text((flag_x+5, flag_y+5), msg, fill=TEXT_COLOR, font=font)
    
    frames.append(img)

# Guardar GIF
os.makedirs("assets", exist_ok=True)
frames[0].save(
    "assets/muneco_pixel_final.gif",
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0
)

print("¡GIF del auto chimba generado en assets/auto_chimba.gif!")
