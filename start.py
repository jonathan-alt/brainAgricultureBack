#!/usr/bin/env python3
"""
Script de inicialização da aplicação Brain Agriculture Backend
"""

import uvicorn
from app.main import app
from app.core.config import config

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=True,
        log_level="info"
    ) 