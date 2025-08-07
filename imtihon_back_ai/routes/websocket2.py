import cv2
import numpy as np
from fastapi import APIRouter, WebSocket
import mediapipe as mp

router = APIRouter()

# Mediapipe FaceMesh setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Landmark indices
LEFT_EYE_IDXS = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_IDXS = [33, 160, 158, 133, 153, 144]
NOSE_IDX = 1

# Thresholds
EAR_THRESHOLD = 0.2  # Eyes closed if EAR < this
HEAD_MOVEMENT_THRESHOLD = 15  # Head moved if nose moved > X pixels


def compute_ear(pts):
    """Compute Eye Aspect Ratio (EAR) from 6 eye landmarks."""
    A = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    B = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    C = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    return (A + B) / (2.0 * C)


def get_landmark_points(landmarks, indices, w, h):
    """Convert normalized Mediapipe landmarks to pixel coordinates."""
    return [
        (int(landmarks.landmark[i].x * w), int(landmarks.landmark[i].y * h))
        for i in indices
    ]


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
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

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            eye_status = "Unknown"
            avg_ear = 0.0

            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                h, w, _ = frame.shape

                # Track nose for head movement
                nose = face_landmarks.landmark[NOSE_IDX]
                nose_x, nose_y = int(nose.x * w), int(nose.y * h)

                if prev_nose_pos:
                    dx = abs(nose_x - prev_nose_pos[0])
                    dy = abs(nose_y - prev_nose_pos[1])
                    if dx > HEAD_MOVEMENT_THRESHOLD or dy > HEAD_MOVEMENT_THRESHOLD:
                        head_moved = True
                prev_nose_pos = (nose_x, nose_y)

                # Eyes
                left_eye_pts = get_landmark_points(face_landmarks, LEFT_EYE_IDXS, w, h)
                right_eye_pts = get_landmark_points(
                    face_landmarks, RIGHT_EYE_IDXS, w, h
                )

                left_ear = compute_ear(left_eye_pts)
                right_ear = compute_ear(right_eye_pts)
                avg_ear = (left_ear + right_ear) / 2.0

                eye_status = "Closed" if avg_ear < EAR_THRESHOLD else "Open"

                # Blink tracking + liveness
                if eye_status == "Closed":
                    eyes_were_closed = True
                elif eyes_were_closed and eye_status == "Open":
                    if head_moved:
                        is_alive = True

                # Draw landmarks
                for pt in left_eye_pts + right_eye_pts:
                    cv2.circle(frame, pt, 2, (0, 255, 0), -1)

                # Draw nose point
                cv2.circle(frame, (nose_x, nose_y), 4, (255, 0, 0), -1)

                # Display text
                cv2.putText(
                    frame,
                    f"Eye: {eye_status}",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    f"EAR: {avg_ear:.2f}",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2,
                )
                cv2.putText(
                    frame,
                    f"Head moved: {head_moved}",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2,
                )

            if is_alive:
                cv2.putText(
                    frame,
                    "Liveness Confirmed",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )

            _, buffer = cv2.imencode(".jpg", frame)
            await websocket.send_bytes(buffer.tobytes())

    except Exception as e:
        print("WebSocket closed or error:", e)
        await websocket.close()
