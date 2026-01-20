db.createCollection("carts", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "items", "updated_at", "user_id"],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId" },
        updated_at: { bsonType: "date" },
        items: {
          bsonType: "array",
          minItems: 0,
          items: {
            bsonType: "object",
            required: ["product_id", "quantity", "variant_id"],
            properties: {
              product_id: { bsonType: "objectId" },
              variant_id: { bsonType: "objectId" },
              quantity: {
                bsonType: "int",
                minimum: 1
              }
            }
          }
        }
      }
    }
  }
});

db.createCollection("inventory_bulk", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "variant_id",
        "warehouse_id",
        "quantity_on_hand",
        "quantity_reserved"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        variant_id: { bsonType: "objectId" },
        warehouse_id: { bsonType: "objectId" },
        quantity_on_hand: { bsonType: "int", minimum: 0 },
        quantity_reserved: { bsonType: "int", minimum: 0 }
      }
    }
  }
});

db.createCollection("inventory_serial", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "serial_number",
        "status",
        "variant_id",
        "warehouse_id",
        "history"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        serial_number: { bsonType: "string", minLength: 1 },
        status: {
          enum: ["available", "reserved", "sold", "damaged", "returned"]
        },
        variant_id: { bsonType: "objectId" },
        warehouse_id: { bsonType: "objectId" },
        history: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["date", "status"],
            properties: {
              date: { bsonType: "date" },
              status: {
                enum: ["available", "reserved", "sold", "damaged", "returned"]
              },
              note: { bsonType: "string" }
            }
          }
        }
      }
    }
  }
});

db.createCollection("manufacturers", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "name", "active", "contact"],
      properties: {
        _id: { bsonType: "objectId" },
        name: { bsonType: "string", minLength: 1 },
        active: { bsonType: "bool" },
        description: { bsonType: "string" },
        website: { bsonType: "string" },
        contact: {
          bsonType: "object",
          required: ["email", "phone"],
          properties: {
            email: { bsonType: "string", pattern: "^.+@.+$" },
            phone: { bsonType: "string" }
          }
        },
        address: {
          bsonType: "object",
          required: ["city", "street", "zip_code"],
          properties: {
            city: { bsonType: "string" },
            street: { bsonType: "string" },
            zip_code: { bsonType: "string" }
          }
        }
      }
    }
  }
});

db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "user_id",
        "items",
        "status",
        "order_date",
        "total_amount",
        "payment_method",
        "billing_address",
        "shipping_address",
        "delivery_method"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId" },
        order_date: { bsonType: "date" },
        payment_method: { bsonType: "string" },
        status: {
          enum: [
            "new",
            "payment_pending",
            "processing",
            "shipped",
            "completed",
            "cancelled"
          ]
        },
        total_amount: { bsonType: "decimal" },
        items: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: [
              "name",
              "product_id",
              "quantity",
              "unit_price",
              "variant_sku"
            ],
            properties: {
              name: { bsonType: "string" },
              product_id: { bsonType: "objectId" },
              quantity: { bsonType: "int" },
              unit_price: { bsonType: "decimal" },
              variant_sku: { bsonType: "string" }
            }
          }
        },
        billing_address: {
          bsonType: "object",
          required: ["street", "city", "postal_code", "country"],
          properties: {
            street: { bsonType: "string" },
            city: { bsonType: "string" },
            postal_code: { bsonType: "string" },
            country: { bsonType: "string" }
          }
        },
        shipping_address: {
          bsonType: "object",
          required: ["street", "city", "postal_code", "country"],
          properties: {
            street: { bsonType: "string" },
            city: { bsonType: "string" },
            postal_code: { bsonType: "string" },
            country: { bsonType: "string" }
          }
        },
        delivery_method: {
          bsonType: "object",
          required: ["name", "cost"],
          properties: {
            name: { bsonType: "string" },
            cost: { bsonType: "decimal" }
          }
        }
      }
    }
  }
});

