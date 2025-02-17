import openai
import json
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_stock_info_gpt4o(text):
    """
    텍스트에서 주식 관련 정보를 추출하여 JSON 형태로 반환하는 함수
    
    Args:
        text (str): 분석할 텍스트
    
    Returns:
        str: JSON 형식의 문자열. 실패시 "[]" 반환
    """
    prompt = f"""
    다음 텍스트는 음성을 인식한 결과인데, 음성인식이 정확하지 않을 수 있어서 최대한 아는 지식 내에서 음성 인식 결과를 보정하고, 그 보정결과 내에서 주식 종목에 대한 추천 정보를 추출하여 JSON 형식의 배열로 결과를 만들어주세요.
    각 종목별로 다음 정보를 포함해야 합니다:
    - 종목: 주식 종목명
    - 가격: 언급된 가격
    - 액션: 매수/매도 추천
    - 의견: 관련된 의견이나 추천 이유
    - 감성: 긍정/부정/중립

    예시:
    [
        {{
            "종목": "삼성전자",
            "가격": "70,000원",
            "액션": "매수",
            "의견": "장기적으로 성장 가능성이 높음",
            "감성": "긍정"
        }},
        {{
            "종목": "현대차",
            "가격": "200,000원",
            "액션": "매도",
            "의견": "단기적으로 하락세 예상",
            "감성": "부정"
        }}
    ]

    주식 관련 정보가 없다면 빈 배열 []을 반환하세요.

    분석할 텍스트:
    {text}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"GPT API 호출 에러: {e}")
        return "[]"