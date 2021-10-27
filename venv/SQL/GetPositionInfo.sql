SELECT name,
    cost
FROM Positions
WHERE shop_id = :shop_id
    AND id = :id