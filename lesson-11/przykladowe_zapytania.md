# Raport sprzedaży i przychodów według kategorii produktów
```
db.orders.aggregate([
  { $unwind: "$items" },
  {
    $lookup: {
      from: "products",
      localField: "items.product_id",
      foreignField: "_id",
      as: "prod_details"
    }
  },
  { $unwind: "$prod_details" },
  { $unwind: "$prod_details.categories" },
  {
    $group: {
      _id: "$prod_details.categories.name",
      total_revenue: { $sum: { $multiply: ["$items.quantity", "$items.unit_price"] } },
      items_sold: { $sum: "$items.quantity" }
    }
  },
  { $sort: { total_revenue: -1 } }
])
```

# Wypisanie wszystkich userów
```
db.users.find()
```

# Wyszukiwanie wszystkich zamówień danego klienta
```
db.orders.find({ "user_id": "user_555" }).sort({ "order_date": -1 })
```

# Sprawdzenie dostępności towaru w konkretnym magazynie
```
db.inventory_bulk.find({ 
  "warehouse_id": "wh_central", 
  "variant_id": ObjectId("6580abc00000000000000001") 
})
```

# Lista produktów z konkretnej kategorii
```
db.products.find({ "categories.id": 10 })
```