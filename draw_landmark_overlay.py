import cv2
import json
import os
from pathlib import Path

# ---------------------------------------------------------
# กำหนดโครงสร้างการเชื่อมต่อกระดูก (Bones Connections)
# ---------------------------------------------------------
POSE_CONNECTIONS = [
    (1, 2), (2, 3), # ตาซ้ายฝั่งใน -> ชั้นนอก
    (4, 5), (5, 6), # ตาขวาฝั่งใน -> ฝั่งนอก
    (9, 10), # ปาก
    (11, 12), # ไหล่ซ้าย - ขวา
    (11, 13), (13, 15), # แขนซ้าย
    (12, 14), (14, 16), # แขนขวา
    (11, 23), # ลำตัวฝั่งซ้าย
    (12, 24), # ลำตัวฝั่งขวา
    (23, 24) # สะโพก
]

HAND_CONNECTIONS = [
    (0, 1), (2, 5), (5, 9), (9, 13), (13, 17), (0, 17), # ฝ่ามือ
    (1, 2), (2, 3), (3, 4), # นิ้วโป้ง
    (5, 6), (6, 7), (7, 8), # นิ้วชี้
    (9, 10), (10, 11), (11, 12), # นิ้วกลาง
    (13, 14), (14, 15), (15, 16), # นิ้วนาง
    (17, 18), (18, 19), (19, 20) # นิ้วก้อย
]

# ---------------------------------------------------------
# ฟังก์ชันวาดโครงกระดูก
# ---------------------------------------------------------
def draw_skeleton(frame, pose_data, left_hand_data, right_hand_data, width, height):
    point_on_faces = [0, 7, 8]
    point_on_hand = [17, 18, 19, 20, 21, 22] # ใส่เอาไว้เพราะว่าไม่ต้องการให้วาดวงกลม ในจุดที่เป็น มือ ที่เป็นผลลัพธ์จาก POSE
    # - - - POSE - - -
    pose_pixels = {}
    # สร้างจุด
    for plm in pose_data:
        idx = plm["landmark_location"]
        px, py = int(plm["x"] * width), int(plm["y"] * height)
        if idx in point_on_faces:
            # cv2.circle(src, center=(x, y), radius=50, color=(B, G, R), thickness=2)
            cv2.circle(frame, (px, py), 2, (219, 198, 156), -1) # ฟ้าอ่อน
            # pass
        elif ((idx <= 24) and (idx not in point_on_hand)):
            if (px != 0 and py != 0):
                pose_pixels[idx] = (px, py)
                cv2.circle(frame, (px, py), 4, (219, 198, 156), -1)
    # สร้างเส้น
    for p_connection in POSE_CONNECTIONS:
        pt1, pt2 = p_connection
        # print(f"pt1: {pt1} and pt2: {pt2}")
        if pt1 in pose_pixels and pt2 in pose_pixels:
            # cv2.line(image, start_point, end_point, color, thickness)
            cv2.line(frame, pose_pixels[pt1], pose_pixels[pt2], (217, 246, 252), 2) # สีขาววนิลา

    # - - - Left Hand - - -
    lh_pixels = {}
    for lhlm in left_hand_data:
        idx = lhlm["landmark_location"]
        px, py = int(lhlm["x"] * width), int(lhlm["y"] * height)
        lh_pixels[idx] = (px, py)
        cv2.circle(frame, (px, py), 3, (39, 114, 35), -1) # เขียวเข้ม
    for lh_connection in HAND_CONNECTIONS:
        pt1, pt2 = lh_connection
        if pt1 in lh_pixels and pt2 in lh_pixels:
            cv2.line(frame, lh_pixels[pt1], lh_pixels[pt2], (102, 154, 81), 1) # เขียวอ่อน

    # - - - Right Hand - - -
    rh_pixels = {}
    for rhlm in right_hand_data:
        idx = rhlm["landmark_location"]
        px, py = int(rhlm["x"] * width), int(rhlm["y"] * height)
        rh_pixels[idx] = (px, py)
        cv2.circle(frame, (px, py), 3, (0, 170, 255), -1) # เหลืองเข้ม
    for rh_connection in HAND_CONNECTIONS:
        pt1, pt2 = rh_connection
        if pt1 in rh_pixels and pt2 in rh_pixels:
            cv2.line(frame, rh_pixels[pt1], rh_pixels[pt2], (134, 215, 255), 1) # เหลืองอ่อน

    return frame
            


# ---------------------------------------------------------
# ฟังก์ชันสร้าง Overlay จากไฟล์ JSON
# ---------------------------------------------------------
def create_overlay_from_json(input_video_path, motion_json_path, output_overlay_path, word_tsl_name):
    dest_overlay_path = os.path.join(output_overlay_path, "overlay.mp4")
    # print(dest_overlay_path)

    with open(motion_json_path, 'r', encoding='utf-8') as reader:
        json_data = json.load(reader)
    # print(json_data)

    motion_data = json_data["motion_data"]
    # print(motion_data)

    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print(type(json_data["total_frames"]))

    if (total_frames == json_data["total_frames"]):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(dest_overlay_path, fourcc, fps, (width, height))

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_idx < len(motion_data):
                landmarks = motion_data[frame_idx]["Image_Coordinates-(normalized_landmark)"]
                pose = landmarks.get("pose", [])
                left_hand = landmarks.get("left_hand", [])
                right_hand = landmarks.get("right_hand", [])

                # เรียกฟังก์ชันวาด Overlay
                drawn_frame = draw_skeleton(frame, pose, left_hand, right_hand, width, height)

            out.write(drawn_frame)
            frame_idx += 1

        out.release()
    else:
        print("Please select the video clip that matches the motion.js file.")
    
    cap.release()
    print(f"{word_tsl_name} overlay is saved at: {dest_overlay_path}")

if __name__ == "__main__":
    print("Executed draw_landmark.py file directly.")
    input_video_path = r"E:\Code\Text-to-ThaiSignLanguage\input\today.mp4"
    motion_json_path = r"E:\Download\MOTION_DICT\T\TODAY\motion.json"
    output_overlay_path = r"E:\Download\MOTION_DICT\T\TODAY"
    word_tsl_name = "TODAY"
    create_overlay_from_json(input_video_path, motion_json_path, output_overlay_path, word_tsl_name)