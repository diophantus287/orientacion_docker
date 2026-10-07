import csv
import os
from pathlib import Path

from flask import Flask, render_template


app = Flask(__name__)
CSV_PATH = Path(os.environ.get("CSV_PATH", "/app/data/analisis_puntuacion_global.csv"))


def load_results():
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        headers = [
            "Orden" if header == "Orden calculado" else header
            for header in (reader.fieldnames or [])
            if header not in {"DNI", "Orden oficial"}
        ]
        results = []
        for row in reader:
            row["Nombre"] = row.get("Nombre", "").split(",", 1)[-1].strip()
            row["Orden"] = row.get("Orden calculado", "")
            results.append(row)
        return headers, results


@app.route("/")
def index():
    headers, results = load_results()
    selected_count = sum(row.get("Seleccionado oficial") == "Sí" for row in results)
    return render_template(
        "index.html",
        headers=headers,
        results=results,
        total=len(results),
        selected_count=selected_count,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)