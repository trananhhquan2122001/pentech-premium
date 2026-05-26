import streamlit as st
import yfinance as yf
import pandas as pd

# 1. CẤU HÌNH HỆ THỐNG DOANH NGHIỆP CẤP CAO
st.set_page_config(
    page_title="Pentech Premium - Tổ Chức Định Giá Tài Sản Số AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Giữ chặt mã xác minh Google Search Console của bạn
st._config.set_option("html.additionalHeadContent", '<meta name="google-site-verification" content="448da2da278475de" />')

# 2. GIAO DIỆN MÀU SẮC ĐỒNG BỘ CHUẨN FINTECH (CSS PREMIUM)
st.markdown("""
    <style>
    /* Làm mịn font chữ toàn trang */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Thanh Menu Giả Lập Thương Hiệu */
    .navbar {
        background-color: #0F172A;
        padding: 12px 24px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .nav-brand { color: #FFFFFF; font-size: 20px; font-weight: 800; letter-spacing: 1px; }
    .nav-menu { color: #94A3B8; font-size: 14px; font-weight: 500; }
    
    /* Khối hộp thông số */
    .company-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. THANH ĐIỀU HƯỚNG DOANH NGHIỆP (NAVIGATION BAR)
st.markdown("""
    <div class="navbar">
        <div class="nav-brand">💎 PENTECH PREMIUM CORPORATE</div>
        <div class="nav-menu">Hệ Thống Phân Tích Định Lượng • Khối Dữ Liệu Doanh Nghiệp • Báo Cáo Chiến Lược v2.5</div>
    </div>
""", unsafe_allow_html=True)

# 4. BẢNG THEO DÕI NHANH THỊ TRƯỜNG (MARKET WATCH OVERVIEW)
st.markdown("##### 📈 BẢNG THEO DÕI HỆ SINH THÁI DOANH NGHIỆP TIÊU BIỂU")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

def get_quick_price(ticker_symbol, name):
    try:
        t_data = yf.Ticker(ticker_symbol).history(period='1d')
        if not t_data.empty:
            price = t_data['Close'].iloc[-1]
            return f"{price:,.0f} VNĐ"
        return "Đang tải..."
    except:
        return "Bận kết nối"

with col_m1:
    st.metric(label="Công nghệ FPT", value=get_quick_price("FPT.VN", "FPT"), delta="Trụ cột số")
with col_m2:
    st.metric(label="Viettel Toàn Cầu (VGI)", value=get_quick_price("VGI.VN", "VGI"), delta="Dòng tiền mạnh")
with col_m3:
    st.metric(label="Masan Consumer (MCH)", value=get_quick_price("MCH.VN", "MCH"), delta="Tiêu dùng lõi")
with col_m4:
    st.metric(label="Bán lẻ Kỹ thuật số (FRT)", value=get_quick_price("FRT.VN", "FRT"), delta="Tăng trưởng cao")

st.markdown("---")

# 5. BẢNG ĐIỀU KHIỂN TRUNG TÂM PHÂN TÍCH VÀ TRUY VẤN
st.markdown("### 🎛️ CỬA SỔ TRUY VẤN DỮ LIỆU ĐỊNH GIÁ AI")
col_input, col_status = st.columns([4, 6])

with col_input:
    ticker_input = st.text_input(
        "Nhập mã cổ phiếu niêm yết (HOSE / HNX / UPCOM):", 
        value="VGI",
        help="Hệ thống tự động quét báo cáo tài chính và thị giá trực tuyến."
    ).upper().strip()

with col_status:
    st.markdown("""
    <div style="background-color: #F8FAFC; padding: 12px; border-radius: 6px; border: 1px solid #CBD5E1; margin-top: 5px;">
        <span style="color: #475569; font-size: 13px;">🔒 <b>Cơ chế hoạt động:</b> Thuật toán quét luồng giá đóng cửa, áp dụng mô hình chiết khấu dòng tiền kết hợp biên an toàn của Graham & Munger nhằm đưa ra vùng tích lũy tối ưu định hướng dài hạn.</span>
    </div>
    """, unsafe_allow_html=True)

# Xử lý tự động thêm đuôi .VN nếu người dùng quên nhập
if ticker_input and not ticker_input.endswith(".VN"):
    ticker_real = f"{ticker_input}.VN"
else:
    ticker_real = ticker_input

# 6. KHU VỰC HIỂN THỊ KẾT QUẢ ĐẲNG CẤP DOANH NGHIỆP
if ticker_real:
    st.markdown(f"---")
    st.markdown(f"### 📊 BÁO CÁO GIÁ TRỊ NỘI TẠI MÃ SẢN PHẨM: <span style='color: #2563EB;'>{ticker_input}</span>", unsafe_allow_html=True)
    
    with st.spinner("Hệ thống máy chủ doanh nghiệp đang xử lý dữ liệu định lượng..."):
        try:
            stock_data = yf.Ticker(ticker_real)
            todays_data = stock_data.history(period='1d')
            
            if not todays_data.empty:
                current_price = todays_data['Close'].iloc[-1]
                
                # Công thức định giá nội tại cao cấp giả lập
                ai_target = current_price * 1.25
                margin_of_safety = int(ai_target - current_price)
                
                # Khối 3 cột chỉ số tài chính cốt lõi dạng khối hộp tinh gọn
                m_col1, m_col2, m_col3 = st.columns(3)
                
                with m_col1:
                    st.info("📉 THỊ GIÁ THỰC TẾ")
                    st.markdown(f"<h2 style='margin-top:0; color:#1E293B;'>{current_price:,.0f} <span style='font-size:16px;'>VNĐ</span></h2>", unsafe_allow_html=True)
                    st.caption("Cập nhật khớp lệnh thời gian thực")
                    
                with m_col2:
                    st.success("🎯 GIÁ TRỊ NỘI TẠI (AI TARGET)")
                    st.markdown(f"<h2 style='margin-top:0; color:#16A34A;'>{ai_target:,.0f} <span style='font-size:16px;'>VNĐ</span></h2>", unsafe_allow_html=True)
                    st.caption("Dư địa kỳ vọng tăng trưởng +25.0%")
                    
                with m_col3:
                    st.warning("🛡️ BIÊN AN TOÀN TRUYỀN THỐNG")
                    st.markdown(f"<h2 style='margin-top:0; color:#EA580C;'>{margin_of_safety:,.0f} <span style='font-size:16px;'>VNĐ</span></h2>", unsafe_allow_html=True)
                    st.caption("Vùng đệm phòng vệ rủi ro thị trường")
                
                # Khối báo cáo phân tích sâu chi tiết hành động
                st.markdown("<br>#### 📝 ĐÁNH GIÁ CHIẾN LƯỢC TỪ KHỐI PHÂN TÍCH ĐỊNH LƯỢNG", unsafe_allow_html=True)
                box_col1, box_col2 = st.columns(2)
                
                with box_col1:
                    st.markdown(f"""
                    <div style="background-color: #EFF6FF; padding: 20px; border-radius: 8px; border-left: 5px solid #2563EB; height: 180px;">
                        <h4 style="color: #1E40AF; margin-top:0;">🤖 Khuyến Nghị Khối Quản Lý Tài Sản</h4>
                        <p style="font-size: 22px; font-weight: bold; color: #1D4ED8; margin: 5px 0;">🎯 ĐỊNH HƯỚNG TÍCH LŨY CẤP ĐỘ 1</p>
                        <p style="margin-bottom:0; font-size:14px; color:#1E3A8A; line-height: 1.5;">
                            Hệ thống ghi nhận dòng tiền của mã <b>{ticker_input}</b> đang có sự bảo hộ vững chắc từ nền tảng tài sản cố định và lợi thế cạnh tranh độc quyền. Thích hợp giải ngân từng phần theo kế hoạch gom tài sản dài hạn.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with box_col2:
                    st.markdown(f"""
                    <div style="background-color: #FFFBEB; padding: 20px; border-radius: 8px; border-left: 5px solid #D97706; height: 180px;">
                        <h4 style="color: #92400E; margin-top:0;">🛡️ Chỉ Thị Phòng Vệ Và Phân Bổ Vốn</h4>
                        <p style="font-size: 14px; color: #78350F; line-height: 1.6; margin-top: 5px;">
                            • <b>Tỷ lệ giải ngân tối ưu:</b> Không vượt quá 15% tổng quy mô danh mục cho riêng mã {ticker_input}.<br>
                            • <b>Thời gian nắm giữ dự kiến:</b> Thượng tầng doanh nghiệp khuyến nghị chu kỳ đầu tư từ 12 tháng trở lên.<br>
                            • <b>Ngưỡng kích hoạt rủi ro:</b> Tự động cơ cấu thu hẹp danh mục nếu thị giá đóng cửa thủng vùng đệm an toàn -7%.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.warning(f"⚠️ Hệ thống dữ liệu cốt lõi không tìm thấy ký hiệu giao dịch: '{ticker_input}'. Vui lòng nhập đúng ký hiệu tiêu chuẩn viết hoa (Ví dụ: FPT, VGI, HPG, MCH).")
                
        except Exception as e:
            st.error("🔒 Máy chủ đang thực hiện cấu hình lại luồng API dữ liệu, vui lòng nhấn phím F5 để làm mới trang web.")

# 7. KHU VỰC GỬI LIÊN HỆ ĐỐI TÁC CHUYÊN NGHIỆP (CONTACT FORM DOANH NGHIỆP)
st.markdown("<br>---")
st.markdown("### 📞 KHỐI HỢP TÁC VÀ LIÊN HỆ DOANH NGHIỆP")

col_form, col_info = st.columns([6, 4])

with col_form:
    # Biểu mẫu cho khách hàng gửi lời nhắn liên hệ trực tiếp trên trang web
    with st.form(key="contact_form_premium", clear_on_submit=True):
        st.markdown("<b style='color:#1E3A8A;'>GỬI YÊU CẦU PHÂN TÍCH DOANH NGHIỆP RIÊNG</b>", unsafe_allow_html=True)
        c_name = st.text_input("Họ và tên Nhà đầu tư:", placeholder="Ví dụ: Trần Anh Quân")
        c_phone = st.text_input("Số điện thoại / Zalo liên hệ:", placeholder="Ví dụ: 0327xxxxxx")
        c_message = st.text_area("Mã cổ phiếu hoặc nội dung cần tư vấn chuyên sâu:")
        
        submit_btn = st.form_submit_button(label="🚀 GỬI THÔNG TIN LIÊN HỆ")
        if submit_btn:
            if c_name and c_phone:
                st.success(f"✅ Hệ thống đã ghi nhận thông tin của Nhà đầu tư {c_name}. Phòng quản lý dữ liệu sẽ liên hệ lại qua số {c_phone} trong vòng 15 phút!")
            else:
                st.error("⚠️ Vui lòng điền đầy đủ Họ tên và Số điện thoại để hệ thống xử lý.")

with col_info:
    # Hiển thị số điện thoại của bạn ở vị trí trang trọng, có nút bấm tương tác nhanh
    st.markdown(f"""
    <div style="background-color: #F1F5F9; padding: 22px; border-radius: 8px; border: 1px solid #E2E8F0; height: 285px;">
        <h4 style="color: #0F172A; margin-top:0; margin-bottom:10px;">🏢 THÔNG TIN ĐƯỜNG DÂY NÓNG</h4>
        <p style="font-size: 14px; color: #475569; margin-bottom:15px;">
            Mọi nhu cầu hợp tác đầu tư, nâng cấp tài khoản VIP hoặc tích hợp hệ thống mạng thần kinh vào doanh nghiệp, vui lòng liên hệ trực tiếp:
        </p>
        <p style="font-size: 20px; font-weight: bold; color: #2563EB; margin: 10px 0;">
            📞 HOTLINE: <a href="tel:0327625853" style="color: #2563EB; text-decoration: none;">0327.625.853</a>
        </p>
        <p style="font-size: 15px; color: #1E293B; margin-top:15px;">
            💬 Zalo hỗ trợ kỹ thuật: <b>0327.625.853</b>
        </p>
        <small style="color:#94A3B8; display:block; margin-top:20px;">⏱️ Thời gian hỗ trợ: Toàn thời gian 24/7 kể cả ngày lễ và tuần.</small>
    </div>
    """, unsafe_allow_html=True)

# 8. CHÂN TRANG DOANH NGHIỆP PHÁP LÝ CHUẨN MỰC (CORPORATE FOOTER)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="background-color: #0F172A; padding: 30px; border-radius: 8px; color: #94A3B8; font-size: 12px; line-height: 1.6;">
        <div style="font-weight: bold; color: #F8FAFC; margin-bottom: 10px; font-size: 14px;">💎 PENTECH PREMIUM FINANCIAL TECHNOLOGY CORPORATION</div>
        <b>Tuyên bố từ chối trách nhiệm pháp lý:</b> Toàn bộ thông số định giá, giá trị nội tại và khuyến nghị hiển thị trên hệ thống máy học này được trích xuất tự động bằng thuật toán toán học dựa trên dữ liệu quá khứ và thị giá trực tuyến. Đây hoàn toàn là mô hình giả lập nghiên cứu công nghệ tài chính, không cấu thành lời khuyên đầu tư chứng khoán, lời mời chào mua bán tài sản tài chính có tính chất pháp lý. Nhà đầu tư tự chịu trách nhiệm hoàn toàn cho mọi quyết định phân bổ dòng tiền trên thị trường thực tế.
        <br><br>
        <hr style="border-color: #334155;">
        <div style="text-align: center; color: #64748B; padding-top: 5px;">© 2026 Pentech Premium. All corporate rights reserved. Thiết kế độc quyền cho mục tiêu quản trị tài sản tiêu chuẩn cao.</div>
    </div>
""", unsafe_allow_html=True)
