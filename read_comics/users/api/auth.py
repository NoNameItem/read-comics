from dj_rest_auth.jwt_auth import JWTCookieAuthentication


class Auth(JWTCookieAuthentication):
    def authenticate(self, request):
        if not request.session.session_key:
            return None
        return super(Auth, self).authenticate(request)
