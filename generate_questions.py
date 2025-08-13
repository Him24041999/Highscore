import re, os, textwrap
from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

SRC_MD = "ML-Official-T1-Math-01.md"
OUT_DIR = Path("ml_official_t1_math_outputs")
OUT_DIR.mkdir(exist_ok=True)

def make_placeholder(text, outfile, size=(900, 400)):
    img = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 22)
        small = ImageFont.truetype("DejaVuSans.ttf", 18)
    except:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    margin, y = 20, 20
    draw.text((margin, y), "Figure unavailable", fill="black", font=font)
    y += 40
    for line in textwrap.wrap(text, width=80):
        draw.text((margin, y), line, fill="black", font=small)
        y += 26
    img.save(outfile)

with open(SRC_MD, "r", encoding="utf-8") as f:
    md = f.read()

pattern = re.compile(r"(?m)^\s*(\d+)\.\s*(.*?)(?=^\s*\d+\.\s*|\Z)", re.DOTALL)
blocks = pattern.findall(md)

questions = []
for num, block in blocks:
    num = int(num)
    imgs = re.findall(r"!\[.*?\]\((.*?)\)", block)
    options = []
    for letter in ["A", "B", "C", "D", "E"]:
        m = re.search(rf"\({letter}\)\s*(.+?)(?=(\([A-E]\))|\Z)", block, re.DOTALL)
        if m:
            options.append(m.group(1).strip())
    stem = re.split(r"\(A\)", block, maxsplit=1)[0].strip()
    questions.append({"number": num, "stem": stem, "options": options, "images": imgs})

solutions = {
    1:"A", 2:None, 3:"E", 4:"B", 5:"E", 6:None, 7:"C", 8:"B", 9:"A", 10:"D",
    11:None, 12:"E", 13:"A", 14:"C", 15:"E", 16:"D", 17:None, 18:"E", 19:None,
    20:"D", 21:None, 22:"A", 23:"D", 24:"A", 25:"E"
}
explanations = {
    1:"n + 5 = 5 ⇒ n = 0.",
    2:"Needs figure to determine sequence.",
    3:"20 + x illustrations.",
    4:"4□86 < 4486 ⇒ □ = 3.",
    5:"3/8 + 4/7 = 53/56.",
    6:"Needs figure for altitude difference.",
    7:"0.5 × 23.5 × 0.2 = 2.35.",
    8:"25 + 10 + 1 = 36 using 3 coins.",
    9:"(1/2) × (1/4) = 1/8.",
    10:"SV = 36 after midpoint calculations.",
    11:"Question text corrupted.",
    12:"4 shirts × 3 pants = 12.",
    13:"3n - 1 is always even for odd n.",
    14:"$40 covers 290 miles.",
    15:"3/8 = 0.375 closest to 37%.",
    16:"Smallest club has 33 students.",
    17:"Needs figure for shaded region.",
    18:"5 gold ⇒ 90 copper coins.",
    19:"Needs figure for geometry.",
    20:"Result = 28 after order of operations.",
    21:"Needs figure for hole/card positions.",
    22:"(3n)/2 is integer if n is even.",
    23:"Book has 120 pages.",
    24:"Circumference = 12π.",
    25:"Price after changes = 126."
}

html_parts = [
    "<html><head><meta charset='utf-8'><title>Math Solutions</title>",
    "<style>body{font-family:Arial;max-width:900px;margin:40px auto;} .q{border:1px solid #ccc;padding:10px;margin:10px 0;border-radius:8px}</style></head><body>",
    "<h1>Math Answer Report</h1>"
]
csv_rows = []

for q in questions:
    num = q["number"]
    html_parts.append(f"<div class='q'><h2>Q{num}</h2><p>{q['stem']}</p>")
    if q["images"]:
        placeholder_path = OUT_DIR / f"q{num:02d}_placeholder.png"
        make_placeholder(f"Question {num} needs the original figure.", placeholder_path)
        html_parts.append(f"<img src='{placeholder_path.name}' style='max-width:100%;'>")
    if q["options"]:
        html_parts.append("<ul>" + "".join([f"<li>({chr(65+i)}) {opt}</li>" for i,opt in enumerate(q["options"])]) + "</ul>")
    ans = solutions.get(num)
    expl = explanations.get(num, "—")
    html_parts.append(f"<p><b>Answer:</b> {ans if ans else 'Needs figure'}</p>")
    html_parts.append(f"<p><b>Explanation:</b> {expl}</p></div>")
    csv_rows.append({"Question": num, "Answer": ans if ans else "Needs figure", "Explanation": expl})

html_parts.append("</body></html>")

with open(OUT_DIR / "solutions.html", "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))
pd.DataFrame(csv_rows).to_csv(OUT_DIR / "answers.csv", index=False)

print(f"Report saved to: {OUT_DIR/'solutions.html'}")
print(f"CSV saved to: {OUT_DIR/'answers.csv'}")
