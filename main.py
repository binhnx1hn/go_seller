#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Platform Web Embedder
Ứng dụng PySide6 để nhúng nhiều trang web (Shopee, Lazada, TikTok) vào desktop app
"""

import sys
import json
import os
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QListWidget, QListWidgetItem,
    QInputDialog, QMessageBox, QLabel
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont


class WebSiteManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.websites = []
        self.config_file = "websites_config.json"
        self.current_website = None
        self.load_config()
        self.init_ui()
        
    def load_config(self):
        """Tải cấu hình từ file JSON"""
        default_sites = [
            {"name": "Shopee", "url": "https://shopee.vn/user/purchase/", "icon": "shopee"},
            {"name": "Lazada", "url": "https://www.lazada.vn/customer/order/index/", "icon": "lazada"},
            {"name": "TikTok Shop", "url": "https://seller-vn.tiktok.com/", "icon": "tiktok"}
        ]
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.websites = json.load(f)
            except:
                self.websites = default_sites
        else:
            self.websites = default_sites
            self.save_config()
    
    def save_config(self):
        """Lưu cấu hình vào file JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.websites, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu cấu hình: {e}")
    
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        self.setWindowTitle("Multi-Platform Web Manager")
        self.setGeometry(100, 100, 1400, 900)
        
        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Tạo layout ngang chính
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === SIDEBAR BÊN TRÁI ===
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(250)
        sidebar_widget.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
            }
            QListWidget {
                background-color: #2b2b2b;
                color: white;
                border: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3b3b3b;
            }
            QListWidget::item:hover {
                background-color: #3b3b3b;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        
        sidebar_layout = QVBoxLayout()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)
        
        # # Tiêu đề sidebar
        # title_label = QLabel("Danh Sách Trang Web")
        # sidebar_layout.addWidget(title_label)
        
        # Danh sách các trang web
        self.website_list = QListWidget()
        self.website_list.itemClicked.connect(self.on_website_selected)
        self.website_list.itemDoubleClicked.connect(self.on_website_double_clicked)
        sidebar_layout.addWidget(self.website_list)
        
        # Nút thêm trang web mới
        btn_add = QPushButton("+ Thêm Trang Web")
        btn_add.clicked.connect(self.add_website)
        sidebar_layout.addWidget(btn_add)
        
        # Nút xóa trang web
        btn_remove = QPushButton("🗑 Xóa Trang Web")
        btn_remove.clicked.connect(self.remove_website)
        sidebar_layout.addWidget(btn_remove)
        
        # Cập nhật danh sách
        self.update_website_list()
        
        # === WEB VIEW BÊN PHẢI ===
        self.web_view = QWebEngineView()
        
        # Load trang web đầu tiên nếu có
        if self.websites:
            self.load_website(self.websites[0])
        
        # Thêm sidebar và web view vào layout chính
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.web_view, 1)  # stretch factor = 1 để web view chiếm phần còn lại
    
    def load_icon_from_file(self, platform_name):
        """Tải icon từ file trong thư mục icons/"""
        # Map tên platform với tên file icon
        icon_files = {
            "shopee": "icon_shopee.jpg",
            "lazada": "icon_lazada.png",
            "tiktok": "icon_tiktok.png",
        }
        
        # Lấy tên file icon
        icon_file = icon_files.get(platform_name.lower())
        if not icon_file:
            return None
        
        # Đường dẫn đến file icon
        icon_path = os.path.join("icons", icon_file)
        
        # Kiểm tra file có tồn tại không
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                # Scale icon về kích thước phù hợp (32x32 hoặc 40x40)
                scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                return QIcon(scaled_pixmap)
        
        return None
    
    def create_default_icon(self, platform_name):
        """Tạo icon mặc định nếu không tìm thấy file"""
        # Màu sắc đặc trưng cho mỗi platform
        colors = {
            "shopee": QColor(238, 77, 45),  # Màu cam đỏ của Shopee
            "lazada": QColor(0, 123, 193),   # Màu xanh của Lazada
            "tiktok": QColor(0, 0, 0),       # Màu đen của TikTok
        }
        
        # Emoji hoặc ký tự đại diện
        emojis = {
            "shopee": "🛒",
            "lazada": "📦",
            "tiktok": "🎵",
        }
        
        # Tạo pixmap 32x32
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Lấy màu và emoji
        color = colors.get(platform_name.lower(), QColor(100, 100, 100))
        emoji = emojis.get(platform_name.lower(), "🌐")
        
        # Vẽ nền tròn với màu
        painter.setBrush(QColor(color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(2, 2, 28, 28)
        
        # Vẽ emoji/text
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 18, QFont.Bold)
        painter.setFont(font)
        painter.drawText(0, 0, 32, 32, Qt.AlignCenter, emoji)
        painter.end()
        
        return QIcon(pixmap)
    
    def get_platform_icon(self, website):
        """Lấy icon cho website dựa trên tên hoặc URL"""
        name_lower = website.get('name', '').lower()
        url_lower = website.get('url', '').lower()
        
        # Xác định platform name
        platform_name = None
        
        # Kiểm tra icon trong config
        if 'icon' in website:
            platform_name = website['icon']
        # Tự động nhận diện platform từ tên hoặc URL
        elif 'shopee' in name_lower or 'shopee' in url_lower:
            platform_name = 'shopee'
        elif 'lazada' in name_lower or 'lazada' in url_lower:
            platform_name = 'lazada'
        elif 'tiktok' in name_lower or 'tiktok' in url_lower:
            platform_name = 'tiktok'
        else:
            platform_name = 'default'
        
        # Thử load icon từ file trước
        icon = self.load_icon_from_file(platform_name)
        if icon:
            return icon
        
        # Nếu không tìm thấy file, dùng icon mặc định
        return self.create_default_icon(platform_name)
    
    def update_website_list(self):
        """Cập nhật danh sách trang web trong sidebar"""
        self.website_list.clear()
        for website in self.websites:
            item = QListWidgetItem(website['name'])
            item.setData(Qt.UserRole, website['url'])
            
            # Thêm icon
            icon = self.get_platform_icon(website)
            item.setIcon(icon)
            
            self.website_list.addItem(item)
    
    def on_website_selected(self, item):
        """Xử lý khi click vào một trang web trong danh sách"""
        url = item.data(Qt.UserRole)
        website = next((w for w in self.websites if w['url'] == url), None)
        if website:
            self.load_website(website)
    
    def on_website_double_clicked(self, item):
        """Xử lý khi double-click vào một trang web"""
        self.on_website_selected(item)
    
    def load_website(self, website):
        """Tải trang web vào web view"""
        self.current_website = website
        self.web_view.setUrl(QUrl(website['url']))
        self.setWindowTitle(f"{website['name']} - Multi-Platform Web Manager")
    
    def add_website(self):
        """Thêm trang web mới"""
        name, ok1 = QInputDialog.getText(
            self, 'Thêm Trang Web', 'Nhập tên trang web:'
        )
        if not ok1 or not name:
            return
        
        url, ok2 = QInputDialog.getText(
            self, 'Thêm Trang Web', 'Nhập URL:'
        )
        if not ok2 or not url:
            return
        
        # Kiểm tra URL hợp lệ
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Kiểm tra trùng lặp
        if any(w['url'] == url for w in self.websites):
            QMessageBox.warning(self, 'Cảnh báo', 'Trang web này đã tồn tại!')
            return
        
        new_website = {"name": name, "url": url, "icon": "default"}
        self.websites.append(new_website)
        self.save_config()
        self.update_website_list()
        
        # Tự động chọn trang web vừa thêm
        for i in range(self.website_list.count()):
            item = self.website_list.item(i)
            if item.data(Qt.UserRole) == url:
                self.website_list.setCurrentItem(item)
                self.load_website(new_website)
                break
    
    def remove_website(self):
        """Xóa trang web đã chọn"""
        current_item = self.website_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, 'Cảnh báo', 'Vui lòng chọn trang web để xóa!')
            return
        
        url = current_item.data(Qt.UserRole)
        website = next((w for w in self.websites if w['url'] == url), None)
        
        if website:
            reply = QMessageBox.question(
                self, 'Xác nhận', 
                f'Bạn có chắc muốn xóa "{website["name"]}"?',
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.websites = [w for w in self.websites if w['url'] != url]
                self.save_config()
                self.update_website_list()
                
                # Load trang web đầu tiên nếu còn
                if self.websites:
                    self.load_website(self.websites[0])
                else:
                    self.web_view.setUrl(QUrl("about:blank"))
                    self.setWindowTitle("Multi-Platform Web Manager")


def main():
    """Hàm main để chạy ứng dụng"""
    app = QApplication(sys.argv)
    
    # Thiết lập style cho ứng dụng
    app.setStyle('Fusion')
    
    # Tạo và hiển thị cửa sổ chính
    window = WebSiteManager()
    window.show()
    
    # Chạy event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

