import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes.delete import router as delete_router
from app.routes.imports import router

app = FastAPI()
app.include_router(router)
app.include_router(delete_router)
app.add_exception_handler(RequestValidationError, JSONResponse)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc) -> JSONResponse:
    print(exc)
    return JSONResponse(
        status_code=400,
        content={}
    )


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
