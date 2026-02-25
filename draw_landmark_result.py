import cv2
import numpy as np
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
# ฟังก์ชันการวาด Stick Figure
# ---------------------------------------------------------
def draw_stick_figure(background, pose, left_hand, right_hand, width, height):
    point_on_faces = [0, 7, 8]
    point_on_hand = [17, 18, 19, 20, 21, 22]

    # - - - POSE - - -
    pose_pixels = {}
    for plm in pose:
        idx = plm["landmark_location"]
        px, py = int(plm["x"] * width), int(plm["y"] * height)
        if idx in point_on_faces:
            cv2.circle(background, (px, py), 2, (0, 0, 0), -1) # ดำเข้ม
        elif ((idx <= 24) and (idx not in point_on_hand)):
            if (px != 0 and py != 0):
                pose_pixels[idx] = (px, py)
                cv2.circle(background, (px, py), 4, (0, 0, 0), -1)
    for p_connection in POSE_CONNECTIONS:
        pt1, pt2 = p_connection
        if (pt1 in pose_pixels) and (pt2 in pose_pixels):
            cv2.line(background, pose_pixels[pt1], pose_pixels[pt2], (34, 34, 34), 2) # สีดำอ่อน

    # - - - Left Hand - - -
    lh_pixels = {}
    for lhlm in left_hand:
        idx = lhlm["landmark_location"]
        px, py = int(lhlm["x"] * width), int(lhlm["y"] * height)
        lh_pixels[idx] = (px, py)
        cv2.circle(background, (px, py), 3, (39, 114, 35), -1) # เขียวเข้ม
    for lh_connection in HAND_CONNECTIONS:
        pt1, pt2 = lh_connection
        if pt1 in lh_pixels and pt2 in lh_pixels:
            cv2.line(background, lh_pixels[pt1], lh_pixels[pt2], (102, 154, 81), 1) # เขียวอ่อน

    # - - - Right Hand - - -
    rh_pixels = {}
    for rhlm in right_hand:
        idx = rhlm["landmark_location"]
        px, py = int(rhlm["x"] * width), int(rhlm["y"] * height)
        rh_pixels[idx] = (px, py)
        cv2.circle(background, (px, py), 3, (0, 170, 255), -1) # เหลืองเข้ม
    for rh_connection in HAND_CONNECTIONS:
        pt1, pt2 = rh_connection
        if pt1 in rh_pixels and pt2 in rh_pixels:
            cv2.line(background, rh_pixels[pt1], rh_pixels[pt2], (134, 215, 255), 1) # เหลืองอ่อน

    return background


# ---------------------------------------------------------
# ฟังก์ชันสร้าง Stick Figure จากลำดับของ Gloss Sequence
# ---------------------------------------------------------
def create_stick_figure(gloss_sequence, motion_dict_dir, result_output_path, fps, frame_width, frame_height, result_name):
    os.makedirs(result_output_path, exist_ok = True)
    output = os.path.join(result_output_path, result_name)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output, fourcc, fps, (frame_width, frame_height))

    for i in gloss_sequence:
        # เพื่อ if-else สำหรับท่าทางการยืนนิ่ง แต่ตอนนี้ยังไม่เพิ่มเลยยังไม่มี if-else
        if i == "":
            word_gloss_motion_dir = os.path.join(motion_dict_dir, "STILL.json")

            with open(word_gloss_motion_dir, 'r', encoding='utf-8') as reader:
                json_data = json.load(reader)

            motion_data = json_data["motion_data"]

            frame_idx = 0
            while frame_idx < len(motion_data):
                background_img = np.full((frame_width, frame_height, 3), 255, dtype=np.uint8)
                landmarks = motion_data[frame_idx]["Image_Coordinates-(normalized_landmark)"]
                pose = landmarks.get("pose", [])
                left_hand = landmarks.get("left_hand", [])
                right_hand = landmarks.get("right_hand", [])

                drawn_img = draw_stick_figure(background_img, pose, left_hand, right_hand, frame_width, frame_height)

                out.write(drawn_img) 
                frame_idx += 1
        else:
            first_letter = i[0]
            subfolder_dir = os.path.join(motion_dict_dir, first_letter)
            gloss_dir = os.path.join(subfolder_dir, i)
            word_gloss_motion_dir = os.path.join(gloss_dir, "motion.json")

            with open(word_gloss_motion_dir, 'r', encoding='utf-8') as reader:
                json_data = json.load(reader)

            motion_data = json_data["motion_data"]

            frame_idx = 0
            while frame_idx < len(motion_data):
                background_img = np.full((frame_width, frame_height, 3), 255, dtype=np.uint8)
                landmarks = motion_data[frame_idx]["Image_Coordinates-(normalized_landmark)"]
                pose = landmarks.get("pose", [])
                left_hand = landmarks.get("left_hand", [])
                right_hand = landmarks.get("right_hand", [])
                # empty list มีค่า เป็น false 
                if (left_hand or right_hand):
                    drawn_img = draw_stick_figure(background_img, pose, left_hand, right_hand, frame_width, frame_height)
                    out.write(drawn_img)
                
                frame_idx += 1

    out.release()
    print(f"{result_name} Figure saved at: {output}")

if __name__ == "__main__":
    gloss_sequence = ["I", "", "HELLO(FRIEND)"]
    motion_dict_dir = r"E:\Download\MOTION_DICT"
    result_output_path = r"E:\Download\Stick_Figure"
    result_name = "stick_figure_2.mp4"
    fps = 50
    frame_width = 600
    frame_height = 600
    create_stick_figure(gloss_sequence, motion_dict_dir, result_output_path, fps, frame_width, frame_height, result_name)
        