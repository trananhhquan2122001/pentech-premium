st.markdown(
    """
    <meta name="google-site-verification" content="ĐOẠN_MÃ_BẢO_MẬT_CỦA_BẠN" />
    """, 
    unsafe_allow_html=True
)
import yfinance as yf
import pandas as pd

# 1. Cấu hình giao diện chuẩn Doanh Nghiệp
st.set_page_config(page_title="Pentech Premium", layout="wide", page_icon="💰")

# CSS để làm đẹp nút bấm và màu sắc
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 PENTECH PREMIUM: HỆ THỐNG ĐỊNH GIÁ CHIẾN LƯỢC")
st.info("Chào mừng nhà đầu tư chuyên nghiệp. Hệ thống đang sử dụng dữ liệu thời gian thực.")

# 2. Sidebar chuyên nghiệp
with st.sidebar:
    st.header("🔑 Khu vực quản trị")
    ticker = st.text_input("Nhập mã (VD: MCH.VN, FPT.VN):", "MCH.VN").upper()
    pe_target = st.slider("P/E Kỳ Vọng:", 5, 30, 15)
    margin = st.slider("Biên an toàn (%):", 10, 50, 25)
    st.divider()
    st.write("📞 **Hỗ trợ & Đăng ký VIP:** 09xx.xxx.xxx")
    st.write("💳 **Gói dịch vụ:** Premium Member")

# 3. Xử lý dữ liệu
if ticker:
    data = yf.Ticker(ticker)
    df = data.info
    price = df.get('currentPrice') or df.get('regularMarketPrice')
    eps = df.get('trailingEps', 0)
    
    if price and eps > 0:
        # Hiển thị chỉ số chính
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Giá thị trường", f"{price:,.0f} đ")
        with col2: st.metric("Lợi nhuận/CP (EPS)", f"{eps:,.0f} đ")
        with col3: st.metric("P/E hiện tại", f"{df.get('trailingPE', 0):.2f}")

        # Tính toán định giá
        val_thuc = eps * pe_target
        gia_mua = val_thuc * (1 - margin/100)
        upside = ((val_thuc / price) - 1) * 100

        st.divider()
        
        # Bảng kết quả chuyên nghiệp
        res1, res2, res3 = st.columns(3)
        res1.success(f"🎯 GIÁ TRỊ THỰC\n\n**{val_thuc:,.0f} đ**")
        res2.warning(f"🛡️ GIÁ MUA AN TOÀN\n\n**{gia_mua:,.0f} đ**")
        res3.info(f"📈 TIỀM NĂNG TĂNG TRƯỞNG\n\n**{upside:.1f} %**")

        if price <= gia_mua:
            st.balloons()
            st.success("🚀 ĐÂY LÀ ĐIỂM MUA VÀNG THEO CHIẾN LƯỢC CANSLIM & VALUE INVESTING")
    else:
        st.error("Không tìm thấy dữ liệu. Hãy đảm bảo thêm đuôi .VN (VD: VCB.VN)")
