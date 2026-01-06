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
            self.df = pd.read_excel(file_path) # Đọc Sheet 1
            # Lấy thêm cột Tieu_De
            self.tieu_de_map = self.df.set_index('So')['Tieu_De'].to_dict()
            self.data_map = self.df.set_index('So')['Loi_Khuyen'].to_dict()
            self.tu_khoa_map = self.df.set_index('So')['Tu_Khoa'].to_dict()
        except Exception:
            self.tieu_de_map = {} # Dự phòng nếu lỗi
            self.data_map = {}
            self.tu_khoa_map = {}

    def rut_gon(self, n, keep_master=True):
        while n > 9:
            if keep_master and n in [11, 22, 33]: break
            n = sum(int(digit) for digit in str(n))
        return n

    def lay_noi_dung(self, so):
        # Lấy Tiêu đề, Từ khóa, Lời khuyên (3 món)
        td = self.tieu_de_map.get(so, f"CON SỐ {so}") # Mặc định nếu chưa có Excel
        tk = self.tu_khoa_map.get(so, "")
        lk = self.data_map.get(so, "Chưa có dữ liệu cho số này.")
        return td, tk, lk 

    def tinh_con_so_chu_dao(self, ngay_sinh_str):
        numbers = [int(d) for d in ngay_sinh_str if d.isdigit()]
        so = self.rut_gon(sum(numbers))
        return so, self.lay_noi_dung(so)

    def tinh_chi_so_su_menh(self, ho_ten):
        alphabet_map = {
            'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2, 'C': 3, 'L': 3, 'U': 3,
            'D': 4, 'M': 4, 'V': 4, 'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
            'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8, 'I': 9, 'R': 9
        }
        ho_ten = ho_ten.upper()
        tong = sum(alphabet_map.get(char, 0) for char in ho_ten)
        so = self.rut_gon(tong)
        return so, self.lay_noi_dung(so)
    
    def tinh_nam_ca_nhan(self, ngay_sinh_str, nam_hien_tai=2026):
        clean_date = re.sub(r'[^0-9]', '', ngay_sinh_str)
        if len(clean_date) >= 4:
            ngay, thang = int(clean_date[:2]), int(clean_date[2:4])
            tong = self.rut_gon(ngay) + self.rut_gon(thang) + self.rut_gon(nam_hien_tai)
            so = self.rut_gon(tong, keep_master=False)
            return so, self.lay_noi_dung(so)
        return 0, ("", "", "") # Trả về 3 giá trị rỗng

# --- CLASS 2: TỬ VI (NÂNG CẤP ĐỌC EXCEL) ---
class TuVi:
    def __init__(self, file_path='data_thansohoc.xlsx'):
        self.can = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
        self.chi = ["Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi"]
        
        # --- ĐỌC DỮ LIỆU TỪ SHEET 'TuVi' ---
        try:
            # sheet_name='TuVi' là tên Sheet anh vừa tạo
            self.df_tuvi = pd.read_excel(file_path, sheet_name='TuVi')
            # Chuyển đổi thành Dictionary để tra cứu cho nhanh
            # Cấu trúc: {'Tý': {'Tong_Quan': '...', 'Su_Nghiep': '...'}, 'Sửu': ...}
            self.data_tuvi = self.df_tuvi.set_index('Con_Giap').T.to_dict()
        except Exception as e:
            # Nếu lỡ quên tạo sheet thì dùng data dự phòng này
            self.data_tuvi = {} 
            print(f"Lỗi đọc Sheet TuVi: {e}")

    def tinh_can_chi(self, nam_sinh):
        can = self.can[nam_sinh % 10]
        chi = self.chi[nam_sinh % 12]
        return can, chi

    def lay_luan_giai_tu_vi(self, chi):
        # Lấy thông tin từ Excel dựa vào Chi (Tý, Sửu...)
        data = self.data_tuvi.get(chi, None)
        if data:
            return data
        else:
            return {
                "Tong_Quan": "Chưa có dữ liệu chi tiết.",
                "Su_Nghiep": "Đang cập nhật...",
                "Tai_Loc": "Đang cập nhật...",
                "Tinh_Cam": "Đang cập nhật..."
            }

    def tinh_cung_hoang_dao(self, ngay, thang):
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
    # 1. Hiển thị ảnh (Bỏ tham số caption đi nha anh)
st.image(img_url, use_container_width=True)
    
    # 2. Tự chế Caption xịn bằng HTML
st.markdown(
        """
        <div style="text-align: center; margin-top: 10px;">
            <strong style="color: blue; font-size: 18px;">
                Xuân Bính Ngọ 2026 - Vạn Sự Như Ý
            </strong>
            </b>
            <br><br>
            <span style="color: #ff9f43; font-style: italic;">
                Cầu xin Thượng đế ban cho con sự tĩnh tại<br>
                để chấp nhận những nghịch cảnh bất biến,<br>
                dũng khí để xoay chuyển những điều trong tầm tay,<br>
                và tuệ giác để phân định rõ ranh giới giữa hai điều đó.
            </span>
        </div>
        """,
unsafe_allow_html=True
        )

