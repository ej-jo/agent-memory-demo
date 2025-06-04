# Agent Memory 기능 Demo

AI Agent가 사용자와의 대화를 기억하고, 문맥에 맞게 응답할 수 있도록 구현한 데모 프로젝트입니다.

## 주요 기능

- **Streamlit UI**로 사용자 인터페이스 제공  
- **FastAPI 백엔드** 연동  
- **실시간 스트리밍 응답** 지원  
- **LangChain 기반 메모리 구조 적용** (Short-term / Long-term Memory)  
- **출처 정보 및 연관 질문 제공**

## 설치 방법

```bash
git clone https://github.com/ej-jo/agent-memory-demo.git
cd agent-memory-demo
pip install -r requirements.txt
streamlit run kt_aiagent_poc.py
```

## 디렉토리 구조

```
agent-memory-demo/
├── kt_aiagent_poc.py        # Streamlit 프론트엔드 (메인 실행 파일)
├── requirements.txt         # 필요한 파이썬 패키지
└── README.md                # 프로젝트 설명 문서
```

## 예시 질문

- "요즘 핫한 디저트가 뭐야?"
- "손님을 늘리기 위한 SNS 홍보 전략은?"
- "우리 가게 매출 분석 좀 도와줘."
- "디저트 가게 창업하려고 하는데 어떤 점을 고려해야 해?"
