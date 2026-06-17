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
        self.main_divider = customtkinter.CTkFrame(
            self.main_frame,
            height=1,
            fg_color=self.DIVIDER_COLOR,
            corner_radius=0
        )
        self.main_divider.grid(row=1, column=0, sticky="ew", pady=(0, 15))

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

        # Hiển thị hoặc ẩn header & divider dựa trên tab hoạt động
        if self.active_tab_name in ["Quản lý nhà cung cấp", "Quản lý đơn hàng"]:
            self.header_frame.grid_remove()
            if hasattr(self, 'main_divider'):
                self.main_divider.grid_remove()
        else:
            self.header_frame.grid()
            if hasattr(self, 'main_divider'):
                self.main_divider.grid()

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
        elif self.active_tab_name == "Quản lý nhà cung cấp":
            supplier_view = SupplierView(self.content_area, font_family=self.FONT_FAMILY)
            supplier_view.pack(expand=True, fill="both")
        elif self.active_tab_name == "Quản lý đơn hàng":
            order_view = OrderView(self.content_area, font_family=self.FONT_FAMILY)
            order_view.pack(expand=True, fill="both")
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
            height=34,
            command=self.open_export_form
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

    def open_export_form(self):
        """Mở popup thêm phiếu xuất hàng mới (CTkToplevel)."""
        popup = customtkinter.CTkToplevel(self)
        popup.title("Thêm Phiếu Xuất Kho")
        
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
            text="Thêm Phiếu Xuất Kho",
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
        
        # Section 1: Thông tin phiếu xuất
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
            text="Thông tin phiếu xuất kho",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#3b82f6", # Màu xanh dương
            anchor="w"
        )
        sec1_title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")
        
        # Cột 1: Mã phiếu xuất *
        col1_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col1_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        lbl_ma = customtkinter.CTkLabel(col1_frame, text="Mã phiếu xuất *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ma.pack(anchor="w", pady=(0, 2))
        entry_ma = customtkinter.CTkEntry(col1_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ma.insert(0, "PX20604")
        entry_ma.pack(fill="x")
        
        # Cột 2: Ngày xuất *
        col2_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col2_frame.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        lbl_ngay = customtkinter.CTkLabel(col2_frame, text="Ngày xuất *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ngay.pack(anchor="w", pady=(0, 2))
        entry_ngay = customtkinter.CTkEntry(col2_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ngay.insert(0, "17/06/2026")
        entry_ngay.pack(fill="x")
        
        # Cột 3: Người nhận/Kho nhận *
        col3_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col3_frame.grid(row=1, column=2, padx=15, pady=5, sticky="ew")
        lbl_nhan = customtkinter.CTkLabel(col3_frame, text="Người nhận/Kho nhận *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_nhan.pack(anchor="w", pady=(0, 2))
        entry_nhan = customtkinter.CTkEntry(col3_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_nhan.insert(0, "Bếp chính - Khu A")
        entry_nhan.pack(fill="x")
        
        # Dòng 2: Ghi chú
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
            text="Chi tiết nguyên liệu xuất",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#3b82f6",
            anchor="w"
        )
        sec2_title.pack(side="left")
        
        # Lưới nhập liệu
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
        grid_frame.grid_columnconfigure(4, weight=30)  # Lý do xuất
        grid_frame.grid_columnconfigure(5, weight=5)   # Xóa
        
        headers_sec2 = ["Stt", "Nguyên liệu", "Đơn vị", "Số lượng", "Lý do xuất", ""]
        for col_idx, h_text in enumerate(headers_sec2):
            lbl = customtkinter.CTkLabel(
                grid_frame,
                text=h_text,
                font=(self.FONT_FAMILY, 11, "bold"),
                text_color="#475569",
                anchor="center" if col_idx in [0, 2, 5] else "e" if col_idx == 3 else "w"
            )
            lbl.grid(row=0, column=col_idx, padx=4, pady=8, sticky="ew")
            
        rows = []
        
        def add_row():
            row_idx = len(rows) + 1
            grid_row = row_idx
            
            lbl_stt = customtkinter.CTkLabel(grid_frame, text=str(row_idx), font=(self.FONT_FAMILY, 11), text_color="#1e293b")
            lbl_stt.grid(row=grid_row, column=0, padx=4, pady=5)
            
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
            combo_nl.grid(row=grid_row, column=1, padx=4, pady=5, sticky="ew")
            
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
            combo_dv.grid(row=grid_row, column=2, padx=4, pady=5, sticky="ew")
            
            entry_sl = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11), justify="right")
            entry_sl.insert(0, "10")
            entry_sl.grid(row=grid_row, column=3, padx=4, pady=5, sticky="ew")
            
            entry_lydo = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11))
            entry_lydo.insert(0, "Chế biến món ăn")
            entry_lydo.grid(row=grid_row, column=4, padx=4, pady=5, sticky="ew")
            
            row_widgets = {
                "stt_lbl": lbl_stt,
                "combo_nl": combo_nl,
                "combo_dv": combo_dv,
                "entry_sl": entry_sl,
                "entry_lydo": entry_lydo,
            }
            
            def delete_row():
                rows.remove(row_widgets)
                for w in row_widgets.values():
                    w.destroy()
                for i, r_w in enumerate(rows):
                    new_idx = i + 1
                    r_w["stt_lbl"].configure(text=str(new_idx))
                    r_w["stt_lbl"].grid(row=new_idx, column=0)
                    r_w["combo_nl"].grid(row=new_idx, column=1)
                    r_w["combo_dv"].grid(row=new_idx, column=2)
                    r_w["entry_sl"].grid(row=new_idx, column=3)
                    r_w["entry_lydo"].grid(row=new_idx, column=4)
                    r_w["del_btn"].grid(row=new_idx, column=5)
            
            del_btn = customtkinter.CTkButton(
                grid_frame,
                text="🗑️",
                font=(self.FONT_FAMILY, 11),
                fg_color="#fee2e2",
                hover_color="#fca5a5",
                text_color="#ef4444",
                corner_radius=4,
                height=28,
                width=28,
                command=delete_row
            )
            del_btn.grid(row=grid_row, column=5, padx=4, pady=5)
            row_widgets["del_btn"] = del_btn
            
            rows.append(row_widgets)

        add_row_btn = customtkinter.CTkButton(
            sec2_header,
            text="+ Thêm dòng",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#10b981", # Xanh lá
            hover_color="#059669",
            text_color="#ffffff",
            corner_radius=6,
            height=28,
            command=add_row
        )
        add_row_btn.pack(side="right")
        
        # Thêm dòng đầu tiên mặc định
        add_row()
        
        # ── 3. Footer (Nút Hủy và Lưu phiếu xuất) ──
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
        footer_frame.grid_rowconfigure(0, weight=1)
        
        footer_buttons = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
        footer_buttons.pack(side="right", padx=20)
        
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
            text="Lưu phiếu xuất",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="#ffffff",
            corner_radius=6,
            height=36,
            command=popup.destroy
        )
        save_btn.pack(side="left", padx=5)
 
 
