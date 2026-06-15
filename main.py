import os
from PIL import Image, ImageTk, ImageEnhance
import customtkinter
from tkinter import messagebox

import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Thiết lập chế độ giao diện sáng để giữ tông màu sáng-tối tương phản chuẩn phong cách Web
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

class WarehouseLoginApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # 1. Cấu hình cửa sổ chính
        self.title("Hệ thống Quản lý & Dự đoán Kho hàng - Đăng Nhập")
        self.width = 1000
        self.height = 600
        self.resizable(False, False)  # Cố định kích thước để đảm bảo tỷ lệ hoàn hảo
        
        # Căn giữa cửa sổ trên màn hình
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Cấu hình grid chính chia cửa sổ thành 2 phần: Trái (60%) và Phải (40%)
        self.grid_columnconfigure(0, weight=6)  # Left side (60%)
        self.grid_columnconfigure(1, weight=4)  # Right side (40%)
        self.grid_rowconfigure(0, weight=1)

        # 2. PHẦN BÊN TRÁI: Panel tối màu giới thiệu phần mềm
        self.setup_left_panel()

        # 3. PHẦN BÊN PHẢI: Panel sáng chứa Form đăng nhập
        self.setup_right_panel()

    def setup_left_panel(self):
        # Frame chính bên trái
        left_frame = customtkinter.CTkFrame(self, fg_color="transparent", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # 1. Đường dẫn ảnh tuyệt đối
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bg_image_path = os.path.join(current_dir, "assets", "background_sign-up.png")

        # 2. Đọc ảnh bằng PIL, làm tối vừa phải (độ sáng 0.4)
        bg_image_pil = Image.open(bg_image_path)
        bg_image_pil = bg_image_pil.resize((600, 600), Image.Resampling.LANCZOS)
        enhancer = ImageEnhance.Brightness(bg_image_pil)
        bg_image_pil = enhancer.enhance(0.4)

        # 3. Đưa vào 1 CTkLabel duy nhất phủ kín cột trái
        bg_image = customtkinter.CTkImage(light_image=bg_image_pil, dark_image=bg_image_pil, size=(600, 600))
        bg_label = customtkinter.CTkLabel(left_frame, image=bg_image, text="", fg_color="transparent")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 4. Gom toàn bộ text vào 1 content_frame đè lên bg_label
        content_frame = customtkinter.CTkFrame(bg_label, fg_color="transparent", corner_radius=0)
        content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # ── Header nhỏ ──
        category_label = customtkinter.CTkLabel(
            content_frame,
            text="AI-POWERED INVENTORY SYSTEM",
            font=("Segoe UI", 11, "normal"),
            text_color="#e0f2fe",
            fg_color="transparent"
        )
        category_label.pack(side="top", anchor="w", padx=50, pady=(60, 8))

        # ── Tiêu đề chính ──
        main_title = customtkinter.CTkLabel(
            content_frame,
            text="Quản lý Kho hàng và dự đoán lượng hàng cần nhập cho các tháng",
            font=("Segoe UI", 28, "bold"),
            text_color="white",
            wraplength=450,
            justify="left",
            anchor="w",
            fg_color="transparent"
        )
        main_title.pack(side="top", anchor="w", padx=50, pady=(0, 15))

        # ── Dòng mô tả nhỏ ──
        desc_label = customtkinter.CTkLabel(
            content_frame,
            text="Tối ưu hóa chuỗi cung ứng, tự động hóa quy trình quản lý kho hàng và ứng dụng mô hình AI dự báo xu hướng tiêu thụ sản phẩm.",
            font=("Segoe UI", 13, "normal"),
            text_color="white",
            wraplength=450,
            justify="left",
            anchor="w",
            fg_color="transparent"
        )
        desc_label.pack(side="top", anchor="w", padx=50, pady=(0, 40))

        # ── Danh sách 4 tính năng (emoji) ──
        features = [
            "📦 Quản lý xuất nhập kho tự động",
            "🤖 Dự đoán nhu cầu thị trường bằng AI",
            "📊 Báo cáo trực quan & Cảnh báo",
            "🔔 Tự động gửi cảnh báo tồn kho"
        ]

        feature_labels = []
        for feature_text in features:
            fl = customtkinter.CTkLabel(
                content_frame,
                text=feature_text,
                font=("Segoe UI", 13, "normal"),
                text_color="white",
                anchor="w",
                fg_color="transparent"
            )
            fl.pack(side="top", anchor="w", padx=50, pady=(0, 18))
            feature_labels.append(fl)

        # ── Footer bản quyền ──
        footer_label = customtkinter.CTkLabel(
            content_frame,
            text="© 2026 SmartWarehouse Inc. All rights reserved.",
            font=("Segoe UI", 10, "normal"),
            text_color="#94a3b8",
            fg_color="transparent"
        )
        footer_label.pack(side="bottom", anchor="w", padx=50, pady=(0, 60))

        # Áp dụng pywinstyles tạo độ trong suốt sắc nét trên Windows
        try:
            import pywinstyles
            self.update()
            
            # Sử dụng key color là "#fffffe" (gần như trắng) làm màu nền cho content_frame.
            # Tất cả các nhãn (labels) bên trong có fg_color="transparent", do đó chúng sẽ tự động thừa kế 
            # màu nền "#fffffe" này. Khi áp dụng set_opacity cho content_frame với màu key này, 
            # Windows sẽ khử toàn bộ màu nền của cả khung và các nhãn chữ con cùng lúc, 
            # giữ lại phần text sắc nét nguyên bản mà không bị vẽ chồng lấn/rỗ chữ.
            key_color = "#fffffe"
            content_frame.configure(fg_color=key_color)
            
            self.update()
            
            # Chỉ áp dụng set_opacity duy nhất một lần cho content_frame. 
            # Tuyệt đối không gọi cho từng label con để tránh tạo ra nhiều lớp cửa sổ lồng nhau gây nhòe và lặp nét chữ.
            pywinstyles.set_opacity(content_frame, color=key_color)
        except Exception:
            pass



    def setup_right_panel(self):
        # Panel bên phải có màu nền xám nhạt (#f1f5f9) để làm nổi bật Card màu trắng
        right_frame = customtkinter.CTkFrame(self, fg_color="#f1f5f9", corner_radius=0)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Card chứa Form Đăng nhập màu trắng bo góc cực đẹp đặt ở chính giữa
        card_frame = customtkinter.CTkFrame(
            right_frame, 
            width=360,
            height=480,
            fg_color="#ffffff", 
            corner_radius=20,
            border_width=1,
            border_color="#e2e8f0"
        )
        # Sử dụng place để căn giữa tuyệt đối
        card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo/Icon Đăng nhập
        logo_label = customtkinter.CTkLabel(
            card_frame,
            text="🔑",
            font=("Segoe UI", 36),
            width=60,
            height=60,
            fg_color="#eff6ff",
            text_color="#3b82f6",
            corner_radius=30
        )
        logo_label.pack(pady=(35, 10))

        # Tiêu đề Form
        title_label = customtkinter.CTkLabel(
            card_frame,
            text="Đăng Nhập",
            font=("Segoe UI", 24, "bold"),
            text_color="#0f172a"
        )
        title_label.pack(pady=(0, 2))

        subtitle_label = customtkinter.CTkLabel(
            card_frame,
            text="Vui lòng nhập thông tin tài khoản",
            font=("Segoe UI", 12),
            text_color="#64748b"
        )
        subtitle_label.pack(pady=(0, 25))

        # --- Ô Nhập Username ---
        username_label = customtkinter.CTkLabel(
            card_frame,
            text="Tên đăng nhập",
            font=("Segoe UI", 12, "bold"),
            text_color="#475569"
        )
        username_label.pack(anchor="w", padx=30, pady=(0, 4))

        self.username_entry = customtkinter.CTkEntry(
            card_frame,
            placeholder_text="Nhập email hoặc username",
            height=38,
            corner_radius=8,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8",
            font=("Segoe UI", 12)
        )
        self.username_entry.pack(fill="x", padx=30, pady=(0, 15))

        # --- Ô Nhập Password ---
        password_label = customtkinter.CTkLabel(
            card_frame,
            text="Mật khẩu",
            font=("Segoe UI", 12, "bold"),
            text_color="#475569"
        )
        password_label.pack(anchor="w", padx=30, pady=(0, 4))

        # Container cho mật khẩu và nút ẩn/hiện mật khẩu
        pass_container = customtkinter.CTkFrame(card_frame, fg_color="transparent")
        pass_container.pack(fill="x", padx=30, pady=(0, 12))

        self.password_entry = customtkinter.CTkEntry(
            pass_container,
            placeholder_text="Nhập mật khẩu",
            show="*",
            height=38,
            corner_radius=8,
            fg_color="#f8fafc",
            border_color="#cbd5e1",
            text_color="#0f172a",
            placeholder_text_color="#94a3b8",
            font=("Segoe UI", 12)
        )
        self.password_entry.pack(side="left", fill="x", expand=True)

        # Nút chuyển đổi ẩn hiện mật khẩu dạng Hiện/Ẩn cực kỳ rõ ràng
        self.show_password_btn = customtkinter.CTkButton(
            pass_container,
            text="Hiện",
            width=50,
            height=38,
            fg_color="#f1f5f9",
            hover_color="#e2e8f0",
            text_color="#475569",
            corner_radius=8,
            font=("Segoe UI", 11, "bold"),
            command=self.toggle_password_visibility
        )
        self.show_password_btn.pack(side="right", padx=(8, 0))

        # --- Checkbox Ghi nhớ mật khẩu ---
        self.remember_var = customtkinter.StringVar(value="off")
        self.remember_checkbox = customtkinter.CTkCheckBox(
            card_frame,
            text="Ghi nhớ đăng nhập",
            variable=self.remember_var,
            onvalue="on",
            offvalue="off",
            font=("Segoe UI", 12),
            text_color="#475569",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=5,
            border_width=2
        )
        self.remember_checkbox.pack(anchor="w", padx=30, pady=(0, 20))

        # --- Nút Đăng Nhập màu xanh lam ---
        self.login_btn = customtkinter.CTkButton(
            card_frame,
            text="Đăng Nhập",
            height=40,
            corner_radius=8,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 13, "bold"),
            text_color="#ffffff",
            command=self.handle_login
        )
        self.login_btn.pack(fill="x", padx=30, pady=(0, 15))

        # Liên kết hỗ trợ hoặc quên mật khẩu
        help_label = customtkinter.CTkLabel(
            card_frame,
            text="Quên mật khẩu?",
            font=("Segoe UI", 11, "bold"),
            text_color="#3b82f6",
            cursor="hand2"
        )
        help_label.pack(pady=(0, 15))
        help_label.bind("<Button-1>", lambda e: messagebox.showinfo("Khôi phục mật khẩu", "Vui lòng liên hệ với Quản trị viên hệ thống để khôi phục mật khẩu của bạn."))

    def toggle_password_visibility(self):
        # Chuyển đổi trạng thái hiển thị mật khẩu
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.show_password_btn.configure(text="Ẩn")
        else:
            self.password_entry.configure(show="*")
            self.show_password_btn.configure(text="Hiện")

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        remember = self.remember_var.get()

        # Kiểm tra trường thông tin trống
        if not username or not password:
            messagebox.showerror(
                "Lỗi nhập liệu", 
                "Vui lòng điền đầy đủ tên đăng nhập và mật khẩu!"
            )
            return

        # Giả lập xác thực người dùng (tài khoản demo: admin / admin123)
        if username == "admin" and password == "admin123":
            remember_status = "Đã bật" if remember == "on" else "Không bật"
            messagebox.showinfo(
                "Đăng nhập thành công",
                f"Chào mừng {username} trở lại hệ thống!\n"
                f"Trạng thái ghi nhớ đăng nhập: {remember_status}."
            )
        else:
            messagebox.showerror(
                "Đăng nhập thất bại",
                "Tên đăng nhập hoặc mật khẩu không chính xác.\n"
                "Mẹo: Hãy thử tài khoản: admin / mật khẩu: admin123"
            )

if __name__ == "__main__":
    app = WarehouseLoginApp()
    app.mainloop()
