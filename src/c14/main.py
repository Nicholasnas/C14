from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import httpx


app = FastAPI()


@app.get('/')
async def hello_api():
    content = "<h1>Api para obtenção de dados de pokemons</h1>"
    return HTMLResponse(content)
    

@app.get("/{pokemon_name}")
async def get_persons(pokemon_name:str):
    async with httpx.AsyncClient() as client:
        
        response = await client.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Pokemon não encontrado")
        
        try:
            
            return response.json()
        except Exception:
            raise HTTPException(status_code=500, detail="Resposta da api errada")
            
 

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
