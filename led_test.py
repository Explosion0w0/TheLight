import RPi.GPIO as GPIO
import time



LED_PIN = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

freq = 100

LIGHT = GPIO.PWM(LED_PIN, freq)

try:
    while True:
        for i in range(100):
            LIGHT.start(i)
            if (i%10 == 0):
                print(i)
            time.sleep(0.05)
except KeyboardInterrupt:
    print("stop")
    GPIO.cleanup()