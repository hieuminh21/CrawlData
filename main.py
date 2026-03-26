from scrapling.fetchers import StealthyFetcher
import pandas as pd
import time

def scrape_dauthau_stats():
    """Hàm cào dữ liệu thống kê từ DauThau.info"""

    # URL của trang web cần cào
    url = "https://dauthau.asia/"
    print(f"Đang truy cập: {url}...")

    # Khởi tạo Fetcher tàng hình
    # headless=False giúp mở trình duyệt lên để vượt bot tốt hơn
    fetcher = StealthyFetcher(headless=False)

    try:
        # Tải trang web
        page = fetcher.fetch(url, wait_until="networkidle")

        # Tạm dừng để bạn có thời gian xử lý Captcha nếu xuất hiện
        print("ĐANG ĐỢI 15 GIÂY... Hãy giải Captcha/Xác minh nếu trình duyệt yêu cầu!")
        time.sleep(15)

        if page.status == 200:
            print("Đã tải trang thành công. Bắt đầu trích xuất dữ liệu...")
            data_list = []

            # Tìm tất cả các khối chứa thông tin (có class là 'info')
            info_blocks = page.css('div.info')

            for block in info_blocks:
                # Lấy tiêu đề (trong thẻ h2.lang_title)
                title_node = block.css('h2.lang_title')
                # Lấy tổng số lượng (trong thẻ span.span_total)
                total_node = block.css('span.span_total')

                # Kiểm tra xem khối này có chứa cả tiêu đề và số lượng không
                if title_node and total_node:
                    title = title_node[0].text.strip()
                    total = total_node[0].text.strip()

                    data_list.append({
                        "Danh mục": title,
                        "Số lượng": total
                    })

            # Kiểm tra và lưu kết quả
            if data_list:
                # Tạo DataFrame từ danh sách
                df = pd.DataFrame(data_list)

                # Lưu ra file CSV (Excel có thể đọc được)
                # encoding='utf-8-sig' đảm bảo hiển thị đúng tiếng Việt trong Excel
                df.to_csv("ThongKeDauThau.csv", index=False, encoding='utf-8-sig')

                print("\n--- HOÀN THÀNH ---")
                print(f"Đã tìm thấy {len(df)} danh mục thống kê.")
                print("Dữ liệu đã được lưu vào file: ThongKeDauThau.csv")

                # In một phần dữ liệu ra màn hình
                print("\nTrích xuất mẫu:")
                print(df.head(10).to_string())
            else:
                print("\n--- KHÔNG CÓ DỮ LIỆU ---")
                print("Trang tải thành công nhưng không tìm thấy khối '.info' nào.")
                print("Có thể giao diện trang đã thay đổi hoặc dữ liệu bị ẩn bởi JavaScript.")
        else:
            print(f"Lỗi: Không thể truy cập trang. Mã lỗi: {page.status}")

    except Exception as e:
        print(f"Đã xảy ra lỗi bất ngờ: {e}")

if __name__ == "__main__":
    scrape_dauthau_stats()