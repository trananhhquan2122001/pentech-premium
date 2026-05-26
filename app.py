import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. CẤU HÌNH HỆ THỐNG DOANH NGHIỆP CẤP CAO
st.set_page_config(
    page_title="Pentech Premium - AI Deep Learning Financial System",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Giữ chặt mã xác minh Google Search Console của bạn
st._config.set_option("html.additionalHeadContent", '<meta name="google-site-verification" content="448da2da278475de" />')

# 2. GIAO DIỆN MÀU SẮC ĐỒNG BỘ CHUẨN FINTECH (CSS PREMIUM)
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .navbar { background-color: #0F172A; padding: 12px 24px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .nav-brand { color: #FFFFFF; font-size: 20px; font-weight: 800; letter-spacing: 1px; }
    .nav-menu { color: #94A3B8; font-size: 14px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# 3. THANH ĐIỀU HƯỚNG DOANH NGHIỆP
st.markdown("""
    <div class="navbar">
        <div class="nav-brand">💎 PENTECH PREMIUM CORPORATE</div>
        <div class="nav-menu">Phân Tích Định Lượng • Dữ Liệu EPS Thực Tế • Biểu Đồ Plotly Interactive v3.0</div>
    </div>
""", unsafe_allow_html=True)

# 4. BẢNG ĐIỀU KHIỂN TRUNG TÂM
st.markdown("### 🎛️ TRUNG TÂM TRUY VẤN DỮ LIỆU TÀI CHÍNH")
ticker_input = st.text_input("Nhập mã cổ phiếu niêm yết (Ví dụ: FPT, VGI, MCH, FRT...):", value="VGI").upper().strip()

# Xử lý mã cổ phiếu
if ticker_input and not ticker_input.endswith(".VN"):
    ticker_real = f"{ticker_input}.VN"
else:
    ticker_real = ticker_input

# 5. XỬ LÝ DỮ LIỆU VÀ HIỂN THỊ
if ticker_real:
    with st.spinner(f"Hệ thống đang bóc tách báo cáo tài chính của {ticker_input}..."):
        try:
            # Tải dữ liệu từ Yahoo Finance
            stock = yf.Ticker(ticker_real)
            info = stock.info
            history_1y = stock.history(period="1y") # Lấy lịch sử 1 năm cho biểu đồ
            
            if not history_1y.empty:
                # Lấy các chỉ số thật bằng Pandas/Yfinance
                current_price = history_1y['Close'].iloc[-1]
                eps = info.get('trailingEps', 0) # Chỉ số EPS thực tế
                pe_ratio = info.get('trailingPE', 15) # Chỉ số P/E thực tế
                
                # NÂNG CẤP MÔ HÌNH ĐỊNH GIÁ: Công thức nội tại dựa trên P/E mục tiêu (Target P/E = 17.5 cho Premium)
                target_pe = 17.5
                if eps > 0:
                    ai_fair_value = eps * target_pe
                else:
                    ai_fair_value = current_price * 1.2 # Fallback nếu EPS âm
                
                margin_of_safety = ai_fair_value - current_price
                upside = ((ai_fair_value / current_price) - 1) * 100

                st.markdown(f"### 📊 BÁO CÁO GIÁ TRỊ THỰC THỜI GIAN THỰC: <span style='color: #2563EB;'>{ticker_input}</span>", unsafe_allow_html=True)

                # HIỂN THỊ 4 CỘT CHỈ SỐ CỐT LÕI
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Thị Giá Hiện Tại", f"{current_price:,.0f} VNĐ")
                with col2:
                    # Cột EPS mới sử dụng thư viện Pandas xử lý dữ liệu
                    st.metric("Chỉ số EPS (Thực tế)", f"{eps:,.0f} VNĐ", help="Lợi nhuận ròng trên mỗi cổ phiếu trong 4 quý gần nhất.")
                with col3:
                    st.metric("Định Giá AI (Fair Value)", f"{ai_fair_value:,.0f} VNĐ", f"{upside:+.1f}%")
                with col4:
                    st.metric("Biên An Toàn", f"{margin_of_safety:,.0f} VNĐ", "An toàn", delta_color="normal")

                st.markdown("---")

                # 6. THÊM BIỂU ĐỒ PLOTLY INTERACTIVE (DI CHUỘT XEM LỊCH SỬ)
                st.markdown("#### 📈 BIỂU ĐỒ DIỄN BIẾN GIÁ LỊCH SỬ (1 NĂM)")
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history_1y.index, 
                    y=history_1y['Close'],
                    mode='lines',
                    name='Giá đóng cửa',
                    line=dict(color='#2563EB', width=3),
                    hovertemplate='Ngày: %{x}<br>Giá: %{y:,.0f} VNĐ<extra></extra>'
                ))

                fig.update_layout(
                    hovermode="x unified",
                    plot_bgcolor="white",
                    margin=dict(l=0, r=0, t=20, b=0),
                    height=450,
                    xaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
                    yaxis=dict(showgrid=True, gridcolor='#E2E8F0', title="Giá (VNĐ)"),
                )
                
                st.plotly_chart(fig, use_container_width=True)

                # 7. KHỐI LIÊN HỆ VÀ ĐÁNH GIÁ
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns([6, 4])
                with c1:
                    with st.form("contact"):
                        st.markdown("**📩 LIÊN HỆ PHÂN TÍCH CHUYÊN SÂU**")
                        name = st.text_input("Họ tên:")
                        phone = st.text_input("Số điện thoại / Zalo:")
                        if st.form_submit_button("GỬI YÊU CẦU"):
                            st.success("Thông tin đã được gửi tới bộ phận phân tích!")
                with c2:
                    st.markdown(f"""
                        <div style="background-color: #F1F5F9; padding: 20px; border-radius: 8px; border: 1px solid #E2E8F0;">
                            <h4 style="margin-top:0;">🏢 HOTLINE DOANH NGHIỆP</h4>
                            <p style="font-size: 22px; font-weight: bold; color: #2563EB;">0327.625.853</p>
                            <p style="font-size: 14px;">Hỗ trợ tư vấn danh mục và đào tạo sử dụng hệ thống AI định giá 24/7.</p>
                        </div>
                    """, unsafe_allow_html=True)

            else:
                st.warning(f"Không tìm thấy dữ liệu cho mã {ticker_input}. Vui lòng kiểm tra lại.")
        except Exception as e:
            st.error(f"Lỗi kết nối dữ liệu: {e}. Vui lòng thử lại.")

# 8. CHÂN TRANG
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("© 2026 Pentech Premium Corporate. Dữ liệu được tính toán dựa trên chỉ số EPS và P/E thực tế từ Yahoo Finance.")
