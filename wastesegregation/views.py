
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import base64
import asyncio
import time
from ultralytics import YOLO
import supervision as sv

model = YOLO(r'WasteSegregation/model')
box_annotator = None

cap = cv2.VideoCapture(0)

async def read_camera(websocket):
    global box_annotator
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame
        if box_annotator is None:
            box_annotator = sv.BoxAnnotator(
                thickness=2,
                text_thickness=2,
                text_scale=1
            )

        excluded_classes = [25,24,23]
        
        start_time = time.perf_counter()
        
        result = model(frame, agnostic_nms=True)[0]
            
        detections = sv.Detections.from_yolov8(result)
        
        filtered_detections = [
            detection for detection in detections
            if detection[1] >=0.2 and detection[2] not in excluded_classes
        ]
        
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in filtered_detections
        ]
        
        frame = box_annotator.annotate(scene=frame, detections=filtered_detections, labels=labels)
        
        end_time = time.perf_counter()
        fps = 1 / (end_time - start_time)
        print(f"FPS: {fps:.2f}")
        # cv2.putText(frame, f"FPS: {fps:.2f}",(20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
        # Convert the frame to base64
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Send the frame to the WebSocket
        await websocket.send_text(jpg_as_text)


async def websocket_endpoint(websocket):
    await read_camera(websocket)


def index(request):
    return render(request, "index.html")
