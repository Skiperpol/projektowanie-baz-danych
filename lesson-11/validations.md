# Card

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'items',
      'updated_at',
      'user_id'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      items: {
        bsonType: 'array',
        minItems: 0,
        items: {
          bsonType: 'object',
          properties: {
            product_id: {
              bsonType: 'objectId'
            },
            quantity: {
              bsonType: 'int',
              minimum: 1,
              description: 'Ilość musi być liczbą całkowitą większą od 0'
            },
            variant_id: {
              bsonType: 'objectId'
            }
          },
          required: [
            'product_id',
            'quantity',
            'variant_id'
          ]
        }
      },
      updated_at: {
        bsonType: 'date'
      },
      user_id: {
        bsonType: 'objectId'
      }
    }
  }
}
```

# Inventory bulk

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'quantity_on_hand',
      'quantity_reserved',
      'variant_id',
      'warehouse_id'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      variant_id: {
        bsonType: 'objectId'
      },
      warehouse_id: {
        bsonType: 'objectId'
      },
      quantity_on_hand: {
        bsonType: 'int',
        minimum: 0,
        description: 'Fizyczna liczba sztuk w magazynie'
      },
      quantity_reserved: {
        bsonType: 'int',
        minimum: 0,
        description: 'Liczba sztuk zarezerwowanych (np. w koszykach lub opłaconych)'
      }
    }
  }
}
```

# Inventory serial

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'history',
      'serial_number',
      'status',
      'variant_id',
      'warehouse_id'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      serial_number: {
        bsonType: 'string',
        minLength: 1
      },
      status: {
        'enum': [
          'available',
          'reserved',
          'sold',
          'damaged',
          'returned'
        ],
        description: 'Musi być jednym ze zdefiniowanych stanów'
      },
      variant_id: {
        bsonType: 'objectId'
      },
      warehouse_id: {
        bsonType: 'objectId'
      },
      history: {
        bsonType: 'array',
        items: {
          bsonType: 'object',
          required: [
            'date',
            'status'
          ],
          properties: {
            date: {
              bsonType: 'date'
            },
            status: {
              'enum': [
                'available',
                'reserved',
                'sold',
                'damaged',
                'returned'
              ]
            },
            note: {
              bsonType: 'string'
            }
          }
        }
      }
    }
  }
}
```

# Manufacturers

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: ['_id', 'active', 'contact', 'name'],
    properties: {
      _id: { bsonType: 'objectId' },
      name: { bsonType: 'string', minLength: 1 },
      active: { bsonType: 'bool' },
      description: { bsonType: 'string' },
      website: { bsonType: 'string' },
      contact: {
        bsonType: 'object',
        required: ['email', 'phone'],
        properties: {
          email: { 
            bsonType: 'string',
            pattern: '^.+@.+$',
            description: 'Musi być poprawnym adresem email'
          },
          phone: { bsonType: 'string' }
        }
      },
      address: {
        bsonType: 'object',
        required: ['city', 'street', 'zip_code'],
        properties: {
          city: { bsonType: 'string' },
          street: { bsonType: 'string' },
          zip_code: { bsonType: 'string' }
        }
      }
    }
  }
}
```

# Orders

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'billing_address',
      'delivery_method',
      'items',
      'order_date',
      'payment_method',
      'shipping_address',
      'status',
      'total_amount',
      'user_id'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      billing_address: {
        bsonType: 'object',
        properties: {
          city: {
            bsonType: 'string'
          },
          country: {
            bsonType: 'string'
          },
          postal_code: {
            bsonType: 'string'
          },
          street: {
            bsonType: 'string'
          }
        },
        required: [
          'city',
          'country',
          'postal_code',
          'street'
        ]
      },
      delivery_method: {
        bsonType: 'object',
        properties: {
          cost: {
            bsonType: 'decimal'
          },
          name: {
            bsonType: 'string'
          }
        },
        required: [
          'cost',
          'name'
        ]
      },
      items: {
        bsonType: 'array',
        items: {
          bsonType: 'object',
          properties: {
            name: {
              bsonType: 'string'
            },
            product_id: {
              bsonType: 'objectId'
            },
            quantity: {
              bsonType: 'int'
            },
            unit_price: {
              bsonType: 'decimal'
            },
            variant_sku: {
              bsonType: 'string'
            }
          },
          required: [
            'name',
            'product_id',
            'quantity',
            'unit_price',
            'variant_sku'
          ]
        }
      },
      order_date: {
        bsonType: 'date'
      },
      payment_method: {
        bsonType: 'string'
      },
      shipping_address: {
        bsonType: 'object',
        properties: {
          city: {
            bsonType: 'string'
          },
          country: {
            bsonType: 'string'
          },
          postal_code: {
            bsonType: 'string'
          },
          street: {
            bsonType: 'string'
          }
        },
        required: [
          'city',
          'country',
          'postal_code',
          'street'
        ]
      },
      status: {
        'enum': [
          'new',
          'payment_pending',
          'processing',
          'shipped',
          'completed',
          'cancelled'
        ],
        description: 'Status zamówienia musi być zgodny z procesem logistycznym'
      },
      total_amount: {
        bsonType: 'decimal'
      },
      user_id: {
        bsonType: 'objectId'
      }
    }
  }
}
```

# Products

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'avg_rating',
      'base_attributes',
      'categories',
      'description',
      'manufacturer',
      'name',
      'review_count',
      'variants'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      avg_rating: {
        bsonType: 'decimal'
      },
      base_attributes: {
        bsonType: 'object',
        properties: {
          connection: {
            bsonType: 'string'
          },
          warranty: {
            bsonType: 'string'
          }
        },
        required: [
          'connection',
          'warranty'
        ]
      },
      categories: {
        bsonType: 'array',
        items: {
          bsonType: 'object',
          properties: {
            id: {
              bsonType: 'objectId'
            },
            name: {
              bsonType: 'string'
            }
          },
          required: [
            'id',
            'name'
          ]
        }
      },
      description: {
        bsonType: 'string'
      },
      manufacturer: {
        bsonType: 'object',
        properties: {
          id: {
            bsonType: 'objectId'
          },
          name: {
            bsonType: 'string'
          }
        },
        required: [
          'id',
          'name'
        ]
      },
      name: {
        bsonType: 'string'
      },
      review_count: {
        bsonType: 'int'
      },
      variants: {
        bsonType: 'array',
        items: {
          bsonType: 'object',
          properties: {
            _id: {
              bsonType: 'objectId'
            },
            attributes: {
              bsonType: 'object',
              properties: {
                color: {
                  bsonType: 'string'
                }
              },
              required: [
                'color'
              ]
            },
            base_price: {
              bsonType: 'decimal'
            },
            current_promotion: {
              bsonType: 'object',
              properties: {
                final_price: {
                  bsonType: 'decimal'
                },
                promo_id: {
                  bsonType: 'objectId'
                }
              },
              required: [
                'final_price',
                'promo_id'
              ]
            },
            inventory_type: {
              bsonType: 'string'
            },
            sku: {
              bsonType: 'string'
            }
          },
          required: [
            '_id',
            'attributes',
            'base_price',
            'inventory_type',
            'sku'
          ]
        }
      }
    }
  }
}
```

