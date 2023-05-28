from django.contrib.auth import get_user_model
User = get_user_model()

class BadRequest:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        response['Access-Control-Allow-Headers'] = "*"
        response['Access-Control-Allow-Methods'] = "*"
        response['Access-Control-Allow-Origin'] = "*"
        return response


