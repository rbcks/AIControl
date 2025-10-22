import { useMemo } from "react";
import { useAssessmentStore } from "../store.js";

function Result() {
  const { result, reset, loading, error } = useAssessmentStore();

  const shareLink = useMemo(() => {
    if (!result) return "";
    return `${window.location.origin}/share/${result.slug}`;
  }, [result]);

  if (loading && !result) {
    return (
      <div className="rounded-2xl bg-slate-800/70 p-10 text-center text-slate-200">
        결과를 계산 중입니다...// Computing result...
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-slate-800/80 p-8 shadow ring-1 ring-slate-700/60">
        <h2 className="text-2xl font-semibold text-white">추천 커리어 Top 3// Top 3 Career Tracks</h2>
        <p className="mt-2 text-slate-300">
          세션: {result.session_id} · 공유 링크: <span className="text-indigo-300">{shareLink}</span>
        </p>
      </div>
      {error && (
        <div className="rounded-lg border border-red-500/50 bg-red-500/10 px-4 py-3 text-red-200">
          {error}
        </div>
      )}
      <div className="space-y-4">
        {result.recommendations.map((item) => (
          <div
            key={item.career}
            className="rounded-2xl bg-slate-800/70 p-6 shadow-lg ring-1 ring-slate-700/50"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold text-white">{item.career}</h3>
              <span className="text-indigo-300">Score: {item.score}</span>
            </div>
            <p className="mt-2 text-slate-300">{item.description}</p>
            <div className="mt-3 text-sm text-slate-400">
              <p>적합 이유// Reasons</p>
              <ul className="list-disc pl-5">
                {item.reasons.map((reason, idx) => (
                  <li key={idx}>{reason}</li>
                ))}
              </ul>
            </div>
            <div className="mt-3 text-sm text-slate-400">
              <p>성장 로드맵// Growth Roadmap</p>
              <ul className="list-disc pl-5">
                {item.growth_plan.map((plan, idx) => (
                  <li key={idx}>{plan}</li>
                ))}
              </ul>
            </div>
            <div className="mt-4 flex gap-4 text-xs text-slate-400">
              <span>Bonus: {item.bonus}</span>
              <span>Penalty: {item.penalty}</span>
            </div>
          </div>
        ))}
      </div>
      <button
        onClick={reset}
        className="inline-flex items-center rounded-lg bg-indigo-500 px-6 py-3 text-lg font-medium text-white shadow hover:bg-indigo-400"
      >
        다시 테스트하기// Restart Test
      </button>
    </div>
  );
}

export default Result;
