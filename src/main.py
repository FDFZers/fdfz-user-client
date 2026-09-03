import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings

# 禁用沙盒（Linux 系统可能需要）
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简易网页浏览器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 定义主页 URL
        self.home_url = QUrl("https://ffwiki.top/")
        
        # ===== 配置 WebEngine 设置 =====
        settings = QWebEngineSettings.defaultSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        
        # ===== 修改 User-Agent =====
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 导航栏
        nav_layout = QHBoxLayout()
        
        # 后退按钮
        self.back_btn = QPushButton("◀ 后退")
        self.back_btn.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_btn)
        
        # 前进按钮
        self.forward_btn = QPushButton("前进 ▶")
        self.forward_btn.clicked.connect(self.go_forward)
        nav_layout.addWidget(self.forward_btn)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.clicked.connect(self.refresh_page)
        nav_layout.addWidget(self.refresh_btn)
        
        # 主页按钮（新增）
        self.home_btn = QPushButton("🏠 主页")
        self.home_btn.clicked.connect(self.go_home)
        nav_layout.addWidget(self.home_btn)
        
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
        
        # 创建网页视图
        self.browser = QWebEngineView()
        self.browser.urlChanged.connect(self.update_navigation_buttons)
        layout.addWidget(self.browser)
        
        # ===== 加载主页 =====
        self.browser.setUrl(self.home_url)
        
    def update_navigation_buttons(self):
        """更新导航按钮状态"""
        self.back_btn.setEnabled(self.browser.history().canGoBack())
        self.forward_btn.setEnabled(self.browser.history().canGoForward())
    
    def go_back(self):
        """后退"""
        self.browser.back()
    
    def go_forward(self):
        """前进"""
        self.browser.forward()
    
    def refresh_page(self):
        """刷新页面"""
        self.browser.reload()
    
    def go_home(self):
        """返回主页"""
        self.browser.setUrl(self.home_url)


def main():
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()