SELECT name,
       SUM([count]) count,
       SUM([count] * cost) summa
FROM Orders
     INNER JOIN Orders_tail tail
           ON Orders.rowid = tail.order_id
     INNER JOIN Positions
           ON tail.position_id = Positions.id
              AND Orders.shop = Positions.shop_id
WHERE Orders.rowid = :order_id
    AND tail.user_id = :id
GROUP BY name
ORDER BY 1