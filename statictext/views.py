from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import FaqFilter
from .models import StaticText, CompanyDetails, Regulations, FAQ, DropDownClass, FaqCategory
from .serializer import ListStaticTextSerializer, RegulationsSerializer, CompanySerializer, \
    FAQSerializer, DropDownListSerializer, FaqCategorySerializer


# Create your views here.

@extend_schema(tags=["Configurations"], summary="List all Static text.", responses=ListStaticTextSerializer)
class ListAllStaticTextAPIView(ListAPIView):
    queryset = StaticText.objects.all()
    serializer_class = ListStaticTextSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Create a dictionary with unique keys for each title
        title_dict = {item['slug']: item['title'] for item in serializer.data}

        # Wrap the dictionary within a single dictionary
        wrapped_data = {'data': title_dict}

        return Response(wrapped_data)


@extend_schema(tags=["Configurations"], summary="TermsAndCondition.", responses=RegulationsSerializer)
class TermsAndConditionView(APIView):

    def get(self, request, *args, **kwargs):
        regulation = Regulations.objects.filter(id=1).first()

        if regulation:
            serializer = RegulationsSerializer(regulation)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Configurations"], summary="Privacy Policy.", responses=RegulationsSerializer)
class PrivacyPolicyView(APIView):

    def get(self, request, *args, **kwargs):
        regulation = Regulations.objects.filter(id=2).first()

        if regulation:
            serializer = RegulationsSerializer(regulation)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Configurations"], summary="List all company regulations.", responses=RegulationsSerializer)
class AboutUsView(APIView):
    def get(self, request, *args, **kwargs):
        regulation = Regulations.objects.filter(id=3).first()

        if regulation:
            serializer = RegulationsSerializer(regulation)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(tags=["Configurations"], summary="FAQ Category", responses=FaqCategorySerializer)
class FaqCategoryListView(ListAPIView):
    queryset = FaqCategory.objects.filter(is_active=True)
    serializer_class = FaqCategorySerializer


@extend_schema(tags=["Configurations"], summary="FAQ", responses=FAQSerializer)
class FaqView(ListAPIView):
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = FaqFilter
    search_fields = ['question']


@extend_schema(tags=["Configurations"], summary="Company Detail.", responses=CompanySerializer)
class CompanyDetailView(ListAPIView):
    queryset = CompanyDetails.objects.all()
    serializer_class = CompanySerializer
    pagination_class = None


@extend_schema(tags=["Configurations"], summary="Dropdown list.", responses=DropDownListSerializer)
class DropDownList(ListAPIView):
    queryset = DropDownClass.objects.all()
    serializer_class = DropDownListSerializer
    pagination_class = None
