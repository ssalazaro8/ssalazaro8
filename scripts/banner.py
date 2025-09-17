from PIL import Image, ImageDraw, ImageFont
import os

# Dimensiones del banner
W, H = 600, 200
frames = []
font = ImageFont.load_default()

# Textos que se mostrarán en secuencia
texts = [
    "⚽ El jugador se prepara...",
    "⚽ Patea el balón...",
    "⚽ El balón vuela...",
    "🏟️ GOOOOOOL !!!",
    "SAMUEL SALAZAR OSPINA"
]

# Crear los frames del GIF
for t in texts:
    img = Image.new("RGB", (W, H), color="navy")
    d = ImageDraw.Draw(img)
    
    # Obtener ancho y alto del texto usando textbbox
    bbox = d.textbbox((0, 0), t, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    # Dibujar el texto centrado
    d.text(((W - w) / 2, (H - h) / 2), t, fill="white", font=font)
    frames.append(img)

# Crear carpeta de salida si no existe
os.makedirs("assets", exist_ok=True)

# Guardar como GIF animado
frames[0].save(
    "assets/banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1000,   # duración de cada frame (ms)
    loop=0           # 0 = bucle infinito
)
