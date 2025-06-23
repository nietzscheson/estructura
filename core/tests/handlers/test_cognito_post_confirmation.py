from src.handlers.cognito_post_confirmation import handler


def test_cognito_post_confirmation(post_confirmation_event, mock_s3_uploader):
    result = handler(post_confirmation_event, None)

    assert result["response"] == {}
