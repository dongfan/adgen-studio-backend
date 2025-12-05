from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from app.template_engine import compose_banner
import os
from fastapi.staticfiles import StaticFiles

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def root():
    return {"message": "AdGen Studio Backend API running with GPT-5-mini!"}


class CopyRequest(BaseModel):
    product_name: str
    description: str
    tone: str = "casual"


@app.post("/generate-copy")
def generate_copy(req: CopyRequest):

    prompt = f"""
너는 한국 최고의 마케팅 카피라이터야.

아래 제품 정보를 참고해서
서로 스타일이 다른 광고 문구 3개를 생성해줘.

제품명: {req.product_name}
설명: {req.description}
톤: {req.tone}

출력 형식:
1) ...
2) ...
3) ...
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {"copies": response.choices[0].message.content}

@app.post("/compose-banner")
async def compose_banner_api(
    text: str,
    file: UploadFile = File(...)
):
    import uuid

    # 경로 설정
    filename = f"banner_{uuid.uuid4()}.png"
    input_path = f"temp_{uuid.uuid4()}.png"
    output_path = f"static/{filename}"

    # 원본 파일 저장
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # 이미지 합성
    from app.template_engine import compose_banner
    compose_banner(input_path, text, output_path)

    # 원본 삭제
    os.remove(input_path)

    # 최종 URL 반환
    return {
        "image_url": f"http://localhost:8000/static/{filename}"
    }