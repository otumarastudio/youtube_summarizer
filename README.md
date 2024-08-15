# 📺 YouTube Channel Video Summarizer

[![Python Version](https://img.shields.io/badge/python-3.12.1-blue)]
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

YouTube Channel Video Summarizer는 YouTube 채널의 여러 동영상 내용을 자동으로 요약하여 마크다운 파일로 생성하는 Python 기반 도구입니다.

## 🌟 주요 기능

- YouTube 채널에서 지정된 수의 최신 동영상 정보 추출
- 각 동영상의 스크립트 추출 및 AI를 활용한 내용 요약
- 요약된 내용을 포함한 마크다운 파일 생성

## 🛠️ 설치 방법

1. 저장소 클론:
   ```
   git clone https://github.com/otumarastudio/youtube_summarizer.git
   cd youtube-summarizer
   ```

2. 가상 환경 생성 및 활성화:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows의 경우: venv\Scripts\activate
   ```

3. 필요한 패키지 설치:
   ```
   pip install -r requirements.txt
   ```

4. OpenAI API 키 설정:
   - `.env` 파일 생성 후 다음 내용 추가:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## 🚀 사용 방법

1. 스크립트 실행:
   ```
   python youtube_summarizer.py
   ```

2. 프롬프트에 따라 YouTube 채널 ID 포함된 URL과 요약할 동영상 수 입력

3. 생성된 마크다운 파일에서 요약 내용 확인

## 🔮 향후 계획

- 단일 YouTube 동영상 URL을 입력받아 요약하는 기능 추가
- 사용자 친화적인 웹 UI 개발

## 🤝 기여하기

프로젝트 개선에 관심이 있으시다면 이슈를 열거나 풀 리퀘스트를 제출해 주세요.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
