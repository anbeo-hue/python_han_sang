import tkinter as tk
from tkinter import ttk
import customtkinter
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Thiết lập font và style chung
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

class PredictionView(customtkinter.CTkScrollableFrame):
    """Màn hình Dự đoán tháng tới (PredictionView) với các biểu đồ, sự kiện và bảng chi tiết."""
    
    def __init__(self, parent, font_family="Segoe UI"):
        super().__init__(parent, fg_color="transparent", corner_radius=0)
        self.FONT_FAMILY = font_family
        
        # Cấu hình grid chính
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Tiêu đề
        self.grid_rowconfigure(1, weight=0)  # 4 Summary Cards
        self.grid_rowconfigure(2, weight=0)  # Middle Section (Events & Matplotlib Chart)
        self.grid_rowconfigure(3, weight=1)  # Table Area
        
        # Bộ dữ liệu Mock Data cho các nguyên liệu
        self.ingredients_data = {
            "NL001": {
                "ma": "NL001",
                "ten": "Thịt bò",
                "t5": "350 kg",
                "t6": "420 kg",
                "t7_forecast": "520.5 kg",
                "percent": "+24%",
                "val_t5": 350.0,
                "val_t6": 420.0,
                "avg": 385.0,
                "holiday_effect": 0.30,
                "expected": 500.5,
                "safety_stock": 20.0,
                "color": "#10b981", # Xanh lá
                "chart_data": [350, 420, 520.5]
            },
            "NL002": {
                "ma": "NL002",
                "ten": "Thịt heo",
                "t5": "400 kg",
                "t6": "450 kg",
                "t7_forecast": "585.0 kg",
                "percent": "+30%",
                "val_t5": 400.0,
                "val_t6": 450.0,
                "avg": 425.0,
                "holiday_effect": 0.30,
                "expected": 552.5,
                "safety_stock": 32.5,
                "color": "#3498db", # Xanh dương
                "chart_data": [400, 450, 585.0]
            },
            "NL003": {
                "ma": "NL003",
                "ten": "Cá hồi",
                "t5": "120 kg",
                "t6": "130 kg",
                "t7_forecast": "143.0 kg",
                "percent": "+10%",
                "val_t5": 120.0,
                "val_t6": 130.0,
                "avg": 125.0,
                "holiday_effect": 0.10,
                "expected": 137.5,
                "safety_stock": 5.5,
                "color": "#9b59b6", # Tím
                "chart_data": [120, 130, 143.0]
            },
            "NL004": {
                "ma": "NL004",
                "ten": "Rau xà lách",
                "t5": "200 kg",
                "t6": "220 kg",
                "t7_forecast": "286.0 kg",
                "percent": "+30%",
                "val_t5": 200.0,
                "val_t6": 220.0,
                "avg": 210.0,
                "holiday_effect": 0.30,
                "expected": 273.0,
                "safety_stock": 13.0,
                "color": "#e67e22", # Cam
                "chart_data": [200, 220, 286.0]
            },
            "NL005": {
                "ma": "NL005",
                "ten": "Bột mì",
                "t5": "600 kg",
                "t6": "620 kg",
                "t7_forecast": "682.0 kg",
                "percent": "+10%",
                "val_t5": 600.0,
                "val_t6": 620.0,
                "avg": 610.0,
                "holiday_effect": 0.10,
                "expected": 671.0,
                "safety_stock": 11.0,
                "color": "#1abc9c", # Teal
                "chart_data": [600, 620, 682.0]
            }
        }
        
        # 1. TIÊU ĐỀ
        self.create_title_section()
        
        # 2. 4 THẺ TỔNG QUAN
        self.create_summary_cards()
        
        # 3. KHU VỰC PHÂN TÍCH CHIA 2 CỘT
        self.create_analysis_section()
        
        # 4. KHU VỰC BẢNG DỰ BÁO CHI TIẾT
        self.create_table_section()
        
    def create_title_section(self):
        """Tạo tiêu đề trang và đường kẻ phân cách."""
        title_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        title_lbl = customtkinter.CTkLabel(
            title_frame,
            text="Dự đoán tháng tới",
            font=(self.FONT_FAMILY, 26, "bold"),
            text_color="#0f172a"
        )
        title_lbl.pack(side="left")
        
        divider = customtkinter.CTkFrame(self, height=2, fg_color="#cbd5e1")
        divider.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
    def create_summary_cards(self):
        """Tạo 4 thẻ tổng quan nằm ngang đẹp mắt."""
        cards_container = customtkinter.CTkFrame(self, fg_color="transparent")
        cards_container.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        # Cấu hình chia 4 cột đều nhau
        for i in range(4):
            cards_container.grid_columnconfigure(i, weight=1, uniform="pred_cards")
            
        # Dữ liệu của 4 card
        # Thẻ 1: Xanh lá, Thẻ 2: Xanh dương, Thẻ 3: Vàng rêu, Thẻ 4: Đỏ
        cards_data = [
            {"title": "Tổng món ăn", "value": "180", "color": "#10b981", "bg_icon": "#e6f4ea", "icon": "🍳"},
            {"title": "Tổng nguyên liệu", "value": "12.000.000", "color": "#3b82f6", "bg_icon": "#e8f0fe", "icon": "📦"},
            {"title": "Nguyên liệu cần nhập", "value": "12.000.000", "color": "#a16207", "bg_icon": "#fef9c3", "icon": "🛒"},
            {"title": "Tổng nguyên liệu dự kiến", "value": "12.000.000", "color": "#ef4444", "bg_icon": "#fee2e2", "icon": "🔮"}
        ]
        
        for idx, data in enumerate(cards_data):
            card = customtkinter.CTkFrame(
                cards_container,
                fg_color="#ffffff",
                corner_radius=10,
                border_width=1,
                border_color="#e2e8f0"
            )
            # Tạo khoảng cách margin hợp lý
            card.grid(row=0, column=idx, sticky="nsew", padx=6 if idx > 0 and idx < 3 else (0, 6) if idx == 0 else (6, 0))
            
            card.grid_columnconfigure(0, weight=0)
            card.grid_columnconfigure(1, weight=1)
            
            # Icon Badge tròn
            icon_badge = customtkinter.CTkLabel(
                card,
                text=data["icon"],
                font=(self.FONT_FAMILY, 18),
                fg_color=data["bg_icon"],
                text_color=data["color"],
                width=42,
                height=42,
                corner_radius=21
            )
            icon_badge.grid(row=0, column=0, rowspan=2, padx=15, pady=18, sticky="w")
            
            # Tiêu đề card
            title_lbl = customtkinter.CTkLabel(
                card,
                text=data["title"],
                font=(self.FONT_FAMILY, 12, "bold"),
                text_color="#64748b",
                anchor="w"
            )
            title_lbl.grid(row=0, column=1, padx=(0, 15), pady=(12, 2), sticky="w")
            
            # Giá trị
            val_lbl = customtkinter.CTkLabel(
                card,
                text=data["value"],
                font=(self.FONT_FAMILY, 18, "bold"),
                text_color=data["color"],
                anchor="w"
            )
            val_lbl.grid(row=1, column=1, padx=(0, 15), pady=(0, 12), sticky="w")
            
    def create_analysis_section(self):
        """Tạo khu vực Middle Section chia 2 cột: Cột trái (1/3), Cột phải (2/3)"""
        middle_container = customtkinter.CTkFrame(self, fg_color="transparent")
        middle_container.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        # Chia tỉ lệ cột 1:2 (tương đương 1/3 và 2/3)
        middle_container.grid_columnconfigure(0, weight=1, uniform="mid_cols")
        middle_container.grid_columnconfigure(1, weight=2, uniform="mid_cols")
        
        # --- CỘT TRÁI: Sự kiện trong tháng 7/2026 ---
        left_card = customtkinter.CTkFrame(
            middle_container,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#e2e8f0"
        )
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Tiêu đề cột trái
        left_title = customtkinter.CTkLabel(
            left_card,
            text="Sự kiện trong tháng 7/2026",
            font=(self.FONT_FAMILY, 15, "bold"),
            text_color="#0f172a"
        )
        left_title.pack(anchor="w", padx=15, pady=(15, 12))
        
        # Danh sách sự kiện giả lập
        events = [
            ("🎉", "Ngày gia đình", "29/5"),
            ("🏖️", "Kì nghỉ hè", "26/05"),
            ("🇻🇳", "Lễ Quốc Khánh", "1/5")
        ]
        
        events_frame = customtkinter.CTkFrame(left_card, fg_color="transparent")
        events_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        for icon, name, date in events:
            event_row = customtkinter.CTkFrame(events_frame, fg_color="transparent")
            event_row.pack(fill="x", pady=5)
            
            icon_lbl = customtkinter.CTkLabel(event_row, text=icon, font=(self.FONT_FAMILY, 14), width=24)
            icon_lbl.pack(side="left", padx=(0, 8))
            
            name_lbl = customtkinter.CTkLabel(event_row, text=name, font=(self.FONT_FAMILY, 13), text_color="#1e293b")
            name_lbl.pack(side="left")
            
            date_lbl = customtkinter.CTkLabel(event_row, text=f"({date})", font=(self.FONT_FAMILY, 12, "italic"), text_color="#64748b")
            date_lbl.pack(side="right")
            
        # Hộp ghi chú cuối khung
        note_box = customtkinter.CTkFrame(
            left_card,
            fg_color="#e0f2fe",  # Nền xanh nhạt
            corner_radius=8
        )
        note_box.pack(fill="x", padx=15, pady=(0, 15))
        
        note_title_lbl = customtkinter.CTkLabel(
            note_box,
            text="💡 Ghi chú",
            font=(self.FONT_FAMILY, 12, "bold"),
            text_color="#0369a1",
            anchor="w"
        )
        note_title_lbl.pack(fill="x", padx=12, pady=(8, 2))
        
        note_desc_lbl = customtkinter.CTkLabel(
            note_box,
            text="Các sự kiện và mức ảnh hưởng được ước tính tự động dựa trên phân tích dữ liệu lịch sử cùng kỳ các năm trước.",
            font=(self.FONT_FAMILY, 11),
            text_color="#0369a1",
            wraplength=220,
            justify="left",
            anchor="w"
        )
        note_desc_lbl.pack(fill="x", padx=12, pady=(0, 10))
        
        # --- CỘT PHẢI: Xu hướng tiêu thụ ---
        right_card = customtkinter.CTkFrame(
            middle_container,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#e2e8f0"
        )
        right_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Tiêu đề cột phải
        right_title = customtkinter.CTkLabel(
            right_card,
            text="Xu hướng tiêu thụ",
            font=(self.FONT_FAMILY, 15, "bold"),
            text_color="#0f172a"
        )
        right_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Vẽ biểu đồ Matplotlib và nhúng vào cột phải
        self.draw_trend_chart(right_card)
        
    def draw_trend_chart(self, parent):
        """Vẽ biểu đồ cột kết hợp đường biểu diễn xu hướng tiêu thụ."""
        # Tạo Figure
        fig, ax = plt.subplots(figsize=(7, 2.7), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')
        
        # Trục X và dữ liệu (Mẫu tổng hợp của thịt bò làm đại diện)
        months = ["Tháng 5/2026", "Tháng 6/2026", "Tháng 7/2026\n(Dự báo)"]
        consumption = [350, 420, 520.5]
        
        # Vẽ cột: Tháng 5 & 6 màu xanh dương, Tháng 7 màu xanh lá
        bar_colors = ["#3b82f6", "#3b82f6", "#10b981"]
        bars = ax.bar(months, consumption, color=bar_colors, width=0.4, label="Sản lượng")
        
        # Vẽ đường xu hướng màu đỏ
        ax.plot(months, consumption, color="#ef4444", marker="o", linewidth=2.5, label="Xu hướng")
        
        # Trang trí biểu đồ
        ax.set_ylim(0, 600)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#cbd5e1')
        ax.spines['bottom'].set_color('#cbd5e1')
        ax.tick_params(colors='#64748b', labelsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#cbd5e1')
        
        # Thêm text giá trị lên đầu cột
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height} kg',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # Đẩy text lên trên 3pt
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#1e293b')
            
        ax.legend(loc="upper left", frameon=False, prop={'family': self.FONT_FAMILY, 'size': 9})
        fig.tight_layout()
        
        # Nhúng vào tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        plt.close(fig)
        
    def create_table_section(self):
        """Tạo khu vực chứa bảng dữ liệu dự báo chi tiết và thanh công cụ."""
        table_container = customtkinter.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=10,
            border_width=1,
            border_color="#e2e8f0"
        )
        table_container.grid(row=4, column=0, sticky="nsew", pady=(0, 15))
        
        # --- 1. THANH CÔNG CỤ (TOOLBAR) ---
        toolbar = customtkinter.CTkFrame(table_container, fg_color="transparent")
        toolbar.pack(fill="x", padx=15, pady=15)
        
        title_tbl = customtkinter.CTkLabel(
            toolbar,
            text="Dự báo chi tiết nguyên liệu",
            font=(self.FONT_FAMILY, 15, "bold"),
            text_color="#0f172a"
        )
        title_tbl.pack(side="left")
        
        # Ô tìm kiếm bên phải
        self.search_entry = customtkinter.CTkEntry(
            toolbar,
            placeholder_text="Tìm tên nguyên liệu... 🔍",
            font=(self.FONT_FAMILY, 12),
            width=260,
            height=34,
            corner_radius=6,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8"
        )
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self.filter_table)
        
        # --- 2. BẢNG DỮ LIỆU (TTK.TREEVIEW) ---
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Prediction.Treeview",
            background="#ffffff",
            foreground="#1e293b",
            fieldbackground="#ffffff",
            rowheight=34,
            font=(self.FONT_FAMILY, 11),
            borderwidth=0
        )
        
        style.map(
            "Prediction.Treeview",
            background=[("selected", "#e0f2fe")],
            foreground=[("selected", "#0369a1")]
        )
        
        style.configure(
            "Prediction.Treeview.Heading",
            background="#f8fafc",
            foreground="#475569",
            font=(self.FONT_FAMILY, 11, "bold"),
            borderwidth=1,
            relief="flat"
        )
        
        # Khung chứa bảng và scrollbar
        table_frame = customtkinter.CTkFrame(table_container, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        columns = ("ma_nl", "ten_nl", "t5", "t6", "t7_forecast", "percent", "action")
        
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Prediction.Treeview"
        )
        
        # Thiết lập tag cho Zebra Row striping
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f8fafc")
        
        # Định nghĩa tiêu đề & độ rộng các cột
        headers = {
            "ma_nl": "Mã NL",
            "ten_nl": "Tên nguyên liệu",
            "t5": "Tháng 5/2026 (tiêu thụ)",
            "t6": "Tháng 6/2026 (tiêu thụ)",
            "t7_forecast": "Dự báo tháng 7/2026",
            "percent": "Tăng/Giảm",
            "action": "Thao tác"
        }
        
        for col, heading in headers.items():
            self.tree.heading(col, text=heading, anchor="center" if col in ["ma_nl", "percent", "action"] else "w")
            if col in ["t5", "t6", "t7_forecast"]:
                self.tree.column(col, anchor="e", width=160)
            elif col in ["ma_nl", "percent"]:
                self.tree.column(col, anchor="center", width=100)
            elif col == "action":
                self.tree.column(col, anchor="center", width=80)
            else:
                self.tree.column(col, anchor="w", width=220)
                
        # Nạp dữ liệu vào bảng
        self.populate_table()
        
        # Gắn scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Gắn sự kiện double click vào dòng
        self.tree.bind("<Double-1>", self.on_row_double_click)
        
    def populate_table(self, filter_text=""):
        """Nạp dữ liệu vào bảng dựa trên bộ lọc tìm kiếm."""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Lọc và nạp dữ liệu
        idx = 0
        for code, item in self.ingredients_data.items():
            if filter_text.lower() in item["ten"].lower() or filter_text.lower() in item["ma"].lower():
                row_tag = "evenrow" if idx % 2 == 0 else "oddrow"
                # Thao tác: 👁️ (Xem chi tiết)
                values = (item["ma"], item["ten"], item["t5"], item["t6"], item["t7_forecast"], item["percent"], "👁️")
                self.tree.insert("", "end", values=values, tags=(row_tag,))
                idx += 1
                
    def filter_table(self, event=None):
        """Xử lý sự kiện khi gõ vào ô tìm kiếm."""
        query = self.search_entry.get().strip()
        self.populate_table(query)
        
    def on_row_double_click(self, event):
        """Xử lý sự kiện bấm đúp chuột vào một hàng."""
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        values = self.tree.item(selected_item, "values")
        if not values:
            return
            
        code = values[0]  # Lấy Mã NL
        self.open_prediction_detail(code)
        
    def open_prediction_detail(self, code):
        """Mở Popup Chi Tiết Dự Báo dạng CTkToplevel."""
        if code not in self.ingredients_data:
            return
            
        data = self.ingredients_data[code]
        
        # Tạo cửa sổ Popup
        popup = customtkinter.CTkToplevel(self)
        popup.title(f"Chi tiết dự báo : {data['ten'].lower()} ({data['ma']})")
        
        popup_width = 500
        popup_height = 600
        
        # Căn giữa cửa sổ popup so với cửa sổ cha hoặc màn hình chính
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        try:
            parent_window = self.winfo_toplevel()
            parent_w = parent_window.winfo_width()
            parent_h = parent_window.winfo_height()
            parent_x = parent_window.winfo_x()
            parent_y = parent_window.winfo_y()
            x = parent_x + (parent_w - popup_width) // 2
            y = parent_y + (parent_h - popup_height) // 2
        except Exception:
            x = (screen_w - popup_width) // 2
            y = (screen_h - popup_height) // 2
            
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.resizable(False, False)
        popup.configure(fg_color="#f8fafc")
        
        # Khóa tương tác với cửa sổ chính khi popup mở
        popup.grab_set()
        
        # 1. Header (Tiêu đề Popup)
        header_frame = customtkinter.CTkFrame(popup, fg_color="#e0f2fe", height=60, corner_radius=0)
        header_frame.pack(fill="x", side="top")
        
        header_lbl = customtkinter.CTkLabel(
            header_frame,
            text=f"🔍 Chi Tiết Dự Báo {data['ten'].upper()}",
            font=(self.FONT_FAMILY, 16, "bold"),
            text_color="#0369a1"
        )
        header_lbl.pack(pady=18, padx=20, anchor="w")
        
        # 2. Main content container
        content_frame = customtkinter.CTkFrame(popup, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=25)
        
        # Tiêu đề mục phép tính
        calc_section_lbl = customtkinter.CTkLabel(
            content_frame,
            text="Cơ sở dữ liệu và các bước tính toán:",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#0f172a"
        )
        calc_section_lbl.pack(anchor="w", pady=(0, 15))
        
        # Helper vẽ dòng phép tính dạng dot leaders
        def create_calc_row(parent_frame, label_text, val_text):
            row = customtkinter.CTkFrame(parent_frame, fg_color="transparent")
            row.pack(fill="x", pady=6)
            
            lbl_left = customtkinter.CTkLabel(row, text=label_text, font=(self.FONT_FAMILY, 13), text_color="#475569")
            lbl_left.pack(side="left")
            
            lbl_right = customtkinter.CTkLabel(row, text=val_text, font=(self.FONT_FAMILY, 13, "bold"), text_color="#1e293b")
            lbl_right.pack(side="right")
            
            dots_lbl = customtkinter.CTkLabel(row, text=" " + "." * 70 + " ", font=(self.FONT_FAMILY, 12), text_color="#cbd5e1")
            dots_lbl.pack(side="left", fill="x", expand=True)
            
        # Nạp dữ liệu chi tiết phép tính
        avg_str = f"{data['avg']} kg"
        effect_str = f"+{int(data['holiday_effect'] * 100)}%"
        expected_str = f"{data['expected']} kg"
        margin_str = f"+{data['safety_stock']} kg"
        
        create_calc_row(content_frame, "Tiêu thụ tháng 5/2026", data["t5"])
        create_calc_row(content_frame, "Tiêu thụ tháng 6/2026", data["t6"])
        create_calc_row(content_frame, "Trung bình của 2 tháng", avg_str)
        create_calc_row(content_frame, "Ảnh hưởng của mùa du lịch", effect_str)
        create_calc_row(content_frame, f"Dự kiến sau 2 tháng ({data['avg']} x {1 + data['holiday_effect']})", expected_str)
        create_calc_row(content_frame, f"Dự đoán phòng tồn kho ({data['safety_stock']}kg)", margin_str)
        
        # Khoảng cách trước kết quả
        spacer = customtkinter.CTkFrame(content_frame, height=20, fg_color="transparent")
        spacer.pack()
        
        # 3. Khung Kết Quả đề xuất nhập
        result_frame = customtkinter.CTkFrame(
            content_frame,
            fg_color="#d4edda",  # Nền xanh lá nhạt
            corner_radius=8,
            border_width=1,
            border_color="#c3e6cb"
        )
        result_frame.pack(fill="x", pady=10)
        
        result_title = customtkinter.CTkLabel(
            result_frame,
            text="Kết quả đề xuất nhập",
            font=(self.FONT_FAMILY, 14, "bold"),
            text_color="#155724"  # Xanh lá đậm
        )
        result_title.pack(side="left", padx=15, pady=18)
        
        result_val = customtkinter.CTkLabel(
            result_frame,
            text=data["t7_forecast"],
            font=(self.FONT_FAMILY, 20, "bold"),
            text_color="#155724"
        )
        result_val.pack(side="right", padx=15, pady=18)
        
        # 4. Footer (Mô tả công thức & Nút đóng)
        footer_frame = customtkinter.CTkFrame(popup, fg_color="#ffffff", height=70, corner_radius=0, border_width=1, border_color="#cbd5e1")
        footer_frame.pack(fill="x", side="bottom")
        
        # Ghi chú công thức giải thích
        formula_lbl = customtkinter.CTkLabel(
            footer_frame,
            text="* Công thức: Dự kiến = (Trung bình 2 tháng x (1 + Ảnh hưởng mùa)) + Tồn kho dự phòng",
            font=(self.FONT_FAMILY, 10, "italic"),
            text_color="#64748b"
        )
        formula_lbl.pack(side="left", padx=15, pady=10)
        
        close_btn = customtkinter.CTkButton(
            footer_frame,
            text="Đóng",
            font=(self.FONT_FAMILY, 12, "bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="#ffffff",
            corner_radius=6,
            height=32,
            width=80,
            command=popup.destroy
        )
        close_btn.pack(side="right", padx=15, pady=10)


# Đoạn mã kiểm thử độc lập
if __name__ == "__main__":
    class StandaloneApp(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.title("Kiểm thử PredictionView")
            self.geometry("1100x650")
            self.configure(fg_color="#f5f6f8")
            
            # Frame chính bọc ngoài để mô phỏng content_area trong Dashboard
            container = customtkinter.CTkFrame(self, fg_color="transparent")
            container.pack(expand=True, fill="both", padx=20, pady=20)
            
            # Khởi tạo PredictionView
            view = PredictionView(container)
            view.pack(expand=True, fill="both")
            
    app = StandaloneApp()
    app.mainloop()
