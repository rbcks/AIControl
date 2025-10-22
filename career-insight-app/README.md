# Career Insight App

"""적성 기반 커리어 추천 웹앱"""은 FastAPI와 React를 이용해 외부 사용자가 성향 테스트를 진행하고 맞춤형 커리어 로드맵을 얻을 수 있게 하는 예제 프로젝트입니다.// This sample app pairs FastAPI with React to deliver an adaptive aptitude-driven career recommendation flow.

## Project Structure// 프로젝트 구조

```
career-insight-app/
├─ backend/
│  ├─ main.py
│  ├─ models.py
│  ├─ db.py
│  ├─ engine/
│  │  ├─ scorer.py
│  │  ├─ recommender.py
│  │  ├─ state.py
│  │  └─ routing.py
│  └─ item_bank/
│     ├─ questions_v1.json
│     └─ career_profiles_v1.json
└─ frontend/
   ├─ package.json
   ├─ vite.config.js
   ├─ tailwind.config.js
   ├─ postcss.config.js
   ├─ index.html
   └─ src/
      ├─ main.jsx
      ├─ App.jsx
      ├─ index.css
      ├─ api.js
      ├─ store.js
      ├─ pages/
      │  ├─ Test.jsx
      │  └─ Result.jsx
      └─ components/
         └─ QuestionCard.jsx
```

## Backend Setup// 백엔드 설정

1. Install dependencies (FastAPI, Uvicorn, SQLAlchemy recommended via pip).// 의존성 설치(pip 이용 권장).
2. Move to the `backend/` directory and run the development server: // `backend/` 디렉토리로 이동 후 개발 서버 실행:

```bash
uvicorn main:app --reload
```

The API exposes `POST /start`, `POST /answer`, `POST /result` with CORS enabled for quick testing.// API는 빠른 테스트를 위해 CORS가 활성화된 상태로 세 개의 POST 엔드포인트를 제공합니다.

## Frontend Setup// 프론트엔드 설정

1. Navigate to `frontend/` and install packages: // `frontend/`로 이동 후 패키지 설치:

```bash
npm install
```

2. Start the Vite dev server: // Vite 개발 서버 실행:

```bash
npm run dev
```

Set the environment variable `VITE_API_BASE` if the backend is hosted elsewhere.// 백엔드가 다른 위치에 있다면 `VITE_API_BASE` 환경 변수를 설정하세요.

## Adaptive Flow Summary// 적응형 흐름 요약

- `/start`는 새로운 세션과 초기 3개 문항을 생성합니다.
- `/answer`는 가중치를 활용해 trait 벡터를 업데이트하고 다음 문항을 제공합니다.// `/answer` updates trait vectors and returns the next adaptive question.
- `/result`는 코사인 유사도, 가치 보너스, 충돌 패널티로 상위 3개 커리어 트랙을 추천합니다.// `/result` blends cosine similarity with value bonuses and conflict penalties to rank careers.

## Deployment Notes// 배포 참고

- 프론트엔드는 Vercel, 백엔드는 Render 배포를 가정합니다.
- SQLite는 기본 저장소이며 Postgres로의 확장이 가능합니다.// SQLite powers local storage, and Postgres can be adopted for production.

즐거운 커리어 탐색 되세요!// Enjoy exploring your career pathways!
