"""Refresh the two-row IMDb aggregate-rating extract without retaining raw data."""

from __future__ import annotations

import csv
import gzip
import io
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "tables" / "movie_lab_imdb_aggregate_ratings.csv"
URL = "https://datasets.imdbws.com/title.ratings.tsv.gz"
FILMS = {
    "tt10872600": "Spider-Man: No Way Home",
    "tt1517268": "Barbie",
}


def main() -> None:
    request = Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=90) as response:
        compressed = response.read()
    text = gzip.decompress(compressed).decode("utf-8")
    reader = csv.DictReader(io.StringIO(text), delimiter="\t")
    selected = [row for row in reader if row["tconst"] in FILMS]
    selected.sort(key=lambda row: row["tconst"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "tconst",
                "averageRating",
                "numVotes",
                "film",
                "retrieved_date",
                "temporal_use",
            ]
        )
        for row in selected:
            writer.writerow(
                [
                    row["tconst"],
                    row["averageRating"],
                    row["numVotes"],
                    FILMS[row["tconst"]],
                    date.today().isoformat(),
                    "Post-release descriptive assurance only; not a tradable signal",
                ]
            )
    print(f"Wrote {len(selected)} aggregate rating rows to {OUTPUT}")


if __name__ == "__main__":
    main()

