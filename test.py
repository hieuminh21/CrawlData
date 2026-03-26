from scrapling import BeautifulSoupFetcher # Dùng bộ đọc HTML tĩnh

# Đoạn HTML bạn vừa copy
html_content = """
<a href="#duandtpt">
    <svg class="svg-icon" width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 3H3V42C3 42.7956 3.31607 43.5587 3.87868 44.1213C4.44129 44.6839 5.20435 45 6 45H45V42H6V3Z" fill="white"></path>
        <path d="M45 13.5H34.5V16.5H39.885L28.5 27.885L22.065 21.435C21.9256 21.2944 21.7597 21.1828 21.5769 21.1067C21.3941 21.0305 21.198 20.9913 21 20.9913C20.802 20.9913 20.6059 21.0305 20.4231 21.1067C20.2403 21.1828 20.0744 21.2944 19.935 21.435L9 32.385L11.115 34.5L21 24.615L27.435 31.065C27.5744 31.2056 27.7403 31.3172 27.9231 31.3933C28.1059 31.4695 28.302 31.5087 28.5 31.5087C28.698 31.5087 28.8941 31.4695 29.0769 31.3933C29.2597 31.3172 29.4256 31.2056 29.565 31.065L42 18.615V24H45V13.5Z" fill="white"></path>
    </svg>
    <div class="info">
        <span class="span_total font-span">577.795</span>
        <span class="span_total_moi font-span">577.795</span>
        <h2 class="lang_title">Dự án đầu tư phát triển</h2> 
    </div>
</a>
"""

# Phân tích đoạn HTML
page = BeautifulSoupFetcher(html_content).fetch()

# 1. Tìm thẻ div class "info"
thong_tin_block = page.css('div.info')

if thong_tin_block:
    # 2. Lấy con số (lấy phần tử đầu tiên [0])
    so_luong = thong_tin_block[0].css('span.span_total')[0].text.strip()

    # 3. Lấy tiêu đề
    tieu_de = thong_tin_block[0].css('h2.lang_title')[0].text.strip()

    print("--- KẾT QUẢ ---")
    print(f"Loại danh mục: {tieu_de}")
    print(f"Tổng số lượng: {so_luong}")
else:
    print("Không tìm thấy dữ liệu.")