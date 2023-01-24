Please check `setup.md` for setup instructions

# Introduction

	In this application,Admins can 
        Create Vehicle Stations and Vehicles.(Admin signup functionality is not implemented. Admin a/c should be created using Django’s createsuperuser command.)
        See Vehicle stations
        See Vehicles and their QR

    Users can 
        Signup/login using phone number and OTP. ( OTP sending functionality is not implemented.OTP is printed on the console which can be used to verify.)
        See all Vehicle Stations
        See all Vehicles
        Pick a vehicle
        Return Vehicle to any Vehicle Station


# API documentation

 

# Admin APIs

# Admin Login API

Endpoint: /admin_login

Method: POST

Description:
This API is used for admin login. It takes in a JSON object in the request body with the following parameters:

    username (string) - The username of the admin user.
    password (string) - The password of the admin user.

It returns a JSON object with the following parameters:

    token (string) - A token that can be used for authentication.
    message (string) - The message "Login successful" if the login was successful, otherwise "Invalid credentials".

Example Request Body:
{
"username": "admin",
"password": "password123"
}

Example Response:
{
    "token": "ecd0d84a94f832f03d1db0c9fd9420e4a53c4800",
    "message": "Login successful"
}




# Admin Vehicle Station API

Endpoint: /admin_vehicle_station

Method: GET, POST

Description:
This API is used for creating or getting Vehicle Station by admin. It requires authentication and user should be admin.

Method: POST

    Takes in a JSON object in the request body with the following parameters:
        station_name (string) - The name of the station.
        location (string) - The address of the station.
    Returns a JSON object with the following parameters:
        data (object) - The details of the created VehicleStation
    If validation fails, it raises an error with the validation error message.

Method: GET

    Takes in query parameters with the following parameter:
        station_id (integer) - The id of the station to be retrieved.
    Returns a JSON object with the following parameters:
        data (object/array) - The details of the retrieved VehicleStation/VehicleStations
    If the station_id is not provided, it returns all the VehicleStations.
    If the provided station_id is not found, it raises an error with message "Given VehicleStation not found" and status code 404

Example Request Body (POST):
{
    "station_name": "Jaga station",
    "location": "Coimbatore"
}

Example Response (POST):
{
    "data": {
        "id": 3,
        "station_name": "Jaga station",
        "location": "Coimbatore",
        "created_by": 1
    }
}

Example Request (GET):
/admin_vehicle_station?station_id=1

Example Response (GET):
{
    "data": {
        "id": 1,
        "station_name": "Jaga station",
        "location": "Coimbatore",
        "created_by": 1
    }
}
}


# Admin Vehicle API

Endpoint: /admin_vehicle

Method: GET, POST

Description:
This API is used for creating or getting Vehicle by admin. It requires authentication and user should be admin.

Method: POST

    Takes in a JSON object in the request body with the following parameters:
        number (string) - The registration number of the vehicle.
        model (string) - The model of the vehicle.
        current_station (integer) - ID of the station to which this vehicle should be assigned

    Returns a JSON object with the following parameters:
        data (object) - The details of the created vehicle
    If validation fails, it raises an error with the validation error message.

Method: GET

    Takes in query parameters with the following parameter:
        vehicle_id (integer) - The id of the vehicle to be retrieved.
    Returns a JSON object with the following parameters:
        data (object/array) - The details of the retrieved vehicle/vehicles
    If the vehicle_id is not provided, it returns all the vehicles.
    If the provided vehicle_id is not found, it raises an error with message "Given vehicle not found" and status code 404

Example Request Body (POST):
{
    "model":"Tata hello",
    "number":"TN42W1234",
    "current_station":1
}

Example Response (POST):
{
    "data": {
        "id": 2,
        "model": "Tata hello",
        "number": "TN42W1234",
        "created_by": 1,
        "current_station": 1,
        "is_rented": false,
        "rented_by": null,
        "qr_code": "base64 encoded QR code"
        }
}

Example Request (GET):
/admin_vehicle?vehicle_id=1

Example Response (GET):
{
    "data": {
        "id": 1,
        "model": "Tata hello",
        "number": "TN42W1234",
        "created_by": 1,
        "current_station": 1,
        "is_rented": false,
        "rented_by": null,
        "qr_code": "base64 encoded QR code"
        }
}

