import requests
import time

class PredatorCar:
    def __init__(self, ip_address, left_pins, right_pins):
        """
        Initialize the car.
        :param ip_address: IP address of the Pi (e.g., "192.168.1.100")
        :param left_pins: Tuple (forward_pin, backward_pin, enable_pin)
        :param right_pins: Tuple (forward_pin, backward_pin, enable_pin)
        """
        self.base_url = f"http://{ip_address}:8000"
        self.left_pins = left_pins
        self.right_pins = right_pins
        print(f"Connected to Predator Car at {self.base_url}")

    def _send_batch(self, commands):
        try:
            response = requests.post(f"{self.base_url}/gpio/set", json={"commands": commands}, timeout=0.5)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Connection Error: {e}")
            return False

    def stop(self):
        """Stops the car immediately."""
        try:
            requests.post(f"{self.base_url}/stop", timeout=0.5)
        except:
            pass

    def move(self, left_speed, right_speed):
        """
        Move the car.
        :param left_speed: -1.0 to 1.0
        :param right_speed: -1.0 to 1.0
        """
        commands = []
        
        # Helper to generate commands for one motor
        def add_motor_cmds(pins, speed):
            fwd, bwd, en = pins
            speed = max(-1.0, min(1.0, speed))
            abs_speed = abs(speed)
            
            if speed > 0:
                commands.append({"pin": fwd, "value": 1})
                commands.append({"pin": bwd, "value": 0})
            elif speed < 0:
                commands.append({"pin": fwd, "value": 0})
                commands.append({"pin": bwd, "value": 1})
            else:
                commands.append({"pin": fwd, "value": 0})
                commands.append({"pin": bwd, "value": 0})
            
            # PWM for speed control
            commands.append({"pin": en, "pwm": abs_speed})

        add_motor_cmds(self.left_pins, left_speed)
        add_motor_cmds(self.right_pins, right_speed)
        
        self._send_batch(commands)

    def set_gpio(self, pin, value):
        """Set a generic GPIO pin (e.g. for lights)."""
        self._send_batch([{"pin": pin, "value": value}])
