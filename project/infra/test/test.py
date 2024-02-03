import cv2
import numpy as np

# Configurações do vídeo
output_path = 'video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 1
frame_size = (640, 480)

# Inicializa o VideoWriter
out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

cap = cv2.VideoCapture(0)

for i in range(10):
    # Gera 10 frames simples e adiciona ao vídeo
    ok, frame = cap.read()

    # Adiciona o frame ao vídeo
    out.write(frame)

# Libera o objeto VideoWriter
out.release()

print("Vídeo gerado com sucesso.")
