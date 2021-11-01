import os
import uvicorn
from fastapi import FastAPI, status
from app.adapters.database.coursesModel import Base
from app.adapters.database.database import engine
from app.adapters.http import collaboratorController, courseController, suscriptionController
from app.core.logger import logger

Base.metadata.create_all(bind=engine)

# Create app with FAST API
app = FastAPI(debug=True)

logger.info("Starting Course-Service")


@app.get('/ping', status_code=status.HTTP_200_OK)
async def root():
    logger.warn("This is an testing endpoint, not intended for productive environment")
    return "pong"

app.include_router(courseController.router, prefix="/api")
app.include_router(suscriptionController.router, prefix="/api")
app.include_router(collaboratorController.router, prefix="/api")

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    logger.info("Using port: " + port)
    uvicorn.run(app, host='0.0.0.0', port=port)
