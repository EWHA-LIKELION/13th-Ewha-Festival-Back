from django.shortcuts import render, get_object_or_404
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import GuestBookSerializer
from booths.models import Booth
from .models import *

# Create your views here.

class GuestBookView(views.APIView):
    # post(방명록 작성), get(only 방명록 조회)
    serializer_class = GuestBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, booth_id): #방명록 작성 
        '''
        if not request.user.is_authenticated:
            return Response({'message': '로그인한 유저만 방명록을 작성할 수 있습니다.', 
                             'data': serializer.data}, 
                            status=HTTP_401_UNAUTHORIZED)
        '''
        try:
            booth= Booth.objects.get(pk=booth_id)
        except Booth.DoesNotExist:
            return Response({'message':'부스를 찾을 수 없습니다.'},
                            status=HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data, 
                                           context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(booth=booth)
            return Response({'message': '방명록 작성 성공!', 'data': serializer.data}, 
                            status=HTTP_200_OK)
        else:
            return Response({'message': '방명록 작성 실패!', 'data': serializer.errors}, 
                            status=HTTP_400_BAD_REQUEST)
        
    def get(self, request, booth_id):
        try:
            booth= Booth.objects.get(pk=booth_id)
        except Booth.DoesNotExist:
            return Response({'message':'부스를 찾을 수 없습니다.'},
                            status=HTTP_404_NOT_FOUND)
        
        contents = GuestBook.objects.filter(booth=booth)
        serializers = GuestBookSerializer(contents,
                                          many=True,
                                          context={'request': request})
        return Response({'message': '부스 방명록 조회 성공!', 
                         'data': serializers.data}, 
                         status=HTTP_200_OK)

class GuestBookDeleteView(views.APIView):
    serializer_class = GuestBookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, booth_id, guestbook_id):  # 방명록 삭제
        '''
        if not request.user.is_authenticated:
            return Response({'message': '로그인한 유저만 방명록을 삭제할 수 있습니다.'}, 
                            status=HTTP_401_UNAUTHORIZED)
        '''
        try:
            guestbook = GuestBook.objects.get(pk=guestbook_id, booth_id=booth_id)
        except GuestBook.DoesNotExist:
            return Response({'message': '해당 방명록을 찾을 수 없습니다.'}, 
                            status=HTTP_404_NOT_FOUND)

        if guestbook.user != request.user:
            return Response({'message': '본인이 작성한 방명록만 삭제할 수 있습니다.'}, 
                            status=HTTP_403_FORBIDDEN)

        guestbook.delete()
        return Response({'message': '방명록 삭제 성공!'}, 
                        status=HTTP_204_NO_CONTENT)