import socket
import cv2
import pickle
import struct
import pyaudio

# ---------- Audio Configuration ----------
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# ---------- Network Configuration ----------
SERVER_IP = "0.0.0.0"  # Listen on all interfaces
PORT = 9999

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)
print(f"[+] Server listening on {SERVER_IP}:{PORT}")

conn, addr = server_socket.accept()
print(f"[+] Connection from {addr}")

# ---------- Setup Video and Audio ----------
video = cv2.VideoCapture(0)
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, frames_per_buffer=CHUNK)

try:
    while True:
        # Capture video frame
        ret, frame = video.read()
        if not ret:
            break

        # Read audio chunk
        audio_data = stream.read(CHUNK)

        # Serialize frame and audio
        payload = {"frame": frame, "audio": audio_data}
        data = pickle.dumps(payload)
        message = struct.pack("Q", len(data)) + data

        conn.sendall(message)
except Exception as e:
    print("[-] Error:", e)
finally:
    video.release()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    conn.close()
    server_socket.close()
