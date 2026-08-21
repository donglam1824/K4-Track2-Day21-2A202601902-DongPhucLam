# Báo Cáo Lab Day 21 - CI/CD cho AI Systems


| | |
|---|---|
| Họ và tên | Đồng Phúc Lâm |
| MSSV | 2A202601902 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/donglam1824/K4-Track2-Day21-2A202601902-DongPhucLam |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do


| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Lần chạy thứ 3 có `f1_score` cao nhất (0.7149), tốt hơn so với lần 1 và 2. Đáng chú ý, lần chạy có accuracy cao nhất (lần 1: 0.8780) lại không trùng với lần có f1_score cao nhất. Điều này cho thấy mô hình ở lần 1 có thể dự đoán đúng nhiều mẫu của lớp đa số hơn để kéo accuracy lên, nhưng lại bỏ sót hoặc sai nhiều ở lớp thiểu số (làm F1 giảm). Qua các lần chạy, có thể thấy sự đánh đổi: nếu giảm `learning_rate` (lần 2), ta phải tăng số cây `n_estimators` hoặc độ sâu, nếu không mô hình sẽ bị underfitting và cho kết quả rất thấp.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy


Tập dữ liệu Adult có phân bố lớp mất cân bằng mạnh, với tỷ lệ lớp thu nhập > 50K (lớp dương) chỉ chiếm khoảng 24.8%. Vì sự mất cân bằng này, nếu một mô hình "lười biếng" luôn dự đoán tất cả là "thu nhập thấp" thì nó vẫn dễ dàng đạt được accuracy là 0.752. Tuy nhiên, accuracy 0.752 hoàn toàn vô dụng vì mô hình không thể phát hiện được bất kỳ trường hợp thu nhập cao nào.

Ngược lại, F1-score (khi tính riêng cho lớp dương) kết hợp giữa Precision và Recall, phản ánh chính xác khả năng mô hình nhận diện lớp thu nhập > 50K mà không bị đánh lừa bởi lớp đa số. Khi gọi hàm `f1_score`, ta tuyệt đối KHÔNG dùng tham số `average="weighted"` hay `average="macro"` vì các phép trung bình này sẽ cộng gộp cả F1 rất cao của lớp đa số, làm chỉ số bị kéo lên ảo và che lấp đi việc mô hình đang phân loại kém ở lớp thiểu số cần quan tâm.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết


| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Lỗi SSH timeout khi chạy pipeline hoặc gọi API bị từ chối kết nối | Quên mở port 8080 trên tường lửa (firewall) của máy ảo đám mây | Đăng nhập vào Cloud Console và thêm luật tường lửa cho phép ingress TCP trên port 8080 |
| Job Train trong GitHub Actions bị lỗi xác thực Cloud Storage | Chưa thêm hoặc thêm sai cấu hình secret `STORAGE_CREDENTIALS` trong GitHub Repo | Vào Settings > Secrets and variables > Actions để kiểm tra và cập nhật đúng nội dung của file `sa-key.json` |
| Lỗi khi push DVC: `google.api_core.exceptions.NotFound` | Nhập sai tên bucket hoặc chưa thiết lập biến môi trường chỉ định file JSON xác thực | Sửa lại tên bucket trong `.dvc/config` (bằng lệnh dvc remote) và export `GOOGLE_APPLICATION_CREDENTIALS` đúng đường dẫn |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)


| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7091 | 0.8720 |
| Bước 3 (thêm `train_batch2`) | 0.7339 | 0.8840 |

**Nhận xét:** f1_score tăng nhẹ (khoảng 0.02) do dữ liệu lớn hơn cung cấp thêm một số mẫu hình (patterns) tốt hơn cho lớp thiểu số, kéo theo accuracy cũng tăng. Tuy nhiên mức tăng không đột phá vì `train_batch2` vốn được chia ngẫu nhiên từ cùng một nguồn nên vẫn mang phân phối tương tự `train_batch1`. Mấu chốt là pipeline đã chạy tự động thành công và an toàn triển khai model mới.

