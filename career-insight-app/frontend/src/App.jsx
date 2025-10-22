import { useEffect } from "react";
import { useAssessmentStore } from "./store";
import Test from "./pages/Test.jsx";
import Result from "./pages/Result.jsx";

function App() {
  const { view, fetchInitial } = useAssessmentStore();

  useEffect(() => {
    // Preload nothing, wait for user interaction.// 미리 로드하지 않고 사용자 상호작용을 대기.
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <header className="px-6 py-8 text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-white">
          Career Insight Navigator
        </h1>
        <p className="mt-2 text-slate-300">
          성향 기반 커리어 로드맵을 발견하세요.// Discover your trait-driven career roadmap.
        </p>
      </header>
      <main className="mx-auto max-w-3xl px-6 pb-12">
        {view === "test" && <Test />}
        {view === "result" && <Result />}
        {view === "landing" && (
          <div className="rounded-2xl bg-slate-800/70 p-10 text-center shadow-xl">
            <p className="text-lg text-slate-200">
              3단계 적성 테스트로 나만의 커리어 트랙을 찾아보세요.// Take the 3-stage aptitude test.
            </p>
            <button
              onClick={fetchInitial}
              className="mt-8 inline-flex items-center rounded-lg bg-indigo-500 px-6 py-3 text-lg font-medium text-white shadow hover:bg-indigo-400"
            >
              테스트 시작// Start Test
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
