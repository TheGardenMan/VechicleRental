import base64
from io import BytesIO

import qrcode
from api.models import Vehicle, VehicleStation
from rest_framework import serializers


class VehicleStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleStation
        fields = ["id", "station_name", "location", "created_by"]


class VehicleSerializer(serializers.ModelSerializer):
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            "id",
            "model",
            "number",
            "created_by",
            "current_station",
            "is_rented",
            "rented_by",
            "qr_code",
        ]

    def get_qr_code(self, obj):
        qr_code_image = qrcode.make(str({"vehicle_id": obj.id}))
        buffered = BytesIO()
        qr_code_image.save(buffered, format="JPEG")
        qrcode_b64 = base64.b64encode(buffered.getvalue())
        return qrcode_b64


class UserVehicleStationSerializer(serializers.ModelSerializer):
    """
    VehicleStation serializer for normal (non-Admin) user.
    Hides some fields that should not be available to user
    """

    class Meta:
        model = VehicleStation
        fields = ["id", "station_name", "location"]


class UserVehicleSerializer(serializers.ModelSerializer):
    """
    Vehicle serializer for normal (non-Admin) user.
    Hides some fields that should not be available to user
    """

    class Meta:
        model = Vehicle
        fields = ["id", "model", "number", "rented_on"]
