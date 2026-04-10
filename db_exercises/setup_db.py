import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# Local DuckDB file path
DB_URL = "duckdb:///db_exercises/analytics.db"

def setup_db():
    engine = create_engine(DB_URL)
    
    with engine.connect() as conn:
        # 1. Read and Execute Schema from external file
        print("🔨 Applying schema from schema.sql...")
        with open("db_exercises/schema.sql", "r") as f:
            # DuckDB-engine handles multi-statement strings well
            conn.execute(text(f.read()))
        conn.commit()

        # 2. Seed Data
        print("🌱 Seeding entities...")
        entities = [
            ('amazon.com', 'E-commerce'), ('ebay.com', 'E-commerce'),
            ('facebook.com', 'Social Media'), ('tiktok.com', 'Social Media'),
            ('google.com', 'Search')
        ]
        for site, cat in entities:
            conn.execute(
                text("INSERT OR IGNORE INTO entity_metadata VALUES (:id, :cat, 'General')"),
                {"id": site, "cat": cat}
            )

        # 3. Seed Metrics (2025)
        print("📈 Generating daily metrics...")
        start_date = datetime(2025, 1, 1)
        metrics = []
        for site, _ in entities:
            for i in range(365):
                d = (start_date + timedelta(days=i)).date()
                metrics.append({"id": site, "date": d, "v": random.randint(1000, 150000), "t": "Desktop"})
                metrics.append({"id": site, "date": d, "v": random.randint(1000, 150000), "t": "Mobile"})
        conn.execute(text("INSERT OR IGNORE INTO metrics_daily VALUES (:id, :date, :v, :t)"), metrics)

        # 4. Seed Attribute/Keyword Data
        print("🔍 Generating attribute performance...")
        keywords = ['shoes', 'electronics', 'trending', 'login', 'search']
        attr_payload = []
        for site, _ in entities:
            for kw in keywords:
                attr_payload.append({
                    "kw": kw, "id": site, "date": "2025-06-01", 
                    "src": random.choice(['Organic', 'Paid']), "vol": random.randint(500, 10000)
                })
        conn.execute(text("INSERT INTO attribute_performance VALUES (:kw, :id, :date, :src, :vol)"), attr_payload)

        # 5. Seed Logs (Bot patterns & Sessions)
        print("🖱️ Simulating behavior logs...")
        logs = []
        # Create a Bot User (ID 9999)
        bot_ts = datetime(2026, 1, 1, 12, 0, 0)
        for i in range(10):
            logs.append({"uid": 9999, "ts": bot_ts + timedelta(seconds=i), "id": random.choice([s[0] for s in entities]), "type": "click"})
        
        # Create normal users
        for _ in range(1000):
            uid = random.randint(100, 300)
            site = random.choice([s[0] for s in entities])
            ts = datetime(2026, 1, random.randint(1, 28), random.randint(0,23), random.randint(0,59))
            logs.append({"uid": uid, "ts": ts, "id": site, "type": "click"})

        conn.execute(text("INSERT INTO activity_logs VALUES (:uid, :ts, :id, :type)"), logs)
        conn.commit()
        print("\n✅ Setup Complete! Local database 'analytics.db' is ready.")

if __name__ == "__main__":
    setup_db()