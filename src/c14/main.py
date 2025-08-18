from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import httpx
import json

app = FastAPI(debug=True)

@app.get("/{pokemon_name}")
async def get_pokemon(pokemon_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Pokémon não encontrado")
        
        try:
            data = response.json()
            return JSONResponse(
                content=json.loads(json.dumps(data, indent=4)),  # força identação
                media_type="application/json"
            )
        except Exception:
            raise HTTPException(status_code=500, detail="Resposta da API não é JSON válido")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
