import base64
from django.contrib.auth.models import User
from realtors.models import Realtor
from faker import Faker

import django
import os
import random
import requests

import json

from django.contrib.auth import get_user_model
from slugify import slugify

import base64


User = get_user_model()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realest_estate.settings')

django.setup()



def set_house():
    fake = Faker(['en_US'])

    for i in range(0, 50):

        response = requests.get(
            "https://pixabay.com/api/?key=22161424-08421d893c81fc01d6d419611&q=house+architecture&image_type=photo&per_page=100")

        jsn = response.json()

        url = jsn["hits"][i]["webformatURL"]

        address = fake.street_address()
        
        data = dict(
            realtor=random.randint(2, Realtor.objects.count()),
            slug=slugify(address),
            title=fake.street_name() + "House",
            address=address,
            city=fake.city(),
            state=fake.country(),
            zipcode=fake.postcode(),
            description=fake.paragraph(nb_sentences=7),
            sale_type="For Sale" if fake.pybool() else "For Rent",
            price=random.randint(10, 50) * 10 ** 4,
            bedrooms=random.randint(2, 7),
            bathrooms=random.randint(2, 7),
            sqft=random.randint(10, 20) * 10**2,
            open_house=fake.pybool(),
            photo_main=str(base64.b64encode(
                requests.get(url).content).decode('ASCII'))
        )
        json_object = json.dumps(data, indent=4)

        res = requests.post("http://127.0.0.1:8000/api/listings/", headers={
                            'Content-Type': 'application/json', 'charset': 'utf-8'}, data=json_object)
        data = res.json()

        print("data", data)

def set_realtors():

    fake = Faker(['en_US'])

    for i in range(0, 10):

        response = requests.get(
            "https://pixabay.com/api/?key=22161424-08421d893c81fc01d6d419611&q=people+face&image_type=photo")

        jsn = response.json()

        url = jsn["hits"][i]["webformatURL"]

        data = dict(
            name = fake.name(),
            photo = str(base64.b64encode(requests.get(url).content).decode('ASCII')),
            description=fake.paragraph(nb_sentences=10),
            phone=fake.phone_number(),
            email=fake.email(),
            top_seller=fake.pybool(),
        )


        json_object = json.dumps(data, indent=4)

        res = requests.post("http://127.0.0.1:8000/api/realtors/", headers={
                            'Content-Type': 'application/json', 'charset': 'utf-8'}, data=json_object)
        data = res.json()

        print("data", data)





        