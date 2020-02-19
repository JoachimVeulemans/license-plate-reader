from os import environ
from uuid import uuid4

from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, Response, FileResponse
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run
from aiohttp import ClientSession
from numpy import fromstring, uint8
import cv2

import datetime
import time

from object_detection import Detector

origin = "localhost:4200"

app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_headers=["*"], allow_origins=[origin, "*"], allow_methods=['*'], allow_credentials=True)
detector = Detector()


@app.route("/")
def root(request):
    return HTMLResponse("Server up & running!")
    

@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_image_from_bytes(bytes)


@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    return predict_image_from_bytes(bytes)


@app.route("/lp", methods=["GET"])
async def get_plate(request):
    try:
        id = request.query_params["id"]
        i = request.query_params["i"]
        filename = "tmp/" + id + "-lp-" + i + ".png"
        open(filename)
        return FileResponse(filename)
    except KeyError:
        return HTMLResponse("Error: parameter 'id' was not present.")
    except IOError:
        return HTMLResponse("Error: id: '" + id + "' was not found.")

@app.route("/orig", methods=["GET"])
async def get_orig(request):
    try:
        id = request.query_params["id"]
        filename = "tmp/" + id + "-car.png"
        open(filename)
        return FileResponse(filename)
    except KeyError:
        return HTMLResponse("Error: parameter 'id' was not present.")
    except IOError:
        return HTMLResponse("Error: id: '" + id + "' was not found.")

@app.route("/car", methods=["GET"])
async def get_car(request):
    try:
        id = request.query_params["id"]
        i = request.query_params["i"]
        filename = "tmp/" + id + "-car-" + i + ".png"
        open(filename)
        return FileResponse(filename)
    except KeyError:
        return HTMLResponse("Error: parameter 'id' or 'i' was not present.")
    except IOError:
        return HTMLResponse("Error: id: '" + id + "' was not found.")


def predict_image_from_bytes(bytes):
    img = cv2.imdecode(fromstring(bytes, uint8), cv2.IMREAD_UNCHANGED)
    filename = str(uuid4())

    start = time.time()
    lp = detector.detect_debug(img, filename)
    end = time.time()
    print("Inference took {:.6f} seconds".format(end - start) + " " + str(datetime.datetime.now()))

    return JSONResponse({"id": filename, "licenses": lp})

    
async def get_bytes(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


def _build_cors_preflight_response():
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['content-type'] = 'application/json'
    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT,DELETE"
    return response


def _build_cors_actual_response(response):
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    run(app, host='0.0.0.0', port=port)
