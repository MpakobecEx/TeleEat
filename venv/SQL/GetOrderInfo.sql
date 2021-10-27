SELECT user,
       shop
FROM Orders
WHERE rowid = :order_id