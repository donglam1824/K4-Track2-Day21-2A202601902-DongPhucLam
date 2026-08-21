# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

<!--
HƯỚNG DẪN - đọc rồi XÓA TOÀN BỘ các khối chú thích này sau khi điền xong:

  - Giới hạn: KHÔNG QUÁ 1 TRANG A4, tương đương khoảng 450 - 550 từ nội dung.
  - Chỉ điền vào các chỗ ___ và các ô trong bảng. Không thêm mục mới.
  - Viết bằng câu hoàn chỉnh, không gạch đầu dòng cụt lủn.
  - Kiểm tra độ dài sau khi đã xóa hết chú thích:
        wc -w nop-bai/bao-cao.md
    và xem trước bản in bằng cách mở file trên GitHub rồi Ctrl+P / Cmd+P.
-->

| | |
|---|---|
| Họ và tên | Đồng Phúc Lâm |
| MSSV | 2A202601902 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/donglam1824/K4-Track2-Day21-2A202601902-DongPhucLam |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

<!-- Khoảng 120 - 150 từ. Điền kết quả thật từ MLflow UI ở Bước 1, tối thiểu 3 lần chạy. -->

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Lần chạy thứ 3 có `f1_score` cao nhất (0.7149), tốt hơn so với lần 1 và 2. Đáng chú ý, lần chạy có accuracy cao nhất (lần 1: 0.8780) lại không trùng với lần có f1_score cao nhất. Điều này cho thấy mô hình ở lần 1 có thể dự đoán đúng nhiều mẫu của lớp đa số hơn để kéo accuracy lên, nhưng lại bỏ sót hoặc sai nhiều ở lớp thiểu số (làm F1 giảm). Qua các lần chạy, có thể thấy sự đánh đổi: nếu giảm `learning_rate` (lần 2), ta phải tăng số cây `n_estimators` hoặc độ sâu, nếu không mô hình sẽ bị underfitting và cho kết quả rất thấp.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

<!-- Khoảng 120 - 150 từ. -->

Tập dữ liệu Adult có phân bố lớp mất cân bằng mạnh, với tỷ lệ lớp thu nhập > 50K (lớp dương) chỉ chiếm khoảng 24.8%. Vì sự mất cân bằng này, nếu một mô hình "lười biếng" luôn dự đoán tất cả là "thu nhập thấp" thì nó vẫn dễ dàng đạt được accuracy là 0.752. Tuy nhiên, accuracy 0.752 hoàn toàn vô dụng vì mô hình không thể phát hiện được bất kỳ trường hợp thu nhập cao nào.

Ngược lại, F1-score (khi tính riêng cho lớp dương) kết hợp giữa Precision và Recall, phản ánh chính xác khả năng mô hình nhận diện lớp thu nhập > 50K mà không bị đánh lừa bởi lớp đa số. Khi gọi hàm `f1_score`, ta tuyệt đối KHÔNG dùng tham số `average="weighted"` hay `average="macro"` vì các phép trung bình này sẽ cộng gộp cả F1 rất cao của lớp đa số, làm chỉ số bị kéo lên ảo và che lấp đi việc mô hình đang phân loại kém ở lớp thiểu số cần quan tâm.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

<!-- Nêu 2 - 3 khó khăn thật, mỗi ô một câu ngắn. -->

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

<!-- Lấy số liệu từ bảng ở mục 3.6 của tasks/buoc-3.md. -->

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | ___ | ___ |
| Bước 3 (thêm `train_batch2`) | ___ | ___ |

**Nhận xét:** ___

<!--
Một câu trả lời trung thực kiểu "f1 giảm 0,01 vì dữ liệu mới cùng phân phối, không mang
thêm thông tin mới" được đánh giá cao hơn kết luận sai rằng thêm dữ liệu luôn tốt hơn.
-->

---

## 5. Phần Bonus Đã Thực Hiện (nếu có)

<!-- Xóa cả mục 5 nếu không làm bonus. Mỗi bonus tối đa 1 dòng. -->

- [ ] Bonus 1 - Tracking MLflow từ xa với DagsHub: ___
- [ ] Bonus 2 - Điều chỉnh ngưỡng quyết định: ___
- [ ] Bonus 3 - Báo cáo precision / recall tự động: ___
- [ ] Bonus 4 - Hoàn trả về phiên bản trước: ___
- [ ] Bonus 5 - Cảnh báo lệch lạc dữ liệu: ___
