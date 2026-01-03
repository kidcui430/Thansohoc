import streamlit as st
import pandas as pd
import re
from datetime import datetime
from streamlit_extras.let_it_rain import rain

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Gieo Quẻ Đầu Năm 2026", page_icon="🌸", layout="centered")

# --- CLASS 1: THẦN SỐ HỌC (GIỮ NGUYÊN) ---
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
            if keep_master and n in [11, 22, 33]: break
            n = sum(int(digit) for digit in str(n))
        return n

    def lay_noi_dung(self, so):
        tk = self.tu_khoa_map.get(so, "")
        lk = self.data_map.get(so, "Chưa có dữ liệu cho số này.")
        return tk, lk

    def tinh_con_so_chu_dao(self, ngay_sinh_str):
        numbers = [int(d) for d in ngay_sinh_str if d.isdigit()]
        so = self.rut_gon(sum(numbers))
        return so, self.lay_noi_dung(so)

    def tinh_chi_so_su_menh(self, ho_ten):
        ho_ten = ho_ten.upper()
        tong = sum(self.alphabet_map.get(char, 0) for char in ho_ten)
        so = self.rut_gon(tong)
        return so, self.lay_noi_dung(so)
    
    def tinh_nam_ca_nhan(self, ngay_sinh_str, nam_hien_tai=2026):
        clean_date = re.sub(r'[^0-9]', '', ngay_sinh_str)
        if len(clean_date) >= 4:
            ngay, thang = int(clean_date[:2]), int(clean_date[2:4])
            tong = self.rut_gon(ngay) + self.rut_gon(thang) + self.rut_gon(nam_hien_tai)
            so = self.rut_gon(tong, keep_master=False)
            return so, self.lay_noi_dung(so)
        return 0, ("", "")

# --- CLASS 2: TỬ VI & PHƯƠNG ĐÔNG (MỚI THÊM) ---
class TuVi:
    def __init__(self):
        self.can = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
        self.chi = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
        # Data vận hạn năm 2026 (Bính Ngọ) cho 12 con giáp
        self.van_han_2026 = {
            "Tý": "⚠️ Xung Thái Tuế: Năm nay có nhiều biến động, cần cẩn trọng trong đi lại và giao tiếp. Tránh đầu tư mạo hiểm.",
            "Sửu": "⚠️ Hại Thái Tuế: Dễ gặp chuyện thị phi, tiểu nhân quấy phá. Nên giữ mình, làm việc chắc chắn.",
            "Dần": "✨ Tam Hợp (Dần - Ngọ - Tuất): Năm rất tốt để triển khai dự án lớn. Quý nhân phù trợ, công việc hanh thông.",
            "Mão": "💥 Phá Thái Tuế: Cẩn thận rắc rối về giấy tờ, tình cảm gia đạo cần vun vén nhiều hơn.",
            "Thìn": "🌤️ Bình Hòa: Mọi việc ở mức trung bình. Cần nỗ lực tự thân, không nên trông chờ may mắn.",
            "Tỵ": "🔥 Năm bản lề: Có cơ hội thăng tiến nhưng cũng nhiều áp lực. Sức khỏe cần chú ý.",
            "Ngọ": "⭐ Năm Tuổi (Trực Thái Tuế): Áp lực nhiều nhưng là cơ hội bứt phá ('Lửa thử vàng'). Cần kiên nhẫn.",
            "Mùi": "❤️ Nhị Hợp: Rất tốt cho chuyện tình cảm và hợp tác làm ăn. Có tin vui đưa tới.",
            "Thân": "🌤️ Bình Ổn: Tài lộc khá, công việc tiến triển đều. Nên học thêm kỹ năng mới.",
            "Dậu": "💓 Đào Hoa: Nhân duyên tốt, người độc thân dễ gặp ý trung nhân. Tài chính khởi sắc.",
            "Tuất": "✨ Tam Hợp: Thiên thời địa lợi. Năm cực tốt để mua nhà, tậu xe hoặc thăng chức.",
            "Hợi": "🌊 Bình Hòa: Cần quản lý tài chính chặt chẽ. Tránh cho vay mượn lung tung."
        }

    def tinh_can_chi(self, nam_sinh):
        """Tính Can Chi từ năm dương lịch"""
        can = self.can[nam_sinh % 10]
        chi = self.chi[nam_sinh % 12]
        return can, chi

    def tinh_cung_hoang_dao(self, ngay, thang):
        """Tính cung hoàng đạo phương Tây"""
        if (thang == 3 and ngay >= 21) or (thang == 4 and ngay <= 19): return "Bạch Dương ♈"
        if (thang == 4 and ngay >= 20) or (thang == 5 and ngay <= 20): return "Kim Ngưu ♉"
        if (thang == 5 and ngay >= 21) or (thang == 6 and ngay <= 21): return "Song Tử ♊"
        if (thang == 6 and ngay >= 22) or (thang == 7 and ngay <= 22): return "Cự Giải ♋"
        if (thang == 7 and ngay >= 23) or (thang == 8 and ngay <= 22): return "Sư Tử ♌"
        if (thang == 8 and ngay >= 23) or (thang == 9 and ngay <= 22): return "Xử Nữ ♍"
        if (thang == 9 and ngay >= 23) or (thang == 10 and ngay <= 23): return "Thiên Bình ♎"
        if (thang == 10 and ngay >= 24) or (thang == 11 and ngay <= 21): return "Bọ Cạp ♏"
        if (thang == 11 and ngay >= 22) or (thang == 12 and ngay <= 21): return "Nhân Mã ♐"
        if (thang == 12 and ngay >= 22) or (thang == 1 and ngay <= 19): return "Ma Kết ♑"
        if (thang == 1 and ngay >= 20) or (thang == 2 and ngay <= 18): return "Bảo Bình ♒"
        return "Song Ngư ♓"

