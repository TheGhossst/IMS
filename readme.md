```bash
python -m venv venv
venv\Scripts\activate
```

```bash
pip install opencv-python pyaudio numpy
```
Run server.py on one machine.
Get the server’s IP address (e.g., ipconfig or ifconfig).
Edit client.py → set SERVER_IP to that address.
Run client.py on another machine in the same LAN.
You should see live webcam video and hear audio.
