import os
from processor import process_sign_language_video

def batch_process_videos(base_dir, log_file):

    if not os.path.exists(base_dir):
        print(f"Not found base directory in {base_dir}")
        return

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    print(f"Start processing video in: {base_dir}")

    # ตัวแปรเก็บจำนวนของไฟล์คำที่ถูกแปลงเป็น motion.json
    processed_count = 0
    error_count = 0
    count_word = 1

    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("- - - Log การแปลงคลิปวิดีโอคำภาษามือไทยที่ผิดพลาด - - -\n")
        log.flush()

        # os.walk จะทำหน้าที่มุดเข้าไปในทุกโฟลเดอร์ย่อย ไม่ว่าจะลึกแค่ไหน
        for root, dirs, files in os.walk(base_dir):
            # ถ้าในโฟลเดอร์นั้นมีไฟล์ original.mp4
            if "original.mp4" in files:
                video_path = os.path.join(root, "original.mp4")
                json_path = os.path.join(root, "motion.json")

                # ดึงชื่อคำศัพท์ออกมาจาก Path เพื่อส่งให้ฟังก์ชัน
                # โครงสร้างคือ MOTION_DICT/หมวด/ชื่อคำศัพท์/v1 
                # หน้าตาของ root ตอนนี้คือ : MOTION_DICT/ก/เกิน/v1
                path_parts = os.path.split(root)
                # path_parts = ["MOTION_DICT/ก/เกิน", "v1"] 
                word_name = os.path.split(path_parts[0])[1] # ดึงชื่อคำศัพท์ออกมา
                variant_name = path_parts[1]

                print(f"Order [{count_word}] --> Starting extract motion from: {word_name}/[{variant_name}]")

                try:
                    # 1. ส่งให้ฟังก์ชันประมวลผล
                    process_sign_language_video(video_path, json_path)

                    # 2. ตรวจสอบความปลอดภัย: เช็คว่าไฟล์ motion.json สร้างสำเร็จแล้วจริงๆ
                    if os.path.exists(json_path):
                        # 3. ถ้าสร้างเสร็จสมบูรณ์ ให้ลบไฟล์ original.mp4 สำหรับ variant นั้นๆ ทิ้งเลย
                        os.remove(video_path)
                        processed_count += 1
                        print(f"Word: {word_name}/[{variant_name}] processing motion.json success.")
                    else:
                        error_count += 1
                        log.write(f"Word: {word_name}/[{variant_name}] processing motion.json not success.")
                        log.flush()
                        print(f"Word: {word_name}/[{variant_name}] processing motion.json not success.")

                except Exception as e:
                    error_count += 1
                    print(f"Have an error in '{word_name}' in [{variant_name}]. | Error: {e}")
                    log.write(f"Path: {root} | Error: {e}\n")
                    
                count_word += 1

    print("Summary")
    print(f"Created motion.json: {processed_count} files")
    print(f"Found Error: {error_count} files")

def count_element(base_dir, mode):
    target = ""

    if (mode.upper() == "VIDEO"):
        target = "original.mp4"
    elif (mode.upper() == "MOTION"):
        target = "motion.json"
    else:
        target = ""

    if not os.path.exists(base_dir):
        print(f"Not found base directory in {base_dir}")
        return

    count = 0

    if target == "":
        return f"Error"
    else:
        for root, dirs, files in os.walk(base_dir):
            if target in files:
                count += 1
            

    print("Summary")
    print(f"{base_dir} has {target}: {count} files")

if __name__ == "__main__":
    base_motion_dir = r"E:\Download\MOTION_DICT"
    base_video_dir = r"E:\Download\MOTION_DICT-1"
    log_file = r"E:\Code\Text-to-ThaiSignLanguage\error_motion_log.txt"
    batch_process_videos(base_video_dir, log_file)
    # count_element(base_video_dir, "video")