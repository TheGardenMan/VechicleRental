from django.contrib.auth.models import User
from django.db import models


class TempUser(models.Model):
    phone_number = models.CharField(max_length=16, unique=True)
    otp_secret = models.CharField(max_length=32)
    is_verified = models.BooleanField(default=False)
    verified_on = models.DateTimeField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    # auto_now updates the given field whenever a model is "save()"d
    modified_on = models.DateTimeField(auto_now=True)


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    phone_number = models.CharField(max_length=16)
    otp_secret = models.CharField(max_length=32, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class VehicleStation(models.Model):
    station_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)


class Vehicle(models.Model):
    model = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="vehicle_creator"
    )

    # where the vehicle currently was
    current_station = models.ForeignKey(
        VehicleStation, null=True, db_index=True, on_delete=models.DO_NOTHING
    )

    # if this vehicle is currently rented
    is_rented = models.BooleanField(default=False, db_index=True)
    rented_by = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    rented_on = models.DateTimeField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)


# "log" of all rents and returns
class Rentals(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # if True, this transaction about
    # "rented" event. Else "returned" event
    is_rented = models.BooleanField(default=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)

    # which station does this vehicle rented from / returned to

    station = models.ForeignKey(VehicleStation, on_delete=models.DO_NOTHING)
    # when this "event" (rent or return) happened
    created_on = models.DateTimeField(auto_now_add=True)
