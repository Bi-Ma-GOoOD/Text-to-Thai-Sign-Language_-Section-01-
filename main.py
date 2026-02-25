from pathlib import Path
import os

from processor import process_sign_language_video
from draw_landmark_overlay import create_overlay_from_json

# ---------------------------------------------------------
# ฟังก์ชันสร้าง Main Structure File System
# ---------------------------------------------------------
def create_structure_file(storage_path):
    folder_store_name = "MOTION_DICT"
    main_storage_path = ""
    creating_sub_folder_flags = False
    # แปลงเป็น Path Object
    p = Path(storage_path)
    # print(p.name)
    # ถ้าเกิดว่า storage_path ที่ใส่มา indext สุดท้ายของ path ไม่ใช่คำว่า MOTION_DICT เราจะสร้างโฟลเดอร์นี้ให้เลยอัตโนมัติ
    if (p.name.upper() != folder_store_name):
        final_path = os.path.join(storage_path, folder_store_name)
        # print(final_path)
        try:
            os.makedirs(final_path)
            print('Created Folder "MOTION_DICT" successfully.')
            main_storage_path = final_path
            print(f"main storage created at {main_storage_path}")
            creating_sub_folder_flags = True
        except FileExistsError:
            print(f"One or more directories in '{final_path}' already exist.")
            return final_path
        except PermissionError:
            print(f"Permission denied: Unable to create '{final_path}'.")
            return final_path
        except Exception as e:
            print(f"Error: {e}")
            return final_path
    else :
        main_storage_path = storage_path
        creating_sub_folder_flags = False

    # - - - ส่วนนี้สร้าง folder ที่เป็น A-Z อิงจากชื่อไฟล์ input - - -
    # ถ้าเกิดว่าในโฟลเดอร์ของ MOTION_DICT ยังไม่มี subfolder ตั้งแต่ A-Z ให้เปลี่ยน creating_sub_folder_flags จาก False ให้เป็น True
    if (creating_sub_folder_flags):
        if (create_subfolder(main_storage_path)):
            print("created sub-folder success.")
        else:
            print("something wrong during creating subfolder")
    else:
        print("Not creating sub-folder")

    return main_storage_path

# ---------------------------------------------------------
# ฟังก์ชันสร้าง Sub-Folder
# ---------------------------------------------------------
def create_subfolder(main_storage_path):
    for i in range(65, 91):
        subfolder_name = chr(i)
        subfolder_path = os.path.join(main_storage_path, subfolder_name)
        try:
            os.makedirs(subfolder_path)
        except FileExistsError:
            print(f"One or more directories in '{subfolder_path}' already exist.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{subfolder_path}'.")
        except Exception as e:
            print(f"Error: {e}")
    
    return True

# ---------------------------------------------------------
# ฟังก์ชันสร้าง Folder ของคำภาษาไทยนั้นๆ ในหมวดหมู่ของตัวอักษรนั้นๆ
# ---------------------------------------------------------
def create_destination_dir(path_dir, word_tsl_name):
    dest_dir = os.path.join(path_dir, word_tsl_name)
    try:
        os.makedirs(dest_dir)
    except FileExistsError:
        # print(f"One or more directories in '{dest_dir}' already exist.")
        return dest_dir
    except PermissionError:
        print(f"Permission denied: Unable to create '{dest_dir}'.")
    except Exception as e:
        print(f"Error: {e}")
    
    return dest_dir

# ---------------------------------------------------------
# ฟังก์ชันการทำงานหลัก
# ---------------------------------------------------------
def main():
    storage_path = r"E:\Download\MOTION_DICT"
    # สร้าง Folder และ Sub-folder
    result_path = create_structure_file(storage_path)
    # print(f"destination storage path is: {result_path}")
    
    input_video_path = r"E:\Code\Text-to-ThaiSignLanguage\input"
    input_video_list = ["hello(friend).mp4"]
    # stem attribute extracts the file
    # name in uppercase
    # ชื่อของอินพุตไฟล์ ควรเป็นคำภาษามือไทย ที่แปลงเป็นอังกฤษแล้วจะดีที่สุด เช่น [วันนี้ => TODAY]

    # - - - ส่วนของการสร้าง motion.json - - -
    for i in input_video_list:
        word_tsl_name = Path(i).stem
        word_tsl_name = word_tsl_name.replace(" ", "_").upper()
        # print(f"word_tsl_name: {word_tsl_name}")
        folder_group_name = word_tsl_name[0].upper()
        # print(f"folder_group_name: {folder_group_name}")
        path_dir = os.path.join(result_path, folder_group_name)
        # print(f"path_dir: {path_dir}")
        # สร้างโฟลเดอร์ของคำนั้นๆ ลงหมวดหมู่ของศัพท์นั้นๆ
        destination_dir = create_destination_dir(path_dir, word_tsl_name)
        # print(f"main destination directory for {word_tsl_name} at {destination_dir}")
        input_video = os.path.join(input_video_path, i)
        process_sign_language_video(word_tsl_name, input_video, destination_dir)
    # - - - จบส่วนของการสร้าง motion.json - - - 


    # - - - ส่วนของการสร้าง Overlay.mp4 - - -
    # create_overlay_from_json(input_video_path, motion_json_path, output_overlay_path, word_tsl_name)
    # - - - จบส่วนของการสร้าง Overlay.mp4 - - -


if __name__ == "__main__":
    main()