# --- GIAO DIỆN CHÍNH ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    img_url = "https://i.pinimg.com/1200x/8a/95/b4/8a95b4423db111f3d5ec61466d459418.jpg"
    st.image(img_url, caption="Xuân Bính Ngọ 2026 - Vạn Sự Như Ý", use_container_width=True)

st.markdown("<h1 style='text-align: center; color: #d63031;'>🔮 GIEO QUẺ ĐẦU NĂM 🔮</h1>", unsafe_allow_html=True)
st.write("---")

c1, c2 = st.columns(2)
with c1: ten_nhap = st.text_input("Họ Tên:", placeholder="VD: KID TRIẾT VŨ")
with c2: ngay_sinh_input = st.date_input("Ngày Sinh:", min_value=datetime(1950, 1, 1))

if st.button("🧧 XEM LUẬN GIẢI NGAY 🧧", type="primary"):
    if not ten_nhap:
        st.warning("Vui lòng nhập tên!")
    else:
        ten_nhap = ten_nhap.upper()
        # Xử lý dữ liệu
        app_ts = ThanSoHoc()
        app_tv = TuVi() # Gọi thêm class Tử Vi
        
        ns_str = ngay_sinh_input.strftime("%d%m%Y")
        ngay_hien_thi = ngay_sinh_input.strftime("%d/%m/%Y")
        nam_sinh = ngay_sinh_input.year
        ngay_sinh = ngay_sinh_input.day
        thang_sinh = ngay_sinh_input.month
        
        # 1. Tính Thần số học
        so_cd, (tk_cd, lk_cd) = app_ts.tinh_con_so_chu_dao(ns_str)
        so_sm, (tk_sm, lk_sm) = app_ts.tinh_chi_so_su_menh(ten_nhap)
        so_nam, (tk_nam, lk_nam) = app_ts.tinh_nam_ca_nhan(ns_str, 2026)
        
        # 2. Tính Tử vi
        can, chi = app_tv.tinh_can_chi(nam_sinh)
        tuoi_am = 2026 - nam_sinh + 1
        cung_hd = app_tv.tinh_cung_hoang_dao(ngay_sinh, thang_sinh)
        loi_khuyen_2026 = app_tv.van_han_2026.get(chi, "Bình thường")

        # Hiệu ứng
        rain(emoji="💸", font_size=35, falling_speed=5, animation_length="infinite")
        st.success(f"XIN CHÀO GIA CHỦ : **{ten_nhap}**  \n(Sinh ngày: {ngay_hien_thi})")

        # HIỂN THỊ 4 TAB
        t1, t2, t3, t4 = st.tabs(["🌟 Số Chủ Đạo", "💎 Sứ Mệnh", "📅 Năm 2026", "☯️ Tử Vi & Vận Hạn"])
        
        with t1:
            st.metric("CON SỐ CHỦ ĐẠO", so_cd)
            st.info(f"**{tk_cd}**")
            st.write(lk_cd)
            
        with t2:
            st.metric("CHỈ SỐ SỨ MỆNH", so_sm)
            st.info(f"**{tk_sm}**")
            st.write(lk_sm)

        with t3:
            st.metric(f"NĂM CÁ NHÂN {so_nam}", "Dự báo Thần số học")
            st.warning("Lời khuyên năm nay:")
            st.write(lk_nam)

        with t4: # Tab mới của anh đây
            st.subheader(f"Tuổi Âm: {tuoi_am} tuổi - {can} {chi}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Con Giáp", f"Tuổi {chi}")
            with col_b:
                st.metric("Cung Hoàng Đạo", cung_hd)
            
            st.write("---")
            st.markdown(f"#### 📜 Vận hạn năm Bính Ngọ 2026 cho tuổi {chi}:")
            st.info(loi_khuyen_2026)
            st.caption("*Lưu ý: Tuổi âm tính theo năm Dương lịch nhập vào (chưa xét tháng sinh âm lịch chi tiết).*")

st.write("---")
st.caption("KID. TRIẾT VŨ - Chúc mừng năm mới Xuân Bính Ngọ 2026")