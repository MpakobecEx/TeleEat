SELECT COUNT(*)
FROM Positions
WHERE shop_id = :shop_id
      AND parent = :parent