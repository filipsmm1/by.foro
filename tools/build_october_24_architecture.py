"""Build three original architecture guides with reviewed project imagery."""
import json
from pathlib import Path
import build_september_27_architecture as builder

builder.DATE = "2026-10-24"
builder.base.PUBLISHED = builder.DATE
builder.base.PUBLISHED_LABEL = "24 October 2026"
builder.base.PUBLISHED_ISO = builder.DATE + "T12:00:00+02:00"
builder.STORIES = json.loads((Path(__file__).parent / "october_24_architecture.json").read_text(encoding="utf-8"))

if __name__ == "__main__":
    builder.main()
