from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import (
    PlazoFijoReadSerializer, PlazoFijoWriteSerializer,
    EntidadReadSerializer, EntidadWriteSerializer
    )
from .models import PlazoFijo, Entidad

# Create your views here.
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def PlazoFijoView(request, id=None):
    if request.method == 'GET':
        if id:
            plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
            serializer = PlazoFijoReadSerializer(plazo)
            return Response(serializer.data)
        else:
            plazos = PlazoFijo.objects.filter(user=request.user)
            serializer = PlazoFijoReadSerializer(plazos, many=True)
            return Response(serializer.data)

    if request.method == 'POST':
        serializer = PlazoFijoWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'PATCH':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        serializer = PlazoFijoWriteSerializer(plazo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        plazo.delete()
        return Response({'detail': 'Correctly deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def EntidadView(request, id=None, id_entidad=None):
    if request.method == 'GET':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidades = Entidad.objects.filter(plazo_fijo=plazo)
        serializer = EntidadReadSerializer(entidades, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        serializer = EntidadWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(plazo_fijo=plazo)
            plazo.num_entidades += 1
            plazo.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'PATCH':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidad = get_object_or_404(Entidad, pk=id_entidad)

        if entidad.plazo_fijo != plazo:
            return Response({'detail': 'Entidad does not belong to the plazo'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EntidadWriteSerializer(entidad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidad = get_object_or_404(Entidad, pk=id_entidad)

        if entidad.plazo_fijo != plazo:
            return Response({'detail': 'Entity does not belong to the plazo'}, status=status.HTTP_400_BAD_REQUEST)

        entidad.delete()
        nuevo_monto = plazo.calcular_monto()
        plazo.monto = nuevo_monto
        plazo.num_entidades -= 1
        plazo.save()
        return Response({'detail': 'Correctly deleted'})