class SupplierView(customtkinter.CTkFrame):
    """Màn hình Quản lý nhà cung cấp sử dụng Mock data."""
    
    def __init__(self, parent, font_family="Segoe UI"):
        super().__init__(parent, fg_color="#f5f6f8", corner_radius=0)
        self.FONT_FAMILY = font_family
        
        # Cấu hình grid cho màn hình chính của SupplierView
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Tiêu đề trang
        self.grid_rowconfigure(1, weight=0) # Đường kẻ phân cách
        self.grid_rowconfigure(2, weight=1) # Vùng chứa bảng (Table container)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập các thành phần giao diện chính."""
        # 1. Tiêu đề góc trái trên cùng
        self.title_label = customtkinter.CTkLabel(
            self,
            text="Quản lý nhà cung cấp",
            font=(self.FONT_FAMILY, 28, "bold"),
            text_color="#000000",
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Đường kẻ ngang mờ ở dưới để phân cách không gian
        self.divider = customtkinter.CTkFrame(
            self,
            height=1,
            fg_color="#cbd5e1",
            corner_radius=0
        )
        self.divider.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # 2. Khu vực Bảng (Table Container) - nền trắng, bo góc, có viền
        self.table_container = customtkinter.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.table_container.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        
        # Thanh công cụ (Toolbar) bên trong table_container
        self.toolbar = customtkinter.CTkFrame(
            self.table_container,
            fg_color="transparent"
        )
        self.toolbar.pack(fill="x", padx=15, pady=15)
        
        # Ô tìm kiếm bên trái
        self.search_entry = customtkinter.CTkEntry(
            self.toolbar,
            placeholder_text="Tìm mã hoặc tên nhà cung cấp 🔍",
            font=(self.FONT_FAMILY, 12),
            width=300,
            height=34,
            corner_radius=6,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8"
        )
        self.search_entry.pack(side="left")
        
        # Nút "+ Thêm nhà cung cấp" bên phải màu xanh dương nhạt
        self.add_btn = customtkinter.CTkButton(
            self.toolbar,
            text="+ Thêm nhà cung cấp",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#e0f2fe", # sky-100
            hover_color="#bae6fd", # sky-200
            text_color="#0369a1", # sky-700
            corner_radius=6,
            height=34,
            command=self.open_supplier_form
        )
        self.add_btn.pack(side="right")
        
        # Gọi hàm tạo bảng
        self.setup_table()
        
    def setup_table(self):
        """Cấu hình bảng ttk.Treeview hiển thị thông tin nhà cung cấp."""
        import tkinter as tk
        from tkinter import ttk
        
        # Cấu hình style cho Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Supplier.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=32,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Supplier.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Supplier.Treeview.Heading",
            background="#E5E7EB", # Nền tiêu đề xám nhạt như yêu cầu
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        # Khung bọc bảng và thanh cuộn
        table_frame = customtkinter.CTkFrame(self.table_container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ma_ncc", "ten_ncc", "dia_chi", "sdt", "email", "loai_ncc")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Supplier.Treeview"
        )
        
        # Cấu hình thẻ Zebra Row tag
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f8fafc")
        
        # Tiêu đề cột
        headers = {
            "ma_ncc": "Mã nhà cc",
            "ten_ncc": "Tên nhà cung cấp",
            "dia_chi": "Địa chỉ",
            "sdt": "Số điện thoại",
            "email": "Email",
            "loai_ncc": "Loại nhà cung cấp"
        }
        
        for col, heading in headers.items():
            self.tree.heading(col, text=heading, anchor="w")
            if col == "ma_ncc":
                self.tree.column(col, anchor="center", width=100)
            elif col == "sdt":
                self.tree.column(col, anchor="center", width=120)
            elif col == "loai_ncc":
                self.tree.column(col, anchor="w", width=140)
            elif col == "dia_chi":
                self.tree.column(col, anchor="w", width=220)
            else:
                self.tree.column(col, anchor="w", width=180)
                
        # Dữ liệu giả (Mock data)
        mock_data = [
            ("NCC001", "Công ty TNHH thực phẩm", "242 Huỳnh Văn Nghệ", "0123456789", "xyz.@gmail.com", "NCC chính"),
            ("NCC002", "Công ty TNHH thực phẩm", "242 Huỳnh Văn Nghệ", "0123456789", "xyz.@gmail.com", "NCC phụ"),
            ("NCC003", "Nhà phân phối nông sản Sạch", "12 Hoàng Hoa Thám", "0987654321", "nongsansach@gmail.com", "NCC phụ"),
            ("NCC004", "Tổng kho gia vị miền Nam", "456 Lê Lợi", "0911223344", "giavimiennam@gmail.com", "NCC chính"),
            ("NCC005", "Đại lý bao bì Hoàng Gia", "789 Nguyễn Huệ", "0933445566", "hoanggia@gmail.com", "NCC phụ"),
            ("NCC006", "Nước đá tinh khiết Bình Minh", "321 Trần Hưng Đạo", "0944556677", "binhminh@gmail.com", "NCC phụ"),
        ]
        
        for i, item in enumerate(mock_data):
            row_tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=item, tags=(row_tag,))
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def open_supplier_form(self):
        """Mở popup thêm nhà cung cấp mới (CTkToplevel)."""
        popup = customtkinter.CTkToplevel(self)
        popup.title("Thêm Nhà Cung Cấp Mới")
        
        # Kích thước popup 500x500
        popup_width = 500
        popup_height = 500
        
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
            text="Thêm Nhà Cung Cấp Mới",
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
        
        # Card chứa Form nhập thông tin
        form_card = customtkinter.CTkFrame(
            scroll_content,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        form_card.pack(fill="x", padx=15, pady=15)
        form_card.grid_columnconfigure(0, weight=1)
        
        # Helper to create a vertical label-entry pair
        def create_field(parent, row, label_text, default_value="", is_combo=False, combo_values=None):
            field_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
            field_frame.grid(row=row, column=0, padx=15, pady=8, sticky="ew")
            
            lbl = customtkinter.CTkLabel(
                field_frame, 
                text=label_text, 
                font=(self.FONT_FAMILY, 12, "bold"), 
                text_color="#475569"
            )
            lbl.pack(anchor="w", pady=(0, 2))
            
            if is_combo:
                widget = customtkinter.CTkComboBox(
                    field_frame,
                    values=combo_values or [],
                    height=32,
                    corner_radius=6,
                    border_color="#cbd5e1",
                    fg_color="#f8fafc",
                    font=(self.FONT_FAMILY, 12),
                    dropdown_font=(self.FONT_FAMILY, 12)
                )
                if default_value:
                    widget.set(default_value)
            else:
                widget = customtkinter.CTkEntry(
                    field_frame,
                    height=32,
                    corner_radius=6,
                    border_color="#cbd5e1",
                    fg_color="#f8fafc",
                    font=(self.FONT_FAMILY, 12)
                )
                if default_value:
                    widget.insert(0, default_value)
            
            widget.pack(fill="x")
            return widget

        # Xếp dọc các trường thông tin
        create_field(form_card, 0, "Mã nhà cung cấp *", "NCC007")
        create_field(form_card, 1, "Tên nhà cung cấp *", "Công ty TNHH Bánh kẹo Ánh Dương")
        create_field(form_card, 2, "Số điện thoại *", "0922334455")
        create_field(form_card, 3, "Email *", "anhduong@gmail.com")
        create_field(form_card, 4, "Địa chỉ *", "123 Đường 3/2, Quận 10, TP.HCM")
        create_field(form_card, 5, "Loại nhà cung cấp *", "NCC chính", is_combo=True, combo_values=["NCC chính", "NCC phụ"])
        
        # ── 3. Footer (Nút Hủy và Lưu thông tin) ──
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
        footer_frame.grid_rowconfigure(0, weight=1)
        
        footer_buttons = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
        footer_buttons.pack(side="right", padx=20)
        
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
            text="Lưu thông tin",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#3b82f6", # Màu xanh dương
            hover_color="#2563eb",
            text_color="#ffffff",
            corner_radius=6,
            height=36,
            command=popup.destroy
        )
        save_btn.pack(side="left", padx=5)


