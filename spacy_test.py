import spacy
from spacy.matcher import Matcher

nlp = spacy.load("ko_core_news_sm")
matcher = Matcher(nlp.vocab)

def extract_stock_info(text):
    doc = nlp(text)
    matches = matcher(doc)
    stock_info_list = []

    print("--- 토큰 정보 ---") # 디버깅 출력 시작
    for token in doc:
        print(f"Token: {token.text}, POS: {token.pos_}")
    print("--- 패턴 매칭 결과 ---") # 디버깅 출력 시작


    # 매칭된 패턴 및 정보 추출 (match_id, start, end)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # 매칭된 패턴 이름
        span = doc[start:end]         # 매칭된 토큰 스팬
        extracted_info = {}

        if string_id == "STOCK_RECOMMENDATION":
            # 패턴: [종목명] + [가격] + [매수/매도] + [추천/의견] + [긍정/부정]
            종목명 = doc[start:end-4].text  # 종목명 (매칭된 스팬에서 앞부분 추출 - 예시)
            가격정보 = doc[end-4:end-3].text # 가격 정보 (예시)
            액션 = doc[end-3:end-2].text    # 매수/매도 액션 (예시)
            의견 = doc[end-2:end-1].text    # 추천/의견 (예시)
            감성 = doc[end-1:end].text    # 긍정/부정 (예시)

            extracted_info = {
                "종목": 종목명.strip(),
                "가격": 가격정보.strip(),
                "액션": 액션.strip(),
                "의견": 의견.strip(),
                "감성": 감성.strip()
            }
            stock_info_list.append(extracted_info)
            print(f"  패턴 매칭 성공: {string_id}, 스팬: {span.text}") # 디버깅 출력: 매칭 성공 시 정보 출력

    if not stock_info_list: # 추출된 정보가 없을 때 메시지 출력
        print("  추출된 정보 없음") # 디버깅 출력: 정보 추출 실패 시 메시지 출력

    return stock_info_list
# 매칭 패턴 정의 (더욱 정교하게 다듬어야 함)
# 패턴 1: [종목명] + [가격] + "부근" + "에서" + [매수/매도] + "추천" + [감성 표현]
pattern1 = [
    {"POS": "NOUN", "OP": "+"},  # 종목명 (명사, 1개 이상) - 예시: 삼성전자, 레인보우 로보틱스 (더 구체적인 종목명 패턴 필요)
    {"TEXT": {"REGEX": r"[0-9,]+(원|만원)"}}, # 가격 (숫자 + "원" 또는 "만원")
    {"TEXT": "부근"},
    {"TEXT": "에서"},
    {"TEXT": {"IN": ["매수", "매도"]}}, # 매수 또는 매도
    {"TEXT": "추천"},
    {"TEXT": {"IN": ["드립니다", "드립니다.", "하시길", "하십시오", "바랍니다", "모아가시기", "이익실현", "하십시오"]}}, # 추천/의견 관련 표현 (더 다양하게 확장 필요)
    {"TEXT": {"IN": ["긍정", "적극", "좋습니다", "좋아보입니다", "유망합니다"] }, "OP": "?"} # 긍정/부정 감성 표현 (선택적으로 매칭, 긍정 키워드 예시, 더 확장 및 부정 키워드 추가 필요)
]
matcher.add("STOCK_RECOMMENDATION", [pattern1]) # Matcher에 패턴 추가


# 테스트 문장 (사용자 요청 문장)
test_sentences = [
    "저는 오늘 여러가지 주식을 봤지만 삼성전자 5만6천원 부근에서 매수하시길 추천 드리고, 차곡차곡 모아가시기 바랍니다. 그리고 레인보우 로보틱스는 12만원에서 최종 매도 하시고 이익실현 하시기 바랍니다."
]

for sentence in test_sentences:
    stock_info = extract_stock_info(sentence)
    print(f"\n--- 문장: {sentence} ---")
    if stock_info:
        for info in stock_info:
            print(f"  종목: {info['종목']}")
            print(f"  가격: {info['가격']}")
            print(f"  액션: {info['액션']}")
            print(f"  액션: {info['액션']}")
            print(f"  의견: {info['의견']}")
            print(f"  감성: {info['감성']}")
            print("---")
    else:
        print("  추출된 정보 없음")


        