import cv2
import os
from pathlib import Path
from processor import process_sign_language_video

def preprocess_sign_language_video(input_video_path, output_video_path):
    # 1. เช็คว่ามีไฟล์วิดีโออยู่จริงไหม
    if not os.path.isfile(input_video_path):
        print(f"[ERROR] video not found: {input_video_path}")
        return False

    # 2. เปิดไฟล์วิดีโอ
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"[ERROR] can't open this video at path: {input_video_path}")
        return False

    # 3. ดึงข้อมูลพื้นฐานของวิดีโอ (FPS, ความกว้าง, ความสูง)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 4. เตรียมตัวเขียนวิดีโอใหม่ (ใช้ Codec 'mp4v' สำหรับไฟล์ .mp4)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    # *** เทคนิคที่ 4: แปลงเป็นขาวดำ ***
    # เนื่องจากเราจะแปลงเป็นขาวดำ เราต้องบอก VideoWriter ว่า `isColor=False`
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height), isColor=True)

    print(f"-> Pre-processing video in path: {input_video_path}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # =========================================================
        # --- เริ่มต้นกระบวนการ Pre-processing (4 เทคนิค) ---
        # =========================================================
        # ** เทคนิคที่ 2: ลบ Noise (GaussianBlur) **
        # การเบลอนิดๆ จะช่วยลบ Noise ได้ดี
        blurred = cv2.GaussianBlur(frame, (3,3), 0)

        # ** เทคนิคที่ 1: ปรับความคมชัด (Unsharp Mask) **
        # เป็นการเอาภาพ Contrast สูง (frame) มาลบกับภาพเบลอ (blurred) 
        # เพื่อเน้นเส้นขอบให้ชัดเจนขึ้น
        sharpened = cv2.addWeighted(frame, 2.0, blurred, -1.0, 0)

        # =========================================================

        # 6. เขียนเฟรมที่ประมวลผลแล้วลงไฟล์วิดีโอใหม่
        out.write(sharpened)

    # 7. ปิดไฟล์และล้างข้อมูลในหน่วยความจำ
    cap.release()
    out.release()
    print(f"[SUCCESS] Pre-processing saved at: {output_video_path}")
    return True

# ทดสอบรัน
if __name__ == "__main__":
    # prototype path: E:\Download\Final_CS_Test\Prototype_video
    ### pre_process
    # pre_process path: E:\Download\Final_CS_Test\pre_process
    in_vid_list = [
        r"E:\Download\Final_CS_Test\Prototype_video\HPV.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\Lalamove.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เข้าใจ.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เคเอฟซี.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เงินสด.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เช้า.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เดิน.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เบา.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ใจเย็น.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ไนกี้.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\กิน.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ข้าว.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ถั่วงอก.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\หนัก.mp4",
    ]

    out_vid_list = [
        r"E:\Download\Final_CS_Test\Prototype_video\HPV.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\Lalamove.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เข้าใจ.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เคเอฟซี.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เงินสด.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เช้า.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เดิน.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\เบา.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ใจเย็น.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ไนกี้.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\กิน.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ข้าว.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\ถั่วงอก.mp4",
        r"E:\Download\Final_CS_Test\Prototype_video\หนัก.mp4"
    ]
    
    out_for_pre_process_motion_list = [
        r"E:\Download\Final_CS_Test\non_pre_process\motion\HPV.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\Lalamove.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\เข้าใจ.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\เคเอฟซี.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\เงินสด.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\เช้า.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\เดิน.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\เบา.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\ใจเย็น.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\ไนกี้.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\กิน.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\ข้าว.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\ถั่วงอก.json",
        r"E:\Download\Final_CS_Test\non_pre_process\motion\หนัก.json"
    ]
    for i in range(14):
        # preprocess_sign_language_video(in_vid_list[i], out_vid_list[i])
        process_sign_language_video(out_vid_list[i], out_for_pre_process_motion_list[i])