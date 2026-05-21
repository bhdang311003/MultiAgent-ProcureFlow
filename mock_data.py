DEPARTMENT_BUDGETS = {
    "AI Engineering": {"total": 2_000_000_000, "spent": 800_000_000},
    "Product":        {"total": 1_500_000_000, "spent": 200_000_000},
    "Marketing":      {"total":   500_000_000, "spent": 450_000_000},
    "HR":             {"total":   300_000_000, "spent":  50_000_000},
    "Finance":        {"total":   400_000_000, "spent": 100_000_000},
}

APPROVERS = {
    "manager": {"name": "Nguyen Van A", "email": "manager@company.com"},
    "finance":  {"name": "Tran Thi B",  "email": "finance@company.com"},
    "cto":      {"name": "Le Van C",    "email": "cto@company.com"},
}

VENDOR_CATALOG = {
    "MacBook Pro M4": [
        {"vendor": "FPT Shop",      "unit_price": 52_000_000, "delivery_days": 3,  "warranty_years": 1},
        {"vendor": "CellphoneS",    "unit_price": 51_500_000, "delivery_days": 2,  "warranty_years": 1},
        {"vendor": "Apple Vietnam", "unit_price": 54_000_000, "delivery_days": 7,  "warranty_years": 2},
    ],
    "Dell XPS 15": [
        {"vendor": "FPT Shop",      "unit_price": 38_000_000, "delivery_days": 5,  "warranty_years": 1},
        {"vendor": "Nguyen Kim",    "unit_price": 37_500_000, "delivery_days": 4,  "warranty_years": 1},
    ],
    "iPhone 16 Pro": [
        {"vendor": "FPT Shop",      "unit_price": 33_000_000, "delivery_days": 2,  "warranty_years": 1},
        {"vendor": "CellphoneS",    "unit_price": 32_500_000, "delivery_days": 1,  "warranty_years": 1},
        {"vendor": "Apple Vietnam", "unit_price": 34_000_000, "delivery_days": 5,  "warranty_years": 2},
    ],
}

# < 50M → manager only
# 50M–200M → manager + finance
# >= 200M → manager + finance + cto
THRESHOLDS = {
    "manager_only":     50_000_000,
    "finance_required": 200_000_000,
}
