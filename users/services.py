import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(prod):
    """ Создание продукта в страйпе """
    stripe_product = stripe.Product.create(name=prod)
    return stripe_product


def create_stripe_price(payment_amount, product_id):
    """Создает цену в stripe"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(payment_amount),
        product_data={"name": product_id},
    )


def create_stripe_sessions(price):
    """Создает сессию для оплаты"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
