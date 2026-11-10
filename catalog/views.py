from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Manufacturer, Part
from .serializers import CategorySerializer, ManufacturerSerializer, PartSerializer


def error_response(message, status_code, details=None):
    data = {"error": message}
    if details:
        data["details"] = details
    return Response(data, status=status_code)


class CategoryList(APIView):
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
    def get(self, request):
        parts = Part.objects.all()

        category_id = request.query_params.get('category')
        manufacturer_id = request.query_params.get('manufacturer')
        search = request.query_params.get('search')

        if category_id:
            parts = parts.filter(category_id=category_id)
        if manufacturer_id:
            parts = parts.filter(manufacturer_id=manufacturer_id)
        if search:
            parts = parts.filter(title__icontains=search)

        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response(
            "Invalid data for part creation.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )


class PartDetail(APIView):
    def get_object(self, pk):
        try:
            return Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return None

    def get(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part)
        return Response(serializer.data)

    def put(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return error_response(
            "Invalid data for part update.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )

    def patch(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return error_response(
            "Invalid data for part update.",
            status.HTTP_400_BAD_REQUEST,
            serializer.errors,
        )

    def delete(self, request, pk):
        part = self.get_object(pk)
        if part is None:
            return error_response(f"Part with ID {pk} not found.", status.HTTP_404_NOT_FOUND)
        part.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

