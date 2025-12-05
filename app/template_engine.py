from PIL import Image, ImageDraw, ImageFont
import textwrap

def compose_banner(
    image_path: str,
    text: str,
    output_path: str,
    target_size=(1080, 1080)
):
    """
    고급형 banner generator
    - 이미지 리사이즈
    - 반투명 텍스트 박스
    - 텍스트 자동 줄바꿈
    """

    # 1) Base 이미지 로드
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(target_size, Image.LANCZOS)

    # 2) 폰트 설정
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    font_size = 42
    font = ImageFont.truetype(font_path, font_size)

    # 3) 텍스트 줄바꿈 처리
    wrapped_text = textwrap.fill(text, width=22)

    # 4) Draw 객체
    draw = ImageDraw.Draw(img)

    # 5) 텍스트 bbox 계산 (최신 Pillow 방식)
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 6) 중앙 하단 배치
    padding = 50
    x = (img.width - text_w) // 2
    y = img.height - text_h - padding

    # 7) 반투명 박스
    box_padding = 40
    box_coords = [
        x - box_padding,
        y - box_padding,
        x + text_w + box_padding,
        y + text_h + box_padding
    ]

    draw.rectangle(box_coords, fill=(0, 0, 0, 160))

    # 8) 텍스트 그리기
    draw.multiline_text((x, y), wrapped_text, fill=(255, 255, 255, 255), font=font)

    # 9) 파일 저장
    img.save(output_path)

    return output_path
