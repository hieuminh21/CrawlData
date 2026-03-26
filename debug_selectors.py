"""
Script debug: Lấy HTML thực tế từ trang và kiểm tra CSS selectors
"""
from scrapling.fetchers import StealthyFetcher
import time

print("=== DEBUG CRAWLER ===\n")

fetcher = StealthyFetcher(headless=False)
url = "https://dauthau.asia/thongbao/moithau/?page=1"
print(f"[*] Đang truy cập: {url}\n")
print("[!] Hãy giải Captcha nếu có, chương trình sẽ tự động tiếp tục sau 5 giây...\n")

time.sleep(5)

page = fetcher.fetch(url, wait_until="networkidle")

if page.status == 200:
    print(f"✓ Truy cập thành công! (Status: {page.status})\n")
    
    # Lấy HTML thô
    html_content = page.html
    print("[+] Kiểm tra HTML của bảng dữ liệu:")
    print("=" * 80)
    
    # Tìm đoạn HTML chứa bảng
    if '<tr' in html_content:
        # Lấy 2000 ký tự đầu tiên của bảng
        start_idx = html_content.find('<tr')
        end_idx = min(start_idx + 3000, len(html_content))
        sample_html = html_content[start_idx:end_idx]
        print(sample_html)
    else:
        print("[!] Không tìm thấy <tr> trong HTML")
    
    print("\n" + "=" * 80)
    print("\n[+] Kiểm tra CSS selectors:")
    
    # Kiểm tra các hàng (tr)
    cac_dong = page.css('tr')
    print(f"  - Tìm thấy {len(cac_dong)} hàng (tr)")
    
    if len(cac_dong) > 0:
        print(f"\n[+] Kiểm tra hàng thứ 1:")
        dong_dau = cac_dong[0]
        
        # Kiểm tra các cột (td)
        cac_td = dong_dau.css('td')
        print(f"  - Số cột (td): {len(cac_td)}")
        
        # Kiểm tra từng cột
        for idx, td in enumerate(cac_td[:5]):  # Kiểm tra 5 cột đầu
            text_content = td.text.strip()
            data_column = td.attrib.get('data-column', 'N/A')
            print(f"    TD[{idx}]: data-column='{data_column}', text='{text_content[:50]}'")
        
        print(f"\n[+] Kiểm tra các selector cụ thể:")
        
        # Kiểm tra các selector
        selectors_to_check = [
            'td[data-column="Gói thầu"] a',
            'td[data-column="Chủ đầu tư"] a',
            'td[data-column="Ngày đăng tải"] div',
            'td[data-column="Đóng thầu"] div',
            'td a',  # Kiểm tra xem có thẻ <a> nào không
        ]
        
        for selector in selectors_to_check:
            result = dong_dau.css(selector)
            print(f"  - Selector '{selector}': Tìm thấy {len(result)} phần tử")
            if result:
                print(f"    → Text: '{result[0].text.strip()[:50]}'")
        
        print(f"\n[+] Toàn bộ HTML của hàng 1 (200 ký tự đầu):")
        print(dong_dau.html[:200])
    
else:
    print(f"[!] Lỗi: Status {page.status}")

print("\n" + "=" * 80)
print("[*] Đóng trình duyệt...")
fetcher.close()