class OrderView(customtkinter.CTkFrame):
    """Màn hình Quản lý đơn hàng sử dụng Mock data."""
    
    def __init__(self, parent, font_family="Segoe UI"):
        super().__init__(parent, fg_color="#f5f6f8", corner_radius=0)
        self.FONT_FAMILY = font_family
        
        # Cấu hình grid chính cho OrderView
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Tiêu đề trang
        self.grid_rowconfigure(1, weight=0) # Đường kẻ phân cách
        self.grid_rowconfigure(2, weight=0) # Thẻ tổng quan
        self.grid_rowconfigure(3, weight=1) # Vùng chứa chính (Split screen)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập các thành phần giao diện chính."""
        # 1. Tiêu đề góc trái trên cùng
        self.title_label = customtkinter.CTkLabel(
            self,
            text="Quản lý đơn hàng",
            font=(self.FONT_FAMILY, 28, "bold"),
            text_color="#000000",
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Đường kẻ ngang mờ ở dưới để phân cách
        self.divider = customtkinter.CTkFrame(
            self,
            height=1,
            fg_color="#cbd5e1",
            corner_radius=0
        )
        self.divider.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # 2. Thẻ Tổng Quan (Overview Cards)
        cards_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        cards_data = [
            ("Tổng đơn hàng", "180", "#10b981"),        # xanh lá
            ("Tổng giá trị đơn hàng", "12.000.000đ", "#3b82f6"), # xanh dương
            ("Đã hủy", "12", "#854d0e"),                  # vàng rêu/olive
            ("Đã hoàn tất", "168", "#ef4444")             # đỏ
        ]
        
        for i, (title, value, color) in enumerate(cards_data):
            card = customtkinter.CTkFrame(
                cards_frame,
                fg_color="#ffffff",
                corner_radius=10,
                border_width=1,
                border_color="#e2e8f0",
                height=90
            )
            card.grid(row=0, column=i, padx=(0 if i==0 else 10, 0), sticky="ew")
            card.grid_propagate(False)
            
            lbl_title = customtkinter.CTkLabel(
                card, 
                text=title, 
                font=(self.FONT_FAMILY, 12, "bold"), 
                text_color="#64748b",
                anchor="w"
            )
            lbl_title.pack(anchor="w", padx=15, pady=(15, 2))
            
            lbl_val = customtkinter.CTkLabel(
                card, 
                text=value, 
                font=(self.FONT_FAMILY, 24, "bold"), 
                text_color=color,
                anchor="w"
            )
            lbl_val.pack(anchor="w", padx=15, pady=(0, 15))

        # 3. Vùng chứa chính (Split screen layout)
        self.content_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=3, column=0, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=7)
        self.content_container.grid_columnconfigure(1, weight=0)
        
        # table_frame (bên trái)
        self.table_frame = customtkinter.CTkFrame(
            self.content_container,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        self.table_frame.grid(row=0, column=0, sticky="nsew")
        
        # Toolbar của table_frame
        toolbar = customtkinter.CTkFrame(self.table_frame, fg_color="transparent")
        toolbar.pack(fill="x", padx=15, pady=15)
        
        search_entry = customtkinter.CTkEntry(
            toolbar,
            placeholder_text="Tìm kiếm đơn hàng... 🔍",
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
        
        add_btn = customtkinter.CTkButton(
            toolbar,
            text="+ Thêm đơn hàng",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#e0f2fe", # sky-100
            hover_color="#bae6fd", # sky-200
            text_color="#0369a1", # sky-700
            corner_radius=6,
            height=34,
            command=self.open_add_order_form
        )
        add_btn.pack(side="right")
        
        # Bảng Treeview
        import tkinter as tk
        from tkinter import ttk
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Order.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=32,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Order.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Order.Treeview.Heading",
            background="#E5E7EB",
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        table_inner_frame = customtkinter.CTkFrame(self.table_frame, fg_color="transparent")
        table_inner_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ma_dh", "danh_sach", "ngay_dat", "gia_tri", "trang_thai")
        
        self.tree = ttk.Treeview(
            table_inner_frame,
            columns=columns,
            show="headings",
            style="Order.Treeview"
        )
        
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f8fafc")
        
        headers = {
            "ma_dh": "Mã đơn hàng",
            "danh_sach": "Danh sách đơn hàng",
            "ngay_dat": "Ngày đặt hàng",
            "gia_tri": "Giá trị đơn hàng",
            "trang_thai": "Trạng thái"
        }
        
        for col, heading in headers.items():
            self.tree.heading(col, text=heading, anchor="w")
            if col == "ma_dh":
                self.tree.column(col, anchor="center", width=100)
            elif col == "ngay_dat":
                self.tree.column(col, anchor="center", width=120)
            elif col == "gia_tri":
                self.tree.column(col, anchor="e", width=130)
            elif col == "trang_thai":
                self.tree.column(col, anchor="center", width=120)
            else:
                self.tree.column(col, anchor="w", width=250)
                
        mock_data = [
            ("DH0001", "Hamburger bò, Khoai tây chiên, Coca-Cola", "15/05/2026", "250.000", "Đã hoàn tất"),
            ("DH0002", "Pizza hải sản, Tỏi nướng, Pepsi", "16/05/2026", "450.000", "Đã hoàn tất"),
            ("DH0003", "Mỳ Ý sốt bò bằm, Nước ép cam", "17/05/2026", "180.000", "Đã hủy"),
            ("DH0004", "Hamburger gà, Gà rán (2 miếng), Fanta", "17/05/2026", "320.000", "Đã hoàn tất"),
            ("DH0005", "Salad ức gà, Súp bí đỏ, Nước suối", "17/05/2026", "150.000", "Đang xử lý")
        ]
        
        for i, item in enumerate(mock_data):
            row_tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=item, tags=(row_tag,))
            
        scrollbar = ttk.Scrollbar(table_inner_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.tree.bind("<Double-1>", self.on_row_double_click)
        
        # detail_frame (bên phải, ẩn lúc đầu)
        self.detail_frame = customtkinter.CTkFrame(
            self.content_container,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0",
            width=450
        )
        self.detail_frame.grid_propagate(False)
        
        detail_header = customtkinter.CTkFrame(self.detail_frame, fg_color="transparent")
        detail_header.pack(fill="x", padx=15, pady=(15, 10))
        
        lbl_detail_title = customtkinter.CTkLabel(
            detail_header,
            text="Lịch sử đơn hàng",
            font=(self.FONT_FAMILY, 16, "bold"),
            text_color="#1e293b",
            anchor="w"
        )
        lbl_detail_title.pack(side="left")
        
        close_btn = customtkinter.CTkButton(
            detail_header,
            text="✖",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="transparent",
            text_color="#94a3b8",
            hover_color="#fee2e2",
            width=28,
            height=28,
            corner_radius=14,
            command=self.hide_detail_frame
        )
        close_btn.pack(side="right")
        
        detail_divider = customtkinter.CTkFrame(self.detail_frame, height=1, fg_color="#cbd5e1")
        detail_divider.pack(fill="x", padx=15, pady=(0, 10))
        
        self.detail_scroll = customtkinter.CTkScrollableFrame(
            self.detail_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.detail_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 15))

    def on_row_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        values = self.tree.item(selected_item[0], "values")
        if not values:
            return
        
        ma_dh, ngay_dat, danh_sach, gia_tri, trang_thai = values[0], values[2], values[1], values[3], values[4]
        self.show_order_detail(ma_dh, ngay_dat, danh_sach, gia_tri, trang_thai)
        
    def hide_detail_frame(self):
        self.content_container.grid_columnconfigure(1, weight=0)
        self.detail_frame.grid_forget()

    def get_order_items(self, ma_dh):
        db = {
            "DH0001": [
                ("Hamburger bò", 1, "150.000"),
                ("Khoai tây chiên", 1, "60.000"),
                ("Coca-Cola", 2, "20.000")
            ],
            "DH0002": [
                ("Pizza hải sản", 1, "350.000"),
                ("Tỏi nướng", 1, "50.000"),
                ("Pepsi", 2, "25.000")
            ],
            "DH0003": [
                ("Mỳ Ý sốt bò bằm", 1, "130.000"),
                ("Nước ép cam", 1, "50.000")
            ],
            "DH0004": [
                ("Hamburger gà", 1, "120.000"),
                ("Gà rán (2 miếng)", 1, "160.000"),
                ("Fanta", 2, "20.000")
            ],
            "DH0005": [
                ("Salad ức gà", 1, "90.000"),
                ("Súp bí đỏ", 1, "40.000"),
                ("Nước suối", 1, "20.000")
            ],
        }
        return db.get(ma_dh, [("Món ăn mẫu", 1, "100.000")])

    def num_to_vietnamese_words(self, value_str):
        db = {
            "250.000": "Hai trăm năm mươi nghìn đồng",
            "450.000": "Bốn trăm năm mươi nghìn đồng",
            "180.000": "Một trăm tám mươi nghìn đồng",
            "320.000": "Ba trăm hai mươi nghìn đồng",
            "150.000": "Một trăm năm mươi nghìn đồng"
        }
        return db.get(value_str, "Không xác định")

    def show_order_detail(self, ma_dh, ngay_dat, danh_sach, gia_tri, trang_thai):
        self.content_container.grid_columnconfigure(1, weight=3)
        self.detail_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        for w in self.detail_scroll.winfo_children():
            w.destroy()
            
        info_frame = customtkinter.CTkFrame(self.detail_scroll, fg_color="transparent")
        info_frame.pack(fill="x", pady=(5, 10))
        
        ma_lbl = customtkinter.CTkLabel(info_frame, text=ma_dh, font=(self.FONT_FAMILY, 20, "bold"), text_color="#0f172a")
        ma_lbl.pack(anchor="w")
        
        badge_colors = {
            "Đã hoàn tất": ("#d1fae5", "#065f46"),
            "Đang xử lý": ("#dbeafe", "#1e40af"),
            "Đã hủy": ("#fee2e2", "#991b1b")
        }
        bg, fg = badge_colors.get(trang_thai, ("#f1f5f9", "#475569"))
        
        badge = customtkinter.CTkLabel(
            info_frame,
            text=trang_thai,
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color=bg,
            text_color=fg,
            corner_radius=4,
            height=20,
            padx=8
        )
        badge.pack(anchor="w", pady=(4, 0))
        
        ngay_lbl = customtkinter.CTkLabel(
            self.detail_scroll, 
            text=f"Ngày đặt hàng: {ngay_dat}", 
            font=(self.FONT_FAMILY, 12), 
            text_color="#475569"
        )
        ngay_lbl.pack(anchor="w", pady=(0, 15))
        
        items_card = customtkinter.CTkFrame(self.detail_scroll, fg_color="#f8fafc", corner_radius=6, border_width=1, border_color="#cbd5e1")
        items_card.pack(fill="x", pady=(0, 15))
        
        header_grid = customtkinter.CTkFrame(items_card, fg_color="transparent")
        header_grid.pack(fill="x", padx=10, pady=5)
        customtkinter.CTkLabel(header_grid, text="Tên món", font=(self.FONT_FAMILY, 11, "bold"), text_color="#475569", anchor="w").pack(side="left")
        customtkinter.CTkLabel(header_grid, text="Giá (SL)", font=(self.FONT_FAMILY, 11, "bold"), text_color="#475569", anchor="e").pack(side="right")
        
        divider = customtkinter.CTkFrame(items_card, height=1, fg_color="#e2e8f0")
        divider.pack(fill="x", padx=10, pady=(0, 5))
        
        items = self.get_order_items(ma_dh)
        for name, qty, price in items:
            row = customtkinter.CTkFrame(items_card, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=3)
            
            customtkinter.CTkLabel(row, text=name, font=(self.FONT_FAMILY, 12), text_color="#1e293b", anchor="w").pack(side="left")
            customtkinter.CTkLabel(row, text=f"{price} x {qty}", font=(self.FONT_FAMILY, 12), text_color="#1e293b", anchor="e").pack(side="right")
            
        total_frame = customtkinter.CTkFrame(self.detail_scroll, fg_color="transparent")
        total_frame.pack(fill="x", pady=(5, 5))
        
        customtkinter.CTkLabel(total_frame, text="Tổng giá trị:", font=(self.FONT_FAMILY, 13, "bold"), text_color="#475569").pack(side="left")
        customtkinter.CTkLabel(total_frame, text=f"{gia_tri}đ", font=(self.FONT_FAMILY, 16, "bold"), text_color="#ef4444").pack(side="right")
        
        words = self.num_to_vietnamese_words(gia_tri)
        words_lbl = customtkinter.CTkLabel(
            self.detail_scroll,
            text=f"Bằng chữ: {words} chẵn.",
            font=(self.FONT_FAMILY, 11, "italic"),
            text_color="#64748b",
            wraplength=410,
            justify="left",
            anchor="w"
        )
        words_lbl.pack(anchor="w", pady=(5, 10))

    def open_add_order_form(self):
        """Mở popup thêm đơn hàng mới (CTkToplevel)."""
        popup = customtkinter.CTkToplevel(self)
        popup.title("Thêm Đơn Hàng Mới")
        
        popup_width = 800
        popup_height = 650
        
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
        popup.grab_set()
        
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=0) # Header
        popup.grid_rowconfigure(1, weight=1) # Main Scrollable content
        popup.grid_rowconfigure(2, weight=0) # Footer
        
        # ── 1. Header (Xanh dương, chữ trắng) ──
        header_frame = customtkinter.CTkFrame(
            popup,
            fg_color="#1e3a8a",
            height=50,
            corner_radius=0
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_rowconfigure(0, weight=1)
        
        header_title = customtkinter.CTkLabel(
            header_frame,
            text="Quản lý đơn hàng",
            font=(self.FONT_FAMILY, 18, "bold"),
            text_color="#ffffff",
            anchor="w"
        )
        header_title.grid(row=0, column=0, padx=20, sticky="w")
        
        # ── 2. Nội dung chính cuộn được ──
        scroll_content = customtkinter.CTkScrollableFrame(
            popup,
            fg_color="#f8fafc",
            corner_radius=0
        )
        scroll_content.grid(row=1, column=0, sticky="nsew")
        scroll_content.grid_columnconfigure(0, weight=1)
        
        # Section 1: Thông tin đơn hàng
        section1_card = customtkinter.CTkFrame(
            scroll_content,
            fg_color="#ffffff",
            corner_radius=8,
            border_width=1,
            border_color="#e2e8f0"
        )
        section1_card.pack(fill="x", padx=15, pady=(15, 10))
        section1_card.grid_columnconfigure((0, 1), weight=1)
        
        sec1_title = customtkinter.CTkLabel(
            section1_card,
            text="Thông tin đơn hàng",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#1e3a8a",
            anchor="w"
        )
        sec1_title.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")
        
        # Cột 1: Mã đơn hàng *
        col1_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col1_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        lbl_ma = customtkinter.CTkLabel(col1_frame, text="Mã đơn hàng *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ma.pack(anchor="w", pady=(0, 2))
        entry_ma = customtkinter.CTkEntry(col1_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ma.insert(0, "DH0006")
        entry_ma.pack(fill="x")
        
        # Cột 2: Ngày đặt *
        col2_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        col2_frame.grid(row=1, column=1, padx=15, pady=5, sticky="ew")
        lbl_ngay = customtkinter.CTkLabel(col2_frame, text="Ngày đặt *", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_ngay.pack(anchor="w", pady=(0, 2))
        entry_ngay = customtkinter.CTkEntry(col2_frame, height=32, corner_radius=6, border_color="#cbd5e1", fg_color="#f8fafc")
        entry_ngay.insert(0, "17/06/2026")
        entry_ngay.pack(fill="x")
        
        # Dòng 2: Ghi chú
        note_frame = customtkinter.CTkFrame(section1_card, fg_color="transparent")
        note_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=(10, 15), sticky="ew")
        lbl_note = customtkinter.CTkLabel(note_frame, text="Ghi chú", font=(self.FONT_FAMILY, 12, "bold"), text_color="#475569")
        lbl_note.pack(anchor="w", pady=(0, 2))
        textbox_note = customtkinter.CTkTextbox(note_frame, height=60, corner_radius=6, border_width=1, border_color="#cbd5e1", fg_color="#f8fafc")
        textbox_note.pack(fill="x")
        
        # Section 2: Thông tin món ăn
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
            text="Thông tin món ăn",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#1e3a8a",
            anchor="w"
        )
        sec2_title.pack(side="left")
        
        # Lưới nhập liệu
        grid_frame = customtkinter.CTkFrame(
            section2_card,
            fg_color="#f8fafc",
            corner_radius=6,
            border_width=1,
            border_color="#cbd5e1"
        )
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        grid_frame.grid_columnconfigure(0, weight=5)   # Stt
        grid_frame.grid_columnconfigure(1, weight=30)  # Món ăn
        grid_frame.grid_columnconfigure(2, weight=15)  # Giá tiền
        grid_frame.grid_columnconfigure(3, weight=15)  # Số lượng
        grid_frame.grid_columnconfigure(4, weight=15)  # Thành tiền
        grid_frame.grid_columnconfigure(5, weight=5)   # Xóa
        
        headers_sec2 = ["Stt", "Món ăn", "Giá tiền", "Số lượng", "Thành tiền", ""]
        for col_idx, h_text in enumerate(headers_sec2):
            lbl = customtkinter.CTkLabel(
                grid_frame,
                text=h_text,
                font=(self.FONT_FAMILY, 11, "bold"),
                text_color="#475569",
                anchor="center" if col_idx in [0, 3, 5] else "e" if col_idx in [2, 4] else "w"
            )
            lbl.grid(row=0, column=col_idx, padx=4, pady=8, sticky="ew")
            
        rows = []
        
        def recalculate_total():
            grand_total = 0
            for r in rows:
                try:
                    price_str = r["entry_price"].get().replace(".", "").strip()
                    qty_str = r["entry_qty"].get().strip()
                    price = int(price_str) if price_str else 0
                    qty = int(qty_str) if qty_str else 0
                    row_total = price * qty
                    r["lbl_row_total"].configure(text=f"{row_total:,}".replace(",", "."))
                    grand_total += row_total
                except Exception:
                    pass
            total_label.configure(text=f"Tổng tiền: {grand_total:,}đ".replace(",", "."))
            
        def add_row():
            row_idx = len(rows) + 1
            grid_row = row_idx
            
            lbl_stt = customtkinter.CTkLabel(grid_frame, text=str(row_idx), font=(self.FONT_FAMILY, 11), text_color="#1e293b")
            lbl_stt.grid(row=grid_row, column=0, padx=4, pady=5)
            
            combo_mon = customtkinter.CTkComboBox(
                grid_frame,
                values=["Hamburger bò", "Hamburger gà", "Pizza hải sản", "Khoai tây chiên", "Mỳ Ý sốt bò bằm", "Gà rán (2 miếng)"],
                font=(self.FONT_FAMILY, 11),
                dropdown_font=(self.FONT_FAMILY, 11),
                height=28,
                corner_radius=4,
                border_color="#cbd5e1",
                command=lambda val: on_dish_change(val)
            )
            combo_mon.set("Hamburger bò")
            combo_mon.grid(row=grid_row, column=1, padx=4, pady=5, sticky="ew")
            
            entry_price = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11), justify="right")
            entry_price.insert(0, "150.000")
            entry_price.grid(row=grid_row, column=2, padx=4, pady=5, sticky="ew")
            entry_price.bind("<KeyRelease>", lambda e: recalculate_total())
            
            entry_qty = customtkinter.CTkEntry(grid_frame, height=28, corner_radius=4, border_color="#cbd5e1", font=(self.FONT_FAMILY, 11), justify="right")
            entry_qty.insert(0, "1")
            entry_qty.grid(row=grid_row, column=3, padx=4, pady=5, sticky="ew")
            entry_qty.bind("<KeyRelease>", lambda e: recalculate_total())
            
            lbl_row_total = customtkinter.CTkLabel(grid_frame, text="150.000", font=(self.FONT_FAMILY, 11, "bold"), text_color="#1e293b", anchor="e")
            lbl_row_total.grid(row=grid_row, column=4, padx=4, pady=5, sticky="ew")
            
            row_widgets = {
                "stt_lbl": lbl_stt,
                "combo_mon": combo_mon,
                "entry_price": entry_price,
                "entry_qty": entry_qty,
                "lbl_row_total": lbl_row_total,
            }
            
            def on_dish_change(val):
                price_map = {
                    "Hamburger bò": "150.000",
                    "Hamburger gà": "120.000",
                    "Pizza hải sản": "350.000",
                    "Khoai tây chiên": "60.000",
                    "Mỳ Ý sốt bò bằm": "130.000",
                    "Gà rán (2 miếng)": "160.000"
                }
                entry_price.delete(0, "end")
                entry_price.insert(0, price_map.get(val, "50.000"))
                recalculate_total()
                
            def delete_row():
                rows.remove(row_widgets)
                for w in row_widgets.values():
                    w.destroy()
                for i, r_w in enumerate(rows):
                    new_idx = i + 1
                    r_w["stt_lbl"].configure(text=str(new_idx))
                    r_w["stt_lbl"].grid(row=new_idx, column=0)
                    r_w["combo_mon"].grid(row=new_idx, column=1)
                    r_w["entry_price"].grid(row=new_idx, column=2)
                    r_w["entry_qty"].grid(row=new_idx, column=3)
                    r_w["lbl_row_total"].grid(row=new_idx, column=4)
                    r_w["del_btn"].grid(row=new_idx, column=5)
                recalculate_total()
            
            del_btn = customtkinter.CTkButton(
                grid_frame,
                text="🗑️",
                font=(self.FONT_FAMILY, 11),
                fg_color="#fee2e2",
                hover_color="#fca5a5",
                text_color="#ef4444",
                corner_radius=4,
                height=28,
                width=28,
                command=delete_row
            )
            del_btn.grid(row=grid_row, column=5, padx=4, pady=5)
            row_widgets["del_btn"] = del_btn
            
            rows.append(row_widgets)
            recalculate_total()

        add_row_btn = customtkinter.CTkButton(
            sec2_header,
            text="+ Thêm món ăn",
            font=(self.FONT_FAMILY, 11, "bold"),
            fg_color="#10b981", # Xanh lá
            hover_color="#059669",
            text_color="#ffffff",
            corner_radius=6,
            height=28,
            command=add_row
        )
        add_row_btn.pack(side="right")
        
        add_row()
        
        # ── 3. Footer (Nút Hủy và Lưu đơn hàng) ──
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
        footer_frame.grid_rowconfigure(0, weight=1)
        
        total_label = customtkinter.CTkLabel(
            footer_frame,
            text="Tổng tiền: 150.000đ",
            font=(self.FONT_FAMILY, 16, "bold"),
            text_color="#1e3a8a",
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
            text="Lưu đơn hàng",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="#ffffff",
            corner_radius=6,
            height=36,
            command=popup.destroy
        )
        save_btn.pack(side="left", padx=5)


if __name__ == "__main__":
    app = DashboardWindow()
    app.mainloop()
