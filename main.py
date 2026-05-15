import pdfplumber
import requests
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PDFRequest(BaseModel):
    url: str

@app.post("/convert")
async def convert_pdf_to_md(request: PDFRequest):
    temp_pdf = "/tmp/target.pdf"
    
    try:
        # 1. 下載 PDF 檔案
        response = requests.get(request.url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="無法下載 PDF 檔案")
        
        with open(temp_pdf, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # 2. 開始解析 PDF
        markdown_content = []
        with pdfplumber.open(temp_pdf) as pdf:
            # 這裡採用逐頁處理，避免 400 頁一次塞爆記憶體
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    markdown_content.append(f"## Page {i+1}\n\n{text}\n")
        
        # 3. 清理暫存檔並回傳結果
        os.remove(temp_pdf)
        return {"markdown": "\n".join(markdown_content)}

    except Exception as e:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def health_check():
    return {"status": "工廠運作中"}
