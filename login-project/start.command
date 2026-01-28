#!/bin/bash
# 1. 파일이 위치한 폴더로 이동 (띄어쓰기 처리를 위해 따옴표 사용)
cd "/Users/gimhoejun/VS code/login-project"

# 2. 가상 환경 활성화
source .venv/bin/activate

# 3. 서버 실행
uvicorn main:app --reload