Note: Sample data in QR code: {"vehicle_id": 1}





# User APIs

# User Signup API

Endpoint: /user_signup

Method: GET, POST

Description:
This API is used for user signup. It allows user to get or verify OTP for phone number.

Method: POST

    Takes in a JSON object in the request body with the following parameters:
        phone_number (string) - The phone number of the user.
        otp (string) - The OTP received by the user.
    Returns a JSON object with the following parameters:
        token (string) - A token that can be used for authentication.
        message (string) - The message "Account created" if the signup was successful, otherwise "Verification failed"
    If phone_number or otp is missing, it raises an error with message "phone_number or otp missing"
    If the given phone_number already exists, it raises an error with message "Account with given phone_number already exists"
    If the otp is not verified, it raises an error with message "Verification failed"

    Note: OTP is not sent but printed to the console. 

Method: GET

    Takes in query parameter with the following parameter:
        phone_number (string) - The phone number of the user.
    Returns a JSON object with the following parameters:
        message (string) - The message "OTP has been sent to phone_number_here" if the OTP is sent successfully.
    If phone_number is missing, it raises an error with message "phone_number missing"
    If the given phone_number already exists, it raises an error with message "Account with given phone_number already exists"

    Note: OTP is not sent but printed to the console. 


Example Request Body (POST):
{
    "phone_number":"911234567893",
    "otp":"55815"
}

Example Response (POST):
{
"token": "ecd0d84a94f832f03d1db0c9fd9420e4a53c4800",
"message": "Account created"
}

Example Request (GET):
/user_signup?phone_number=1234567890

Example Response (GET):
{
"message": "OTP has been sent to 1234567890"
}


# User Login API

Endpoint: /user_login

Method: GET, POST

Description:
This API is used for user login. It allows user to get or verify OTP for phone number.

Method: POST

    Takes in a JSON object in the request body with the following parameters:
        phone_number (string) - The phone number of the user.
        otp (string) - The OTP received by the user.
    Returns a JSON object with the following parameters:
        token (string) - A token that can be used for authentication.
    If phone_number or otp is missing, it raises an error with message "phone_number or otp missing"
    If the otp is not verified, it raises an error with message "Verification failed"

Method: GET

    Takes in query parameter with the following parameter:
        phone_number (string) - The phone number of the user.
    Returns a JSON object with the following parameters:
        message (string) - The message "OTP has been sent to {phone_number}" if the OTP is sent successfully.
    If phone_number is missing, it raises an error with message "phone_number missing"

Example Request Body (POST):
{
    "phone_number":"911234567893",
    "otp":"78120"
}

Example Response (POST):
{
    "token": "66a49312d58ac6dd1fd5a9acf073fc36cf098cb8"
}


Example Request (GET):
    /user_login/?phone_number=911234567893


Example Response (GET):

{
    "message": "OTP has been sent to 911234567893"
}



# User Vehicle Station API

Endpoint: /user_vehicle_station

Method: GET

Description:
This API is used to retrieve all the vehicle stations. The API requires authentication and can only be accessed by an authenticated user.

It returns a JSON object with the following parameters:
    data (list) - A list of all the vehicle stations. Each object in the list contains the parameters as shown in example response

Example Request:
    GET /user_vehicle_station

Example Response:
{
    "data": [
        {
            "id": 1,
            "station_name": "Jaga station",
            "location": "Coimbatore"
        },
        {
            "id": 2,
            "station_name": "Jaga station",
            "location": "Coimbatore"
        },
        {
            "id": 3,
            "station_name": "Jaga station",
            "location": "Coimbatore"
        }
    ]
}


# User Vehicle API

Endpoint: /user_vehicle

Method: GET,PUT

Description:
    This API is used for picking or returning a vehicle by user and for getting vehicles available in a station.

Example GET requests:
    /user_vehicle/?current=1
        returns details about user's currently picked vehicle

    /user_vehicle/?station_id=1
        returns details about vehicles available in a station
    

Example PUT requests:
    Given vehicle will be `picked` by user
    body
        `{
            "vehicle_id": 1,
            "action": "pick"
        }`

    Given vehicle will be returned to given station

    body
        `{
            "vehicle_id": 2,
            "station_id": 1,
            "action": "return"
        }`



Note: Postman collection has been attached. Set `admin_token` and  `user_token` to respective values after importing