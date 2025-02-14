from flask import Flask, Response, request
import cv2
import numpy as np

app = Flask(__name__)

# Здесь будет храниться поток данных
frame = None

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_frames():
    global frame
    while True:
        if frame is not None:
            # Кодируем изображение в JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

@app.route('/update_frame', methods=['POST'])
def update_frame():
    global frame
    frame = cv2.imdecode(np.frombuffer(request.data, np.uint8), cv2.IMREAD_COLOR)
    return '', 204

@app.route('/')
def index():
    return '''
    <html>
        <head>
            <title>Screen Capture</title>
        </head>
        <body>
            <h1>Live Screen Capture</h1>
            <img src="/video_feed">
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
