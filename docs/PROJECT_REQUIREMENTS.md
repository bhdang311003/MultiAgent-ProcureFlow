# Multi-Agent Procurement Approval System

## Mô tả yêu cầu dự án

Công ty hiện đang xử lý các yêu cầu mua sắm nội bộ thông qua email và các bước approve thủ công, dẫn đến nhiều vấn đề như:

* approval chậm,
* khó kiểm tra ngân sách,
* khó theo dõi trạng thái request,
* dễ xảy ra request trùng lặp,
* khó phát hiện request bất thường,
* vendor pricing không được tối ưu.

Công ty cần xây dựng một hệ thống AI tự động hóa workflow procurement nội bộ bằng mô hình multi-agent orchestration.

Hệ thống cần cho phép nhân viên submit purchase requests bằng ngôn ngữ tự nhiên, ví dụ:

```text
Cần mua 20 MacBook Pro M4 cho team AI Engineering,
ngân sách khoảng 1 tỷ VNĐ,
cần trong vòng 2 tuần.
```

Sau khi nhận request, hệ thống AI cần tự động:

* phân tích nội dung request,
* trích xuất thông tin procurement,
* kiểm tra ngân sách phòng ban,
* phát hiện request bất thường hoặc trùng lặp,
* so sánh vendor,
* quyết định luồng approval phù hợp,
* gửi notification cho các bên liên quan,
* lưu workflow state và approval history.

Hệ thống cần được thiết kế theo hướng enterprise workflow automation platform thay vì chatbot đơn giản.

---

## Các chức năng chính

### 1. Request Understanding

* Phân tích request dạng ngôn ngữ tự nhiên.
* Trích xuất:

  * sản phẩm,
  * số lượng,
  * phòng ban,
  * ngân sách,
  * mức độ ưu tiên.

---

### 2. Budget Validation

* Kiểm tra ngân sách còn lại của phòng ban.
* Đánh dấu request vượt ngân sách.
* Trigger finance review nếu cần.

---

### 3. Risk Detection

* Phát hiện request trùng lặp.
* Phát hiện giá bất thường.
* Phát hiện số lượng bất thường.
* Đánh giá risk score của request.

---

### 4. Vendor Comparison

* So sánh vendor pricing.
* Đề xuất vendor phù hợp.
* Phân tích chi phí procurement.

---

### 5. Approval Routing

* Tự động quyết định approval workflow.
* Route request tới đúng approver dựa trên business rules.

Ví dụ:

* request nhỏ → manager approve,
* request lớn → finance + CTO approve.

---

### 6. Notification System

* Gửi approval requests.
* Gửi workflow updates.
* Thông báo trạng thái procurement.

---

### 7. Workflow Tracking

* Lưu workflow states.
* Lưu approval history.
* Tracking trạng thái request theo thời gian thực.

---

## Mục tiêu kỹ thuật

Hệ thống cần thể hiện:

* AI orchestration,
* multi-agent workflows,
* workflow automation,
* conditional routing,
* state management,
* production-oriented backend architecture,
* enterprise AI operations.

Dự án hướng tới mô hình AI operational workflow system dành cho doanh nghiệp.
