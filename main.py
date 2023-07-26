from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db.postgres import Base, engine
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.services.role import get_all_role




def create_app():
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="VMS API",
            version="1.0.0",
            description="VMS API",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app = FastAPI(
        title="VMS API",
        description="VMS API",
        swagger_ui_parameters={
            # "defaultModelsExpandDepth": -1,
            "displayRequestDuration": True,
            "showExtensions": True,
            "showModels": True
        },
        openapi_schema=custom_openapi
    )
    app.openapi_url = "/openapi.json"
    app.include_router(auth_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")

    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError)->JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "detail": exc.errors()[0]['type']+", "+exc.errors()[0]['msg']+" ("+ exc.errors()[0]['loc'][1]+")"},
    )


@app.get("/")
async def root():
    Base.metadata.create_all(engine)
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
