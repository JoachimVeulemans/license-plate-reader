from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from gpiozero import LED
from time import sleep

app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_headers=["*"], allow_origins=["*"], allow_methods=['*'], allow_credentials=True)


@app.route("/")
def root(request):
    return HTMLResponse("Raspberry Pi Listener is up & running!")


@app.route("/garagedoor", methods=["POST"])
def garagedoor(request):
    led = LED(17)
    led.toggle()
    return HTMLResponse("Garage door toggled")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=443)

    """
    led = LED(17)

    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)
    """
