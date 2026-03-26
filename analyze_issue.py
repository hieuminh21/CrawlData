"""
Script phân tích vấn đề: Tại sao crawling lấy được nhiều dữ liệu nhưng CSV chỉ có 1 bản ghi
"""
import pandas as pd
import os

print("=" * 70)
print("PHÂN TÍCH VẤN ĐỀ - CRAWLING DATA")
print("=" * 70)

# Danh sách các file CSV
csv_files = [f for f in os.listdir('.') if f.startswith('DanhSachGoiThau_') and f.endswith('.csv')]
csv_files.sort(reverse=True)

if not csv_files:
    print("[!] Không tìm thấy file CSV nào.")
else:
    print(f"\n[+] Tìm thấy {len(csv_files)} file CSV")
    
    # Phân tích file mới nhất
    latest_file = csv_files[0]
    print(f"\n[>] Phân tích file mới nhất: {latest_file}")
    
    df = pd.read_csv(latest_file)
    print(f"    - Số dòng: {len(df)}")
    print(f"    - Số cột: {len(df.columns)}")
    print(f"    - Các cột: {list(df.columns)}")
    
    print(f"\n[>] Dữ liệu trong file:")
    print(df.to_string())
    
    print(f"\n[>] Kiểm tra giá trị trống:")
    print(df.isnull().sum())
    
    print(f"\n[>] Kiểm tra giá trị cột 'Gói thầu':")
    for idx, val in enumerate(df['Gói thầu'].tolist()):
        print(f"    - Row {idx}: '{val}'")

print("\n" + "=" * 70)
print("LỜI GỢI Ý:")
print("=" * 70)
print("""
NGUYÊN NHÂN CHÍNH: drop_duplicates(subset=['Gói thầu'])
- Nếu cột 'Gói thầu' có giá trị trống hoặc giống nhau
  => Tất cả bản ghi đó sẽ bị coi là trùng lặp
  => Chỉ giữ lại 1 bản ghi, xóa hết những cái khác

GIẢI PHÁP:
1. Dùng drop_duplicates(subset=['Gói thầu', 'Chủ đầu tư', 'Ngày đăng tải', 'Đóng thầu'])
   => So sánh toàn bộ các trường, không chỉ 'Gói thầu'
   
2. Kiểm tra xem CSS selector có lấy được 'Gói thầu' không
   => Nếu không lấy được => tất cả đều trống => xóa hết
   
3. Thêm logging chi tiết để theo dõi dữ liệu từng bước

✓ Code đã được cập nhật với logging chi tiết!
""")
print("=" * 70)

