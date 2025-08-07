from fastapi import APIRouter, WebSocket, Query
import numpy as np
import cv2
from models.yolo_model import model, COCO_CLASSES
from celery_config.tasks import send_evidence, send_liveness
import mediapipe as mp

router = APIRouter()

# YOLO target classes
TARGET_CLASSES = {"person", "cell phone", "book"}

# Mediapipe FaceMesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Landmark indices for liveness detection
LEFT_EYE_IDXS = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_IDXS = [33, 160, 158, 133, 153, 144]
NOSE_IDX = 1

# Liveness detection thresholds
EAR_THRESHOLD = 0.2
HEAD_MOVEMENT_THRESHOLD = 15


def compute_ear(pts):
    A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    return (A + B) / (2.0 * C)


def get_landmark_points(landmarks, indices, w, h):
    return [
        (int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h))
        for i in indices
    ]


sent_evidence_sessions = set()
sent_liveness_sessions = set()


@router.websocket("/imtihon/ai/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str = Query(...)):
    await websocket.accept()

    eyes_were_closed = False
    head_moved = False
    is_alive = False
    prev_nose_pos = None

    try:
        while True:
            data = await websocket.receive_bytes()
            npimg = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            h, w, _ = frame.shape

            # ----------------- LIVENESS DETECTION -----------------
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                for idx in LEFT_EYE_IDXS + RIGHT_EYE_IDXS + [NOSE_IDX]:
                    landmark = face_landmarks.landmark[idx]
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)  # yellow dots

                # Nose movement
                nose = face_landmarks.landmark[NOSE_IDX]
                nose_x, nose_y = int(nose.x * w), int(nose.y * h)
                if prev_nose_pos:
                    dx = abs(nose_x - prev_nose_pos[0])
                    dy = abs(nose_y - prev_nose_pos[1])
                    if dx > HEAD_MOVEMENT_THRESHOLD or dy > HEAD_MOVEMENT_THRESHOLD:
                        head_moved = True
                prev_nose_pos = (nose_x, nose_y)

                # Eye Aspect Ratio (EAR)
                left_eye_pts = get_landmark_points(face_landmarks, LEFT_EYE_IDXS, w, h)
                right_eye_pts = get_landmark_points(
                    face_landmarks, RIGHT_EYE_IDXS, w, h
                )

                left_ear = compute_ear(left_eye_pts)
                right_ear = compute_ear(right_eye_pts)
                avg_ear = (left_ear + right_ear) / 2.0
                eye_status = "Closed" if avg_ear < EAR_THRESHOLD else "Open"

                if eye_status == "Closed":
                    eyes_were_closed = True
                elif eyes_were_closed and eye_status == "Open" or head_moved:
                    is_alive = True

            # ----------------- YOLO OBJECT DETECTION -----------------
            results = model(
                frame, stream=True, imgsz=384, conf=0.5, device="cpu"  # "cuda:0",
            )

            detections = []
            for result in results:
                for box in result.boxes.cpu().numpy():
                    cls_id = int(box.cls[0])
                    class_name = COCO_CLASSES[cls_id]
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    if class_name in TARGET_CLASSES and conf > 0.5:
                        detections.append(
                            {
                                "class": class_name,
                                "conf": conf,
                                "bbox": [x1, y1, x2, y2],
                            }
                        )
                        color = (0, 255, 0) if class_name == "person" else (255, 0, 0)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(
                            frame,
                            f"{class_name} {conf:.2f}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            color,
                            2,
                        )

            # Highlight if violations occur
            person_count = sum(1 for d in detections if d["class"] == "person")
            phone_or_book = any(
                d["class"] in ["cell phone", "book"] for d in detections
            )
            if person_count > 1 or phone_or_book:
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
                cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)

            # Add liveness confirmation overlay
            if is_alive and session_id not in sent_liveness_sessions:
                cv2.putText(
                    frame,
                    "Liveness Confirmed",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )
                send_liveness.delay(session_id, True)
                sent_liveness_sessions.add(session_id)
            # Encode & send frame
            _, buffer = cv2.imencode(".jpg", frame)
            if (
                person_count > 1
                or phone_or_book
                and session_id not in sent_evidence_sessions
            ):
                send_evidence.delay(
                    person_count > 1, phone_or_book, buffer.tobytes(), session_id
                )
                sent_evidence_sessions.add(session_id)

            await websocket.send_bytes(buffer.tobytes())

    except Exception as e:
        print("WebSocket closed or error:", e)
        await websocket.close()
