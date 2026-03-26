from scrapling.fetchers import StealthyFetcher
import pandas as pd
import time

def crawler_dauthau_chuyen_nghiep():
    print("=== KHỞI ĐỘNG CRAWLER CHUYÊN NGHIỆP ===")

    # Khởi tạo trình duyệt, hiện giao diện để bạn dễ xử lý Captcha
    fetcher = StealthyFetcher(headless=False)
    all_data = [] # Giỏ đựng dữ liệu chung cho tất cả các trang

    # Cài đặt số trang muốn cào (Ví dụ: Từ trang 1 đến trang 3)
    for so_trang in range(1, 4):
        url = f"https://dauthau.asia/thongbao/moithau/?page={so_trang}"
        print(f"\n---> [TRANG {so_trang}] Đang truy cập: {url}")

        # Truy cập trang và đợi load xong JavaScript
        page = fetcher.fetch(url, wait_until="networkidle")

        # Xử lý thời gian chờ để vượt mặt hệ thống chống Bot
        if so_trang == 1:
            print("ĐANG ĐỢI 5 GIÂY: Hãy nhấp giải Captcha trên trình duyệt (nếu có)!")
            time.sleep(5)
        else:
            print("Nghỉ ngơi 5 giây để tránh bị khóa IP...")
            time.sleep(5)

        # Nếu vào trang thành công
        if page.status == 200:
            # Lấy tất cả các dòng (tr) trong trang web
            cac_dong = page.css('tr')
            so_luong_trang_nay = 0
            print(f"[DEBUG] Số lượng hàng (tr) tìm thấy: {len(cac_dong)}")

            for dong in cac_dong:
                # 1. Tìm Gói Thầu (Vào tận thẻ a)
                a_goi_thau = dong.css('td[data-column="Gói thầu"] a')

                if a_goi_thau:
                    # --- LẤY TÊN VÀ MÃ GÓI THẦU CHUẨN XÁC ---
                    # Lấy tên gói thầu từ title
                    goi_thau = a_goi_thau[0].attrib.get('title', '').strip()
                    if not goi_thau:
                        goi_thau = a_goi_thau[0].text.strip()

                    # Lấy Mã TBMT
                    ma_tbmt_node = a_goi_thau[0].css('span.bidding-code')
                    ma_tbmt = ma_tbmt_node[0].text.strip() if ma_tbmt_node else ""

                    # Lấy link gốc
                    link = a_goi_thau[0].attrib.get('href', '')
                    full_link = link if link.startswith('http') else "https://dauthau.asia" + link

                    if not goi_thau:
                        goi_thau = full_link.split('/')[-1] # Phương án back-up cuối cùng

                    # 2. Tìm Chủ Đầu Tư và Mã CĐT
                    a_chu_dau_tu = dong.css('td[data-column="Chủ đầu tư"] a')
                    if a_chu_dau_tu:
                        chu_dau_tu = a_chu_dau_tu[0].attrib.get('title', '').strip()
                        if not chu_dau_tu:
                            chu_dau_tu = a_chu_dau_tu[0].text.strip()

                        ma_cdt_node = a_chu_dau_tu[0].css('span.solicitor-code')
                        ma_cdt = ma_cdt_node[0].text.strip() if ma_cdt_node else ""
                    else:
                        chu_dau_tu = "Đang cập nhật"
                        ma_cdt = ""

                    # 3. Ngày đăng tải
                    div_ngay_dang = dong.css('td[data-column="Ngày đăng tải"] div')
                    ngay_dang = div_ngay_dang[0].text.strip() if div_ngay_dang else ""

                    # 4. Đóng thầu
                    div_dong_thau = dong.css('td[data-column="Đóng thầu"] div')
                    dong_thau = div_dong_thau[0].text.strip() if div_dong_thau else ""

                    # Cho dữ liệu vào giỏ
                    all_data.append({
                        "Mã TBMT": ma_tbmt,
                        "Gói thầu": goi_thau,
                        "Mã CĐT": ma_cdt,
                        "Chủ đầu tư": chu_dau_tu,
                        "Ngày đăng tải": ngay_dang,
                        "Đóng thầu": dong_thau,
                        "Đường dẫn": full_link
                    })
                    so_luong_trang_nay += 1

            print(f"[+] Hoàn thành Trang {so_trang}: Thu được {so_luong_trang_nay} gói thầu.")

        else:
            print(f"[!] Lỗi ở Trang {so_trang} (Mã: {page.status}). Dừng Crawler!")
            break

    # === TỔNG KẾT VÀ LƯU FILE ===
    if all_data:
        print(f"\n[DEBUG] Tổng số bản ghi trước xóa trùng: {len(all_data)}")

        # Chuyển thành bảng
        df = pd.DataFrame(all_data)
        print(f"[DEBUG] DataFrame shape trước xóa trùng: {df.shape}")

        # Xóa các gói thầu bị trùng lặp (dùng Mã TBMT là chuẩn xác nhất)
        df_before = df.copy()
        df = df.drop_duplicates(subset=['Mã TBMT', 'Gói thầu'])
        print(f"[DEBUG] Bản ghi bị xóa do trùng lặp: {len(df_before) - len(df)}")
        print(f"[DEBUG] DataFrame shape sau xóa trùng: {df.shape}")

        # Thêm thời gian vào tên file để không bao giờ bị trùng hay lỗi Permission
        thoi_gian_hien_tai = time.strftime("%d%m%Y_%H%M%S")
        file_name = f"DanhSachGoiThau_{thoi_gian_hien_tai}.csv"

        # Lưu ra Excel (CSV)
        df.to_csv(file_name, index=False, encoding='utf-8-sig')

        print("\n===============================")
        print(f"🎉 XUẤT SẮC! Đã thu thập thành công tổng cộng {len(df)} gói thầu.")
        print(f"📁 Dữ liệu đã được lưu vào: {file_name}")
        print("===============================\n")
    else:
        print("\n[!] Không lấy được dữ liệu. Hãy kiểm tra lại mạng hoặc Captcha.")

if __name__ == "__main__":
    crawler_dauthau_chuyen_nghiep()