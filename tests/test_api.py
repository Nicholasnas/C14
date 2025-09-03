import unittest
from fastapi.testclient import TestClient
from c14.main import app

client = TestClient(app)

class TestAPI(unittest.TestCase):

    def test_valid_cep_returns_city(self):
        response = client.get("/cep/01001000")
        self.assertEqual(response.status_code, 200)
        self.assertIn("logradouro", response.json())

    def test_valid_cep_returns_json(self):
        response = client.get("/cep/01001000")
        self.assertEqual(response.headers["content-type"], "application/json")

    def test_valid_cep_contains_uf(self):
        response = client.get("/cep/01001000")
        self.assertIn("uf", response.json())

    def test_valid_cep_contains_localidade(self):
        response = client.get("/cep/01001000")
        self.assertIn("localidade", response.json())

    def test_valid_cep_data_consistency(self):
        response = client.get("/cep/01001000")
        data = response.json()
        self.assertEqual(data["cep"], "01001-000")

    def test_cep_with_letters(self):
        response = client.get("/cep/abcd1234")
        self.assertEqual(response.status_code, 400)

    def test_cep_too_short(self):
        response = client.get("/cep/12345")
        self.assertEqual(response.status_code, 400)

    def test_cep_too_long(self):
        response = client.get("/cep/123456789")
        self.assertEqual(response.status_code, 400)

    def test_cep_with_special_chars(self):
        response = client.get("/cep/12-345-678")
        self.assertEqual(response.status_code, 400)


    def test_non_existent_cep(self):
        response = client.get("/cep/99999999")
        self.assertEqual(response.status_code, 404)

    def test_non_existent_cep_message(self):
        response = client.get("/cep/99999999")
        self.assertIn("CEP não encontrado", response.text)

    # ---- Robustez da API ----
    def test_empty_cep(self):
        response = client.get("/cep/")
        self.assertEqual(response.status_code, 404)

    def test_invalid_path(self):
        response = client.get("/ceps/01001000")
        self.assertEqual(response.status_code, 404)

    def test_post_not_allowed(self):
        response = client.post("/cep/01001000")
        self.assertEqual(response.status_code, 405)

    def test_many_requests(self):
        for _ in range(5):
            response = client.get("/cep/01001000")
            self.assertEqual(response.status_code, 200)

    def test_response_has_expected_keys(self):
        response = client.get("/cep/01001000")
        keys = response.json().keys()
        self.assertTrue("logradouro" in keys and "bairro" in keys)

    def test_response_is_dict(self):
        response = client.get("/cep/01001000")
        self.assertIsInstance(response.json(), dict)

    def test_cep_normalization(self):
        """Mesmo sem hífen deve retornar formatado com hífen"""
        response = client.get("/cep/01001000")
        self.assertEqual(response.json()["cep"], "01001-000")

if __name__ == "__main__":
    unittest.main()
