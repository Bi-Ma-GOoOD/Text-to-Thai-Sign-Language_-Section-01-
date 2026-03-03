import cv2
import os
import numpy as np

# ---------------------------------------------------------
# ทดสอบการสร้างภาพที่มีพื้นหลังสีข้าว
# ---------------------------------------------------------
def create_write_bg():
    img = np.full((500, 500, 3),255, dtype = np.uint8)
    img = cv2.circle(img, (50, 50), 20, (219, 198, 156), -1)
    img = cv2.circle(img, (350, 350), 20, (219, 198, 156), -1)
    img = cv2.line(img, (50, 50), (350, 350), (255, 255, 255), 8)

    cv2.imshow("Canvas Line", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# ---------------------------------------------------------
# ทดสอบการกำจัด Still ที่ซ้อนกันมากกว่า 1 คำขึ้นไป
# ---------------------------------------------------------
def merge_still():
    data_dict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    final_sequence_for_show = []
    final_sequence_for_motion = []
    group = []

    # input_sequence จะได้มาจาก Gemini ที่ผมอยากให้ Gemini ส่งเวอร์ชันแรกของการทำ Tokenization มาก่อน แบบก่อนที่จะไปดูคำในลิสต์ และให้ผลลัพธ์มาเป็นคำ และ empty string อะ
    input_sequence = ['z', 'e', 'k', 'o', 'b', 'c', 'l', 'm', 'n', 'd', 'p']
    # output_sequence เป็นสิ่งที่ได้มาจาก Gemini ที่ผา่นการดูคำใน Dict มาแล้วว่าคำไหนมี (ถ้ามีก็ให้เก็บเป็นคำนั้นเลย หรือ คำที่ใกล้เคียงกับบริบทที่สุด) และ ไม่มี (ถ้าไม่มี ให้เก็บเป็น empty string)
    output_sequence = ['empty_string', 'e', 'empty_string', 'empty_string', 'b', 'c', 'empty_string', 'empty_string', 'empty_string', 'd', 'empty_string']

    for i in range(len(output_sequence)):
        out_token = output_sequence[i]
        
        if out_token == 'empty_string':
            # ถ้าเป็น empty_string ให้เก็บคำจาก input_sequence ลงใน group สะสมไปเรื่อยๆ
            group.append(input_sequence[i])
        else:
            # ถ้ามีของใน group สะสมอยู่ (แปลว่าก่อนหน้านี้มี empty_string)
            if len(group) > 0:
                if len(group) == 1:
                    final_sequence_for_show.append(group[0])
                else:
                    final_sequence_for_show.append(group)
                
                final_sequence_for_motion.append('still')
                group = [] # รีเซ็ต group ให้ว่างเปล่าเพื่อรอสะสมคำใหม่
            
            # เก็บคำปกติลงในลิสต์ผลลัพธ์
            final_sequence_for_show.append(out_token)
            final_sequence_for_motion.append(out_token)

    # เช็คว่ามี group หลงเหลืออยู่ที่ท้าย sequence หรือไม่
    if len(group) > 0:
        if len(group) == 1:
            final_sequence_for_show.append(group[0])
        else:
            final_sequence_for_show.append(group)
        final_sequence_for_motion.append('still')

    print(f"final_sequence_for_show: {final_sequence_for_show}")
    print(f"final_sequence_for_motion: {final_sequence_for_motion}")

def create_destination_dir():
    word = "TANK"
    word_path = r"E:\Download\MOTION_DICT\T\TEACH"
    existing_versions = [d for d in os.listdir(word_path) if os.path.isdir(os.path.join(word_path, d))]
    next_version = f"v{len(existing_versions) + 1}"
    print(next_version)

def manage_name():
    """
    ห้ามมีสิ่งเหล่านี้อยู่ใน Path
    \ / : * ? " < > |
    """

    seperate_mark = ["(", ":", "/"]
    word = [
        "ครู (ท่าทางที่1)",
        "ฝรั่งเศส :สาธารณรัฐฝรั่งเศส (ท่ามือที่1 เป็นท่ามือไทย)",
        "แพทย์ / หมอ",
        "เอเซียทีค เดอะ ริเวอร์ ฟรอนต์ (ท่าที่1)",
        "เกิน",
        "ฟุตบอล เอฟซี"
    ]
    base_word = ""
    context = ""
    flag = True

    for i in word:
        for j in i:
            if j in seperate_mark:
                if j == "(":
                    flag = False
                    txt = i.split(j, 1)
                    base_word = txt[0].strip()
                    context = txt[1].replace(")", " ").strip()
                    break
                elif j == ":":
                    flag = False
                    txt = i.split(j, 1)
                    base_word = txt[0].strip()
                    context = txt[1].strip()
                    break
                elif j == "/":
                    flag = False
                    base_word = i.replace("/", "หรือ").replace(" ", "_").strip()
                    context = "ท่าปกติ (ไม่มีคำอธิบายเพิ่มเติม)"
                    break
        
        if (flag):
            base_word = i.replace(" ", "_").strip()
            context = "ท่าปกติ (ไม่มีคำอธิบายเพิ่มเติม)"
            print(f"B: {base_word}, C: {context}")
        else:
            print(f"B: {base_word}, C: {context}")

    

if __name__ == "__main__":
    print("Test.py")
    # create_write_bg()
    # merge_still()
    # create_destination_dir()
    manage_name()