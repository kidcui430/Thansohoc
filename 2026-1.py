import streamlit as st
import pandas as pd
import textwrap
import re
from datetime import datetime

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Gieo Quẻ Đầu Năm 2026",
    page_icon="🌸",
    layout="centered"
)

# --- CLASS XỬ LÝ LOGIC (GIỮ NGUYÊN) ---
class ThanSoHoc:
    def __init__(self, file_path='data_thansohoc.xlsx'):
        try:
            self.df = pd.read_excel(file_path)
            self.data_map = self.df.set_index('So')['Loi_Khuyen'].to_dict()
            self.tu_khoa_map = self.df.set_index('So')['Tu_Khoa'].to_dict()
        except Exception:
            self.data_map = {}
            self.tu_khoa_map = {}

        self.alphabet_map = {
            'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2,
            'C': 3, 'L': 3, 'U': 3, 'D': 4, 'M': 4, 'V': 4,
            'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
            'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8,
            'I': 9, 'R': 9
        }

    def rut_gon(self, n, keep_master=True):
        while n > 9:
            if keep_master and n in [11, 22, 33]:
                break
            n = sum(int(digit) for digit in str(n))
        return n

    def lay_noi_dung(self, so):
        tu_khoa = self.tu_khoa_map.get(so, "")
        loi_khuyen = self.data_map.get(so, "Chưa có dữ liệu cho số này trong Excel.")
        # Streamlit tự ngắt dòng nên không cần textwrap ở đây cũng được
        return tu_khoa, loi_khuyen

    def tinh_con_so_chu_dao(self, ngay_sinh_str):
        # Đầu vào ngay_sinh_str dạng "ddmmyyyy"
        numbers = [int(d) for d in ngay_sinh_str if d.isdigit()]
        tong = sum(numbers)
        so = self.rut_gon(tong)
        return so, self.lay_noi_dung(so)

    def tinh_chi_so_su_menh(self, ho_ten):
        ho_ten = ho_ten.upper()
        tong = 0
        for char in ho_ten:
            if char in self.alphabet_map:
                tong += self.alphabet_map[char]
        so = self.rut_gon(tong)
        return so, self.lay_noi_dung(so)
    
    def tinh_nam_ca_nhan(self, ngay_sinh_str, nam_hien_tai=2026):
        clean_date = re.sub(r'[^0-9]', '', ngay_sinh_str)
        if len(clean_date) >= 4:
            ngay = int(clean_date[:2])
            thang = int(clean_date[2:4])
            tong = self.rut_gon(ngay) + self.rut_gon(thang) + self.rut_gon(nam_hien_tai)
            so = self.rut_gon(tong, keep_master=False)
            # Lưu ý: Năm cá nhân dùng bộ dữ liệu riêng hoặc dùng chung tuỳ anh
            # Ở đây em tạm dùng chung bộ data để demo
            return so, self.lay_noi_dung(so)
        return 0, ("", "Ngày sinh không hợp lệ")

# --- GIAO DIỆN STREAMLIT (PHẦN MỚI) ---

# 1. Ảnh bìa & Tiêu đề
# --- SỬA LẠI PHẦN HIỂN THỊ ẢNH ---

# Tạo bố cục 3 cột: Cột giữa rộng gấp đôi (số 2) để chứa ảnh, 2 cột bên cạnh để trống làm lề
col1, col2, col3 = st.columns([1, 2, 1])

with col2: # Chỉ làm việc với cột giữa
    # --- LỰA CHỌN ẢNH ĐẸP (Anh thích cái nào thì bỏ dấu # ở đầu dòng đó) ---
    
    # Lựa chọn 1: Cành mai vàng chụp cận cảnh, xóa phông (Rất nghệ thuật)
   img_url = "https://i.pinimg.com/1200x/8a/95/b4/8a95b4423db111f3d5ec61466d459418.jpg"
    
    # Lựa chọn 2: Không khí Tết ấm cúng với trà và hoa (Nhìn rất Chill)
    # img_url = "https://images.unsplash.com/photo-1643124915187-7450d741700c?q=80&w=1000&auto=format&fit=crop"
    
    # Lựa chọn 3: Hoa đào hồng tươi (Nếu anh thích màu hồng)
    # img_url = "https://images.unsplash.com/photo-1549887551-b156a99c0a81?q=80&w=1000&auto=format&fit=crop"

    # Hiển thị ảnh trong cột giữa
    st.image(img_url, caption="Chào Xuân Bính Ngọ 2026", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #d63031;'>🔮 GIEO QUẺ THẦN SỐ HỌC 🔮</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Khu vực nhập liệu
col1, col2 = st.columns(2)

with col1:
    ten_nhap = st.text_input("Nhập Họ và Tên của bạn:", placeholder="Ví dụ: Kid - cùi")

with col2:
    ngay_sinh_input = st.date_input("Chọn Ngày Sinh:", min_value=datetime(1950, 1, 1))

# Nút bấm xem kết quả
if st.button("🧧 XEM LUẬN GIẢI NGAY 🧧", type="primary"):
    if not ten_nhap:
        st.warning("Vui lòng nhập tên của bạn!")
    else:
        ten_nhap = ten_nhap.upper()
        # Khởi tạo Class
        app = ThanSoHoc()
        
        # Chuyển đổi ngày sinh từ lịch sang chuỗi "ddmmyyyy" để tính toán
        ngay_sinh_str = ngay_sinh_input.strftime("%d%m%Y")
        ngay_hien_thi = ngay_sinh_input.strftime("%d/%m/%Y")
        
        # Tính toán
        so_chu_dao, (tk_cd, lk_cd) = app.tinh_con_so_chu_dao(ngay_sinh_str)
        so_su_menh, (tk_sm, lk_sm) = app.tinh_chi_so_su_menh(ten_nhap)
        so_nam, (tk_nam, lk_nam) = app.tinh_nam_ca_nhan(ngay_sinh_str, 2026)

        # Hiển thị kết quả đẹp mắt
        st.balloons() # Hiệu ứng bóng bay chúc mừng
        
        st.success(f"Chào bạn **{ten_nhap.upper()}** (Sinh ngày: {ngay_hien_thi})")
        
        # Tab chia nội dung cho gọn
        tab1, tab2, tab3 = st.tabs(["🌟 Số Chủ Đạo", "💎 Sứ Mệnh", "📅 Năm 2026"])
        
        with tab1:
            st.metric(label="CON SỐ CHỦ ĐẠO", value=so_chu_dao)
            st.info(f"**Từ khóa:** {tk_cd}")
            st.write(lk_cd)
            
        with tab2:
            st.metric(label="CHỈ SỐ SỨ MỆNH", value=so_su_menh)
            st.info(f"**Từ khóa:** {tk_sm}")
            st.write(lk_sm)

        with tab3:
            st.metric(label="NĂM CÁ NHÂN 2026", value=so_nam)
            st.warning("Dự báo vận hạn năm nay:")
            # Lưu ý: Phần lời khuyên này đang lấy từ data chung, 
            # anh nhớ cập nhật Excel phần năm cá nhân nếu muốn riêng biệt nhé
            st.write(lk_nam) 

st.write("---")

st.caption("KID. TRIẾT VŨ - Chúc mừng năm mới Xuân Bính Ngọ 2026")
