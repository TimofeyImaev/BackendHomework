import uvicorn
import random
import secrets

from fastapi import FastAPI

app = FastAPI()


@app.get("/random")
async def random():
    s = secrets.token_urlsafe(16)
    return s


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()