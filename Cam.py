import cv2
import numpy as np
import os
import random
import time

# Fonction pour convertir une image en ASCII
def image_to_ascii(image, cols=80, rows=24):
    height, width, _ = image.shape
    cell_width = width / cols
    cell_height = height / rows
    ascii_art = ""
    
    # Caractères ASCII pour représenter les niveaux de luminosité
    chars = " ____-@#Gvq#@-____"
    
    for i in range(rows):
        for j in range(cols):
            x = int(j * cell_width)
            y = int(i * cell_height)
            roi = image[y:y + int(cell_height), x:x + int(cell_width)]
            brightness = np.mean(roi)
            char_index = min(int(brightness / 255 * (len(chars) - 1)), len(chars) - 1)
            ascii_art += chars[char_index]
        ascii_art += "\n"
    
    return ascii_art

# Fonction pour ajuster la netteté, le contraste et la luminosité
def ajuster_image(image, netteté=1.0, contraste=1.0, luminosité=0):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel * netteté)
    image = cv2.convertScaleAbs(image, alpha=contraste, beta=luminosité)
    return image

# Fonction pour générer un fond animé de style cmatrix
def generate_cmatrix_background(cols=80, rows=24):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    background = ""
    for _ in range(rows):
        line = "".join(random.choice(chars) for _ in range(cols))
        background += line + "\n"
    return background

# Capturer le flux vidéo de la webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam.")
    exit()

# Paramètres initiaux
netteté = 1.0
contraste = 1.0
luminosité = 0

while True:
    # Lire une frame de la webcam
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire la frame.")
        break
    
    # Redimensionner la frame pour une meilleure performance
    frame = cv2.resize(frame, (160, 90))  # Résolution réduite pour l'ASCII
    
    # Ajuster la netteté, le contraste et la luminosité
    frame_ajustée = ajuster_image(frame, netteté, contraste, luminosité)
    
    # Convertir l'image en ASCII
    ascii_art = image_to_ascii(frame_ajustée, cols=80, rows=24)
    
    # Générer un fond animé de style cmatrix
    cmatrix_background = generate_cmatrix_background(cols=80, rows=24)
    
    # Superposer l'ASCII art de la webcam sur le fond animé
    combined_art = ""
    for line_webcam, line_cmatrix in zip(ascii_art.split("\n"), cmatrix_background.split("\n")):
        combined_line = "".join([c1 if c1 != " " else c2 for c1, c2 in zip(line_webcam, line_cmatrix)])
        combined_art += combined_line + "\n"
    
    # Effacer l'écran et afficher l'ASCII art combiné
    os.system('cls' if os.name == 'nt' else 'clear')
    print(combined_art)
    
    # Attendre un peu pour limiter la fréquence d'affichage
    time.sleep(0.1)
    
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la webcam et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()

