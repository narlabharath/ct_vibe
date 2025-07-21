"""
File-Based Chat System API Routes
=================================
This module defines API endpoints for user authentication, file uploads, session management, and chat interactions.
All session and file operations are performed for the hardcoded user 'testuser'.
"""


# =========================
# Imports
# =========================
import os
import glob
from datetime import datetime
from typing import Dict, Tuple, List, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.session import save_session_metadata





# =========================
# Pydantic Models
# =========================
class LoginRequest(BaseModel):
    """
    Model for login request payload.
    """
    username: str
    password: str

class QueryRequest(BaseModel):
    """
    Model for chat query request payload.
    """
    session_id: str
    question: str

class RenameSessionRequest(BaseModel):
    """
    Model for session rename request payload.
    """
    new_name: str


# =========================
# Router Initialization
# =========================
router = APIRouter()


# =========================
# Auth Endpoints
# =========================
@router.post(
    "/login",
    tags=["Auth"],
    summary="Simulated login endpoint",
    response_description="Fixed user_id for demonstration."
)
def login(request: LoginRequest) -> Dict[str, str]:
    """
    Simulate user authentication and return a fixed user_id.
    """
    return {"user_id": "testuser"}

 # =========================
# Session Endpoints
# =========================
@router.post(
    "/sessions/{session_id}/rename",
    tags=["Session"],
    summary="Rename a session",
    response_description="Success message with session_id and new name."
)
def rename_session(session_id: str, request: RenameSessionRequest):
    """
    Rename a session by updating the session_name in metadata.json for the given session_id.
    Returns a success message with session_id and new name.
    Handles file not found and JSON errors.
    """
    import json
    import re
    import shutil
    from datetime import datetime
    user_id = "testuser"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    sessions_base = os.path.join(BASE_DIR, "backend", "sessions", user_id)
    old_session_dir = os.path.join(sessions_base, session_id)
    meta_path = os.path.join(old_session_dir, "metadata.json")
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail=f"Session metadata not found for session_id: {session_id}")
    try:
        with open(meta_path, "r") as f:
            meta = json.load(f)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session metadata JSON.")

    # Slugify new_name and append timestamp for uniqueness
    def slugify(value):
        value = re.sub(r'[^a-zA-Z0-9\-_]+', '-', value.strip().lower())
        value = re.sub(r'-+', '-', value)
        return value.strip('-_')
    slug = slugify(request.new_name)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_session_id = f"{slug}_{timestamp}"
    new_session_dir = os.path.join(sessions_base, new_session_id)

    # Check for folder conflict
    if os.path.exists(new_session_dir):
        raise HTTPException(status_code=409, detail=f"A session with the name '{request.new_name}' already exists at this time.")

    # Rename the folder
    try:
        shutil.move(old_session_dir, new_session_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rename session folder: {e}")

    # Update metadata.json with new session_id and session_name
    meta["session_id"] = new_session_id
    meta["session_name"] = request.new_name
    new_meta_path = os.path.join(new_session_dir, "metadata.json")
    try:
        with open(new_meta_path, "w") as f:
            json.dump(meta, f, indent=2)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save updated session metadata.")

    return {
        "message": "Session renamed successfully",
        "session_id": new_session_id,
        "session_name": request.new_name
    }


@router.get(
    "/sessions",
    tags=["Session"],
    summary="List all sessions for the current user",
    response_description="List of session metadata."
)
def list_sessions() -> List[Dict[str, Any]]:
    """
    List all sessions for the hardcoded user 'testuser'.
    Reads metadata.json from each session folder and returns a list of session metadata.
    """
    import json
    user_id = "testuser"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    sessions_dir = os.path.join(BASE_DIR, "backend", "sessions", user_id)
    print(f"[DEBUG] Looking for sessions in: {sessions_dir}")
    if not os.path.exists(sessions_dir):
        print(f"Session dir not found: {sessions_dir}")
        return []
    session_metas = []
    for session_path in glob.glob(os.path.join(sessions_dir, "*/metadata.json")):
        try:
            with open(session_path, "r") as f:
                print(f"Reading session metadata from: {session_path}")
                meta = json.load(f)
                session_metas.append({
                    "session_id": meta.get("session_id"),
                    "session_name": meta.get("session_name"),
                    "created_at": meta.get("created_at"),
                    "filenames": meta.get("filenames", [])
                })
        except Exception:
            continue
    return session_metas

@router.get(
    "/sessions/{session_id}/files",
    tags=["Session"],
    summary="List all files in a session",
    response_description="List of files with filename and size in bytes."
)
def list_session_files(session_id: str) -> Any:
    """
    List all files in the files/ subdirectory of a session for the hardcoded user 'testuser'.
    Returns a list of dicts with filename and size in bytes.
    """
    user_id = "testuser"
    import json
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    files_dir = os.path.join(BASE_DIR, "backend", "sessions", user_id, session_id, "files")
    print(f"[DEBUG] Looking for files in: {files_dir}")
    if not os.path.exists(files_dir):
        return {"error": f"Session or files directory not found: {files_dir}"}
    file_list = []
    for fname in os.listdir(files_dir):
        fpath = os.path.join(files_dir, fname)
        if os.path.isfile(fpath):
            file_list.append({
                "filename": fname,
                "size": os.path.getsize(fpath)
            })
    return {"files": file_list}

@router.get(
    "/sessions/{session_id}/files/{filename}",
    tags=["Session"],
    summary="Get a file from a session",
    response_description="Stream the file content or download it."
)
def get_session_file(session_id: str, filename: str, download: bool = False):
    """
    Return the file content for the specified file in the session's files/ directory.
    If download=true, set Content-Disposition: attachment.
    Return 404 if file is not found.
    """
    user_id = "testuser"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    file_path = os.path.join(BASE_DIR, "backend", "sessions", user_id, session_id, "files", filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    headers = None
    if download:
        headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return FileResponse(file_path, headers=headers)

@router.post(
    "/upload",
    tags=["Session"],
    summary="Upload files and start a new session",
    response_description="Session ID and list of uploaded filenames."
)
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload multiple files, create a new session folder, save files, and store session metadata.
    Assumes user_id = 'testuser'.
    """
    user_id = "testuser"
    session_id, files_folder = create_session_folder(user_id)
    filenames = []
    for upload in files:
        file_location = os.path.join(files_folder, upload.filename)
        with open(file_location, "wb") as f:
            content = await upload.read()
            f.write(content)
        filenames.append(upload.filename)
    session_dir = os.path.dirname(files_folder)
    save_session_metadata(session_id, user_id, filenames, session_dir)
    return {"session_id": session_id, "filenames": filenames}

# =========================
# Chat Endpoints
# =========================
@router.post(
    "/query",
    tags=["Chat"],
    summary="Query a session with a question",
    response_description="Mocked answer and chat log update."
)
def query_session(request: QueryRequest):
    """
    Accepts a session_id and question, returns a mocked answer, and appends the Q&A to chat.json in the session folder.
    Now returns output as an ordered list of text and plot events.
    """
    import json, io, contextlib, base64, glob, os, sys
    import matplotlib.pyplot as plt
    import pandas as pd
    user_id = "testuser"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    session_dir = os.path.join(BASE_DIR, "backend", "sessions", user_id, request.session_id)
    chat_path = os.path.join(session_dir, "chat.json")
    # Prepare ordered output list
    output_events = []
    # Patch plt.show to capture plots as events
    original_show = plt.show
    def capture_show(*args, **kwargs):
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        encoded_img = base64.b64encode(buf.read()).decode('utf-8')
        output_events.append({"type": "plot", "content": f"data:image/png;base64,{encoded_img}"})
        plt.close()
    plt.show = capture_show
    # Patch sys.stdout.write to capture text as events
    original_write = sys.stdout.write
    def capture_write(text):
        if text.strip():
            output_events.append({"type": "text", "content": text})
        return original_write(text)
    sys.stdout.write = capture_write
    try:
        # Scenario: text1, plot1, text2
        print("Note: File reading is temporarily disabled. Showing mock output only.\n")
        print(f"This is a placeholder response for: {request.question}\n")
        print("Now generating a plot...\n")
        plt.figure()
        import numpy as np
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        plt.plot(x, y)
        plt.title("Placeholder sine wave plot")
        plt.show()
        print("Plot generated above.\n")
        print("End of response.\n")
    finally:
        plt.show = original_show  # Restore
        sys.stdout.write = original_write
    answer = {
        "events": output_events
    }
    # Load chat log
    chat_log = []
    if os.path.exists(chat_path):
        try:
            with open(chat_path, "r") as f:
                chat_log = json.load(f)
        except Exception:
            chat_log = []
    from datetime import datetime
    chat_log.append({
        "question": request.question,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })
    with open(chat_path, "w") as f:
        json.dump(chat_log, f, indent=2)
    return {"answer": answer}

@router.get(
    "/sessions/{session_id}/chat",
    tags=["Chat"],
    summary="Get chat log for a session",
    response_description="List of questions and answers with timestamps."
)
def get_chat_log(session_id: str):
    """
    Returns the list of questions and answers (with timestamps) from chat.json in the session folder.
    If the file does not exist, returns an empty list.
    """
    import json
    user_id = "testuser"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    session_dir = os.path.join(BASE_DIR, "backend", "sessions", user_id, session_id)
    chat_path = os.path.join(session_dir, "chat.json")
    if not os.path.exists(chat_path):
        return []
    try:
        with open(chat_path, "r") as f:
            chat_log = json.load(f)
        result = []
        for entry in chat_log:
            result.append({
                "question": entry.get("question"),
                "answer": entry.get("answer"),
                "timestamp": entry.get("timestamp")
            })
        return result
    except Exception:
        return []
# =========================
# Delete Session Endpoint
# =========================
from fastapi import status

@router.delete(
    "/sessions/{session_id}",
    tags=["Session"],
    summary="Delete a session and its files",
    response_description="Session deleted successfully."
)
def delete_session(session_id: str):
    """
    Delete the session folder and all its contents for the hardcoded user 'testuser'.
    """
    import shutil
    user_id = "testuser"
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    session_dir = os.path.join(BASE_DIR, "backend", "sessions", user_id, session_id)
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail=f"Session not found: {session_id}")
    try:
        shutil.rmtree(session_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {e}")
    return {"message": "Session deleted successfully", "session_id": session_id}


# =========================
# Helper Functions
# =========================
def create_session_folder(user_id: str) -> Tuple[str, str]:
    """
    Generates a timestamped session_id, creates the session folders, and returns (session_id, full_path_to_files_folder).

    Args:
        user_id (str): The user identifier.

    Returns:
        Tuple[str, str]: (session_id, absolute path to files folder)
    """
    session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    base_path = os.path.join("sessions", user_id, session_id)
    files_path = os.path.join(base_path, "files")
    os.makedirs(files_path, exist_ok=True)
    return session_id, os.path.abspath(files_path)



