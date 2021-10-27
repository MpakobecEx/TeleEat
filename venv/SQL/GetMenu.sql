SELECT id,
       name,
       cost
FROM Positions
WHERE shop_id = :shop_id
      AND Positions.parent = :parent