import hashlib
import json
from pathlib import Path

bdir = Path("outputs/controlled_benchmark")
manifest = json.loads((bdir / "benchmark_manifest.json").read_text(encoding="utf-8"))

for fname, exp_hash in manifest.get("files_sha256", {}).items():
    fpath = bdir / fname
    if fpath.exists():
        actual_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()
        match = (actual_hash == exp_hash)
        print(f"{fname}: match={match}")
        if not match:
            print(f"  Expected: {exp_hash}")
            print(f"  Actual:   {actual_hash}")
    else:
        print(f"{fname}: FILE NOT FOUND")
