from rest_framework.request import Request
from rest_framework.throttling import UserRateThrottle


class SendCodeThrottle(UserRateThrottle):
    scope = "send_code"
    rate = "5/min"


class TokenObtainThrottle(UserRateThrottle):
    scope = "token_obtain"
    rate = "5/min"


class TokenObtainEmailThrottle(TokenObtainThrottle):
    def get_ident(self, request: Request) -> str | None:
        return request.data.get("email")
