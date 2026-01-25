import time
import psycopg
import clickhouse_connect

PG_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "huy",
    "password": "huy123",
    "dbname": "huy"
}

CH_CONFIG = {
    "host": "localhost",
    "port": 8123,
    "username": "default",
    "password": ""
}

# Benchmark queries - mix of OLTP and OLAP patterns
QUERIES = {
    "Point lookup by ID": """
        SELECT * FROM orders WHERE order_id = 500000
    """,
    
    "Lookup by customer": """
        SELECT * FROM orders WHERE customer_id = 12345 LIMIT 100
    """,
    
    "Count all rows": """
        SELECT COUNT(*) FROM orders
    """,
    
    "Sum by category": """
        SELECT category, SUM(quantity * unit_price) as revenue
        FROM orders GROUP BY category ORDER BY revenue DESC
    """,
    
    "Monthly revenue": """
        SELECT 
            EXTRACT(YEAR FROM order_date) as year,
            EXTRACT(MONTH FROM order_date) as month,
            SUM(quantity * unit_price - discount) as net_revenue,
            COUNT(*) as order_count
        FROM orders
        GROUP BY year, month
        ORDER BY year, month
    """,
    
    "Top regions by category": """
        SELECT region, category, 
            SUM(quantity * unit_price) as revenue,
            AVG(unit_price) as avg_price
        FROM orders
        GROUP BY region, category
        ORDER BY revenue DESC
        LIMIT 20
    """,
    
    "Payment method analysis": """
        SELECT payment_method,
            COUNT(*) as orders,
            SUM(quantity * unit_price) as total,
            AVG(discount) as avg_discount
        FROM orders
        GROUP BY payment_method
    """,
    
    "Date range filter + aggregation": """
        SELECT category, COUNT(*), SUM(quantity * unit_price)
        FROM orders
        WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY category
    """,
}

CH_QUERIES = {
    "Monthly revenue": """
        SELECT 
            toYear(order_date) as year,
            toMonth(order_date) as month,
            SUM(quantity * unit_price - discount) as net_revenue,
            COUNT(*) as order_count
        FROM orders
        GROUP BY year, month
        ORDER BY year, month
    """,
    
    "Date range filter + aggregation": """
        SELECT category, COUNT(*), SUM(quantity * unit_price)
        FROM orders
        WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31'
        GROUP BY category
    """,
}


def run_postgres_query(query: str) -> tuple[float, int]:
    """Run query on PostgreSQL, return (time, row_count)."""
    conn = psycopg.connect(**PG_CONFIG)
    cur = conn.cursor()
    
    start = time.time()
    cur.execute(query)
    rows = cur.fetchall()
    elapsed = time.time() - start
    
    cur.close()
    conn.close()
    return elapsed, len(rows)


def run_clickhouse_query(query: str) -> tuple[float, int]:
    """Run query on ClickHouse, return (time, row_count)."""
    client = clickhouse_connect.get_client(**CH_CONFIG)
    
    start = time.time()
    result = client.query(query)
    elapsed = time.time() - start
    
    return elapsed, result.row_count


def main():
    print("=" * 70)
    print("OLTP (PostgreSQL) vs OLAP (ClickHouse) Benchmark")
    print("=" * 70)
    print()
    
    results = []
    
    for name, pg_query in QUERIES.items():
        ch_query = CH_QUERIES.get(name, pg_query)
        
        print(f"Query: {name}")
        print("-" * 50)
        
        # Run PostgreSQL
        pg_time, pg_rows = run_postgres_query(pg_query)
        print(f"  PostgreSQL: {pg_time*1000:>8.2f} ms  ({pg_rows} rows)")
        
        # Run ClickHouse
        ch_time, ch_rows = run_clickhouse_query(ch_query)
        print(f"  ClickHouse: {ch_time*1000:>8.2f} ms  ({ch_rows} rows)")
        
        # Compare
        if pg_time < ch_time:
            winner = "PostgreSQL"
            speedup = ch_time / pg_time
        else:
            winner = "ClickHouse"
            speedup = pg_time / ch_time
        
        print(f"  Winner: {winner} ({speedup:.1f}x faster)")
        print()
        
        results.append((name, pg_time, ch_time, winner, speedup))
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"{'Query':<35} {'PG (ms)':>10} {'CH (ms)':>10} {'Winner':>12}")
    print("-" * 70)
    
    for name, pg_time, ch_time, winner, speedup in results:
        print(f"{name:<35} {pg_time*1000:>10.2f} {ch_time*1000:>10.2f} {winner:>12}")
    
    print()
    print("Key takeaways:")
    print("- PostgreSQL (OLTP): Optimized for point lookups, transactions, row-based")
    print("- ClickHouse (OLAP): Optimized for aggregations, analytics, column-based")


if __name__ == "__main__":
    main()
