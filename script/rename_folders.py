import os

def rename_folders_with_spaces(base_dir):
    print("Investigating and change folder with space to underscore instead..")
    
    count = 0 # เอาไว้นับว่ามีกี่โฟลเดอร์ที่มีช่องว่างคั่น

    # 1. วนลูปโฟลเดอร์หมวดหมู่พยัญชนะ (ก, ข, ค, ...)
    if not os.path.exists(base_dir):
        print("Can't find base_dir path")
        return

    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)

        if os.path.isdir(category_path):
            # 2. วนลูปโฟลเดอร์ชื่อคำศัพท์ที่อยู่ข้างใน
            for word_folder in os.listdir(category_path):
                # ถ้าเจอช่องว่างในชื่อโฟลเดอร์
                if " " in word_folder:
                    old_path = os.path.join(category_path, word_folder)

                    # แทนที่ช่องว่างด้วย "_"
                    new_word_folder = word_folder.replace(" ", "_")
                    new_path = os.path.join(category_path, new_word_folder)

                    try:
                        os.rename(old_path, new_path)
                        print(f"Change old folder name: [{word_folder}] ---> [{new_word_folder}]")
                        count += 1
                    except Exception as e:
                        print(f"Can't change this folder name: [{word_folder}]")
    
    print(f"Processing successfully!! folder name changed {count} folders")


if __name__ == "__main__":
    base_dir = r"E:\Download\MOTION_DICT-1"
    rename_folders_with_spaces(base_dir)