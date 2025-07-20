import os
import json
from datetime import datetime
from typing import List

def save_session_metadata(session_id: str, user_id: str, filenames: List[str], session_dir: str) -> None:
    """
    Save session metadata as metadata.json in the given session_dir.
    """
    metadata = {
        "session_id": session_id,
        "user_id": user_id,
        "filenames": filenames,
        "created_at": datetime.now().isoformat(),
        "session_name": session_id  # Default session name is the session_id
    }
    metadata_path = os.path.join(session_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
