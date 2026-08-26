from pathlib import Path

exec((Path(__file__).resolve().parents[1] / "app.py").read_text())
