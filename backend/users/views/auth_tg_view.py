import hmac
import hashlib
import urllib.parse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, login
from users.services.invite_service import InviteService
from users.serializers import UserSerializer

User = get_user_model()

class AuthTgView(APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        init_data = request.data.get("init_data")
        if not init_data:
            return Response({"error": "No init_data provided"}, status=400)

        try:
            data = dict(urllib.parse.parse_qsl(init_data, strict_parsing=True))
        except Exception:
            return Response({"error": "Invalid init_data"}, status=400)

        if not self.verify_telegram_auth(data):
            return Response({"error": "Invalid hash"}, status=403)

        # Telegram user
        user_data = eval(data.get("user", "{}"))
        tg_id = user_data.get("id")
        username = user_data.get("username")
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")

        # поиск или создание пользователя
        user = User.objects.filter(tg_id=tg_id).first()
        if not user:
            invite_key = data.get("start_param")
            if invite_key:
                try:
                    user = InviteService.activate_invite(
                        telegram_id=tg_id,
                        input_key=invite_key,
                        telegram_username=username,
                    )
                except Exception:
                    user = None
            if not user:
                user = User.objects.create(
                    username=f"user_{tg_id}",
                    first_name=first_name or "",
                    last_name=last_name or "",
                    tg_id=tg_id,
                )

        # 🔹 создаём Django-сессию
        login(request, user)
        request.session.set_expiry(7 * 24 * 60 * 60)  # сессия живёт неделю

        # определяем роль (менеджер)
        is_manager = user.department and user.department.manager_id == user.id

        serializer = UserSerializer(user, context={"request": request})
        return Response(
            {
                "user": serializer.data,
                "is_manager": is_manager,
                "sessionid": request.session.session_key,
            },
            status=status.HTTP_200_OK,
        )

    # Проверка подписи Telegram
    def verify_telegram_auth(self, data: dict) -> bool:
        received_hash = data.pop("hash", None)
        if not received_hash:
            return False
        check_list = [f"{k}={v}" for k, v in sorted(data.items())]
        data_check_string = "\n".join(check_list)
        secret_key = hashlib.sha256(
            f"WebAppData{settings.TELEGRAM_BOT_TOKEN}".encode()
        ).digest()
        calculated_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()
        return calculated_hash == received_hash
