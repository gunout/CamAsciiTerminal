import cv2
import numpy as np
import os

# Fonction pour convertir une image en ASCII
def image_to_ascii(image, cols=80, rows=24):
    # Redimensionner l'image pour correspondre au nombre de colonnes et de lignes
    height, width, _ = image.shape
    cell_width = width / cols
    cell_height = height / rows
    ascii_art = ""
    
    # Caractères ASCII pour représenter les niveaux de luminosité
    chars = " ____-@#Gvq#@-____"
    
    for i in range(rows):
        for j in range(cols):
            # Extraire la région de l'image correspondant à la cellule
            x = int(j * cell_width)
            y = int(i * cell_height)
            roi = image[y:y + int(cell_height), x:x + int(cell_width)]
            
            # Calculer la luminosité moyenne de la région
            brightness = np.mean(roi)
            
            # Convertir la luminosité en caractère ASCII
            char_index = min(int(brightness / 255 * (len(chars) - 1)), len(chars) - 1)
            ascii_art += chars[char_index]
        ascii_art += "\n"
    
    return ascii_art

# Fonction pour ajuster la netteté, le contraste et la luminosité
def ajuster_image(image, netteté=1.0, contraste=1.0, luminosité=0):
    # Ajuster la netteté
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel * netteté)
    
    # Ajuster le contraste et la luminosité
    image = cv2.convertScaleAbs(image, alpha=contraste, beta=luminosité)
    
    return image

# Capturer le flux vidéo de la webcam
cap = cv2.VideoCapture(0)

# Vérifier si la webcam est ouverte
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
    
    # Effacer l'écran et afficher l'ASCII art
    os.system('cls' if os.name == 'nt' else 'clear')
    print(ascii_art)
    
    # Attendre un peu pour limiter la fréquence d'affichage
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la webcam et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
