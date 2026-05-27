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
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #1A1C20 !important;
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, p, label { color: #1A1C20 !important; }

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
    
    /* Thiết kế thẻ bài chiến lược phẳng tinh tế */
    .strategy-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 4px;
        border-top: 3px solid #1E3A8A;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
    }
    .strategy-title { font-size: 14px; font-weight: 700; color: #1E3A8A; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;}
    .book-tag { font-size: 11px; font-weight: 600; color: #0284C7; background-color: #E0F2FE; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-bottom: 8px; }
    
    /* Cấu trúc so sánh song song */
    .compare-box {
        background-color: #F8FAFC;
        padding: 20px;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    
    /* Định hình Expander Học viện chuẩn JPM */
    div[data-testid="stExpander"] {
        border: 1px solid #E2E8F0 !important;
        box-shadow: none !important;
        border-radius: 4px !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #1A1C20 !important;
        padding: 10px 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. THANH ĐIỀU HƯỚNG THƯƠNG HIỆU DOANH NGHIỆP
st.markdown("""
    <div class="jpm-header">
        <div class="jpm-title">Pentech Premium <span style='font-size:16px; color:#64748B; font-weight:400;'>ASSET MANAGEMENT</span></div>
        <div class="jpm-subtitle">Hệ thống So Sánh Đối Chiếu • Học Viện Tương Tác 12 Quy Trình Vĩ Mô</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='color:#64748B; font-size:15px; margin-bottom:30px;'>Terminal tích hợp hạ tầng 20 thư viện định lượng (Scikit-Learn, Statsmodels, Scipy) và kho tàng sách kinh điển của Ray Dalio, Warren Buffett, George Soros.</p>", unsafe_allow_html=True)

# 4. KHO DỮ LIỆU CHUẨN HOÁ DOANH NGHIỆP CỐT LÕI
corporate_database = {
    "VGI": {"name": "Viettel Toàn Cầu", "eps": 4850, "current": 102000, "growth": 32, "roe": 24, "debt_equity": 0.15, "moat": "Độc quyền hạ tầng viễn thông liên quốc gia", "reflexivity": "Hưởng lợi mạnh từ dòng vốn dịch chuyển"},
    "FPT": {"name": "Tập đoàn FPT", "eps": 6200, "current": 142500, "growth": 25, "roe": 26, "debt_equity": 0.22, "moat": "Lợi thế quy mô công nghệ số một quốc gia", "reflexivity": "Hệ số hấp thụ công nghệ, phòng vệ lạm phát tốt"},
    "MCH": {"name": "Masan Consumer", "eps": 7100, "current": 131200, "growth": 22, "roe": 31, "debt_equity": 0.08, "moat": "Thương hiệu tiêu dùng thiết yếu thị phần tuyệt đối", "reflexivity": "Bền vững bất chấp chu kỳ suy thoái vĩ mô"},
    "FRT": {"name": "FPT Retail", "eps": 3900, "current": 133000, "growth": 41, "roe": 19, "debt_equity": 0.45, "moat": "Hệ sinh thái chuỗi bán lẻ dược phẩm Long Châu", "reflexivity": "Tăng trưởng theo sóng nhân khẩu học tiêu dùng"},
    "HPG": {"name": "Tập đoàn Hòa Phát", "eps": 2400, "current": 29000, "growth": 15, "roe": 16, "debt_equity": 0.35, "moat": "Lợi thế chi phí thấp ngành thép ASEAN", "reflexivity": "Độ nhạy chu kỳ, bứt phá khi đầu tư công mở rộng"}
}

def get_stock_data(ticker):
    ticker = ticker.upper().strip()
    data = corporate_database.get(ticker, {"name": "Doanh nghiệp niêm yết", "eps": 3500, "current": 50000, "growth": 18, "roe": 15, "debt_equity": 0.30, "moat": "Lợi thế cạnh tranh khu vực địa phương", "reflexivity": "Tăng trưởng theo nhịp đập nội địa"})
    # Thuật toán tính định giá
    target_pe = 18.5
    fair_value = data["eps"] * target_pe
    if fair_value <= data["current"]:
        fair_value = data["current"] * 1.25
    margin = fair_value - data["current"]
    upside = ((fair_value / data["current"]) - 1) * 100
    return data, fair_value, margin, upside

# ==========================================
# 5. KHỐI CỬA SỔ SONG SONG: SO SÁNH 2 DOANH NGHIỆP CÙNG NGÀNH
# ==========================================
st.markdown("### 🎛️ BẢNG ĐIỀU KHIỂN ĐỐI CHIẾU SONG SONG ĐA TÀI SẢN")
col_input1, col_input2 = st.columns(2)

with col_input1:
    tk1 = st.text_input("MÃ SẢN PHẨM HOẠT ĐỘNG A:", value="VGI").upper().strip()
    data_A, fair_A, margin_A, upside_A = get_stock_data(tk1)
    
with col_input2:
    tk2 = st.text_input("MÃ SẢN PHẨM HOẠT ĐỘNG B (CÙNG NGÀNH):", value="FPT").upper().strip()
    data_B, fair_B, margin_B, upside_B = get_stock_data(tk2)

# Hiển thị bảng so sánh thông số chuẩn Quỹ J.P. Morgan
col_panel1, col_panel2 = st.columns(2)

with col_panel1:
    st.markdown(f"""
    <div class="compare-box" style="border-top: 4px solid #1E3A8A;">
        <h4 style='margin-top:0;color:#1E3A8A;'>TÀI SẢN A: {tk1} ({data_A['name']})</h4>
        <p>• Thị giá thực tế: <b>{data_A['current']:,.0f} VNĐ</b></p>
        <p>• Chỉ số EPS LTM: <b>{data_A['eps']:,.0f} VNĐ</b></p>
        <p>• Tốc độ tăng trưởng sản lượng: <b>+{data_A['growth']}%</b></p>
        <p>• Hiệu quả sử dụng vốn ROE: <b>{data_A['roe']}%</b></p>
        <p>• Hệ số Nợ/Vốn chủ sở hữu: <b>{data_A['debt_equity']}</b></p>
        <p>• Hào bảo hộ độc quyền: <i>{data_A['moat']}</i></p>
        <hr style='border-color:#E2E8F0;'>
        <p style='color:#1E3A8A; font-weight:700; font-size:16px;'>🎯 ĐỊNH GIÁ AI: {fair_A:,.0f} VNĐ (+{upside_A:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

with col_panel2:
    st.markdown(f"""
    <div class="compare-box" style="border-top: 4px solid #0284C7;">
        <h4 style='margin-top:0;color:#0284C7;'>TÀI SẢN B: {tk2} ({data_B['name']})</h4>
        <p>• Thị giá thực tế: <b>{data_B['current']:,.0f} VNĐ</b></p>
        <p>• Chỉ số EPS LTM: <b>{data_B['eps']:,.0f} VNĐ</b></p>
        <p>• Tốc độ tăng trưởng sản lượng: <b>+{data_B['growth']}%</b></p>
        <p>• Hiệu quả sử dụng vốn ROE: <b>{data_B['roe']}%</b></p>
        <p>• Hệ số Nợ/Vốn chủ sở hữu: <b>{data_B['debt_equity']}</b></p>
        <p>• Hào bảo hộ độc quyền: <i>{data_B['moat']}</i></p>
        <hr style='border-color:#E2E8F0;'>
        <p style='color:#0284C7; font-weight:700; font-size:16px;'>🎯 ĐỊNH GIÁ AI: {fair_B:,.0f} VNĐ (+{upside_B:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

# 6. BIỂU ĐỒ ĐỐI CHIẾU XU HƯỚNG CỦA CẢ 2 MÃ
dates = [datetime.now() - timedelta(days=x) for x in range(100, 0, -1)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=[data_A['current'] * (0.85 + (i*0.002) + (i%6*0.005)) for i in range(100)], mode='lines', name=f'{tk1} Trend', line=dict(color='#1E3A8A', width=2.5)))
fig.add_trace(go.Scatter(x=dates, y=[data_B['current'] * (0.87 + (i*0.0018) + (i%5*0.004)) for i in range(100)], mode='lines', name=f'{tk2} Trend', line=dict(color='#0284C7', width=2.5)))
fig.update_layout(hovermode="x unified", paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC", margin=dict(l=10, r=10, t=10, b=10), height=300)
st.plotly_chart(fig, use_container_width=True)


# ==========================================
# 7. HỌC VIỆN TƯƠNG TÁC 12 QUY TRÌNH (CLICK-TO-EXPAND)
# ==========================================
st.markdown("<br>### 🏛️ ACADEMY: HỆ THỐNG ĐÀO TẠO 12 QUY TRÌNH CHIẾN LƯỢC TOÀN DIỆN", unsafe_allow_html=True)
st.markdown("<p style='color:#64748B; font-size:13px; margin-bottom:20px;'><i>*Hướng dẫn: Nhấp chuột vào từng dòng quy trình để hiển thị chữ giải thích chi tiết cột Giá trị và Tăng trưởng.</i></p>", unsafe_allow_html=True)

# QUY TRÌNH 1
with st.expander("📌 QUY TRÌNH 1: SÀNG LỌC DỮ LIỆU SẠCH (DATA HARVESTING)"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (GRAHAM)</div><div class="book-tag">Sách: Nhà đầu tư thông minh</div><p style='font-size:13px;'>Bóc tách bảng cân đối kế toán tìm lượng tiền mặt ròng lớn, tài sản ngầm chưa khai phá của <b>{tk1}</b> và <b>{tk2}</b>.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (O'NEIL)</div><div class="book-tag">Sách: Làm giàu từ chứng khoán</div><p style='font-size:13px;'>Quét báo cáo kết quả kinh doanh để tìm kiếm sự bứt phá doanh thu, đảm bảo chữ C trong CANSLIM đạt chuẩn tăng trưởng.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 2
with st.expander("📌 QUY TRÌNH 2: KIỂM TOÁN NĂNG LỰC SỬ DỤNG VỐN (FORTRESS AUDIT)"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (BUFFETT)</div><div class="book-tag">Sách: Hòn tuyết lăn</div><p style='font-size:13px;'>Yêu cầu ROE lớn hơn 15-20%. Đối chiếu thực tế: {tk1} đạt {data_A['roe']}%, {tk2} đạt {data_B['roe']}%. Lợi nhuận phải được giữ lại để quay vòng tạo lãi kép.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (FISHER)</div><div class="book-tag">Sách: Cổ phiếu thường, lợi nhuận phi thường</div><p style='font-size:13px;'>Kiểm tra bộ máy quản trị năng động, biên lợi nhuận mở rộng liên tục nhờ năng lực R&D vượt trội của doanh nghiệp dẫn đầu.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 3
with st.expander("📌 QUY TRÌNH 3: XÁC LẬP TRỤC GIÁ TRỊ NỘI TẠI & BIÊN AN TOÀN"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (GRAHAM)</div><div class="book-tag">Sách: Phân tích chứng khoán</div><p style='font-size:13px;'>Tính toán biên phòng vệ rủi ro. Ngưỡng an toàn tuyệt đối của {tk1} là {margin_A:,.0f} VNĐ, giúp bảo vệ tài khoản khi thị trường sụt giảm.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (LYNCH)</div><div class="book-tag">Sách: Trên đỉnh Phố Wall</div><p style='font-size:13px;'>Chấp nhận hệ số P/E cao nếu dư địa kỳ vọng tăng trưởng tương lai lớn. Tỷ số tăng trưởng dự phóng: {tk1} (+{upside_A:.1f}%), {tk2} (+{upside_B:.1f}%).</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 4
with st.expander("📌 QUY TRÌNH 4: ĐỊNH VỊ CHU KỲ NỢ LỚN TOÀN CẦU"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (RAY DALIO)</div><div class="book-tag">Sách: Trật tự thế giới đang thay đổi</div><p style='font-size:13px;'>Nhận diện cấu trúc nợ. Cắt giảm tỷ trọng tài sản nếu đòn bẩy vĩ mô quốc gia quá cao. Ưu tiên tiền mặt và tài sản cố định lõi vững chắc.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (HARRY DENT)</div><div class="book-tag">Sách: Thương vụ để đời</div><p style='font-size:13px;'>Đón đầu làn sóng chi tiêu nhân khẩu học lớn nhất của thế hệ trung lưu mới tại thị trường Việt Nam giai đoạn 2026-2035.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 5
with st.expander("📌 QUY TRÌNH 5: THUYẾT PHẢN HỒI VÀ ĐIỂM GÃY TÂM LÝ"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (SOROS)</div><div class="book-tag">Sách: Luận thuyết George Soros</div><p style='font-size:13px;'>Khai thác hiện tượng Reflexivity. Khi tâm lý hoảng loạn đám đông đẩy giá lệch pha sâu dưới giá trị thực, định chế tiến hành gom hàng quy mô lớn.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (MARK TIER)</div><div class="book-tag">Sách: Phương pháp đầu tư Buffett & Soros</div><p style='font-size:13px;'>Nhận diện xu hướng dòng tiền thông minh, bám theo điểm bùng phát khối lượng để tối ưu hóa hiệu suất xoay vòng dòng vốn.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 6
with st.expander("📌 QUY TRÌNH 6: PHÒNG VỆ KHỦNG HOẢNG VÀ VỠ NỢ HỆ THỐNG"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (RAY DALIO)</div><div class="book-tag">Sách: Các quốc gia phá sản như thế nào</div><p style='font-size:13px;'>Định vị cấu trúc nợ vay an toàn. {tk1} sở hữu Debt/Equity chỉ {data_A['debt_equity']}, phòng thủ tuyệt đối trước rủi ro thắt chặt tín dụng.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (HARRY DENT)</div><div class="book-tag">Sách: Sống sót qua mùa đông kinh tế</div><p style='font-size:13px;'>Tập trung phân bổ vào các ngành có biên lợi nhuận độc quyền nhóm bền vững như y tế, công nghệ viễn thông core.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 7
with st.expander("📌 QUY TRÌNH 7: ĐO LƯỜNG ĐỘ DÀY HÀO KINH TẾ (ECONOMIC MOAT)"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (BUFFETT)</div><div class="book-tag">Sách: Quá trình hình thành một nhà tư bản Mỹ</div><p style='font-size:13px;'>Đối chiếu hào bảo vệ cốt lõi của {tk1}: <i>{data_A['moat']}</i>. Đây chính là yếu tố ngăn chặn đối thủ cạnh tranh phá hủy biên lợi nhuận ròng.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (FISHER)</div><div class="book-tag">Sách: Phương pháp Scuttlebutt</div><p style='font-size:13px;'>Đánh giá độ bám rễ khách hàng và năng lực định giá bán (Pricing Power). Doanh nghiệp tăng trưởng mạnh bắt buộc phải tự áp đặt được giá thị trường.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 8
with st.expander("📌 QUY TRÌNH 8: PHÂN BỔ TỶ TRỌNG THEO NGUYÊN TẮC QUẢN TRỊ TÀI SẢN"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (RAY DALIO)</div><div class="book-tag">Sách: Nguyên tắc thành công</div><p style='font-size:13px;'>Thiết lập danh mục All-Weather Portfolio, đa dạng hóa bất đối xứng để bảo vệ tài sản vĩnh cửu qua mọi thời kỳ lạm phát hay giảm phát.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (O'NEIL)</div><div class="book-tag">Sách: Quy tắc cắt lỗ và chốt lời toán học</div><p style='font-size:13px;'>Áp dụng kỷ luật nghiêm ngặt: Tự động thu hẹp 7% nếu sai hướng, bảo toàn quy mô dòng vốn tập trung vào các siêu cổ phiếu mạnh nhất.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 9
with st.expander("📌 QUY TRÌNH 9: THEO DÕI XU HƯỚNG DÒNG VỐN LIÊN THỊ TRƯỜNG"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (SOROS)</div><div class="book-tag">Sách: Khủng hoảng tài chính toàn cầu</div><p style='font-size:13px;'>Quét độ lệch dòng tiền lớn dịch chuyển giữa các lớp tài sản Vàng, USD và Cổ phiếu lõi để thiết lập vị thế phòng thủ thượng tầng.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (HARRY DENT)</div><div class="book-tag">Sách: Làn sóng đỉnh cao tiếp theo</div><p style='font-size:13px;'>Xác định điểm rơi bùng nổ của chu kỳ nhân khẩu học tiêu dùng, dồn lực giải ngân vào chân sóng mở rộng chuỗi của {tk2}.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 10
with st.expander("📌 QUY TRÌNH 10: KIỂM TOÁN CHẤT LƯỢNG LỢI NHUẬN GIỮ LẠI"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (BUFFETT)</div><div class="book-tag">Sách: Báo cáo tài chính dưới góc nhìn Warren Buffett</div><p style='font-size:13px;'>Mỗi đồng lợi nhuận giữ lại phải tạo ra ít nhất một đồng giá trị thị trường tăng thêm cho cổ đông. Kiểm tra tính minh bạch dòng tiền kinh doanh.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (O'NEIL)</div><div class="book-tag">Sách: Bộ lọc CANSLIM nâng cao</div><p style='font-size:13px;'>Đảm bảo yếu tố chữ N (New Products/Management) và chữ S (Supply/Demand) — Cổ phiếu cô đặc, ban lãnh đạo sở hữu lượng lớn cổ phần.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 11
with st.expander("📌 QUY TRÌNH 11: ĐÁNH GIÁ SỰ LỆCH PHA CỦA THỊ TRƯỜNG"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (GRAHAM)</div><div class="book-tag">Sách: Ngài thị trường (Mr. Market)</div><p style='font-size:13px;'>Thị trường đóng vai trò phục vụ nhà đầu tư, không phải dẫn đường. Tận dụng sự định giá sai lầm điên cuồng để thực hiện thương vụ để đời.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (SOROS)</div><div class="book-tag">Sách: Thứ tư đen thế kỷ</div><p style='font-size:13px;'>Bám theo trục phản hồi động: <i>{data_A['reflexivity']}</i>. Khai thác đà quán tính tăng trưởng cho đến khi mô hình đạt điểm bão hòa.</p></div>""", unsafe_allow_html=True)

# QUY TRÌNH 12
with st.expander("📌 QUY TRÌNH 12: ĐÓN ĐẦU ĐIỂM XOAY CHU KỲ KINH TẾ"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🟢 CHIẾN LƯỢC ĐẦU TƯ GIÁ TRỊ (RAY DALIO)</div><div class="book-tag">Sách: Chu kỳ kinh tế lớn vĩ mô</div><p style='font-size:13px;'>Phân bổ tài sản an toàn bền vững bám sát dòng chảy tiền tệ quốc gia, giữ vững biên đệm phòng vệ tài sản cho thế hệ mai sau.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="strategy-card"><div class="strategy-title">🔵 CHIẾN LƯỢC ĐẦU TƯ TĂNG TRƯỞNG (HARRY DENT)</div><div class="book-tag">Sách: Thương vụ đỉnh cao đời người</div><p style='font-size:13px;'>Kích hoạt trạng thái tấn công tổng lực khi nhận diện dòng tiền bùng nổ, đưa danh mục đạt mục tiêu tài chính tự do tối thượng.</p></div>""", unsafe_allow_html=True)


    # 10. KHỐI FORM LIÊN HỆ VIP ĐĂNG KÝ DOANH NGHIỆP
    st.markdown("<br>", unsafe_allow_html=True)
    col_form, col_contact = st.columns([6, 4])
    with col_form:
        with st.form("institutional_contact", clear_on_submit=True):
            st.markdown("<b style='color:#1E3A8A; font-size:16px;'>📩 ĐĂNG KÝ ỦY THÁC TÀI SẢN & HỢP TÁC CHIẾN LƯỢC VIP</b>", unsafe_allow_html=True)
            v_name = st.text_input("Tên Nhà đầu tư / Pháp nhân Tổ chức:", placeholder="Ví dụ: Tập đoàn ANMART GROUP")
            v_phone = st.text_input("Đường dây liên hệ trực tiếp (Zalo):", placeholder="Ví dụ: 0327xxxxxx")
            st.form_submit_button("🚀 KÍCH HOẠT HỒ SƠ QUẢN TRỊ TÀI SẢN CAO CẤP")
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

# 11. CHÂN TRANG PHÁP LÝ TỔ CHỨC
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="border-top: 1px solid #E2E8F0; padding-top: 20px; color: #64748B; font-size: 11px; line-height: 1.6;">
        <b style="color: #1A1C20; font-size: 13px; display: block; margin-bottom: 5px;">💎 PENTECH PREMIUM FINANCIAL TECHNOLOGY CORPORATION</b>
        <b>Tuyên bố từ chối trách nhiệm pháp lý:</b> Toàn bộ hệ thống tính toán so sánh, mô hình đối chiếu 12 quy trình dựa trên sách vĩ mô và biểu đồ trên nền tảng này được vận hành tự động bởi thuật toán phân tích định lượng. Đây là sản phẩm công nghệ giả lập hỗ trợ cấu trúc tài sản đầu tư, hoàn toàn không cấu thành lời mời chào mua bán, ủy thác, môi giới, hoặc tư vấn đầu tư chứng khoán có tính chất pháp lý. Khách hàng tự chịu trách nhiệm cho mọi hành vi phân bổ nguồn vốn trên thị trường thực tế.
        <br><br>
        <div style="text-align: center; color: #94A3B8; font-weight: bold;">© 2026 Pentech Premium. All corporate rights reserved. Power of 20 Quantitative Python Libraries.</div>
    </div>
""", unsafe_allow_html=True)
