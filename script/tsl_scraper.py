import requests
from bs4 import BeautifulSoup
import os
import json
import time
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
        return base_word[0].upper()

def process_single_url(word_url, base_dir):
    # ------------------------------------------------
    # 1. โหลดหน้าเว็บและสร้างโครงสร้างของ Tree 
    # ------------------------------------------------
    response = requests.get(word_url, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # ------------------------------------------------
    # 2. ดึงชื่อคำศัพท์ และ แยกบริบท (Context)
    # ------------------------------------------------
    # แยก (เราต่างแยกย้ายกันไป : ท่ามือนี้เป็นลักษณนามแทนตัวบุคคล) - ฐานข้อมูลภาษามือไทย | Thai Sign Language Database
    title_tag = soup.find('title')
    if not title_tag:
        raise ValueError("Word not found!")

    # ดึงข้อความออกมา เช่น "ครู (ท่ามือที่1) - ฐานข้อมูลภาษามือไทย..."
    raw_title = title_tag.text.strip()
    
    # ตัดอักษรตั้งแต่เครื่องหมาย '-' ทิ้งไป เพื่อให้เหลือแค่ "ครู (ท่ามือที่1)"
    full_title = raw_title.split('-')[0].strip()

    # ค้นหาวงเล็บเพื่อแยกชื่อคำหลัก และ บริบท ออกจากกัน
    # หาตำแหน่งของ '(' และ ':' (ถ้าหาไม่เจอจะได้ค่า -1)
    idx_paren = full_title.find('(')
    idx_colon = full_title.find(':')

    # แปลงค่า -1 ให้เป็น infinity เพื่อให้เปรียบเทียบง่ายว่าอะไรมาก่อน
    pos_paren = idx_paren if idx_paren != -1 else float('inf')
    pos_colon = idx_colon if idx_colon != -1 else float('inf')

    # เงื่อนไข 1: เจอ '(' ก่อน
    if pos_paren < pos_colon:
        parts = full_title.split('(', 1)
        base_word = parts[0].strip().replace(" ", "_")
        context = parts[1].replace(')', '').strip()
        
    # เงื่อนไข 2: เจอ ':' ก่อน
    elif pos_colon < pos_paren:
        parts = full_title.split(':', 1)
        base_word = parts[0].strip().replace(" ", "_")
        context = parts[1].strip()
        
    # เงื่อนไข 3 & 4: ไม่มีทั้ง '(' และ ':'
    else:
        if '/' in full_title: # มี '/'
            base_word = full_title.replace("/", "หรือ").replace(" ", "_").strip()
            context = "ท่าปกติ (ไม่มีคำอธิบายเพิ่มเติม)"
        else: # ไม่มีอะไรเลย (มีแค่ช่องว่าง หรือคำปกติ)
            base_word = full_title.replace(" ", "_").strip()
            context = "ท่าปกติ (ไม่มีคำอธิบายเพิ่มเติม)"

    # ------------------------------------------------
    # 3. ดึงลิงก์วิดีโอ .mp4
    # ------------------------------------------------
    video_tag = soup.find('video')
    if not video_tag:
        raise ValueError("Video not found!")

    source_tag = video_tag.find('source', type='video/mp4')
    if not source_tag or 'src' not in source_tag.attrs:
        raise ValueError(".MP4 not found!")

    video_url = source_tag['src']

    # ------------------------------------------------
    # 4. จัดการโครงสร้าง File System และ meta.json
    # ------------------------------------------------
    # แปลงเป็น Path Object
    main_path = ""
    p = Path(base_dir)

    # ตรวจสอบก่อนว่า มีโฟลเดอร์ที่ชื่อว่า Motion_dict หรือยัง เพราะระบบจะเก็บค่าการเคลื่อนที่และคำศัพท์ต่างๆ อยู่ในนี้
    if p.name.upper() != "CLIP_WORD_DICT-1":
        # สร้างโฟลเดอร์หลัก
        main_path = os.path.join(base_dir, "CLIP_WORD_DICT-1")
        os.makedirs(main_path, exist_ok=True)
    else:
        main_path = base_dir

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
            return "SKIPPED", f"This context already have in this {base_word}, skip dowload."

    # 4.3 หาหมายเลขเวอร์ชันถัดไป (นับจำนวน key ใน json แล้ว + 1)
    next_variant_key_num = len(meta_data) + 1
    new_variant_key = f"v{next_variant_key_num}"

    # 4.4 อัปเดตไฟล์ meta.json
    meta_data[new_variant_key] = context
    with open(meta_path, 'w', encoding='utf-8') as writer:
        json.dump(meta_data, writer, ensure_ascii=False, indent=4)

    # 4.5 สร้างโฟลเดอร์เวอร์ชันย่อย (บริบท ใหม่ที่พึ่งถูกเพิ่มเข้ามา)
    variant_dir = os.path.join(word_dir, new_variant_key)
    os.makedirs(variant_dir, exist_ok=True)

    # ------------------------------------------------
    # 5. ดาวน์โหลดไฟล์ .mp4
    # ------------------------------------------------
    output_filepath = os.path.join(variant_dir, "original.mp4")
    vid_response = requests.get(video_url, stream=True)
    vid_response.raise_for_status()

    with open(output_filepath, 'wb') as video:
        for chunk in vid_response.iter_content(chunk_size=8192):
            video.write(chunk)

    return "SUCCESS", f"save word {base_word} at version: {new_variant_key} successed."

def main():
    base_dir = r"E:\Download\CLIP_WORD_DICT-1"
    url_file = r"E:\Code\Text-to-ThaiSignLanguage\all_sign_language_urls.txt"
    # url_file = r"E:\Code\Text-to-ThaiSignLanguage\test_language_urls.txt"
    error_file = r"E:\Code\Text-to-ThaiSignLanguage\error_log01.txt"

    if not os.path.exists(url_file):
        print(f"Not found url in {url_file}")
        return

    # อ่านลิงก์ทั้งหมดมาเก็บใน List
    with open(url_file, 'r', encoding='utf-8') as reader:
        urls = [line.strip() for line in reader if line.strip()]

    print(f"All link amount {len(urls)} are ready to dowload.")
    print("- - - - - - - - - -")

    success_count = 0
    skip_count = 0
    error_count = 0

    with open(error_file, 'w', encoding='utf-8') as err_log:
        err_log.write("--- Log การดาวน์โหลดที่ผิดพลาด ---\n")

        for idx, url in enumerate(urls, 1):
            print(f"[{idx}/{len(urls)}] processing: {url}")
            try:
                status, msg = process_single_url(url, base_dir)
                print(f"---> msg: {msg}")

                if status == "SUCCESS":
                    success_count += 1
                elif status == "SKIPPED":
                    skip_count += 1
                    err_log.write(f"(SKIPPED) URL: {url}\n | Desp: {msg}")
            except Exception as e:
                print(f"---> Mistake: {e}")
                error_count += 1
                err_log.write(f"(Error) URL: {url} | Error: {e}\n")

            time.sleep(1)
    
    # Summary
    print("Process Successfully")
    print(f"Complete: {success_count} clips.")
    print(f"Skip: {skip_count} clips.")
    print(f"Mistake: {error_count} clips. Check at error_log.txt")

if __name__ == "__main__":
    main()