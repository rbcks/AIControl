import QuestionCard from "../components/QuestionCard.jsx";
import { useAssessmentStore } from "../store.js";

function Test() {
  const { currentQuestion, answerQuestion, loading, answers, queue, error } = useAssessmentStore();

  const answeredCount = Object.keys(answers).length;
  const remaining = queue.length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between rounded-xl bg-slate-800/60 px-6 py-4 text-sm text-slate-200">
        <span>
          응답 수: {answeredCount} / 남은 문항: {Math.max(remaining - 1, 0)}// Answers vs remaining count.
        </span>
        {loading && <span className="text-indigo-300">계산 중...// Calculating...</span>}
      </div>
      {error && (
        <div className="rounded-lg border border-red-500/50 bg-red-500/10 px-4 py-3 text-red-200">
          {error}
        </div>
      )}
      <QuestionCard question={currentQuestion} onAnswer={answerQuestion} loading={loading} />
    </div>
  );
}

export default Test;
