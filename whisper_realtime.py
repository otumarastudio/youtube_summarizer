import openai
import sounddevice as sd
import numpy as np
import io
import wave
from dotenv import load_dotenv
import os
import signal
from gpt_NER import extract_stock_info_gpt4o
import json

# .env 파일 로드 및 API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 녹음 설정
samplerate = 44100  # 샘플링 레이트
channels = 1        # 모노 오디오
blocksize = 1024    # 오디오 청크 사이즈

# 버퍼 설정
buffer_duration = 5  # 버퍼할 오디오 길이(초)
overlap_duration = 1  # 오버랩 길이(초)
buffer_size = int(samplerate * buffer_duration)
overlap_size = int(samplerate * overlap_duration)
audio_buffer = np.zeros((buffer_size, channels), dtype=np.float32)
buffer_index = 0

# 전체 음성 기록을 위한 변수들
all_transcripts = []
is_running = True

def signal_handler(signum, frame):
    """Ctrl+C 처리를 위한 시그널 핸들러"""
    global is_running
    print("\n음성 인식을 종료하고 결과를 분석합니다...")
    is_running = False

def audio_callback(indata, frames, time, status):
    """오디오 데이터가 들어올 때마다 호출되는 콜백 함수."""
    global buffer_index, audio_buffer
    if status:
        print(status)
    
    # 버퍼에 새 데이터 추가
    space_left = buffer_size - buffer_index
    if frames <= space_left:
        audio_buffer[buffer_index:buffer_index + frames] = indata
        buffer_index += frames
    else:
        # 버퍼가 가득 차면 처리
        audio_buffer[buffer_index:] = indata[:space_left]
        process_audio_chunk(audio_buffer.copy())
        
        # 오버랩을 위해 마지막 부분을 버퍼의 시작으로 복사
        audio_buffer[:overlap_size] = audio_buffer[-overlap_size:]
        buffer_index = overlap_size
        
        # 남은 데이터 처리
        remaining_data = indata[space_left:]
        if len(remaining_data) > 0:
            audio_buffer[buffer_index:buffer_index + len(remaining_data)] = remaining_data
            buffer_index += len(remaining_data)

def process_audio_chunk(audio_data):
    """오디오 청크를 Whisper API로 STT 변환하고 텍스트 출력."""
    pcm_audio = (audio_data * 32767).astype(np.int16)
    byte_io = io.BytesIO()

    with wave.open(byte_io, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setframerate(samplerate)
        wf.setsampwidth(2)
        wf.writeframes(pcm_audio.tobytes())
    
    byte_io.seek(0)

    try:
        transcript = openai_stt(byte_io)
        if transcript.strip():
            print("🎤: " + transcript)
            all_transcripts.append(transcript)
    except Exception as e:
        print(f"STT 변환 에러: {e}")

def openai_stt(audio_file):
    """OpenAI Whisper API를 사용하여 음성을 텍스트로 변환."""
    audio_file.name = "recording.wav"
    # Using a potentially better model for transcription
    transcript = openai.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        language="ko"
    )
    return transcript.text

def analyze_transcripts():
    """모든 트랜스크립트를 결합하고 NER 분석 수행"""
    if not all_transcripts:
        print("분석할 텍스트가 없습니다.")
        return
    
    full_text = " ".join(all_transcripts)
    print("\n=== 전체 인식된 텍스트 ===")
    print(full_text)
    print("\n=== 주식 정보 분석 결과 ===")
    
    try:
        stock_info = extract_stock_info_gpt4o(full_text)
        
        # JSON 파싱 시도
        try:
            if isinstance(stock_info, str):
                parsed_info = json.loads(stock_info)
            else:
                parsed_info = stock_info

            if parsed_info and len(parsed_info) > 0:
                for info in parsed_info:
                    print(f"\n주식 종목 정보:")
                    print(f"- 종목: {info.get('종목', 'N/A')}")
                    print(f"- 가격: {info.get('가격', 'N/A')}")
                    print(f"- 액션: {info.get('액션', 'N/A')}")
                    print(f"- 의견: {info.get('의견', 'N/A')}")
                    print(f"- 감성: {info.get('감성', 'N/A')}")
            else:
                print("주식 관련 정보를 찾을 수 없습니다.")
        
        # JSON 파싱 실패시 원본 출력
        except json.JSONDecodeError:
            print("GPT 분석 결과:")
            print(stock_info)
        except Exception as e:
            print("GPT 분석 결과 (구조화 실패):")
            print(stock_info)
            
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")

def realtime_transcription():
    """실시간 음성 녹음 및 STT 변환 시작."""
    global is_running
    
    print("실시간 음성 텍스트 변환 시작... 마이크에 대고 말하세요.")
    print("Ctrl+C를 눌러 종료하고 분석을 시작합니다.\n")

    # Ctrl+C 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)

    try:
        with sd.InputStream(samplerate=samplerate,
                          channels=channels,
                          blocksize=blocksize,
                          callback=audio_callback):
            while is_running:
                sd.sleep(100)
            
            # 종료 시 분석 수행
            analyze_transcripts()
            
    except sd.PortAudioError as e:
        print(f"오디오 에러 발생: {e}")
        print("사용 가능한 오디오 장치 목록:")
        print(sd.query_devices())

if __name__ == '__main__':
    realtime_transcription()
