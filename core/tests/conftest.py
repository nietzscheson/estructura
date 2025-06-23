import json
import os
import subprocess
import uuid
from unittest.mock import MagicMock, patch
import copy

import pytest
from dependency_injector.providers import Singleton
from faker import Faker
from httpx import ASGITransport, AsyncClient

from src.args import StructureArgs
from src.container import MainContainer
from src.main import app

from fastapi import Request
from tests.factories import UserFactory


@pytest.fixture
def faker():
    return Faker("es_MX")


AWARE_USER_SUB = "515b85a0-c0d1-7039-9a5e-e5e71cdc0e83"


@pytest.fixture
async def user_sub_aware():
    return AWARE_USER_SUB


@pytest.fixture
async def user_aware(user_sub_aware, db):
    user = UserFactory.create(sub=user_sub_aware, email="test@example.com")

    db.add(user)
    db.commit()

    return user


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
                "email": "estructura@nietzscheson.com",
                "email_verified": "True",
                "event_id": "d1fd4da7-6ce5-4d2c-b81c-fd58bd8c0f23",
                "exp": "1746385209",
                "iat": "1746381609",
                "iss": "https://cognito-idp.us-east-2.amazonaws.com/us-east-1_XIgvM8ria",
                "jti": "a1b4ecc9-76f2-4557-9bbc-1e53f78bb271",
                "origin_jti": "7bc4cf7a-4405-443b-a473-762192a28a10",
                "sub": AWARE_USER_SUB,
                "token_use": "id",
            },
            "scopes": None,
        },
        "domainName": "internal.estructura.nietzscheson.com",
        "domainPrefix": "internal",
        "httpMethod": "GET",
        "identity": {
            "accessKey": None,
            "accountId": None,
            "apiKey": None,
            "apiKeyId": None,
            "caller": None,
            "cognitoAuthenticationProvider": None,
            "cognitoAuthenticationType": None,
            "cognitoIdentityId": None,
            "cognitoIdentityPoolId": None,
            "sourceIp": "187.150.71.117",
            "user": None,
            "userAgent": "HTTPie/3.2.4",
            "userArn": None,
        },
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
        (
            b"x-amzn-request-context",
            json.dumps(event).encode(),
        )
    )
    response = await call_next(request)
    return response


@pytest.fixture
async def http_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
        await client.aclose()


@pytest.fixture
def apply_migrations(scope="function"):
    subprocess.run(["alembic", "downgrade", "base"])
    subprocess.run(["alembic", "upgrade", "head"])
    yield
    subprocess.run(["alembic", "downgrade", "base"])


@pytest.fixture
def main_container():
    container = MainContainer()

    return container


@pytest.fixture
def db(main_container, apply_migrations):
    session = main_container.session()

    with session() as session:
        yield session


@pytest.fixture
def texttract_jobs_ids():
    return (
        "3595c3a4b1523a868282a5deacc3143083ab25279090be6e6c4097908d4608ea",
        "080524a6e5a4c2c42dbf4a5c86b51aa06e49d963582b85565708b14a5c8ecea6",
        "642d0e9bc3f5b59182ca257a4eb5c97422c095037278b0a8d22fb685c5689b89",
    )


@pytest.fixture
def mock_textract_start(texttract_jobs_ids):
    with patch("src.services.textract.Textract.start", autospec=True) as mock_client:
        mock_client.return_value = uuid.uuid4().hex
        yield mock_client


@pytest.fixture
def receipts_files():
    base_path = "tests/files/receipts/"
    documents = set()
    for file in sorted(os.listdir(base_path)):
        if file.startswith("receipt_") and file.endswith((".jpeg", ".jpg")):
            file_path = os.path.join(base_path, file)
            with open(file_path, "rb") as f:
                documents.add(f.read())
    return documents


@pytest.fixture
def mock_s3_uploader():
    with patch("src.services.uploader.Uploader.__call__", autospec=True) as mock_upload:
        mock_upload.return_value = uuid.uuid4().hex
        yield mock_upload
        
