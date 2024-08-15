import os
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
import scrapetube
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from openai import OpenAI
import questionary


# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

def get_video_details(video_url):
    try:
        response = requests.get(video_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        date_element = soup.find('meta', itemprop='uploadDate')
        date = date_element['content'] if date_element else 'Unknown date'
        
        views_element = soup.find('meta', itemprop='interactionCount')
        views = views_element['content'] if views_element else 'Unknown views'
        
        return {'date': date, 'views': views}
    except Exception as e:
        logging.error(f"Error getting video details: {str(e)}")
        return {'date': 'Unknown date', 'views': 'Unknown views'}

def get_video_transcript(video_id, language='ko'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return " ".join([text['text'] for text in transcript])
    except NoTranscriptFound:
        logging.warning(f"No transcript found for video {video_id}")
        return None
    except Exception as e:
        logging.error(f"Error getting transcript for video {video_id}: {str(e)}")
        return None

def generate_summary(script):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": """다음 프롬프트를 사용하여 부동산 콘텐츠의 스크립트로부터 인사이트 리포트를 생성하세요.:

                1. 콘텐츠 개요
                2. 상담의 목적과 내용
                3. 전체 콘텐츠의 주요 키워드
                4. 상세 내용
                5. 언급된 주요 지역
                6. 주요한 인사이트(교훈)
                7. 그래서 내집마련을 원하는 내가 알아야할 결론

                이 요약 리포트는 콘텐츠의 핵심을 빠르게 파악하고, 개인 투자자에게 유용한 인사이트를 얻는 데 도움이 되어야 합니다."""},
                {"role": "user", "content": f"Here is the script: {script}"}
            ]
        )
        return response.choices[0].message.content  # content만 반환

    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        return None

def format_date(date_string):
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
        return date_object.strftime("%Y년 %m월 %d일")
    except ValueError:
        logging.warning(f"Date format error: {date_string}")
        return "날짜 정보 없음"

def format_views(views):
    try:
        return f"{int(views):,}"
    except ValueError:
        logging.warning(f"Views format error: {views}")
        return "조회수 정보 없음"

def get_thumbnail_url(video_id):
    return f"https://img.youtube.com/vi/{video_id}/0.jpg"

def create_markdown(videos):
    markdown_content = "# 부동산 상담 콘텐츠 요약\n\n"
    
    for video in videos:
        title = video.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title')
        video_id = video.get('videoId', 'Unknown ID')
        url = f"https://www.youtube.com/watch?v={video_id}"
        date = video.get('details', {}).get('date', 'Unknown Date')
        views = video.get('details', {}).get('views', 'Unknown Views')
        
        markdown_content += f"## [{title}]({url})\n\n"
        markdown_content += f"![썸네일](https://img.youtube.com/vi/{video_id}/0.jpg)\n\n"
        markdown_content += f"- 업로드 날짜: {date}\n"
        markdown_content += f"- 조회수: {views}회\n\n"
        
        if 'summary' in video and video['summary']:
            markdown_content += f"### 요약\n\n{video['summary']}\n\n"  # 직접 summary 내용 사용
        else:
            markdown_content += "### 요약\n\n요약 정보가 없습니다.\n\n"
        
        markdown_content += "---\n\n"
    
    return markdown_content

def scrape_and_summarize_youtube_videos(channel_url, video_count):
    try:
        videos = list(scrapetube.get_channel(channel_url=channel_url, limit=video_count))
        logging.info(f"Retrieved {len(videos)} videos from the channel")

        for video in videos:
            video_id = video['videoId']
            video['url'] = f"https://www.youtube.com/watch?v={video_id}"
            video['details'] = get_video_details(video['url'])
            video['script'] = get_video_transcript(video_id)
            video['script_true'] = video['script'] is not None
            video['length'] = len(video['script']) if video['script'] else 0
            time.sleep(0.1)

        for video in videos:
            if video['script_true']:
                video['summary'] = generate_summary(video['script'])  # 이미 content만 반환됨
                logging.info(f"Generated summary for video: {video['title']}")
            else:
                video['summary'] = None
                logging.warning(f"No script available for video: {video['title']}")
            time.sleep(0.1)

        channel_name = channel_url.split("/")[-1]
        today_date = datetime.now().strftime("%Y%m%d")
        json_filename = f"{channel_name}_{today_date}_{video_count}videos.json"
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=4, ensure_ascii=False, default=str)
        logging.info(f"Created JSON file: {json_filename}")

        markdown_content = create_markdown(videos)
        markdown_filename = f"{channel_name}_{today_date}_{video_count}videos_summary.md"
        
        with open(markdown_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        logging.info(f"Created Markdown file: {markdown_filename}")

        return videos, json_filename, markdown_filename

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return None, None, None


def is_valid_youtube_channel(url):
    return url.startswith("https://www.youtube.com/@")

if __name__ == "__main__":
    # 채널 URL 입력 받기
    channel_url = questionary.text(
        "YouTube 채널 URL을 입력해주세요 (예: https://www.youtube.com/@channelname):",
        validate=lambda text: True if is_valid_youtube_channel(text) else "올바른 YouTube 채널 URL을 입력해주세요."
    ).ask()

    # 비디오 개수 입력 받기
    video_count = questionary.text(
        "몇 개의 최신 영상을 분석하시겠습니까? (1-100 사이의 숫자를 입력해주세요):",
        validate=lambda text: text.isdigit() and 1 <= int(text) <= 100
    ).ask()
    video_count = int(video_count)

    print(f"선택한 채널: {channel_url}")
    print(f"분석할 영상 수: {video_count}")

    # 사용자 확인
    if questionary.confirm("분석을 시작하시겠습니까?").ask():
        videos, json_file, markdown_file = scrape_and_summarize_youtube_videos(channel_url, video_count)
        if videos:
            print(f"프로세스가 완료되었습니다. {json_file}와 {markdown_file}에서 결과를 확인하세요.")
        else:
            print("프로세스가 실패했습니다. 로그를 확인해주세요.")
    else:
        print("프로그램을 종료합니다.")
