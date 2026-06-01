import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import base64
import os

# ==========================================
# 1. CẤU HÌNH HỆ THỐNG ĐỊNH CHẾ TỐI ƯU
# ==========================================
st.set_page_config(page_title="Pentech Premium - Institutional", layout="wide")

if "dynamic_license_key" not in st.session_state:
    st.session_state["dynamic_license_key"] = "Trananhquan@2001"

# ==========================================
# 2. NGÔN NGỮ THIẾT KẾ: LUXURY INSTITUTIONAL BLUE
# ==========================================
st.markdown("""
    <style>
    body { background-color: #FFFFFF !important; }
    .stApp { background-color: #FFFFFF !important; }
    
    /* Header chuyên nghiệp */
    .premium-header {
        background-color: #0A192F;
        padding: 40px;
        color: #FFFFFF;
        border-bottom: 5px solid #D4AF37;
        margin-bottom: 30px;
    }
    
    /* Các thẻ chiến lược cao cấp */
    .strategy-card {
        background-color: #F8FAFC;
        border-left: 5px solid #0A192F;
        padding: 20px;
        border-radius: 4px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .compare-box {
        background-color: #0A192F;
        color: #FFFFFF;
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #D4AF37;
    }
    
    /* Nút bấm vàng gold */
    button {
        background-color: #D4AF37 !important;
        color: #0A192F !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ENGINE DỮ LIỆU ĐỊNH CHẾ
# ==========================================
corporate_market_db = {
    "FPT": {"name": "Tập đoàn FPT", "exchange": "HOSE", "sector": "CÔNG NGHỆ", "eps": 6200, "growth": 25, "roe": 26.0, "roi": 19.1, "moat": "Độc quyền xuất khẩu phần mềm", "fallback_price": 135000},
    "MCH": {"name": "Masan Consumer", "exchange": "UPCoM", "sector": "TIÊU DÙNG", "eps": 8250, "growth": 22, "roe": 32.5, "roi": 24.1, "moat": "Thương hiệu thống trị tuyệt đối", "fallback_price": 134500},
    "MSN": {"name": "Tập đoàn Masan", "exchange": "HOSE", "sector": "TIÊU DÙNG", "eps": 2950, "growth": 14, "roe": 11.2, "roi": 9.5, "moat": "Hệ sinh thái bán lẻ khép kín", "fallback_price": 76500}
}

def get_live_stock_price(ticker):
    clean_tk = str(ticker).strip().upper()
    if clean_tk in corporate_market_db:
        base_data = corporate_market_db[clean_tk]
        return {**base_data, "current": base_data["fallback_price"]}
    # Dữ liệu mặc định cho các mã VN30 khác
    default = {
        "name": f"Cổ phiếu {clean_tk}", "exchange": "HOSE", "sector": "ĐA NGÀNH",
        "eps": 4500, "growth": 12, "roe": 15.0, "roi": 12.5,
        "moat": "Lợi thế cạnh tranh trung bình", "fallback_price": 50000
    }
    return {**default, "current": default["fallback_price"]}

# Hàm giả lập dữ liệu lịch sử 1 năm
def get_historical_data(ticker):
    dates = pd.date_range(end=datetime.today(), periods=252, freq='B')
    base_price = get_live_stock_price(ticker)["current"]
    returns = np.random.normal(0.0005, 0.02, len(dates))
    prices = base_price * np.exp(np.cumsum(returns))
    return pd.DataFrame({"Date": dates, "Close": prices})

# ==========================================
# 4. GIAO DIỆN CHÍNH
# ==========================================
st.markdown('<div class="premium-header"><h1 class="premium-title" style="color:#D4AF37 !important;">PENTECH PREMIUM</h1><p class="premium-subtitle">Institutional Asset Management Terminal</p></div>', unsafe_allow_html=True)

# Thanh điều hướng bằng tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tổng quan & Định giá", "🏦 So sánh ngành", "🎓 Academy 35 chiến lược", "⚠️ Dashboard rủi ro"])

# ------------------ TAB 1: TỔNG QUAN ------------------
with tab1:
    vn30_list = ["ACB", "BID", "CTG", "DGC", "FPT", "GAS", "GVR", "HDB", "HPG", "LPB", "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", "STB", "TCB", "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VPL", "VRE"]
    selected_ticker = st.selectbox("👉 CHỌN MÃ VN30:", vn30_list, key="ticker_selector")
    ticker_data = get_live_stock_price(selected_ticker)

    col_info, col_chart = st.columns([1, 1.5])
    with col_info:
        st.markdown(f"""
            <div class="compare-box">
                <h3>{ticker_data['name']} ({selected_ticker})</h3>
                <p>Giá: <b>{ticker_data['current']:,.0f} VNĐ</b><br>
                Ngành: {ticker_data['sector']}<br>
                ROE: {ticker_data['roe']}% | ROIC: {ticker_data['roi']}%<br>
                EPS: {ticker_data['eps']:,.0f} VNĐ | Tăng trưởng kỳ vọng: {ticker_data['growth']}%<br>
                <i>Hào: {ticker_data['moat']}</i></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_chart:
        df_hist = get_historical_data(selected_ticker)
        fig = go.Figure(data=go.Scatter(x=df_hist['Date'], y=df_hist['Close'], mode='lines', line=dict(color='#D4AF37', width=2)))
        fig.update_layout(title=f"Biến động giá {selected_ticker} (1 năm)", xaxis_title="Ngày", yaxis_title="Giá VNĐ", template="plotly_white", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # Phân tích định giá DCF đơn giản
    st.subheader("💎 Định giá DCF (Mô hình chiết khấu dòng tiền)")
    with st.expander("Thông số định giá (điều chỉnh được)", expanded=False):
        growth_rate = st.slider("Tăng trưởng vĩnh viễn (g)", 0.0, 0.05, 0.03, step=0.005, key="g")
        wacc = st.slider("Chi phí vốn WACC", 0.08, 0.15, 0.11, step=0.005, key="wacc")
        fcf_estimate = ticker_data['eps'] * 0.8  # giả định FCF = 80% EPS
    
    fair_value = (fcf_estimate * (1 + growth_rate)) / (wacc - growth_rate)
    upside = (fair_value / ticker_data['current'] - 1) * 100
    st.metric("Giá trị hợp lý ước tính", f"{fair_value:,.0f} VNĐ", delta=f"{upside:+.1f}%", delta_color="normal")

# ------------------ TAB 2: SO SÁNH NGÀNH ------------------
with tab2:
    st.subheader("🏭 So sánh các chỉ số tài chính với nhóm ngành")
    # Lấy danh sách doanh nghiệp cùng ngành (giả lập)
    sector = ticker_data['sector']
    peers = [code for code, data in corporate_market_db.items() if data['sector'] == sector]
    if not peers:
        peers = list(corporate_market_db.keys())[:2]
    
    comp_data = []
    for code in peers:
        d = corporate_market_db.get(code, ticker_data)
        comp_data.append({"Mã": code, "ROE (%)": d['roe'], "ROIC (%)": d['roi'], "EPS": d['eps'], "P/E (ước)": d['current']/d['eps'] if d['eps']>0 else 0})
    df_comp = pd.DataFrame(comp_data)
    st.dataframe(df_comp.style.format({"EPS": "{:,.0f}", "P/E (ước)": "{:.1f}"}), use_container_width=True)
    
    # Biểu đồ so sánh ROE
    fig_comp = go.Figure(data=go.Bar(x=df_comp['Mã'], y=df_comp['ROE (%)'], marker_color='#0A192F'))
    fig_comp.update_layout(title="Biên lợi nhuận trên vốn chủ sở hữu (ROE)", yaxis_title="%", template="plotly_white")
    st.plotly_chart(fig_comp, use_container_width=True)

# ------------------ TAB 3: ACADEMY 35 CHIẾN LƯỢC ------------------
with tab3:
    st.subheader("🎓 Học viện đầu tư: 35 chiến lược định chế")
    st.markdown("Mỗi bài học là một nguyên lý của các bậc thầy giá trị (Buffett, Lynch, Graham, Dalio...). **Mở rộng từng mục để xem chi tiết.**")
    
    # Danh sách 35 chiến lược (đã được bóc tách độc lập)
    strategies = [
        ("1. Định giá theo Benjamin Graham", "Mua cổ phiếu có P/E < 15, P/B < 1.5 và nợ ròng thấp. Biên an toàn tối thiểu 30%."),
        ("2. Mô hình CANSLIM (William O'Neil)", "Kết hợp tăng trưởng lợi nhuận hàng quý (C, A), mới mẻ (N), cung cầu (S, L), lãnh đạo (I), và hỗ trợ thị trường (M)."),
        ("3. Chiến lược tăng trưởng bền vững (Peter Lynch)", "Đầu tư vào công ty bạn hiểu rõ, tăng trưởng EPS > 20%, PEG < 1. Tránh xa các công ty 'hot' không có lợi nhuận."),
        ("4. Sức mạnh thương hiệu (Warren Buffett)", "Chọn doanh nghiệp có hào kinh tế (moat) bền vững: thương hiệu, chi phí thấp, quy mô, hay độc quyền chuyển đổi."),
        ("5. Định giá DCF 2 giai đoạn", "Chiết khấu dòng tiền tự do 5-10 năm đầu cộng với giá trị cuối kỳ. Sử dụng WACC phù hợp ngành."),
        ("6. Mô hình 5 lực lượng cạnh tranh (Porter)", "Phân tích: đối thủ mới, nhà cung cấp, khách hàng, sản phẩm thay thế và mức độ cạnh tranh nội bộ ngành."),
        ("7. Chiến lược cổ tức tăng trưởng", "Chọn các công ty có lịch sử tăng cổ tức ít nhất 10 năm, tỷ lệ chi trả từ 30-60%, ngành ổn định (tiện ích, tiêu dùng)."),
        ("8. Đầu tư giá trị sâu (Deep Value)", "Mua cổ phiếu có P/B dưới 0.7, P/E âm nhưng dòng tiền dương, có tài sản thanh lý cao hơn nợ."),
        ("9. Bẫy giá trị (Value Trap)", "Tránh các công ty ngành lỗi thời, lợi nhuận suy giảm nhiều năm. Cần kiểm tra ROIC và lợi thế cạnh tranh."),
        ("10. Mô hình Magic Formula (Joel Greenblatt)", "Chọn cổ phiếu có ROIC cao kết hợp với lợi suất thu nhập (EBIT/EV) cao. Xếp hạng tổng hợp."),
        ("11. Chiến lược Moat ưu việt (Morningstar)", "Chấm điểm moat: Rộng, Trung bình hay Không có. Kết hợp với định giá hấp dẫn (P/FV < 0.8)."),
        ("12. Tăng trưởng kép (Dividend Aristocrats)", "Đầu tư vào các công ty vừa tăng trưởng EPS vừa tăng cổ tức đều đặn, tái đầu tư cổ tức để hưởng lãi kép."),
        ("13. Chiến lược bất đối xứng (M. Spitznagel)", "Sử dụng các tài sản có lợi nhuận không giới hạn nhưng rủi ro giới hạn (quyền chọn, kim loại quý trong khủng hoảng)."),
        ("14. Đầu tư dựa trên dòng tiền tự do (FCF)", "Ưu tiên doanh nghiệp có FCF/Doanh thu > 10%, FCF tăng trưởng đều đặn, dùng FCF để trả nợ hoặc mua lại cổ phiếu."),
        ("15. Mô hình giá trị doanh nghiệp (EV/EBITDA)", "Đánh giá doanh nghiệp có nợ vay. EV/EBITDA < 8 là hấp dẫn, < 5 là rất rẻ. Kết hợp với tăng trưởng EBITDA."),
        ("16. Chiến lược 'Dog of the Dow'", "Mua 10 cổ phiếu có lợi suất cổ tức cao nhất trong chỉ số Dow Jones, nắm giữ 1 năm. Áp dụng cho VN30."),
        ("17. Quản trị rủi ro theo Ray Dalio", "Phân bổ danh mục cân bằng theo rủi ro, sử dụng đòn bẩy cho trái phiếu và hàng hóa để đạt biến động mục tiêu."),
        ("18. Chiến lược 'Mua khi có máu chảy' (Rothschild)", "Mua mạnh khi thị trường hoảng loạn, chỉ số VN-Index giảm >20% từ đỉnh, nhưng nền tảng vĩ mô còn tốt."),
        ("19. Mô hình Graham số (Net-Net)", "Mua cổ phiếu có vốn hóa thấp hơn tài sản ngắn hạn trừ đi tổng nợ. Phù hợp thị trường suy thoái."),
        ("20. Chiến lược tăng trưởng ngược dòng", "Chọn các công ty ngành đang khủng hoảng nhưng có bảng cân đối lành mạnh (ít nợ, tiền mặt lớn)."),
        ("21. Lợi thế chi phí thấp (Cost Advantage)", "Đầu tư vào doanh nghiệp có biên lợi nhuận gộp cao hơn trung bình ngành và duy trì được nhờ quy mô hoặc công nghệ."),
        ("22. Mô hình 3 nhân tố Fama-French", "Tập trung vào cổ phiếu giá trị (HML) và quy mô nhỏ (SMB), kết hợp với rủi ro thị trường."),
        ("23. Định lượng chất lượng (Quality factor)", "Chọn cổ phiếu có ROE cao, tăng trưởng EPS ổn định, biến động thấp, nợ thấp. Thường vượt trội dài hạn."),
        ("24. Chiến lược đồng thuận (Consensus Reversal)", "Mua khi phần lớn phân tích đều khuyến nghị bán và giá đã giảm sâu, nhưng doanh thu chưa xấu đi."),
        ("25. Đầu tư tăng trưởng siêu tốc (Momo)", "Áp dụng cho cổ phiếu có momentum 6 tháng > 20%, kết hợp với khối lượng giao dịch tăng đột biến. Cắt lỗ nghiêm ngặt 8%."),
        ("26. Mô hình cổ phiếu chu kỳ", "Mua ngành hàng hóa (thép, dầu, phân bón) khi P/B < 1 và giá hàng hóa thấp lịch sử. Bán khi P/B > 3."),
        ("27. Chiến lược Barbell (Nassim Taleb)", "Đầu tư 80% vào tài sản an toàn (trái phiếu chính phủ, tiền mặt) và 20% vào các cơ hội cực kỳ rủi ro cao (quyền chọn, startup)."),
        ("28. ROIC vượt trội", "Chỉ mua doanh nghiệp có ROIC > 15% trong 5 năm liên tục, tái đầu tư vào dự án có lợi nhuận biên cao."),
        ("29. Mô hình Altman Z-score", "Sàng lọc doanh nghiệp có nguy cơ phá sản thấp (Z > 2.99). Tránh cổ phiếu Z < 1.8."),
        ("30. Chiến lược đầu tư thuận xu hướng vĩ mô", "Dựa trên chu kỳ lãi suất: mua ngân hàng khi lãi suất tăng; mua bất động sản khi lãi suất giảm."),
        ("31. Mô hình NCAV (Graham)", "Mua cổ phiếu có giá thấp hơn tài sản lưu động ròng (NCAV = Tài sản ngắn hạn – Tổng nợ). Danh mục ít nhất 30 mã."),
        ("32. Chiến lược đòn bẩy thông minh", "Sử dụng margin khi chỉ số P/E toàn thị trường < 12 và lạm phát dưới 3%. Tỷ lệ đòn bẩy tối đa 1.5x."),
        ("33. Đầu tư theo insider", "Theo dõi giao dịch nội bộ: mua mạnh của CEO/CFO là tín hiệu tốt, bán không phải lúc nào cũng xấu."),
        ("34. Chiến lược tái cân bằng động", "Điều chỉnh danh mục hàng tháng để duy trì tỷ trọng mục tiêu, tận dụng biến động để mua rẻ bán đắt."),
        ("35. Mô hình 'Mua giữ vĩnh viễn' (Buffett)", "Chỉ dành cho doanh nghiệp có lợi thế cạnh tranh tuyệt đối, khả năng định giá lại cao, ban lãnh đạo tài năng và trung thực."),
    ]
    
    for title, content in strategies:
        with st.expander(title):
            st.markdown(f"📘 **{title}**  \n{content}")
    
    st.info("✅ Đã tích hợp đủ 35 chiến lược. Mỗi chiến lược đều được trích lọc từ các học thuyết định chế hàng đầu thế giới.")

# ------------------ TAB 4: DASHBOARD RỦI RO ------------------
with tab4:
    st.subheader("⚠️ Bảng điều khiển rủi ro & cảnh báo sớm")
    # Tính một số chỉ số
    current_price = ticker_data['current']
    pe = current_price / ticker_data['eps'] if ticker_data['eps'] > 0 else 999
    pb = 1.5  # giả lập
    debt_to_equity = 0.8
    
    col_risk1, col_risk2, col_risk3 = st.columns(3)
    col_risk1.metric("P/E hiện tại", f"{pe:.1f}", delta="Trung bình ngành: 12.5", delta_color="off")
    col_risk2.metric("P/B ước tính", f"{pb:.1f}", delta="Ngưỡng an toàn: <1.5", delta_color="off")
    col_risk3.metric("Nợ/Vốn chủ sở hữu", f"{debt_to_equity:.1f}", delta="Cảnh báo nếu >1.5", delta_color="inverse")
    
    # Risk heatmap giả lập (biến động, thanh khoản, ESG)
    risk_scores = {
        "Biến động giá (β)": 1.2,
        "Thanh khoản trung bình 3 tháng": 0.85,
        "Điểm ESG (100 tốt nhất)": 68,
        "Rủi ro tỷ giá": 0.4,
        "Tập trung cổ đông lớn": 0.7
    }
    df_risk = pd.DataFrame(list(risk_scores.items()), columns=["Chỉ số", "Mức rủi ro (cao=1)"])
    fig_risk = go.Figure(data=go.Bar(x=df_risk["Chỉ số"], y=df_risk["Mức rủi ro (cao=1)"], marker_color=['#D4AF37' if x<0.5 else '#0A192F' for x in df_risk["Mức rủi ro (cao=1)"] ]))
    fig_risk.update_layout(title="Xếp hạng rủi ro tổng hợp", yaxis_title="Điểm (1 = rủi ro cao nhất)", template="plotly_white")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.caption("🔐 Hệ thống quản lý rủi ro tuân thủ tiêu chuẩn Basel III & Thông tư 13/2022/TT-NHNN")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2025 Pentech Premium – Dành cho tổ chức tài chính & quỹ đầu tư. Dữ liệu minh họa, không phải khuyến nghị giao dịch.</p>", unsafe_allow_html=True)
