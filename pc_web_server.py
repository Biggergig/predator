from flask import Flask, render_template, request, jsonify
from predator_lib import PredatorCar
import threading

app = Flask(__name__)

# --- Configuration ---
# REPLACE WITH YOUR PI'S IP ADDRESS
PI_IP = "192.168.1.135"

# Pin Configuration (Forward, Backward, Enable)
LEFT_PINS = (17, 27, 22)
RIGHT_PINS = (23, 24, 25)

# Initialize Car
car = PredatorCar(PI_IP, LEFT_PINS, RIGHT_PINS)

@app.route('/')
def index():
    return render_template('index.html', pi_ip=PI_IP)

@app.route('/api/drive', methods=['POST'])
def drive():
    data = request.json
    # Joystick sends x, y coordinates (-1.0 to 1.0)
    x = data.get('x', 0)
    y = data.get('y', 0)
    
    # Simple Tank Drive Mixing
    # Y is forward speed, X is turn
    left = y + x
    right = y - x
    
    # Clamp to -1.0 to 1.0
    left = max(-1.0, min(1.0, left))
    right = max(-1.0, min(1.0, right))
    
    car.move(left, right)
    return jsonify({"status": "ok", "left": left, "right": right})

@app.route('/api/stop', methods=['POST'])
def stop():
    car.stop()
    return jsonify({"status": "stopped"})

@app.route('/api/gpio', methods=['POST'])
def gpio():
    data = request.json
    pin = data.get('pin')
    value = data.get('value')
    car.set_gpio(pin, value)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("Starting Predator Control System...")
    print(f"Connecting to Pi at {PI_IP}...")
    app.run(host='0.0.0.0', port=5000, debug=True)
