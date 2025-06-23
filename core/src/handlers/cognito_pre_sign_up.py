from src.container import MainContainer




def handler(event, context):
    main_container = MainContainer()

    cognito = main_container.cognito_client()
    user_pool_id = event["userPoolId"]
    email = event["request"]["userAttributes"].get("email")
    trigger_source = event["triggerSource"]

    if email:
        response = cognito.list_users(
            UserPoolId=user_pool_id, Filter=f'email = "{email}"', Limit=1
        )

        if response["Users"]:
            raise Exception("This user already exists...")

    if trigger_source == "PreSignUp_ExternalProvider":
        event["response"]["autoConfirmUser"] = True
        event["response"]["autoVerifyEmail"] = True

    return event
