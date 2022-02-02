from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from extensions.models import Checklist
from extensions.serializers import ChecklistSerializer


class ChecklistCatalog(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        checklists_user = Checklist.objects.filter(event=pk).filter(viewers=request.user.id)
        print(checklists_user)
        serializer_data = ChecklistSerializer(checklists_user, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
