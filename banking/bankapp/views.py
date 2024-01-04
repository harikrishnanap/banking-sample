from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import Branches
from rest_framework import status
from .serializers import BranchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
def index(request):
    return render(request, 'home.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')

# # @api_view(['GET'])
# def get_branches(request, district_id):
    
#     try:
#         branches = Branches.objects.filter(district_id=district_id)
#         print('branches ', branches)
#         serializer = BranchSerializer(branches, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
#     except Branches.DoesNotExist:
#         return Response({"message": "District not found"}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

@api_view(['GET'])
def get_branches(request, district_id):
    try:
        branches = Branches.objects.filter(district_id=district_id)
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')
    except Branches.DoesNotExist:
        return Response({"message": "District not found"}, status=status.HTTP_404_NOT_FOUND, content_type='application/json')