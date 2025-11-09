# backend/users/views/invite_view.py
from rest_framework import viewsets, permissions, decorators, response, status
from users.serializers import InviteKeySerializer
from users.services.invite_service import InviteService
from users.models import Department

class InviteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        invites = InviteService.list_invites()
        return response.Response(InviteKeySerializer(invites, many=True).data)

    def retrieve(self, request, pk=None):
        invite = InviteService.get_invite_detail(pk)
        return response.Response(InviteKeySerializer(invite).data)

    def create(self, request):
        department = Department.objects.get(id=request.data['department'])
        if request.user != department.manager and not request.user.is_staff:
            return response.Response({'error': 'No permission'}, status=403)

        invite = InviteService.create_invite(
            created_by=request.user,
            department=department,
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            telegram_username=request.data.get('telegram_username')
        )
        return response.Response(InviteKeySerializer(invite).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        InviteService.delete_invite(pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def activate(self, request):
        try:
            user = InviteService.activate_invite(
                telegram_id=request.data.get('telegram_id'),
                input_key=request.data.get('invite_key'),
                telegram_username=request.data.get('telegram_username')
            )
        except Exception as e:
            return response.Response({'error': str(e)}, status=400)
        return response.Response({'success': True, 'user_id': user.id, 'username': user.username}, status=201)

