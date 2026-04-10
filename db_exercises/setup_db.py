import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# This creates a file named 'analytics.db' inside the db_exercises folder
DB_URL = "duckdb:///db_exercises/analytics.db"

def setup_db():
    engine = create_engine(DB_URL)
    
    with engine.connect() as conn:
        print("🔨 Creating local database from schema...")
        with open("db_exercises/schema.sql", "r") as f:
            for statement in f.read().split(';'):
                if statement.strip():
                    conn.execute(text(statement))
        
        # Seed Metadata
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

        # Seed Daily Metrics (2025)
        print("📈 Generating traffic data...")
        start_date = datetime(2025, 1, 1)
        metrics = []
        for site, _ in entities:
            for i in range(365):
                d = (start_date + timedelta(days=i)).date()
                metrics.append({"id": site, "date": d, "v": random.randint(1000, 100000), "t": "Desktop"})
                metrics.append({"id": site, "date": d, "v": random.randint(1000, 150000), "t": "Mobile"})
        
        conn.execute(text("INSERT OR IGNORE INTO metrics_daily VALUES (:id, :date, :v, :t)"), metrics)

        # Seed Activity Logs (Bot patterns & Sessions)
        print("🖱️ Simulating user activity logs...")
        logs = []
        for _ in range(2000):
            uid = random.randint(1000, 1200)
            site = random.choice([s[0] for s in entities])
            ts = datetime(2026, 1, random.randint(1, 28), random.randint(0,23), random.randint(0,59))
            logs.append({"uid": uid, "ts": ts, "id": site, "type": "click"})
            
            # 50% chance of a follow-up click (Sessionization exercise)
            if random.random() > 0.5:
                logs.append({"uid": uid, "ts": ts + timedelta(minutes=random.randint(1, 15)), "id": site, "type": "click"})

        conn.execute(text("INSERT INTO activity_logs VALUES (:uid, :ts, :id, :type)"), logs)
        conn.commit()
        print("\n✅ Database 'analytics.db' is ready!")

if __name__ == "__main__":
    setup_db()
