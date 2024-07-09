from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import (
    PlazoFijoReadSerializer, PlazoFijoWriteSerializer,
    EntidadReadSerializer, EntidadWriteSerializer,
    OperacionReadSerializer, OperacionWriteSerializer,
    )
from .models import PlazoFijo, Entidad, Operacion
from .utils import generar_lista_fechas

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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        serializer = PlazoFijoWriteSerializer(plazo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        plazo.delete()
        return Response({'detail': 'Correctly deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def EntidadView(request, id=None, id_entidad=None):
    if request.method == 'GET':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidades = Entidad.objects.filter(plazo=plazo)
        serializer = EntidadReadSerializer(entidades, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        serializer = EntidadWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(plazo=plazo)
            plazo.num_entidades += 1
            plazo.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidad = get_object_or_404(Entidad, pk=id_entidad, plazo=plazo)
        serializer = EntidadWriteSerializer(entidad, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidad = get_object_or_404(Entidad, pk=id_entidad, plazo=plazo)
        entidad.delete()
        nuevo_monto = plazo.calcular_monto()
        plazo.monto = nuevo_monto
        plazo.num_entidades -= 1
        plazo.save()
        return Response({'detail': 'Correctly deleted'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def OperacionView(request, id=None, id_entidad=None):
    if request.method == 'GET':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        if id_entidad:
            entidad = get_object_or_404(Entidad, pk=id_entidad, plazo=plazo)
            operaciones = Operacion.objects.filter(entidad=entidad)
            serializer = OperacionReadSerializer(operaciones, many=True)
            return Response(serializer.data)
        operaciones = Operacion.objects.filter(plazo=plazo)
        serializer = OperacionReadSerializer(operaciones, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not id_entidad:
            return Response({'detail': 'You must provide an entity id'}, status=status.HTTP_400_BAD_REQUEST)

        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        entidad = get_object_or_404(Entidad, pk=id_entidad, plazo=plazo)
        serializer = OperacionWriteSerializer(data=request.data)
        if serializer.is_valid():
            # Evitar que se registren operaciones antes de las existentes
            fecha = serializer.validated_data.get('fecha')
            operaciones_existentes = Operacion.objects.filter(entidad=entidad, fecha__gt=fecha, tipo__in=['Deposito', 'Retiro'])
            if operaciones_existentes.exists():
                return Response({'detail': 'An operation cannot be recorded before existing operations.'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el monto actual de la entidad
            ultima_operacion = Operacion.objects.filter(entidad=entidad, fecha=fecha)
            if ultima_operacion.exists():
                monto = ultima_operacion.last().nuevo_monto
            else:
                monto = 0

            # Verificar actualizaciones de monto
            tipo = serializer.validated_data.get('tipo')
            if tipo == 'Retiro':
                if monto < serializer.validated_data.get('monto'):
                    return Response({'detail': 'Not enough money'}, status=status.HTTP_400_BAD_REQUEST)
                monto -= serializer.validated_data.get('monto')
            else:
                monto += serializer.validated_data.get('monto')


            # Eliminar los intereses viejos y crear la operacion
            intereses_viejos = Operacion.objects.filter(entidad=entidad, tipo='Interes', fecha__gt=fecha).delete()
            serializer.save(entidad=entidad, plazo=plazo, nuevo_monto=monto)

            # Generar los intereses nuevos
            entidad.monto = monto
            lista_fechas = generar_lista_fechas(fecha)
            for fecha in lista_fechas:
                entidad.generar_interes(fecha)
            entidad.save()

            # Actualizar el monto del plazo
            plazo.monto = plazo.calcular_monto()
            plazo.save()

            # Retornar la operacion
            return Response(serializer.data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ! ELIMINAR PROXIMAMENTE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def InteresesView(request, id=None):
    if request.method == 'POST':
        plazo = get_object_or_404(PlazoFijo, pk=id, user=request.user)
        plazo.calcular_intereses()
        return Response({'detail': 'Interests calculated'})