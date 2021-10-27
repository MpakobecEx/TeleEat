UPDATE Orders
SET stop = datetime('now')
WHERE rowid = :order_id