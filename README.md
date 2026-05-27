# Multi-Agent Procurement Approval System

An enterprise workflow automation system that uses multi-agent AI orchestration to process internal purchase requests — automating the entire procurement workflow from parsing to approval routing.

## Overview

Employees submit purchase requests. The system automatically analyzes, validates, and routes them through the appropriate approval chain.

<p align="center">
    <img width="650" height="540" alt="image" src="https://github.com/user-attachments/assets/95c7bfca-b2b6-45e6-96aa-6463bbcce374" />
    <img width="800" height="40" alt="image" src="https://github.com/user-attachments/assets/33e3aca2-c6d2-403d-a697-82a9683bdc40" />
    <img width="600" height="800" alt="image" src="https://github.com/user-attachments/assets/04e2eb7b-0b4b-4732-b541-bbebe19d5ee1" />

</p>




## Architecture

```
User Input
    │
    ▼
request_parser      ← LLM: extract structured data from natural language
    │
    ▼
budget_validator    ← check department remaining budget
    │
    ▼
risk_detector       ← LLM: detect anomalies, duplicates, abnormal pricing
    │
    ▼
vendor_comparator   ← LLM: compare vendors, recommend best option
    │
    ▼
approval_router     ← LLM: dynamic routing based on amount, risk, product type
    │
    ▼
notify_approvers    ← send approval notifications
    │
    ▼
human_approval      ← PAUSE: wait for each approver decision
    │
    ▼
notify_submitter    ← send final result to submitter
```

Built with **LangGraph** — each agent is a node in a StateGraph with conditional edges and human-in-the-loop support.

## Tech Stack

- **LangGraph** — multi-agent orchestration, state management, human-in-the-loop
- **LLM** — LLM API from OpenRouter
- **FastAPI** — REST API layer
- **Streamlit** — UI for employees and approvers
- **Python** — core language

## Features

- Natural language request parsing
- Budget validation against department limits
- Risk detection with procurement history context
- Vendor comparison and recommendation
- Dynamic approval routing (based on amount + risk score + product type)
- Human-in-the-loop approval workflow
- Persistent procurement history for duplicate detection

## Project Structure

```
multiagent_buying/
├── agents/
│   ├── request_parser.py       # LLM: parse natural language
│   ├── budget_validator.py     # check department budget
│   ├── risk_detector.py        # LLM: risk analysis + history
│   ├── vendor_comparator.py    # LLM: vendor recommendation
│   ├── approval_router.py      # LLM: dynamic routing
│   ├── human_approval.py       # interrupt: wait for approvers
│   ├── notify_approvers.py     # notify approvers
│   └── notify_submitter.py     # notify submitter with result
├── pages/
│   └── approver.py             # Streamlit approver portal
├── graph.py                    # LangGraph StateGraph definition
├── state.py                    # ProcurementState TypedDict
├── llm_client.py               # OpenRouter API wrapper
├── mock_data.py                # mock budgets, vendors, approvers
├── memory.py                   # procurement history & active requests
├── api.py                      # FastAPI endpoints
├── streamlit_app.py            # Streamlit employee portal
└── main.py                     # CLI entry point (for testing)
```

## Setup

### Option 1: Docker (recommended)

1. Create `.env` file:
```
API_KEY=your_openrouter_api_key
```

2. Run:
```
docker compose up
```

Access the app at `http://localhost:8501`

### Option 2: Local

1. Create and activate a virtual environment
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create `.env` file:
```
API_KEY=your_openrouter_api_key
```

4. Run the API server:
```
uvicorn api:app --reload
```

5. Run the Streamlit UI (new terminal):
```
streamlit run streamlit_app.py
```

## Docker Images

Pre-built images are available on Docker Hub:

