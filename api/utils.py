from datetime import datetime

import pyotp
from api.errors import APIError
from api.models import Rentals, TempUser, UserData, Vehicle, VehicleStation
from api.serializers import UserVehicleSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


def get_temp_user_from_phone_number(phone_number):
    """
    Get or create the TempUser obj and return it.
    Since same user might try to signup multiple times
    without verifying OTP, get_or_create is used.
    """
    temp_user, created = TempUser.objects.get_or_create(
        phone_number=phone_number
    )
    return temp_user


def send_signup_otp(phone_number):
    """
    Send signup otp to user(TempUser).
    Currently just prints the OTP instead of
    sending it.
    """
    temp_user = get_temp_user_from_phone_number(phone_number)
    base32secret3232 = pyotp.random_base32()
    otp = pyotp.TOTP(base32secret3232, interval=60, digits=5)
    print(f"OTP for {phone_number} is {otp.now()}")
    # save the secret so that we can verify OTP against it later
    temp_user.otp_secret = base32secret3232
    temp_user.save()


def verify_signup_otp(phone_number, otp):
    """
    Verify the OTP sent to user(TempUser) trying to signup.
    Temp user is marked as *verified*.
    """
    temp_user = get_temp_user_from_phone_number(phone_number)
    is_verified = pyotp.TOTP(
        temp_user.otp_secret, interval=60, digits=5
    ).verify(otp)
    if is_verified:
        temp_user.is_verified = True
        temp_user.verified_on = datetime.now()
        temp_user.save()
    return is_verified


def get_user_data_from_phone_number(phone_number):
    """
    Return the UserData object for given phone_number
    """
    user_data = UserData.objects.filter(phone_number=phone_number).first()
    if not user_data:
        raise APIError(message="Account with given phone number doesn't exist")
    return user_data


def send_login_otp(phone_number):
    """
    Send login otp to user(User).
    Currently just prints the OTP instead of
    sending it.
    """
    user_data = get_user_data_from_phone_number(phone_number)
    base32secret3232 = pyotp.random_base32()
    otp = pyotp.TOTP(base32secret3232, interval=60, digits=5)
    print(f"Login OTP for {phone_number} is {otp.now()}")
    user_data.otp_secret = base32secret3232
    user_data.save()


def verify_login_otp(phone_number, otp):
    """
    Verify the OTP sent to user(User) trying to signup.
    Temp user is marked as *verified*.
    """
    user_data = get_user_data_from_phone_number(phone_number)
    is_verified = pyotp.TOTP(
        user_data.otp_secret, interval=60, digits=5
    ).verify(otp)
    if is_verified:
        user_data.is_verified = True
        user_data.verified_on = datetime.now()
        user_data.save()
    return is_verified, user_data.user


def create_user(phone_number):
    """
    Create User and UserData for given phone_number
    """
    user = User.objects.create(username=phone_number)
    UserData.objects.get_or_create(user=user, phone_number=phone_number)
    return user


def get_token(user):
    """
    Return token(get_or_create) for given User
    """
    token, is_created = Token.objects.get_or_create(user=user)
    return token.key


def get_rented_vehicle(user):
    """
    Return serliazed rented Vehicle for given user.
    APIError is raised if there are no vehicles for given user.
    """
    try:
        rented_vehicle = Vehicle.objects.get(rented_by=user)
        return UserVehicleSerializer(rented_vehicle).data
    except ObjectDoesNotExist:
        raise APIError(message="You have not rented any vehicle.")


def get_available_vehicles(station_id):
    """
    Return QuerySet of Vehicles in given station_id
    """
    station = VehicleStation.objects.get(id=station_id)
    return Vehicle.objects.filter(current_station=station)


def pick_vehicle(vehicle_id, user):
    """
    "pick" given vehicle (vehicle_id) by given user
    """
    if Vehicle.objects.filter(id=vehicle_id, rented_by=user).exists():
        raise APIError(message="You have already rented this vehicle")
    elif Vehicle.objects.filter(id=vehicle_id, is_rented=True).exists():
        raise APIError(message="This vehicle has already been rented")
    elif Vehicle.objects.filter(rented_by=user).exists():
        raise APIError(message="You have already rented a vehicle")

    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except ObjectDoesNotExist:
        return False, "Unrecognised vehicle"

    if not vehicle.is_rented:
        vehicle.is_rented = True
        vehicle.rented_on = datetime.now()
        vehicle.rented_by = user
        vehicle.save()
        Rentals.objects.create(
            user=user,
            is_rented=True,
            vehicle=vehicle,
            station=vehicle.current_station,
        )
        return True, ""
    return False, "This vehicle is already rented"


def return_vehicle(vehicle_id, station_id, user):
    """
    "pick" given vehicle (vehicle_id) by given user to given station(station_id)
    """
    vehicle = Vehicle.objects.get(id=vehicle_id)

    if vehicle.is_rented and vehicle.rented_by == user:
        vehicle.is_rented = False
        vehicle.rented_on = None
        vehicle.current_station = VehicleStation.objects.get(id=station_id)
        vehicle.rented_by = None
        vehicle.save()
        Rentals.objects.create(
            user=user,
            is_rented=False,
            vehicle=vehicle,
            station=vehicle.current_station,
        )
        return True, ""
    else:
        return False, "Wrong vehicle"
