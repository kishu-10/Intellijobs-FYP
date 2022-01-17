from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from vacancy.serializers import *
from rest_framework import status

# Create your views here.
class JobListView(ListAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.filter(
        is_active=True, deadline__gte=date.today()).order_by('-id')

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        print(category)
        if category:
            queryset = Job.objects.filter(
                is_active=True, category=category, deadline__gte=date.today()).order_by('-created_at')
        else:
            queryset = Job.objects.filter(
                is_active=True, deadline__gte=date.today()).order_by('-created_at')

        return queryset

class CategoriesListView(APIView):

    def get(self, request):
        """API to fetch all the Job Categories"""
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)


class JobDetailView(APIView):

    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk)
        except:
            return Response([],
                            status=status.HTTP_400_BAD_REQUEST
                            )
        serializer = JobDetailSerializer(job, context={'request': request})
        return Response({'job_detail': serializer.data})



class CategoryCreateView(APIView):

    def post(self, request):
        serializer = JobCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)