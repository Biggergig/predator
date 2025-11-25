import time
import threading
from typing import List, Optional
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from gpiozero import PWMOutputDevice, DigitalOutputDevice

app = FastAPI()

# --- Global State ---
# Store active devices to prevent re-initialization and allow cleanup
# Key: pin number (int), Value: gpiozero device object
active_devices = {}
last_command_time = time.time()
WATCHDOG_TIMEOUT = 2.0  # Seconds

# --- Pydantic Models ---
class PinCommand(BaseModel):
    pin: int
    value: Optional[float] = None # 0 or 1 for digital, 0.0-1.0 for PWM. If None, ignored.
    pwm: Optional[float] = None   # Explicit PWM value 0.0-1.0

class PinBatch(BaseModel):
    commands: List[PinCommand]

# --- Watchdog ---
def watchdog_loop():
    """Checks if we haven't received a command in a while. If so, stop everything."""
    global last_command_time
    while True:
        if time.time() - last_command_time > WATCHDOG_TIMEOUT:
            stop_all_pins()
        time.sleep(0.5)

# Start watchdog in a background thread
watchdog_thread = threading.Thread(target=watchdog_loop, daemon=True)
watchdog_thread.start()

# --- Helper Functions ---
def get_or_create_device(pin: int, is_pwm: bool):
    """Gets an existing device or creates a new one for the given pin."""
    if pin in active_devices:
        device = active_devices[pin]
        # If we need PWM but have Digital (or vice versa), close and recreate
        if is_pwm and isinstance(device, DigitalOutputDevice) and not isinstance(device, PWMOutputDevice):
            device.close()
        elif not is_pwm and isinstance(device, PWMOutputDevice):
            device.close()
        else:
            return device

    try:
        if is_pwm:
            device = PWMOutputDevice(pin)
        else:
            device = DigitalOutputDevice(pin)
        active_devices[pin] = device
        return device
    except Exception as e:
        print(f"Error initializing pin {pin}: {e}")
        return None

def stop_all_pins():
    """Stops all active pins."""
    for pin, device in active_devices.items():
        device.off()
        # print(f"Watchdog/Stop: Pin {pin} turned off.") # Debug logging

# --- Endpoints ---

@app.post("/gpio/set")
def set_pins(batch: PinBatch):
    global last_command_time
    last_command_time = time.time()
    
    results = []
    for cmd in batch.commands:
        is_pwm = cmd.pwm is not None
        target_value = cmd.pwm if is_pwm else cmd.value
        
        if target_value is None:
            continue

        device = get_or_create_device(cmd.pin, is_pwm)
        if device:
            if is_pwm:
                device.value = max(0.0, min(1.0, target_value))
            else:
                if target_value > 0.5:
                    device.on()
                else:
                    device.off()
            results.append({"pin": cmd.pin, "status": "ok", "value": target_value})
        else:
            results.append({"pin": cmd.pin, "status": "error"})
            
    return {"results": results}

@app.post("/stop")
def stop_endpoint():
    global last_command_time
    last_command_time = time.time()
    stop_all_pins()
    return {"status": "stopped"}

@app.get("/")
def health_check():
    return {"status": "Predator Pi Firmware Online"}

if __name__ == "__main__":
    import uvicorn
    # Run on 0.0.0.0 to be accessible from the network
    uvicorn.run(app, host="0.0.0.0", port=8000)
