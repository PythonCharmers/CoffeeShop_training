"""
API endpoints for Connexion to consume
"""
from sqlalchemy import or_

from .models import Shop
from coffeeshop.server import db


PAGE_SIZE = 10


def list_shops(page=1):
    """
    List of shops from the database

    :param page: Result page
    :type page: int
    :rtype: list of dict
    """
    return [
        {'id': shop.id, 'name': shop.name, 'address': shop.address}
        for shop in
        Shop.query.offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE)
    ]


def get_shop(shop_id):
    """
    Get the shop by the ID

    :param shop_id: ID of the shop
    :type shop_id: int
    :rtype: dict
    """
    shop = Shop.query.get_or_404(shop_id)
    return {'id': shop.id, 'name': shop.name, 'address': shop.address}


def search(q, page=1):
    """
    Search for a shop by a given query

    :param q: The query to search for
    :type q: str
    :param page: Result page
    :type page: int
    :rtype: list of dict
    """
    search_term = f'%{q}%'
    found_shops = Shop.query.filter(or_(
        Shop.name.ilike(search_term),
        Shop.address.ilike(search_term)
    )).offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE)

    return [
        {'id': shop.id, 'name': shop.name, 'address': shop.address}
        for shop in found_shops
    ]
