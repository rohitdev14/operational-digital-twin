"""Generate Day-2 synthetic telemetry as CSV."""
import csv
from pathlib import Path
from model.simulation import simulate

def main():
    rows=simulate(); out=Path("artifacts/day2_telemetry.csv"); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    print(f"Generated {len(rows)} telemetry rows -> {out}")
    print(f"Final cumulative energy: {rows[-1]['energy_kwh']:.3f} kWh")
    print(f"Pumps running range: {min(r['pumps_running'] for r in rows)}-{max(r['pumps_running'] for r in rows)}")
if __name__=="__main__": main()
