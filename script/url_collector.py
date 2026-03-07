import requests
from bs4 import BeautifulSoup
import time

def collect_urls():
    sitemaps = [
        "https://www.th-sl.com/post-sitemap.xml",
        "https://www.th-sl.com/post-sitemap2.xml",
        "https://www.th-sl.com/post-sitemap3.xml",
        "https://www.th-sl.com/post-sitemap4.xml"
    ]

    all_word_urls = []

    print("Start pulling all url... ")

    for url in sitemaps:
        print(f"Pulling clip url from: {url}.")
        try:
            response = requests.get(url)
            response.raise_for_status() # เช็คว่าโหลดสำเร็จไหม (status 200)

            # ใช้ 'xml' parser เพราะไฟล์ต้นทางเป็น XML
            soup = BeautifulSoup(response.content, 'xml')

            # ในไฟล์ Sitemap ลิงก์เป้าหมายจะถูกเก็บอยู่ใน <loc>
            loc_tags = soup.find_all('loc')

            for loc in loc_tags:
                target_url = loc.text.strip()
                # กรองเอาเฉพาะลิงก์โพสต์ 
                if target_url.endswith('/'):
                    all_word_urls.append(target_url)

            print(f"can pull url amount: {len(loc_tags)} links.")
        
        except Exception as e:
            print(f"Has error at url: {url} and error: {e}")

        # หน่วงเวลา 1 วินาที
        time.sleep(1)

    print(f"All URLs have been collected.: {len(all_word_urls)}")

    # บันทึกทุกอย่างลงไฟล์ Text
    # output_filename = r"E:\Code\Text-to-ThaiSignLanguage\all_sign_language_urls.txt"
    # with open(output_filename, "w", encoding="utf-8") as file:
    #     for link in all_word_urls:
    #         file.write(link + "\n")

    # print(f"Saved all_sign_language_urls.txt at {output_filename} successfully.")

if __name__ == "__main__":
    collect_urls()