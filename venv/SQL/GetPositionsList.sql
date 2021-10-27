SELECT name,
       SUM([count]) sum_count,
       SUM([count] * cost) summa
FROM Orders
     INNER JOIN Orders_tail tail
           ON Orders.rowid = tail.order_id
     INNER JOIN Positions
           ON tail.position_id = Positions.id
              AND Orders.shop = Positions.shop_id
WHERE stop IS NULL
GROUP BY name
ORDER BY 1