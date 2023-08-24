from django.contrib.auth import login

from accounts.models import User


class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            login(request, user)

        response = self.get_response(request)
        return response
