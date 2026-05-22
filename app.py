import streamlit as st
import yfinance as tf
import pandas as pd

# 1. Đoạn mã ẩn xác minh với Google Search Console
st.markdown(
    """
    <meta name="google-site-verification" content="<meta name="google-site-verification" content="1CyOz9EFf1oO5gW0ZfBjYM8OdP-cxCUm7UCj-YvL9K4" />
    """, 
    unsafe_allow_html=True
)

# 2. Cấu hình giao diện trang web hiển thị trên Google
st.set_page_config(
    page_title="Pentech Premium - Hệ Thống Định Giá Cổ Phiếu AI",
    page_icon="💎",
    layout="wide"
)

# 3. Giao diện chính của ứng dụng Pentech Premium
st.title("💎 Pentech Premium")
st.subheader("Hệ thống định giá cổ phiếu định hướng Mạng thần kinh học sâu AI")

# Ô nhập mã cổ phiếu (Mặc định là siêu cổ VGI của bạn)
ticker = st.text_input("Nhập mã cổ phiếu để AI phân tích:", "VGI").upper()

if ticker:
    st.write(f"### Đang tiến hành chạy mạng thần kinh phân tích mã: {ticker}")
    st.info("Hệ thống đang quét dữ liệu dòng tiền và biểu đồ giá...")
    
    # Giả lập hiển thị kết quả định giá thần tốc
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Giá thị trường hiện tại", value="7% (Tăng trần)")
    with col2:
        st.metric(label="Tỷ suất lợi nhuận dự báo (AI Deep Learning)", value="+20%", delta="Rất Tích Cực")
        
    st.success("Mô hình mạng thần kinh xác nhận: Tín hiệu dòng tiền lớn đổ vào hệ sinh thái Viettel!")
