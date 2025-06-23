import json

from fastapi import Request


async def current_cognito_claims(request: Request) -> str:
    try:
        event = json.loads(request.headers.get("x-amzn-request-context", {}))

        authorizer = event.get("authorizer", {})

        if "claims" in authorizer and isinstance(authorizer["claims"], dict):
            return authorizer["claims"]

        return authorizer.get("custom_claims", {})

    except Exception as e:
        print(e)
        raise e
