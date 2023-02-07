import base64
from django.contrib.auth.models import User
from listings.serializers import ListingSerializer
from accounts.models import UserAccount
from faker import Faker

import django
import os
import random
import requests

from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realest_estate.settings')

django.setup()

# HOME_IMAGES = [
#     'https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
#     'https://www.bhg.com/thmb/0Fg0imFSA6HVZMS2DFWPvjbYDoQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/white-modern-house-curved-patio-archway-c0a4a3b3-aa51b24d14d0464ea15d36e05aa85ac9.jpg',
#     'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRs_DL2uFBGanoPOo9VFQdRUfmb8N-mHxf268eqUmhkXtM9_r0qBGaYBsZt4pGCtiwd4Og&usqp=CAU'
#     'https://t3.ftcdn.net/jpg/05/62/86/46/360_F_562864607_3Q3F4auiwahzzZPBJSpEGJ1xjV00Ii3w.jpg'
#     'https://res.cloudinary.com/brickandbatten/image/upload/c_scale,w_464,h_324,dpr_2/f_auto,q_auto/v1641000863/wordpress_assets/22826-ModContemporary-Accents_w-GauntletGray-a-ok.jpg?_i=AA'
# ]


def set_house():
    fake = Faker(['en_US'])

    for i in range(0, 5):

        response = requests.get(
            "https://pixabay.com/api/?key=22161424-08421d893c81fc01d6d419611&q=house+architecture&image_type=photo")

        jsn = response.json()

        url = jsn["hits"][i]["webformatURL"]

        # def get_as_base64():

        #     return base64.b64encode(requests.get(url).content)

        address = fake.street_address()
        data = dict(
            realtor=random.randint(1, User.objects.count()),
            slug=slugify(address),
            title=fake.street_name() + "House",
            address=address,
            city=fake.city(),
            state=fake.country(),
            zipcode=fake.postcode(),
            description=fake.paragraph(nb_sentences=5),
            sale_type="For Sale",
            price=random.randint(3, 12) * 10 ** 4,
            bedrooms=random.randint(1, 5),
            bathrooms=random.randint(1, 5),
            sqft=random.randint(1, 20) * 10**2,
            open_house=fake.pybool(),
            photo_main=base64.b64encode(requests.get(url).content)
        )

        serializer = ListingSerializer(data=data)
        if i == 0:
            print(data)

        print("****************************")
        if serializer.is_valid():
            serializer.save()
            print('home saved')
        else:
            continue


# def get_books(key_word):
#     fake = Faker(['en_US'])
#     url = 'http://openlibrary.org/search.json'
#     payload = {'q': key_word}
#     response = requests.get(url, params=payload)

#     if response.status_code != 200:
#         print('Bad request made', response.status_code)
#         return

#     jsn = response.json()
#     books = jsn.get('docs')

#     for book in books:
#         book_name = book.get('title')
#         data = dict(
#             name=book_name,
#             author=book.get('author_name')[0],
#             description='-'.join(book.get('author_facet')),
#             date_of_relase=fake.date_time_between(
#                 start_date='-10y', end_date='now', tzinfo=None),
#         )

#         serializer = BookSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             print('book saved: ', book_name)
#         else:
#             continue
