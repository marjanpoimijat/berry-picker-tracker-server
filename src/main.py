from fastapi import FastAPI, Response, HTTPException
import requests
from dotenv import load_dotenv
import os
app = FastAPI()
load_dotenv()

@app.get("/")
def get_root():
    return {"Hello": "World"}

@app.get("/nlsapi/{z}/{y}/{x}")
def get_nls_tile(z, y, x):

    print("z %s, y %s, x %s," % (z,y,x))
    api_key = os.getenv("NLS_API_KEY")
    url = "https://avoin-karttakuva.maanmittauslaitos.fi/avoin/wmts/1.0.0/maastokartta/default/WGS84_Pseudo-Mercator/{z}/{y}/{x}.png"\
        .format(z=z, y=y, x=x)
    response =requests.get(url, auth=(api_key, ""), stream=True)
    print(url)
    print(api_key)
    if response.status_code == 200:
        print("Success")
        return Response(content=response.content, media_type="image/png", status_code=200)
    return HTTPException(status_code=404, detail="Image not found.") 
