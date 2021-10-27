SELECT Shops.name,
       Shops.phone,
       Shops.site
FROM Shops
WHERE id = :shop_id