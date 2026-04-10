import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
import os

# Local DuckDB file path
DB_URL = "duckdb:///db_exercises/analytics.db"

def setup_db():
    engine = create_engine(DB_URL)

    # Remove existing DB so the script is idempotent and can be re-run freely
    db_path = DB_URL.replace("duckdb:///", "")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Removed existing database.")

    with engine.connect() as conn:
        # 1. Read and Execute Schema from external file
        print("🔨 Applying schema from schema.sql...")
        with open("db_exercises/schema.sql", "r") as f:
            conn.execute(text(f.read()))
        conn.commit()

        # 2. Seed Entities
        # Note: ebay.com has NO keyword data (interesting for Q13/Q14 anti-join questions)
        print("🌱 Seeding entities...")
        entities = [
            ('amazon.com',  'E-commerce'),
            ('ebay.com',    'E-commerce'),
            ('facebook.com','Social Media'),
            ('tiktok.com',  'Social Media'),
            ('google.com',  'Search'),
        ]
        for site, cat in entities:
            conn.execute(
                text("INSERT OR IGNORE INTO entity_metadata VALUES (:id, :cat, 'General')"),
                {"id": site, "cat": cat}
            )

        # 3. Seed Metrics (full year 2025)
        # Each site has a realistic base traffic level and seasonal pattern so that:
        # - Q7  (ranking by total)         → clear winner (amazon >> others)
        # - Q8  (avg by device)            → mobile > desktop for tiktok/facebook, opposite for google
        # - Q9  (HAVING > 20M)             → only 2–3 sites qualify
        # - Q18 (rolling avg)              → smooth trends visible
        # - Q20 (day-over-day delta)       → meaningful swings
        # - Q21 (best desktop day)         → one clear peak per site
        # - Q25 (mobile share % by month)  → tiktok heavily mobile, google heavily desktop
        # - Q27 (week-over-week growth)    → tiktok grows over the year, ebay declines
        # - Q28 (z-score anomalies)        → deliberate traffic spikes injected per site
        print("📈 Generating daily metrics...")

        start_date = datetime(2025, 1, 1)

        # Base daily visits (desktop, mobile) and growth trend per site
        site_profiles = {
            'amazon.com':   {"base_d": 120_000, "base_m": 90_000,  "trend": 0.0002},
            'ebay.com':     {"base_d": 40_000,  "base_m": 25_000,  "trend": -0.0003},  # declining
            'facebook.com': {"base_d": 55_000,  "base_m": 95_000,  "trend": 0.0001},
            'tiktok.com':   {"base_d": 30_000,  "base_m": 130_000, "trend": 0.0008},   # fast mobile growth
            'google.com':   {"base_d": 200_000, "base_m": 80_000,  "trend": 0.0001},
        }

        # Inject deliberate traffic spikes (for Q28 z-score anomalies)
        spikes = {
            'amazon.com':   {15: 3.5, 200: 4.0},   # day 15 and 200 = big spikes
            'tiktok.com':   {90: 5.0},
            'google.com':   {180: 3.8},
            'facebook.com': {45: 3.2},
            'ebay.com':     {300: 3.0},
        }

        metrics = []
        for site, _ in entities:
            profile = site_profiles[site]
            site_spikes = spikes.get(site, {})
            for i in range(365):
                d = (start_date + timedelta(days=i)).date()
                trend_factor = 1 + profile["trend"] * i

                # Add mild weekly seasonality (weekends ~20% lower for B2B-ish sites)
                weekday = (start_date + timedelta(days=i)).weekday()
                season = 0.85 if weekday >= 5 else 1.0

                base_d = int(profile["base_d"] * trend_factor * season)
                base_m = int(profile["base_m"] * trend_factor * season)

                v_d = int(random.gauss(base_d, base_d * 0.08))
                v_m = int(random.gauss(base_m, base_m * 0.08))

                # Apply spike if this is a spike day
                if i in site_spikes:
                    v_d = int(v_d * site_spikes[i])
                    v_m = int(v_m * site_spikes[i])

                metrics.append({"id": site, "date": d, "v": max(1000, v_d), "t": "Desktop"})
                metrics.append({"id": site, "date": d, "v": max(1000, v_m), "t": "Mobile"})

        conn.execute(text("INSERT OR IGNORE INTO metrics_daily VALUES (:id, :date, :v, :t)"), metrics)

        # 4. Seed Attribute/Keyword Data
        # ebay.com intentionally excluded → appears in metrics but NOT here (Q13/Q14)
        # Multiple dates so Q10 pivot has meaningful organic vs paid split
        # Each site has one clearly dominant keyword (Q17 top keyword per site)
        print("🔍 Generating attribute performance...")

        keywords = ['shoes', 'electronics', 'trending', 'login', 'search']

        # Dominant keyword per site (will get 5–10x more volume than others)
        dominant = {
            'amazon.com':   'electronics',
            'facebook.com': 'login',
            'tiktok.com':   'trending',
            'google.com':   'search',
        }

        attr_payload = []
        attr_dates = ['2025-03-01', '2025-06-01', '2025-09-01']
        entities_with_keywords = [e for e in entities if e[0] != 'ebay.com']

        for site, _ in entities_with_keywords:
            for kw in keywords:
                for dt in attr_dates:
                    is_dominant = (dominant.get(site) == kw)
                    vol_base = random.randint(5000, 10000) if is_dominant else random.randint(300, 2000)
                    # Skew organic/paid: dominant keywords tend to be organic
                    src = 'Organic' if (is_dominant and random.random() < 0.8) else random.choice(['Organic', 'Paid'])
                    attr_payload.append({
                        "kw": kw, "id": site, "date": dt,
                        "src": src, "vol": vol_base
                    })

        conn.execute(text("INSERT INTO attribute_performance VALUES (:kw, :id, :date, :src, :vol)"), attr_payload)

        # 5. Seed Activity Logs (for Q24/Q26 bot detection and Q29 sessionization)
        print("🖱️ Simulating behavior logs...")
        logs = []

        # --- Bot user 9999: 10 clicks within 10 seconds (Q24 back-to-back, Q26 >5/minute) ---
        bot_ts = datetime(2026, 1, 1, 12, 0, 0)
        for i in range(10):
            logs.append({
                "uid": 9999,
                "ts": bot_ts + timedelta(seconds=i),
                "id": random.choice([s[0] for s in entities]),
                "type": "click"
            })

        # --- Bot user 8888: bursts in multiple minutes (also caught by Q26) ---
        for burst in range(3):
            burst_ts = datetime(2026, 1, 2, 10 + burst, 0, 0)
            for i in range(8):
                logs.append({
                    "uid": 8888,
                    "ts": burst_ts + timedelta(seconds=i * 4),
                    "id": random.choice([s[0] for s in entities]),
                    "type": "click"
                })

        # --- Normal users: realistic browsing sessions (Q29 sessionization) ---
        # Users have 1–3 sessions per day with realistic inter-click gaps
        normal_users = list(range(100, 150))  # 50 distinct users
        for uid in normal_users:
            num_sessions = random.randint(1, 3)
            for _ in range(num_sessions):
                # Session start: random time in January 2026
                session_start = datetime(2026, 1, random.randint(1, 28),
                                         random.randint(7, 22), random.randint(0, 59))
                num_clicks = random.randint(2, 8)
                ts = session_start
                site = random.choice([s[0] for s in entities])
                for _ in range(num_clicks):
                    logs.append({"uid": uid, "ts": ts, "id": site, "type": "click"})
                    # Inter-click gap: 10s–5min within a session
                    ts += timedelta(seconds=random.randint(10, 300))

        # --- Add a gap >30min for same user to create a clear second session (Q29) ---
        for uid in random.sample(normal_users, 20):
            early = datetime(2026, 1, 5, 9, 0, 0)
            late  = datetime(2026, 1, 5, 11, 0, 0)  # 2hr gap → new session
            for click_ts in [early, early + timedelta(minutes=2), late, late + timedelta(minutes=3)]:
                logs.append({"uid": uid, "ts": click_ts, "id": random.choice([s[0] for s in entities]), "type": "click"})

        conn.execute(text("INSERT INTO activity_logs VALUES (:uid, :ts, :id, :type)"), logs)
        conn.commit()
        print("\n✅ Setup Complete! Local database 'analytics.db' is ready.")

if __name__ == "__main__":
    setup_db()