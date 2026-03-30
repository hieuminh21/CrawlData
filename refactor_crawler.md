# Refactor Checklist - Dauthau Crawler

## Tinh trang sau dot refactor hien tai

- [x] Tach `BASE_URL`, `SEARCH_PATH`, `SEARCH_PARAMS_BASE`
- [x] Bo sung `CrawlerConfig` (keyword, date range, page, retry, delay)
- [x] Tach layer `fetch` (`fetch_page`, `fetch_list_page`, `fetch_detail_page`)
- [x] Tach layer `parser` (`parse_list_page`, `_parse_detail_fields`)
- [x] Tach business flow (`crawl_list`, `crawl_detail`, `crawler_dauthau_chuyen_nghiep`)
- [x] Data model bang `@dataclass Tender`
- [x] Filter logic qua `is_valid_item()`
- [x] Chuyen `print` sang `logging`
- [x] Giu mapping header (`LIST_HEADER_ALIASES`, `DETAIL_HEADER_ALIASES`)
- [ ] Pipeline pattern / clean architecture (de xuat cho dot tiep theo)

## 1. Config (Web mẫu)

-   Tách BASE_URL
-   Tách search params (keyword, date, page)

## 2. Layers

### Fetch layer

-   Chỉ gọi HTTP (StealthyFetcher)

### Parser layer

-   parse_list_page
-   parse_detail_page

### Utils

-   normalize_key
-   extract_text
-   extract_ma_tbmt

### Business logic

-   crawl_list
-   crawl_detail

### Export

-   export_to_excel

## 3. Crawl flow

1.  Crawl list
2.  Filter data
3.  Crawl detail
4.  Merge data
5.  Export

## 4. Header mapping

-   LIST_HEADER_ALIASES
-   DETAIL_HEADER_ALIASES

## 5. Data model

-   Dùng dataclass (Tender)

## 6. Refactor function lớn

-   Chia nhỏ crawler chính thành nhiều hàm

## 7. Filter logic

-   is_valid_item()

## 8. Config hệ thống

-   REQUEST_DELAY
-   MAX_RETRY

## 9. Logging

-   Dùng logging thay print

## 10. Nâng cao

-   Pipeline pattern
-   Clean architecture
