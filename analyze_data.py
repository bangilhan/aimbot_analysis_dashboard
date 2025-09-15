import pandas as pd
import json
import os

def analyze_excel_data():
    """Excel 데이터를 분석하고 JSON으로 변환"""
    try:
        # Excel 파일 읽기
        df = pd.read_excel('sample_fps_aimbot_data.xlsx')
        
        print("데이터 구조:")
        print(f"행 수: {len(df)}")
        print(f"열 수: {len(df.columns)}")
        print("\n열 이름:")
        print(df.columns.tolist())
        
        print("\n첫 5행 데이터:")
        print(df.head())
        
        print("\n데이터 타입:")
        print(df.dtypes)
        
        # 유니크한 플레이어 ID 추출
        unique_players = df['player'].unique() if 'player' in df.columns else []
        unique_games = df['game'].unique() if 'game' in df.columns else []
        
        print(f"\n유니크한 플레이어 수: {len(unique_players)}")
        print(f"플레이어 ID들: {unique_players}")
        print(f"\n유니크한 게임 수: {len(unique_games)}")
        print(f"게임 ID들: {unique_games}")
        
        # 치터 정보 확인
        if 'cheater' in df.columns:
            cheater_stats = df['cheater'].value_counts()
            print(f"\n치터 통계:")
            print(cheater_stats)
        
        # 데이터를 JSON으로 변환하여 저장
        data_dict = df.to_dict('records')
        
        with open('fps_data.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n데이터가 fps_data.json으로 저장되었습니다.")
        
        return df
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

if __name__ == "__main__":
    df = analyze_excel_data()