- [`bhdang311003/procureflow-api`](https://hub.docker.com/r/bhdang311003/procureflow-api)
- [`bhdang311003/procureflow-streamlit`](https://hub.docker.com/r/bhdang311003/procureflow-streamlit)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/requests` | Submit a new purchase request |
| `GET` | `/requests` | List all active requests |
| `GET` | `/requests/{id}` | Get request details and status |
| `POST` | `/requests/{id}/decision` | Submit approve/reject decision |

## Workflow

1. Employee submits request via Streamlit UI → receives `thread_id`
2. System runs all agents automatically (parse → validate → risk → vendor → route)
3. Approvers notified — review details in Approver Portal
4. Each approver approves or rejects
5. Submitter receives final result notification

======================================================

# Hệ thống Tự động quy trình Phê duyệt Mua sắm nội bộ

Hệ thống tự động hóa quy trình mua sắm nội bộ doanh nghiệp bằng kiến trúc multi-agent AI — tự động hóa toàn bộ quy trình từ phân tích đến phê duyệt.

## Tổng quan

Nhân viên đưa ra yêu cầu mua sắm. Hệ thống tự động phân tích, kiểm tra và chuyển yêu cầu đến đúng người phê duyệt.

## Kiến trúc

Mỗi agent là một node trong LangGraph StateGraph, xử lý một bước trong workflow:

```
User Input
    │
    ▼
request_parser      ← LLM: trích xuất dữ liệu có cấu trúc từ ngôn ngữ tự nhiên của yêu cầu
    │
    ▼
budget_validator    ← kiểm tra ngân sách còn lại của bộ phận
    │
    ▼
risk_detector       ← LLM: phát hiện các nguy cơ, dữ liệu trùng lặp, giá cả bất thường
    │
    ▼
vendor_comparator   ← LLM: so sánh các nhà cung cấp, đề xuất lựa chọn tốt nhất
    │
    ▼
approval_router     ← LLM: định tuyến phê duyệt dựa trên số tiền, rủi ro và loại sản phẩm.
    │
    ▼
notify_approvers    ← gửi yêu cầu phê duyệt
    │
    ▼
human_approval      ← PAUSE: chờ quyết định của từng người phê duyệt.
    │
    ▼
notify_submitter    ← gửi kết quả phê duyệt cho người yêu cầu.
```

## Project Structure

```
MultiAgent_ProcureFlow/
├── agents/
│   ├── request_parser.py       # LLM: phân tích ngôn ngữ tự nhiên
│   ├── budget_validator.py     # kiểm tra ngân sách phòng ban
│   ├── risk_detector.py        # LLM: phân tích rủi ro + lịch sử
│   ├── vendor_comparator.py    # LLM: đề xuất nhà cung cấp
│   ├── approval_router.py      # LLM: định tuyến phê duyệt
│   ├── human_approval.py       # dừng workflow, chờ aphê duyệt
│   ├── notify_approvers.py     # thông báo cho người phê duyệt
│   └── notify_submitter.py     # thông báo kết quả cho người yêu cầu
├── pages/
│   └── approver.py             # giao diện Streamlit cho người phê duyệt
├── graph.py                    # định nghĩa LangGraph StateGraph
├── state.py                    # ProcurementState TypedDict
├── llm_client.py               # wrapper gọi OpenRouter API
├── mock_data.py                # dữ liệu giả lập ngân sách, vendor, approver
├── memory.py                   # lịch sử mua sắm & request đang active
├── api.py                      # FastAPI endpoints
├── streamlit_app.py            # giao diện Streamlit cho nhân viên
└── main.py                     # CLI để test
```

## Tính năng

- Parse yêu cầu ngôn ngữ tự nhiên
- Kiểm tra ngân sách phòng ban
- Phát hiện rủi ro dựa trên lịch sử mua sắm
- So sánh và đề xuất nhà cung cấp
- Định tuyến phê duyệt tự động (theo số tiền + risk + loại sản phẩm)
- Human-in-the-loop: chờ từng người phê duyệt duyệt theo thứ tự
- Lưu lịch sử mua sắm để phát hiện request trùng lặp

## Cài đặt
### Cách 1: Docker

1. Tạo file `.env`:
```
API_KEY=your_openrouter_api_key
```

2. Run:
```
docker compose up
```

Truy cập và sử dụng tại `http://localhost:8501`

### Cách 2: Local

1. Tạo virtual environment và cài dependencies:
```
pip install -r requirements.txt
```

2. Tạo file `.env`:
```
API_KEY=your_openrouter_api_key
```

3. Chạy API server:
```
uvicorn api:app --reload
```

4. Chạy Streamlit UI (terminal khác):
```
streamlit run streamlit_app.py
```

## Luồng hoạt động

1. Nhân viên gửi yêu cầu mua sắm → nhận `thread_id` của yêu cầu đó
2. Hệ thống tự chạy các agent (parse → validate → risk → vendor → route)
3. Người phê duyệt nhận thông báo → xem chi tiết tại Approver Portal
4. Từng người phê duyệt sẽ approve hoặc reject theo thứ tự
5. Nhân viên nhận thông báo kết quả cuối
