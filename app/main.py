import os
import uvicorn
from fastapi import FastAPI, status
#from app.adapters.database.database import engine
from app.core.logger import logger

# Create app with FAST API
app = FastAPI(debug=True)

logger.info("Starting User-Service")


@app.get('/ping', status_code=status.HTTP_200_OK)
async def root():
    logger.warn("This is an testing endpoint, not intended for productive environment")
    return "pong"

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)
    logger.info("Using port: " + port)
    uvicorn.run(app, host='0.0.0.0', port=port)
