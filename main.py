import PIL.ImageOps
from pdf2image import convert_from_path
import PIL
import uvicorn
import io
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import FastAPI, Request

TILE_SIZE = 2 ** 8
FULL_SIZE = 2 ** 13


def prepare():
    image = convert_from_path(pdf_path='assets/P0447_PL_101_1-50.pdf', dpi=200, poppler_path=r"poppler-21.10.0/Library/bin")[0]
    image = PIL.ImageOps.pad(image, size=(FULL_SIZE, FULL_SIZE), color=(255, 255, 255, 0))
    for z in range(0, 6):
        for x in range(0, 2 ** z):
            for y in range(0, 2 ** z):
                get_image(image, x, y, z)


def get_image(image, x: int, y: int, z: int):
    cut_size = FULL_SIZE / 2 ** z
    if cut_size < TILE_SIZE:
        print("tiles too small: ", cut_size, z)
    tile = image.crop(box=(x * cut_size, y * cut_size, (x+1) * cut_size, (y+1) * cut_size))
    tile = PIL.ImageOps.contain(tile, (TILE_SIZE, TILE_SIZE))
    tile.save(f'static/tiles/tile-{z}-{x}-{y}.png')


if __name__ == "__main__":
    # prepare()
    app = FastAPI()
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
    uvicorn.run(app, port=80)


