from PIL import Image, ImageDraw, ImageFont
import os

# Dimensiones del GIF
W, H = 200, 100
frames = []

# Posiciones iniciales
muneco_x = 10
muneco_y = 60
balon_x = 150
balon_y = 70

# Fuente para el mensaje final
font = ImageFont.load_default()

# --------------------
# 1. Muñequito corriendo hacia el balón
# --------------------
for step in range(10):
    img = Image.new("RGB", (W, H), "skyblue")
    d = ImageDraw.Draw(img)
    
    # Dibujar balón
    d.ellipse((balon_x, balon_y, balon_x+10, balon_y+10), fill="orange")
    
    # Dibujar muñequito (cabeza, cuerpo, brazos, piernas)
    head_radius = 5
    # Cabeza
    d.ellipse((muneco_x+step*10, muneco_y-head_radius*2,
               muneco_x+step*10+head_radius*2, muneco_y), fill="black")
    # Cuerpo
    d.line((muneco_x+step*10+head_radius, muneco_y,
            muneco_x+step*10+head_radius, muneco_y+15), fill="black", width=2)
    # Brazos
    d.line((muneco_x+step*10+head_radius-5, muneco_y+5,
            muneco_x+step*10+head_radius+5, muneco_y+5), fill="black", width=2)
    # Piernas
    d.line((muneco_x+step*10+head_radius, muneco_y+15,
            muneco_x+step*10+head_radius-5, muneco_y+25), fill="black", width=2)
    d.line((muneco_x+step*10+head_radius, muneco_y+15,
            muneco_x+step*10+head_radius+5, muneco_y+25), fill="black", width=2)
    
    frames.append(img)

# --------------------
# 2. Patea el balón (una frame donde el balón se mueve)
# --------------------
for step in range(5):
    img = Image.new("RGB", (W, H), "skyblue")
    d = ImageDraw.Draw(img)
    
    # Muñequito parado frente al balón
    x = muneco_x+10*10  # última posición de la corrida
    # Cabeza
    d.ellipse((x, muneco_y-head_radius*2, x+head_radius*2, muneco_y), fill="black")
    # Cuerpo
    d.line((x+head_radius, muneco_y, x+head_radius, muneco_y+15), fill="black", width=2)
    # Brazos
    d.line((x+head_radius-5, muneco_y+5, x+head_radius+5, muneco_y+5), fill="black", width=2)
    # Piernas
    d.line((x+head_radius, muneco_y+15, x+head_radius-5, muneco_y+25), fill="black", width=2)
    d.line((x+head_radius, muneco_y+15, x+head_radius+5, muneco_y+25), fill="black", width=2)
    
    # Balón avanzando
    balon_pos = balon_x + step*5
    d.ellipse((balon_pos, balon_y, balon_pos+10, balon_y+10), fill="orange")
    
    frames.append(img)

# --------------------
# 3. Celebración del gol
# --------------------
for _ in range(5):
    img = Image.new("RGB", (W, H), "skyblue")
    d = ImageDraw.Draw(img)
    
    # Muñequito saltando (cuerpo un poco más arriba)
    x = muneco_x+10*10
    y = muneco_y - 5
    d.ellipse((x, y-head_radius*2, x+head_radius*2, y), fill="black")
    d.line((x+head_radius, y, x+head_radius, y+15), fill="black", width=2)
    d.line((x+head_radius-5, y+5, x+head_radius+5, y+5), fill="black", width=2)
    d.line((x+head_radius, y+15, x+head_radius-5, y+25), fill="black", width=2)
    d.line((x+head_radius, y+15, x+head_radius+5, y+25), fill="black", width=2)
    
    # Balón en la portería (a la derecha)
    d.ellipse((W-20, balon_y, W-10, balon_y+10), fill="orange")
    
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
    "assets/muneco.gif",
    save_all=True,
    append_images=frames[1:],
    duration=200,  # ms por frame
    loop=0
)
