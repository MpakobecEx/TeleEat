UPDATE Orders_tail
SET [count] = :count
WHERE order_id = :order_id
      AND user_id = :user_id
      AND [count] IS NULL