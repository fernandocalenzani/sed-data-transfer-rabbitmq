from flask import Flask, render_template, Response
from flask_opencv_streamer.streamer import Streamer
import cv2

app = Flask(__name__)

# Configuração do servidor RTSP
streamer = Streamer(port=3030, requires_auth=False)

# Função para capturar frames da webcam


def webcam_gen():
    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Rota para a página HTML


@app.route('/')
def index():
    return render_template('index.html')

# Rota para o stream de vídeo RTSP


@app.route('/video_feed')
def video_feed():
    return Response(webcam_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
