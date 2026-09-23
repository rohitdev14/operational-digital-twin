"""Render lightweight Day-2 SVG plots without plotting dependencies."""
from pathlib import Path
from model.simulation import simulate
W,H,PAD=900,320,55

def polyline(values,vmin,vmax):
    n=len(values); pts=[]
    for i,v in enumerate(values):
        x=PAD+(W-2*PAD)*i/max(1,n-1); y=H-PAD-(H-2*PAD)*(v-vmin)/(vmax-vmin)
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)

def svg(title,series,ymin,ymax,ylabel):
    grid=[]
    for i in range(5):
        y=PAD+(H-2*PAD)*i/4; val=ymax-(ymax-ymin)*i/4
        grid.append(f'<line x1="{PAD}" y1="{y:.1f}" x2="{W-PAD}" y2="{y:.1f}" stroke="#ddd"/><text x="8" y="{y+4:.1f}" font-size="12">{val:.1f}</text>')
    lines=[]; palette=["#1565c0","#c62828","#2e7d32"]
    for idx,(name,values) in enumerate(series):
        lines.append(f'<polyline fill="none" stroke="{palette[idx]}" stroke-width="2" points="{polyline(values,ymin,ymax)}"/><text x="{PAD+idx*190}" y="{H-15}" font-size="12" fill="{palette[idx]}">{name}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" fill="white"/>
<text x="{W/2}" y="24" text-anchor="middle" font-size="18" font-family="sans-serif">{title}</text>
<text x="16" y="{H/2}" transform="rotate(-90 16 {H/2})" text-anchor="middle" font-size="12">{ylabel}</text>
{''.join(grid)}
<line x1="{PAD}" y1="{H-PAD}" x2="{W-PAD}" y2="{H-PAD}" stroke="#333"/>
<text x="{W/2}" y="{H-32}" text-anchor="middle" font-size="12">Time: 0–359 s</text>
{''.join(lines)}
</svg>'''

def main():
    rows=simulate(); out=Path("artifacts"); out.mkdir(exist_ok=True)
    (out/"day2_pressure.svg").write_text(svg("Header pressure response",[("PT-001 model head",[r["header_head_m"] for r in rows]),("Setpoint",[r["setpoint_head_m"] for r in rows])],0,60,"Head (m)"))
    (out/"day2_control.svg").write_text(svg("VSD speed and pump staging",[("VSD speed x5",[r["speed_pu"]*5 for r in rows]),("Pumps running",[r["pumps_running"] for r in rows])],0,5.5,"Scaled speed / pump count"))
    (out/"day2_power.svg").write_text(svg("Calculated shaft power",[("Total power",[r["total_power_kw"] for r in rows])],0,110,"Power (kW)"))
    print("Generated Day-2 SVG plots in artifacts/")
if __name__=="__main__": main()
