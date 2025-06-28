#!/usr/bin/env python3

import asyncio
from app.main import app

async def test_container():
    print("Iniciando teste do container...")
    
    # Verificar se o container existe antes do startup
    print(f"Container antes do startup: {hasattr(app, 'container')}")
    
    # Executar o evento de startup
    await app.router.startup()
    
    # Verificar se o container foi criado
    print(f"Container após startup: {hasattr(app, 'container')}")
    
    if hasattr(app, 'container'):
        print(f"Service disponível: {hasattr(app.container, 'brain_agriculture_service')}")
        if hasattr(app.container, 'brain_agriculture_service'):
            service = app.container.brain_agriculture_service()
            print(f"Service criado: {service}")
    
    # Executar o evento de shutdown
    await app.router.shutdown()

if __name__ == "__main__":
    asyncio.run(test_container()) 