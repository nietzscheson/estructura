import json


class ExceptionHandler:
    def __call__(self, e):
        # exception to status code mapping goes here...
        status_code = 400
        return {"statusCode": status_code, "body": json.dumps(str(e))}
