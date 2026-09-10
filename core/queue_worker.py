import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if not os.environ.get("AI_LOCAL_MODEL_PATH"):
    local_model = ROOT / "trained_model_vscode1"
    if local_model.exists():
        os.environ["AI_LOCAL_MODEL_PATH"] = str(local_model)

from services.queue_worker import main

if __name__ == "__main__":
    raise SystemExit(main())
