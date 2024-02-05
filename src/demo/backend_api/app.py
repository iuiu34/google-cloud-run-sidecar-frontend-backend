from random import randint

from fastapi import FastAPI, Request

from demo.frontend.api.verify import VerifyFrontendMiddleware

app = FastAPI(
    title="Backend api",
    version="0.0.1",
)

app.add_middleware(VerifyFrontendMiddleware)


@app.get("/get_random_number")
async def get_random_number():
    return {"random_number": randint(1, 100)}


@app.get("/get_headers")
async def get_random_number(request: Request):
    return {"origin": request.client.host,
            "request_headers": request.headers}


@app.get("/")
async def homepage():
    return {"message": "ok"}
