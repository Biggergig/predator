from gpiozero import LED
from signal import pause

# Initialize GPIO 14 as an LED
# Note: This uses BCM numbering, so GPIO 14 is physical pin 8 on the header.
led = LED(14)

print("Blinking GPIO 14. Press Ctrl+C to stop.")

# Blink the LED: on for 1 second, off for 1 second
led.blink(on_time=1, off_time=1)

# Keep the script running to maintain the blink
pause()
