from flask import Flask, request, redirect
import os

app = Flask(__name__)

STATUS_FILE = "status.txt"

def read_status():
    if os.path.exists(STATUS_FILE):
        val = open(STATUS_FILE).read().strip()
        if val in ("on", "off"):
            return val
    return "off"

def write_status(val):
    with open(STATUS_FILE, "w") as f:
        f.write(val)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Robo Hand</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: monospace;
      background: #ffffff;
      color: #000000;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      gap: 32px;
    }}
    .status-line {{
      display: flex;
      align-items: baseline;
      gap: 12px;
      font-size: 2.4rem;
      font-weight: bold;
    }}
    .status-label {{
      color: #000000;
    }}
    .status-value {{
      color: {color};
    }}
    .btn {{
      display: inline-block;
      text-decoration: none;
      font-family: monospace;
      font-size: 0.9rem;
      letter-spacing: 0.1em;
      padding: 10px 32px;
      border: 1px solid {btn_color};
      color: {btn_color};
      background: transparent;
      transition: background 0.15s, color 0.15s;
    }}
    .btn:hover {{
      background: {btn_color};
      color: #ffffff;
    }}
  </style>
</head>
<body>
  <div class="status-line">
    <span class="status-label">Status:</span>
    <span class="status-value">{status}</span>
  </div>
  <a class="btn" href="/main.py?knopka={action}">{label}</a>
</body>
</html>"""

@app.route("/main.py")
def index():
    knopka = request.args.get("knopka")
    if knopka in ("on", "off"):
        write_status(knopka)
        return redirect("/main.py")

    status = read_status()

    if status == "on":
        color, btn_color, action, label = "#4caf50", "#f44336", "off", "ВЫКЛЮЧИТЬ"
    else:
        color, btn_color, action, label = "#f44336", "#4caf50", "on", "ВКЛЮЧИТЬ"

    return HTML.format(status=status.upper(), color=color,
                       btn_color=btn_color, action=action, label=label)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)