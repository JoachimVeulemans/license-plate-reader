from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse, Response, FileResponse
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import urllib.request
import os
import cv2
import pytesseract
import re
import numpy as np
import imutils
import uuid

origin="localhost:4200"
app = Starlette(debug=True)
app.add_middleware(CORSMiddleware, allow_headers=["*"], allow_origins=[origin, "*"], allow_methods=['*'],  allow_credentials=True)


@app.route("/")
def root(request):
    return HTMLResponse("Backend License Plate Reader is up & running!")


@app.route("/original", methods=["GET"])
async def get_original(request):
    id = request.query_params["id"]
    return FileResponse("plate-" + id + ".png")


@app.route("/plate", methods=["GET"])
async def get_plate(request):
    id = request.query_params["id"]
    return FileResponse("plate-" + id + ".png")    


@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes_img = await (data["file"].read())
    nparr = np.fromstring(bytes_img, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return get_license_plate_text(img)


def return_license(license, id):
    return JSONResponse({"license": license, "id": id})


def get_license_plate_text(img):
    # Resize image so why can use different formats of images with the same code
    img = cv2.resize(img, (620, 480))

    # Convert image to grey scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur image in order to reduce noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Execute Canny to do edge detection
    edged = cv2.Canny(gray, 30, 200)

    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screen_cnts = []

    # Loop over our contours
    for c in cnts:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # Let's say when it has 4 corners, we have found the license
        # TODO -> Future improvement, maybe check every box with 4 corners? return array of possibilities?
        if len(approx) == 4:
            screen_cnts.append(approx)
            break

    for screen_cnt in screen_cnts:
        cv2.drawContours(img, [screen_cnt], -1, (0, 255, 0), 3)

        # Make everything around the license black
        mask = np.zeros(gray.shape, np.uint8)
        blacked_img = cv2.drawContours(mask, [screen_cnt], 0, 255, -1,)
        blacked_img = cv2.bitwise_and(img, img, mask=mask)

        # Crop image
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        cropped = gray[topx:bottomx+1, topy:bottomy+1]

        # Convert image to text through tesseract
        # https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options
        text = pytesseract.image_to_string(cropped, config='--psm 11')

        # ######################################
        # #### Uncomment below for testing #####
        # ######################################
        """
        cv2.imshow('Original', img)
        cv2.imshow('Blacked', blacked_img)
        cv2.imshow('Cropped', cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """

        id = str(uuid.uuid1())

        cv2.imwrite('original-' + id + '.png', img)
        cv2.imwrite('plate-' + id + '.png', cropped)

        #text = text.upper().replace("\n", "")
        text = re.sub('[^A-Z0-9.]', '', text.upper())

        if text != "":
            return return_license(text, id)

    return return_license("", 0)


def _build_cors_prelight_response():
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
    port = int(os.environ.get('PORT', 443))
    uvicorn.run(app, host='0.0.0.0', port=port)
