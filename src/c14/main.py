from fastapi import FastAPI, HTTPException
import requests
import uvicorn

app = FastAPI(
    title="Validador de CEP API",
    version="1.0.0"
)

def get_address_by_cep(cep: str):
    if not cep.isdigit() or len(cep) != 8:
        raise HTTPException(status_code=400, detail="CEP inválido")

    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro na consulta externa")

    data = response.json()
    if "erro" in data:
        raise HTTPException(status_code=404, detail="CEP não encontrado")

    return data

@app.get("/cep/{cep}")
def read_cep(cep: str):
    return get_address_by_cep(cep)

if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)