# Promotions

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'discount',
      'end_date',
      'is_active',
      'name',
      'start_date',
      'target'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      discount: {
        bsonType: 'object',
        properties: {
          type: {
            bsonType: 'string'
          },
          value: {
            bsonType: 'int'
          }
        },
        required: [
          'type',
          'value'
        ]
      },
      end_date: {
        bsonType: 'date'
      },
      is_active: {
        bsonType: 'bool'
      },
      name: {
        bsonType: 'string'
      },
      start_date: {
        bsonType: 'date'
      },
      target: {
        bsonType: 'object',
        properties: {
          scope: {
            bsonType: 'string'
          },
          target_id: {
            bsonType: 'objectId'
          }
        },
        required: [
          'scope',
          'target_id'
        ]
      }
    }
  }
}
```

# Reviews

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'comment',
      'helpful_votes',
      'posted_at',
      'product_id',
      'rating',
      'user_id'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      product_id: {
        bsonType: 'objectId'
      },
      user_id: {
        bsonType: 'objectId'
      },
      rating: {
        bsonType: 'int',
        minimum: 1,
        maximum: 5,
        description: 'Ocena w skali 1-5'
      },
      comment: {
        bsonType: 'string',
        minLength: 5,
        maxLength: 2000
      },
      helpful_votes: {
        bsonType: 'int',
        minimum: 0
      },
      posted_at: {
        bsonType: 'date'
      }
    }
  }
}
```

# User favorites

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'added_at',
      'product_id',
      'user_id'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      user_id: {
        bsonType: 'objectId'
      },
      product_id: {
        bsonType: 'objectId'
      },
      added_at: {
        bsonType: 'date'
      },
      variant_id: {
        bsonType: 'objectId'
      }
    }
  }
}
```

# Users

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'addresses',
      'email',
      'first_name',
      'last_name',
      'password_hash',
      'registered_at',
      'roles'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      email: {
        bsonType: 'string',
        pattern: '^.+@.+$',
        description: 'Unikalny adres email użytkownika'
      },
      first_name: {
        bsonType: 'string',
        minLength: 1
      },
      last_name: {
        bsonType: 'string',
        minLength: 1
      },
      password_hash: {
        bsonType: 'string'
      },
      registered_at: {
        bsonType: 'date'
      },
      roles: {
        bsonType: 'array',
        items: {
          'enum': [
            'customer',
            'admin',
            'warehouse_staff',
            'support'
          ]
        }
      },
      addresses: {
        bsonType: 'array',
        items: {
          bsonType: 'object',
          required: [
            'city',
            'country',
            'id',
            'is_default_shipping',
            'postal_code',
            'street'
          ],
          properties: {
            id: {
              bsonType: 'objectId'
            },
            street: {
              bsonType: 'string'
            },
            city: {
              bsonType: 'string'
            },
            postal_code: {
              bsonType: 'string'
            },
            country: {
              bsonType: 'string'
            },
            is_default_shipping: {
              bsonType: 'bool'
            },
            phone: {
              bsonType: 'string'
            }
          }
        }
      }
    }
  }
}
```

# Warehouses

```
{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'address',
      'is_active',
      'name',
      'type'
    ],
    properties: {
      _id: {
        bsonType: 'objectId'
      },
      name: {
        bsonType: 'string'
      },
      type: {
        'enum': [
          'central',
          'local',
          'pickup_point'
        ],
        description: 'Rodzaj placówki'
      },
      is_active: {
        bsonType: 'bool'
      },
      address: {
        bsonType: 'object',
        required: [
          'city',
          'country',
          'postal_code',
          'street'
        ],
        properties: {
          street: {
            bsonType: 'string'
          },
          city: {
            bsonType: 'string'
          },
          postal_code: {
            bsonType: 'string'
          },
          country: {
            bsonType: 'string'
          }
        }
      },
      location: {
        bsonType: 'object',
        required: [
          'type',
          'coordinates'
        ],
        properties: {
          type: {
            'enum': [
              'Point'
            ]
          },
          coordinates: {
            bsonType: 'array',
            minItems: 2,
            maxItems: 2,
            items: {
              bsonType: 'double'
            }
          }
        }
      }
    }
  }
}
```