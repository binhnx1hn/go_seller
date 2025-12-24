# Go Seller - Multi-Platform Web Manager

Ứng dụng desktop sử dụng PySide6 để quản lý và nhúng nhiều trang web (Shopee, Lazada, TikTok Shop) vào desktop app.

## Tính năng

- ✅ **Sidebar quản lý trang web**: Danh sách các trang web ở bên trái
- ✅ **Hỗ trợ nhiều nền tảng**: Shopee, Lazada, TikTok Shop (mặc định)
- ✅ **Thêm/Xóa trang web**: Dễ dàng thêm hoặc xóa các trang web tùy chỉnh
- ✅ **Lưu cấu hình**: Tự động lưu danh sách trang web vào file JSON
- ✅ **Giao diện hiện đại**: Sidebar tối màu, dễ nhìn
- ✅ **Chuyển đổi nhanh**: Click vào trang web trong sidebar để chuyển đổi

## Yêu cầu

- Python 3.8 trở lên
- PySide6 (bao gồm QWebEngineWidgets)

## Cài đặt

1. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python main.py
```

## Sử dụng

1. **Xem trang web**: Click vào tên trang web trong sidebar bên trái
2. **Thêm trang web mới**: Click nút "+ Thêm Trang Web" và nhập tên + URL
3. **Xóa trang web**: Chọn trang web trong danh sách và click "🗑 Xóa Trang Web"

## Cấu trúc dự án

- `main.py` - File chính chứa code ứng dụng
- `requirements.txt` - Danh sách các package cần thiết
- `websites_config.json` - File lưu cấu hình các trang web (tự động tạo)
- `README.md` - File hướng dẫn này

## Trang web mặc định

Ứng dụng đi kèm với 3 trang web mặc định (có logo đặc trưng):
- **🛒 Shopee**: https://shopee.vn/user/purchase/
- **📦 Lazada**: https://www.lazada.vn/customer/order/index/
- **🎵 TikTok Shop**: https://seller-vn.tiktok.com/

## Lưu ý

- Ứng dụng sử dụng QWebEngineView để hiển thị web content
- Cần kết nối internet để tải các trang web
- Các trang web có thể yêu cầu đăng nhập để xem nội dung đầy đủ
- Cấu hình được lưu tự động vào `websites_config.json`