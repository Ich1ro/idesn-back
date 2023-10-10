"""main"""

import os
import uvicorn
from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import MultiTenantAzureAuthorizationCodeBearer
from endpoints import images, templates, text, quizzes, questions


APP_CLIENT_ID = os.environ["APP_CLIENT_ID"]

app = FastAPI()

azure_scheme = MultiTenantAzureAuthorizationCodeBearer(
    app_client_id=APP_CLIENT_ID,
    scopes={
        f'api://{APP_CLIENT_ID}/openid': 'openid',
        f'api://{APP_CLIENT_ID}/email': 'email',
        f'api://{APP_CLIENT_ID}/offline_access': 'offline_access',
    },
    validate_iss=False
)

app.openapi()

dependencies = [Security(azure_scheme, scopes=['email'])]

"""
to authorize endpoint add dependencies
app.include_router(endpoint.router, dependencies=dependencies)
"""
app.include_router(images.router)
app.include_router(templates.router)
app.include_router(text.router)
app.include_router(quizzes.router)
app.include_router(questions.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()


def main() -> None:
    """entry point"""
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