st.markdown("<h1 style='text-align: center; color: #d63031;'>🔮 GIEO QUẺ ĐẦU NĂM 🔮</h1>", unsafe_allow_html=True)
st.write("---")

c1, c2 = st.columns(2)
with c1: ten_nhap = st.text_input("Họ Tên:", placeholder="VD: DoraeMon ...")
with c2: ngay_sinh_input = st.date_input("Ngày Sinh:", min_value=datetime(1950, 1, 1), format="DD/MM/YYYY")

if st.button("🧧 XEM LUẬN GIẢI NGAY 🧧", type="primary"):
    if not ten_nhap:
        st.warning("Vui lòng nhập tên!")
    else:
        ten_nhap = ten_nhap.upper()
        # Xử lý dữ liệu
        app_ts = ThanSoHoc()
        app_tv = TuVi()
        
        ns_str = ngay_sinh_input.strftime("%d%m%Y")
        ngay_hien_thi = ngay_sinh_input.strftime("%d/%m/%Y")
        nam_sinh = ngay_sinh_input.year
        ngay_sinh = ngay_sinh_input.day
        thang_sinh = ngay_sinh_input.month
        
        # Tính toán
        so_cd, (td_cd, tk_cd, lk_cd) = app_ts.tinh_con_so_chu_dao(ns_str)
        so_sm, (td_sm, tk_sm, lk_sm) = app_ts.tinh_chi_so_su_menh(ten_nhap)
        so_nam, (td_nam, tk_nam, lk_nam) = app_ts.tinh_nam_ca_nhan(ns_str, 2026)
        
        can, chi = app_tv.tinh_can_chi(nam_sinh)
        tuoi_am = 2026 - nam_sinh + 1
        cung_hd = app_tv.tinh_cung_hoang_dao(ngay_sinh, thang_sinh)
        
        # Lấy dữ liệu chi tiết từ Excel
        luan_giai_chi_tiet = app_tv.lay_luan_giai_tu_vi(chi)

        # Hiệu ứng
        rain(emoji="✨", font_size=34, falling_speed=5, animation_length=5)
        st.success(f"XIN CHÀO GIA CHỦ: **{ten_nhap}**  \n(Sinh ngày: {ngay_hien_thi})")

        # HIỂN THỊ 4 TAB
        t1, t2, t3, t4 = st.tabs(["🌟 Số Chủ Đạo", "💎 Sứ Mệnh", "📅 Năm 2026", "☯️ Tử Vi & Vận Hạn"])
        
        with t1:
            # Hiện cái Tiêu đề "SỐ 1 - NGƯỜI KHỞI XƯỚNG" to đùng lên màu đỏ
            st.markdown(f"<h3 style='color: #d63031; text-align: center;'>{td_cd}</h3>", unsafe_allow_html=True)
            
            c_so, c_loi = st.columns([1, 3])
            with c_so:
                st.metric("CHỈ SỐ", so_cd)
            with c_loi:
                st.info(f"**Từ khóa:** {tk_cd}")
                st.write(lk_cd)
            
        with t2:
            st.markdown(f"<h3 style='color: #0984e3; text-align: center;'>{td_sm}</h3>", unsafe_allow_html=True)
            
            c_so, c_loi = st.columns([1, 3])
            with c_so:
                st.metric("CHỈ SỐ", so_sm)
            with c_loi:
                st.info(f"**Từ khóa:** {tk_sm}")
                st.write(lk_sm)

        with t3:
            st.metric("NĂM CÁ NHÂN 2026", so_nam, delta="LỜI KHUYÊN CHO NĂM NAY")
            st.warning(f"**{td_nam}**") # Hiện tiêu đề năm cá nhân
            st.write(lk_nam)

        with t4:
            st.subheader(f"Tuổi Âm: {tuoi_am} tuổi - {can} {chi}")
            col_a, col_b = st.columns(2)
            with col_a: st.metric("Con Giáp", f"Tuổi {chi}")
            with col_b: st.metric("Cung Hoàng Đạo", cung_hd)
            
            st.write("---")
            st.markdown(f"#### 📜 Vận hạn năm Bính Ngọ 2026 cho tuổi {chi}:")
            
            # --- PHẦN HIỂN THỊ CHI TIẾT CHUYÊN NGHIỆP ---
            with st.expander("🚩 TỔNG QUAN NĂM 2026 (Bấm để xem)", expanded=True):
                st.write(luan_giai_chi_tiet['Tong_Quan'])
            
            c_job, c_money = st.columns(2)
            with c_job:
                st.info("💼 **SỰ NGHIỆP**")
                st.caption(luan_giai_chi_tiet['Su_Nghiep'])
            with c_money:
                st.success("💰 **TÀI LỘC**")
                st.caption(luan_giai_chi_tiet['Tai_Loc'])
                
            st.warning(f"❤️ **TÌNH CẢM & GIA ĐẠO**: {luan_giai_chi_tiet['Tinh_Cam']}")
            # -----------------------------------------------

st.write("---")
st.caption("KÍNH CHÚC NĂM MỚI AN KHANG, THỊNH VƯỢNG - KID-CUI")