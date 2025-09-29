import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from c14.main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):

    @patch('c14.main.requests.get')
    def test_valida_cep_mockado(self, mock_get):
        # Criar o objeto para simular o retorno do request get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
                "cep": "37542-000",
                "logradouro": "",
                "complemento": "",
                "unidade": "",
                "bairro": "",
                "localidade": "Estiva",
                "uf": "MG",
                "estado": "Minas Gerais",
                "regiao": "Sudeste",
                "ibge": "3124500",
                "gia": "",
                "ddd": "35",
                "siafi": "4489"
            }
        mock_get.return_value = mock_response
        
        response = client.get("/cep/37542000")
        # Validar se API retornou o esperado
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["cep"], "37542-000")
        self.assertIn("logradouro", data)
        self.assertIn("bairro", data)
        self.assertIn("uf", data)
        self.assertIn("localidade", data)
    
    
    # CEP inexistente
    @patch("c14.main.requests.get")
    def test_cep_inexistente_mockado(self, mock_get):
        # Simulamos o retorno que o ViaCEP da quando o CEP nao existe
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"erro": True}
        mock_get.return_value = mock_response

        # Chamamos a rota da API
        response = client.get("/cep/99999999")

        # A API deve devolver erro 404 com a mensagem
        self.assertEqual(response.status_code, 404)
        self.assertIn("CEP não encontrado", response.text)

    # Erro na API externa 
    @patch("c14.main.requests.get")
    def test_erro_api_externa(self, mock_get):
        # Simulamos que a API externa respondeu com erro 500
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Chamamos a rota da API
        response = client.get("/cep/01001000")

        # A API deve repassar o erro como "Erro na consulta externa"
        self.assertEqual(response.status_code, 500)
        self.assertIn("Erro na consulta externa", response.text)

    def test_valida_cep_retorna_cidade(self):
        response = client.get("/cep/01001000")
        self.assertEqual(response.status_code, 200)
        self.assertIn("logradouro", response.json())

    def test_valida_cep_retorna_json(self):
        response = client.get("/cep/01001000")
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_valida_cep_contem_uf(self):
        response = client.get("/cep/01001000")
        self.assertIn("uf", response.json())
        
    def test_valida_cep_contem_localidade(self):
        response = client.get("/cep/01001000")
        self.assertIn("localidade", response.json())

    def test_valida_cep_data_consistencia(self):
        response = client.get("/cep/01001000")
        data = response.json()
        self.assertEqual(data["cep"], "01001-000")

    def test_cep_with_letters(self):
        response = client.get("/cep/abcd1234")
        self.assertEqual(response.status_code, 400)

    def test_cep_curto_invalido(self):
        response = client.get("/cep/12345")
        self.assertEqual(response.status_code, 400)

    def test_cep_longo_invalido(self):
        response = client.get("/cep/123456789")
        self.assertEqual(response.status_code, 400)

    def test_cep_com_caracteres_especiais(self):
        response = client.get("/cep/12-345-678")
        self.assertEqual(response.status_code, 400)

    def test_cep_inexistente_not_found(self):
        response = client.get("/cep/99999999")
        self.assertEqual(response.status_code, 404)

    def test_cep_nao_encontrado_mensagem(self):
        response = client.get("/cep/99999999")
        self.assertIn("CEP não encontrado", response.text)

    def test_cep_vazio(self):
        response = client.get("/cep/")
        self.assertEqual(response.status_code, 404)

    def test_cep_invalido(self):
        response = client.get("/ceps/01001000")
        self.assertEqual(response.status_code, 404)

    def test_post_not_allowed(self):
        response = client.post("/cep/01001000")
        self.assertEqual(response.status_code, 405)

    def test_varias_chamadas_requests(self):
        for _ in range(5):
            response = client.get("/cep/01001000")
            self.assertEqual(response.status_code, 200)

    def test_response_contem_logradouro_e_bairro(self):
        response = client.get("/cep/01001000")
        keys = response.json().keys()
        self.assertTrue("logradouro" in keys and "bairro" in keys)

    def test_valida_se_retorna_um_dict(self):
        response = client.get("/cep/01001000")
        self.assertIsInstance(response.json(), dict)

    def test_cep_normalizado(self):
        """Mesmo sem hífen deve retornar formatado com hífen"""
        response = client.get("/cep/01001000")
        data = response.json()
        self.assertEqual(data["cep"], "01001-000")

if __name__ == "__main__":
    unittest.main()
    # python -m unittest test_api.py -v