import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Category, Manufacturer, Part
from .serializers import CategorySerializer, ManufacturerSerializer, PartSerializer
from .permissions import IsAdminOrReadOnly

logger = logging.getLogger(__name__)


def error_response(message, status_code, details=None):
    data = {"error": message}
    if details:
        data["details"] = details
    return Response(data, status=status_code)


class CategoryList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response(
            "Invalid data for category creation.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )


class CategoryDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response(f"Category with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response(f"Category with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return error_response(
            "Invalid data for category update.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response(f"Category with ID {pk} not found.", status.HTTP_404_NOT_FOUND)

        parts_count = category.parts.count()
        if parts_count > 0:
            return error_response(
                f"Cannot delete category '{category.name}' because it has {parts_count} related part(s).",
                status.HTTP_409_CONFLICT,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ManufacturerList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        manufacturers = Manufacturer.objects.all().order_by('name')
        serializer = ManufacturerSerializer(manufacturers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response(
            "Invalid data for manufacturer creation.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )


class ManufacturerDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Manufacturer.objects.get(pk=pk)
        except Manufacturer.DoesNotExist:
            return None

    def get(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response(f"Manufacturer with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = ManufacturerSerializer(manufacturer)
        return Response(serializer.data)

    def put(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response(f"Manufacturer with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = ManufacturerSerializer(manufacturer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return error_response(
            "Invalid data for manufacturer update.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )

    def delete(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response(f"Manufacturer with ID {pk} not found.", status.HTTP_404_NOT_FOUND)

        parts_count = manufacturer.parts.count()
        if parts_count > 0:
            return error_response(
                f"Cannot delete manufacturer '{manufacturer.name}' because it has {parts_count} related part(s).",
                status.HTTP_409_CONFLICT,
            )
        manufacturer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PartList(APIView):
    permission_classes = [IsAdminOrReadOnly]

    @extend_schema(
        summary='List PC parts',
        description='Returns a list of PC parts.',
        auth=[],
        parameters=[
            OpenApiParameter(name='category', type=int, description='Filter by category ID'),
            OpenApiParameter(name='manufacturer', type=int, description='Filter by manufacturer ID'),
            OpenApiParameter(name='search', type=str, description='Search parts by title (case-insensitive)'),
        ],
        responses={200: PartSerializer(many=True)},
    )
    def get(self, request):
        parts = Part.objects.all()

        category_id = request.query_params.get('category')
        manufacturer_id = request.query_params.get('manufacturer')
        search = request.query_params.get('search')

        logger.debug(
            f"Listing parts (category={category_id}, manufacturer={manufacturer_id}, search={search})",
        )
        try:
            if category_id:
                parts = parts.filter(category_id=category_id)
            if manufacturer_id:
                parts = parts.filter(manufacturer_id=manufacturer_id)
            if search:
                parts = parts.filter(title__icontains=search)
        except ValueError:
            logger.error(f"Part with category ID {category_id}, manufacture ID {manufacturer_id} not found.")
            return error_response("Not correct search query.", status.HTTP_400_BAD_REQUEST)

        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Create a PC part',
        description='Creates a new PC part. Requires admin privileges.',
        request=PartSerializer,
        responses={
            201: PartSerializer,
            400: {'description': 'Invalid data'},
            401: {'description': 'Authentication credentials were not provided'},
            403: {'description': 'Admin privileges required'},
        },
        examples=[
            OpenApiExample(
                'Create CPU example',
                value={
                    'title': 'Ryzen 5 5600',
                    'category': 1,
                    'manufacturer': 1,
                    'price': '5500.00',
                    'rating': '4.80',
                    'specs': {'cores': 6, 'threads': 12},
                    'description': '6-core processor',
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            part = serializer.save()
            logger.info(
                f"Part created: id={part.id}, title={part.title}, user_id={request.user.id}"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning(
            f"Part creation validation failed: user_id={request.user.id}, fields={list(serializer.errors.keys())}"
        )
        return error_response(
            "Invalid data for part creation.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )


class PartDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, pk):
        try:
            return Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return None

    @extend_schema(
        summary='Retrieve a PC part',
        auth=[],
        responses={
            200: PartSerializer,
            404: {'description': 'Part not found'},
        },
    )
    def get(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            logger.warning(f"Part not found: id={pk}")
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part)
        return Response(serializer.data)

    @extend_schema(
        summary='Update a PC part',
        description='Full update of a PC part. Requires admin privileges.',
        request=PartSerializer,
        responses={
            200: PartSerializer,
            400: {'description': 'Invalid data'},
            401: {'description': 'Authentication credentials were not provided'},
            403: {'description': 'Admin privileges required'},
            404: {'description': 'Part not found'},
        },
    )
    def put(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            logger.warning(f"Part not found for update: id={pk}")
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, data=request.data)
        if serializer.is_valid():
            updated_part = serializer.save()
            logger.info(
                f"Part updated: id={updated_part.id}, user_id={request.user.id}"
            )
            return Response(serializer.data)
        logger.warning(
            f"Part update validation failed: id={pk}, user_id={request.user.id}, fields={list(serializer.errors.keys())}"
        )
        return error_response(
            "Invalid data for part update.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )

    @extend_schema(
        summary='Partially update a PC part',
        description='Partial update of a PC part. Requires admin privileges.',
        request=PartSerializer,
        responses={
            200: PartSerializer,
            400: {'description': 'Invalid data'},
            401: {'description': 'Authentication credentials were not provided'},
            403: {'description': 'Admin privileges required'},
            404: {'description': 'Part not found'},
        },
    )
    def patch(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            logger.warning(f"Part not found for partial update: id={pk}")
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, data=request.data, partial=True)
        if serializer.is_valid():
            updated_part = serializer.save()
            logger.info(
                f"Part partially updated: id={updated_part.id}, user_id={request.user.id}"
            )
            return Response(serializer.data)
        logger.warning(
            f"Part partial update validation failed: id={pk}, user_id={request.user.id}, fields={list(serializer.errors.keys())}"
        )
        return error_response(
            "Invalid data for part update.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )

    @extend_schema(
        summary='Delete a PC part',
        description='Deletes a PC part. Requires admin privileges.',
        responses={
            204: None,
            401: {'description': 'Authentication credentials were not provided'},
            403: {'description': 'Admin privileges required'},
            404: {'description': 'Part not found'},
        },
    )
    def delete(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            logger.warning(f"Part not found for deletion: id={pk}")
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        part.delete()
        logger.info(f"Part deleted: id={pk}, user_id={request.user.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

