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
        elif self.active_tab_name == "Tồn kho":
            inventory_view = InventoryView(self.content_area, font_family=self.FONT_FAMILY)
            inventory_view.pack(expand=True, fill="both")
        elif self.active_tab_name == "Nhập Kho":
            import_view = ImportView(self.content_area, font_family=self.FONT_FAMILY)
            import_view.pack(expand=True, fill="both")
        elif self.active_tab_name == "Xuất Kho":
            export_view = ExportView(self.content_area, font_family=self.FONT_FAMILY)
            export_view.pack(expand=True, fill="both")
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


class InventoryView(customtkinter.CTkScrollableFrame):
    """Màn hình Tồn kho hiển thị các thẻ tổng quan và bảng dữ liệu nguyên liệu."""
    
    def __init__(self, parent, font_family="Segoe UI"):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.FONT_FAMILY = font_family
        
        # Cấu hình grid cho self (đối tượng cuộn)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Dòng 1: Cards
        self.grid_rowconfigure(1, weight=1) # Dòng 2: Table Section
        
        # Gọi các hàm dựng từng phần
        self.create_summary_cards()
        self.create_table_section()
        
    def create_summary_cards(self):
        """Tạo 4 thẻ tổng quan nằm ngang của màn hình Tồn kho."""
        cards_container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        cards_container.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Chia đều 4 cột
        for i in range(4):
            cards_container.grid_columnconfigure(i, weight=1, uniform="inv_card_cols")

        # Cấu hình cho 4 card của Tồn kho
        # (Icon, Title, Value, Color, Bg_color_for_icon, Text_color_for_value)
        card_data = [
            ("📦", "Tổng nguyên liệu", "120", "#10b981", "#e6f4ea", "#2ecc71"), # Xanh lá
            ("🛒", "Tổng số lượng tồn kho", "1.234", "#3b82f6", "#e8f0fe", "#3498db"), # Xanh dương
            ("🚚", "Tổng giá trị tồn kho", "15.200.000", "#a16207", "#fef9c3", "#d4ac0d"), # Vàng rêu
            ("📈", "Số lượng nguyên liệu sắp hết", "12", "#ef4444", "#fee2e2", "#e74c3c") # Đỏ
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

    def create_table_section(self):
        """Tạo khu vực chứa bảng tồn kho (tìm kiếm và bảng Treeview)."""
        table_container = customtkinter.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        table_container.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        
        # ── 1. Thanh công cụ (Toolbar) ──
        toolbar = customtkinter.CTkFrame(
            table_container,
            fg_color="transparent"
        )
        toolbar.pack(fill="x", padx=15, pady=15)
        
        # Ô tìm kiếm bên trái
        search_entry = customtkinter.CTkEntry(
            toolbar,
            placeholder_text="Tìm mã hoặc tên nguyên liệu 🔍",
            font=(self.FONT_FAMILY, 12),
            width=300,
            height=34,
            corner_radius=6,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8"
        )
        search_entry.pack(side="left")
        
        # Nút "+ Thêm nguyên liệu" bên phải màu xanh dương nhạt
        add_btn = customtkinter.CTkButton(
            toolbar,
            text="+ Thêm nguyên liệu",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#e0f2fe", # sky-100
            hover_color="#bae6fd", # sky-200
            text_color="#0369a1", # sky-700
            corner_radius=6,
            height=34
        )
        add_btn.pack(side="right")
        
        # ── 2. Bảng dữ liệu (ttk.Treeview) ──
        import tkinter as tk
        from tkinter import ttk
        
        # Cấu hình style cho Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Inventory.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=32,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Inventory.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Inventory.Treeview.Heading",
            background="#f8fafc",
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        # Khung bọc bảng và thanh cuộn
        table_frame = customtkinter.CTkFrame(table_container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ma_nl", "ten_nl", "danh_muc", "sl_ton", "ton_min", "trang_thai", "gia_tri")
        
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Inventory.Treeview"
        )
        
        # Cấu hình thẻ Zebra Row tag
        tree.tag_configure("evenrow", background="#ffffff")
        tree.tag_configure("oddrow", background="#f8fafc")
        
        # Tiêu đề cột
        headers = {
            "ma_nl": "Mã nguyên liệu",
            "ten_nl": "Tên nguyên liệu",
            "danh_muc": "Danh mục",
            "sl_ton": "Số lượng tồn",
            "ton_min": "Tồn kho tối thiểu",
            "trang_thai": "Trạng thái tồn",
            "gia_tri": "Giá trị"
        }
        
        for col, heading in headers.items():
            if col == "trang_thai":
                tree.heading(col, text=heading, anchor="center")
                tree.column(col, anchor="center", width=120)
            elif col in ["sl_ton", "ton_min", "gia_tri"]:
                tree.heading(col, text=heading, anchor="w")
                tree.column(col, anchor="e", width=110)
            elif col == "ma_nl":
                tree.heading(col, text=heading, anchor="w")
                tree.column(col, anchor="w", width=110)
            else:
                tree.heading(col, text=heading, anchor="w")
                tree.column(col, anchor="w", width=130)
                
        # Mock data 3 dòng
        mock_data = [
            ("NL001", "Thịt bò", "Thịt", "20kg", "45kg", "Còn đủ", "4.000.000"),
            ("NL002", "Thịt heo", "Thịt", "20kg", "45kg", "Sắp hết", "4.000.000"),
            ("NL001", "Thịt bò", "Thịt", "20kg", "45kg", "Hết hàng", "4.000.000")
        ]
        
        for i, item in enumerate(mock_data):
            row_tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=item, tags=(row_tag,))
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class ImportView(customtkinter.CTkScrollableFrame):
    """Màn hình Nhập Kho hiển thị các phiếu nhập hàng và mở popup thêm phiếu nhập mới."""
    
    def __init__(self, parent, font_family="Segoe UI"):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.FONT_FAMILY = font_family
        
        # Cấu hình grid cho self (đối tượng cuộn)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Dòng 1: Cards
        self.grid_rowconfigure(1, weight=1) # Dòng 2: Table Section
        
        # Dựng giao diện
        self.create_summary_cards()
        self.create_table_section()
        
    def create_summary_cards(self):
        """Tạo 4 thẻ tổng quan nằm ngang của màn hình Nhập Kho."""
        cards_container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        cards_container.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        # Chia đều 4 cột
        for i in range(4):
            cards_container.grid_columnconfigure(i, weight=1, uniform="imp_card_cols")

        # Cấu hình 4 card
        # (Icon, Title, Value, Bg_color_for_icon, Text_color_for_value)
        card_data = [
            ("📝", "Tổng phiếu nhập", "26", "#e6f4ea", "#2ecc71"), # Xanh lá
            ("🏢", "Tổng nhà cung cấp", "12", "#e8f0fe", "#3498db"), # Xanh dương
            ("💰", "Tổng giá trị nhập hàng", "15.200.000", "#fef9c3", "#d4ac0d"), # Vàng rêu
            ("📦", "Tổng số lượng nhập hàng", "1.234", "#fee2e2", "#e74c3c") # Đỏ
        ]

        for i, (icon, title, val, icon_bg, val_color) in enumerate(card_data):
            card = customtkinter.CTkFrame(
                cards_container,
                fg_color="#ffffff",
                corner_radius=8,
                border_width=1,
                border_color="#e2e8f0"
            )
            card.grid(row=0, column=i, sticky="nsew", padx=6 if i > 0 and i < 3 else (0, 6) if i == 0 else (6, 0))
            
            card.grid_columnconfigure(0, weight=0)
            card.grid_columnconfigure(1, weight=1)
            
            # Icon badge tròn
            icon_badge = customtkinter.CTkLabel(
                card,
                text=icon,
                font=(self.FONT_FAMILY, 18),
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

    def create_table_section(self):
        """Tạo khu vực chứa bảng nhập kho (tìm kiếm và bảng Treeview)."""
        table_container = customtkinter.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        table_container.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        
        # ── 1. Thanh công cụ (Toolbar) ──
        toolbar = customtkinter.CTkFrame(
            table_container,
            fg_color="transparent"
        )
        toolbar.pack(fill="x", padx=15, pady=15)
        
        # Ô tìm kiếm bên trái
        search_entry = customtkinter.CTkEntry(
            toolbar,
            placeholder_text="Tìm mã hoặc tên nguyên liệu 🔍",
            font=(self.FONT_FAMILY, 12),
            width=250,
            height=34,
            corner_radius=6,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8"
        )
        search_entry.pack(side="left")
        
        # Khung chứa 4 nút bên phải
        buttons_frame = customtkinter.CTkFrame(toolbar, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # Nút 1: Tự động cộng tồn kho (vàng nhạt)
        auto_stock_btn = customtkinter.CTkButton(
            buttons_frame,
            text="Tự động cộng tồn kho",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#fef9c3", # yellow-100
            hover_color="#fef08a", # yellow-200
            text_color="#a16207", # yellow-800
            corner_radius=6,
            height=34,
            width=140
        )
        auto_stock_btn.pack(side="left", padx=4)
        
        # Nút 2: Cập nhật (màu tím)
        update_btn = customtkinter.CTkButton(
            buttons_frame,
            text="Cập nhật",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#f3e8ff", # purple-100
            hover_color="#e9d5ff", # purple-200
            text_color="#7e22ce", # purple-700
            corner_radius=6,
            height=34,
            width=80
        )
        update_btn.pack(side="left", padx=4)
        
        # Nút 3: Xóa phiếu nhập (đỏ nhạt)
        delete_btn = customtkinter.CTkButton(
            buttons_frame,
            text="Xóa phiếu nhập",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#fee2e2", # red-100
            hover_color="#fca5a5", # red-200
            text_color="#b91c1c", # red-700
            corner_radius=6,
            height=34,
            width=110
        )
        delete_btn.pack(side="left", padx=4)
        
        # Nút 4: + Thêm phiếu nhập (xanh dương)
        add_btn = customtkinter.CTkButton(
            buttons_frame,
            text="+ Thêm phiếu nhập",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#3b82f6", # blue-500
            hover_color="#2563eb", # blue-600
            text_color="#ffffff",
            corner_radius=6,
            height=34,
            command=self.open_import_form
        )
        add_btn.pack(side="left", padx=(4, 0))
        
        # ── 2. Bảng dữ liệu (ttk.Treeview) ──
        import tkinter as tk
        from tkinter import ttk
        
        # Cấu hình style cho Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Import.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=32,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Import.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Import.Treeview.Heading",
            background="#f8fafc",
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        table_frame = customtkinter.CTkFrame(table_container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ma_lo", "nha_cc", "nguyen_lieu", "sl_nhap", "gia_nhap", "nsx", "hsd", "trang_thai")
        
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Import.Treeview"
        )
        
        # Zebra Row tags
        tree.tag_configure("evenrow", background="#ffffff")
        tree.tag_configure("oddrow", background="#f8fafc")
        
        # Tiêu đề cột
        headers = {
            "ma_lo": "Mã lô hàng",
            "nha_cc": "Nhà cung cấp",
            "nguyen_lieu": "Nguyên liệu",
            "sl_nhap": "Số lượng nhập",
            "gia_nhap": "Giá nhập",
            "nsx": "Ngày sản xuất",
            "hsd": "Hạn sử dụng",
            "trang_thai": "Trạng thái"
        }
        
        for col, heading in headers.items():
            tree.heading(col, text=heading, anchor="w")
            if col in ["sl_nhap", "gia_nhap"]:
                tree.column(col, anchor="e", width=100)
            elif col in ["nsx", "hsd", "trang_thai"]:
                tree.column(col, anchor="center", width=110)
            elif col == "ma_lo":
                tree.column(col, anchor="w", width=100)
            elif col == "nha_cc":
                tree.column(col, anchor="w", width=180)
            else:
                tree.column(col, anchor="w", width=120)
                
        # Mock data 3 dòng
        mock_data = [
            ("PN20601", "Công ty TNHH thực phẩm", "Thịt", "20kg", "200.000/kg", "1/5/2026", "15/5/2026", "Đã nhập"),
            ("PN20602", "Công ty CP Nông sản sạch", "Rau xà lách", "50kg", "30.000/kg", "10/5/2026", "17/5/2026", "Đã nhập"),
            ("PN20603", "Nhà phân phối Bánh mì Hà Nội", "Bánh mì", "100 cái", "5.000/cái", "15/5/2026", "18/5/2026", "Chưa nhập")
        ]
        
        for i, item in enumerate(mock_data):
            row_tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=item, tags=(row_tag,))
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def open_import_form(self):
        """Mở popup thêm phiếu nhập hàng mới (CTkToplevel)."""
        popup = customtkinter.CTkToplevel(self)
        popup.title("Thêm Phiếu Nhập")
        
        # Kích thước popup 800x600
        popup_width = 800
        popup_height = 600
        
        # Căn giữa popup so với cửa sổ cha hoặc màn hình
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        try:
            parent_w = self.winfo_toplevel().winfo_width()
            parent_h = self.winfo_toplevel().winfo_height()
            parent_x = self.winfo_toplevel().winfo_x()
            parent_y = self.winfo_toplevel().winfo_y()
            x = parent_x + (parent_w - popup_width) // 2
            y = parent_y + (parent_h - popup_height) // 2
        except:
            x = (screen_w - popup_width) // 2
            y = (screen_h - popup_height) // 2
            
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)
        
        # Khóa tương tác cửa sổ chính
        popup.grab_set()
        
        # Bố cục lưới chính của popup
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=0) # Header
        popup.grid_rowconfigure(1, weight=1) # Main Scrollable content
        popup.grid_rowconfigure(2, weight=0) # Footer
        
        # ── 1. Header (Nền xanh nhạt, chữ đậm) ──
        header_frame = customtkinter.CTkFrame(
            popup,
            fg_color="#e0f2fe", # sky-100
            height=50,
            corner_radius=0
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_rowconfigure(0, weight=1)
        
        header_title = customtkinter.CTkLabel(
            header_frame,
            text="Phiếu Nhập Kho",
            font=(self.FONT_FAMILY, 18, "bold"),
            text_color="#0369a1", # sky-700
            anchor="w"
        )
        header_title.grid(row=0, column=0, padx=20, sticky="w")
        
        # ── 2. Nội dung chính cuộn được ──
        scroll_content = customtkinter.CTkScrollableFrame(
            popup,
            fg_color="#f8fafc", # xám cực nhạt làm nền
            corner_radius=0
        )
        scroll_content.grid(row=1, column=0, sticky="nsew")
        scroll_content.grid_columnconfigure(0, weight=1)
        
        # Section 1: Thông tin phiếu nhập
        section1_card = customtkinter.CTkFrame(
            scroll_content,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        section1_card.pack(fill="x", padx=15, pady=(15, 10))
        section1_card.grid_columnconfigure((0, 1, 2), weight=1)
        
        sec1_title = customtkinter.CTkLabel(
            section1_card,
            text="Thông tin phiếu nhập",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#3b82f6", # Màu xanh dương
            anchor="w"
        )
        sec1_title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")
        
        # Cột 1: Mã phiếu nhập *
        col1_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col1_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        lbl_ma = customtkinter.CTkLabel(col1_frame, text="Mã phiếu nhập *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ma.pack(anchor="w", pady=(0, 2))
        entry_ma = customtkinter.CTkEntry(col1_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ma.insert(0, "PN20604")
        entry_ma.pack(fill="x")
        
        # Cột 2: Ngày nhập hàng *
        col2_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col2_frame.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        lbl_ngay = customtkinter.CTkLabel(col2_frame, text="Ngày nhập hàng *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ngay.pack(anchor="w", pady=(0, 2))
        entry_ngay = customtkinter.CTkEntry(col2_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ngay.insert(0, "16/06/2026")
        entry_ngay.pack(fill="x")
        
        # Cột 3: Nhà cung cấp *
        col3_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col3_frame.grid(row=1, column=2, padx=15, pady=5, sticky="ew")
        lbl_ncc = customtkinter.CTkLabel(col3_frame, text="Nhà cung cấp *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ncc.pack(anchor="w", pady=(0, 2))
        entry_ncc = customtkinter.CTkEntry(col3_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ncc.insert(0, "Công ty TNHH thực phẩm")
        entry_ncc.pack(fill="x")
        
        # Dòng 2: Ghi chú (CTkTextbox nhỏ)
        note_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        note_frame.grid(row=2, column=0, columnspan=3, padx=15, pady=(10, 15), sticky="ew")
        lbl_note = customtkinter.CTkLabel(note_frame, text="Ghi chú", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_note.pack(anchor="w", pady=(0, 2))
        textbox_note = customtkinter.CTkTextbox(note_frame, height=60, corner_radius=6, border_width=1, border_color="#cbd5e1", fg_color="#f8fafc")
        textbox_note.pack(fill="x")
        
        # Section 2: Chi tiết nguyên liệu
        section2_card = customtkinter.CTkFrame(
            scroll_content,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        section2_card.pack(fill="both", expand=True, padx=15, pady=(10, 15))
        
        sec2_header = customtkinter.CTkFrame(section2_card, fg_color="transparent")
        sec2_header.pack(fill="x", padx=15, pady=(15, 10))
        
        sec2_title = customtkinter.CTkLabel(
            sec2_header,
            text="Chi tiết nguyên liệu",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#3b82f6",
            anchor="w"
        )
        sec2_title.pack(side="left")
        
        add_row_btn = customtkinter.CTkButton(
            sec2_header,
            text="+ Thêm nguyên liệu",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#10b981", # Xanh lá
            hover_color="#059669",
            text_color="#ffffff",
            corner_radius=6,
            height=28
        )
        add_row_btn.pack(side="right")
        
        # Lưới nhập liệu (Grid Frame giả lập bảng)
        grid_frame = customtkinter.CTkFrame(
            section2_card,
            fg_color="#f8fafc",
            corner_radius=6,
            border_width=1,
            border_color="#cbd5e1"
        )
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        grid_frame.grid_columnconfigure(0, weight=5)   # Stt
        grid_frame.grid_columnconfigure(1, weight=30)  # Nguyên liệu
        grid_frame.grid_columnconfigure(2, weight=15)  # Đơn vị
        grid_frame.grid_columnconfigure(3, weight=15)  # Số lượng
        grid_frame.grid_columnconfigure(4, weight=15)  # Giá nhập
        grid_frame.grid_columnconfigure(5, weight=15)  # Tổng tiền
        grid_frame.grid_columnconfigure(6, weight=20)  # Hạn sử dụng
        grid_frame.grid_columnconfigure(7, weight=5)   # Xóa
        
        # Dòng tiêu đề bảng chi tiết nguyên liệu
        headers_sec2 = ["Stt", "Nguyên liệu", "Đơn vị", "Số lượng", "Giá nhập", "Tổng tiền", "Hạn sử dụng", ""]
        for col_idx, h_text in enumerate(headers_sec2):
            lbl = customtkinter.CTkLabel(
                grid_frame,
                text=h_text,
                font=(self.FONT_FAMILY, 11, "bold"),
                text_color="#475569",
                anchor="center" if col_idx in [0, 2, 7] else "e" if col_idx in [3, 4, 5] else "w"
            )
            lbl.grid(row=0, column=col_idx, padx=4, pady=8, sticky="ew")
            
        # Dòng dữ liệu mẫu
        lbl_stt = customtkinter.CTkLabel(grid_frame, text="1", font=(self.FONT_FAMILY, 11), text_color="#1e293b")
        lbl_stt.grid(row=1, column=0, padx=4, pady=5)
        
        combo_nl = customtkinter.CTkComboBox(
            grid_frame,
            values=["Thịt bò", "Thịt heo", "Rau xà lách", "Bánh mì", "Bột mì"],
            font=(self.FONT_FAMILY, 11),
            dropdown_font=(self.FONT_FAMILY, 11),
            height=28,
            corner_radius=4,
            border_color="#cbd5e1"
        )
        combo_nl.set("Thịt bò")
        combo_nl.grid(row=1, column=1, padx=4, pady=5, sticky="ew")
        
        combo_dv = customtkinter.CTkComboBox(
            grid_frame,
            values=["kg", "g", "cái", "lít"],
            font=(self.FONT_FAMILY, 11),
            dropdown_font=(self.FONT_FAMILY, 11),
            height=28,
            corner_radius=4,
            border_color="#cbd5e1"
        )
        combo_dv.set("kg")
        combo_dv.grid(row=1, column=2, padx=4, pady=5, sticky="ew")
        
        entry_sl = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11), justify="right")
        entry_sl.insert(0, "20")
        entry_sl.grid(row=1, column=3, padx=4, pady=5, sticky="ew")
        
        entry_gn = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11), justify="right")
        entry_gn.insert(0, "200.000")
        entry_gn.grid(row=1, column=4, padx=4, pady=5, sticky="ew")
        
        lbl_tt = customtkinter.CTkLabel(grid_frame, text="4.000.000", font=(self.FONT_FAMILY, 11, "bold"), text_color="#1e293b", anchor="e")
        lbl_tt.grid(row=1, column=5, padx=4, pady=5, sticky="ew")
        
        entry_hsd = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11))
        entry_hsd.insert(0, "15/5/2026")
        entry_hsd.grid(row=1, column=6, padx=4, pady=5, sticky="ew")
        
        del_btn = customtkinter.CTkButton(
            grid_frame,
            text="🗑️",
            font=(self.FONT_FAMILY, 11),
            fg_color="#fee2e2",
            hover_color="#fca5a5",
            text_color="#ef4444",
            corner_radius=4,
            height=28,
            width=28
        )
        del_btn.grid(row=1, column=7, padx=4, pady=5)
        
        # ── 3. Footer (Tổng tiền bên trái, 2 nút bên phải) ──
        footer_frame = customtkinter.CTkFrame(
            popup,
            fg_color="#ffffff",
            height=60,
            corner_radius=0,
            border_width=1,
            border_color="#e2e8f0"
        )
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=0)
        footer_frame.grid_rowconfigure(0, weight=1)
        
        total_label = customtkinter.CTkLabel(
            footer_frame,
            text="Tổng tiền: 4.000.000",
            font=(self.FONT_FAMILY, 16, "bold"),
            text_color="#3b82f6",
            anchor="w"
        )
        total_label.grid(row=0, column=0, padx=20, sticky="w")
        
        footer_buttons = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
        footer_buttons.grid(row=0, column=1, padx=20, sticky="e")
        
        cancel_btn = customtkinter.CTkButton(
            footer_buttons,
            text="Hủy",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#ffffff",
            border_width=1,
            border_color="#cbd5e1",
            text_color="#0f172a",
            hover_color="#f1f5f9",
            corner_radius=6,
            height=36,
            width=80,
            command=popup.destroy
        )
        cancel_btn.pack(side="left", padx=5)
        
        save_btn = customtkinter.CTkButton(
            footer_buttons,
            text="Lưu phiếu nhập",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="#ffffff",
            corner_radius=6,
            height=36,
            command=popup.destroy
        )
        save_btn.pack(side="left", padx=5)


class ExportView(customtkinter.CTkScrollableFrame):
    """Màn hình Xuất Kho hiển thị các phiếu xuất hàng và danh sách hàng xuất."""
    
    def __init__(self, parent, font_family="Segoe UI"):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.FONT_FAMILY = font_family
        
        # Cấu hình grid cho self (đối tượng cuộn)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Dựng giao diện
        self.create_table_section()
        
    def create_table_section(self):
        """Tạo khu vực chứa bảng xuất kho (tìm kiếm và bảng Treeview)."""
        table_container = customtkinter.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        table_container.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        
        # ── 1. Thanh công cụ (Toolbar) ──
        toolbar = customtkinter.CTkFrame(
            table_container,
            fg_color="transparent"
        )
        toolbar.pack(fill="x", padx=15, pady=15)
        
        # Ô tìm kiếm bên trái
        search_entry = customtkinter.CTkEntry(
            toolbar,
            placeholder_text="Tìm mã hoặc tên nguyên liệu 🔍",
            font=(self.FONT_FAMILY, 12),
            width=300,
            height=34,
            corner_radius=6,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8"
        )
        search_entry.pack(side="left")
        
        # Nút "+ Thêm phiếu xuất" bên phải màu xanh dương nhạt
        add_btn = customtkinter.CTkButton(
            toolbar,
            text="+ Thêm phiếu xuất",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#e0f2fe", # sky-100
            hover_color="#bae6fd", # sky-200
            text_color="#0369a1", # sky-700
            corner_radius=6,
            height=34
        )
        add_btn.pack(side="right")
        
        # ── 2. Bảng dữ liệu (ttk.Treeview) ──
        import tkinter as tk
        from tkinter import ttk
        
        # Cấu hình style cho Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Export.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=32,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Export.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Export.Treeview.Heading",
            background="#E5E7EB", # Nền tiêu đề xám nhạt như yêu cầu
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        table_frame = customtkinter.CTkFrame(table_container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ma_lo", "nguyen_lieu", "sl_xuat", "don_vi", "ngay_xuat", "ly_do", "hsd")
        
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Export.Treeview"
        )
        
        # Zebra Row tags
        tree.tag_configure("evenrow", background="#ffffff")
        tree.tag_configure("oddrow", background="#f8fafc")
        
        # Tiêu đề cột
        headers = {
            "ma_lo": "Mã lô hàng",
            "nguyen_lieu": "Nguyên liệu",
            "sl_xuat": "Số lượng xuất",
            "don_vi": "Đơn vị",
            "ngay_xuat": "Ngày xuất",
            "ly_do": "Lý do xuất",
            "hsd": "Hạn sử dụng"
        }
        
        for col, heading in headers.items():
            tree.heading(col, text=heading, anchor="w")
            if col == "sl_xuat":
                tree.column(col, anchor="e", width=110)
            elif col in ["don_vi", "ngay_xuat", "hsd"]:
                tree.column(col, anchor="center", width=100)
            elif col == "ma_lo":
                tree.column(col, anchor="w", width=110)
            elif col == "ly_do":
                tree.column(col, anchor="w", width=180)
            else:
                tree.column(col, anchor="w", width=140)
                
        # Mock data 3 dòng
        mock_data = [
            ("PN20601", "Thịt", "20", "kg", "10/5/2026", "", "15/5/2026"),
            ("PN20601", "Thịt", "20", "", "10/5/2026", "", "15/5/2026"),
            ("PN20601", "bánh mì", "20", "cái", "11/5/2026", "", "15/5/2026")
        ]
        
        for i, item in enumerate(mock_data):
            row_tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=item, tags=(row_tag,))
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    app = DashboardWindow()
    app.mainloop()
