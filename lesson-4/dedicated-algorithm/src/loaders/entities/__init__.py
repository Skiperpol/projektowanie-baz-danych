from .category import load_category
from .address import load_address
from .warehouse import load_warehouse
from .attribute import load_attribute
from .option import load_option
from .manufacturer import load_manufacturer
from .promotion import load_promotion
from .product import load_product
from .variant import load_variant
from .stock_item import load_stockitem
from .user import load_user
from .delivery_method import load_delivery_method
from .payment_method import load_payment_method
from .status import load_status
from .cart import load_cart
from .cart_item import load_cartitem
from .order import load_order
from .order_item import load_orderitem
from .shipment import load_shipment
from .favorite_product import load_favoriteproduct
from .product_category import load_productcategory
from .product_attribute import load_productattribute
from .variant_option import load_variantoption
from .review import load_review

ENTITY_LOADERS = {
    "category": load_category,
    "address": load_address,
    "warehouse": load_warehouse,
    "attribute": load_attribute,
    "option": load_option,
    "manufacturer": load_manufacturer,
    "promotion": load_promotion,
    "product": load_product,
    "variant": load_variant,
    "stockitem": load_stockitem,
    "user": load_user,
    "deliverymethod": load_delivery_method,
    "paymentmethod": load_payment_method,
    "status": load_status,
    "cart": load_cart,
    "cartitem": load_cartitem,
    "order": load_order,
    "orderitem": load_orderitem,
    "shipment": load_shipment,
    "favoriteproduct": load_favoriteproduct,
    "productcategory": load_productcategory,
    "productattribute": load_productattribute,
    "variantoption": load_variantoption,
    "review": load_review,
}

__all__ = ["ENTITY_LOADERS"]

