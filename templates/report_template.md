# 📊 CSV AI Analyst Report

## 🔍 Data Summary

### Column Types:
{% for col, dtype in summary.dtypes.items() %}
- **{{ col }}**: {{ dtype }}
{% endfor %}

---

### Missing Values:
{% for col, count in summary.missing_values.items() %}
- **{{ col }}**: {{ count }}
{% endfor %}

---

### Summary Statistics:
{% for col, stats in summary.summary_stats.items() %}
#### {{ col }}
{% for stat, value in stats.items() %}
- {{ stat }}: {{ value }}
{% endfor %}
{% endfor %}

---

## 🤖 Q&A Interactions

{% for item in interactions %}
### ❓ Question:
{{ item.question }}

### 🧠 Code Generated:
```python
{{ item.code }}
