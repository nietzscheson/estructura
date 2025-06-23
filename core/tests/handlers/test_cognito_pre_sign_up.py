import pytest
from src.handlers.cognito_pre_sign_up import handler

def test_handler_email_already_exists(cognito_pre_sig_up_fixture_event, mock_cognito_client):
   with pytest.raises(Exception, match="This user already exists..."):
       handler(cognito_pre_sig_up_fixture_event, None)

def test_handler_auto_confirm_on_federation(cognito_pre_sig_up_fixture_event, mock_cognito_client):
   cognito_pre_sig_up_fixture_event["triggerSource"] = "PreSignUp_ExternalProvider"
   cognito_pre_sig_up_fixture_event["request"]["userAttributes"]["email"] = "new@example.com"

   mock_cognito_client.list_users.return_value = {"Users": []}

   result = handler(cognito_pre_sig_up_fixture_event, None)
   assert result["response"]["autoConfirmUser"] is True
   assert result["response"]["autoVerifyEmail"] is True
#
#
