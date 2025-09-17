from PIL import Image, ImageDraw, ImageFont
import os

# Dimensiones del GIF
W, H = 250, 120
frames = []

# Posiciones iniciales
muneco_x = 10
muneco_y = 80
balon_x = 150
balon_y = 90

# Fuente para el mensaje final
font = ImageFont.load_default()

# --------------------
# 1. Muñequito corriendo hacia el balón (brazos y piernas se mueven)
# --------------------
for step in range(10):
    img = Image.new("RGB", (W, H), "skyblue")
    d = ImageDraw.Draw(img)
    
    # Dibujar balón
    d.ellipse((balon_x, balon_y, balon_x+10, balon_y+10), fill="orange")
    
    # Muñequito
    x = muneco_x + step*10
    y = muneco_y
    
    # Cabeza
    d.ellipse((x, y-10, x+10, y), fill="black")
    # Cuerpo
    d.line((x+5, y, x+5, y+20), fill="black", width=2)
    # Brazos alternando arriba/abajo
    if step % 2 == 0:
        d.line((x+5-7, y+5, x+5+7, y+5), fill="black", width=2)
        d.line((x+5-5, y+20, x+5-10, y+30), fill="black", width=2)
        d.line((x+5+5, y+20, x+5+10, y+30), fill="black", width=2)
    else:
        d.line((x+5-7, y+10, x+5+7, y+10), fill="black", width=2)
        d.line((x+5-5, y+20, x+5-8, y+30), fill="black", width=2)
        d.line((x+5+5, y+20, x+5+8, y+30), fill="black", width=2)
    
    frames.append(img)

# --------------------
# 2. Patea el balón (balón se mueve hacia portería)
# --------------------
for step in range(10):
    img = Image.new("RGB", (W, H), "skyblue")
    d = ImageDraw.Draw(img)
    
    # Portería
    goal_x = W - 40
    goal_y = 50
    d.rectangle((goal_x, goal_y, goal_x+30, goal_y+40), outline="white", width=2)
    
    # Malla inicial
    for i in range(1, 3):
        d.line((goal_x, goal_y+i*10, goal_x+30, goal_y+i*10), fill="white")
    for i in range(1, 3):
        d.line((goal_x+i*10, goal_y, goal_x+i*10, goal_y+40), fill="white")
    
    # Muñequito frente al balón
    x = muneco_x + 10*10
    y = muneco_y
    d.ellipse((x, y-10, x+10, y), fill="black")
    d.line((x+5, y, x+5, y+20), fill="black", width=2)
    d.line((x-2, y+5, x+12, y+5), fill="black", width=2)  # brazos extendidos
    d.line((x, y+20, x-5, y+30), fill="black", width=2)
    d.line((x+10, y+20, x+15, y+30), fill="black", width=2)
    
    # Balón avanzando
    balon_pos = balon_x + step*8
    d.ellipse((balon_pos, balon_y, balon_pos+10, balon_y+10), fill="orange")
    
    frames.append(img)

# --------------------
# 3. Gol y portería con malla moviéndose
# --------------------
for step in range(6):
    img = Image.new("RGB", (W, H), "skyblue")
    d = ImageDraw.Draw(img)
    
    # Portería
    goal_x = W - 40
    goal_y = 50
    d.rectangle((goal_x, goal_y, goal_x+30, goal_y+40), outline="white", width=2)
    
    # Malla oscilando
    for i in range(1, 3):
        offset = (-2)**step if i % 2 == 0 else 2**(step%2)
        d.line((goal_x+offset, goal_y+i*10, goal_x+30+offset, goal_y+i*10), fill="white")
    for i in range(1, 3):
        offset = (-1)**step * i
        d.line((goal_x+i*10, goal_y, goal_x+i*10, goal_y+40), fill="white")
    
    # Balón dentro de la portería
    d.ellipse((goal_x+10, goal_y+15, goal_x+20, goal_y+25), fill="orange")
    
    # Muñequito celebrando
    x = muneco_x + 10*10
    y = muneco_y - 5
    d.ellipse((x, y-10, x+10, y), fill="black")
    d.line((x+5, y, x+5, y+20), fill="black", width=2)
    d.line((x-2, y+5, x+12, y+0), fill="black", width=2)
    d.line((x, y+20, x-5, y+30), fill="black", width=2)
    d.line((x+10, y+20, x+15, y+30), fill="black", width=2)
    
    frames.append(img)

# --------------------
# 4. Mensaje final
# --------------------
img = Image.new("RGB", (W, H), "skyblue")
d = ImageDraw.Draw(img)
msg = "¡Bienvenido a mi perfil!"
bbox = d.textbbox((0,0), msg, font=font)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
d.text(((W-w)/2, (H-h)/2), msg, fill="black", font=font)
frames.append(img)

# Crear carpeta de salida si no existe
os.makedirs("assets", exist_ok=True)

# Guardar GIF animado
frames[0].save(
    "assets/muneco_gol.gif",
    save_all=True,
    append_images=frames[1:],
    duration=200,
    loop=0
)

print("¡GIF generado en assets/muneco_gol.gif!")
