# tasks.py
from celery_config.celery_worker import celery_app
from io import BytesIO
import uuid
import requests


@celery_app.task(name="celery_config.tasks.send_evidence")
def send_evidence(
    is_many_people: bool, is_device_used: bool, evidence_file: bytes, session_id: int
):
    try:
        print(f"🔔 Celery task received: {session_id}")
        print(f"📌 is_many_people: {is_many_people}")
        print(f"📌 is_device_used: {is_device_used}")
        print(f"📦 evidence_file size: {len(evidence_file)} bytes")
    except Exception as e:
        print("❌ Error in send_evidence task:", str(e))
        raise

    url = "http://django:8000/imtihon/crud/api/students/evidence/"
    header = {
        "X-API-KEY": "52953885efcce046770bc5c576bab385763641cfb9c9ae1b8509111394106998",
    }

    file = BytesIO(evidence_file)
    file_name = f"frame_{uuid.uuid4()}.jpg"
    files = {"evidence_file": (file_name, file, "image/jpeg")}

    data = {"type": "device", "session": session_id}

    response = requests.post(url, files=files, data=data, headers=header)

    print("Status:", response.status_code)
    print("Response:", response.text)


@celery_app.task(name="celery_config.tasks.send_liveness")
def send_liveness(session_id: int, is_live: bool):
    url = "http://django:8000/imtihon/crud/api/students/evidence/live-check/"
    header = {
        "X-API-KEY": "52953885efcce046770bc5c576bab385763641cfb9c9ae1b8509111394106998",
        "Content-Type": "application/json",
    }

    # 🔧 Use the correct key name: session_id
    data = {"is_live": is_live, "session_id": session_id}

    response = requests.post(url, json=data, headers=header)

    print("Status:", response.status_code)
    print("Response:", response.text)
