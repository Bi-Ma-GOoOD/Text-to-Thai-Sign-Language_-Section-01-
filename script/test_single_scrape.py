import requests
from bs4 import BeautifulSoup
import os
import json
from pathlib import Path

def get_first_consonant(base_word):
    """
    ฟังก์ชันสำหรับหาพยัญชนะไทยตัวแรกในสตริง
    เพื่อข้ามพวกสระหน้า (เ, แ, โ, ใ, ไ)
    """
    char = ""
    for c in base_word:
        if c >= "ก" and c <= "ฮ":
            char = c
            break
    
    if (char != ""):
        return char
    else:
        return base_word[0]


def test_single_scrape_with_meta(word_url, base_dir):
    print(f"Processing with url: {word_url}")

    try:
        # ------------------------------------------------
        # 1. โหลดหน้าเว็บและสร้างโครงสร้างของ Tree 
        # ------------------------------------------------
        response = requests.get(word_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # ------------------------------------------------
        # 2. ดึงชื่อคำศัพท์ และ แยกบริบท (Context)
        # ------------------------------------------------
        # แยก (เราต่างแยกย้ายกันไป : ท่ามือนี้เป็นลักษณนามแทนตัวบุคคล) - ฐานข้อมูลภาษามือไทย | Thai Sign Language Database
        title_tag = soup.find('title')
        if not title_tag:
            print("Word's name not found!")
            return

        # ดึงข้อความออกมา เช่น "ครู (ท่ามือที่1) - ฐานข้อมูลภาษามือไทย..."
        raw_title = title_tag.text.strip()
        
        # ตัดอักษรตั้งแต่เครื่องหมาย '-' ทิ้งไป เพื่อให้เหลือแค่ "ครู (ท่ามือที่1)"
        full_title = raw_title.split('-')[0].strip()

        # ค้นหาวงเล็บเพื่อแยกชื่อคำหลัก และ บริบท ออกจากกัน
        if '(' in full_title:
            parts = full_title.split('(', 1)
            base_word = parts[0].strip()
            # เอาวงเล็บปิดด้านหลังออกด้วย
            context = parts[1].replace(')', '').strip()
        elif ':' in full_title:
            parts = full_title.split(':', 1)
            base_word = parts[0].strip()
            context = parts[1].strip()
        else:
            base_word = full_title
            context = "ท่าปกติ (ไม่มีคำอธิบายเพิ่มเติม)"
        
        print(f"Word: {base_word}")
        print(f"Word's context: {context}")

        # ------------------------------------------------
        # 3. ดึงลิงก์วิดีโอ .mp4
        # ------------------------------------------------
        video_tag = soup.find('video')
        if not video_tag:
            print("Video not found!")
            return

        source_tag = video_tag.find('source', type='video/mp4')
        if not source_tag or 'src' not in source_tag.attrs:
            print(".MP4 not found!")
            return

        video_url = source_tag['src']
        print(f"Link video: {video_url}")

        # ------------------------------------------------
        # 4. จัดการโครงสร้าง File System และ meta.json
        # ------------------------------------------------
        # แปลงเป็น Path Object
        main_path = ""
        p = Path(base_dir)

        # ตรวจสอบก่อนว่า มีโฟลเดอร์ที่ชื่อว่า Motion_dict หรือยัง เพราะระบบจะเก็บค่าการเคลื่อนที่และคำศัพท์ต่างๆ อยู่ในนี้
        if p.name.upper() != "MOTION_DICT-1":
            # สร้างโฟลเดอร์หลัก
            main_path = os.path.join(base_dir, "MOTION_DICT-1")
            os.makedirs(main_path, exist_ok=True)

        # ดึงอักษรตัวแรกของคำภาษามือไทยคำนั้นๆ
        first_char = get_first_consonant(base_word)

        # สร้างโฟลเดอร์ระดับคำศัพท์ (เช่น MOTION_DICT/ค/ครู)
        word_dir = os.path.join(main_path, first_char, base_word)
        os.makedirs(word_dir, exist_ok=True)

        meta_path = os.path.join(word_dir, "meta.json")
        meta_data = {}

        # 4.1 ถ้ามีไฟล์ meta.json อยู่แล้ว ให้อ่านข้อมูลขึ้นมา
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as reader:
                meta_data = json.load(reader)

        # 4.2 เช็คว่าบริบท (Context) นี้ ถูกโหลดไปหรือยัง ป้องกันการโหลดซ้ำ
        for variant_key, key_context in meta_data.items():
            if key_context == context:
                print(f"This context already have in this {base_word}, skip dowload.")
                return

        # 4.3 หาหมายเลขเวอร์ชันถัดไป (นับจำนวน key ใน json แล้ว + 1)
        next_variant_key_num = len(meta_data) + 1
        new_variant_key = f"v{next_variant_key_num}"

        # 4.4 อัปเดตไฟล์ meta.json
        meta_data[new_variant_key] = context
        with open(meta_path, 'w', encoding='utf-8') as writer:
            json.dump(meta_data, writer, ensure_ascii=False, indent=4)
        print(f"Update meta.json in {base_word} at path {meta_path} successfully.")

        # 4.5 สร้างโฟลเดอร์เวอร์ชันย่อย (บริบท ใหม่ที่พึ่งถูกเพิ่มเข้ามา)
        variant_dir = os.path.join(word_dir, new_variant_key)
        os.makedirs(variant_dir, exist_ok=True)

        # ------------------------------------------------
        # 5. ดาวน์โหลดไฟล์ .mp4
        # ------------------------------------------------
        output_filepath = os.path.join(variant_dir, "original.mp4")
        print(f"video will saving at {output_filepath}")

        vid_response = requests.get(video_url, stream=True)
        vid_response.raise_for_status()

        with open(output_filepath, 'wb') as video:
            for chunk in vid_response.iter_content(chunk_size=8192):
                video.write(chunk)

        print(f"Dowload video success.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Open file test_single_scrape.py")
    base_dir = r"E:\Download"
    # ทดสอบ 1: ครู ท่าที่ 1
    # test_url_1 = "https://www.th-sl.com/word/5-53-1/" 
    
    # ทดสอบ 2: ครู ท่าที่ 2 (เพื่อดูว่ามันสร้าง v2 และอัปเดต meta.json หรือไม่)
    # test_url_2 = "https://www.th-sl.com/word/5-53-2/"
    
    # ทดสอบ 3: คำที่ไม่มีวงเล็บ (เช่น คำว่า เกิน)
    test_url_3 = "https://www.th-sl.com/hand/2568-0388/"
    
    print("----- Start testing -----")
    test_single_scrape_with_meta(test_url_3, base_dir)
