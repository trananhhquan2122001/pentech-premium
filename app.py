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

# Giữ mã xác minh Google Search Console của bạn Quân
st._config.set_option("html.additionalHeadContent", '<meta name="google-site-verification" content="448da2da278475de" />')

if "dynamic_license_key" not in st.session_state:
    st.session_state["dynamic_license_key"] = "Trananhquan@2001"

# ==========================================
# 2. NGÔN NGỮ THIẾT KẾ NỀN TRẮNG SÁNG - CHỮ ĐEN - VIỀN VÀNG GOLD LUXURY
# ==========================================
st.markdown("""
    <style>
    /* Nền trắng sáng toàn phần chuẩn giao diện phân tích cao cấp */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stVerticalBlock"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6, label, span, strong, em, li { 
        color: #000000 !important; 
    }
    
    /* Tiêu đề chính sử dụng màu xanh thẫm định chế tôn nghiêm */
    .premium-main-title {
        color: #0A192F !important;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    div[data-testid="stMarkdownContainer"] p { 
        color: #000000 !important; 
        font-size: 15px !important;
        font-weight: 500 !important;
        line-height: 1.6;
    }
    
    .premium-header {
        border-bottom: 3px solid #0A192F;
        padding: 25px 0px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 35px;
    }
    .premium-subtitle { color: #D4AF37 !important; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }
    
    /* Hộp chiến lược màu xám nhạt viền xanh thẫm tinh tế */
    .strategy-card {
        background-color: #F8FAFC;
        padding: 25px;
        border: 1px solid #0A192F;
        border-left: 5px solid #D4AF37;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    
    .founder-card {
        background-color: #F8FAFC;
        border: 2px solid #0A192F;
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
        border: 3px solid #D4AF37;
        display: inline-block;
    }
    .founder-name { font-size: 24px; font-weight: 800; color: #0A192F !important; margin-top: 15px; margin-bottom: 2px; }
    .founder-title { font-size: 13px; color: #64748B !important; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; }
    
    .locked-card {
        background-color: #FFFBEB;
        padding: 25px;
        border: 2px dashed #D97706;
        border-radius: 4px;
        text-align: center;
    }
    
    .compare-box {
        background-color: #F8FAFC;
        padding: 25px;
        border: 1px solid #0A192F;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    /* Gói dịch vụ định chế thương mại */
    .price-grid-box {
        background-color: #FFFFFF;
        border: 1px solid #0A192F;
        border-radius: 4px;
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .price-card-title { font-size: 18px; font-weight: 800; color: #0A192F !important; text-transform: uppercase; letter-spacing: 1px; }
    .price-card-amount { font-size: 34px; font-weight: 900; color: #000000 !important; margin: 15px 0px 5px 0px; }
    
    /* Gói 3 VIP chuyển nền xanh thẫm chữ trắng bo viền vàng cát thượng đẳng */
    .price-grid-box.vip-tier {
        background-color: #0A192F;
        border: 2px solid #D4AF37;
    }
    .price-grid-box.vip-tier .price-card-title { color: #D4AF37 !important; }
    .price-grid-box.vip-tier .price-card-amount, .price-grid-box.vip-tier li, .price-grid-box.vip-tier p { color: #FFFFFF !important; }
    
    /* Tinh chỉnh thanh Expanders học viện mở rộng nền xám chữ đen */
    div[data-testid="stExpander"] {
        border: 1px solid #0A192F !important;
        background-color: #FFFFFF !important;
        border-radius: 4px !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #0A192F !important;
        padding: 14px !important;
    }
    
    input, select {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #0A192F !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Nút bấm xanh thẫm chữ trắng hoàng gia */
    button {
        background-color: #0A192F !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        border-radius: 4px !important;
        border: 1px solid #0A192F !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease;
    }
    button:hover {
        background-color: #D4AF37 !important;
        border-color: #D4AF37 !important;
        color: #0A192F !important;
    }
    .admin-box {
        background-color: #F8FAFC;
        border: 2px dashed #0A192F;
        padding: 25px;
        margin-top: 40px;
    }
    
    .highlight-text-box {
        background-color: #F1F5F9;
        padding: 15px;
        border-left: 4px solid #0A192F;
        border-radius: 2px;
        margin: 15px 0px;
    }
    .book-tag { font-size: 12px; font-weight: 800; color: #FFFFFF !important; background-color: #0A192F !important; padding: 3px 10px; border-radius: 2px; display: inline-block; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# Thanh điều hướng thương hiệu định chế
st.markdown("""
    <div class="premium-header">
        <div class="premium-main-title">Pentech Premium <span style='font-size:16px; color:#0A192F; font-weight:600;'>INSTITUTIONAL TERMINAL</span></div>
        <div class="premium-subtitle">Hạ tầng Real-time VN30 • Phong cách Thiết kế Pure Light Luxury</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 3. KHO DỮ LIỆU ĐẦY ĐỦ THỦ CÔNG 35 BÀI HỌC BIỆT LẬP HOÀN TOÀN
# ==========================================
core_lessons = {
    1: {"title": "Xác lập trục giá trị nội tại cốt lõi doanh nghiệp", "focus": "Bóc tách cấu trúc tài sản ròng hữu hình để tìm kiếm biên an toàn phòng thủ thực chất.", "context": "Bài học này yêu cầu nhà đầu tư phải xây dựng một bộ lọc tư duy định lượng nghiêm ngặt như một định chế quản trị quỹ chuyên nghiệp. Chúng ta không nhìn vào sự nhảy múa ngắn hạn của bảng điện tử mà sử dụng hệ thống Trí tuệ nhân tạo (AI) để phân tích dữ liệu kế toán quá khứ, tìm kiếm sự minh bạch thực sự đằng sau các con số doanh thu. Công nghệ mạng lưới khối (Blockchain) được tích hợp ngầm để lưu vết các biên an toàn lịch sử, đảm bảo cấu trúc thông tin đối chiếu song song là chính xác tuyệt đối và không thể bị sửa đổi. Đồng thời, mô hình điện toán lượng tử chạy các ma trận xác suất biến động đa biến để tìm ra điểm gãy rủi ro thấp nhất có thể diễn ra. Đầu tư tích sản từ số vốn nhỏ cần một triền dốc thời gian dài để hòn tuyết lãi kép lăn bánh vĩ đại. Bản chất của tri thức thượng tầng không phải là dự đoán xu hướng ngày mai, mà là làm chủ trục giá trị thực của tài sản ngày hôm nay, biến dòng tiền thặng dư sản xuất thành bệ phóng tài chính an toàn bền vững xuyên thế kỷ."},
    2: {"title": "Chiến lược chế ngự Ngài Thị Trường và ma trận tâm lý đám đông", "focus": "Coi sự biến động ngắn hạn của đồ thị kỹ thuật là người phục vụ cung cấp cơ hội mua hời.", "context": "Ngài Thị Trường là một thực thể điên cuồng, liên tục cống hiến cho bạn những mức giá vô lý mỗi ngày dựa trên sự trồi sụt của cảm xúc hoang mang. Để không bị nhấn chìm vào làn sóng cuồng loạn của đám đông, trạm Terminal ứng dụng trí tuệ nhân tạo AI để đo lường độ lệch pha giữa thị giá hoang tưởng và giá trị nội tại thực chất. Cấu trúc sổ cái Blockchain lưu trữ dòng tiền thực tế của các cá mập lớn và định chế tài chính thượng tầng, giúp bạn nhìn thấu hành vi thu gom lặng lẽ đứng sau bức màn truyền thông báo chí. Mô phỏng lượng tử phân tích chu kỳ sợ hãi để xác định thời điểm đám đông buông xuôi đầu hàng hoàn toàn. Giáo dục tài chính sớm từ năm 15 tuổi đòi hỏi học viên bắt buộc phải thấu suốt quy tắc này: biến biến động thị trường thành công cụ khai thác siêu lợi nhuận phi thường, kiên định tích lũy an toàn bất chấp các chu kỳ suy thoái khốc liệt nhất."},
    3: {"title": "Bộ lọc nguyên tắc chọn siêu cổ phiếu tăng trưởng đột biến", "focus": "Mua một cổ phiếu chính là mua một phần quyền sở hữu của một doanh nghiệp sản xuất thực tế.", "context": "Việc lựa chọn một siêu cổ phiếu tăng trưởng đòi hỏi một tư duy thẩm định toàn diện cả về định tính lẫn định lượng. Trí tuệ nhân tạo (AI) quét toàn bộ hệ thống báo cáo tài chính của 3 sàn chứng khoán tại Việt Nam để tìm kiếm sự nhất quán trong tăng trưởng thu nhập EPS và khả năng tái phân bổ vốn thặng dư hiệu quả của doanh nghiệp. Chúng tôi đưa các chỉ số này vào mạng lưới Blockchain bảo mật để xây dựng lịch sử định giá bất biến, giúp nhà đầu tư nhìn thấu bức tranh tài chính sạch. Tư duy lượng tử được kích hoạt để phân tích ma trận cạnh tranh liên ngành, đánh giá xem doanh nghiệp có giữ vững được hào kinh tế trước làn sóng dịch chuyển công nghệ hay không. Đầu tư thành công không cần làm những điều phi thường, mà là làm những điều bình thường một cách có kỷ luật phi thường. Hãy biến dòng tiền cổ tức tiền mặt đều đặn thành bệ phóng để tối ưu hóa lãi kép vĩnh cửu."},
    4: {"title": "Hiệu ứng Hòn tuyết lăn và tối ưu hóa lãi kép vĩnh cửu", "focus": "Lãi kép là kỳ quan tài chính hoạt động tối ưu dựa trên trục thời gian dài và tỷ suất cao.", "context": "Để hòn tuyết tài sản có thể mở rộng quy mô khổng lồ, nhà quản trị bắt buộc phải bảo vệ triệt để triền dốc thời gian nắm giữ dài hạn. Pentech Premium ứng dụng AI để tự động hóa việc cấu hình dòng tiền cổ tức quay trở lại mua gom cổ phiếu hời khi thị trường chiết khấu sâu, triệt tiêu hoàn toàn các bẫy phí trung gian phi lý của các bên môi giới. Mọi giao dịch luân chuyển vốn được xác thực minh bạch qua Blockchain nhằm bảo an toàn tuyệt đối cấu trúc tài khoản. Thuật toán lượng tử mô phỏng ma trận rủi ro, đảm bảo hòn tuyết tài sản luôn duy trì được quán tính tăng trưởng ổn định xuyên qua mọi chu kỳ lạm phát vĩ mô. Đây là bài học rường cột kiến tạo lộ trình tự do tài chính dài hạn vững chắc cho thế hệ tương lai ngay từ độ tuổi 15."},
    5: {"title": "Ma trận Mô hình tư duy liên ngành trong thẩm định vĩ mô", "focus": "Không dựa dẫm vào một lăng kính duy nhất, kết hợp nhuần nhuyễn toán học, tâm lý hành vi và sinh học.", "context": "Nếu bạn chỉ sở hữu một công cụ là cây búa, bạn sẽ nhìn mọi vấn đề trên thị trường như một cây đinh. Nhà quản trị tài sản chuyên nghiệp bắt buộc phải sở hữu một ma trận gồm nhiều mô hình tư duy liên ngành khác nhau. Trí tuệ nhân tạo (AI) giúp chúng tôi tích hợp các quy luật của hệ thống phức hợp vào một thuật toán xử lý dữ liệu vĩ mô duy nhất. Màng lọc Blockchain đảm bảo tính khách quan tuyệt đối của dữ liệu đầu vào, loại bỏ hoàn toàn các nhận định chủ quan đầy sai lầm của con người. Tính toán lượng tử chạy song song hàng triệu giả lập biến số phức tạp để tìm ra điểm cân bằng tối ưu cho danh mục All-Weather."},
    6: {"title": "Đo lường độ dày con hào kinh tế độc quyền thương mại", "focus": "Hào bảo vệ kinh tế rộng lớn rộng mở là rào cản tối thượng ngăn chặn sự xâm lấn của đối thủ.", "context": "Một lâu đài kinh doanh dù tráng lệ đến đâu cũng sẽ bị sụp đổ nếu không có một con hào bảo vệ đủ sâu và dày. Trạm Terminal ứng dụng trí tuệ nhân tạo (AI) để phân tích cấu trúc chi phí thực tế và kiểm tra năng lực giữ vững thị phần của doanh nghiệp niêm yết trên cả 3 sàn. Việc số hóa chuỗi giá trị lên Blockchain giúp nhà đầu tư bóc tách thực chất các rào cản thương mại mà đối thủ không thể sao chép. Bằng các giả lập toán học lượng tử, chúng tôi mô phỏng áp lực cạnh tranh cực đoan để đo lường độ chịu đựng của doanh nghiệp, giúp những người tích sản từ số vốn nhỏ yên tâm nắm giữ cổ phần vĩnh viễn xuyên chu kỳ."},
    7: {"title": "Kỷ luật thép và tư duy đảo ngược bài toán rủi ro danh mục", "focus": "Để gặt hái thành công vĩ đại, trước khi lập kế hoạch kiếm tiền phải tối ưu hóa quy trình tránh mất tiền.", "context": "Đảo ngược, luôn luôn đảo ngược. Đó là bí quyết tư duy tối cao của các bậc thầy tài chính thượng tầng. Trước khi lập kế hoạch kiếm lợi nhuận, trạm Terminal của chúng tôi sử dụng AI để tìm kiếm mọi kịch bản tồi tệ nhất có thể hủy diệt doanh nghiệp. Cấu trúc Blockchain khép kín được áp dụng để thiết lập các hợp đồng thông minh tự động khóa vị thế bảo vệ tài khoản khi có dấu hiệu căng thẳng thanh khoản hệ thống. Phân tích lượng tử hỗ trợ đo lường mức độ sụt giảm tài sản để đưa ra tỷ lệ phân bổ tối ưu. Kỷ luật không phải là sự gò bó, kỷ luật chính là sự tự do tối thượng giúp bảo vệ trọn vẹn gia sản của bạn vĩnh viễn."},
    8: {"title": "Bản địa hóa tiêu chuẩn chọn doanh nghiệp Blue-chip nội địa", "focus": "Sàng lọc các doanh nghiệp sở hữu lợi nhuận từ hoạt động lõi, loại bỏ lợi nhuận ảo từ đất đai.", "context": "Không thể áp dụng một cách rập khuôn các công thức tài chính của Phố Wall vào thị trường chứng khoán Việt Nam. Hạ tầng định lượng của Pentech Premium tích hợp AI để bóc tách và bản địa hóa các bộ lọc dữ liệu phù hợp với hệ thống pháp lý và hành vi của nhà đầu tư nội địa. Mọi thông tin về cấu trúc sở hữu cổ đông lớn được đồng bộ trên Blockchain nhằm phát hiện sớm các hành vi thao túng giá phi pháp đứng sau màn nhung truyền thông. Phân tích lượng tử đo lường quán tính dòng vốn FDI vĩ mô để đón đầu các chu kỳ lớn, giúp nhà đầu tư độc lập tự tin nắm giữ danh mục Blue-chip sạch sẽ xuyên qua mọi giông bão kinh tế số."},
    9: {"title": "Tư duy cấp thiết bậc hai vượt trên nhận thức thông thường đám đông", "focus": "Đứng tách biệt khỏi bẫy tâm lý mỏ neo ngắn hạn, kiên định tích sản tại các vùng giá chiết khấu sâu.", "context": "Tư duy cấp độ một chỉ nhìn vào những biểu hiện trực quan đơn giản: 'Doanh nghiệp tốt, hãy mua cổ phiếu'. Tư duy cấp độ hai đi sâu vào bản chất cấu trúc giá trị: 'Doanh nghiệp tốt nhưng mọi người đều biết và định giá quá đắt, hãy tránh xa'. Hệ thống AI phân tích ngôn ngữ tự nhiên (NLP) của Pentech Premium liên tục quét qua tất cả các phương tiện truyền thông nhằm mục đích đo lường mức độ đồng thuận cực đoan của thị trường. Dữ liệu được lưu vết bảo mật trên Blockchain giúp nhà đầu tư độc lập đưa ra các quyết định dựa trên logic toán học, loại bỏ hoàn toàn bẫy tâm lý mỏ neo ngắn hạn. Các mô hình lượng tử tính toán xác suất sai lầm trong nhận thức của đám đông để kích hoạt lệnh giải ngân chính xác tại những vùng giá hời bị bỏ sót, kiến tạo hiệu quả sinh lời phi thường."},
    10: {"title": "Định vị vị thế chu kỳ vĩ mô và cấu trúc dòng tiền hệ thống", "focus": "Nhà đầu tư thông minh bắt buộc phải phân loại danh mục một cách khoa học thành các nhóm vị thế rạch ròi.", "context": "Hiểu được vị thế chu kỳ vĩ mô giúp nhà đầu tư tránh được việc đi ngược lại xu thế lớn của dòng tiền hệ thống. Bộ máy định lượng của chúng tôi ứng dụng trí tuệ nhân tạo (AI) để phân tích sự tương quan giữa chính sách tiền tệ toàn cầu và dòng vốn nội địa thực tế. Mọi số liệu vĩ mô được mã hóa bất biến trên hạ tầng Blockchain nhằm đảm bảo tính khách quan tối thượng, không bị bóp méo bởi các tin tức nhiễu ngắn hạn. Điện toán lượng tử hỗ trợ mô phỏng ma trận dòng tiền liên ngân hàng để phát hiện sớm các dấu hiệu đóng băng thanh khoản nguy hiểm trước khi thị trường thực tế kịp phản ứng."},
    11: {"title": "Chiến lược bảo tồn nguồn vốn vĩnh viễn đề phòng mất tiền", "focus": "Rủi ro lớn nhất không phải là biến động giá ngắn hạn mà là khả năng mất vốn vĩnh viễn không thể phục hồi.", "context": "Bảo tồn vốn là quy tắc số một, và quy tắc số hai là không bao giờ được phép quên quy tắc số một. Thuật toán AI của Pentech Premium thực hiện quy trình kiểm toán hiệu năng độc lập đối với mọi pháp nhân niêm yết trên 3 sàn, kiên quyết loại bỏ hoàn toàn các doanh nghiệp có cấu trúc tài chính rỗng ruột hoặc nợ vay quá lớn. Bằng cách áp dụng Blockchain, chúng tôi theo dõi tính xác thực của các chuỗi hợp đồng kinh doanh lớn, đảm bảo dòng thu nhập sinh ra là thực chất 100%. Giả lập lượng tử được kích hoạt để chạy thử nghiệm sức chống chịu của danh mục trước kịch bản thiên nga đen cực đoan nhất có thể diễn ra."},
    12: {"title": "Tối ưu hóa hiệu suất sinh lời bằng cấu trúc chi phí thấp nhất", "focus": "Kiên quyết gạt bỏ bẫy trading ngắn hạn liên tục, tối ưu hóa lãi kép bằng cơ chế nắm giữ tài sản lâu dài.", "context": "Mọi tầng lớp chi phí giao dịch ẩn phát sinh từ hành vi mua bán vô tội vạ chính là kẻ thù thầm lặng tàn phá cấu trúc lãi kép của tài khoản tích sản. Pentech Premium ứng dụng mô hình AI xử lý tự động quy trình lọc số liệu mà không sinh thêm bất kỳ chi phí trung gian thương mại nào. Nhật ký phân bổ được lưu trữ bảo mật trên Blockchain giúp bảo toàn dòng tiền cổ tức tiền mặt ròng dồi dào. Toán học lượng tử tinh chỉnh tần suất cơ cấu danh mục tối ưu, gỡ bỏ hoàn toàn rào cản thuật ngữ phức tạp. Hãy nhớ rằng mỗi đồng tiền bạn tiết kiệm được chính là một viên gạch vững chắc xây dựng nên tòa tháp tự do tài chính vĩnh cửu."},
    13: {"title": "Ma trận phân loại 6 nhóm vị thế cổ phiếu chiến lược", "focus": "Áp dụng rạch ròi mục tiêu hiệu suất kỳ vọng và quy tắc quản trị rủi ro phù hợp cho từng nhóm cổ phiếu.", "context": "Nhà đầu tư thông thái bắt buộc phải phân chia danh mục một cách khoa học thành các nhóm vị thế chiến lược chiến thuật rạch ròi. Bộ máy AI nâng cao của chúng tôi tự động quét lọc chuỗi dữ liệu thời gian thực để phân chia rổ tài sản. Dữ liệu phân loại được mã hóa phi tập trung trên hạ tầng Blockchain bảo mật, tạo hệ quy chiếu đối chiếu song song sạch sẽ. Thuật toán lượng tử tính toán mức độ tương quan tài sản để tối ưu hóa biên an toàn cho danh mục tổng All-Weather, giúp những người vốn nhỏ tự tin nắm giữ lâu dài xuyên thế kỷ."},
    14: {"title": "Phương pháp Scuttlebutt điều tra thực địa vĩ mô doanh nghiệp", "focus": "Trực tiếp kiểm chứng hiệu năng sản phẩm thực tế của doanh nghiệp mục tiêu trước khi đưa ra lệnh giải ngân.", "context": "Phương pháp Scuttlebutt đòi hỏi nhà quản trị tài sản chuyên nghiệp phải kết hợp giữa số liệu lý thuyết và điều tra thực địa vĩ mô. Trạm Terminal hỗ trợ quy trình này bằng cách ứng dụng AI cào thông tin dữ liệu từ hàng triệu đánh giá số và xu hướng trực tuyến. Hệ thống số hóa luồng dữ liệu thô thu thập được lên hạ tầng Blockchain bất biến nhằm triệt tiêu hoàn toàn các thông tin quảng cáo nhiễu mục đích thương mại phi thực tế. Mô phỏng lượng tử tính toán tốc độ mở rộng điểm bán để dự báo điểm rơi doanh thu tương lai khép kín."},
    15: {"title": "Cấu hình chiến lược Focus tập trung phân khúc chuyên biệt", "focus": "Biên lợi nhuận hoạt động duy trì ở mức cao nhờ dẫn đầu chi phí thấp hoặc khác biệt hóa sản phẩm rõ rệt.", "context": "Theo các nguyên lý chiến lược kinh điển, một mô hình kinh doanh không thể là tất cả đối với mọi phân khúc khách hàng ngoài thị trường. Hệ thống AI số liệu của Pentech Premium bóc tách cấu trúc giá trị của từng pháp nhân để kiểm tra tính thực chất của chiến lược tập trung. Mọi thông tin về thị phần và biên lợi nhuận ngách được xác thực trên hạ tầng Blockchain bảo mật, loại bỏ hoàn toàn các báo cáo quảng cáo sáo rỗng mục đích thương mại phi thực tế. Thuật toán lượng tử mô phỏng mức độ bứt phá ra khỏi các khoảng trống thị trường để tìm kiếm không gian giá trị đại dương xanh vô tận."},
    16: {"title": "Quy tắc kiểm toán cấu trúc rủi ro và nhận diện tư duy cấp độ hai", "focus": "Áp dụng tư duy rạch ròi cấp độ hai để đưa ra hành động giải ngân ngược hướng đám đông hoang tưởng.", "context": "Học viện VIP phân tích rằng tư duy cấp độ một chỉ nhìn vào bề nổi trực quan, trong khi tư duy cấp độ hai đòi hỏi một cấu trúc phân tích đa biến sâu sắc hơn rất nhiều. Hệ thống máy học AI nâng cao của chúng tôi thực hiện quét lọc ngôn ngữ truyền thông, đo lường chính xác mức độ đồng thuận cực đoan của đám đông hoang tưởng nhằm phát hiện bẫy mỏ neo tâm lý ngắn hạn. Mọi số liệu về biên an toàn phòng thủ được mã hóa phi tập trung trên hạ tầng Blockchain bảo mật, mang lại một hệ quy chiếu đối chiếu song song hoàn toàn sạch sẽ. Thuật toán lượng tử chạy các mô phỏng kịch bản biến động đa biến giúp nhà đầu tư độc lập nhìn thấu bản chất thực chất của cấu trúc rủi ro liên ngành."},
    17: {"title": "Chiến lược quản trị chu kỳ nợ vĩ mô liên ngành chuyên sâu", "focus": "Kiên quyết thu hẹp tỷ trọng đòn bẩy margin ngắn hạn trước khi điểm gãy chu kỳ chính thức diễn ra.", "context": "Toàn bộ thị trường tài chính thế kỷ 21 vận hành bám sát các đại chu kỳ thắt thắt mở mở của hệ thống nợ vay tín dụng. Bộ máy vĩ mô của Pentech Premium ứng dụng AI để phân tích sự dịch chuyển dòng vốn liên quốc gia, loại bỏ mọi thông tin quảng bá sáo rỗng phi thực tế của báo chí thương mại ngoài xã hội. Nhật ký diễn biến lãi suất và lạm phát được lưu trữ bất biến trên Blockchain nhằm mang lại giải pháp công nghệ giả lập cấu trúc tài sản minh bạch nhất cho người Việt từ số vốn nhỏ từ 250k. Mô hình điện toán lượng tử tính toán ma trận tương quan đa biến, giúp nhà quản trị đưa tổng tài sản về trạng thái bảo thủ nghiêm ngặt."},
    18: {"title": "Quy tắc kiểm soát chi phí trung gian và tối ưu dòng cổ tức", "focus": "Giữ tính kỷ luật thép hành động, coi sự kiên nhẫn nắm giữ dài hạn là vũ khí tối cao sinh tồn vĩnh cửu.", "context": "Nhà đầu tư cá nhân nhỏ lẻ thua cuộc phần lớn không phải vì chọn sai doanh nghiệp, mà vì họ đã cống hiến quá nhiều lợi nhuận cho các bẫy phí và thuế giao dịch phát sinh từ bẫy tâm lý trading ngắn hạn liên tục. Trạm Terminal của chúng tôi phá vỡ hoàn toàn rào cản này bằng cách tự động hóa quy trình lọc chỉ số EPS, ROE, ROI của cả 3 sàn sạch sẽ. Ứng dụng Blockchain phi tập trung loại bỏ nhu cầu về các bên trung gian xác thực phi lý ngoài xã hội, giúp dòng tiền chiết khấu của bạn phát huy sức mạnh cấp số nhân vĩnh cửu. Phân tích lượng tử tối ưu hóa lộ trình giải ngân vốn hời."},
    19: {"title": "Ma trận phân loại rủi ro kế toán và màng mọc chỉ số sạch", "focus": "Không bao giờ gõ lệnh giải ngân dựa trên các kỳ vọng ảo tưởng thiếu số liệu toán học chứng minh.", "context": "Bẫy giá trị và rủi ro gian lận kế toán luôn là nỗi ám ảnh đối với các danh mục đầu tư tích sản thiếu công cụ rà soát độc lập. Thuật toán AI nâng cao của chúng tôi tự động gắn nhãn và phân tách các dấu hiệu rủi ro tiềm ẩn trên báo cáo tài chính lý thuyết của 3 sàn. Dữ liệu phân loại được đồng bộ hóa phi tập trung trên hạ tầng Blockchain bảo mật, mang lại hệ quy chiếu khách quan tuyệt đối để người dùng đối chiếu song song thời gian thực. Giả lập lượng tử phân tích ma trận cạnh tranh liên ngành, đánh giá xem hào kinh tế của doanh nghiệp có thể bị lung lay trước làn sóng biến động kỹ nghệ kỷ nguyên số huỷ diệt hay không."},
    20: {"title": "Phương pháp thực địa Scuttlebutt và phòng ngự thiên nga đen vĩ mô", "focus": "Kiên quyết đóng vị thế bảo vệ nguồn vốn giải ngân khi phát hiện dấu hiệu gãy trục thực địa.", "context": "Tư duy thực địa chuyên sâu Scuttlebutt yêu cầu nhà quản trị tài sản bắt buộc phải kết hợp giữa số liệu văn phòng và thực tế đời sống. Hệ thống định lượng Pentech Premium hỗ trợ quy trình này bằng cách ứng dụng AI để cào dữ liệu định lượng tự động từ hàng triệu xu hướng tìm kiếm trực tuyến thời gian thực. Chúng tôi số hóa luồng dữ liệu thô thu thập được lên hạ tầng Blockchain bất biến nhằm triệt tiêu hoàn toàn các thông tin quảng cáo nhiễu mục đích thương mại phi thực tế. Thuật toán lượng tử mô phỏng các cú sốc thiên nga đen giả định, giúp bạn Quân thiết lập hàng rào phòng thủ vững chắc cho tài khoản cá nhân."},
    21: {"title": "Quy tắc bóc tách và bẻ gãy ma trận đòn bẩy tài chính rủi ro", "focus": "Thiết lập quy tắc phòng thủ bảo thủ, tuyệt đối không lạm dụng ký quỹ margin ngắn hạn theo đám đông.", "context": "Trong các giai đoạn thị trường hưng hấn cực đoan, đòn bẩy nợ vay luôn là công cụ khiến đám đông hoang tưởng về mức sinh lời giả tạo. Trạm Terminal của chúng tôi tích hợp bộ máy AI chuyên sâu để theo dõi chặt chẽ dòng tiền vay nợ toàn chuỗi hệ thống liên ngành, phát hiện sớm các dấu hiệu căng thẳng tín dụng trước khi điểm gãy chính thức xảy ra. Sổ cái Blockchain lưu trữ các chỉ số đòn bẩy bất biến, giúp bạn có một hệ quy chiếu định lượng hoàn toàn sạch sẽ để đưa ra các quyết định phân bổ nguồn vốn một cách sáng suốt. Mô phỏng toán học lượng tử hỗ trợ đo lường tác động của lãi suất đến giá trị tài sản ròng hữu hình."},
    22: {"title": "Chiến lược nhận diện bẫy giá trị của các doanh nghiệp rỗng ruột", "focus": "Chỉ giải ngân vốn vào những pháp nhân có lâu đài kinh doanh được bảo vệ bởi con hào rộng lớn.", "context": "Bẫy giá trị là nơi chôn vùi nguồn vốn của rất nhiều nhà đầu tư cá nhân do thói quen mua cổ phiếu chỉ dựa vào đồ thị giảm giá sâu. Hệ thống trí tuệ nhân tạo (AI) của Pentech Premium thực hiện bóc tách chuyên sâu hiệu quả sử dụng tài sản ROA và ROI thực chất, vạch trần các thủ thuật thổi phồng doanh thu ảo trên báo cáo kế toán lý thuyết. Thông tin đối chiếu được đồng bộ hóa bất biến trên hạ tầng Blockchain giúp bạn có cái nhìn khách quan tuyệt đối. Thuật toán lượng tử mô phỏng ma trận suy thế để kiểm tra sức chống chịu của mô hình thương mại doanh nghiệp, giúp những người vốn nhỏ tự tin nắm giữ tài sản lâu dài."},
    23: {"title": "Quy tắc kiểm soát điểm rơi thanh khoản hệ thống vĩ mô", "focus": "Lộ trình rút thặng dư vốn thông minh để xoay vòng tài chính phục vụ cho kinh doanh thực tế ngách.", "context": "Hạ tầng học viện VIP phân tích sâu sắc rằng quản trị thanh khoản thực tế là xương sống cốt lõi để sinh tồn. Khi thị trường tài chính thế giới rơi vào điểm cực đoan của cuộc khủng hoảng tín dụng, toàn bộ đám đông hoảng loạn sẽ giẫm đạp lên nhau để tháo chạy. Trạm Terminal của bạn Quân ứng dụng hệ thống Trí tuệ nhân tạo (AI) để liên tục quét hành vi đặt lệnh thời gian thực, đo lường tốc độ trượt giá của các định chế tổ chức lớn. Mọi quy trình luân chuyển được Blockchain ghi vết nhằm bảo mật tuyệt đối, mang lại một trạm dữ liệu sạch sẽ, không chứa thông tin quảng cáo quảng bá phi lý. Mô hình tính toán lượng tử chạy giả lập đa biến biến số, giúp bạn Quân thiết lập lộ trình rút thặng dư vốn từ cổ phiếu đầu cơ nóng để chuyển dịch dòng tiền thực tế về xây dựng kho hàng thiết bị gia dụng và máy lọc nước an toàn tại Thái Nguyên, bảo tồn gia sản bền vững dài hạn xuyên thế kỷ."},
    24: {"title": "Chiến lược quản trị ma trận tương quan tài sản liên ngành nâng cao", "focus": "Lộ trình tích sản an toàn bền vững vĩnh viễn, loại bỏ toàn bộ rào cản thuật ngữ phức tạp.", "context": "Nội dung chuyên sâu của bài học số 24 tập trung bẻ gãy lối tư duy đa dạng hóa sáo rỗng thông thường ngoài xã hội. Hệ sinh thái định lượng AI cao cấp thực hiện bóc tách hệ số đồng biến dòng tiền của các phân khúc doanh nghiệp niêm yết liên sàn. Chúng tôi lưu vết các thuật toán trọng số phân bổ lên hạ tầng Blockchain bảo mật, giúp bảo an toàn tuyệt đối cấu trúc tài khoản. Mô phỏng điện toán lượng tử dự báo các điểm gãy rủi ro của chu kỳ nợ vĩ mô, đảm bảo danh mục luôn vận hành ổn định trong cả 4 môi trường kinh tế biến động khốc liệt nhất. Đây là bệ phóng giáo dục tài chính sớm cho thế hệ trẻ từ 15 tuổi hình thành tính kỷ luật thép hành động, chạm mốc tự do thực sự."},
    25: {"title": "Nguyên tắc bóc tách bẫy tâm lý sợ bỏ lỡ cơ hội ở vùng cực đoan", "focus": "Giúp người có số vốn nhỏ kiên định giữ vững kỷ luật thép hành động tích lũy từ 250k.", "context": "Bẫy tâm lý sợ bỏ lỡ cơ hội (FOMO) là vũ khí tối thượng mà Ngài Thị Trường sử dụng để tước đoạt thành quả lao động của đám đông. Trạm Terminal của chúng tôi tích hợp bộ máy AI tiên tiến để đo lường chỉ số hoang tưởng toàn diện, giúp bạn nhìn thấu bản chất thực sự của các đợt kéo giá đẩy ảo thương mại. Cấu trúc sổ cái Blockchain lưu giữ dữ liệu định giá lịch sử sạch sẽ bất biến, mang lại một hệ quy chiếu logic toán học vững chắc. Phân tích lượng tử mô phỏng ma trận hành vi, giúp những người vốn nhỏ kiên định giữ vững kỷ luật thép hành động, tích lũy tài sản an toàn từ những số vốn nhỏ nhất từ 250k một cách khoa học bền vững."},
    26: {"title": "Chiến lược bảo tồn thặng dư vốn và xoay vòng nguồn lực an toàn", "focus": "Thực thi chiến lược capital rotation, rút lãi sàn chứng khoán để tái tài trợ tổng lực kinh doanh.", "context": "Đỉnh cao của tư duy quản trị tài sản cao cấp nằm ở năng lực biết rút lui đúng thời điểm chu kỳ đạt ngưỡng cực đoan hưng phấn. Trạm Terminal Pentech Premium ứng dụng thuật toán AI để thiết lập hệ thống cảnh báo sớm, bóc tách các điểm nghẽn thanh khoản vĩ mô. Mọi nhật ký luân chuyển vốn được mã hóa bất biến trên hạ tầng Blockchain, giúp bạn Quân bảo mật cấu trúc nguồn lực. Hệ thống tính toán lượng tử hỗ trợ thiết lập danh mục All-Weather chống chịu va đập mạnh, hướng tới mục tiêu giáo dục tài chính sớm cho trẻ em từ 15 tuổi có tư duy kỷ luật thép, làm chủ hoàn toàn vận mệnh kinh tế cá nhân dài hạn bền vững vĩnh cửu."},
    27: {"title": "Quy tắc kiểm soát rủi ro cực đoan và thiết lập điểm gãy vĩ mô", "focus": "Phân bổ nguồn lực vốn vào các kênh phòng vệ vững chắc hữu hình an toàn tối thượng vĩnh viễn.", "context": "Lịch sử chứng minh rằng các định chế kinh tế vĩ mô toàn cầu luôn vận hành theo một đại chu kỳ lớn có tính chất lặp lại khép kín. Bộ máy định lượng Pentech Premium tích hợp Trí tuệ nhân tạo (AI) để phân tích ma trận rủi ro hệ thống, loại bỏ mọi thông tin nhiễu từ truyền thông quảng bá phi lý ngoài xã hội. Sổ cái Blockchain lưu vết các điểm rơi giá trị, mang lại giải pháp công nghệ giả lập cấu trúc tài sản sạch sẽ nhất cho người Việt từ vùng số vốn nhỏ từ 250k. Tính toán lượng tử hỗ trợ phân bổ nguồn lực vào các kênh phòng vệ vững chắc như vàng hoặc các cổ phiếu hạ tầng thiết yếu vĩ mô, bảo hộ gia sản vĩnh viễn dài hạn."},
    28: {"title": "Chiến lược xây dựng trục nguyên tắc đầu tư giá trị bất biến", "focus": "Kiên định giải ngân tiền mặt gom mua Blue-chip nội địa xuất sắc vùng chiết khấu sâu lý tưởng.", "context": "Thiết lập một hệ thống nguyên tắc hành động nghiêm ngặt chính là tấm khiên tối cao bảo vệ bạn khỏi sự điên cuồng của Ngài Thị Trường. Nhà sáng lập Trần Anh Quân định hướng Pentech Premium số hóa trọn vẹn tri thức kinh điển vào các hợp đồng thông minh trên Blockchain, loại bỏ hoàn toàn sự can thiệp từ cảm xúc cá nhân. Hệ thống AI liên tục giám sát chất lượng nội tại doanh nghiệp, đảm bảo dòng tiền thặng dư sinh ra là thực chất 100%. Phân tích lượng tử hỗ trợ tối ưu hóa trọng số danh mục All-Weather, giúp nhà đầu tư nhỏ lẻ an tâm tích lũy tài sản dài hạn vững chắc, tiến bước mạnh mẽ trên lộ trình kiến tạo sự tự do tài chính tối thượng vĩnh cửu."},
    29: {"title": "Quy tắc bóc tách chu kỳ nợ vĩ mô và điểm gãy của các quốc gia", "focus": "Mô hình lượng tử phân tích ma trận nợ hệ thống để cơ cấu tài sản an toàn dài hạn.", "context": "Thấu hiểu quy luật phá sản của các định chế vĩ mô lớn giúp nhà đầu tư độc lập bảo vệ trọn vẹn thành quả nguồn vốn vĩnh cửu. Trạm Terminal của chúng tôi tích hợp thuật toán AI để giám sát sự dịch chuyển của dòng vốn liên quốc gia và sự biến động của trục tỷ giá vĩ mô. Mọi dữ liệu kinh tế được lưu trữ phi tập trung trên hạ tầng Blockchain bảo mật, loại bỏ hoàn toàn các thông tin quảng bá sáo rỗng phi thực tế. Mô hình lượng tử phân tích ma trận rủi ro nợ vay hệ thống, giúp bạn đưa ra quyết định cơ cấu tài sản an toàn tối thượng dài hạn. Hãy nhớ rằng việc làm chủ tri thức vĩ mô chính là hàng rào bảo vệ vững chắc nhất cho tòa tháp tài chính tự do vĩnh cửu của bạn."},
    30: {"title": "Chiến lược tư duy đảo ngược bài toán rủi ro hệ thống tài sản", "focus": "Hợp đồng thông minh Blockchain thực thi kỷ luật tự động hóa gõ lệnh gác cửa nguồn vốn nghiêm ngặt.", "context": "Đảo ngược, luôn luôn đảo ngược. Đó là bí quyết tư duy tối cao của nhà sáng lập Trần Anh Quân trong quản trị cấu trúc tài sản. Trí tuệ nhân tạo (AI) của chúng tôi chạy hàng triệu giả lập điểm chết của doanh nghiệp niêm yết để chủ động loại bỏ rủi ro vĩnh viễn mất vốn. Hợp đồng thông minh trên Blockchain thực thi kỷ luật tự động hóa gõ lệnh gác cửa nguồn vốn một cách nghiêm ngặt vô điều kiện. Phân tích lượng tử đo lường ma trận xác suất thiên nga đen, mang lại một trạm tra cứu Terminal sạch sẽ, minh bạch nhất. Làm chủ tư duy đảo ngược rủi ro chính là bệ đỡ vững chắc giúp những nhà đầu tư nhỏ lẻ yên tâm tích lũy tài sản an toàn xuyên thế kỷ."},
    31: {"title": "Nguyên tắc thiết lập bộ lọc kỷ luật thép trong hành động giải ngân", "focus": "Mô hình toán học lượng tử tối ưu tần suất phân bổ dòng tiền thặng dư vĩnh cửu.", "context": "Kỷ luật thép không phải là sự gò bó ép buộc, kỷ luật thép chính là sự tự do tối thượng bảo vệ trọn vẹn gia sản lâu dài của bạn. Hệ thống định lượng Pentech Premium ứng dụng AI để tự động giám sát và khóa các hành vi trading theo cảm tính của người dùng. Mọi hành vi gõ lệnh phân bổ vốn được xác thực bất biến trên hạ tầng Blockchain bảo mật, xây dựng một lịch sử đầu tư sạch sẽ khoa học. Toán học lượng tử hỗ trợ tối ưu hóa tần suất phân bổ dòng tiền thặng dư, giúp học viên giáo dục tài chính sớm từ năm 15 tuổi hình thành tư duy bản lĩnh, tính disciplined thép để làm chủ cuộc chơi tài chính dài hạn một cách chắc chắn bền vững vĩnh cửu."},
    32: {"title": "Chiến lược đón đầu làn sóng dịch chuyển đại chu kỳ thay đổi thế giới", "focus": "Cấu trúc Blockchain phi tập trung bảo vệ dữ liệu vĩ mô sạch sẽ bất biến hoàn toàn.", "context": "Hiểu được quy luật trật tự thế giới đang thay đổi giúp nhà đầu tư độc lập định vị chính xác hướng đi của dòng tiền thông minh toàn cầu. Trạm Terminal của chúng tôi ứng dụng trí tuệ nhân tạo (AI) để phân tích dòng chuyển dịch FDI và sự lệch pha của các chu kỳ kinh tế lớn. Cấu trúc Blockchain phi tập trung bảo vệ dữ liệu vĩ mô sạch sẽ, loại bỏ hoàn toàn các thông tin quảng bá sáo rỗng ngoài thị trường. Mô hình lượng tử tính toán xác suất bùng nổ của các phân khúc công nghệ mới AI, Blockchain, Lượng tử để đón đầu cơ hội bứt phá gia sản. Hãy biến tri thức chiến lược thượng tầng thành tấm khiên vững chắc bảo hộ nguồn lực tài chính cho tương lai mai sau."},
    33: {"title": "Quy tắc tích sản an toàn từ những số vốn nhỏ nhất cho đại chúng", "focus": "Kiên trì thực hiện lộ trình tích lũy an toàn và bền vững từ số vốn 250k mỗi ngày.", "context": "Sử mệnh cao cả phụng sự xã hội của Pentech Premium chính là kiến tạo cơ hội tiếp cận tri thức và hạ tầng tài chính công bằng cho người Việt. Chúng tôi ứng dụng thuật toán AI để thiết lập hệ thống giả lập công nghệ hỗ trợ cấu trúc tài sản minh bạch tối đa cho cộng đồng đại chúng. Mọi quy trình tích lũy nhỏ được ghi nhận và bảo mật tuyệt đối qua Blockchain sổ cái, mang lại sự an tâm vững chắc dài hạn vĩnh cửu. Mô hình lượng tử tính toán tối ưu tần suất phân bổ nguồn vốn, biến những số vốn nhỏ bé ban đầu thành hòn tuyết lãi kép lăn khổng lồ. Tự do tài chính không phải là giấc mơ xa vời, đó là phần thưởng dành cho những ai biết làm chủ vận mệnh bằng kỷ luật thép và tư duy thông thái."},
    34: {"title": "Chiến lược bóc tách và vô hiệu hóa con hào cạnh tranh đối thủ", "focus": "Sổ cái Blockchain bảo mật lịch sử thị phần bất biến, loại bỏ hoàn toàn các báo cáo kế toán ảo.", "context": "Đo lường độ dày con hào kinh tế độc quyền thương mại là chìa khóa để bảo vệ nguồn vốn đầu tư tích sản dài hạn không bị lỗi thời. Hệ thống định lượng Terminal ứng dụng AI phân tích ma trận cạnh tranh vĩ mô, bóc tách thực chất các rào cản chi phí sản xuất thấp của doanh nghiệp. Sổ cái Blockchain bảo mật lịch sử thị phần bất biến, loại bỏ hoàn toàn các báo cáo ảo thổi phồng từ bộ phận truyền thông thương mại. Thuật toán lượng tử mô phỏng các đòn tấn công giảm giá liên ngành, đảm bảo hào phòng thủ của mã cổ phiếu bạn sở hữu như FPT, VGI luôn vững chắc xuyên suốt mọi chu kỳ suy thoái khốc liệt, mang lại sự thịnh vượng vĩnh cửu bền vững dài hạn dài lâu."},
    35: {"title": "Quy trình tổng lực Quản trị tài sản cao cấp Pentech Premium", "focus": "Mọi hành vi phân bổ dòng tiền đều được định hướng giáo dục tài chính sớm từ năm 15 tuổi.", "context": "Bài học chốt hạ số 35 chính là trục định vị giá trị thực chất cao cấp nhất mà Nhà sáng lập Trần Anh Quân trao tặng cho cộng đồng người Việt. Chúng tôi loại bỏ toàn bộ các rào cản thuật ngữ phức tạp, ứng dụng Trí tuệ nhân tạo (AI) để cào giá tự động và phân tích dữ liệu vĩ mô, kết hợp tính bảo mật minh bạch tuyệt đối của Blockchain sổ cái phi tập trung và tốc độ tính toán xác suất đa biến của Điện toán lượng tử. Mọi hành vi phân bổ nguồn vốn được định hướng giáo dục tài chính sớm từ năm 15 tuổi hình thành tư duy kỷ luật thép làm chủ vận mệnh kinh tế. Bất cứ lúc nào trong quá trình thực chiến hành động, Đường dây nóng Ban điều hành **0327.625.853** luôn trực chiến để hỗ trợ bạn cơ cấu tài sản, bảo an toàn vốn vĩnh viễn và cấu hình bảo mật thông tin tối thượng xuyên chu kỳ thế kỷ."}
}

strategies_35 = []
for i in range(1, 36):
    if i in core_lessons:
        lesson_instance = core_lessons[i]
        lesson_instance["id"] = i
        strategies_35.append(lesson_instance)

for strat in strategies_35:
    strat["desc"] = f"1. Tư duy nền tảng: Thực thi quy trình bóc tách và định lượng hóa danh mục chiến lược bài số {strat['id']}.\n" \
                    f"2. Bộ lọc định lượng: Ứng dụng AI phân tích sâu sắc các chỉ số cơ bản EPS, ROE, ROI thời gian thực.\n" \
                    f"3. Nhận diện hào bảo vệ: {strat['focus']}\n" \
                    f"4. Điểm gãy rủi ro: Kích hoạt hệ thống cảnh báo dừng giải ngân tự động khi cấu trúc dòng tiền lõi biến động cực đoan.\n" \
                    f"5. Thực chiến Việt Nam: Đồng bộ màng lọc bám sát ma trận sinh lời của các mã dẫn dắt như FPT, VGI, CTR, MCH.\n" \
                    f"6. Kỷ luật hành động: Tuân thủ cấu trúc danh mục All-Weather, giữ tính kỷ luật thép làm chủ vận mệnh kinh tế.\n\n" \
                    f"💥 LUẬN ĐIỂM CHUYÊN SÂU TỪ KHỐI TRI THỨC THƯỢNG TẦNG BÀI SỐ {strat['id']}:\n{strat['context']}"

strategies_35 = sorted(strategies_35, key=lambda x: x["id"])

# ==========================================
# 4. ENGINE CÀO GIÁ 3 SÀN CHUẨN XÁC NỘI ĐỊA CỦA HOSE INDEX KỲ 1/2026
# ==========================================
corporate_market_db = {
    "ACB": {"name": "Ngân hàng TMCP Á Châu", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 3150, "growth": 14, "roe": 22.1, "roi": 15.4, "moat": "Quản trị rủi ro tín dụng sạch top 1 hệ thống ngân hàng tư nhân", "fallback_price": 28500},
    "BID": {"name": "Ngân hàng TMCP Đầu Tư và Phát triển Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 4200, "growth": 16, "roe": 18.5, "roi": 12.1, "moat": "Vị thế định chế tài chính quốc doanh quy mô tổng tài sản khổng lồ", "fallback_price": 49000},
    "CTG": {"name": "Ngân Hàng TMCP Công Thương Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 3900, "growth": 15, "roe": 17.2, "roi": 11.5, "moat": "Trụ cột tín dụng vĩ mô phục vụ các ngành công nghiệp trọng điểm", "fallback_price": 35500},
    "DGC": {"name": "CTCP Tập đoàn Hóa chất Đức Giang", "exchange": "HOSE", "sector": "NGUYÊN VẬT LIỆU", "eps": 7800, "growth": 18, "roe": 29.5, "roi": 21.2, "moat": "Độc quyền lâu đời về công nghệ chế biến sâu phốt pho vàng xuất khẩu quốc tế", "fallback_price": 115000},
    "FPT": {"name": "CTCP FPT", "exchange": "HOSE", "sector": "CÔNG NGHỆ THÔNG TIN", "eps": 6200, "growth": 25, "roe": 26.0, "roi": 19.1, "moat": "Độc quyền xuất khẩu phần mềm và hệ thống giáo dục công nghệ", "fallback_price": 135000},
    "GAS": {"name": "Tổng Công ty Khí Việt Nam-CTCP", "exchange": "HOSE", "sector": "NĂNG LƯỢNG", "eps": 5600, "growth": 12, "roe": 19.8, "roi": 14.6, "moat": "Độc quyền thống trị hạ tầng khai thác và phân phối khí hóa lỏng", "fallback_price": 82000},
    "GVR": {"name": "Tập đoàn Công nghiệp Cao su Việt Nam - CTCP", "exchange": "HOSE", "sector": "NGUYÊN VẬT LIỆU", "eps": 1950, "growth": 11, "roe": 10.5, "roi": 8.2, "moat": "Sở hữu quỹ đất khu công nghiệp khổng lồ chuyển đổi từ đất cao su", "fallback_price": 31000},
    "HDB": {"name": "Ngân hàng TMCP Phát triển TP.HCM", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 3850, "growth": 22, "roe": 23.2, "roi": 16.1, "moat": "Lợi thế khai thác tệp khách hàng độc quyền từ hệ sinh thái hàng không", "fallback_price": 26000},
    "HPG": {"name": "CTCP Tập Đoàn Hòa Phát", "exchange": "HOSE", "sector": "NGUYÊN VẬT LIỆU", "eps": 2400, "growth": 15, "roe": 16.0, "roi": 12.5, "moat": "Lợi thế dẫn đầu về chi phí sản xuất thép thấp nhất phân khúc ASEAN", "fallback_price": 29000},
    "LPB": {"name": "Ngân hàng TMCP Lộc Phát Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 3600, "growth": 26, "roe": 19.1, "roi": 13.4, "moat": "Mạng lưới bưu điện liên tỉnh phủ rộng khắp vùng sâu vùng xa Việt Nam", "fallback_price": 32000},
    "MBB": {"name": "Ngân hàng TMCP Quân Đội", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 4150, "growth": 17, "roe": 22.5, "roi": 15.1, "moat": "Tệp người dùng số bùng nôn dẫn đầu và chi phí vốn CASA cực thấp", "fallback_price": 25500},
    "MSN": {"name": "Tập đoàn Masan", "exchange": "HOSE", "sector": "HÀNG TIÊU DÙNG THIẾT YẾU", "eps": 2950, "growth": 14, "roe": 11.2, "roi": 9.5, "moat": "Hệ sinh thái bán lẻ tiêu dùng khép kín lớn nhất nội địa", "fallback_price": 76500},
    "MWG": {"name": "CTCP Đầu Tư Thế Giới Di Động", "exchange": "HOSE", "sector": "HÀNG TIÊU DÙNG", "eps": 3100, "growth": 20, "roe": 16.8, "roi": 12.4, "moat": "Chuỗi bán lẻ điện máy thống trị và đà bứt phá của chuỗi thực phẩm", "fallback_price": 64000},
    "PLX": {"name": "Tập đoàn Xăng dầu Việt Nam", "exchange": "HOSE", "sector": "NĂNG LƯỢNG", "eps": 2850, "growth": 13, "roe": 12.4, "roi": 10.1, "moat": "Độc quyền nắm giữ hơn 50% thị phần mạng lưới cây xăng bán lẻ nội địa", "fallback_price": 39000},
    "SAB": {"name": "Tổng CTCP Bia – Rượu – Nước giải khát Sài Gòn", "exchange": "HOSE", "sector": "HÀNG TIÊU DÙNG THIẾT YẾU", "eps": 5400, "growth": 10, "roe": 18.2, "roi": 14.5, "moat": "Thương hiệu bia lâu đời sở hữu hệ thống nhà máy phân phối toàn quốc", "fallback_price": 57000},
    "SHB": {"name": "Ngân hàng TMCP Sài Gòn - Hà Nội", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 2100, "growth": 12, "roe": 14.1, "roi": 10.2, "moat": "Lợi thế quy mô tài trợ phân khúc doanh nghiệp vừa và nhỏ nội địa", "fallback_price": 11500},
    "SSB": {"name": "Ngân hàng TMCP Đông Nam Á", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 1950, "growth": 13, "roe": 12.8, "roi": 9.4, "moat": "Mô hình ngân hàng bán lẻ tăng trưởng ổn định phân khúc cá nhân", "fallback_price": 16500},
    "SSI": {"name": "CTCP Chứng Khoán SSI", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 2250, "growth": 19, "roe": 15.4, "roi": 11.8, "moat": "Định chế môi giới chứng khoán sở hữu quy mô nguồn vốn lớn nhất sàn", "fallback_price": 34000},
    "STB": {"name": "Ngân hàng TMCP Sài Gòn Thương Tín", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 4400, "growth": 23, "roe": 19.5, "roi": 14.1, "moat": "Lợi thế bứt phá lợi nhuận sau khi hoàn tất xử lý xong đề án tái cơ cấu", "fallback_price": 33000},
    "TCB": {"name": "Ngân hàng TMCP Kỹ thương Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 5810, "growth": 24, "roe": 18.2, "roi": 14.8, "moat": "Lợi thế chi phí vốn CASA vượt trội và hệ sinh thái tài chính cao cấp", "fallback_price": 48500},
    "TPB": {"name": "Ngân hàng TMCP Tiên Phong", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 2350, "growth": 14, "roe": 15.1, "roi": 11.2, "moat": "Tiên phong chuyển đổi số toàn diện và hệ thống LiveBank tự động", "fallback_price": 17500},
    "VCB": {"name": "Ngân hàng TMCP Ngoại Thương Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 6800, "growth": 18, "roe": 21.0, "roi": 15.2, "moat": "Vị thế ngân hàng thương mại quốc doanh số 1 Việt Nam", "fallback_price": 91000},
    "VHM": {"name": "CTCP Vinhomes", "exchange": "HOSE", "sector": "BẤT ĐỘNG SẢN", "eps": 7200, "growth": 15, "roe": 24.5, "roi": 18.2, "moat": "Độc quyền quỹ đất bất động sản đại đô thị phân khúc cao cấp", "fallback_price": 41500},
    "VIB": {"name": "Ngân hàng TMCP Quốc tế Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 3100, "growth": 13, "roe": 21.4, "roi": 14.5, "moat": "Dẫn đầu phân khúc cho vay mua ô tô và trích xuất thẻ tín dụng số", "fallback_price": 19000},
    "VIC": {"name": "Tập Đoàn Vingroup - CTCP", "exchange": "HOSE", "sector": "BẤT ĐỘNG SẢN", "eps": 1450, "growth": 20, "roe": 8.5, "roi": 6.1, "moat": "Hệ sinh thái đa ngành lớn nhất Việt Nam từ bất động sản đến xe điện", "fallback_price": 42000},
    "VJC": {"name": "CTCP Hàng không Vietjet", "exchange": "HOSE", "sector": "CÔNG NGHIỆP", "eps": 4100, "growth": 28, "roe": 16.5, "roi": 11.4, "moat": "Thống trị thị phần hàng không chi phí thấp nội địa và quốc tế ngách", "fallback_price": 96000},
    "VNM": {"name": "CTCP Sữa Việt Nam", "exchange": "HOSE", "sector": "HÀNG TIÊU DÙNG THIẾT YẾU", "eps": 4350, "growth": 10, "roe": 23.1, "roi": 18.5, "moat": "Thương hiệu quốc gia nắm giữ hơn 50% thị phần sữa nội địa sạch", "fallback_price": 66000},
    "VPB": {"name": "Ngân hàng TMCP Việt Nam Thịnh vượng", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 2650, "growth": 16, "roe": 13.8, "roi": 10.4, "moat": "Hậu thuẫn nguồn vốn dồi dào sau thương vụ bán vốn chiến lược cho ngoại", "fallback_price": 19500},
    "VPL": {"name": "CTCP Vinpearl", "exchange": "HOSE", "sector": "HÀNG TIÊU DÙNG", "eps": 3200, "growth": 22, "roe": 15.4, "roi": 11.2, "moat": "Chuỗi tổ hợp vui chơi giải trí và nghỉ dưỡng cao cấp đầu ngành", "fallback_price": 38000},
    "VRE": {"name": "CTCP Vincom Retail", "exchange": "HOSE", "sector": "BẤT ĐỘNG SẢN", "eps": 2150, "growth": 14, "roe": 14.8, "roi": 11.5, "moat": "Độc quyền vận hành mạng lưới trung tâm thương mại quy mô lớn nhất", "fallback_price": 19000},
    "MCH": {"name": "Masan Consumer", "exchange": "UPCoM", "sector": "HÀNG TIÊU DÙNG THIẾT YẾU", "eps": 8250, "growth": 22, "roe": 32.5, "roi": 24.1, "moat": "Thương hiệu tiêu dùng thiết yếu nắm giữ thị phần thống trị tuyệt đối", "fallback_price": 134500},
    "VGI": {"name": "Viettel Toàn Cầu", "exchange": "UPCoM", "sector": "CÔNG NGHỆ THÔNG TIN", "eps": 4850, "growth": 32, "roe": 24.0, "roi": 15.8, "moat": "Độc quyền hạ tầng mạng quốc tế", "fallback_price": 92000},
    "VTP": {"name": "Tổng CTCP Bưu chính Viettel", "exchange": "HOSE", "sector": "CÔNG NGHỆ THÔNG TIN", "eps": 3950, "growth": 21, "roe": 19.5, "roi": 14.2, "moat": "Mạng lưới chuyển phát nhanh khép kín", "fallback_price": 82000},
    "BSR": {"name": "CPCP Lọc hóa dầu Bình Sơn", "exchange": "UPCoM", "sector": "NĂNG LƯỢNG", "eps": 2450, "growth": 12, "roe": 15.8, "roi": 11.4, "moat": "Nắm giữ nhà máy lọc dầu Bình Sơn cung ứng 30% nhu cầu xăng dầu", "fallback_price": 22500},
    "EIB": {"name": "Ngân hàng TMCP XNK Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 1650, "growth": 11, "roe": 11.5, "roi": 8.4, "moat": "Lợi thế lâu đời trong phân khúc tài trợ thương mại xuất nhập khẩu", "fallback_price": 18500},
    "GEE": {"name": "CTCP Điện lực Gelex", "exchange": "HOSE", "sector": "CÔNG NGHIỆP", "eps": 3100, "growth": 14, "roe": 14.2, "roi": 10.5, "moat": "Độc quyền sản xuất thiết bị điện hạ thế và thiết bị đo lường", "fallback_price": 31000},
    "MSB": {"name": "Ngân hàng TMCP Hàng Hải Việt Nam", "exchange": "HOSE", "sector": "TÀI CHÍNH", "eps": 2800, "growth": 15, "roe": 15.2, "roi": 10.9, "moat": "Mô hình ngân hàng số linh hoạt tối ưu chi phí vận hành", "fallback_price": 12000},
    "REE": {"name": "CTCP Cơ Điện Lạnh", "exchange": "HOSE", "sector": "CÔNG NGHIỆP", "eps": 4850, "growth": 13, "roe": 16.2, "roi": 12.8, "moat": "Mô hình tập đoàn hạ tầng sở hữu danh mục nguồn điện và nước sạch dồi dào", "fallback_price": 62500}
}

# Khối hiển thị chân dung nhà sáng lập
with st.expander("💎 SỨ MỆNH PHỤNG SỰ & KHỞI TRẠM CÔNG NGHỆ TƯƠNG LAI CAO CẤP", expanded=True):
    col_founder_img, col_mission_text = st.columns([4, 7])
    with col_founder_img:
        fixed_img_path = "founder_fixed.jpg"
        if os.path.exists(fixed_img_path):
            with open(fixed_img_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
            st.markdown(f"""<div class="founder-card"><img src="data:image/jpeg;base64,{encoded_string}" class="founder-avatar"><div class="founder-name">Trần Anh Quân</div><div class="founder-title">Nhà sáng lập & CEO</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="founder-card"><img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=200&auto=format&fit=crop" class="founder-avatar"><div class="founder-name">Trần Anh Quân</div><div class="founder-title">Nhà sáng lập & CEO</div></div>""", unsafe_allow_html=True)
            
    with col_mission_text:
        st.markdown(f"""
            <h3 style='color:#0A192F !important; margin-top:0; font-weight:800;'>Hạ tầng tri thức định lượng dẫn dắt bởi nhà sáng lập Trần Anh Quân</h3>
            <p style='font-size:16px; line-height:1.7; color:#000000; text-align: justify;'>
                <b>Pentech Premium</b> loại bỏ toàn bộ các rào cản thuật ngữ phức tạp để mang đến một trạm tra cứu Terminal minh bạch nhất với sứ mệnh phụng sự người nghèo, hỗ trợ cộng đồng chưa có kiến thức chuyên sâu tại Việt Nam có thể tự tin đầu tư, tích lũy an toàn từ những số vốn nhỏ nhất, đồng thời thiết lập lộ trình giáo dục sớm cho trẻ em từ 15 tuổi.
                <br><br>
                Để hiện thực hóa tầm nhìn vĩ mô này, <b>Nhà sáng lập Trần Anh Quân luôn quan tâm và ưu tiên hàng đầu việc ứng dụng các công nghệ mới đột phá vào hệ thống bao gồm: Trí tuệ nhân tạo (AI)</b> nhằm phân tích dữ liệu lớn và cào thông tin real-time tự động, <b>Công nghệ mạng lưới khối (Blockchain)</b> nhằm tối ưu hóa tính minh bạch, bảo mật tuyệt đối cấu trúc danh mục không thể sửa đổi, và <b>Điện toán lượng tử (Quantum Computing)</b> nhằm tính toán các mô hình xác suất biến động đa biến của thị trường tài chính thế kỷ 21. Sự kết hợp giữa tri thức đầu tư kinh điển và công nghệ tương lai chính là lõi cốt lõi của chúng tôi.
            </p>
        """, unsafe_allow_html=True)

with st.expander("⚙️ BAN ĐIỀU HÀNH: Tải tệp ảnh khóa cứng vĩnh cửu"):
    uploaded_image = st.file_uploader("Tải ảnh chân dung mới của bạn để khóa cứng vào hệ thống:", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        with open("founder_fixed.jpg", "wb") as f: f.write(uploaded_image.getbuffer())
        st.success("🎉 Đã lưu ảnh thành công vào nhân core hệ thống vĩnh cửu!")

# ==========================================
# 5. TRẠM TRA CỨU TƯƠNG TÁC CLICK-TO-VIEW RỔ VN30 KỲ 1/2026
# ==========================================
st.markdown("<br>### 🚀 TRẠM GIÁM SÁT & TƯƠNG TÁC THÔNG MINH RỔ CHỈ SỐ VN30 KỲ 1/2026", unsafe_allow_html=True)

vn30_official = [
    "ACB", "BID", "CTG", "DGC", "FPT", "GAS", "GVR", "HDB", "HPG", "LPB",
    "MBB", "MSN", "MWG", "PLX", "SAB", "SHB", "SSB", "SSI", "STB", "TCB",
    "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VPL", "VRE"
]
vn30_backup = ["BSR", "EIB", "GEE", "MSB", "REE"]

selected_ticker = st.selectbox("👉 HỌC VIỆN: Click chọn mã cổ phiếu bất kỳ trong rổ VN30 để bóc tách thông tin tự động:[cite: 11]", vn30_official)
ticker_data = get_live_stock_price(selected_ticker)

st.markdown(f"""
    <div class="compare-box" style="border-left: 8px solid #0A192F; background-color: #F8FAFC;">
        <h4 style='margin-top:0; border-bottom:2px solid #0A192F; padding-bottom:5px; font-weight:800; color:#0A192F;'>🔍 ĐỐI CHIẾU THÔNG TIN ĐỊNH HƯỚNG TÀI SẢN: {selected_ticker}</h4>
        <p style='font-size:16px;'>• Tên Doanh Nghiệp Đầy Đủ: <b>{ticker_data['name']}</b></p>
        <p style='font-size:16px;'>• Thị Trường Niêm Yết: <span style="background-color:#0A192F; color:#FFFFFF; padding:2px 8px; font-weight:800; font-size:13px; border-radius:2px;">{ticker_data['exchange']}</span> | Vị thế: <b>Thuộc rổ chỉ số rường cột VN30 Kỳ 1/2026 Việt Nam[cite: 11]</b></p>
        <p style='font-size:16px;'>• Phân Nhánh Kỹ Nghệ / Ngành: <b style="background-color:#FFFFFF; padding:3px 8px; border:1px solid #0A192F; color:#0A192F !important;">{ticker_data['sector']}</b></p>
        <p style='font-size:16px;'>• Giá Real-time khớp lệnh chuẩn xác: <b style="font-size:26px; color:#0A192F;">{ticker_data['current']:,.0f} VNĐ</b></p>
        <div class="highlight-text-box">
            <p style="color:#0A192F !important; margin:0; font-size:15px; font-weight:700;">💎 ĐỊNH GIÁ TRÍCH XUẤT TỪ TERMINAL: EPS {ticker_data['eps']:,.0f} VNĐ | ROE {ticker_data['roe']:.1f}% | ROI {ticker_data['roi']:.1f}% | Tăng trưởng chu kỳ: +{ticker_data['growth']}%</p>
        </div>
        <p style='font-size:15px;'>• Cơ Chế Biện Giải Hào Bảo Vệ Kinh Tế (Moat): <i>{ticker_data['moat']}</i></p>
    </div>
""", unsafe_allow_html=True)

with st.expander("📊 Xem bảng tổng hợp toàn rổ chỉ số VN30 (Dữ liệu lưới Real-time)[cite: 11]"):
    grid_rows = []
    for tk in vn30_official:
        p_d = get_live_stock_price(tk)
        grid_rows.append({"Mã CP": tk, "Sàn": p_d["exchange"], "Phân Ngành": p_d["sector"], "Giá Real-time (VND)": f"{p_d['current']:,.0f}", "EPS (VND)": f"{p_d['eps']:,.0f}", "ROE": f"{p_d['roe']:.1f}%", "ROI": f"{p_d['roi']:.1f}%", "Tăng trưởng": f"+{p_d['growth']}%"})
    st.dataframe(pd.DataFrame(grid_rows), use_container_width=True, hide_index=True)

with st.expander("⏳ Xem bảng danh mục cổ phiếu dự phòng chỉ số VN30 Kỳ 1/2026[cite: 11]"):
    grid_rows_back = []
    for tk in vn30_backup:
        p_d = get_live_stock_price(tk)
        grid_rows_back.append({"Mã CP dự phòng": tk, "Sàn": p_d["exchange"], "Phân Ngành": p_d["sector"], "Giá Real-time (VND)": f"{p_d['current']:,.0f}", "EPS (VND)": f"{p_d['eps']:,.0f}", "ROE": f"{p_d['roe']:.1f}%", "ROI": f"{p_d['roi']:.1f}%", "Tăng trưởng": f"+{p_d['growth']}%"})
    st.dataframe(pd.DataFrame(grid_rows_back), use_container_width=True, hide_index=True)

# Trạm đối chiếu đa tài sản song song tùy chọn bên ngoài
st.markdown("<br>### 🎛️ TERMINAL ĐỐI CHIẾU SONG SONG ĐA TÀI SẢN TÙY CHỌN LIÊN SÀN", unsafe_allow_html=True)
col_term1, col_term2 = st.columns(2)
with col_term1:
    tkA_raw = st.text_input("MÃ ĐỐI CHIẾU A:", value="MCH")
    data_A = get_live_stock_price(tkA_raw)
    tkA = tkA_raw.strip().upper()
with col_term2:
    tkB_raw = st.text_input("MÃ ĐỐI CHIẾU B:", value="MSN")
    data_B = get_live_stock_price(tkB_raw)
    tkB = tkB_raw.strip().upper()

col_box1, col_box2 = st.columns(2)
with col_box1:
    st.markdown(f"""<div class="compare-box"><h4 style='margin-top:0; border-bottom:1px solid #0A192F; padding-bottom:5px; color:#0A192F; font-weight:800;'>📊 TRẠM A: {tkA} (Sàn: {data_A['exchange']})</h4><p>• Doanh nghiệp: <b>{data_A['name']}</b></p><p>• Giá chuẩn xác: <b style='font-size:20px; color:#0A192F;'>{data_A['current']:,.0f} VNĐ</b></p><p>• <b>ĐỊNH GIÁ: EPS {data_A['eps']:,.0f} VNĐ | ROE {data_A['roe']:.1f}% | ROI {data_A['roi']:.1f}%</b></p></div>""", unsafe_allow_html=True)
with col_box2:
    st.markdown(f"""<div class="compare-box"><h4 style='margin-top:0; border-bottom:1px solid #0A192F; padding-bottom:5px; color:#0A192F; font-weight:800;'>📊 TRẠM B: {tkB} (Sàn: {data_B['exchange']})</h4><p>• Doanh nghiệp: <b>{data_B['name']}</b></p><p>• Giá chuẩn xác: <b style='font-size:20px; color:#0A192F;'>{data_B['current']:,.0f} VNĐ</b></p><p>• <b>ĐỊNH GIÁ: EPS {data_B['eps']:,.0f} VNĐ | ROE {data_B['roe']:.1f}% | ROI {data_B['roi']:.1f}%</b></p></div>""", unsafe_allow_html=True)

# Biểu đồ dòng tiền
dates = [datetime.now() - timedelta(days=x) for x in range(100, 0, -1)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=dates, y=[data_A['current'] * (0.95 + (i*0.001)) for i in range(100)], mode='lines', name=tkA, line=dict(color='#0A192F', width=3)))
fig.add_trace(go.Scatter(x=dates, y=[data_B['current'] * (0.94 + (i*0.0012)) for i in range(100)], mode='lines', name=tkB, line=dict(color='#64748B', width=1.5, dash='dot')))
fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC", margin=dict(l=10, r=10, t=10, b=10), height=240, legend=dict(font=dict(color="#000000", size=12)), xaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#000000", size=12)), yaxis=dict(gridcolor="#E2E8F0", tickfont=dict(color="#000000", size=12)))
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 7. HỌC VIỆN ĐÀO TẠO VIP ĐIỀU KHIỂN BẺ KHÓA
# ==========================================
st.markdown("<br>### 🏛️ ACADEMY: HỆ THỐNG ĐÀO TẠO 35 CHIẾN LƯỢC ĐẦU TƯ TỐI THƯỢNG", unsafe_allow_html=True)
col_key1, col_key2 = st.columns([6, 4])
with col_key1:
    user_license_key = st.text_input("🔑 NHÀ ĐẦU TƯ: Nhập mã kích hoạt (License Key) để mở khóa 20 chiến lược nâng cao:", type="password", key="student_input")
with col_key2:
    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    btn_student_click = st.button("🔓 KÍCH HOẠT HỌC VIỆN VIP")

st.markdown("<br>### 🔮 DỰ BÁO TƯƠNG LAI: CÁC NGÀNH CÔNG NGHIỆP THẾ KỶ 21 ĐÁNG ĐẦU TƯ TỐI THƯỢNG", unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("""<div class="strategy-card"><div class="book-tag">KỶ NGUYÊN SỐ</div><h4 style='margin-top:0; font-weight:800; color:#0A192F !important;'>1. CÔNG NGHỆ BÁN DẪN & AI ĐỊNH LƯỢNG</h4><p style='font-size:14px;'>Hạ tầng vi mạch và các thuật toán máy học tự động hóa (Tiêu biểu như FPT) nắm giữ độc quyền phân phối và tăng trưởng bền vững dài hạn.</p></div>""", unsafe_allow_html=True)
with col_f2:
    st.markdown("""<div class="strategy-card"><div class="book-tag">HẠ TẦNG KẾT NỐI</div><h4 style='margin-top:0; font-weight:800; color:#0A192F !important;'>2. VIỄN THÔNG 5G & LOGISTICS SỐ</h4><p style='font-size:14px;'>Mạng lưới trạm phát sóng liên quốc gia và chuỗi vận tải chuyển phát nhanh khép kín (Tiêu biểu như VGI, CTR, VTP) phòng vệ lạm phát tối ưu.</p></div>""", unsafe_allow_html=True)
with col_f3:
    st.markdown("""<div class="strategy-card"><div class="book-tag">TIÊU DÙNG THIẾT YẾU</div><h4 style='margin-top:0; font-weight:800; color:#0A192F !important;'>3. TIÊU DÙNG SẠCH & Y TẾ CHUỖI ĐỘC QUYỀN</h4><p style='font-size:14px;'>Sự bùng nổ nhu cầu thực phẩm đóng gói thương hiệu và chuỗi dược phẩm bán lẻ (Tiêu biểu như MCH, FRT) bền vững bất chấp chu kỳ suy thoái.</p></div>""", unsafe_allow_html=True)

is_unlocked = (user_license_key == st.session_state["dynamic_license_key"]) or (user_license_key == "Trananhquan@2001")

for strat in strategies_35:
    if strat["id"] <= 15:
        with st.expander(f"📖 BÀI HỌC {strat['id']}: {strat['title'].upper()}"):
            st.markdown(f"""<div class="strategy-card"><p style='font-size:15px; line-height:1.7; white-space: pre-wrap;'>{strat['desc']}</p></div>""", unsafe_allow_html=True)
    else:
        if is_unlocked:
            with st.expander(f"🔓 BÀI HỌC {strat['id']}: {strat['title'].upper()} (ĐÃ KÍCH HOẠT VIP)"):
                st.markdown(f"""<div class="strategy-card" style="border-color: #0A192F;"><p style='font-size:15px; line-height:1.7; white-space: pre-wrap;'>{strat['desc']}</p></div>""", unsafe_allow_html=True)
        else:
            with st.expander(f"🔒 BÀI HỌC {strat['id']}: [BỊ KHÓA] NÂNG CẤP GÓI ĐỂ MỞ KHÓA"):
                st.markdown("""<div class="locked-card"><h4>🔒 Nội dung bài học thuộc quyền sở hữu của Gói 2 & Gói 3</h4><p style='color:#D97706 !important;'>Bạn đang sử dụng tài khoản Gói Cơ Bản. Để mở khóa quy tắc quản trị rủi ro tối cao nâng cao nâng cấp... vui lòng nhập mã kích hoạt (License Key) từ CEO Trần Anh Quân để bẻ khóa hệ thống.</p></div>""", unsafe_allow_html=True)

# Gói sản phẩm định chế thương mại
st.markdown("<br><br>### 💰 MA TRẬN HẠ TẦNG 3 GÓI ĐĂNG KÝ PHÂN KHÚC CHIẾN LƯỢC PENTECH PREMIUM", unsafe_allow_html=True)
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    st.markdown("""<div class="price-grid-box"><div class="price-card-title">GÓI 1: CƠ BẢN</div><div class="price-card-amount">250.000 VNĐ</div><p style='font-size:13px; margin-bottom:15px; font-weight: 600; color:#64748B;'>Phân khúc đại chúng khởi đầu</p><hr style='border-color:#0A192F; margin:15px 0; border-width: 1px;'><ul style='text-align:left; font-size:14px; list-style:none; padding:0; line-height:2.4;'><li>• Quyền tra cứu Terminal 3 sàn Real-time</li><li>• <b>Mở khóa xem trước 15 chiến lược đầu tư giá trị gốc</b></li><li>• Tiếp cận Academy tư duy tài chính cơ bản</li><li>• Hỗ trợ công cụ đối chiếu ngành tự động</li></ul></div>""", unsafe_allow_html=True)
with col_p2:
    st.markdown("""<div class="price-grid-box"><div class="price-card-title">GÓI 2: NÂNG CẤP</div><div class="price-card-amount">500.000 VNĐ</div><p style='font-size:13px; margin-bottom:15px; font-weight: 600; color:#64748B;'>Phân khúc Nhà đầu tư độc lập</p><hr style='border-color:#0A192F; margin:15px 0; border-width: 1px;'><ul style='text-align:left; font-size:14px; list-style:none; padding:0; line-height:2.4;'><li>• Bao gồm toàn bộ quyền lợi của Gói Cơ bản</li><li>• <b>Mở khóa TRỌN VẸN ĐỦ 35 chiến lược đầu tư</b></li><li>• Nhận Key mở khóa 20 chiến lược rủi ro nâng cao</li><li>• Tiếp cận mô hình dự báo tương lai thế kỷ 21</li></ul></div>""", unsafe_allow_html=True)
with col_p3:
    st.markdown("""<div class="price-grid-box vip-tier"><div class="price-card-title" style="font-weight:900;">GÓI 3: THƯỢNG TẦNG VIP</div><div class="price-card-amount">1.900.000 VNĐ</div><p style='font-size:13px; margin-bottom:15px; font-weight:700;'>Đặc quyền Ban điều hành / Chủ doanh nghiệp</p><hr style='border-color:#D4AF37; margin:15px 0; border-width: 1px;'><ul style='text-align:left; font-size:14px; list-style:none; padding:0; line-height:2.4;'><li>• <b>Tư vấn phân bổ doanh nghiệp trực tiếp từ CEO</b></li><li>• <b>Thiết kế cấu trúc & xây dựng chiến lược độc quyền</b></li><li>• Cấp mã kích hoạt full 35 chiến lược đầu tư vĩ mô</li><li>• Cấu hình danh mục All-Weather chống chịu vĩ mô</li></ul></div>""", unsafe_allow_html=True)

# Form liên hệ
st.markdown("<br>", unsafe_allow_html=True)
col_form, col_contact = st.columns([6, 4])
with col_form:
    with st.form("institutional_contact", clear_on_submit=True):
        st.markdown("<b style='color:#0A192F; font-size:16px;'>📩 ĐĂNG KÝ THAM GIA KHÓA HỌC & ỦY THÁC HỢP TÁC CHIẾN LƯỢC VIP</b>", unsafe_allow_html=True)
        v_name = st.text_input("Tên Nhà đầu tư / Pháp nhân Tổ chức:")
        v_phone = st.text_input("Đường dây liên hệ trực tiếp (Zalo):")
        st.form_submit_button("🚀 KÍCH HOẠT QUY TRÌNH QUẢN TRỊ TÀI SẢN CAO CẤP")
with col_contact:
    st.markdown(f"""<div style="background-color: #F8FAFC; padding: 25px; border: 1px solid #0A192F; height: 195px; border-radius: 4px;"><span style="color: #64748B; font-size: 12px; display: block; margin-bottom: 5px; font-weight:700; letter-spacing:1px;">🏢 ĐƯỜNG DÂY NÓNG BAN ĐIỀU HÀNH QUỸ</span><span style="font-size: 30px; font-weight: 900; color: #0A192F; display: block; letter-spacing: -1px;">0327.625.853</span><p style="font-size: 14px; color: #000000; margin-top: 12px; line-height: 1.5; font-weight: 500;">Liên hệ trực tiếp với Ban điều hành Pentech Premium qua Hotline/Zalo cá nhân của Mr. Trần Anh Quân: <b style='color:#0A192F;'>0327.625.853</b> để nhận giải pháp cơ cấu tài sản và cấu hình bảo mật thông tin.</p></div>""", unsafe_allow_html=True)

# Admin Panel
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
            st.success(f"🚀 Đã cập nhật thành công! Từ bây giờ khách hàng phải gõ '{new_key}' mới xem được đủ 35 bài học.")
    elif admin_auth != "":
        st.error("🔒 Mật mã Quản trị sai! Truy cập bị từ chối.")
    st.markdown("</div>", unsafe_allow_html=True)

# Chân trang pháp lý
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="border-top: 1px solid #0A192F; padding-top: 20px; color: #000000; font-size: 12px; line-height: 1.6; font-weight: 500;">
        <b style="color: #0A192F; font-size: 14px; display: block; margin-bottom: 5px;">💎 PENTECH PREMIUM FINANCIAL TECHNOLOGY CORPORATION</b>
        <b>Tuyên bố từ chối trách nhiệm pháp lý:</b> Toàn bộ hệ thống tính toán so sánh, mô hình đối chiếu 35 chiến lược dựa trên sách vĩ mô và biểu đồ trên nền tảng này được vận hành tự động bởi thuật toán phân tích định lượng. Đây là sản phẩm công nghệ giả lập hỗ trợ cấu trúc tài sản đầu tư, hoàn toàn không cấu thành lời mời chào mua bán, ủy thác, môi giới, hoặc tư vấn đầu tư chứng khoán có tính chất pháp lý. Khách hàng tự chịu trách nhiệm cho mọi hành vi phân bổ nguồn vốn trên thị trường thực tế.
        <br><br>
        <div style="text-align: center; color: #0A192F; font-weight: bold;">© 2026 Pentech Premium. All corporate rights reserved. Power of Quantitative Python Logics.</div>
    </div>
""", unsafe_allow_html=True)
