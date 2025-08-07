from fastapi import APIRouter, WebSocket, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from models.yolo_model import model, COCO_CLASSES
from celery_config.tasks import send_evidence
from fastapi import WebSocket, Query

router = APIRouter()

TARGET_CLASSES = {"person", "cell phone", "book"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str = Query(...)):
    await websocket.accept()
    try:
        while True:
            # data = await websocket.receive_text()
            data = await websocket.receive_bytes()
            npimg = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            # YOLO detection
            results = model(
                frame,
                stream=True,
                imgsz=360,
                conf=0.5,
                device="cuda:0",  # if torch.cuda.is_available() else "cpu",
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
            # Overlay warning if needed
            person_count = sum(1 for d in detections if d["class"] == "person")
            phone_book = any(d["class"] in ["cell phone", "book"] for d in detections)
            if person_count > 1 or phone_book:
                overlay = frame.copy()
                cv2.rectangle(
                    overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), -1
                )
                alpha = 0.35
                cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # Send ONLY the base64 JPEG (not as JSON!)
            _, buffer = cv2.imencode(".jpg", frame)

            if person_count > 1 or phone_book:

                send_evidence.delay(
                    person_count > 1, phone_book, buffer.tobytes(), session_id
                )
            # b64img = base64.b64encode(buffer).decode("utf-8")
            # await websocket.send_text(b64img)
            await websocket.send_bytes(buffer.tobytes())  # Send raw JPEG binary bytes

    except Exception as e:
        print("WebSocket closed or error:", e)
        await websocket.close()
