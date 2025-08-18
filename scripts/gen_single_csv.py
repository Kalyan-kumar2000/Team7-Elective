#!/usr/bin/env python3
import csv, os, random, uuid, sys
from datetime import datetime, timedelta

PAYMENT = ["card","upi","netbanking","cod"]
CHANNEL = ["web","app","store","partner"]
STATES  = ["TX","CA","NY","IL","FL","WA","NJ","GA","PA","MA"]
CITIES  = ["Houston","Dallas","Austin","San Jose","NYC","Chicago","Miami","Seattle","Newark","Atlanta","Philly","Boston"]

def rand_ts(days=730):
    now = datetime.utcnow()
    start = now - timedelta(days=days)
    dt = start + timedelta(seconds=random.randint(0, int((now - start).total_seconds())))
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def main(out_path, target_bytes):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    header = ["order_id","order_ts","customer_id","product_id","quantity","unit_price_cents",
              "discount_pct","payment_type","city","state","country","channel"]
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        batch = 200000   # adjust for speed/memory
        while True:
            rows = []
            for _ in range(batch):
                rows.append([
                    str(uuid.uuid4()),
                    rand_ts(),
                    random.randint(1, 5_000_000),
                    random.randint(1, 100_000),
                    random.randint(1, 5),
                    random.randint(199, 99_999),
                    random.choice([0,0,0,5,10,15,20]),
                    random.choice(PAYMENT),
                    random.choice(CITIES),
                    random.choice(STATES),
                    "USA",
                    random.choice(CHANNEL),
                ])
            w.writerows(rows)
            f.flush()
            if os.path.getsize(out_path) >= target_bytes:
                break
    print(f"Generated {out_path} size={os.path.getsize(out_path)} bytes")

if __name__ == "__main__":
    out = sys.argv[1]
    tgt = int(sys.argv[2])
    main(out, tgt)

