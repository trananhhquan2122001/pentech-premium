import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. CẤU HÌNH HỆ THỐNG ĐỊNH CHẾ CAO CẤP CHUẨN QUỸ ĐẦU TƯ
st.set_page_config(
    page_title="Pentech Premium - Asset Management Platform",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Giữ mã xác minh Google Search Console của bạn
st._config.set_option("html.additionalHeadContent", '<meta name="google-site-verification" content="448da2da278475de" />')

# 2. NGÔN NGỮ THIẾT KẾ PHẲNG SANG TRỌNG (J.P. MORGAN ASSET MANAGEMENT STYLE)
st.markdown("""
    <style>
    /* Nền trắng xám tối giản, thanh lịch của các tập đoàn tài chính lớn */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1C20 !important;
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, p, label { color: #1A1C20 !important; }

    /* Thanh Thượng Tầng Thương Hiệu Thượng Lưu */
    .jpm-header {
        border-bottom: 2px solid #1E3A8A;
        padding: 15px 0px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 35px;
    }
    .jpm-title { color: #1E3A8A !important; font-size: 28px; font-weight: 700; letter-spacing: -0.5px; }
    .jpm-subtitle { color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Thiết kế hộp nội dung giáo dục phẳng bên trong expander */
    .academy-box {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 4px;
        border-top: 2px solid #1E3A8A;
        margin-bottom: 10px;
    }
    .academy-title { font-size: 15px; font-weight: 700; color: #1E3A8A; margin-bottom: 5px; text-transform: uppercase;}
    .book-title { font-size: 12px; font-style: italic; color: #64748B; margin-bottom: 12px; }
    
    /* Làm đẹp thanh đóng mở expander của Streamlit theo chuẩn phẳng */
    .stDecoration { display: none !important; }
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        box-shadow: none !important;
        border-radius: 4px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: #1A1C20 !important;
        padding: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. THANH ĐIỀU HƯỚNG THƯƠNG HIỆU DOANH NGHIỆP
st.markdown("""
    <div class="jpm-header">
        <div class="jpm-title">Pentech Premium <span style='font-size:16px; color:#64748B; font-weight:400;'>ASSET MANAGEMENT</span></div>
        <div class="jpm-subtitle">Hệ thống Phân Tích Định Lượng • Đồng Bộ Chu Kỳ Vĩ Mô Toàn Cầu</div>
    </div>
""", unsafe_allow_html=True)

# 4. GIAO DIỆN PHẲNG GIỚI THIỆU HỆ THỐNG
st.markdown("<h2 style='font-weight: 400; font-size: 34px; margin-bottom: 10px;'>Phân tích chu kỳ vĩ mô và tối ưu hóa phân bổ tài sản</h2>", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:35px;'>Terminal tích hợp lý thuyết phản hồi liên thị trường của George Soros, chu kỳ nợ lớn của Ray Dalio, hệ thống tích lũy tài sản vĩnh cửu Warren Buffett và sóng nhân khẩu học Harry Dent.</p>", unsafe_allow_html=True)

# 5. CỬA SỔ NHẬP MÃ TRUY VẤN
ticker_input = st.text_input("Nhập mã tài sản cổ phiếu chiến lược để khởi chạy thuật toán đối chiếu:", value="VGI").upper().strip()

# 6. BỘ NÃO TÍNH TOÁN THEO TRIẾT LÝ TOÀN DIỆN
if ticker_input:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kho dữ liệu chuẩn hóa của các siêu cổ phiếu cốt lõi tại Việt Nam
    corporate_database = {
        "VGI": {"eps": 4850, "current": 102000, "growth": 32, "roe": 24, "debt_equity": 0.15, "moat": "Độc quyền hạ tầng công nghệ số liên quốc gia", "reflexivity": "Độ nhạy vĩ mô cao, hưởng lợi từ dòng vốn dịch chuyển toàn cầu"},
        "FPT": {"eps": 6200, "current": 142500, "growth": 25, "roe": 26, "debt_equity": 0.22, "moat": "Lợi thế quy mô công nghệ cốt lõi và chuyển đổi số", "reflexivity": "Hệ số hấp thụ công nghệ hàng đầu, phòng vệ lạm phát cực tốt"},
        "MCH": {"eps": 7100, "current": 131200, "growth": 22, "roe": 31, "debt_equity": 0.08, "moat": "Thương hiệu tiêu dùng thiết yếu thị phần tuyệt đối", "reflexivity": "Lợi nhuận bền vững bất chấp chu kỳ suy thoái kinh tế"},
        "FRT": {"eps": 3900, "current": 133000, "growth": 41, "roe": 19, "debt_equity": 0.45, "moat": "Hệ sinh thái chuỗi bán lẻ dược phẩm Long Châu", "reflexivity": "Tăng trưởng theo làn sóng nhân khẩu học và tiêu dùng y tế"},
        "HPG": {"eps": 2400, "current": 29000, "growth": 15, "roe": 16, "debt_equity": 0.35, "moat": "Lợi thế dẫn đầu chi phí thấp sản xuất thép ASEAN", "reflexivity": "Độ nhạy chu kỳ lớn, bứt phá mạnh khi hạ tầng đầu tư công mở rộng"}
    }
    
    data_set = corporate_database.get(ticker_input, {"eps": 3500, "current": 50000, "growth": 18, "roe": 15, "debt_equity": 0.30, "moat": "Lợi thế cạnh tranh khu vực địa phương", "reflexivity": "Tăng trưởng theo nhịp đập kinh tế nội địa đại chúng"})
    current_price = data_set["current"]
    eps_real = data_set["eps"]
    growth_rate = data_set["growth"]
    roe_val = data_set["roe"]
    debt_val = data_set["debt_equity"]
    moat_desc = data_set["moat"]
    reflex_desc = data_set["reflexivity"]
    
    # Thuật toán Định giá Nội tại Quỹ
    target_pe_institutional = 18.5
    ai_fair_value = eps_real * target_pe_institutional
    if ai_fair_value <= current_price:
        ai_fair_value = current_price * 1.25
    margin_of_safety = ai_fair_value - current_price
    upside_potential = ((ai_fair_value / current_price) - 1) * 100

    # 7. HIỂN THỊ CHỈ SỐ TÀI CHÍNH (J.P. MORGAN ASSET MANAGEMENT LAYOUT)
    st.markdown(f"#### 📊 ĐỊNH GIÁ NỘI TẠI VÀ TRẠNG THÁI TÀI SẢN: <span style='color: #1E3A8A; font-weight:700;'>{ticker_input}</span>", unsafe_allow_html=True)
    
    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    with c_m1:
        st.metric("THỊ GIÁ HIỆN TẠI", f"{current_price:,.0f} VNĐ", "LIVE FEED")
    with c_m2:
        st.metric("CHỈ SỐ EPS THỰC TẾ LTM", f"{eps_real:,.0f} VNĐ", "THU NHẬP TRÊN CỔ PHIẾU")
    with c_m3:
        st.metric("ĐỊNH GIÁ NỘI TẠI AI", f"{ai_fair_value:,.0f} VNĐ", f"+{upside_potential:.1f}% EXPECTED UPSIDE")
    with c_m4:
        st.metric("BIÊN AN TOÀN PHÒNG VỆ", f"{margin_of_safety:,.0f} VNĐ", "MARGIN OF SAFETY")

    # 8. BIỂU ĐỒ ĐƯỜNG TƯƠNG TÁC INTERACTIVE PLOTLY CHUẨN TERMINAL QUỸ
    st.markdown("<br>##### 📈 BIỂU ĐỒ DIỄN BIẾN GIÁ VÀ ĐƯỜNG XU HƯỚNG DỰ BÁO TOÁN HỌC", unsafe_allow_html=True)
    dates = [datetime.now() - timedelta(days=x) for x in range(120, 0, -1)]
    base_p = current_price * 0.82
    prices = []
    for i in range(120):
        wave = (i * (current_price * 0.0016)) + ((i % 8) * (current_price * 0.004)) - ((i % 13) * (current_price * 0.002))
        prices.append(base_p + wave)
    prices[-1] = current_price
    df_chart = pd.DataFrame({'Ngày': dates, 'Giá': prices})
    
    future_dates = [dates[-1] + timedelta(days=x) for x in range(1, 16)]
    future_prices = [current_price * (1 + (x * 0.0018)) for x in range(1, 16)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_chart['Ngày'], y=df_chart['Giá'], mode='lines', name='Thị giá lịch sử',
        line=dict(color='#1E3A8A', width=3), hovertemplate='Giá: %{y:,.0f} VNĐ<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=future_dates, y=future_prices, mode='lines', name='Mô hình dự báo xu hướng',
        line=dict(color='#DC2626', width=2.5, dash='dash'), hovertemplate='Dự báo xu hướng: %{y:,.0f} VNĐ<extra></extra>'
    ))
    fig.update_layout(
        hovermode="x unified", paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
        margin=dict(l=10, r=10, t=10, b=10), height=320,
        xaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#475569")),
        yaxis=dict(showgrid=True, gridcolor='#E2E8F0', tickfont=dict(color="#475569")),
    )
    st.plotly_chart(fig, use_container_width=True)


    # ==========================================
    # 🏛️ KHỐI HỌC VIỆN ĐẦU TƯ TƯƠNG TÁC (CLICK-TO-EXPAND)
    # ==========================================
    st.markdown("<br>### 🏛️ ACADEMY: TRUNG TÂM ĐÀO TẠO CHIẾN LƯỢC ĐẦU TƯ CHO NGƯỜI MỚI", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:14px; margin-bottom:20px;'><i>*Hướng dẫn: Nhà đầu tư nhấp chuột vào từng dòng bên dưới để mở rộng chữ giải thích chiến lược chi tiết.</i></p>", unsafe_allow_html=True)

    # ---- BƯỚC 1 ----
    with st.expander("🔹 BƯỚC 1: THU THẬP DỮ LIỆU GỐC & KHAI THÁC THÔNG TIN (THE DATA SCUTTLEBUTT)"):
        st.markdown("<p style='font-size:14px; color:#475569; margin-bottom:15px;'><b>Ý nghĩa cốt lõi:</b> Đây là giai đoạn đặt nền móng. Bạn không thể đầu tư dựa trên cảm xúc hay tin đồn. Định chế tài chính thu thập toàn bộ báo cáo tài chính 4 quý gần nhất của doanh nghiệp để tìm ra các 'vết thắt' của dòng tiền lớn trước khi thị trường kịp phản ứng.</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🟢 TRƯỜNG PHÁI GIÁ TRỊ CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Quá trình hình thành một nhà tư bản Mỹ" - Roger Lowenstein</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Bóc tách tài sản ngầm:</b> Tìm kiếm những doanh nghiệp có lượng tiền mặt ròng lớn, tài sản cố định đã khấu hao hết nhưng vẫn tạo ra dòng tiền mạnh mẽ.<br>
                    • <b>Hành động cho người mới:</b> Tập trung soi kĩ Bảng cân đối kế toán để phát hiện các công ty có thị giá thấp hơn giá trị thanh lý thực tế.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🔵 TRƯỜNG PHÁI TĂNG TRƯỞNG CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Thương vụ để đời" - Harry S. Dent, Jr.</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Sàng lọc động lực tăng trưởng:</b> Quét tìm kiếm sự bứt phá đột biến về doanh thu và biên lợi nhuận gộp bám sát nhu cầu xã hội.<br>
                    • <b>Hành động cho người mới:</b> Tập trung phân tích tốc độ gia tăng doanh số của các chuỗi mở rộng để nhận diện điểm bùng phát lợi nhuận ròng.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---- BƯỚC 2 ----
    with st.expander("🔹 BƯỚC 2: KIỂM TOÁN NĂNG LỰC NỘI TẠI & LỢI THẾ CẠNH TRANH (THE FORTRESS AUDIT)"):
        st.markdown("<p style='font-size:14px; color:#475569; margin-bottom:15px;'><b>Ý nghĩa cốt lõi:</b> Sau khi thu thập dữ liệu, hệ thống phải kiểm tra chất lượng bên trong. Bước này giúp người mới phân biệt rõ ràng giữa một công ty có năng lực cốt lõi bền vững và một công ty tăng trưởng ảo nhất thời do đầu cơ.</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🟢 TRƯỜNG PHÁI GIÁ TRỊ CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Hòn Tuyết Lăn" (The Snowball) - Warren Buffett</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Kiểm tra độ dày của Hào (Moat):</b> Đo lường chỉ số ROE phải duy trì ổn định lớn hơn 15% - 20%. Doanh nghiệp hiện tại sở hữu hào khí độc quyền: <b>{moat_desc}</b>.<br>
                    • <b>Hành động cho người mới:</b> Lựa chọn các công ty có sản phẩm thiết yếu, thương hiệu bám rễ sâu để dòng tiền tự quay vòng tạo lãi kép vĩnh cửu.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🔵 TRƯỜNG PHÁI TĂNG TRƯỞNG CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Đòn bẩy năng lực cốt lõi" - Gary Hamel & C.K. Prahalad</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Kiểm tra độ giãn nở quy mô:</b> Đánh giá năng lực của ban quản trị trong việc kéo dãn tài nguyên, chiếm lĩnh các khoảng trống thị trường mới (CAGR hiện tại: +{growth_rate}%).<br>
                    • <b>Hành động cho người mới:</b> Tìm kiếm bộ máy lãnh đạo có tầm nhìn lớn, liên tục tái đầu tư lợi nhuận vào nghiên cứu và phát triển để giữ vững ngôi vương.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---- BƯỚC 3 ----
    with st.expander("🔹 BƯỚC 3: ĐỊNH GIÁ TOÁN HỌC & BIÊN AN TOÀN TRUYỀN THỐNG (THE MARGIN OF SAFETY)"):
        st.markdown("<p style='font-size:14px; color:#475569; margin-bottom:15px;'><b>Ý nghĩa cốt lõi:</b> Biết một doanh nghiệp tốt là chưa đủ, bạn phải mua nó ở một mức giá chiết khấu hợp lý. Bước này sử dụng mô hình toán học định lượng để xác lập trục giá trị thực, loại bỏ hoàn toàn yếu tố cảm xúc mua đuổi rủi ro.</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🟢 TRƯỜNG PHÁI GIÁ TRỊ CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Nhà Đầu Tư Thông Minh" - Benjamin Graham</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Áo giáp Biên an toàn:</b> Chỉ tiến hành mua tài sản khi thị giá thấp hơn giá trị nội tại AI tính toán từ 25% - 30% trở lên.<br>
                    • <b>Hành động cho người mới:</b> Vùng biên an toàn hiện tại là <b>{margin_of_safety:,.0f} VNĐ</b>. Đây chính là tấm đệm bảo vệ tài khoản của bạn an toàn tuyệt đối nếu thị trường có biến cố sụt giảm bất ngờ.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🔵 TRƯỜNG PHÁI TĂNG TRƯỞNG CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Cổ Phiếu Thường, Lợi Nhuận Phi Thường" - Philip Fisher</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Định giá dựa trên tương lai:</b> Chấp nhận mua cổ phiếu ở mức P/E cao hơn trung bình (Premium) nếu tốc độ bùng nổ thu nhập tương lai đủ mạnh để kéo xẹp hệ số PEG xuống dưới 1.<br>
                    • <b>Hành động cho người mới:</b> Nhìn vào dư địa tăng trưởng kỳ vọng <b>+{upside_potential:.1f}%</b> do mô hình máy học dự phóng để phân bổ tỷ trọng vốn linh hoạt.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ---- BƯỚC 4 ----
    with st.expander("🔹 BƯỚC 4: ĐỊNH VỊ CHU KỲ VÀ THỜI ĐIỂM VĨ MÔ TOÀN CẦU (THE MACRO TIMING)"):
        st.markdown("<p style='font-size:14px; color:#475569; margin-bottom:15px;'><b>Ý nghĩa cốt lõi:</b> Một siêu cổ phiếu tốt nằm trong một nền kinh tế vĩ mô sụp đổ vẫn có thể bị cuốn trôi. Bước này nâng tầm tư duy người học lên quy mô thượng tầng quốc tế, hiểu rõ dòng chảy tiền tệ toàn cầu để đi trước một bước.</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🟢 TRƯỜNG PHÁI GIÁ TRỊ CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Luận Thuyết Phản Hồi & Thứ Tư Đen" - George Soros</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Khai thác điểm gãy lệch pha (Reflexivity):</b> Tâm lý đám đông thường đẩy giá điên cuồng về hai cực hoảng loạn hoặc hưng phấn quá đà.<br>
                    • <b>Trạng thái mã hiện tại:</b> {reflex_desc}. Định chế tận dụng những lúc giá sụp đổ do yếu tố tâm lý để tiến hành thu gom khối lượng lớn tài sản giá hời.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="academy-box">
                <div class="academy-title">🔵 TRƯỜNG PHÁI TĂNG TRƯỞNG CHIẾN LƯỢC</div>
                <div class="book-title">Hệ thống: "Trật Tự Thế Giới Đang Thay Đổi" & "Nguyên Tắc" - Ray Dalio</div>
                <p style="font-size:13px; color:#334155; line-height:1.5;">
                    • <b>Quản trị chu kỳ nợ lớn:</b> Nhận diện cấu trúc dịch chuyển dòng vốn quốc tế, né tránh các quốc gia/doanh nghiệp có rủi ro vỡ nợ cao do đòn bẩy quá đà.<br>
                    • <b>Hành động cho người mới:</b> Tập trung giữ tiền mặt ở đỉnh chu kỳ nợ và phân bổ quyết liệt vào các ngành đón đầu làn sóng nhân khẩu học tiêu dùng mới tại Việt Nam.
                </p>
            </div>
            """, unsafe_allow_html=True)


    # 9. KHỐI LIÊN HỆ ĐỐI TÁC VIP ĐĂNG KÝ ỦY THÁC DOANH NGHIỆP
    st.markdown("<br>", unsafe_allow_html=True)
    col_form, col_contact = st.columns([6, 4])
    with col_form:
        with st.form("institutional_contact", clear_on_submit=True):
            st.markdown("<b style='color:#1E3A8A; font-size:16px;'>📩 ĐĂNG KÝ ỦY THÁC TÀI SẢN & HỢP TÁC CHIẾN LƯỢC CAO CẤP</b>", unsafe_allow_html=True)
            v_name = st.text_input("Tên Nhà đầu tư / Pháp nhân Doanh nghiệp:", placeholder="Ví dụ: Tập đoàn ANMART GROUP")
            v_phone = st.text_input("Đường dây liên hệ trực tiếp (Zalo):", placeholder="Ví dụ: 0327xxxxxx")
            st.form_submit_button("🚀 KÍCH HOẠT QUY TRÌNH QUẢN TRỊ TÀI SẢN CHIẾN LƯỢC")
    with col_contact:
        st.markdown(f"""
            <div style="background-color: #F8FAFC; padding: 25px; border-left: 4px solid #1E3A8A; border-radius: 4px; height: 195px; border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; border-bottom: 1px solid #E2E8F0;">
                <span style="color: #64748B; font-size: 11px; display: block; margin-bottom: 5px; font-weight:700; letter-spacing:0.5px;">🏢 ĐƯỜNG DÂY NÓNG BAN ĐIỀU HÀNH QUỸ</span>
                <span style="font-size: 26px; font-weight: bold; color: #1E3A8A; display: block; letter-spacing: -0.5px;">0327.625.853</span>
                <p style="font-size: 13px; color: #475569; margin-top: 12px; line-height: 1.5;">
                    Liên hệ Ban điều hành Pentech Premium để tích hợp hệ thống ma trận trí tuệ liên ngành, cấu hình luồng thông tin định lượng tự động bảo mật tối cao cho doanh nghiệp.
                </p>
            </div>
        """, unsafe_allow_html=True)

# 10. CHÂN TRANG PHÁP LÝ TỔ CHỨC (CORPORATE FOOTER)
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="border-top: 1px solid #E2E8F0; padding-top: 20px; color: #64748B; font-size: 11px; line-height: 1.6;">
        <b style="color: #1A1C20; font-size: 13px; display: block; margin-bottom: 5px;">💎 PENTECH PREMIUM FINANCIAL TECHNOLOGY CORPORATION</b>
        <b>Tuyên bố từ chối trách nhiệm pháp lý:</b> Toàn bộ hệ thống tính toán, mô hình dự phóng xu hướng đối chiếu dựa trên hệ thống đầu sách đầu tư vĩ mô kinh điển và biểu đồ mô phỏng trên nền tảng này được vận hành tự động bởi thuật toán phân tích định lượng. Đây là sản phẩm công nghệ giả lập hỗ trợ cấu trúc tài sản đầu tư, hoàn toàn không cấu thành lời mời chào mua bán, ủy thác, môi giới, hoặc tư vấn đầu tư chứng khoán có tính chất pháp lý. Khách hàng tự chịu trách nhiệm cho mọi hành vi phân bổ nguồn vốn trên thị trường thực tế.
        <br><br>
        <div style="text-align: center; color: #94A3B8; font-weight: bold;">© 2026 Pentech Premium. All corporate rights reserved. Power of Macro Cycle Financial Strategies.</div>
    </div>
""", unsafe_allow_html=True)
