from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api import utils
from api.errors import APIError
from api.models import Vehicle, VehicleStation
from api.serializers import (
    UserVehicleSerializer,
    UserVehicleStationSerializer,
    VehicleSerializer,
    VehicleStationSerializer,
)


@api_view(["POST"])
def admin_login(request):
    """Return token for given admin user after verifying credentials"""
    data = request.data
    try:
        user = User.objects.get(
            username=data.get("username"), is_superuser=True
        )
        if user.check_password(data.get("password")):
            token = utils.get_token(user)
            return Response({"token": token, "message": "Login successful"})
        raise APIError(message="Invalid credentials")
    except ObjectDoesNotExist:
        raise APIError(message="Invalid credentials")


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def admin_vehicle_station(request):
    """Create or get VehicleStation"""
    if request.method == "POST":

        vehiclestation_seriliazer = VehicleStationSerializer(
            data={"created_by": request.user.id, **request.data}
        )
        if vehiclestation_seriliazer.is_valid():
            vehiclestation = vehiclestation_seriliazer.save()
            return Response(
                {"data": vehiclestation_seriliazer.data}, status=201
            )
        raise APIError(message=vehiclestation_seriliazer.errors)
    elif request.method == "GET":
        # get one VehicleStation
        station_id = request.query_params.get("station_id", None)
        if station_id:
            try:
                vehiclestation = VehicleStation.objects.get(id=station_id)
                serializer = VehicleStationSerializer(vehiclestation)
                return Response({"data": serializer.data})
            except ObjectDoesNotExist:
                raise APIError(
                    message="Given VehicleStation not found", status=404
                )
        else:
            # get all VehicleStation
            vehiclestations = VehicleStation.objects.all()
            serializer = VehicleStationSerializer(vehiclestations, many=True)
            return Response({"data": serializer.data})


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def admin_vehicle(request):
    """Create or Get Vehicle"""
    if request.method == "POST":
        data = request.data
        vehicle_serializer = VehicleSerializer(
            data={"created_by": request.user.id, **data}
        )
        if vehicle_serializer.is_valid():
            vehicle = vehicle_serializer.save()
            return Response({"data": vehicle_serializer.data}, status=201)
        raise APIError(message=vehicle_serializer.errors)

    elif request.method == "GET":
        # get one Vehicle
        vehicle_id = request.query_params.get("vehicle_id", None)
        if vehicle_id:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            serializer = VehicleSerializer(vehicle)
            return Response({"data": serializer.data})
        else:
            # get all Vehicle
            vehicles = Vehicle.objects.all()
            serializer = VehicleSerializer(vehicles, many=True)
            return Response({"data": serializer.data})


@api_view(["GET", "POST"])
def user_signup(request):
    """
    User signup. Get or verify OTP
    """
    if request.method == "POST":
        data = request.data
        phone_number = data.get("phone_number", None)
        otp = data.get("otp", None)
        if not phone_number or not otp:
            raise APIError(message="phone_number or otp missing")

        if User.objects.filter(username=phone_number).exists():
            raise APIError(
                message="Account with given phone_number already exists"
            )

        is_verified = utils.verify_signup_otp(phone_number, otp)

        if is_verified:
            with transaction.atomic():
                user = utils.create_user(phone_number)
                token = utils.get_token(user)
                return Response(
                    {"token": token, "message": "Account created"}, status=201
                )
        else:
            raise APIError(message="Verification failed")

    elif request.method == "GET":
        phone_number = request.query_params.get("phone_number", None)
        if not phone_number:
            raise APIError(message="phone_number missing")
        if User.objects.filter(username=phone_number).exists():
            raise APIError(
                message="Account with given phone_number already exists"
            )
        utils.send_signup_otp(phone_number)
        return Response({"message": f"OTP has been sent to {phone_number}"})


@api_view(["GET", "POST"])
def user_login(request):
    """
    User login. Get or verify OTP
    """
    if request.method == "POST":
        data = request.data
        phone_number = data.get("phone_number", None)
        otp = data.get("otp", None)
        if not phone_number or not otp:
            raise APIError(message="phone_number or otp missing")
        is_verified, user = utils.verify_login_otp(phone_number, otp)

        if is_verified:
            token = utils.get_token(user)
            return Response({"token": token})

    elif request.method == "GET":
        phone_number = request.query_params.get("phone_number", None)
        if not phone_number:
            raise APIError(message="phone_number missing")
        utils.send_login_otp(phone_number)
        return Response({"message": f"OTP has been sent to {phone_number}"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_vehicle_station(request):
    # Get all the vehicle stations
    vehiclestations = VehicleStation.objects.all()
    serializer = UserVehicleStationSerializer(vehiclestations, many=True)
    return Response({"data": serializer.data})


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_vehicle(request):
    if request.method == "GET":
        current = request.query_params.get("current", None)
        station_id = request.query_params.get("station_id", None)
        if current:
            # get details of currently rented vehicle
            rented_vehicle = utils.get_rented_vehicle(request.user)
            return Response({"rented_vehicle": rented_vehicle})
        elif station_id:
            # get details of vehicles  that are available for
            # rent in given station.
            available_vehicles = utils.get_available_vehicles(station_id)
            serializer = UserVehicleSerializer(available_vehicles, many=True)
            return Response(
                {
                    "available_vehicles": serializer.data,
                    "station_id": station_id,
                }
            )
        else:
            raise APIError(message="station_id or current flag missing")
    elif request.method == "PUT":
        # pick or return a vehicle
        data = request.data
        vehicle_id = data.get("vehicle_id", None)
        action = data.get("action", None)

        if not vehicle_id or not action:
            raise APIError(message="vehicle_id or action missing")

        if action == "pick":
            picked, error = utils.pick_vehicle(vehicle_id, request.user)
            if picked:
                return Response({"message": "Vehicle picked"})
            raise APIError(message=error)

        elif action == "return":
            station_id = data.get("station_id", None)
            if not station_id:
                return APIError(message="station_id missing")
            returned, error = utils.return_vehicle(
                vehicle_id, station_id, request.user
            )
            if returned:
                return Response({"message": "Vehicle returned"})
            raise APIError(message=error)
