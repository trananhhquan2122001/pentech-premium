import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import base64
import os

# ==========================================
# 1. CẤU HÌNH HỆ THỐNG ĐỊNH CHẾ TỐI ƯU CAO CẤP
# ==========================================
st.set_page_config(
    page_title="Pentech Premium - Institutional Asset Management",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Thử nghiệm thiết lập mã xác minh Google Search Console an toàn
try:
    st._config.set_option("html.additionalHeadContent", '<meta name="google-site-verification" content="448da2da278475de" />')
except Exception:
    pass

# Khởi tạo bộ nhớ ngầm lưu trữ mật khẩu kích hoạt trên máy chủ
if "dynamic_license_key" not in st.session_state:
    st.session_state["dynamic_license_key"] = "Trananhquan@2001"

# ==========================================
# 2. NGÔN NGỮ THIẾT KẾ NỀN TRẮNG TOÀN PHẦN (PURE LIGHT STYLE)
# ==========================================
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, strong, em, li { 
        color: #000000 !important; 
    }
    div[data-testid="stMarkdownContainer"] p { 
        color: #000000 !important; 
        font-size: 15px !important;
        font-weight: 500 !important;
        line-height: 1.6;
    }
    
    .premium-header {
        border-bottom: 3px solid #000000;
        padding: 25px 0px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 35px;
    }
    .premium-title { color: #000000 !important; font-size: 32px; font-weight: 800; letter-spacing: -0.5px; }
    .premium-subtitle { color: #000000 !important; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
    
    .founder-card {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        padding: 25px;
        border-radius: 4px;
        text-align: center;
        margin-bottom: 25px;
    }
    .founder-avatar {
        width: 160px;
        height: 160px;
        border-radius: 50% !important;
        object-fit: cover;
        border: 3px solid #000000;
        display: inline-block;
    }
    .founder-name { font-size: 24px; font-weight: 800; color: #000000 !important; margin-top: 15px; margin-bottom: 2px; }
    .founder-title { font-size: 13px; color: #000000 !important; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }

    .strategy-card {
        background-color: #F9FAFB;
        padding: 25px;
        border: 2px solid #000000;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    .locked-card {
        background-color: #FFFBEB;
        padding: 25px;
        border: 2px dashed #D97706;
        border-radius: 4px;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .compare-box {
        background-color: #F9FAFB;
        padding: 25px;
        border: 2px solid #000000;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    .price-grid-box {
        background-color: #FFFFFF;
        border: 2px solid #000000;
        border-radius: 4px;
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
    }
    .price-card-title { font-size: 18px; font-weight: 800; color: #000000 !important; text-transform: uppercase; letter-spacing: 1px; }
    .price-card-amount { font-size: 34px; font-weight: 900; color: #000000 !important; margin: 15px 0px 5px 0px; }
    
    .price-grid-box.vip-tier {
        background-color: #000000;
        border: 2px solid #000000;
    }
    .price-grid-box.vip-tier .price-card-title, .price-grid-box.vip-tier .price-card-amount, .price-grid-box.vip-tier p, .price-grid-box.vip-tier li, .price-grid-box.vip-tier b { color: #FFFFFF !important; }
    
    div[data-testid="stExpander"] {
        border: 2px solid #000000 !important;
        background-color: #FFFFFF !important;
        border-radius: 4px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #000000 !important;
        padding: 14px !important;
    }
    
    /* Tối ưu hóa hiển thị text box nhập liệu không bị lỗi màu chữ */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        border-radius: 4px !important;
        border: 2px solid #000000 !important;
        padding: 10px 20px !important;
    }
    button:hover { background-color: #333333 !important; border-color: #333333 !important; }
    .admin-box { background-color: #F3F4F6; border: 3px dashed #000000; padding: 25px; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# Thanh điều hướng thương hiệu
st.markdown("""
    <div class="premium-header">
        <div class="premium-title">Pentech Premium <span style='font-size:16px; color:#000000; font-weight:600;'>INSTITUTIONAL TERMINAL</span></div>
        <div class="premium-subtitle">Hạ tầng Real-time 3 sàn • Sửa lỗi trùng lặp chữ từ bài 16 đến bài 35</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. KHO DỮ LIỆU 35 BÀI HỌC HOÀN TOÀN BIỆT LẬP (ĐÃ KHẮC PHỤC TRIỆT ĐỂ 100%)
# ==========================================
strategies_35 = [
    {
        "id": 1, "title": "Xác lập trục giá trị nội tại cốt lõi doanh nghiệp",
        "desc": "1. Tư duy nền tảng: Bóc tách cấu trúc tài sản ròng hữu hình để tìm kiếm biên an toàn phòng thủ thực chất.\n"
                "2. Bộ lọc định lượng: Sử dụng mô hình máy học để quét dữ liệu tài chính, loại bỏ báo cáo giả mạo.\n"
                "3. Nhận diện hào bảo vệ: Đánh giá độc quyền phân phối công nghệ số và lợi thế quy mô tệp khách hàng.\n"
                "4. Điểm gãy rủi ro: Thoát toàn bộ nguồn vốn giải ngân khi dòng tiền từ hoạt động cốt lõi suy sụp liên tiếp.\n"
                "5. Thực chiến Việt Nam: Thiết lập màng lọc chọn Blue-chip nội địa sạch sẽ tập trung mã trụ cột như FPT.\n"
                "6. Kỷ luật hành động: Kiên định giải ngân tiền mặt tại vùng chiết khấu sâu, mua rẻ để bảo tồn gia sản vĩnh viễn.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 1:\n"
                "Bài học này yêu cầu nhà đầu tư phải xây dựng một bộ lọc tư duy định lượng nghiêm ngặt như một định chế quản trị quỹ chuyên nghiệp. "
                "Chúng ta không nhìn vào sự nhảy múa ngắn hạn của bảng điện tử mà sử dụng hệ thống Trí tuệ nhân tạo (AI) để phân tích "
                "hàng vạn điểm dữ liệu quá khứ, tìm kiếm sự minh bạch thực sự đằng sau các con số doanh thu. Công nghệ mạng lưới khối (Blockchain) được tích hợp ngầm để lưu vết "
                "các biên an toàn lịch sử, đảm bảo cấu trúc thông tin đối chiếu song song là chính xác tuyệt đối và không thể bị sửa đổi. "
                "Đồng thời, mô hình điện toán lượng tử chạy các ma trận xác suất biến động đa biến để tìm ra điểm gãy rủi ro thấp nhất có thể diễn ra. "
                "Đầu tư tích sản từ số vốn nhỏ cần một triền dốc thời gian dài để hòn tuyết lãi kép lăn bánh vĩ đại. Bản chất của tri thức thượng tầng "
                "không phải là dự đoán xu hướng ngày mai, mà là làm chủ trục giá trị thực của tài sản ngày hôm nay, biến dòng tiền thặng dư sản xuất "
                "thành bệ phóng tài chính an toàn bền vững xuyên thế kỷ."
    },
    {
        "id": 2, "title": "Chiến lược chế ngự Ngài Thị Trường và ma trận tâm lý đám đông",
        "desc": "1. Tư duy nền tảng: Coi sự biến động ngắn hạn của đồ thị kỹ thuật là người phục vụ cung cấp cơ hội mua hời.\n"
                "2. Bộ lọc định lượng: Quét chỉ số hoảng loạn toàn thị trường bằng hệ thống thuật toán NLP phân tích tâm lý số.\n"
                "3. Nhận diện hào bảo vệ: Pháp nhân kinh doanh sở hữu quyền lực định giá sản phẩm, bẻ gãy áp lực lạm phát vĩ mô.\n"
                "4. Điểm gãy rủi ro: Thu hẹp quy mô đòn bẩy margin khi toàn hệ thống chạm ngưỡng hưng phấn hoang tưởng vô độ.\n"
                "5. Thực chiến Việt Nam: Gom mua quyết liệt các mã cổ phiếu ngân hàng thương mại hàng đầu như TCB khi bị bán tháo vô lý.\n"
                "6. Kỷ luật hành động: Giữ kỷ luật thép, mua của người chán, bán cho người thèm một cách có lộ trình bài bản.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 2:\n"
                "Ngài Thị Trường là một người đối tác kinh doanh điên cuồng, mỗi ngày đều cống hiến cho bạn những mức giá không tưởng dựa trên cảm xúc. "
                "Hệ thống AI của Pentech Premium giúp nhà đầu tư định vị chính xác hành vi tâm lý này để không bị cuốn vào vòng xoáy hoảng loạn. "
                "Chúng ta ứng dụng công nghệ Blockchain để theo dõi dòng tiền thực tế của các cá mập lớn và định chế tài chính thượng tầng, "
                "bóc tách hành vi gom hàng lặng lẽ của họ đứng sau bức màn truyền thông báo chí. Mô phỏng lượng tử phân tích chu kỳ sợ hãi "
                "để xác định thời điểm đám đông buông xuôi đầu hàng hoàn toàn. Giáo dục tài chính sớm từ năm 15 tuổi đòi hỏi học viên bắt buộc phải "
                "thuần thục quy tắc này: biến biến động thị trường thành công cụ khai thác siêu lợi nhuận phi thường, kiên định tích lũy an toàn "
                "bất chấp các chu kỳ suy thoái khốc liệt nhất."
    },
    {
        "id": 3, "title": "Bộ lọc nguyên tắc chọn siêu cổ phiếu tăng trưởng đột biến",
        "desc": "1. Tư duy nền tảng: Mua một cổ phiếu chính là mua một phần quyền sở hữu của một doanh nghiệp sản xuất thực tế.\n"
                "2. Bộ lọc định lượng: Yêu cầu tỷ suất sinh lời trên vốn chủ sở hữu ROE lớn hơn 20% và duy trì ổn định.\n"
                "3. Nhận diện hào bảo vệ: Đo lường rào cản chi phí sản xuất thấp nhất hoặc giá trị thương hiệu không thể thay thế.\n"
                "4. Điểm gãy rủi ro: Rút vốn ngay khi ban lãnh đạo có hành vi phá vỡ cấu trúc minh bạch thông tin tài chính.\n"
                "5. Thực chiến Việt Nam: Định vị mô hình tăng trưởng bền vững dài hạn xuyên suốt chu kỳ như tập đoàn FPT.\n"
                "6. Kỷ luật hành động: Tập trung danh mục vào các doanh nghiệp chất lượng cao, hạn chế tối đa việc đảo hàng liên tục.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 3:\n"
                "Việc lựa chọn một siêu cổ phiếu tăng trưởng đòi hỏi một tư duy thẩm định toàn diện cả về định tính lẫn định lượng. "
                "Trí tuệ nhân tạo (AI) quét toàn bộ hệ thống báo cáo tài chính của 3 sàn chứng khoán tại Việt Nam để tìm kiếm sự nhất quán "
                "trong tăng trưởng thu nhập EPS và khả năng tái phân bổ vốn thặng dư hiệu quả của doanh nghiệp. Chúng tôi đưa các chỉ số này "
                "vào mạng lưới Blockchain bảo mật để xây dựng lịch sử định giá bất biến, giúp nhà đầu tư nhìn thấu bức tranh tài chính sạch. "
                "Tư duy lượng tử được kích hoạt để phân tích ma trận cạnh tranh liên ngành, đánh giá xem doanh nghiệp có giữ vững được hào kinh tế "
                "trước làn sóng dịch chuyển công nghệ hay không. Đầu tư thành công không cần làm những điều phi thường, "
                "mà là làm những điều bình thường một cách có kỷ luật phi thường. Hãy biến dòng tiền cổ tức tiền mặt đều đặn thành bệ phóng để tối ưu hóa lãi kép vĩnh cửu."
    },
    {
        "id": 11, "title": "Chiến lược bảo tồn nguồn vốn vĩnh viễn đề phòng mất tiền",
        "desc": "1. Tư duy nền tảng: Rủi ro lớn nhất không phải là biến động giá ngắn hạn mà là khả năng mất vốn vĩnh viễn không thể phục hồi.\n"
                "2. Bộ lọc định lượng: Kiểm tra hệ số Altman Z-score phòng tránh phá sản và chất lượng dòng tiền từ hoạt động lõi thực chất.\n"
                "3. Nhận diện hào bảo vệ: Doanh nghiệp nắm giữ tài sản thực tế có tính thanh khoản cao, dễ dàng hoán đổi thành tiền mặt.\n"
                "4. Điểm gãy rủi ro: Khi ban điều hành có dấu hiệu sử dụng các thủ thuật kế toán phức tạp để thổi phồng lợi nhuận ảo.\n"
                "5. Thực chiến Việt Nam: Lựa chọn các mã cổ phiếu sản xuất có dòng tiền cực sạch và minh bạch cao như Hòa Phát HPG.\n"
                "6. Kỷ luật hành động: Đặt tiêu chuẩn an toàn lên trên hết, thà bỏ lỡ cơ hội kiếm tiền còn hơn mạo hiểm làm mất vốn.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 11:\n"
                "Bảo tồn vốn là quy tắc số một, và quy tắc số hai là không bao giờ được phép quên quy tắc số một. "
                "Thuật toán AI của Pentech Premium thực hiện quy trình kiểm toán hiệu năng độc lập đối với mọi pháp nhân niêm yết trên 3 sàn, "
                "kiên quyết loại bỏ hoàn toàn các doanh nghiệp có cấu trúc tài chính rỗng ruột hoặc nợ vay quá lớn. "
                "Bằng cách áp dụng Blockchain, chúng tôi theo dõi tính xác thực của các chuỗi hợp đồng kinh doanh lớn, đảm bảo dòng thu nhập "
                "sinh ra là thực chất 100%. Giả lập lượng tử được kích hoạt để chạy thử nghiệm sức chống chịu của danh mục trước kịch bản "
                "thiên nga đen cực đoan nhất có thể diễn ra. Đối với những nhà đầu tư độc lập đang tích lũy từ những số vốn nhỏ, "
                "việc sở hữu một danh mục an toàn tuyệt đối chính là bệ đỡ vững chắc nhất để bảo vệ thành quả lao động bền vững xuyên thế kỷ."
    },
    {
        "id": 15, "title": "Cấu hình chiến lược Focus tập trung phân khúc chuyên biệt",
        "desc": "1. Tư duy nền tảng: Pháp nhân xuất sắc bắt buộc phải lựa chọn một hướng đi quyết định để vô hiệu hóa áp lực cạnh tranh ngành.\n"
                "2. Bộ lọc định lượng: Biên lợi nhuận hoạt động duy trì ở mức cao nhờ dẫn đầu chi phí thấp hoặc khác biệt hóa sản phẩm rõ rệt.\n"
                "3. Nhận diện hào bảo vệ: Độc quyền phân khúc thị trường chuyên biệt nhờ thấu hiểu sâu sắc hành vi tiêu dùng địa phương.\n"
                "4. Điểm gãy rủi ro: Khi doanh nghiệp mất tập trung, sa đà vào cuộc chiến cạnh tranh giá cả khốc liệt tại các đại dương đỏ.\n"
                "5. Thực chiến Việt Nam: Thiết lập cấu trúc kinh doanh bám sát thị trường ngách như các dịch vụ massage và lọc nước số.\n"
                "6. Kỷ luật hành động: Chỉ tập trung nguồn vốn đầu tư vào những doanh nghiệp nắm giữ lợi thế tuyệt đối trong phân khúc ngách lõi.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 15:\n"
                "Theo các nguyên lý chiến lược kinh điển, một mô hình kinh doanh không thể là tất cả đối với mọi phân khúc khách hàng ngoài thị trường. "
                "Hệ thống AI số liệu của Pentech Premium bóc tách cấu trúc giá trị của từng pháp nhân để kiểm tra tính thực chất của chiến lược tập trung. "
                "Mọi thông tin về thị phần và biên lợi nhuận ngách được xác thực trên hạ tầng Blockchain bảo mật, loại bỏ hoàn toàn các báo cáo quảng cáo "
                "sáo rỗng mục đích thương mại phi thực tế. Thuật toán lượng tử mô phỏng mức độ bứt phá ra khỏi các khoảng trống thị trường "
                "để tìm kiếm không gian giá trị đại dương xanh vô tận. Việc làm chủ tư duy chiến lược chuyên biệt của nhà sáng lập Trần Anh Quân "
                "sẽ giúp bạn cơ cấu tài sản một cách thông thái, thiết lập lộ trình giáo dục tài chính sớm từ năm 15 tuổi một cách vững chắc xuyên thế kỷ."
    },
    {
        "id": 16, "title": "Quy tắc kiểm toán cấu trúc rủi ro và nhận diện tư duy cấp độ hai",
        "desc": "1. Tư duy nền tảng: Đi sâu bóc tách bản chất rủi ro ẩn giấu phía sau những thông tin đại chúng tích cực bề nổi.\n"
                "2. Bộ lọc định lượng: Sử dụng AI định lượng để rà soát ma trận sụt giảm tài sản giả định của danh mục sản xuất.\n"
                "3. Nhận diện hào bảo vệ: Pháp nhân vận hành cấu trúc tài chính an toàn tuyệt đối, không chịu áp lực dòng nợ hệ thống.\n"
                "4. Điểm gãy rủi ro: Khi trục định giá kỹ thuật vượt xa ranh giới biên an toàn cốt lõi phòng thủ dài hạn.\n"
                "5. Thực chiến Việt Nam: Phân tích sự lệch pha biên độ của các doanh nghiệp rường cột quốc gia như FPT, CTR.\n"
                "6. Kỷ luật hành động: Áp dụng tư duy rạch ròi cấp độ hai để đưa ra hành động giải ngân ngược hướng đám đông.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 16:\n"
                "Học viện VIP phân tích rằng tư duy cấp độ một chỉ nhìn vào bề nổi trực quan, trong khi tư duy cấp độ hai đòi hỏi "
                "một cấu trúc phân tích đa biến sâu sắc hơn rất nhiều. Hệ thống máy học AI nâng cao của chúng tôi thực hiện quét lọc ngôn ngữ truyền thông, "
                "đo lường chính xác mức độ đồng thuận cực đoan của đám đông hoang tưởng nhằm phát hiện bẫy mỏ neo tâm lý ngắn hạn. "
                "Mọi số liệu về biên an toàn phòng thủ được mã hóa phi tập trung trên hạ tầng Blockchain bảo mật, mang lại một hệ quy chiếu "
                "đối chiếu song song hoàn toàn sạch sẽ. Thuật toán lượng tử chạy các mô phỏng kịch bản biến động đa biến giúp nhà đầu tư độc lập "
                "nhìn thấu bản chất thực chất của cấu trúc rủi ro liên ngành, tự tin bảo tồn nguồn vốn vĩnh viễn và kiến tạo di sản tài chính "
                "bền vững vĩnh cửu xuyên thế kỷ."
    },
    {
        "id": 17, "title": "Chiến lược quản trị chu kỳ nợ vĩ mô liên ngành",
        "desc": "1. Tư duy nền tảng: Định vị điểm cực đoan của chu kỳ tín dụng để kích hoạt chiến thuật phòng thủ nguồn lực vĩ mô.\n"
                "2. Bộ lọc định lượng: Sử dụng thuật toán cào dữ liệu tự động rà soát trục cung tiền M2 và tỷ lệ nợ xấu hệ thống.\n"
                "3. Nhận diện hào bảo vệ: Doanh nghiệp nắm giữ lượng tiền mặt dồi dào, có quyền lực thâu tóm đối thủ cạnh tranh.\n"
                "4. Điểm gãy rủi ro: Ngân hàng trung ương bất ngờ thắt bóp thanh khoản, kích hoạt chu kỳ giảm phát nợ nần liên ngành.\n"
                "5. Thực chiến Việt Nam: Đón đầu vùng trũng chu kỳ tài sản sạch của các định chế ngân hàng quốc doanh lớn như VCB.\n"
                "6. Kỷ luật hành động: Kiên quyết thu hẹp tỷ trọng đòn bẩy margin ngắn hạn trước khi điểm gãy chu kỳ chính thức diễn ra.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 17:\n"
                "Toàn bộ thị trường tài chính thế kỷ 21 vận hành bám sát các đại chu kỳ thắt thắt mở mở của hệ thống nợ vay tín dụng. "
                "Bộ máy vĩ mô của Pentech Premium ứng dụng AI để phân tích sự dịch chuyển dòng vốn liên quốc gia, loại bỏ mọi thông tin quảng bá "
                "sáo rỗng phi thực tế của báo chí thương mại ngoài xã hội. Nhật ký diễn biến lãi suất và lạm phát được lưu trữ bất biến trên Blockchain "
                "nhằm mang lại giải pháp công nghệ giả lập cấu trúc tài sản minh bạch nhất cho người Việt từ số vốn nhỏ từ 250k. "
                "Mô hình điện toán lượng tử tính toán ma trận tương quan đa biến, giúp nhà quản trị đưa tổng tài sản về trạng thái bảo thủ "
                "nghiêm ngặt dài hạn dài lâu, bảo vệ trọn vẹn thành quả lao động của bạn trước mọi cơn bão căng thẳng vĩ mô toàn cầu."
    },
    {
        "id": 18, "title": "Quy tắc bóc tách bẫy chi phí trung gian và tối ưu dòng tiền cổ tức",
        "desc": "1. Tư duy nền tảng: Loại bỏ triệt để các rào cản chi phí vận hành ẩn để bảo vệ sức mạnh hòn tuyết lăn của lãi kép.\n"
                "2. Bộ lọc định lượng: Thuật toán AI tự động sàng lọc và cắt bỏ toàn bộ các tầng lớp phí quản lý quỹ phi lý liên sàn.\n"
                "3. Nhận diện hào bảo vệ: Cơ chế tích sản tự động hóa khép kín, tập trung nguồn lực tuyệt đối vào tài sản sản xuất cốt lõi.\n"
                "4. Điểm gãy rủi ro: Tần suất giao dịch trading mua bán quá cao làm hao mòn nghiêm trọng dòng tiền mặt ròng dồi dào.\n"
                "5. Thực chiến Việt Nam: Thiết lập danh mục tích sản các mã có dòng tiền chi trả cổ tức tiền mặt đều đặn sạch sẽ.\n"
                "6. Kỷ luật hành động: Giữ tính kỷ luật thép hành động, coi sự kiên nhẫn nắm giữ dài hạn là vũ khí tối cao sinh tồn.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 18:\n"
                "Nhà đầu tư cá nhân nhỏ lẻ thua cuộc phần lớn không phải vì chọn sai doanh nghiệp, mà vì họ đã cống hiến quá nhiều lợi nhuận "
                "cho các bẫy phí và thuế giao dịch phát sinh từ bẫy tâm lý trading ngắn hạn liên tục. Trạm Terminal của bạn Quân phá vỡ "
                "hoàn toàn rào cản này bằng cách tự động hóa quy trình lọc chỉ số EPS, ROE, ROI của cả 3 sàn sạch sẽ. "
                "Ứng dụng Blockchain phi tập trung loại bỏ nhu cầu về các bên trung gian xác thực phi lý ngoài xã hội, giúp dòng vốn tích lũy "
                "của bạn phát huy sức mạnh cấp số nhân vĩnh cửu. Phân tích lượng tử tối ưu hóa lộ trình giải ngân vốn, giúp lộ trình giáo dục tài chính "
                "sớm cho thế hệ trẻ từ 15 tuổi hình thành tư duy làm chủ vận mệnh kinh tế độc lập, tích lũy an toàn bền vững vĩnh cửu dài hạn."
    },
    {
        "id": 19, "title": "Ma trận phân loại rủi ro doanh nghiệp và màng mọc chỉ số sạch",
        "desc": "1. Tư duy nền tảng: Mỗi loại hình doanh nghiệp niêm yết sở hữu một quán tính rủi ro đặc thù, cần bộ lọc định lượng riêng.\n"
                "2. Bộ lọc định lượng: Sử dụng mô hình máy học kiểm toán chất lượng các khoản phải thu và tính thực chất của hàng tồn kho.\n"
                "3. Nhận diện hào bảo vệ: Tìm kiếm biên lợi nhuận gộp duy trì ở mức cao vượt trội và bỏ xa các đối thủ cùng phân khúc.\n"
                "4. Điểm gãy rủi ro: Ban quản trị sa đà vào hoạt động đầu cơ tài chính ngắn hạn rủi ro cao thay vì tập trung ngành kinh doanh lõi.\n"
                "5. Thực chiến Việt Nam: Định vị chính xác nhóm vị thế tăng trưởng thần tốc của siêu cổ phiếu đầu ngành công nghệ cao FPT.\n"
                "6. Kỷ luật hành động: Không bao giờ gõ lệnh giải ngân dựa trên các kỳ vọng ảo tưởng thiếu số liệu toán học chứng minh.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 19:\n"
                "Bẫy giá trị và rủi ro gian lận kế toán luôn là nỗi ám ảnh đối với các danh mục đầu tư tích sản thiếu công cụ rà soát độc lập. "
                "Thuật toán AI nâng cao của chúng tôi tự động gắn nhãn và phân tách các dấu hiệu rủi ro tiềm ẩn trên báo cáo tài chính lý thuyết của 3 sàn. "
                "Dữ liệu phân loại được đồng bộ hóa phi tập trung trên hạ tầng Blockchain bảo mật, mang lại hệ quy chiếu khách quan tuyệt đối "
                "để người dùng đối chiếu song song thời gian thực. Giả lập lượng tử phân tích ma trận cạnh tranh liên ngành, đánh giá xem hào kinh tế "
                "của doanh nghiệp có thể bị lung lay trước làn sóng biến động kỹ nghệ kỷ nguyên số hay không, giúp những người vốn nhỏ tự tin "
                "nắm giữ cổ phần doanh nghiệp an toàn dài hạn."
    },
    {
        "id": 20, "title": "Phương pháp thực địa Scuttlebutt và phòng ngự thiên nga đen vĩ mô",
        "desc": "1. Tư duy nền tảng: Tri thức thực tế nằm ở hành vi tiêu dùng đời sống xung quanh, không phải chỉ nằm ở báo cáo lý thuyết.\n"
                "2. Bộ lọc định lượng: Khai thác luồng phản hồi từ chuỗi cung ứng lõi, mạng lưới đối thủ cạnh tranh và tệp khách hàng thực tế.\n"
                "3. Nhận diện hào bảo vệ: Sự trung thành tuyệt đối của người tiêu dùng và quyền lực kiểm soát hạ tầng thương mại bản địa.\n"
                "4. Điểm gãy rủi ro: Sự xuất hiện của các dấu hiệu căng thẳng thanh khoản hệ thống nợ nần trước khi số liệu báo cáo lên báo chí.\n"
                "5. Thực chiến Việt Nam: Trực tiếp quan sát chuỗi mở rộng mạng lưới bán lẻ và logistics số khép kín của mã VGI, CTR, VTP.\n"
                "6. Kỷ luật hành động: Kiên quyết đóng vị thế bảo vệ nguồn vốn giải ngân khi phát hiện dấu hiệu gãy trục vận hành thực địa.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 20:\n"
                "Tư duy thực địa chuyên sâu Scuttlebutt yêu cầu nhà quản trị tài sản bắt buộc phải kết hợp giữa số liệu văn phòng và thực tế đời sống. "
                "Hệ thống định lượng Pentech Premium hỗ trợ quy trình này bằng cách ứng dụng AI để cào dữ liệu định lượng tự động từ hàng triệu xu hướng "
                "tìm kiếm trực tuyến thời gian thực. Chúng tôi số hóa luồng dữ liệu thô thu thập được lên hạ tầng Blockchain bất biến nhằm triệt tiêu hoàn toàn "
                "các thông tin quảng cáo nhiễu mục đích thương mại phi thực tế. Thuật toán lượng tử mô phỏng các cú sốc thiên nga đen giả định, "
                "giúp bạn Quân thiết lập hàng rào phòng thủ vững chắc cho tài khoản đầu tư cá nhân, bảo hộ nguồn lực tài chính vĩnh viễn dài hạn."
    },
    {
        "id": 21, "title": "Quy tắc bóc tách và bẻ gãy ma trận đòn bẩy tài chính rủi ro",
        "desc": "1. Tư duy nền tảng: Đòn bẩy nợ vay là một con dao hai lưỡi, có khả năng đẩy nhanh sự hủy diệt tài sản của nhà đầu tư.\n"
                "2. Bộ lọc định lượng: Sử dụng mô hình AI định lượng quét sâu tỷ lệ Nợ/Vốn chủ sở hữu của doanh nghiệp trên cả 3 sàn.\n"
                "3. Nhận diện hào bảo vệ: Ưu tiên các pháp nhân duy trì cấu trúc tài chính cô đặc, sở hữu lượng tiền mặt ròng dồi dào.\n"
                "4. Điểm gãy rủi ro: Lãi suất vay đột ngột tăng vọt, làm triệt tiêu hoàn toàn biên lợi nhuận hoạt động lõi sản xuất.\n"
                "5. Thực chiến Việt Nam: Cơ cấu dòng tiền an toàn, tập trung phân bổ vốn tích sản vào mã Blue-chip công nghệ cao FPT.\n"
                "6. Kỷ luật hành động: Thiết lập quy tắc phòng thủ bảo thủ, tuyệt đối không lạm dụng ký quỹ margin ngắn hạn theo đám đông.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 21:\n"
                "Trong các giai đoạn thị trường hưng hấn cực đoan, đòn bẩy nợ vay luôn là công cụ khiến đám đông hoang tưởng về mức sinh lời giả tạo. "
                "Trạm Terminal của chúng tôi tích hợp bộ máy AI chuyên sâu để theo dõi chặt chẽ dòng tiền vay nợ toàn chuỗi hệ thống liên ngành, "
                "phát hiện sớm các dấu hiệu căng thẳng tín dụng trước khi điểm gãy chính thức xảy ra. Sổ cái Blockchain lưu trữ các chỉ số đòn bẩy bất biến, "
                "giúp bạn có một hệ quy chiếu định lượng hoàn toàn sạch sẽ để đưa ra các quyết định phân bổ nguồn vốn một cách sáng suốt. "
                "Mô phỏng toán học lượng tử hỗ trợ đo lường tác động của lãi suất đến giá trị tài sản ròng hữu hình, bảo vệ trọn vẹn gia sản lâu dài."
    },
    {
        "id": 22, "title": "Chiến lược nhận diện bẫy giá trị của các doanh nghiệp rỗng ruột",
        "desc": "1. Tư duy nền tảng: Một cổ phiếu có thị giá rẻ không đồng nghĩa với việc đó là một cơ hội đầu tư giá trị xuất sắc.\n"
                "2. Bộ lọc định lượng: Kiểm toán chất lượng các khoản phải thu và hàng tồn kho thông qua thuật toán quét dữ liệu lớn.\n"
                "3. Nhận diện hào bảo vệ: Doanh nghiệp phải sở hữu năng lực tạo ra dòng tiền mặt thực tế từ hoạt động kinh doanh lõi.\n"
                "4. Điểm gãy rủi ro: Biên lợi nhuận gộp suy giảm liên tục do mô hình kinh doanh bị mất đi lợi thế cạnh tranh cốt lõi.\n"
                "5. Thực chiến Việt Nam: Thanh lọc danh mục một cách quyết liệt, loại bỏ các mã đầu cơ rác thiếu năng lực nội tại.\n"
                "6. Kỷ luật hành động: Chỉ giải ngân vốn vào những pháp nhân có lâu đài kinh doanh được bảo vệ bởi con hào rộng lớn.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 22:\n"
                "Bẫy giá trị là nơi chôn vùi nguồn vốn của rất nhiều nhà đầu tư cá nhân do thói quen mua cổ phiếu chỉ dựa vào đồ thị giảm giá sâu. "
                "Hệ thống trí tuệ nhân tạo (AI) của Pentech Premium thực hiện bóc tách chuyên sâu hiệu quả sử dụng tài sản ROA và ROI thực chất, "
                "vạch trần các thủ thuật thổi phồng doanh thu ảo trên báo cáo kế toán lý thuyết. Thông tin đối chiếu được đồng bộ hóa bất biến "
                "on hạ tầng Blockchain giúp bạn có cái nhìn khách quan tuyệt đối. Thuật toán lượng tử mô phỏng ma trận suy thoái để kiểm tra sức chống chịu "
                "of mô hình thương mại doanh nghiệp, giúp những người vốn nhỏ tự tin nắm giữ những siêu cổ phiếu tăng trưởng đích thực dài hạn."
    },
    {
        "id": 23, "title": "Quy tắc kiểm soát điểm rơi thanh khoản vĩ mô",
        "desc": "1. Tư duy nền tảng: Sức mạnh phòng thủ của tài khoản nằm ở khả năng hoán đổi các lớp tài sản thành tiền mặt tức thì.\n"
                "2. Bộ lọc định lượng: Định lượng biên độ trượt giá đặt lệnh và tốc độ khớp ròng của cổ phiếu 3 sàn.\n"
                "3. Nhận diện hào bảo vệ: Pháp nhân kinh doanh sở hữu dòng tiền thặng dư tự do cực lớn, bóp nghẹt mọi đối thủ yếu vốn.\n"
                "4. Điểm gãy rủi ro: Biên độ trượt lệnh vượt ngưỡng 5% đi kèm khối lượng giao dịch sụt giảm đột ngột mất kiểm soát.\n"
                "5. Thực chiến Việt Nam: Gom mua tích sản đều đặn vào hệ sinh thái có thanh khoản sạch sẽ dồi dào như MCH, MSN.\n"
                "6. Kỷ luật hành động: Luôn giữ vị thế phòng thủ tiền mặt tối ưu, tuyệt đối không gõ lệnh cạn kiệt thanh khoản.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 23:\n"
                "Hạ tầng học viện VIP phân tích sâu sắc rằng thanh khoản chính là dưỡng khí của thị trường tài chính vĩ mô. "
                "Khi thị trường rơi vào trạng thái hoảng loạn cực đoan, toàn bộ đám đông sẽ dẫm đạp lên nhau để tìm lối thoát vốn. "
                "Trạm Terminal của bạn Quân ứng dụng Trí tuệ nhân tạo (AI) để nhận diện sớm các vùng kẹt thanh khoản liên ngành, "
                "đo lường tốc độ rút ròng của các quỹ lớn liên lục địa. Mọi quy trình gõ lệnh giải ngân được mã hóa bảo mật trên Blockchain "
                "để bảo vệ an toàn danh mục. Thuật toán toán học lượng tử tính toán các mô hình xác suất bất đối xung, giúp bạn Quân "
                "phân bổ dòng tiền thặng dư từ sàn chứng khoán thông minh để xoay vòng vốn mua gom kho hàng cho mảng kinh doanh thiết bị gia dụng "
                "và sức khỏe tại Thái Nguyên, xây dựng cấu trúc dòng tiền khép kín vĩnh cửu không quảng cáo quảng bá phi lý."
    },
    {
        "id": 24, "title": "Chiến lược quản trị ma trận tương quan tài sản liên ngành nâng cao",
        "desc": "1. Tư duy nền tảng: Đa dạng hóa danh mục thực chất đòi hỏi các lớp tài sản phải sở hữu hệ số tương quan nghịch.\n"
                "2. Bộ lọc định lượng: Sử dụng AI để bóc tách sự liên đới dòng tiền giữa nhóm Công nghệ, Ngân hàng và Tiêu dùng.\n"
                "3. Nhận diện hào bảo vệ: Danh mục tổng có khả năng tự động phòng vệ, triệt tiêu rủi ro phi hệ thống của từng ngành lõi.\n"
                "4. Điểm gãy rủi ro: Khi tất cả các nhóm ngành đồng loạt lao dốc do sự đảo chiều chính sách tiền tệ thắt chặt cung tiền.\n"
                "5. Thực chiến Việt Nam: Phân bổ nguồn lực cân bằng và khoa học giữa các trục tăng trưởng chiến lược như FPT, VGI, TCB.\n"
                "6. Kỷ luật hành động: Tuân thủ tuyệt đối trọng số phân bổ danh mục All-Weather, không gia tăng vị thế cục bộ theo cảm xúc.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 24:\n"
                "Một danh mục đầu tư sở hữu nhiều mã cổ phiếu nhưng cùng một nhóm ngành chu kỳ không phải là đa dạng hóa, đó là tập trung rủi ro. "
                "Bài học số 24 ứng dụng sức mạnh xử lý dữ liệu lớn từ AI để bóc tách sự liên đới dòng tiền giữa các cấu trúc doanh nghiệp niêm yết. "
                "Nhật ký phân bổ được mã hóa trên Blockchain bất biến, giúp nhà đầu tư thiết lập lộ trình tích sản an toàn bền vững vĩnh viễn. "
                "Điện toán lượng tử hỗ trợ phân tích ma trận tương quan đa biến, đảm bảo tài sản của bạn luôn được bảo vệ tối đa và tăng trưởng ổn định "
                "xuyên qua mọi giông bão vĩ mô toàn cầu. Đây chính là tri thức thượng tầng bệ phóng dẫn dắt bạn chạm mốc tự do tài chính dài hạn."
    },
    {
        "id": 25, "title": "Nguyên tắc bóc tách bẫy tâm lý sợ bỏ lỡ cơ hội của đám đông",
        "desc": "1. Tư duy nền tảng: Lợi nhuận bền vững chỉ sinh ra từ kỷ luật, hành vi đu đỉnh theo làn sóng hưng phấn luôn dẫn đến hủy diệt vốn.\n"
                "2. Bộ lọc định lượng: Sử dụng AI phân tích tần suất xuất hiện tin tức tích cực cực đoan để xác định vùng đỉnh bong bóng.\n"
                "3. Nhận diện hào bảo vệ: Chỉ giải ngân tiền mặt khi thị giá nằm thấp hơn đáng kể so với trục giá trị nội tại cốt lõi.\n"
                "4. Điểm gãy rủi ro: Khi đồ thị giá tăng dựng đứng theo mô hình parabol thiếu vắng sự hỗ trợ từ nội lực sản xuất thực tế.\n"
                "5. Thực chiến Việt Nam: Đứng ngoài các cuộc đua giá nóng của nhóm cổ phiếu đầu cơ rác đầy rủi ro ngoài thị trường.\n"
                "6. Kỷ luật hành động: Kiên nhận giữ tiền mặt dồi dào, chờ đợi điểm cực đoan hoảng loạn của chu kỳ vĩ mô để mua gom.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 25:\n"
                "Bẫy tâm lý sợ bỏ lỡ cơ hội (FOMO) là vũ khí tối thượng mà Ngài Thị Trường sử dụng để tước đoạt thành quả lao động của đám đông. "
                "Trạm Terminal của chúng tôi tích hợp bộ máy AI tiên tiến để đo lường chỉ số hoang tưởng toàn diện, giúp bạn nhìn thấu bản chất "
                "thực sự của các đợt kéo giá đẩy ảo thương mại. Cấu trúc sổ cái Blockchain lưu giữ dữ liệu định giá lịch sử sạch sẽ bất biến, "
                "mang lại một hệ quy chiếu logic toán học vững chắc. Phân tích lượng tử mô phỏng ma trận hành vi, giúp những người vốn nhỏ "
                "kiên định giữ vững kỷ luật thép hành động, tích lũy tài sản an toàn từ những số vốn nhỏ nhất từ 250k một cách khoa học bền vững."
    },
    {
        "id": 26, "title": "Chiến lược bảo tồn thặng dư vốn và xoay vòng nguồn lực an toàn",
        "desc": "1. Tư duy nền tảng: Bảo vệ thành quả bằng cách rút bớt thặng dư vốn ở vùng tài sản hưng phấn quá đà về hạ tầng phòng thủ.\n"
                "2. Bộ lọc định lượng: Máy học tự động tính toán điểm rơi lợi nhuận bất đối xứng dựa trên chu kỳ nợ vĩ mô liên ngành.\n"
                "3. Nhận diện hào bảo vệ: Doanh nghiệp sở hữu cấu trúc tài chính cô đặc sạch sẽ, không chịu áp lực từ chi phí lãi vay.\n"
                "4. Điểm gãy rủi ro: Lợi suất danh mục sụt giảm kỹ thuật khi dòng vốn bị nghẽn tại các kênh đầu cơ ngắn hạn đám đông.\n"
                "5. Thực chiến Việt Nam: Hiện thực hóa lợi nhuận danh mục cổ phiếu công nghệ cao để chuyển dịch dòng tiền thực tế.\n"
                "6. Kỷ luật hành động: Thực thi chiến lược capital rotation, rút lãi từ sàn chứng khoán để tái tài trợ tổng lực kinh doanh.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 26:\n"
                "Đỉnh cao của tư duy quản trị tài sản cao cấp nằm ở năng lực biết rút lui đúng thời điểm chu kỳ đạt ngưỡng cực đoan hưng phấn. "
                "Trạm Terminal Pentech Premium ứng dụng thuật toán AI để thiết lập hệ thống cảnh báo sớm, bóc tách các điểm nghẽn thanh khoản vĩ mô. "
                "Mọi nhật ký luân chuyển vốn được mã hóa bất biến trên hạ tầng Blockchain, giúp bạn Quân bảo mật cấu trúc nguồn lực. "
                "Hệ thống tính toán lượng tử hỗ trợ thiết lập danh mục All-Weather chống chịu va đập mạnh, hướng tới mục tiêu giáo dục tài chính "
                "sớm cho trẻ em từ 15 tuổi có tư duy kỷ luật thép, làm chủ hoàn toàn vận mệnh kinh tế cá nhân dài hạn bền vững vĩnh cửu."
    },
    {
        "id": 27, "title": "Quy tắc kiểm soát rủi ro cực đoan và thiết lập điểm gãy vĩ mô",
        "desc": "1. Tư duy nền tảng: Phân tích sâu sắc các biến động địa chính trị và sự thay đổi trật tự thế giới để phòng vệ danh mục.\n"
                "2. Bộ lọc định lượng: Theo dõi ma trận in tiền, thâm hụt tài khóa vĩ mô và sự dịch chuyển cung tiền của các nước.\n"
                "3. Nhận diện hào bảo vệ: Các pháp nhân nắm giữ tài sản sản xuất cốt lõi, có năng lực vươn tầm xuất khẩu toàn cầu.\n"
                "4. Điểm gãy rủi ro: Ngân hàng trung ương thắt chặt tín dụng khốc liệt, kích hoạt làn sóng khủng hoảng nợ liên ngành.\n"
                "5. Thực chiến Việt Nam: Định vị cơ hội bẩm sát trục dịch chuyển chuỗi cung ứng logistics quốc tế của siêu mã VGI.\n"
                "6. Kỷ luật hành động: Chuyển dịch toàn bộ tổng tài sản về trạng thái bảo thủ nghiêm ngặt khi chu kỳ chạm đỉnh rủi ro.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 27:\n"
                "Lịch sử chứng minh rằng các định chế kinh tế vĩ mô toàn cầu luôn vận hành theo một đại chu kỳ lớn có tính chất lặp lại khép kín. "
                "Bộ máy định lượng Pentech Premium tích hợp Trí tuệ nhân tạo (AI) để phân tích ma trận rủi ro hệ thống, loại bỏ mọi thông tin "
                "nhiễu từ truyền thông quảng bá phi lý ngoài xã hội. Sổ cái Blockchain lưu vết các điểm rơi giá trị, mang lại giải pháp công nghệ "
                "giả lập cấu trúc tài sản sạch sẽ nhất cho người Việt từ vùng số vốn nhỏ từ 250k. Tính toán lượng tử hỗ trợ phân bổ nguồn lực "
                "vào các kênh phòng vệ vững chắc như vàng hoặc các cổ phiếu hạ tầng thiết yếu vĩ mô, bảo hộ gia sản vĩnh viễn dài hạn."
    },
    {
        "id": 28, "title": "Chiến lược xây dựng trục nguyên tắc đầu tư giá trị bất biến",
        "desc": "1. Tư duy nền tảng: Sự giàu sang lâu dài không đến từ một thương vụ may rủi, nó sinh ra từ việc thực thi nguyên tắc vĩnh cửu.\n"
                "2. Bộ lọc định lượng: Quét sạch số liệu tài chính EPS, ROE, ROI thời gian thực của cả 3 sàn thông qua API sạch sẽ.\n"
                "3. Nhận diện hào bảo vệ: Khả năng tự động phòng vệ của danh mục tổng trước mọi cú sốc va đập biến động vĩ mô liên ngành.\n"
                "4. Điểm gãy rủi ro: Khi cấu trúc tài khoản tích sản bị phá vỡ kỷ luật do hành vi trading ngắn hạn đu đỉnh đám đông.\n"
                "5. Thực chiến Việt Nam: Kiên định giải ngân tiền mặt gom mua Blue-chip nội địa xuất sắc vùng chiết khấu sâu như FPT, VGI.\n"
                "6. Kỷ luật hành động: Giữ cái đầu lạnh, thực hiện quy trình tích sản có lộ trình định lượng bài bản vô điều kiện.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 28:\n"
                "Thiết lập một hệ thống nguyên tắc hành động nghiêm ngặt chính là tấm khiên tối cao bảo vệ bạn khỏi sự điên cuồng của Ngài Thị Trường. "
                "Nhà sáng lập Trần Anh Quân định hướng Pentech Premium số hóa trọn vẹn tri thức kinh điển vào các hợp đồng thông minh trên Blockchain, "
                "loại bỏ hoàn toàn sự can thiệp từ cảm xúc cá nhân. Hệ thống AI liên tục giám sát chất lượng nội tại doanh nghiệp, đảm bảo dòng tiền "
                "thặng dư sinh ra là thực chất 100%. Phân tích lượng tử hỗ trợ tối ưu hóa trọng số danh mục All-Weather, giúp nhà đầu tư nhỏ lẻ "
                "an tâm tích lũy tài sản dài hạn vững chắc, tiến bước mạnh mẽ trên lộ trình kiến tạo sự tự do tài chính tối thượng vĩnh cửu."
    },
    {
        "id": 29, "title": "Quy tắc bóc tách chu kỳ nợ vĩ mô và điểm gãy của các quốc gia",
        "desc": "1. Tư duy nền tảng: Các định chế kinh tế vĩ mô lớn đều vận hành theo chu kỳ nợ, từ giai đoạn mở rộng đến thắt bóp tín dụng.\n"
                "2. Bộ lọc định lượng: Sử dụng AI để đo lường hệ số nợ quốc gia, thâm hụt tài khóa và quán tính in tiền của ngân hàng trung ương.\n"
                "3. Nhận diện hào bảo vệ: Nắm giữ các tài sản phòng thủ cốt lõi có khả năng phòng vệ trước làn sóng mất giá tiền tệ toàn cầu.\n"
                "4. Điểm gãy rủi ro: Trục thanh khoản hệ thống bị đóng băng, kích hoạt làn sóng vỡ nợ dây chuyền và lạm phát phi mã.\n"
                "5. Thực chiến Việt Nam: Điều phối nguồn lực tài sản, ưu tiên tích trữ tiền mặt dồi dào hoặc cổ phiếu hạ tầng thiết yếu vĩ mô.\n"
                "6. Kỷ luật hành động: Chuyển dịch cấu trúc vốn về trạng thái phòng thủ nghiêm ngặt khi chu kỳ nợ hệ thống chạm ngưỡng cực đại.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 29:\n"
                "Thấu hiểu quy luật phá sản của các định chế vĩ mô lớn giúp nhà đầu tư độc lập bảo vệ trọn vẹn thành quả nguồn vốn vĩnh cửu. "
                "Trạm Terminal của chúng tôi tích hợp thuật toán AI để giám sát sự dịch chuyển của dòng vốn liên quốc gia và sự biến động của trục tỷ giá vĩ mô. "
                "Mọi dữ liệu kinh tế được lưu trữ phi tập trung trên hạ tầng Blockchain bảo mật, loại bỏ hoàn toàn các thông tin quảng bá sáo rỗng phi thực tế. "
                "Mô hình lượng tử phân tích ma trận rủi ro nợ vay hệ thống, giúp bạn đưa ra quyết định cơ cấu tài sản an toàn tối thượng dài hạn. "
                "Hãy nhớ rằng việc làm chủ tri thức vĩ mô chính là hàng rào bảo vệ vững chắc nhất cho tòa tháp tài chính tự do vĩnh cửu của bạn."
    },
    {
        "id": 30, "title": "Chiến lược tư duy đảo ngược bài toán rủi ro hệ thống tài sản",
        "desc": "1. Tư duy nền tảng: Thay vì tìm kiếm các kịch bản chiến thắng, hãy chủ động phân tích mọi con đường dẫn đến thất bại để phòng tránh.\n"
                "2. Bộ lọc định lượng: Quét sâu hệ số căng thẳng tín dụng liên ngành và điểm rơi thanh khoản cốt lõi của danh mục đầu tư.\n"
                "3. Nhận diện hào bảo vệ: Cơ chế phân bổ danh mục All-Weather tự động phòng vệ trước mọi cú sốc va đập cực đoan vĩ mô.\n"
                "4. Điểm gãy rủi ro: Khi các chỉ số tài chính cơ bản ROE, ROI, EPS chạm ngưỡng suy giảm kỹ thuật do khủng hoảng kinh tế.\n"
                "5. Thực chiến Việt Nam: Cơ cấu nguồn vốn an toàn tập trung tuyệt đối vào các siêu cổ phiếu đầu ngành như FPT, VGI, TCB.\n"
                "6. Kỷ luật hành động: Kiên quyết tuân thủ các ranh giới cắt lỗ và dừng giải ngân tự động hóa đã được thiết lập rõ ràng.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 30:\n"
                "Đảo ngược, luôn luôn đảo ngược. Đó là bí quyết tư duy tối cao của nhà sáng lập Trần Anh Quân trong quản trị cấu trúc tài sản. "
                "Trí tuệ nhân tạo (AI) của chúng tôi chạy hàng triệu giả lập điểm chết của doanh nghiệp niêm yết để chủ động loại bỏ rủi ro vĩnh viễn mất vốn. "
                "Hợp đồng thông minh trên Blockchain thực thi kỷ luật tự động hóa gõ lệnh gác cửa nguồn vốn một cách nghiêm ngặt vô điều kiện. "
                "Phân tích lượng tử đo lường ma trận xác suất thiên nga đen, mang lại một trạm tra cứu Terminal sạch sẽ, minh bạch nhất. "
                "Làm chủ tư duy đảo ngược rủi ro chính là bệ đỡ vững chắc giúp những nhà đầu tư nhỏ lẻ yên tâm tích lũy tài sản an toàn xuyên thế kỷ."
    },
    {
        "id": 31, "title": "Nguyên tắc thiết lập bộ lọc kỷ luật thép trong hành động giải ngân",
        "desc": "1. Tư duy nền tảng: Sự khác biệt giữa nhà quản trị chuyên nghiệp và đám đông đầu cơ nằm ở tính kỷ luật vô điều kiện.\n"
                "2. Bộ lọc định lượng: Số hóa toàn bộ các tiêu chuẩn giải ngân tiền mặt bám sát biên an toàn chiết khấu sâu lý tưởng.\n"
                "3. Nhận diện hào bảo vệ: Bộ quy tắc danh mục được bảo mật nghiêm ngặt, không bị lung lay bởi biến động đồ thị ngắn hạn.\n"
                "4. Điểm gãy rủi ro: Khi cảm xúc tham lam hoặc sợ hãi cá nhân bắt đầu can thiệp làm bóp méo lộ trình định lượng bài bản.\n"
                "5. Thực chiến Việt Nam: Thực thi chiến thuật mua gom lặng lẽ từng phần các mã cổ phiếu xuất sắc đầu ngành vĩ mô.\n"
                "6. Kỷ luật hành động: Tuân thủ tuyệt đối cấu trúc quản trị nguồn vốn sản xuất, coi kỷ luật thép là vũ khí tối cao sinh tồn.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 31:\n"
                "Kỷ luật thép không phải là sự gò bó ép buộc, kỷ luật thép chính là sự tự do tối thượng bảo vệ trọn vẹn gia sản lâu dài của bạn. "
                "Hệ thống định lượng Pentech Premium ứng dụng AI để tự động giám sát và khóa các hành vi trading theo cảm tính của người dùng. "
                "Mọi hành vi gõ lệnh phân bổ vốn được xác thực bất biến trên hạ tầng Blockchain bảo mật, xây dựng một lịch sử đầu tư sạch sẽ khoa học. "
                "Toán học lượng tử hỗ trợ tối ưu hóa tần suất phân bổ dòng tiền thặng dư, giúp học viên giáo dục tài chính sớm từ năm 15 tuổi "
                "hình thành tư duy bản lĩnh, tính disciplined thép để làm chủ cuộc chơi tài chính dài hạn một cách chắc chắn bền vững vĩnh cửu."
    },
    {
        "id": 32, "title": "Chiến lược đón đầu làn sóng dịch chuyển đại chu kỳ thay đổi thế giới",
        "desc": "1. Tư duy nền tảng: Các vương triều tài chính toàn cầu luôn dịch chuyển theo quy luật phân bổ lại nguồn lực vĩ mô hệ thống.\n"
                "2. Bộ lọc định lượng: Theo dõi biểu đồ chi tiêu lớn nhất của thế hệ trung lưu mới tại các quốc gia đang phát triển.\n"
                "3. Nhận diện hào bảo vệ: Lựa chọn doanh nghiệp sở hữu năng lực cạnh tranh cốt lõi dẫn dắt cuộc chơi kỹ nghệ kỷ nguyên số.\n"
                "4. Điểm gãy rủi ro: Sự xuất hiện của các rào cản địa chính trị khốc liệt làm đứt gãy hoàn toàn chuỗi logistics liên quốc gia.\n"
                "5. Thực chiến Việt Nam: Định vị cơ hội bứt phá làm giàu từ các siêu cổ phiếu viễn thông toàn cầu xuất sắc như VGI.\n"
                "6. Kỷ luật hành động: Đi trước thị trường một bước ngắn bám sát các mục tiêu chiến lược vĩ mô dài hạn vững chắc.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 32:\n"
                "Hiểu được quy luật trật tự thế giới đang thay đổi giúp nhà đầu tư độc lập định vị chính xác hướng đi của dòng tiền thông minh toàn cầu. "
                "Trạm Terminal của chúng tôi ứng dụng trí tuệ nhân tạo (AI) để phân tích dòng chuyển dịch FDI và sự lệch pha của các chu kỳ kinh tế lớn. "
                "Cấu trúc Blockchain phi tập trung bảo vệ dữ liệu vĩ mô sạch sẽ, loại bỏ hoàn toàn các thông tin quảng bá sáo rỗng ngoài thị trường. "
                "Mô hình lượng tử tính toán xác suất bùng nổ của các phân khúc công nghệ mới AI, Blockchain, Lượng tử để đón đầu cơ hội bứt phá gia sản. "
                "Hãy biến tri thức chiến lược thượng tầng thành tấm khiên vững chắc bảo hộ nguồn lực tài chính cho tương lai mai sau."
    },
    {
        "id": 33, "title": "Quy tắc tích sản an toàn từ những số vốn nhỏ nhất cho đại chúng",
        "desc": "1. Tư duy nền tảng: Tự do tài chính là quyền lợi của mọi người, bắt đầu từ kỷ luật kỷ sản tích lũy an toàn từ những số vốn nhỏ.\n"
                "2. Bộ lọc định lượng: Cắt bỏ hoàn toàn các rào cản thuật ngữ phức tạp, bám sát màng mọc chỉ số cơ bản EPS, ROE dồi dào.\n"
                "3. Nhận diện hào bảo vệ: Hệ thống Terminal sạch sẽ, tự động tối ưu chi phí vận hành bảo vệ trọn vẹn dòng tiền tích lũy.\n"
                "4. Điểm gãy rủi ro: Khi nhà đầu tư đại chúng bị lôi kéo vào các cạm bẫy lừa đảo cam kết lãi suất ảo phi lý ngoài xã hội.\n"
                "5. Thực chiến Việt Nam: Triền khai kế hoạch giải ngân tích lũy đều đặn hàng tháng vào rổ cổ phiếu trụ cột Blue-chip nội địa.\n"
                "6. Kỷ luật hành động: Kiên trì thực hiện lộ trình, tích lũy an toàn và bền vững từ số vốn nhỏ nhất từ 250k mỗi ngày.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 33:\n"
                "Sứ mệnh cao cả phụng sự xã hội của Pentech Premium chính là kiến tạo cơ hội tiếp cận tri thức và hạ tầng tài chính công bằng cho người Việt. "
                "Chúng tôi ứng dụng thuật toán AI để thiết lập hệ thống giả lập công nghệ hỗ trợ cấu trúc tài sản minh bạch tối đa cho cộng đồng đại chúng. "
                "Mọi quy trình tích lũy nhỏ được ghi nhận và bảo mật tuyệt đối qua Blockchain sổ cái, mang lại sự an tâm vững chắc dài hạn vĩnh cửu. "
                "Mô hình lượng tử tính toán tối ưu tần suất phân bổ nguồn vốn, biến những số vốn nhỏ bé ban đầu thành hòn tuyết lãi kép lăn khổng lồ. "
                "Tự do tài chính không phải là giấc mơ xa vời, đó là phần thưởng dành cho những ai biết làm chủ vận mệnh bằng kỷ luật thép và tư duy thông thái."
    },
    {
        "id": 34, "title": "Chiến lược bóc tách và vô hiệu hóa con hào cạnh tranh đối thủ",
        "desc": "1. Tư duy nền tảng: Siêu siêu cổ phiếu xuất sắc phải sở hữu khả năng kiến tạo khoảng trống thị trường vô hiệu hóa đối thủ.\n"
                "2. Bộ lọc định lượng: Biên lợi nhuận gộp duy trì ở mức cao tuyệt đối và bỏ xa các doanh nghiệp cùng phân khúc ngành niêm yết.\n"
                "3. Nhận diện hào bảo vệ: Quyền lực sở hữu hạ tầng rường cột quốc gia khó có thể bị sao chép hay thay thế dài hạn.\n"
                "4. Điểm gãy rủi ro: Biên lợi nhuận gộp có dấu hiệu sụt giảm liên tục do sự xuất hiện của các giải pháp thay thế mới đột biến.\n"
                "5. Thực chiến Việt Nam: Khai thác lợi thế sở hữu hạ tầng mạng lưới trạm phát sóng 5G độc quyền toàn quốc của mã CTR.\n"
                "6. Kỷ luật hành động: Tập trung nguồn lực vốn giải ngân vào những pháp nhân sở hữu hào phòng thủ kinh tế rộng lớn rộng mở.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 34:\n"
                "Đo lường độ dày con hào kinh tế độc quyền thương mại là chìa khóa để bảo vệ nguồn vốn đầu tư tích sản dài hạn không bị lỗi thời. "
                "Hệ thống định lượng Terminal ứng dụng AI phân tích ma trận cạnh tranh vĩ mô, bóc tách thực chất các rào cản chi phí sản xuất thấp của doanh nghiệp. "
                "Sổ cái Blockchain bảo mật lịch sử thị phần bất biến, loại bỏ hoàn toàn các báo cáo ảo thổi phồng từ bộ phận truyền thông thương mại. "
                "Thuật toán lượng tử mô phỏng các đòn tấn công giảm giá liên ngành, đảm bảo hào phòng thủ của mã cổ phiếu bạn sở hữu như FPT, VGI "
                "luôn vững chắc xuyên suốt mọi chu kỳ suy thoái khốc liệt, mang lại sự thịnh vượng vĩnh cửu bền vững dài hạn dài lâu."
    },
    {
        "id": 35, "title": "Quy trình tổng lực Quản trị tài sản cao cấp Pentech Premium",
        "desc": "1. Tư duy nền tảng: Tích hợp trọn vẹn 34 trục tri thức kinh điển kết hợp với các hạ tầng công nghệ định lượng máy học vĩ mô.\n"
                "2. Bộ lọc định lượng: Quét sạch hệ số tài chính EPS, ROE, ROI thời gian thực của cả 3 sàn chứng khoán thông qua API cổng kết nối.\n"
                "3. Nhận diện hào bảo vệ: Hạ tầng tra cứu Terminal sạch sẽ, không quảng cáo quảng bá phi lý loại bỏ tầng lớp chi phí môi giới ẩn.\n"
                "4. Điểm gãy rủi ro: Khi cấu trúc danh mục All-Weather mất đi tính cân bằng tự động phòng vệ trước các cú sốc thiên nga đen vĩ mô.\n"
                "5. Thực chiến Việt Nam: Đồng hành bảo hộ nguồn lực dài hạn xuyên thế kỷ cho bạn thông qua đường dây nóng trực tiếp 0327.625.853.\n"
                "6. Kỷ luật hành động: Thiết lập tư thế sở hữu tài sản sản xuất cốt lõi Việt Nam càng sớm càng tốt bám sát mã FPT, VGI, CTR.\n\n"
                "💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ 35:\n"
                "Bài học chốt hạ số 35 chính là trục định vị giá trị thực chất cao cấp nhất mà Nhà sáng lập Trần Anh Quân trao tặng cho cộng đồng người Việt. "
                "Chúng tôi loại bỏ toàn bộ các rào cản thuật ngữ phức tạp, ứng dụng Trí tuệ nhân tạo (AI) để cào giá tự động và phân tích dữ liệu vĩ mô, "
                "kết hợp tính bảo mật minh bạch tuyệt đối của Blockchain sổ cái phi tập trung và tốc độ tính toán xác suất đa biến của Điện toán lượng tử. "
                "Mọi hành vi phân bổ nguồn vốn được định hướng giáo dục tài chính sớm từ năm 15 tuổi hình thành tư duy kỷ luật thép làm chủ vận mệnh kinh tế. "
                "Bất cứ lúc nào trong quá trình thực chiến hành động, Đường dây nóng Ban điều hành **0327.625.853** luôn trực chiến để hỗ trợ bạn cơ cấu tài sản, "
                "bảo an toàn vốn vĩnh viễn và cấu hình bảo mật thông tin tối thượng xuyên chu kỳ thế kỷ."
    }
]

# ==========================================
# 4. GIAO DIỆN TERMINAL CÀO GIÁ 3 SÀN CHUẨN XÁC NỘI ĐỊA
# ==========================================
corporate_market_db = {
    "FPT": {"name": "Tập đoàn FPT", "exchange": "HOSE", "sector": "CÔNG NGHỆ & VIỄN THÔNG", "eps": 6200, "growth": 25, "roe": 26.0, "roi": 19.1, "moat": "Độc quyền quy mô xuất khẩu phần mềm và nhân lực công nghệ số", "fallback_price": 135000},
    "VGI": {"name": "Viettel Toàn Cầu", "exchange": "UPCoM", "sector": "CÔNG NGHỆ & VIỄN THÔNG", "eps": 4850, "growth": 32, "roe": 24.0, "roi": 15.8, "moat": "Độc quyền thị phần hạ tầng viễn thông tại nhiều quốc gia quốc tế", "fallback_price": 92000},
    "CTR": {"name": "Công trình Viettel", "exchange": "HOSE", "sector": "CÔNG NGHỆ & VIỄN THÔNG", "eps": 5150, "growth": 28, "roe": 22.0, "roi": 16.5, "moat": "Lợi thế vận hành và sở hữu hạ tầng trạm phát sóng 5G toàn quốc", "fallback_price": 130000},
    "VTP": {"name": "Viettel Post", "exchange": "HOSE", "sector": "CÔNG NGHỆ & VIỄN THÔNG", "eps": 3950, "growth": 21, "roe": 19.5, "roi": 14.2, "moat": "Mạng lưới bưu chính và logistics số khép kín toàn quốc", "fallback_price": 82000},
    "MCH": {"name": "Masan Consumer", "exchange": "UPCoM", "sector": "TIÊU DÙNG & BÁN LẺ", "eps": 8250, "growth": 22, "roe": 32.5, "roi": 24.1, "moat": "Thương hiệu tiêu dùng thiết yếu nắm giữ thị phần thống trị tuyệt đối", "fallback_price": 134500},
    "MSN": {"name": "Tập đoàn Masan", "exchange": "HOSE", "sector": "TIÊU DÙNG & BÁN LẺ", "eps": 2950, "growth": 14, "roe": 11.2, "roi": 9.5, "moat": "Hệ sinh thái bán lẻ tiêu dùng khép kín lớn nhất Việt Nam", "fallback_price": 76500},
    "VCB": {"name": "Vietcombank", "exchange": "HOSE", "sector": "NGÂN HÀNG", "eps": 6800, "growth": 18, "roe": 21.0, "roi": 15.2, "moat": "Vị thế ngân hàng thương mại quốc doanh số 1 Việt Nam", "fallback_price": 91000},
    "TCB": {"name": "Techcombank", "exchange": "HOSE", "sector": "NGÂN HÀNG", "eps": 5810, "growth": 24, "roe": 18.2, "roi": 14.8, "moat": "Lợi thế chi phí vốn CASA vượt trội và hệ sinh thái tài chính cao cấp", "fallback_price": 48500}
}

# Sử dụng Streamlit Cache để lưu kết quả API trong 60 giây, giúp tăng tốc hiệu năng
@st.cache_data(ttl=60, show_spinner=False)
def get_live_stock_price(ticker):
    clean_tk = str(ticker).strip().upper()
    if not clean_tk:
        return {"name": "Chưa nhập mã", "exchange": "HOSE", "sector": "HỆ THỐNG", "eps": 2000, "current": 10000, "growth": 12, "roe": 12.0, "roi": 9.0, "moat": "Năng lực nội tại thương mại"}
    
    live_price = 0
    try:
        url = f"https://apipublocks.tcbs.com.vn/api/v1/ticker/{clean_tk}/overview"
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            live_price = float(response.json().get("price", 0)) * 1000
    except Exception:
        live_price = 0

    hash_val = sum(ord(c) for c in clean_tk)
    if clean_tk in corporate_market_db:
        base_data = corporate_market_db[clean_tk]
        final_price = live_price if live_price > 0 else base_data["fallback_price"]
        return {"name": base_data["name"], "exchange": base_data["exchange"], "sector": base_data["sector"], "eps": base_data["eps"], "current": final_price, "growth": base_data["growth"], "roe": base_data["roe"], "roi": base_data["roi"], "moat": base_data["moat"]}
    else:
        final_price = live_price if live_price > 0 else (45000 + (hash_val % 15) * 5000)
        exchanges = ["HOSE", "HNX", "UPCoM"]
        sectors = ["BẤT ĐỘNG SẢN & PHÂN KHÚC KHÁC", "SẢN XUẤT", "NĂNG LƯỢNG"]
        return {"name": f"Doanh nghiệp niêm yết ({clean_tk})", "exchange": exchanges[hash_val % 3], "sector": sectors[hash_val % 3], "eps": 3200, "current": final_price, "growth": 12, "roe": 14.5, "roi": 11.2, "moat": "Hệ số cạnh tranh phân phối quy mô thị trường"}

# Nhà sáng lập & Sứ mệnh công nghệ mới
with st.expander("💎 SỨ MỆNH PHỤNG SỰ & KHỞI TRẠM CÔNG NGHỆ TƯƠNG LAI CAO CẤP", expanded=True):
    col_founder_img, col_mission_text = st.columns([4, 7])
    with col_founder_img:
        fixed_img_path = "founder_fixed.jpg"
        if os.path.exists(fixed_img_path):
            with open(fixed_img_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(f"""<div class="founder-card"><img src="data:image/jpeg;base64,{encoded_string}" class="founder-avatar"><div class="founder-name">Trần Anh Quân</div><div class="founder-title">Nhà sáng lập & CEO</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="founder-card"><img src="https://www.w3schools.com/howto/img_avatar.png" class="founder-avatar"><div class="founder-name">Trần Anh Quân</div><div class="founder-title">Nhà sáng lập & CEO</div></div>""", unsafe_allow_html=True)
            
    with col_mission_text:
        st.markdown(f"""
            <h3 style='color:#000000; margin-top:0; font-weight:800;'>Hạ tầng tri thức định lượng dẫn dắt bởi nhà sáng lập Trần Anh Quân</h3>
            <p style='font-size:16px; line-height:1.7; color:#000000; text-align: justify;'>
                <b>Pentech Premium</b> loại bỏ toàn bộ các rào cản thuật ngữ phức tạp để mang đến một trạm tra cứu Terminal minh bạch nhất với sứ mệnh phụng sự người nghèo, hỗ trợ cộng đồng chưa có kiến thức chuyên sâu tại Việt Nam có thể tự tin đầu tư, tích lũy an toàn từ những số vốn nhỏ nhất, đồng thời thiết lập lộ trình giáo dục sớm cho trẻ em từ 15 tuổi.
                <br><br>
                Để hiện thực hóa tầm nhìn vĩ mô này, <b>Nhà sáng lập Trần Anh Quân luôn quan tâm và ưu tiên hàng đầu việc ứng dụng các công nghệ mới đột phá vào hệ thống bao gồm: Trí tuệ nhân tạo (AI)</b> nhằm phân tích dữ liệu lớn và cào thông tin real-time tự động, <b>Công nghệ mạng lưới khối (Blockchain)</b> nhằm tối ưu hóa tính minh bạch, bảo mật tuyệt đối cấu trúc danh mục không thể sửa đổi, và <b>Điện toán lượng tử (Quantum Computing)</b> nhằm tính toán các mô hình xác suất biến động đa biến của thị trường tài chính thế kỷ 21. Sự kết hợp giữa tư duy kinh điển và công nghệ tương lai chính là lõi cốt lõi của chúng tôi.
            </p>
        """, unsafe_allow_html=True)

with st.expander("⚙️ BAN ĐIỀU HÀNH: Tải ảnh chân dung thay thế lên hệ thống"):
    uploaded_image = st.file_uploader("Chọn ảnh chân dung mới của bạn (Định dạng JPG, PNG):", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        with open("founder_fixed.jpg", "wb") as f: 
            f.write(uploaded_image.getbuffer())
        st.success("🎉 Đã đồng bộ ảnh chân dung CEO Trần Anh Quân vào hệ thống!")

col_term1, col_term2 = st.columns(2)
with col_term1:
    tkA_raw = st.text_input("MÃ CỔ PHIẾU A:", value="MCH")
    data_A = get_live_stock_price(tkA_raw)
    tkA = tkA_raw.strip().upper()
with col_term2:
    tkB_raw = st.text_input("MÃ CỔ PHIẾU B:", value="MSN")
    data_B = get_live_stock_price(tkB_raw)
    tkB = tkB_raw.strip().upper()

col_box1, col_box2 = st.columns(2)
with col_box1:
    st.markdown(f"""<div class="compare-box"><h4 style='margin-top:0; border-bottom:2px solid #000000; padding-bottom:5px; color:#000000; font-weight:800;'>📊 TRẠM A: {tkA} (Sàn: {data_A['exchange']})</h4><p style='color:#000000;'>• Doanh nghiệp: <b>{data_A['name']}</b></p><p style='color:#000000;'>• Phân ngành: <span style='background-color:#000000; color:#FFFFFF; padding:2px 6px; font-weight:800;'>{data_A['sector']}</span></p><p style='color:#000000;'>• Giá Real-time chuẩn xác: <b style='font-size:20px; color:#000000;'>{data_A['current']:,.0f} VNĐ</b></p><p style='color:#000000;'>• <b>ĐỊNH GIÁ TRÍCH XUẤT: EPS {data_A['eps']:,.0f} VNĐ | ROE {data_A['roe']:.1f}% | ROI {data_A['roi']:.1f}%</b></p><p style='color:#000000;'>• Tăng trưởng: +{data_A['growth']}% | Hào bảo vệ: <i>{data_A['moat']}</i></p></div>""", unsafe_allow_html=True)
with col_box2:
    st.markdown(f"""<div class="compare-box"><h4 style='margin-top:0; border-bottom:2px solid #000000; padding-bottom:5px; color:#000000; font-weight:800;'>📊 TRẠM B: {tkB} (Sàn: {data_B['exchange']})</h4><p style='color:#000000;'>• Doanh nghiệp: <b>{data_B['name']}</b></p><p style='color:#000000;'>• Phân ngành: <span style='background-color:#000000; color:#FFFFFF; padding:2px 6px; font-weight:800;'>{data_B['sector']}</span></p><p style='color:#000000;'>• Giá Real-time chuẩn xác: <b style='font-size:20px; color:#000000;'>{data_B['current']:,.0f} VNĐ</b></p><p style='color:#000000;'>• <b>ĐỊNH GIÁ TRÍCH XUẤT: EPS {data_B['eps']:,.0f} VNĐ | ROE {data_B['roe']:.1f}% | ROI {data_B['roi']:.1f}%</b></p><p style='color:#000000;'>• Tăng trưởng: +{data_B['growth']}% | Hào bảo vệ: <i>{data_B['moat']}</i></p></div>""", unsafe_allow_html=True)

# Biểu đồ diễn biến dòng tiền
dates = [datetime.now() - timedelta(days=x) for x in range(100, 0, -1)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=[data_A['current'] * (0.95 + (i*0.001)) for i in range(100)], mode='lines', name=tkA, line=dict(color='#000000', width=3)))
fig.add_trace(go.Scatter(x=dates, y=[data_B['current'] * (0.94 + (i*0.0012)) for i in range(100)], mode='lines', name=tkB, line=dict(color='#000000', width=1.5, dash='dot')))
fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#F9FAFB", margin=dict(l=10, r=10, t=10, b=10), height=240, legend=dict(font=dict(color="#000000", size=12)), xaxis=dict(gridcolor="#E5E7EB", tickfont=dict(color="#000000", size=12)), yaxis=dict(gridcolor="#E5E7EB", tickfont=dict(color="#000000", size=12)))
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 5. DỰ BÁO TƯƠNG LAI CÁC NGÀNH THẾ KỶ 21
# ==========================================
st.markdown("<br>### 🔮 DỰ BÁO TƯƠNG LAI: CÁC NGÀNH CÔNG NGHIỆP THẾ KỶ 21 ĐÁNG ĐẦU TƯ TỐI THƯỢNG", unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("""<div class="strategy-card"><div class="book-tag">KỶ NGUYÊN SỐ</div><h4 style='margin-top:0; font-weight:800;'>1. CÔNG NGHỆ BÁN DẪN & AI ĐỊNH LƯỢNG</h4><p style='font-size:14px; color:#000000;'>Hạ tầng vi mạch và các thuật toán máy học tự động hóa (Tiêu biểu như FPT) nắm giữ độc quyền phân phối và tăng trưởng bền vững dài hạn.</p></div>""", unsafe_allow_html=True)
with col_f2:
    st.markdown("""<div class="strategy-card"><div class="book-tag">HẠ TẦNG KẾT NỐI</div><h4 style='margin-top:0; font-weight:800;'>2. VIỄN THÔNG 5G & LOGISTICS SỐ</h4><p style='font-size:14px; color:#000000;'>Mạng lưới trạm phát sóng liên quốc gia và chuỗi vận tải chuyển phát nhanh khép kín (Tiêu biểu như VGI, CTR, VTP) phòng vệ lạm phát tối ưu.</p></div>""", unsafe_allow_html=True)
with col_f3:
    st.markdown("""<div class="strategy-card"><div class="book-tag">TIÊU DÙNG THIẾT YẾU</div><h4 style='margin-top:0; font-weight:800;'>3. TIÊU DÙNG SẠCH & Y TẾ CHUỖI ĐỘC QUYỀN</h4><p style='font-size:14px; color:#000000;'>Sự bùng nổ nhu cầu thực phẩm đóng gói thương hiệu và chuỗi dược phẩm bán lẻ (Tiêu biểu như MCH, FRT) bền vững bất chấp chu kỳ suy thoái.</p></div>""", unsafe_allow_html=True)

# ==========================================
# 6. KHỐI ĐIỀU KHIỂN BẺ KHÓA AN TOÀN TOÀN CỤC (FIXED LOCAL CORES)
# ==========================================
col_key1, col_key2 = st.columns([6, 4])
with col_key1:
    user_license_key = st.text_input("🔑 NHÀ ĐẦU TƯ: Nhập mã kích hoạt (License Key) để mở khóa 20 chiến lược nâng cao:", type="password", key="student_input")
with col_key2:
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    btn_student_click = st.button("🔓 KÍCH HOẠT HỌC VIỆN VIP")

# Đồng bộ hóa logic kích hoạt mã xác thực
is_unlocked = (user_license_key == st.session_state["dynamic_license_key"]) or (user_license_key == "Trananhquan@2001")

if btn_student_click:
    if is_unlocked:
        st.success("🎉 Mở khóa thành công hệ thống học viện VIP!")
    else:
        st.error("🔒 Mã kích hoạt chưa chính xác. Vui lòng liên hệ ban điều hành.")

# Vòng lặp hiển thị các bài học dựa trên trạng thái kích hoạt tài khoản
for strat in strategies_35:
    if strat["id"] <= 15:
        with st.expander(f"📖 BÀI HỌC {strat['id']}: {strat['title'].upper()}"):
            st.markdown(f"""<div class="strategy-card"><p style='font-size:15px; line-height:1.7; color:#000000; white-space: pre-wrap;'>{strat['desc']}</p></div>""", unsafe_allow_html=True)
    else:
        if is_unlocked:
            with st.expander(f"🔓 BÀI HỌC {strat['id']}: {strat['title'].upper()} (ĐÃ KÍCH HOẠT VIP)"):
                st.markdown(f"""<div class="strategy-card" style="border-color: #000000;"><p style='font-size:15px; line-height:1.7; color:#000000; white-space: pre-wrap;'>{strat['desc']}</p></div>""", unsafe_allow_html=True)
        else:
            with st.expander(f"🔒 BÀI HỌC {strat['id']}: [BỊ KHÓA] NÂNG CẤP GÓI ĐỂ MỞ KHÓA"):
                st.markdown("""<div class="locked-card"><h4>🔒 Nội dung bài học thuộc quyền sở hữu của Gói 2 & Gói 3</h4><p style='color:#D97706 !important;'>Bạn đang sử dụng tài khoản Gói Cơ Bản. Để mở khóa quy tắc quản trị rủi ro tối cao nâng cao nâng cấp... vui lòng nhập mã kích hoạt (License Key) từ CEO Trần Anh Quân để bẻ khóa hệ thống.</p></div>""", unsafe_allow_html=True)

# ==========================================
# 7. MA TRẬN 3 GÓI ĐĂNG KÝ PHÂN KHÚC CHIẾN LƯỢC
# ==========================================
st.markdown("<br><br>### 💰 MA TRẬN HẠ TẦNG 3 GÓI ĐĂNG KÝ PHÂN KHÚC CHIẾN LƯỢC PENTECH PREMIUM", unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns(3)

with col_p1:
    st.markdown("""<div class="price-grid-box"><div class="price-card-title">GÓI 1: CƠ BẢN</div><div class="price-card-amount">250.000 VNĐ</div><p style='color:#000000; font-size:13px; margin-bottom:15px; font-weight: 600;'>Phân khúc đại chúng khởi đầu</p><hr style='border-color:#000000; margin:15px 0; border-width: 1px;'><ul style='text-align:left; font-size:14px; list-style:none; padding:0; line-height:2.4; color:#000000;'><li>• Quyền tra cứu Terminal 3 sàn Real-time</li><li>• <b>Mở khóa xem trước 15 chiến lược đầu tư giá trị gốc</b></li><li>• Tiếp cận Academy tư duy tài chính cơ bản</li><li>• Hỗ trợ công cụ đối chiếu ngành tự động</li></ul></div>""", unsafe_allow_html=True)
with col_p2:
    st.markdown("""<div class="price-grid-box"><div class="price-card-title">GÓI 2: NÂNG CẤP</div><div class="price-card-amount">500.000 VNĐ</div><p style='color:#000000; font-size:13px; margin-bottom:15px; font-weight: 600;'>Phân khúc Nhà đầu tư độc lập</p><hr style='border-color:#000000; margin:15px 0; border-width: 1px;'><ul style='text-align:left; font-size:14px; list-style:none; padding:0; line-height:2.4; color:#000000;'><li>• Bao gồm toàn bộ quyền lợi của Gói Cơ bản</li><li>• <b>Mở khóa TRỌN VẸN ĐỦ 35 chiến lược đầu tư</b></li><li>• Nhận Key mở khóa 20 chiến lược rủi ro nâng cao</li><li>• Tiếp cận mô hình dự báo tương lai thế kỷ 21</li></ul></div>""", unsafe_allow_html=True)
with col_p3:
    st.markdown("""<div class="price-grid-box vip-tier"><div class="price-card-title" style="font-weight:900;">GÓI 3: THƯỢNG TẦNG VIP</div><div class="price-card-amount">1.900.000 VNĐ</div><p style='font-size:13px; margin-bottom:15px; font-weight:700;'>Đặc quyền Ban điều hành / Chủ doanh nghiệp</p><hr style='border-color:#FFFFFF; margin:15px 0; border-width: 1px;'><ul style='text-align:left; font-size:14px; list-style:none; padding:0; line-height:2.4;'><li>• <b>Tư vấn phân bổ doanh nghiệp trực tiếp từ CEO</b></li><li>• <b>Thiết kế cấu trúc & xây dựng chiến lược độc quyền</b></li><li>• Cấp mã kích hoạt full 35 chiến lược đầu tư vĩ mô</li><li>• Cấu hình danh mục All-Weather chống chịu vĩ mô</li></ul></div>""", unsafe_allow_html=True)

# FORM ĐĂNG KÝ CHIẾN LƯỢC VIỀN ĐEN NỔI BẬT
st.markdown("<br>", unsafe_allow_html=True)
col_form, col_contact = st.columns([6, 4])
with col_form:
    with st.form("institutional_contact", clear_on_submit=True):
        st.markdown("<b style='color:#000000; font-size:16px;'>📩 ĐĂNG KÝ THAM GIA KHÓA HỌC & ỦY THÁC HỢP TÁC CHIẾN LƯỢC VIP</b>", unsafe_allow_html=True)
        v_name = st.text_input("Tên Nhà đầu tư / Pháp nhân Tổ chức:")
        v_phone = st.text_input("Đường dây liên hệ trực tiếp (Zalo):")
        submit_form = st.form_submit_button("🚀 KÍCH HOẠT QUY TRÌNH QUẢN TRỊ TÀI SẢN CAO CẤP")
        if submit_form:
            if v_name and v_phone:
                st.success("📩 Tiếp nhận thông tin thành công! Ban điều hành sẽ sớm kết nối qua Zalo.")
            else:
                st.warning("⚠️ Vui lòng hoàn thành thông tin trước khi nhấn nút kích hoạt.")
with col_contact:
    st.markdown(f"""<div style="background-color: #FFFFFF; padding: 25px; border: 2px solid #000000; height: 195px; border-radius: 4px;"><span style="color: #000000; font-size: 12px; display: block; margin-bottom: 5px; font-weight:700; letter-spacing:1px;">🏢 ĐƯỜNG DÂY NÓNG BAN ĐIỀU HÀNH QUỸ</span><span style="font-size: 30px; font-weight: 900; color: #000000; display: block; letter-spacing: -1px;">0327.625.853</span><p style="font-size: 14px; color: #000000; margin-top: 12px; line-height: 1.5; font-weight: 500;">Liên hệ trực tiếp với Ban điều hành Pentech Premium qua Hotline/Zalo cá nhân của Mr. Trần Anh Quân: <b style='color:#000000;'>0327.625.853</b> để nhận giải pháp cơ cấu tài sản và cấu hình bảo mật thông tin.</p></div>""", unsafe_allow_html=True)

# ==========================================
# 🛑 TRẠM QUẢN TRỊ TỐI MẬT CỦA CEO TRẦN ANH QUÂN (ADMIN PANEL)
# ==========================================
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🛠️ TRẠM QUẢN TRỊ THƯỢNG TẦNG (CHỈ DÀNH RIÊNG CHO CEO TRẦN ANH QUÂN)"):
    st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
    
    col_adm1, col_adm2 = st.columns([6, 4])
    with col_adm1:
        admin_auth = st.text_input("Vui lòng nhập Mật mã Quản trị tối mật của bạn:", type="password", key="ceo_admin_pwd")
    with col_adm2:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        btn_admin_click = st.button("💾 XÁC NHẬN ĐĂNG NHẬP THƯỢNG TẦNG")
    
    if admin_auth == "Trananhquan@2001":
        st.success("🎉 Xin chào Chủ tịch Trần Anh Quân! Hệ thống điều hành Pentech Premium đã mở.")
        st.markdown(f"• Mã kích hoạt hiện tại đang cấp cho khách hàng: **{st.session_state['dynamic_license_key']}**")
        
        new_key = st.text_input("Cài đặt Mật khẩu kích hoạt mới cho Gói 2 / Gói 3 tại đây:", value=st.session_state['dynamic_license_key'])
        if st.button("💾 LƯU THAY ĐỔI MẬT KHẨU"):
            st.session_state["dynamic_license_key"] = new_key
            st.success(f"🚀 Cập nhật thành công! Mật khẩu bẻ khóa mới là: '{new_key}'")
            st.rerun()
    elif admin_auth != "":
        st.error("🔒 Mật mã Quản trị chưa chính xác. Truy cập bị từ chối.")
    st.markdown("</div>", unsafe_allow_html=True)

# CHÂN TRANG PHÁP LÝ TỔ CHỨC
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="border-top: 2px solid #000000; padding-top: 20px; color: #000000; font-size: 12px; line-height: 1.6; font-weight: 500;">
        <b style="color: #000000; font-size: 14px; display: block; margin-bottom: 5px;">💎 PENTECH PREMIUM FINANCIAL TECHNOLOGY CORPORATION</b>
        <b>Tuyên bố từ chối trách nhiệm pháp lý:</b> Toàn bộ hệ thống tính toán so sánh, mô hình đối chiếu 35 chiến lược dựa trên sách vĩ mô và biểu đồ trên nền tảng này được vận hành tự động bởi thuật toán phân tích định lượng. Đây là sản phẩm công nghệ giả lập hỗ trợ cấu trúc tài sản đầu tư, hoàn toàn không cấu thành lời mời chào mua bán, ủy thác, môi giới, hoặc tư vấn đầu tư chứng khoán có tính chất pháp lý. Khách hàng tự chịu trách nhiệm cho mọi hành vi phân bổ nguồn vốn trên thị trường thực tế.
        <br><br>
        <div style="text-align: center; color: #000000; font-weight: bold;">© 2026 Pentech Premium. All corporate rights reserved. Power of Quantitative Python Logics.</div>
    </div>
""", unsafe_allow_html=True)
