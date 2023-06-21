from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User as UserType
from .serializers import ChangeEmailSerializer, ProfileSerializer

User = get_user_model()


class ProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserType | AnonymousUser:
        return self.request.user


class FinishedIssuesStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        user = self.request.user
        if isinstance(user, UserType):
            return Response(
                {
                    "finished_count": user.finished_count,
                    "today_finished_count": user.today_finished_count,
                    "reading_speed": user.reading_speed,
                }
            )
        raise exceptions.NotAuthenticated()


class ChangeEmailView(UpdateAPIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> EmailAddress:
        user = self.request.user
        if isinstance(user, UserType):
            return user.emailaddress_set.get(primary=True)
        raise exceptions.NotAuthenticated()
