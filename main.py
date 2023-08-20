from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

@app.get('/')
def sample():
   return RedirectResponse("https://telegram.me/raceredgebot")