db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "name",
        "description",
        "manufacturer",
        "categories",
        "variants",
        "avg_rating",
        "review_count",
        "base_attributes"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        name: { bsonType: "string" },
        description: { bsonType: "string" },
        avg_rating: { bsonType: "decimal" },
        review_count: { bsonType: "int" },
        base_attributes: {
          bsonType: "object",
          required: ["connection", "warranty"],
          properties: {
            connection: { bsonType: "string" },
            warranty: { bsonType: "string" }
          }
        },
        manufacturer: {
          bsonType: "object",
          required: ["id", "name"],
          properties: {
            id: { bsonType: "objectId" },
            name: { bsonType: "string" }
          }
        },
        categories: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["id", "name"],
            properties: {
              id: { bsonType: "objectId" },
              name: { bsonType: "string" }
            }
          }
        },
        variants: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["_id", "attributes", "base_price", "inventory_type", "sku"],
            properties: {
              _id: { bsonType: "objectId" },
              sku: { bsonType: "string" },
              inventory_type: { bsonType: "string" },
              base_price: { bsonType: "decimal" },
              attributes: {
                bsonType: "object",
                required: ["color"],
                properties: {
                  color: { bsonType: "string" }
                }
              },
              current_promotion: {
                bsonType: "object",
                required: ["final_price", "promo_id"],
                properties: {
                  final_price: { bsonType: "decimal" },
                  promo_id: { bsonType: "objectId" }
                }
              }
            }
          }
        }
      }
    }
  }
});

db.createCollection("promotions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "name",
        "discount",
        "start_date",
        "end_date",
        "is_active",
        "target"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        name: { bsonType: "string" },
        is_active: { bsonType: "bool" },
        start_date: { bsonType: "date" },
        end_date: { bsonType: "date" },
        discount: {
          bsonType: "object",
          required: ["type", "value"],
          properties: {
            type: { bsonType: "string" },
            value: { bsonType: "int" }
          }
        },
        target: {
          bsonType: "object",
          required: ["scope", "target_id"],
          properties: {
            scope: { bsonType: "string" },
            target_id: { bsonType: "objectId" }
          }
        }
      }
    }
  }
});

db.createCollection("reviews", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "product_id",
        "user_id",
        "rating",
        "comment",
        "helpful_votes",
        "posted_at"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        product_id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId" },
        rating: { bsonType: "int", minimum: 1, maximum: 5 },
        comment: { bsonType: "string", minLength: 5, maxLength: 2000 },
        helpful_votes: { bsonType: "int", minimum: 0 },
        posted_at: { bsonType: "date" }
      }
    }
  }
});

db.createCollection("user_favorites", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "user_id", "product_id", "added_at"],
      properties: {
        _id: { bsonType: "objectId" },
        user_id: { bsonType: "objectId" },
        product_id: { bsonType: "objectId" },
        variant_id: { bsonType: "objectId" },
        added_at: { bsonType: "date" }
      }
    }
  }
});

db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "_id",
        "email",
        "first_name",
        "last_name",
        "password_hash",
        "registered_at",
        "roles",
        "addresses"
      ],
      properties: {
        _id: { bsonType: "objectId" },
        email: { bsonType: "string", pattern: "^.+@.+$" },
        first_name: { bsonType: "string", minLength: 1 },
        last_name: { bsonType: "string", minLength: 1 },
        password_hash: { bsonType: "string" },
        registered_at: { bsonType: "date" },
        roles: {
          bsonType: "array",
          items: {
            enum: ["customer", "admin", "warehouse_staff", "support"]
          }
        },
        addresses: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: [
              "id",
              "street",
              "city",
              "postal_code",
              "country",
              "is_default_shipping"
            ],
            properties: {
              id: { bsonType: "objectId" },
              street: { bsonType: "string" },
              city: { bsonType: "string" },
              postal_code: { bsonType: "string" },
              country: { bsonType: "string" },
              is_default_shipping: { bsonType: "bool" },
              phone: { bsonType: "string" }
            }
          }
        }
      }
    }
  }
});

db.createCollection("warehouses", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "name", "type", "is_active", "address"],
      properties: {
        _id: { bsonType: "objectId" },
        name: { bsonType: "string" },
        type: {
          enum: ["central", "local", "pickup_point"]
        },
        is_active: { bsonType: "bool" },
        address: {
          bsonType: "object",
          required: ["street", "city", "postal_code", "country"],
          properties: {
            street: { bsonType: "string" },
            city: { bsonType: "string" },
            postal_code: { bsonType: "string" },
            country: { bsonType: "string" }
          }
        },
        location: {
          bsonType: "object",
          required: ["type", "coordinates"],
          properties: {
            type: { enum: ["Point"] },
            coordinates: {
              bsonType: "array",
              minItems: 2,
              maxItems: 2,
              items: { bsonType: "double" }
            }
          }
        }
      }
    }
  }
});
