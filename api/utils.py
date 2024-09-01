from .client import APIClient
from .endpoints import Endpoints

def get_user_data(user_id):
    client = APIClient()
    return client.get(f'{Endpoints.USERS}/{user_id}')

def create_product(product_data):
    client = APIClient()
    return client.post(Endpoints.PRODUCTS, data=product_data)

# Add other utility functions as needed