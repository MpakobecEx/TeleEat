SELECT MAX(id)
FROM Orders
     INNER JOIN Positions
           ON Orders.shop = Positions.shop_id
WHERE stop IS NULL;