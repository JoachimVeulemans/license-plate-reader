from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import RPi.GPIO as GPIO
from time import sleep

app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_headers=["*"], allow_origins=["*"], allow_methods=['*'], allow_credentials=True)

switches = [11, 13, 15, 22, 36, 37, 16, 18]

GPIO.setmode(GPIO.BOARD)
for i in range(len(switches)):
    GPIO.setup(switches[i], GPIO.OUT)
    GPIO.output(switches[i], GPIO.HIGH)

@app.route("/")
def root(request):
    return HTMLResponse("Raspberry Pi Listener is up & running!")


@app.route("/garage", methods=["GET"])
def garagedoor(request):
    GPIO.output(switches[0], GPIO.LOW)
    sleep(0.1)
    GPIO.output(switches[0], GPIO.HIGH)
    return HTMLResponse("Garage door toggled")


@app.route("/fun", methods=["GET"])
def fun(request):
    for i in range(len(switches)):
        GPIO.output(switches[i], GPIO.LOW)
        print('Switch status = ', GPIO.input(switches[i]))
        sleep(0.1)
        GPIO.output(switches[i], GPIO.HIGH)
        print('Switch status = ', GPIO.input(switches[i]))
    return HTMLResponse("Fun toggled")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
    GPIO.cleanup()