@pytest.fixture
def mock_s3_get():
    with patch("src.services.uploader.Uploader.get", autospec=True) as mock_upload:
        mock_upload.return_value = {}
        yield mock_upload


@pytest.fixture
def default_structure(main_container):
    settings = main_container.settings()
    return settings["DEFAULT_STRUCTURE"]

@pytest.fixture
def template_fixture(main_container, default_structure):
    
    template_repository = main_container.template_repository()

    def _():
        template_create_args = StructureArgs(
            name="Receipt", structure=default_structure
        )

        template = template_repository.create(args=template_create_args)

        return template

    return _


@pytest.fixture
def cognito_pre_sig_up_fixture_event(user_aware):
    return {
        "userPoolId": "us-east-1_XIgvM8ria",
        "triggerSource": "PreSignUp_SignUp",
        "request": {
            "userAttributes": {"email": user_aware.email, "sub": user_aware.sub}
        },
        "response": {},
    }


@pytest.fixture
def post_confirmation_event(user_aware):
    return {
        "request": {
            "userAttributes": {
                "email": user_aware.email,
                "sub": user_aware.sub,
            }
        },
        "response": {},
    }


@pytest.fixture
def mock_cognito_client(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_users.return_value = {"Users": [{"Username": "test@example.com"}]}

    monkeypatch.setattr(
        "src.container.MainContainer.cognito_client",
        Singleton(lambda: mock_client),
    )

    return mock_client


@pytest.fixture
def stripe_client_subscription_expected_response():
    return {
        "adaptive_pricing": None,
        "after_expiration": None,
        "allow_promotion_codes": None,
        "amount_subtotal": 499,
        "amount_total": 499,
        "automatic_tax": {
            "enabled": False,
            "liability": None,
            "provider": None,
            "status": None,
        },
        "billing_address_collection": None,
        "cancel_url": "https://my.estructura.nietzscheson.com/#/subscriptions",
        "client_reference_id": None,
        "client_secret": None,
        "collected_information": {"shipping_details": None},
        "consent": None,
        "consent_collection": None,
        "created": 1750190738,
        "currency": "usd",
        "currency_conversion": None,
        "custom_fields": [],
        "custom_text": {
            "after_submit": None,
            "shipping_address": None,
            "submit": None,
            "terms_of_service_acceptance": None,
        },
        "customer": "cus_SW81XnYTpiWBmF",
        "customer_creation": None,
        "customer_details": {
            "address": None,
            "email": "test@example.com",
            "name": None,
            "phone": None,
            "tax_exempt": "none",
            "tax_ids": None,
        },
        "customer_email": None,
        "discounts": [],
        "expires_at": 1750277138,
        "id": "cs_test_a1S1FEf58k2XSdNyoJfin6uDRt9FTRTKvmgjMBq36NKsDFkUyGynqBplEW",
        "invoice": None,
        "invoice_creation": None,
        "livemode": False,
        "locale": None,
        "metadata": {},
        "mode": "subscription",
        "object": "checkout.session",
        "payment_intent": None,
        "payment_link": None,
        "payment_method_collection": "always",
        "payment_method_configuration_details": None,
        "payment_method_options": {"card": {"request_three_d_secure": "automatic"}},
        "payment_method_types": ["card"],
        "payment_status": "unpaid",
        "permissions": None,
        "phone_number_collection": {"enabled": False},
        "recovered_from": None,
        "saved_payment_method_options": {
            "allow_redisplay_filters": ["always"],
            "payment_method_remove": "disabled",
            "payment_method_save": None,
        },
        "setup_intent": None,
        "shipping_address_collection": None,
        "shipping_cost": None,
        "shipping_options": [],
        "status": "open",
        "submit_type": None,
        "subscription": None,
        "success_url": "https://my.estructura.nietzscheson.com/#/subscriptions",
        "total_details": {"amount_discount": 0, "amount_shipping": 0, "amount_tax": 0},
        "ui_mode": "hosted",
        "url": "https://pay.estructura.nietzscheson.com/c/pay/cs_test_a1S1FEf58k2XSdNyoJfin6uDRt9FTRTKvmgjMBq36NKsDFkUyGynqBplEW#fidkdWxOYHwnPyd1blpxYHZxWjA0V1J3V0JCbk8wMjBTV1BLTXZVV2JhcTBgMlxAM3ZzYkpcM1JkYEddbVxPfU8wNHJuXV9nVHxwf0FjbTxSXUhpfHZcbWJrQkhQbjByUEdkQWNKXENBPX1XNTU0bW5PQVZ0bycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl",
        "wallet_options": None,
    }


@pytest.fixture
def mock_stripe_checkout_session_create(stripe_client_subscription_expected_response):
    with patch("stripe.checkout.Session.create", autospec=True) as mock_client:
        mock_client.return_value = stripe_client_subscription_expected_response
        yield mock_client


@pytest.fixture
def stripe_customer_create_expected_response():
    base_response = {
        "address": None,
        "balance": 0,
        "created": 1750190726,
        "currency": None,
        "default_source": None,
        "delinquent": False,
        "description": None,
        "discount": None,
        "email": "test@example.com",
        "id": "cus_SW81XnYTpiWBmF",
        "invoice_prefix": "XP7AD5CJ",
        "invoice_settings": {
            "custom_fields": None,
            "default_payment_method": None,
            "footer": None,
            "rendering_options": None,
        },
        "livemode": False,
        "metadata": {"account_id": "3e6282328a5f44a6bc929d1163cefe34"},
        "name": None,
        "next_invoice_sequence": 1,
        "object": "customer",
        "phone": None,
        "preferred_locales": [],
        "shipping": None,
        "tax_exempt": "none",
        "test_clock": None,
    }

    def _(overrides):
        response = copy.deepcopy(base_response)
        if overrides:
            from deepmerge import always_merger

            return always_merger.merge(response, overrides)
        return response

    with patch("stripe.Customer.create", autospec=True) as mock_client:
        mock_client.return_value = {}
        yield mock_client


@pytest.fixture
def queuer_expected_response():
    return {
        "MD5OfMessageBody": "c2e25722bb98e80d554fe7afd98bcd23",
        "MessageId": "26c383e0-f3f5-404c-b2c1-5492ccbf2d14",
        "ResponseMetadata": {
            "RequestId": "1693db74-0906-53ba-a4df-bba5052ac872",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amzn-requestid": "1693db74-0906-53ba-a4df-bba5052ac872",
                "date": "Sat, 21 Jun 2025 19:37:16 GMT",
                "content-type": "application/x-amz-json-1.0",
                "content-length": "106",
                "connection": "keep-alive",
            },
            "RetryAttempts": 0,
        },
    }


