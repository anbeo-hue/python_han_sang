import customtkinter
import ctypes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Thiết lập chế độ giao diện sáng để giữ tông màu sáng-tối tương phản chuẩn phong cách Web
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")


class DashboardWindow(customtkinter.CTk):
    """Cửa sổ giao diện chính (Dashboard) quản lý và điều hướng hệ thống kho hàng."""

    FONT_FAMILY = "Segoe UI"
    SIDEBAR_WIDTH = 250
    SIDEBAR_BG = "#6b9bd2"         # Màu xanh dương nhạt theo bản thiết kế
    SIDEBAR_DIVIDER_BG = "#8eb6e6" # Đường phân cách ngang trong sidebar mờ hơn
    MAIN_BG = "#f5f6f8"            # Màu xám cực nhạt giúp nổi bật các card trắng
    DIVIDER_COLOR = "#cbd5e1"      # Đường kẻ phân cách ngang chính

    # Danh sách các Tab điều hướng: (Tên Tab, Emoji đại diện)
    MENU_ITEMS = [
        ("Dashboard", "📊"),
        ("Tồn kho", "📦"),
        ("Nhập Kho", "🛒"),
        ("Xuất Kho", "🚪"),
        ("Quản lý nhà cung cấp", "👥"),
        ("Quản lý đơn hàng", "📋"),
        ("Công thức món ăn", "🍳"),
    ]

    def __init__(self):
        super().__init__()

        # ── Cấu hình cửa sổ tổng thể ──────────────────────────────────
        self.title("Hệ thống Quản lý & Dự đoán Kho hàng - Dashboard")
        self.configure(fg_color=self.MAIN_BG)

        # Căn giữa màn hình
        window_width = 1100
        window_height = 650
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w - window_width) // 2
        y = (screen_h - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(960, 540)

        # Cấu hình grid chính chia cửa sổ thành 2 phần: cột 0 (Sidebar), cột 1 (Main area)
        self.grid_columnconfigure(0, minsize=self.SIDEBAR_WIDTH)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Lưu tên tab đang active để quản lý giao diện
        self.active_tab_name = "Dashboard"
        self.nav_buttons = {}

        # ── Thiết lập các khu vực giao diện ──────────────────────────
        self.setup_sidebar()
        self.setup_main_area()

    def setup_sidebar(self):
        """Thiết lập cột trái - Sidebar và các nút điều hướng."""
        self.sidebar_frame = customtkinter.CTkFrame(
            self,
            fg_color=self.SIDEBAR_BG,
            corner_radius=0,
            width=self.SIDEBAR_WIDTH
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)

        # Cấu hình grid con trong sidebar
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Header
        self.sidebar_frame.grid_rowconfigure(1, weight=0)  # Đường phân cách ngang
        self.sidebar_frame.grid_rowconfigure(2, weight=0)  # Menu Items
        self.sidebar_frame.grid_rowconfigure(3, weight=1)  # Spacer co giãn
        self.sidebar_frame.grid_rowconfigure(4, weight=0)  # Log out

        # ── 1. Header Sidebar ──
        header_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Quản lý & dự đoán\nkho hàng",
            font=(self.FONT_FAMILY, 18, "bold"),
            text_color="#FFFFFF",
            anchor="w",
            justify="left"
        )
        header_label.grid(row=0, column=0, padx=20, pady=(25, 15), sticky="w")

        # ── 2. Đường kẻ ngang mờ phân cách header ──
        header_divider = customtkinter.CTkFrame(
            self.sidebar_frame,
            height=1,
            fg_color=self.SIDEBAR_DIVIDER_BG,
            corner_radius=0
        )
        header_divider.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))

        # ── 3. Container chứa danh sách Menu ──
        menu_container = customtkinter.CTkFrame(self.sidebar_frame, fg_color="transparent")
        menu_container.grid(row=2, column=0, sticky="new")
        menu_container.grid_columnconfigure(0, weight=1)

        # Sinh danh sách các nút menu tự động
        for index, (text, icon) in enumerate(self.MENU_ITEMS):
            self._create_menu_button(menu_container, text, icon, index)

        # ── 4. Nút Log out (ở sát dưới cùng của sidebar) ──
        logout_btn = customtkinter.CTkButton(
            self.sidebar_frame,
            text="🚪  Log out",
            font=(self.FONT_FAMILY, 14),
            fg_color="transparent",
            hover_color="#c0392b", # Hiệu ứng hover đỏ cho hành động thoát
            text_color="#FFFFFF",
            anchor="w",
            height=40,
            corner_radius=8,
            command=self.handle_logout
        )
        logout_btn.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 20))

    def _create_menu_button(self, parent: customtkinter.CTkFrame, text: str, icon: str, row_index: int):
        """Sinh ra nút menu điều hướng với phong cách tương ứng trạng thái active."""
        is_active = (text == self.active_tab_name)

        # Cấu hình màu nền, chữ, icon dựa vào trạng thái active
        if is_active:
            btn_fg = "#FFFFFF"
            btn_text_color = "#000000"
            btn_hover = "#FFFFFF"
        else:
            btn_fg = "transparent"
            btn_text_color = "#FFFFFF"
            # Tạo hiệu ứng di chuột chuyển màu nhẹ khi hover tab chưa chọn
            btn_hover = "#5b8bc2"

        btn = customtkinter.CTkButton(
            parent,
            text=f"{icon}  {text}",
            font=(self.FONT_FAMILY, 13, "bold" if is_active else "normal"),
            fg_color=btn_fg,
            hover_color=btn_hover,
            text_color=btn_text_color,
            anchor="w",
            height=40,
            corner_radius=8,
            command=lambda name=text: self.on_nav_click(name)
        )
        btn.grid(row=row_index, column=0, sticky="ew", padx=15, pady=4)
        self.nav_buttons[text] = btn

    def setup_main_area(self):
        """Thiết lập cột phải - Khu vực hiển thị nội dung chính."""
        self.main_frame = customtkinter.CTkFrame(
            self,
            fg_color=self.MAIN_BG,
            corner_radius=0
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=0) # Tiêu đề trang & Header controls
        self.main_frame.grid_rowconfigure(1, weight=0) # Đường kẻ phân cách chính
        self.main_frame.grid_rowconfigure(2, weight=1) # Vùng chứa nội dung động

        # ── 1. Tiêu đề trang & Header ──
        self.header_frame = customtkinter.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)

        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text=self.active_tab_name,
            font=(self.FONT_FAMILY, 28, "bold"),
            text_color="#000000",
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Khung chứa các nút điều khiển bên phải của Header (ví dụ: bộ lọc ngày)
        self.header_right_frame = customtkinter.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )
        self.header_right_frame.grid(row=0, column=1, sticky="e")

        # ── 2. Đường kẻ phân cách ──
        divider = customtkinter.CTkFrame(
            self.main_frame,
            height=1,
            fg_color=self.DIVIDER_COLOR,
            corner_radius=0
        )
        divider.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # ── 3. Vùng chứa nội dung động ──
        self.content_area = customtkinter.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.content_area.grid(row=2, column=0, sticky="nsew")

        # Nội dung trong content_area
        self.load_placeholder_content()

    def load_placeholder_content(self):
        """Nạp nội dung vào content_area khi chuyển tab."""
        # Xoá các widget cũ trong content_area và header_right_frame
        for widget in self.content_area.winfo_children():
            widget.destroy()
        for widget in self.header_right_frame.winfo_children():
            widget.destroy()

        if self.active_tab_name == "Dashboard":
            self.load_dashboard_content()
        else:
            placeholder_label = customtkinter.CTkLabel(
                self.content_area,
                text=f"⚙️ Tính năng '{self.active_tab_name}' đang được phát triển...",
                font=(self.FONT_FAMILY, 16, "italic"),
                text_color="#64748b"
            )
            placeholder_label.pack(expand=True, fill="both")

    def load_dashboard_content(self):
        """Tải toàn bộ nội dung của màn hình Dashboard."""
        # Tạo Scrollable Frame để chứa toàn bộ nội dung của Dashboard tránh bị vỡ giao diện trên màn hình nhỏ
        scroll_container = customtkinter.CTkScrollableFrame(
            self.content_area,
            fg_color="transparent",
            corner_radius=0
        )
        scroll_container.pack(expand=True, fill="both")
        
        # Cấu hình grid cho scroll_container
        scroll_container.grid_columnconfigure(0, weight=1)
        scroll_container.grid_rowconfigure(0, weight=0) # Dòng 2: Cards
        scroll_container.grid_rowconfigure(1, weight=0) # Dòng 3: Revenue Chart
        scroll_container.grid_rowconfigure(2, weight=0) # Dòng 4: Bottom section
        
        # Gọi các hàm dựng từng phần
        self.create_header()
        self.create_summary_cards(scroll_container)
        self.create_revenue_chart(scroll_container)
        self.create_bottom_section(scroll_container)

    def create_header(self):
        """Tạo phần controls bên phải của Top Bar (Bộ lọc ngày & Nút tra cứu)."""
        # Ô chọn ngày (giả lập bằng CTkLabel nằm trong CTkFrame có viền)
        date_frame = customtkinter.CTkFrame(
            self.header_right_frame,
            fg_color="#ffffff",
            corner_radius=6,
            border_width=1,
            border_color="#cbd5e1",
            height=32
        )
        date_frame.pack(side="left", padx=(0, 10))
        date_frame.pack_propagate(False)

        date_label = customtkinter.CTkLabel(
            date_frame,
            text="01/6/2026 - 30/6/2026 📅",
            font=(self.FONT_FAMILY, 12),
            text_color="#1e293b",
            fg_color="transparent"
        )
        date_label.pack(expand=True, fill="both", padx=12)

        # Nút "Tra cứu 🔍" màu xanh dương nhạt
        search_btn = customtkinter.CTkButton(
            self.header_right_frame,
            text="Tra cứu 🔍",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#e0f2fe", # Màu xanh dương nhạt (sky-100)
            hover_color="#bae6fd", # Hover sky-200
            text_color="#0369a1", # Chữ xanh dương đậm (sky-700)
            corner_radius=6,
            height=32,
            width=90
        )
        search_btn.pack(side="left")

    def create_summary_cards(self, parent):
        """Tạo 4 thẻ tổng quan xếp nằm ngang chia đều không gian."""
        cards_container = customtkinter.CTkFrame(
            parent,
            fg_color="transparent"
        )
        cards_container.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Chia đều 4 cột
        for i in range(4):
            cards_container.grid_columnconfigure(i, weight=1, uniform="card_cols")

        # Định nghĩa cấu hình cho 4 card
        # (Icon, Title, Value, Color, Bg_color_for_icon, Text_color_for_value)
        card_data = [
            ("💰", "Tổng doanh thu", "25.000.000", "#10b981", "#e6f4ea", "#10b981"), # Xanh lá
            ("🛒", "Tổng giá trị nhập hàng", "15.200.000", "#3b82f6", "#e8f0fe", "#3b82f6"), # Xanh dương
            ("📦", "Tổng chi phí nguyên liệu", "15.200.000", "#a16207", "#fef9c3", "#a16207"), # Vàng rêu/olive
            ("📊", "Lợi nhuận ước tính", "10.300.000", "#ef4444", "#fee2e2", "#ef4444") # Đỏ
        ]

        for i, (icon, title, val, color, icon_bg, val_color) in enumerate(card_data):
            card = customtkinter.CTkFrame(
                cards_container,
                fg_color="#ffffff",
                corner_radius=8,
                border_width=1,
                border_color="#e2e8f0"
            )
            # Dùng padx để tạo khoảng cách đẹp mắt
            card.grid(row=0, column=i, sticky="nsew", padx=6 if i > 0 and i < 3 else (0, 6) if i == 0 else (6, 0))
            
            card.grid_columnconfigure(0, weight=0)
            card.grid_columnconfigure(1, weight=1)
            
            # Icon badge tròn
            icon_badge = customtkinter.CTkLabel(
                card,
                text=icon,
                font=(self.FONT_FAMILY, 18),
                text_color=color,
                fg_color=icon_bg,
                width=40,
                height=40,
                corner_radius=20
            )
            icon_badge.grid(row=0, column=0, rowspan=2, padx=12, pady=15, sticky="w")
            
            # Tiêu đề thẻ
            title_lbl = customtkinter.CTkLabel(
                card,
                text=title,
                font=(self.FONT_FAMILY, 11),
                text_color="#64748b",
                anchor="w"
            )
            title_lbl.grid(row=0, column=1, padx=(0, 12), pady=(12, 2), sticky="w")
            
            # Số liệu
            val_lbl = customtkinter.CTkLabel(
                card,
                text=val,
                font=(self.FONT_FAMILY, 16, "bold"),
                text_color=val_color,
                anchor="w"
            )
            val_lbl.grid(row=1, column=1, padx=(0, 12), pady=(0, 12), sticky="w")

    def create_revenue_chart(self, parent):
        """Tạo khu vực biểu đồ kết hợp (Bar & Line) nhúng Matplotlib."""
        chart_frame = customtkinter.CTkFrame(
            parent,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        chart_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Tiêu đề góc trái
        title_lbl = customtkinter.CTkLabel(
            chart_frame,
            text="Biểu đồ doanh thu",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#0f172a"
        )
        title_lbl.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Tạo hình (Figure) của matplotlib
        fig, ax = plt.subplots(figsize=(8, 2.8), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        
        # Dữ liệu giả lập
        months = ["Tháng 1", "Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5"]
        revenue = [35000000, 42000000, 28000000, 48000000, 39000000]
        cost = [25000000, 28000000, 20000000, 30000000, 26000000]
        profit = [r - c for r, c in zip(revenue, cost)]
        
        import numpy as np
        x = np.arange(len(months))
        width = 0.25
        
        # Vẽ cột Doanh thu (xanh dương) và Chi phí (đỏ cam)
        ax.bar(x - width/2, revenue, width, label='Doanh thu', color='#3b82f6')
        ax.bar(x + width/2, cost, width, label='Chi phí', color='#ea580c')
        
        # Vẽ đường Lợi nhuận (xanh lá cây)
        ax.plot(x, profit, label='Lợi nhuận', color='#10b981', marker='o', linewidth=2)
        
        # Định cấu hình trục tọa độ
        ax.set_xticks(x)
        ax.set_xticklabels(months, fontfamily=self.FONT_FAMILY, fontsize=9)
        ax.set_ylim(0, 50000000)
        
        # Format Trục Y dạng rút gọn (ví dụ: 10M, 20M)
        import matplotlib.ticker as ticker
        @ticker.FuncFormatter
        def millions_formatter(x, pos):
            return f'{int(x/1000000)}M' if x > 0 else '0'
        ax.yaxis.set_major_formatter(millions_formatter)
        ax.tick_params(colors='#64748b', labelsize=9)
        
        # Loại bỏ các đường viền trục (spines) ở phía trên và bên phải
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e1')
        ax.spines['bottom'].set_color('#cbd5e1')
        
        # Đường lưới ngang mờ
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#cbd5e1')
        
        # Thêm chú thích (Legend) ở bên phải
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False, prop={'family': self.FONT_FAMILY, 'size': 9})
        
        fig.tight_layout()
        
        # Nhúng biểu đồ vào Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        plt.close(fig)

    def create_bottom_section(self, parent):
        """Tạo dòng 4 chứa biểu đồ Donut tồn kho (cột trái) và bảng dự báo (cột phải)."""
        bottom_container = customtkinter.CTkFrame(
            parent,
            fg_color="transparent"
        )
        bottom_container.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        # Phân chia tỷ lệ cột: cột 0 (trái, Donut) chiếm 42%, cột 1 (phải, Bảng) chiếm 58%
        bottom_container.grid_columnconfigure(0, weight=42, uniform="bottom_row")
        bottom_container.grid_columnconfigure(1, weight=58, uniform="bottom_row")
        
        # ── Cột trái: Biểu đồ tồn kho Donut ──
        left_card = customtkinter.CTkFrame(
            bottom_container,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        left_title = customtkinter.CTkLabel(
            left_card,
            text="Biểu đồ tồn kho",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#0f172a"
        )
        left_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Vẽ biểu đồ Donut
        self.draw_donut_chart(left_card)
        
        # ── Cột phải: Bảng dự báo nhu cầu ──
        right_card = customtkinter.CTkFrame(
            bottom_container,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        right_title = customtkinter.CTkLabel(
            right_card,
            text="Dự báo nhu cầu & dự đoán lượng hàng tháng tới",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#0f172a"
        )
        right_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Dựng bảng Treeview
        self.create_forecast_table(right_card)

    def draw_donut_chart(self, parent):
        """Vẽ biểu đồ Donut tròn khuyết góc và chú thích bên phải."""
        fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        
        categories = ['Còn hàng', 'Sắp hết', 'Hết hàng']
        sizes = [75, 30, 15] # Tổng 120
        colors = ['#10b981', '#f59e0b', '#ef4444']
        
        wedges, texts = ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.35, edgecolor='w', linewidth=2)
        )
        
        # Text ở tâm Donut
        ax.text(
            0, 0, 
            "120\nNguyên Liệu", 
            ha='center', 
            va='center', 
            fontsize=10, 
            fontweight='bold', 
            family=self.FONT_FAMILY,
            color='#1e293b'
        )
        
        ax.axis('equal')  
        
        legend_labels = [f"{cat} ({sz})" for cat, sz in zip(categories, sizes)]
        ax.legend(
            wedges, 
            legend_labels,
            loc="center left",
            bbox_to_anchor=(0.95, 0.5),
            frameon=False,
            prop={'family': self.FONT_FAMILY, 'size': 9}
        )
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        plt.close(fig)

    def create_forecast_table(self, parent):
        """Tạo bảng Treeview dự đoán nhu cầu bằng ttk và tùy biến giao diện."""
        import tkinter as tk
        from tkinter import ttk
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Custom.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=30,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Custom.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Custom.Treeview.Heading",
            background="#f8fafc",
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        table_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("nguyen_lieu", "ton_hien_tai", "nhu_cau", "can_them", "don_vi")
        
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )
        
        headers = {
            "nguyen_lieu": "Nguyên liệu",
            "ton_hien_tai": "Tồn hiện tại",
            "nhu_cau": "Nhu cầu tháng tới",
            "can_them": "Cần thêm",
            "don_vi": "Đơn vị"
        }
        
        for col, heading in headers.items():
            tree.heading(col, text=heading, anchor="w")
            if col in ["ton_hien_tai", "nhu_cau", "can_them"]:
                tree.column(col, anchor="e", width=110)
            elif col == "don_vi":
                tree.column(col, anchor="center", width=70)
            else:
                tree.column(col, anchor="w", width=140)
        
        mock_data = [
            ("Thịt bò", "50", "120", "70", "kg"),
            ("Thịt heo", "80", "150", "70", "kg"),
            ("Rau xà lách", "15", "60", "45", "kg"),
            ("Bánh mì", "100", "300", "200", "cái"),
            ("Bột mì", "40", "100", "60", "kg")
        ]
        
        for item in mock_data:
            tree.insert("", "end", values=item)
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_nav_click(self, name: str):
        """Xử lý sự kiện khi click vào tab trên Sidebar."""
        if name == self.active_tab_name:
            return

        # 1. Reset trạng thái nút active cũ sang in-active
        old_btn = self.nav_buttons.get(self.active_tab_name)
        if old_btn:
            old_btn.configure(
                fg_color="transparent",
                text_color="#FFFFFF",
                hover_color="#5b8bc2",
                font=(self.FONT_FAMILY, 13, "normal")
            )

        # 2. Cập nhật nút active mới sang trạng thái được chọn (Nền trắng, chữ đen)
        self.active_tab_name = name
        new_btn = self.nav_buttons.get(name)
        if new_btn:
            new_btn.configure(
                fg_color="#FFFFFF",
                text_color="#000000",
                hover_color="#FFFFFF",
                font=(self.FONT_FAMILY, 13, "bold")
            )

        # 3. Cập nhật nhãn tiêu đề trang
        self.title_label.configure(text=self.active_tab_name)

        # 4. Tải lại vùng chứa nội dung động
        self.load_placeholder_content()

    def handle_logout(self):
        """Xử lý sự kiện đăng xuất."""
        self.destroy()


if __name__ == "__main__":
    app = DashboardWindow()
    app.mainloop()
