import pandas as pd
import json
import numpy as np
from datetime import datetime

def process_excel_data():
    """Excel 데이터를 처리하고 대시보드용 JSON 생성"""
    try:
        # Excel 파일 읽기
        df = pd.read_excel('sample_fps_aimbot_data.xlsx')
        
        print("데이터 처리 중...")
        print(f"총 행 수: {len(df)}")
        print(f"총 열 수: {len(df.columns)}")
        
        # 유니크한 플레이어별로 데이터 그룹화
        users_data = {}
        
        for player_id in df['player'].unique():
            player_data = df[df['player'] == player_id]
            
            # 기본 통계 계산
            cheater_status = player_data['cheater'].iloc[0] if 'cheater' in player_data.columns else 0
            game_id = player_data['game'].iloc[0] if 'game' in player_data.columns else "unknown"
            
            # 시퀀스 데이터 추출
            aim_sequences = []
            for _, row in player_data.iterrows():
                if pd.notna(row.get('series_1_data')) and pd.notna(row.get('series_2_data')):
                    try:
                        # 시리즈 데이터를 파싱 (문자열로 저장된 경우)
                        x_data = parse_series_data(row.get('series_1_data'))
                        y_data = parse_series_data(row.get('series_2_data'))
                        z_data = parse_series_data(row.get('series_3_data', '[]'))
                        
                        if len(x_data) > 0 and len(y_data) > 0:
                            aim_sequences.append({
                                'seq_group': row.get('seq_group', 0),
                                'x': x_data,
                                'y': y_data,
                                'z': z_data if len(z_data) > 0 else [0] * len(x_data),
                                'timestamp': row.get('series_start_time', 0)
                            })
                    except Exception as e:
                        print(f"시퀀스 데이터 파싱 오류 (Player {player_id}): {e}")
                        continue
            
            # FPS 통계 시뮬레이션 (실제 데이터가 없으므로)
            kd_ratio = simulate_kd_ratio(cheater_status)
            headshot_rate = simulate_headshot_rate(cheater_status)
            accuracy = simulate_accuracy(cheater_status)
            reaction_time = simulate_reaction_time(cheater_status)
            
            # 의심 점수 계산
            suspicion_score = calculate_suspicion_score(aim_sequences, cheater_status)
            
            users_data[player_id] = {
                'id': int(player_id),
                'game': game_id,
                'cheater': int(cheater_status),
                'kd_ratio': kd_ratio,
                'headshot_rate': headshot_rate,
                'accuracy': accuracy,
                'reaction_time': reaction_time,
                'suspicion_score': suspicion_score,
                'aim_sequences': aim_sequences[:5],  # 최대 5개 시퀀스만 저장
                'total_sequences': len(aim_sequences),
                'play_date': '2025-09-01',
                'map': 'de_dust2',
                'primary_weapon': 'AK-47',
                'secondary_weapon': 'Glock-18'
            }
        
        # JSON 파일로 저장
        with open('processed_data.json', 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"처리된 데이터가 processed_data.json으로 저장되었습니다.")
        print(f"총 {len(users_data)}명의 플레이어 데이터가 처리되었습니다.")
        
        return users_data
        
    except Exception as e:
        print(f"데이터 처리 오류: {e}")
        return None

def parse_series_data(series_str):
    """시리즈 데이터 문자열을 파싱하여 리스트로 변환"""
    if pd.isna(series_str) or series_str == '':
        return []
    
    try:
        # 문자열이 리스트 형태인 경우
        if isinstance(series_str, str):
            # 대괄호 제거하고 쉼표로 분리
            series_str = series_str.strip('[]')
            if series_str:
                return [float(x.strip()) for x in series_str.split(',') if x.strip()]
        elif isinstance(series_str, list):
            return [float(x) for x in series_str if pd.notna(x)]
        else:
            return [float(series_str)]
    except:
        return []

def simulate_kd_ratio(cheater_status):
    """K/D 비율 시뮬레이션"""
    if cheater_status:
        return round(np.random.uniform(2.5, 4.5), 2)
    else:
        return round(np.random.uniform(0.8, 2.0), 2)

def simulate_headshot_rate(cheater_status):
    """헤드샷 비율 시뮬레이션"""
    if cheater_status:
        return round(np.random.uniform(0.7, 0.9), 3)
    else:
        return round(np.random.uniform(0.25, 0.45), 3)

def simulate_accuracy(cheater_status):
    """명중률 시뮬레이션"""
    if cheater_status:
        return round(np.random.uniform(0.8, 0.95), 3)
    else:
        return round(np.random.uniform(0.3, 0.6), 3)

def simulate_reaction_time(cheater_status):
    """반응 시간 시뮬레이션 (ms)"""
    if cheater_status:
        return int(np.random.uniform(30, 60))
    else:
        return int(np.random.uniform(150, 250))

def calculate_suspicion_score(aim_sequences, cheater_status):
    """의심 점수 계산"""
    if not aim_sequences:
        return 0.1
    
    # 기본 의심 점수
    base_score = 0.1 if not cheater_status else 0.7
    
    # 조준 패턴 분석
    pattern_score = 0
    for seq in aim_sequences:
        if len(seq['x']) > 1 and len(seq['y']) > 1:
            # 직선성 검사
            x_variance = np.var(seq['x'])
            y_variance = np.var(seq['y'])
            
            # 매우 낮은 분산은 의심스러움
            if x_variance < 0.1 and y_variance < 0.1:
                pattern_score += 0.1
    
    # 정규화
    pattern_score = min(pattern_score / len(aim_sequences), 0.3)
    
    return round(base_score + pattern_score + np.random.uniform(-0.1, 0.1), 3)

if __name__ == "__main__":
    users_data = process_excel_data()
