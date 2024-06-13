import RPi.GPIO as GPIO
import time
import os
from flask import Flask, render_template, request, flash, Response, abort
from threading import Thread
from LED import LED

global bright
bright = 100
autoBright = 100
userControl = False

app = Flask(__name__, template_folder="./page")
app.secret_key = "Super Ultra Hyper Secret Key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/open", methods=["GET", "POST"])
def open():
    global bright, userControl
    bright = 100
    userControl = True
    flash("Open the light", "open")
    return render_template("index.html")


@app.route("/up", methods=["GET", "POST"])
def incBrightness():
    global bright, userControl
    bright += 10
    if (bright > 100):
        bright = 100
    userControl = True
    flash("Increase brightness", "open")
    return render_template("index.html")


@app.route("/down", methods=["GET", "POST"])
def decBrightness():
    global bright, userControl
    bright -= 10
    if (bright < 0):
        bright = 0
    userControl = True
    flash("Decrease brightness", "open")
    return render_template("index.html")

@app.route("/close", methods=["GET", "POST"])
def close():
    global bright, userControl
    bright = 0
    userControl = True
    flash("Close the light", "close")
    return render_template("index.html")

@app.route("/environment", methods=["GET", "POST"])
def enviroLight():
    global userControl
    userControl = False
    flash("Set to environment light", "open")
    return render_template("index.html")

@app.route("/brightness/<val>", methods=["GET", "POST"])
def setBrightness(val):
    global autoBright
    try:
        v = float(val)
        if (v > 100):
            v = 100
        elif (v < 0):
            v = 0
        autoBright = v
        return "auto brightness set to " + str(v)
    except:
        print("set brightness fail")
        abort(400)

def runServer():
    global app
    app.run("0.0.0.0", port=8080)


if __name__ == "__main__":
    led = LED(32, 100)
    server = Thread(target=runServer)
    server.start()
    try:
        while True:
            if (userControl):
                print("user", bright)
                led.glow(bright, 2)
            else:
                print("auto")
                led.glow(autoBright, 2)
    except KeyboardInterrupt:
        del led
        GPIO.cleanup()

    os._exit(0)
