from fastapi import Request
from fastapi.responses import JSONResponse
import json
from .main import app
from src.handlers.cognito_post_confirmation import handler as post_confirmation_handler

AWARE_USER_SUB = "515b85a0-c0d1-7039-9a5e-e5e71cdc0e83"
@app.on_event("startup")
async def seed_data():
    print("🌱 Seeding fake user data...")

    fake_event = {
        "request": {
            "userAttributes": {
                "email": "cristianangulonova@gmail.com",
                "sub": AWARE_USER_SUB,
            }
        }
    }

    try:
        post_confirmation_handler(fake_event, None)
        print("✅ Fake user data created.")
    except Exception as e:
        print("⚠️ Error creating fake data:", e)

@app.middleware("http")
async def handle_options_requests(request: Request, call_next):
    if request.method == "OPTIONS":
        return JSONResponse(
            status_code=200,
            content=None,
            headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type, Range",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Expose-Headers": "Content-Range",
            },
        )
    return await call_next(request)


@app.middleware("http")
async def add_claims(request: Request, call_next):
    event = {
        "accountId": "491085388486",
        "apiId": "xada36wixk",
        "authorizer": {
            "claims": {
                "aud": "63ekpgtus62gh8eof9kqmcinfu",
                "auth_time": "1746381609",
                "cognito:username": AWARE_USER_SUB,
                "email": "cristianangulonova@gmail.com",
                "email_verified": "true",
                "event_id": "d1fd4da7-6ce5-4d2c-b81c-fd58bd8c0f23",
                "exp": "1746385209",
                "iat": "1746381609",
                "iss": "https://cognito-idp.us-east-2.amazonaws.com/us-east-2_9pPQodJ9a",
                "jti": "a1b4ecc9-76f2-4557-9bbc-1e53f78bb271",
                "origin_jti": "7bc4cf7a-4405-443b-a473-762192a28a10",
                "sub": AWARE_USER_SUB,
                "token_use": "id",
            },
            "scopes": None,
        },
        "domainName": "internal.dev.estructura.com",
        "domainPrefix": "internal",
        "httpMethod": "GET",
        "identity": {"sourceIp": "127.0.0.1", "userAgent": "LocalTest/1.0"},
        "path": "/dev/request-context",
        "protocol": "HTTP/1.1",
        "requestId": "KDewUgCgiYcEP8A=",
        "requestTime": "04/May/2025:18:00:20 +0000",
        "requestTimeEpoch": 1746381620809,
        "resourceId": "ANY /{proxy+}",
        "resourcePath": "/{proxy+}",
        "stage": "dev",
    }

    request.headers.__dict__["_list"].append(
        (b"x-amzn-request-context", json.dumps(event).encode())
    )
    return await call_next(request)