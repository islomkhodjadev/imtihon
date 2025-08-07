from ultralytics import YOLO

model = YOLO("yolov8n.pt")
COCO_CLASSES = model.model.names
