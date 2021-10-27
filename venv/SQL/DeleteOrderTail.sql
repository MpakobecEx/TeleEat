DELETE
FROM Orders_tail
WHERE order_id = :order_id
      AND user_id = :user_id
      AND position_id = :position_id