from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.users import router as users_router
from schemas.shared_schemas import ErrorResponse, ErrorBase

app = FastAPI(title="Auth App")

app.include_router(users_router, prefix="/api")

@app.exception_handler(HTTPException)
def http_exception_error_handler(request: Request, exc: HTTPException):
    error = ErrorBase(message=str(exc.detail))
    return JSONResponse(
        status_code=exc.status_code, content=ErrorResponse(errors=[error]).model_dump()
    )

def handle_validation(validation_error) -> ErrorBase:
    message = f"{validation_error['msg']} '{'.'.join(validation_error['loc'][1:])}'"
    return ErrorBase(message=message)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [handle_validation(err) for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(errors=errors).model_dump(),
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)