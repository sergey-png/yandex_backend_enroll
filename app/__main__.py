from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routes.delete import router as delete_router
from app.routes.imports import router as imports_router
from app.routes.nodes import router as nodes_router
from app.routes.sales import router as sales_router

app = FastAPI()
app.include_router(imports_router)
app.include_router(delete_router)
app.include_router(nodes_router)
app.include_router(sales_router)

app.add_exception_handler(RequestValidationError, JSONResponse)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Any, exc: str) -> JSONResponse:
    print(exc)
    return JSONResponse(status_code=400, content={})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
