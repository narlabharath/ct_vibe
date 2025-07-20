import requests

API_BASE = "http://localhost:8000"

def login(username, password):
    return requests.post(f"{API_BASE}/login", json={"username": username, "password": password})

def upload_files(files):
    # files: list of (filename, fileobj)
    return requests.post(f"{API_BASE}/upload", files=files)

def list_sessions():
    return requests.get(f"{API_BASE}/sessions")

def list_files(session_id):
    return requests.get(f"{API_BASE}/sessions/{session_id}/files")

def get_file(session_id, filename):
    return requests.get(f"{API_BASE}/sessions/{session_id}/files/{filename}")

def query(session_id, question):
    return requests.post(f"{API_BASE}/query", json={"session_id": session_id, "question": question})

def get_chat(session_id):
    return requests.get(f"{API_BASE}/sessions/{session_id}/chat")

def rename_session(session_id, new_name):
    return requests.post(f"{API_BASE}/sessions/{session_id}/rename", json={"new_name": new_name})
