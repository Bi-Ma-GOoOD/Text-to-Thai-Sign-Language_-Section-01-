import cv2
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
# ทดสอบการกำจัด Still ที่ซ้อนกันมากกว่า 1 คำขึ้นไป และ กำจัด Still ที่อยู่หน้า และ ท้าย ของลิสต์ Gloss_sequence
# ---------------------------------------------------------
def merge_still():
    example_gloss_sequence = ["", "", "i", "", "", "love", "", "", "you", "", "", ""]
    example_gloss_sequence_1 = ["", "i", "", "love", "", "you", ""]
    final_gloss_sequence = []
    flags = False
    
    for i in example_gloss_sequence:
        if (flags):
            if (i != ""):
                final_gloss_sequence.append(i)
                flags = False
        else:
            if (i == ""):
                final_gloss_sequence.append(i)
                flags = True

    print(f"Before: {final_gloss_sequence}")
    # print(len(final_gloss_sequence))

    # ผมเขียนเงื่อนไขตรงนี้ เพราะว่า ผมคิดว่า ท่าไม่มีท่าที่ทำอะไรเลย (ซึ่งก็คือท่ายืนนิ่ง) ที่อยู่ในท่าเริ่มต้น และ ท่าจบ ซึ่งถ้าเป็นเช่นนั้นแล้ว เราก็ไม่ต้องแสดงก็ได้ เพราะมันไม่มีประโยชน์อะไรที่จะแสดงในเมื่อมันไม่มี
    if (final_gloss_sequence[0] == ""):
        final_gloss_sequence.pop(0)
    if (final_gloss_sequence[len(final_gloss_sequence) - 1] == ""):
        final_gloss_sequence.pop(len(final_gloss_sequence) - 1)

    print(f"After: {final_gloss_sequence}")

    # - - - นำโค้ดที่ผมเขียนนี้ ไปใส่เอาไว้ด้านบนสุดในฟังก์ชัน create_overlay_from_json() เพื่อทำการจัดการ list ใหม่ จากนั้นเอา list ผลลัพธ์ (ซึ่งในที่นี้คือ final_gloss_sequence) ไปทำงานต่อ หรือว่า เอาไปแทนลิสต์เวอร์ชันเก่านั่นแหละครับ
    # เพิ่มเติม : ไม่จำเป็นต้องสร้างฟังก์ชันใหม่นะครับ แค่เอาโค้ดในฟังก์ชัน merge_still() ไปใส่ใน ฟังก์ชัน create_overlay_from_json() บรรทัดบนสุดเลย หรือว่าใส่ล่าง obj การสร้าง video ก้ได้
    # ตัวอย่างการใส่โค้ดใน create_overlay_from_json
    # def create_stick_figure(gloss_sequence, motion_dict_dir, result_output_path, fps, frame_width, frame_height, result_name):
    #     os.makedirs(result_output_path, exist_ok = True)
    #     output = os.path.join(result_output_path, result_name)

    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     out = cv2.VideoWriter(output, fourcc, fps, (frame_width, frame_height))

    #     final_gloss_sequence = []
    #     flags = False
        
    #     for i in gloss_sequence:
    #         if (flags):
    #             if (i != ""):
    #                 final_gloss_sequence.append(i)
    #                 flags = False
    #         else:
    #             if (i == ""):
    #                 final_gloss_sequence.append(i)
    #                 flags = True

    #     if (final_gloss_sequence[0] == ""):
    #         final_gloss_sequence.pop(0)
    #     if (final_gloss_sequence[len(final_gloss_sequence) - 1] == ""):
    #         final_gloss_sequence.pop(len(final_gloss_sequence) - 1)

    #     for i in final_gloss_sequence:
    #         # - - - ทำงานเหมือนเดิมในฟังก์ชันนี้ - - -


if __name__ == "__main__":
    # create_write_bg()
    merge_still()

    