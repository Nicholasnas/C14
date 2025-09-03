# 📍 API de Consulta de CEP

Este projeto é uma **API desenvolvida com FastAPI** que consulta os dados de um endereço a partir de um **CEP** brasileiro.  
A API utiliza a [ViaCEP](https://viacep.com.br) como fonte de dados externa.

---

## ✨ Funcionalidades

- Consulta informações de endereço a partir do CEP.
- Valida formato de CEP (apenas números e 8 dígitos).
- Retorna mensagens de erro apropriadas para:
  - CEP inválido.
  - CEP não encontrado.
  - Erro de comunicação com o serviço externo.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Requests](https://docs.python-requests.org/)
- [Poetry](https://python-poetry.org/) (gerenciador de dependências)
- [unittest](https://docs.python.org/3/library/unittest.html) (testes automatizados)

---

## 📦 Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/Nicholasnas/C14
cd seu-repo
