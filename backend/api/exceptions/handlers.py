from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from api.exceptions import ResourceAlreadyExists
from api.exceptions import ResourceNotFound
from api.exceptions import DomainException


def add_exception_handlers(app):
    @app.exception_handler(ResourceNotFound)
    async def not_found_handler(request: Request, exc: ResourceNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ResourceAlreadyExists)
    async def already_exists_handler(request: Request, exc: ResourceAlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    # fallback generic handler
    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"},
        )
