# Predator Control System - Setup Guide

You have successfully built the **Predator Control System**! This guide will help you set up the Raspberry Pi and your PC to start driving.

## 1. Raspberry Pi Setup (The "Robot")

Do this on the Raspberry Pi (via SSH or monitor).

1.  **Copy Files**: Transfer `pi_firmware.py` and `requirements.txt` to the Pi.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Firmware**:
    ```bash
    python pi_firmware.py
    ```
    *   You should see: `Uvicorn running on http://0.0.0.0:8000`

## 2. PC Setup (The "Controller")

Do this on your Windows PC.

1.  **Install Dependencies**:
    ```bash
    pip install -r pc_requirements.txt
    ```
2.  **Configure IP**:
    *   Open `pc_web_server.py` in your editor.
    *   Find the line: `PI_IP = "192.168.1.100"`
    *   Change it to your Raspberry Pi's actual IP address.
3.  **Run the Controller**:
    ```bash
    python pc_web_server.py
    ```
    *   You should see: `Running on http://0.0.0.0:5000`

## 3. Start Driving!

1.  Open your web browser on the PC.
2.  Go to: `http://localhost:5000`
3.  You should see the **Cyberpunk Interface**.
    *   **Arrow Keys**: Drive the car.
    *   **Spacebar**: Emergency Stop.
    *   **Buttons**: Toggle Headlights/Underglow (if wired).

## Troubleshooting

*   **Connection Error**: Make sure both devices are on the same Wi-Fi. Try `ping <PI_IP>` from your PC.
*   **Motors Not Moving**: Check your L298N wiring.
    *   Left Motor: GPIO 17, 27 (Enable: 22)
    *   Right Motor: GPIO 23, 24 (Enable: 25)
    *   *Note: If your car spins in circles, swap the wires on one motor.*
