from __future__ import annotations

import random
import time
from typing import TYPE_CHECKING

from generators import gen_shipment_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_shipment(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    start_time = time.time()
    print(f"  [{time.strftime('%H:%M:%S')}] Starting shipment load...")
    
    order_ids = loader.generated_ids.get("Order", [])
    if not order_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    print(f"  [{time.strftime('%H:%M:%S')}] Generating {count:,} shipment rows...")
    def rows():
        for i in range(count):
            if i > 0 and i % 50000 == 0:
                print(f"  [{time.strftime('%H:%M:%S')}] Generated {i:,} / {count:,} shipment rows...")
            oid = random.choice(order_ids)
            yield gen_shipment_row(oid, loader.unique_tracking_numbers, loader.tracking_counter)
            loader.tracking_counter += 1

    print(f"  [{time.strftime('%H:%M:%S')}] Inserting shipments into database...")
    loader._copy_stream("public", table_name, columns, rows(), batch)
    print(f"  [{time.strftime('%H:%M:%S')}] Shipments inserted, fetching IDs...")
    
    shipment_ids = loader._fetch_recent_ids("Shipment", count)
    print(f"  [{time.strftime('%H:%M:%S')}] Fetched {len(shipment_ids):,} shipment IDs")
    loader.generated_ids["Shipment"] = shipment_ids

    stock_ids = loader.generated_ids.get("StockItem", [])
    if stock_ids and shipment_ids:
        print(f"  [{time.strftime('%H:%M:%S')}] Updating StockItems with shipment_ids (found {len(stock_ids):,} StockItems)...")
        cur = loader.ps_conn.cursor()
        
        # Get StockItems that don't have shipment_id yet
        print(f"  [{time.strftime('%H:%M:%S')}] Querying StockItems without shipment_id...")
        query_start = time.time()
        cur.execute('SELECT id FROM "StockItem" WHERE shipment_id IS NULL')
        stock_ids_to_update = [row[0] for row in cur.fetchall()]
        query_time = time.time() - query_start
        print(f"  [{time.strftime('%H:%M:%S')}] Found {len(stock_ids_to_update):,} StockItems without shipment_id (query took {query_time:.1f}s)")
        
        if stock_ids_to_update:
            # Process in batches to avoid memory issues and random.sample() slowness
            print(f"  [{time.strftime('%H:%M:%S')}] Processing {len(stock_ids_to_update):,} StockItems in batches (~30% will be updated)...")
            batch_size = 10000
            updates = []
            total_updated = 0
            processed = 0
            
            for i in range(0, len(stock_ids_to_update), batch_size):
                batch_stock_ids = stock_ids_to_update[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (len(stock_ids_to_update) + batch_size - 1) // batch_size
                
                print(f"  [{time.strftime('%H:%M:%S')}] Processing batch {batch_num}/{total_batches} ({len(batch_stock_ids):,} items)...")
                
                # For each stock_id, randomly decide if we update it (30% chance)
                for stock_id in batch_stock_ids:
                    if random.random() < 0.3:
                        shipment_id = random.choice(shipment_ids)
                        updates.append((shipment_id, stock_id))
                
                # Execute updates for this batch
                if updates:
                    print(f"  [{time.strftime('%H:%M:%S')}] Batch {batch_num}: Executing {len(updates):,} updates...")
                    cur.executemany(
                        'UPDATE "StockItem" SET shipment_id = %s WHERE id = %s',
                        updates,
                    )
                    loader.ps_conn.commit()
                    total_updated += len(updates)
                    print(f"  [{time.strftime('%H:%M:%S')}] Batch {batch_num}: Updated {len(updates):,} rows | Total so far: {total_updated:,}")
                    updates = []
                
                processed += len(batch_stock_ids)
                if processed % 50000 == 0:
                    print(f"  [{time.strftime('%H:%M:%S')}] Progress: Processed {processed:,} / {len(stock_ids_to_update):,} StockItems")
            
            print(f"  [{time.strftime('%H:%M:%S')}] Finished: Updated {total_updated:,} StockItems total")
        
        cur.close()
        print(f"  [{time.strftime('%H:%M:%S')}] Finished updating StockItems with shipment_ids")
    
    elapsed = time.time() - start_time
    print(f"  [{time.strftime('%H:%M:%S')}] Shipment load completed in {elapsed:.1f}s")


__all__ = ["load_shipment"]

