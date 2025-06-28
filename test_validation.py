#!/usr/bin/env python3

import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.brain_agriculture.schemas.brain_agriculture import ProdutorCreate

async def test_validation():
    print("Iniciando teste de validação...")
    
    # Executar o evento de startup
    await app.router.startup()
    
    with TestClient(app) as client:
        # Testar a rota de criação de produtor
        produtor_data = {
            "cpf": "123.456.789-00",
            "nomeprodutor": "João Silva"
        }
        
        print(f"Dados do produtor: {produtor_data}")
        
        # Verificar se os dados são válidos
        try:
            produtor = ProdutorCreate(**produtor_data)
            print(f"Schema válido: {produtor}")
        except Exception as e:
            print(f"Erro na validação do schema: {e}")
        
        # Fazer a requisição
        response = client.post("/api/v1/produtores", json=produtor_data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
    
    # Executar o evento de shutdown
    await app.router.shutdown()

if __name__ == "__main__":
    asyncio.run(test_validation()) 