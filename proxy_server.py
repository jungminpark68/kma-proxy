import asyncio
import winsdk.windows.devices.geolocation as wdg
from flask import Flask, jsonify

app = Flask(__name__)

# 전역 변수로 좌표 저장
current_lat = 0.0
current_lon = 0.0

async def get_windows_location():
    """윈도우 위치 서비스를 통해 정밀 좌표를 가져오는 비동기 함수"""
    global current_lat, current_lon
    
    print("🔍 윈도우 위치 서비스에 접근 중... (권한 허용 필요)")
    
    try:
        locator = wdg.Geolocator()
        # 높은 정확도 요청 (Wi-Fi 스캔 포함)
        pos = await locator.get_geoposition_async()
        
        current_lat = pos.coordinate.point.position.latitude
        current_lon = pos.coordinate.point.position.longitude
        
        print(f"✅ 위치 확보 성공!")
        print(f"   위도: {current_lat}")
        print(f"   경도: {current_lon}")
        
    except Exception as e:
        print(f"❌ 위치를 가져올 수 없습니다. (설정 -> 개인정보 -> 위치 켜져있는지 확인)")
        print(f"   에러 내용: {e}")
        # 실패 시 기본값 (서울 시청)
        current_lat = 37.5665
        current_lon = 126.9780

@app.route('/location', methods=['GET'])
def get_location():
    """ESP32가 요청하면 저장된 좌표 반환"""
    print(f"[요청] ESP32에게 좌표 전송: {current_lat}, {current_lon}")
    return jsonify({
        "lat": current_lat,
        "lon": current_lon,
        "source": "Windows Location Service (WPS)"
    })

if __name__ == '__main__':
    # 1. 먼저 윈도우 위치를 한 번 가져옵니다.
    asyncio.run(get_windows_location())
    
    # 2. 서버 시작 (0.0.0.0으로 열어야 외부/가상환경 접속 가능)
    print("🚀 로컬 GPS 서버 가동 시작 (포트 5000)")
    app.run(host='0.0.0.0', port=5000)
