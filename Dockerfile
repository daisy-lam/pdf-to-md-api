# 使用官方 Python 輕量版影像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製工具清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY main.py .

# 暴露 Cloud Run 預設的 8080 埠
EXPOSE 8080

# 啟動 API 伺服器
CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8080"]
