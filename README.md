# Parking Reservaion System.

## Getting Started

First clone the repository from Github and switch to the new directory:

```
https://github.com/SagyanXOXO/Parking-Reservation-System.git
```

Activate the virtualenv for your project.

Install project dependencies:

```
pip install -r requirements.txt
```

Then simply apply the migrations:

```
python manage.py makemigrations
python manage.py migrate
```

You can now run the development server:

```
python manage.py runserver
```

## Overview

In this project, Customers can book a single car park for a single day. The parking has 4 bays numbered from 1-4 inclusively. Therefore, the assumption was that any booking that was completed for a day meant that the booking lasted for that entire day.

A customer record required two essential information i.e name and license plate. Since, license plate are issued to be completely unique they were saved as such. No any authentication strategy was applied in the project.

To complete a booking, the following conditions must me met.

* The parking bay is available.
* Booking must be made at least 24 hrs in advance.
* Same customer cannot book a bay in the park if the customer has already made a booking on the same day.
* Bookings cannot be made in the past.

After the booking is made, it would be best to only allow the customer to update or cancel the booking but since no authentication was used in the project this was not accomplished.

## Running tests

    > python manage.py test

## API Documentation

## List all api roots

> GET /api/v1/

## Customer

### List all customers

    > GET /api/v1/customer/

Lists all registered customers.

### Create a new customer

    > POST /api/v1/customer/

| Parameter     | Type   | Description |
| ------------- | ------ | ----------- |
| name          | String | Required    |
| license_plate | String | Required    |

### Update a customer

    > PUT /api/v1/customer/[int:id](int:id)

| Parameter     | Type   | Description |
| ------------- | ------ | ----------- |
| name          | String | Required    |
| license_plate | String | Required    |

### Get customer detail

    > GET /api/v1/customer/[int:id](int:id)

Get customer detail.

### Delete a customer

    > DELETE /api/v1/customer/[int:id](int:id)

Deletes a customer.

## Booking

### List all bookings

    > GET /api/v1/booking/

| Parameter    | Type   | Description |
| ------------ | ------ | ----------- |
| booking_date | string | Optional    |
| customer     | int    | Optional    |

Lists all valid bookings.
Can be filtered on the basis on date and customer.

### Create a new booking

    > POST /api/v1/booking/

| Parameter    | Type   | Description |
| ------------ | ------ | ----------- |
| booking_date | string | Required    |
| customer     | int    | Required    |
| parking_bay  | int    | Required    |

### Update a booking

    > PUT /api/v1/booking/[int:id](int:id)

| Parameter    | Type   | Description |
| ------------ | ------ | ----------- |
| booking_date | string | Required    |
| customer     | int    | Required    |
| parking_bay  | int    | Required    |

### Get booking detail

    > GET /api/v1/booking/[int:id](int:id)

Get booking detail.

### Delete a booking

    > DELETE /api/v1/booking/[int:id](int:id)

Deletes a customer.

## Parking

### List all free as well as reserved bays for the given date in the car park.

    > GET /api/v1/booking/[str:date](str:date)

### Example Response

'''

    {
        "free": [
            1,
            2,
            3,
            4
        ],
        "reserved": []
    }

'''
