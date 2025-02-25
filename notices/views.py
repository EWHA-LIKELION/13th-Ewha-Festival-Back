from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .models import OperationNotice
from .serializers import OperationNoticeSerializer
# Create your views here.

class OperationNoticeView(APIView):
    def get(self, request, *args, **kwargs):
        # 공지 목록 가져오기 (ListView)
        operation_notices = OperationNotice.objects.all().order_by('-created_at')
        serializer = OperationNoticeSerializer(operation_notices, many=True)
        return Response({"message": "운영 공지 조회 성공!",
                         "data": serializer.data},
                        status=HTTP_200_OK)
 
