import openai
import json
import re
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드 및 API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_json(text):
    """
    GPT 응답에서 JSON 부분만 추출합니다.
    """
    # JSON 블록이 ```json ... ``` 형식으로 감싸져 있다면 추출
    json_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    # 텍스트 전체가 JSON 형식인지 확인
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        return None

def analyze_itb_chunk(chunk_id, text):
    """
    ITB 문서 청크에 대해 위험 문장 검출, ITB Q&A 생성, 그리고 중요도 평가 정보를
    최종 JSON 구조로 반환하는 함수.
    
    최종 JSON 구조:
    {
      "chunk_id": "chunk-001",
      "original_text": "청크의 원본 내용",
      "detected_risks": [
         {
           "id": "risk-001",
           "detected_at": "2025-01-20T15:30:00Z",
           "risk_level": "very high",  // (5단계: very high, high, medium, low, very low)
           "risk_category": "계약 조건 위반",
           "clause": "문장 내용",
           "risk": "위험 요약 설명",
           "notes": "추가 코멘트",
           "related_entities": [
             {"type": "날짜", "value": "2025-06-30"},
             {"type": "금액/비율", "value": "10%"}
           ],
           "mitigation_strategy": "추천 대응 전략",
           "external_references": [
             {
               "reference_type": "법규",
               "name": "계약법",
               "notes": "설명",
               "link": null
             }
           ]
         },
         ...
      ],
      "itb_qa": [
         {
           "question": "질문 내용",
           "answer": "답변 내용"
         },
         ...
      ],
      "analysis_rating": {
         "importance_score": 8.5,
         "target_audience": ["프로젝트 관리팀", "법무팀"],
         "tags": ["계약 조건", "일정 관리", "위험 평가"]
      }
    }
    
    만약 해당 청크에서 관련 정보가 없다면, 각 항목은 빈 배열 또는 빈 객체로 반환하세요.
    
    Args:
        chunk_id (str): 청크의 고유 ID (예: "chunk-001")
        text (str): 분석할 청크 텍스트
        
    Returns:
        str: 위 최종 JSON 구조에 맞춘 JSON 형식의 문자열
    """
    
    prompt = f"""
다음은 ITB(입찰요청서) 문서의 일부 청크에 대한 내용입니다. 
해당 청크에 대해 아래 세 가지 분석을 수행하여, 결과를 오직 아래와 같은 유효한 JSON 객체로 반환해 주세요.

1. [청크 기반 위험 분석 (detected_risks)]
   - 각 위험 요소에 대해 아래 정보를 추출합니다.
     - id: 고유 식별자 (예: "risk-001")
     - detected_at: 위험 검출 시각 (ISO 8601 형식)
     - risk_level: 위험 수준 (very high, high, medium, low, very low)
     - risk_category: 예를 들어 "계약 조건 위반", "가격 변동", "보증 불이행" 등
     - clause: 원문에서 해당 문장의 핵심 내용
     - risk: 위험 요약 설명
     - notes: 추가 검토 사항이나 주석
     - related_entities: 배열, 각 객체는 {{"type": "날짜", "value": "2025-06-30"}}와 같이 구성
     - mitigation_strategy: 추천 대응 전략 (예: "프로젝트 일정 모니터링 시스템 도입...")
     - external_references: 배열, 각 객체는 {{"reference_type": "법규", "name": "계약법", "notes": "설명", "link": null}} 형식

2. [ITB Q&A 생성 (itb_qa)]
   - 청크 내의 핵심 정보를 기반으로 짧은 질문과 답변 세트를 작성합니다.
     예를 들어, "계약 완료 기한은 언제인가요?"와 "2025년 6월 30일까지 완료되어야 합니다."와 같이 작성합니다.

3. [청크별 중요도 평가 및 태깅 (analysis_rating)]
   - 해당 청크의 전체 내용을 분석하여, 중요도를 0~10 점수로 평가하고,
     이 정보가 주로 어떤 대상(예: "프로젝트 관리팀", "법무팀")에 중요한지와
     관련 태그(예: "계약 조건", "일정 관리", "위험 평가")를 부여합니다.

최종 출력은 아래 JSON 형식과 동일해야 합니다.
{{
  "chunk_id": "{chunk_id}",
  "original_text": "{text}",
  "detected_risks": [ ... ],
  "itb_qa": [ ... ],
  "analysis_rating": {{
      "importance_score": <숫자>,
      "target_audience": [ ... ],
      "tags": [ ... ]
  }}
}}

반드시 오직 유효한 JSON 객체만 반환해 주세요.
만약 해당 정보가 없다면, 각 항목은 빈 배열 [] 또는 빈 객체 {{}} 로 반환하세요.

분석할 청크:
{text}
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # 최신 모델 지정
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2500
        )
        raw_content = response.choices[0].message.content.strip()
        extracted = extract_json(raw_content)
        if extracted is None:
            print("JSON 추출 실패. 원문 응답:", raw_content)
            json_result = {
                "chunk_id": chunk_id,
                "original_text": text,
                "detected_risks": [],
                "itb_qa": [],
                "analysis_rating": {}
            }
        else:
            try:
                json_result = json.loads(extracted)
                # 만약 chunk_id나 original_text가 응답에 포함되어 있지 않으면 추가
                if "chunk_id" not in json_result:
                    json_result["chunk_id"] = chunk_id
                if "original_text" not in json_result:
                    json_result["original_text"] = text
            except json.JSONDecodeError as json_err:
                print("JSON 디코딩 에러:", json_err)
                json_result = {
                    "chunk_id": chunk_id,
                    "original_text": text,
                    "detected_risks": [],
                    "itb_qa": [],
                    "analysis_rating": {}
                }
        return json.dumps(json_result, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"GPT API 호출 에러: {e}")
        fallback = {
            "chunk_id": chunk_id,
            "original_text": text,
            "detected_risks": [],
            "itb_qa": [],
            "analysis_rating": {}
        }
        return json.dumps(fallback, ensure_ascii=False)

# 예시: 각 청크에 대해 분석 수행
if __name__ == "__main__":
    sample_chunks = [
        # 청크 1: 계약 이행 및 안전 관리 관련 (EPC 공사 완료 및 안전 관리)
        """
        제1조 (공사 수행 및 완료)
        1. 발주자는 수급자에게 본 EPC 공사의 수행을 의뢰하며, 수급자는 이에 따라 2025년 6월 30일까지 전체 공사를 완료하여야 합니다.
        2. 공사 진행 중 발생할 수 있는 예기치 않은 상황에 대비하여, 수급자는 사전 위험 평가를 실시하고, 공사 진행 상황에 따른 리스크 모니터링 시스템을 구축하여야 합니다.
        3. 본 계약에 명시된 기한 내에 공사가 완료되지 않을 경우, 수급자는 지연 일수에 따라 계약 금액의 10%에 해당하는 벌금을 납부하여야 하며, 추가로 발생하는 손해에 대해 배상할 책임을 집니다.
        4. 더불어, 현지 정부 및 안전 관련 법규에 따라 작업 안전 점검, 승인 절차 및 안전 보증 문서의 제출이 의무화되며, 이에 따른 모든 비용은 수급자가 부담합니다.
        """,

        # 청크 2: 원자재 가격 변동 및 환율 관련 조항 (가격 재협상 및 환율 변동 조정)
        """
        제2조 (원자재 가격 변동 및 재협상)
        1. 본 계약의 이행 중 원자재 가격이 국제 시장 평균 대비 15% 이상 상승할 경우, 수급자와 발주자는 협의를 통해 계약 금액의 재협상을 실시하기로 합의합니다.
        2. 재협상 조건은 사전에 정해진 기준에 따라 산출되며, 관련 시장 동향 보고서 및 국제 원자재 가격 지수를 참고하여 공정한 가격 산정을 진행합니다.
        3. 또한, 본 계약 기간 동안 발생할 수 있는 환율 변동에 대비하여, 환율 변동률에 따른 추가 조정 조건을 계약서 부속 문서에 명시하며, 이에 따른 보정 절차를 사전에 마련합니다.
        4. 수급자는 정기적으로 환율 및 원자재 가격 변동 현황을 보고하며, 발주자는 이를 기반으로 계약 조건 변경 여부를 결정합니다.
        """,

        # 청크 3: 보증 조건 및 분쟁 해결 관련 조항 (보증금, 보증 이행 및 분쟁 조정)
        """
        제3조 (보증 조건 및 분쟁 해결)
        1. 수급자는 계약 이행을 보증하기 위하여 계약 보증금을 납입하며, 보증금 산정 기준 및 반환 조건은 별도의 보증 관련 부속 문서에 상세히 규정합니다.
        2. 보증 조건은 공사의 특성, 기간, 금액 등을 고려하여 산정되며, 보증 이행과 관련한 법적 책임은 수급자가 전적으로 부담합니다.
        3. 보증 조건의 모호한 서술이나 해석의 여지가 있는 경우, 추후 발생할 수 있는 분쟁을 예방하기 위하여, 관련 법규(예: 보증법) 및 현지 규정을 준수하여 명확하게 기재되어야 합니다.
        4. 분쟁 발생 시, 당사자 간의 협의로 해결되지 않을 경우, 중립적인 제3자 중재 기관의 개입을 통해 신속하고 공정한 해결 절차를 진행합니다.
        """,

        # 청크 4: 독소조항이 포함된 불공정 조항 (일방 당사자 유리 및 면책 조항)
        """
        제4조 (불공정 조항 및 면책 조건)
        1. 본 계약의 일부 조항은 발주자에게 전면적인 권한을 부여하고, 수급자에게는 이의 제기나 계약 해지에 관한 어떠한 권리도 부여하지 않는 것으로 구성됩니다.
        2. 특히, 계약 위반 시 발생하는 모든 손해배상 책임은 수급자에게 전적으로 전가되며, 이로 인한 금전적 손실에 대해 발주자는 어떠한 배상 책임도 지지 않습니다.
        3. 계약 해지에 관한 조항 역시 발주자에게 유리하게 작성되어 있으며, 수급자는 어떠한 사유로도 계약 해지 권리를 행사할 수 없습니다.
        4. 이러한 조항들은 수급자에게 과도한 부담을 주어, 장래 발생할 수 있는 법적 분쟁 및 금전적 손실의 위험을 크게 증가시키므로, 신중한 재검토가 필요합니다.
        """,

        # 청크 5: 독소조항이 거의 없는 공정한 계약 조항 (양 당사자 간의 균형과 협의)
        """
        제5조 (공정한 계약 조건 및 상호 협의)
        1. 본 계약은 발주자와 수급자 간의 권리와 의무를 공정하게 규정하며, 모든 조항은 상호 협의를 통해 수정 및 보완될 수 있도록 구성됩니다.
        2. 계약 위반 시 손해배상 책임은 양측이 균등하게 부담하도록 하며, 계약 해지 조항 역시 어느 한쪽에도 과도한 불리함이 없도록 작성됩니다.
        3. 분쟁 발생 시, 당사자들은 중립적인 제3자 중재 기관의 개입을 통해 신속하고 공정하게 문제를 해결하며, 법적 절차는 최소화합니다.
        4. 또한, 본 계약에 포함된 모든 조건은 관련 법규 및 국제 기준을 준수하며, 계약서 작성 시 공정성과 투명성을 최우선으로 고려하여 작성됩니다.
        """,

        # 청크 6: 리스크가 거의 없는 일반적인 조항 (일반적이고 평화로운 계약 이행을 위한 기본 약속)
        """
        제6조 (상호 협력 및 일반 조항)
        1. 본 계약은 양 당사자 간의 신뢰와 상호 존중을 바탕으로 체결되며, 양측은 성실히 계약의 목적을 달성하기 위해 노력할 것을 약속합니다.
        2. 당사자들은 공정한 협의를 통해 모든 분쟁 사항을 우선적으로 해결하며, 특별한 사유가 없는 한 일반적인 계약 조건에 따라 문제를 조정합니다.
        3. 본 계약의 모든 조항은 어떠한 당사자에게도 과도한 부담을 부과하지 않으며, 상호 이익과 원활한 협력을 위한 기본적인 운영 원칙을 준수합니다.
        4. 또한, 계약 이행 과정에서 발생하는 일상적인 행정 및 운영 사항은 양 당사자 간의 원활한 소통을 통해 조율되며, 불필요한 리스크 요소는 최대한 배제합니다.
        """
    ]

    
    for i, chunk in enumerate(sample_chunks, start=1):
        chunk_id = f"chunk-{i:03d}"
        result_json = analyze_itb_chunk(chunk_id, chunk)
        print(result_json)
