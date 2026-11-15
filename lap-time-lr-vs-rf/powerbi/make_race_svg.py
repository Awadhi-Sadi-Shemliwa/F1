"""Animated race-strip SVG used in the Power BI header (Insert > Image). Same template that was injected in the browser."""
W, H = 760, 92
dashes = "".join(f'<rect x="{k*120}" y="44.5" width="60" height="3" rx="1.5" fill="#C8CDD7" opacity="0.55"/>' for k in range(9))
kerbs = ""
for k in range(22):
    c = "#E10600" if k % 2 == 0 else "#EDEDED"
    kerbs += f'<rect x="{k*40}" y="0" width="40" height="4" fill="{c}"/><rect x="{k*40}" y="86" width="40" height="6" fill="{c}"/>'
st = [(12,0.9,70),(22,1.3,40),(31,0.7,90),(58,1.1,60),(67,0.8,50),(76,1.5,80),(18,1.0,30),(52,0.6,45)]
streaks = "".join(f'<line x1="0" y1="{y}" x2="{L}" y2="{y}" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.2"><animateTransform attributeName="transform" type="translate" from="{W+20} 0" to="{-L-20} 0" dur="{d}s" begin="{i*0.17:.2f}s" repeatCount="indefinite"/></line>' for i,(y,d,L) in enumerate(st))
def wheel(cx):
    return (f'<g transform="translate({cx},-14)"><circle r="14" fill="#0E0E10"/><circle r="7.7" fill="#464A54"/><g>'
            '<line x1="0" y1="0" x2="7" y2="0" stroke="#AAB0BC" stroke-width="1.6"/><line x1="0" y1="0" x2="-3.5" y2="6" stroke="#AAB0BC" stroke-width="1.6"/>'
            '<line x1="0" y1="0" x2="-3.5" y2="-6" stroke="#AAB0BC" stroke-width="1.6"/>'
            '<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="0.25s" repeatCount="indefinite"/></g></g>')
def car(col, label):
    return (f'<g transform="scale(0.62)"><ellipse cx="70" cy="1" rx="88" ry="4.5" fill="#000" opacity="0.5"/>'
            f'<polygon points="-14,-34 6,-34 6,-27 -14,-27" fill="{col}"/><rect x="-4" y="-27" width="5" height="11" fill="#14161C"/>'
            f'<polygon points="-6,-20 40,-24 62,-30 80,-24 140,-13 152,-9 150,-6 100,-7 20,-8 -6,-10" fill="{col}"/>'
            '<polygon points="30,-13 120,-11 150,-7 30,-8" fill="#FFFFFF" opacity="0.25"/>'
            '<ellipse cx="63" cy="-31" rx="7" ry="6" fill="#F5F5F5"/><rect x="58" y="-33" width="11" height="3" fill="#14161C"/>'
            '<polyline points="48,-31 64,-39 80,-27" fill="none" stroke="#14161C" stroke-width="2.4"/>'
            '<rect x="128" y="-6" width="30" height="4" fill="#14161C"/>' + wheel(8) + wheel(118) +
            f'<text x="86" y="-14" font-family="Segoe UI, Arial, sans-serif" font-weight="700" font-size="12" fill="#FFFFFF">{label}</text>'
            '<rect x="-17" y="-22" width="5" height="4" fill="#E10600"><animate attributeName="opacity" values="1;0.1;1" dur="0.4s" repeatCount="indefinite"/></rect></g>')
lights = "".join(f'<circle cx="{590+i*24}" cy="58" r="8" fill="#3C1414"><animate attributeName="fill" values="#3C1414;#E10600;#3C1414" keyTimes="0;{(i+1)*0.12:.2f};0.75" calcMode="discrete" dur="3s" repeatCount="indefinite"/></circle>' for i in range(5))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><linearGradient id="asph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151922"/><stop offset="1" stop-color="#0D1016"/></linearGradient></defs>
<rect width="{W}" height="{H}" rx="10" fill="url(#asph)"/>
<g>{dashes}<animateTransform attributeName="transform" type="translate" from="0 0" to="-120 0" dur="0.35s" repeatCount="indefinite"/></g>
<g>{kerbs}<animateTransform attributeName="transform" type="translate" from="0 0" to="-80 0" dur="0.25s" repeatCount="indefinite"/></g>
{streaks}
<g transform="translate(200,50)"><g><animateTransform attributeName="transform" type="translate" values="0 0;90 0;140 0;60 0;0 0" dur="6s" repeatCount="indefinite"/>{car('#38A3FF','LR')}</g></g>
<g transform="translate(250,84)"><g><animateTransform attributeName="transform" type="translate" values="40 0;110 0;60 0;-20 0;40 0" dur="6s" repeatCount="indefinite"/>{car('#FF7A2F','RF')}</g></g>
<text x="590" y="30" font-family="Segoe UI, Arial, sans-serif" font-weight="700" font-size="13" fill="#FFFFFF" letter-spacing="2">LIGHTS OUT</text>
{lights}
</svg>'''
open("assets/race_strip.svg", "w").write(svg)
print(len(svg))
