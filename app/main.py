import os

import uvicorn
from fastapi import FastAPI, status

from app.adapters.database.coursesModel import Base
from app.adapters.database.database import engine
from app.adapters.http import (categoriesController, collaboratorController,
                               courseController, inscriptionController,
                               suscriptionController)
from app.core.logger import logger

Base.metadata.create_all(bind=engine)

# Create app with FAST API
app = FastAPI(debug=True)

logger.info("Starting Course-Service")


@app.get('/ping', status_code=status.HTTP_200_OK)
async def root():
    logger.warning("This is an testing endpoint, not intended for productive environment")
    return "pong"

app.include_router(courseController.router, prefix="/api")
app.include_router(suscriptionController.router, prefix="/api")
app.include_router(collaboratorController.router, prefix="/api")
app.include_router(inscriptionController.router, prefix="/api")
app.include_router(categoriesController.router, prefix="/api")

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    logger.info("Using port: " + port)
    uvicorn.run(app, host='0.0.0.0', port=port)