@pytest.fixture
def mock_queuer(queuer_expected_response):
    with patch("src.services.queuer.Queuer.__call__", autospec=True) as mock_client:
        mock_client.return_value = queuer_expected_response
        yield mock_client





@pytest.fixture
def textract_event_expected_response():
    return {
        "Records": [
            {
                "messageId": "0626a308-e160-4f15-bacd-4ce2b46c6822",
                "receiptHandle": "AQEBXra0F+8S2q5RC3rfptaEEme3pCc2nUBMWHmLazrTgppXU5RE4XOpwfqX5VQABSsQ1oD+2kDvVKOn3i9+PMvt25VU7G0+t9e8ZX/TOJSIW4mTXMPwgVqDFCovwS/2tIoWwoAlw82zARz88dErjtoPFlbYwr+b5/XHd1qfziGm2DRxvl/xYLPI/zvVDWGmViM77HhtwT+dFj5DAKmynSISzMGwBSofuMaLLdolHfYHlfFe2IxktFG222bL5SZMMBmKspTekIMraGlHmobYfLVlq8LWkP2FfdMRsYVZT0pNPiff8liJliTu+ioFt9gXzE/Tpq/saIeD/v2Jm6phXcm1oIh65hXO1bxo6h61UisuTq0DtUnJU+dGk0RgwHXli/lDqDp5WzGxwNxvqHdWPaWZp4T2J47FO474d1we1wizxcuVFC+WJxKfDY16hOXFtKEHVT+BVn6Psajwp99kf/bFGQ==",
                "body": '{\n  "Type" : "Notification",\n  "MessageId" : "339c428d-da63-5b6b-9251-229fd5a12b04",\n  "TopicArn" : "arn:aws:sns:us-east-1:491085388486:AmazonTextract-structfy-default-start-document-text-detection-successful",\n  "Message" : "{\\"JobId\\":\\"8892031365854c059956dd8050314b1c5895a765e1a94b4b93c623924feff169\\",\\"Status\\":\\"SUCCEEDED\\",\\"API\\":\\"StartDocumentTextDetection\\",\\"Timestamp\\":1738018178884,\\"DocumentLocation\\":{\\"S3ObjectName\\":\\"43da2626ea72479ea3d591533db08ed2.pdf\\",\\"S3Bucket\\":\\"structfy-default-files\\"}}",\n  "Timestamp" : "2025-01-27T22:49:38.932Z",\n  "SignatureVersion" : "1",\n  "Signature" : "ecdZJTx+7jWPk8jx45MEc/p/tDyM7Ifp6dcK/xzDx32cvdFESFL/sWZwKRT9aV1plCOSi09cFD5SE/jUvkbpwgh4ESE6RpvpL/2Yk5EQJgG+LqpFx+fm7++UFJMeFu0ZjrbI329OXVTcFGlAgBBhEwMtjfsIwr5rTASW7xC8Cfox9Pmvcg1A8rEdiVUi6RddX7WcceKhg7fLLCFQVqRd8zKml8TNJu+4GeDGf550fRT5f2AbvKkmBjpQj/gudcx2NkOrIpfJ1X781iCsX6gRrC6DRk3ba62PhatIvLniIU5cX2opNIrzvCwH6p7OBJR1HnpF9KYLPjSwP1lPSSffww==",\n  "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-9c6465fa7f48f5cacd23014631ec1136.pem",\n  "UnsubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:491085388486:AmazonTextract-structfy-default-start-document-text-detection-successful:7a114d29-e8f0-481f-b202-161f1f7eb7ef"\n}',
                "attributes": {
                    "ApproximateReceiveCount": "2090",
                    "SentTimestamp": "1738018178964",
                    "SenderId": "AIDAIT2UOQQY3AUEKVGXU",
                    "ApproximateFirstReceiveTimestamp": "1738018178965",
                },
                "messageAttributes": {},
                "md5OfBody": "20635d8db4e7a0d1eef657a0b8eef482",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:491085388486:structfy-default-start-document-text-detection-successful",
                "awsRegion": "us-east-1",
            }
        ]
    }
    


@pytest.fixture
def textract_text_detection_expected_response():
    return "EL PIBITO FRANCISCO JOSE RODRIGUEZ INTERIAN RFC: :ROIF670220E45 AV 135 M 72 L45 SM 321 CANCUN QUINTANA ROO MEXIC 0 CP 77560 LUGAR DE EXPEDICION FOLIO:27060 ORDEN:6 FECHA: 19/03/2025 08:50:46 AM CAJERO:CAJER@ CANT. DESCRIPCION IMPORTE 2 TORTA COCHINITA $100.00 SUBTOTAL: $100.00 TOTAL: $100.00 SON:CIEN PESOS 00/100 M.N. FORMAS DE PAGO CREDITO: $100.00 ESTE NO ES UN COMPROBANTE FISCAL ***SOFT RESTAURANT V10 ***"

@pytest.fixture
def mock_textract_text_detection(textract_text_detection_expected_response):
    with patch("src.services.textract.Textract.text_detection", autospec=True) as mock_client:
        mock_client.return_value = textract_text_detection_expected_response
        yield mock_client
        