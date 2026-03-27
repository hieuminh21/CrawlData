from scrapling.fetchers import StealthyFetcher
import re
import time

LIST_URL = "https://dauthau.asia/thongbao/moithau/?page=1"
MAX_ITEMS = 5


def extract_text(node):
    if not node:
        return ""
    text = getattr(node, "text", "")
    return " ".join(str(text).split()).strip() if text else ""


def extract_ma_tbmt(*values):
    pattern = r"IB\d+(?:\.\d+)?(?:-\d+)?"
    for value in values:
        if not value:
            continue
        match = re.search(pattern, str(value), flags=re.IGNORECASE)
        if match:
            return match.group(0).upper()
    return ""


def parse_detail_fields(detail_page):
    details = {}
    for b_item in detail_page.css(".bidding-detail-item"):
        tit_nodes = b_item.css(".c-tit")
        val_nodes = b_item.css(".c-val")
        if not tit_nodes or not val_nodes:
            continue

        for idx, tit_node in enumerate(tit_nodes):
            key = extract_text(tit_node)
            if not key:
                continue
            value_node = val_nodes[idx] if idx < len(val_nodes) else val_nodes[0]
            value = extract_text(value_node)
            if value:
                details[key] = value

    ma_nodes = detail_page.css(".bd-code, .bidding-code")
    if ma_nodes:
        details["Mã TBMT"] = extract_ma_tbmt(extract_text(ma_nodes[0]), details.get("Mã TBMT", ""))

    return details


def collect_top_links(list_page, limit=5):
    records = []
    for row in list_page.css("tr"):
        a_nodes = row.css('td[data-column="Gói thầu"] a')
        if not a_nodes:
            continue

        a_node = a_nodes[0]
        goi_thau = a_node.attrib.get("title", "").strip() or extract_text(a_node)
        href = a_node.attrib.get("href", "")
        if not href:
            continue

        full_link = href if href.startswith("http") else f"https://dauthau.asia{href}"
        ma_tbmt = extract_ma_tbmt(
            extract_text(a_node.css("span.bidding-code")[0]) if a_node.css("span.bidding-code") else "",
            a_node.attrib.get("title", ""),
            extract_text(a_node),
        )

        records.append(
            {
                "Mã TBMT": ma_tbmt,
                "Gói thầu": goi_thau,
                "Đường dẫn": full_link,
            }
        )

        if len(records) >= limit:
            break

    return records


def main():
    print("=== TEST LAY DETAIL 5 GOI THAU ===")
    fetcher = StealthyFetcher(headless=False)

    try:
        print(f"[*] Dang mo trang danh sach: {LIST_URL}")
        list_page = fetcher.fetch(LIST_URL, wait_until="networkidle")

        if list_page.status != 200:
            print(f"[!] Khong vao duoc trang danh sach. HTTP {list_page.status}")
            return

        records = collect_top_links(list_page, MAX_ITEMS)
        if not records:
            print("[!] Khong tim thay goi thau nao tren trang.")
            return

        print(f"[+] Tim thay {len(records)} goi thau, bat dau lay detail...\n")

        for idx, record in enumerate(records, start=1):
            link = record["Đường dẫn"]
            print(f"--- [{idx}/{len(records)}] {record['Gói thầu']}")
            print(f"    Ma TBMT: {record['Mã TBMT']}")
            print(f"    Link   : {link}")

            try:
                detail_page = fetcher.fetch(link, wait_until="networkidle")
            except Exception as ex:
                print(f"    [!] Loi fetch detail: {ex}\n")
                continue

            if detail_page.status != 200:
                print(f"    [!] Loi HTTP detail: {detail_page.status}\n")
                continue

            details = parse_detail_fields(detail_page)
            if not details:
                print("    [!] Khong parse duoc truong detail.\n")
                continue

            # In nhanh mot so field tieu bieu va tong so field parse duoc.
            ten_du_an = details.get("Tên dự án", "")
            ten_goi = details.get("Tên gói thầu", "")
            dong_thau = details.get("Thời điểm đóng thầu", "")

            print(f"    So field detail: {len(details)}")
            if ten_du_an:
                print(f"    Ten du an      : {ten_du_an}")
            if ten_goi:
                print(f"    Ten goi thau   : {ten_goi}")
            if dong_thau:
                print(f"    Dong thau      : {dong_thau}")

            sample_keys = list(details.keys())[:8]
            print(f"    Mau key detail : {sample_keys}\n")

            time.sleep(1)

    finally:
        try:
            fetcher.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()

