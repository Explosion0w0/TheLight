import RPi.GPIO as GPIO
import time


class LED:
    def __init__(self, pin:int=32, freq:int=100) -> None:
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self.freq = freq
        self.light = GPIO.PWM(pin, freq)

    def glow(self, brightness=100, seconds=2) -> None:
        f = self.freq * brightness / 100.0
        if (f > self.freq):
            f = self.freq
        self.light.start(f)
        print("glow: ", f)
        time.sleep(2)

    def stop(self) -> None:
        print("stop")
        self.light.stop()
        

if __name__ == "__main__":
    try:
        led = LED(32, 100)
        while True:
            bright = int(input("brightness: "))
            led.glow(bright, 2)
    except KeyboardInterrupt:
        print("stop")
        GPIO.cleanup()
