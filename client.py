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
SERVER_IP = "10.126.42.60"
PORT = 9999


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))
data = b""
payload_size = struct.calcsize("Q")

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True, frames_per_buffer=CHUNK)

try:
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024)
            if not packet:
                break
            data += packet

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += client_socket.recv(4*1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        payload = pickle.loads(frame_data)
        frame = payload["frame"]
        audio_data = payload["audio"]

        # Play audio
        stream.write(audio_data)

        # Show video
        cv2.imshow("Client - Video Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print("[-] Error:", e)
finally:
    client_socket.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    cv2.destroyAllWindows()
