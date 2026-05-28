# ... (Giữ nguyên các đoạn khai báo thư viện và cấu hình CSS như cũ)

# BỘ DỮ LIỆU 35 CHIẾN LƯỢC NÂNG CẤP 6 DÒNG CHUYÊN SÂU
strategies_35 = [
    {
        "id": 1, "book": "Security Analysis - B. Graham", "title": "Xác lập trục giá trị nội tại", 
        "desc": "1. Định nghĩa giá trị doanh nghiệp dựa trên tài sản ròng hữu hình.\n2. Tính toán biên an toàn (Margin of Safety) ít nhất 30% so với thị giá.\n3. Chỉ mua khi P/E và P/B thấp hơn mức trung bình 5 năm.\n4. Tránh xa các doanh nghiệp có nợ vay/vốn chủ sở hữu > 1.\n5. Áp dụng cho các mã như VCB, VNM trong các nhịp điều chỉnh sâu.\n6. Bài học: Mua rẻ để không bao giờ phải lo lắng về giá."
    },
    {
        "id": 2, "book": "Nhà Đầu Tư Thông Minh - B. Graham", "title": "Chiến lược chế ngự Ngài Thị Trường", 
        "desc": "1. Coi bảng điện là công cụ phục vụ, không phải người dẫn đường.\n2. Mua khi thị trường hoảng loạn (Panic Selling) vì lý do vĩ mô.\n3. Bán khi thị trường hưng phấn tột độ (Euphoria).\n4. Phân bổ danh mục 50% cổ phiếu, 50% tiền mặt/trái phiếu.\n5. Kiên định không theo đuổi các cổ phiếu đầu cơ nóng.\n6. Bài học: Tâm lý vững vàng chiến thắng 90% nhà đầu tư."
    },
    # ... (Bạn tiếp tục mở rộng tương tự cho đến bài 35)
]

# Phần logic hiển thị trong vòng lặp:
for strat in strategies_35:
    if strat["id"] <= 15:
        with st.expander(f"📖 CHIẾN LƯỢC {strat['id']}: {strat['title'].upper()}"):
            st.markdown(f"""<div class="strategy-card"><div class="book-tag">{strat['book']}</div>
            <pre style='white-space: pre-wrap; font-family: inherit; font-size: 14px;'>{strat['desc']}</pre></div>""", unsafe_allow_html=True)
    else:
        if is_unlocked:
            with st.expander(f"🔓 CHIẾN LƯỢC {strat['id']}: {strat['title'].upper()} (ĐÃ KÍCH HOẠT)"):
                st.markdown(f"""<div class="strategy-card"><div class="book-tag">{strat['book']}</div>
                <pre style='white-space: pre-wrap; font-family: inherit; font-size: 14px;'>{strat['desc']}</pre></div>""", unsafe_allow_html=True)
        else:
            with st.expander(f"🔒 CHIẾN LƯỢC {strat['id']}: [BỊ KHÓA] NÂNG CẤP GÓI"):
                st.markdown(f"""<div class="locked-card"><h4>🔒 Nội dung chuyên sâu 6 dòng của bài học này đã được khóa.</h4>
                <p>Vui lòng nâng cấp gói để đọc trọn vẹn giáo trình.</p></div>""", unsafe_allow_html=True)
