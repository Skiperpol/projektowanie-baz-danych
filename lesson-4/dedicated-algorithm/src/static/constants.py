USER_ROLES = ['user', 'admin', 'warehouseman', 'editor']

STATUS_VALUES = [
    'Pending',
    'Paid',
    'Processing',
    'Shipped',
    'Delivered',
    'Cancelled',
    'Returned'
]

PAYMENT_METHOD_VALUES = [
    'Credit Card',
    'Bank Transfer',
    'PayPal',
    'Cash on Delivery',
    'BLIK',
    'Apple Pay'
]

DELIVERY_METHOD_VALUES = [
    ('Standard Courier', '15.00'),
    ('Express Courier', '25.00'),
    ('Parcel Locker', '12.00'),
    ('Pickup in Store', '0.00'),
    ('International Standard', '45.00'),
    ('International Express', '75.00')
]

WAREHOUSE_VALUES = [
    ('Central Warehouse', 1),
    ('North Hub', 2),
    ('South Hub', 3),
    ('West Logistics Center', 4),
    ('East Logistics Center', 5),
    ('Local Storage A', 6),
    ('Local Storage B', 7),
    ('Returns Center', 8),
    ('Distribution Point Alpha', 9),
    ('Distribution Point Beta', 10)
]

