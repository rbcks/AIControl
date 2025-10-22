import PropTypes from "prop-types";

function QuestionCard({ question, onAnswer, loading }) {
  if (!question) {
    return (
      <div className="rounded-xl bg-slate-800/70 p-10 text-center text-slate-200">
        <p>잠시만 기다려 주세요...// Please wait...</p>
      </div>
    );
  }

  const choices = [1, 2, 3, 4, 5];

  return (
    <div className="rounded-2xl bg-slate-800/80 p-8 shadow-lg ring-1 ring-slate-700/50">
      <p className="text-sm uppercase tracking-wider text-indigo-300">
        {question.dimension}
      </p>
      <h2 className="mt-3 text-2xl font-semibold text-white">{question.text}</h2>
      <p className="mt-4 text-sm text-slate-400">
        1=전혀 아니다 / 5=매우 그렇다.// 1=Not at all / 5=Strongly agree.
      </p>
      <div className="mt-6 grid grid-cols-5 gap-3">
        {choices.map((choice) => (
          <button
            key={choice}
            onClick={() => onAnswer(choice)}
            disabled={loading}
            className="rounded-lg bg-indigo-600/80 py-3 text-lg font-medium text-white shadow transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-slate-600"
          >
            {choice}
          </button>
        ))}
      </div>
    </div>
  );
}

QuestionCard.propTypes = {
  question: PropTypes.shape({
    id: PropTypes.string,
    text: PropTypes.string,
    dimension: PropTypes.string,
  }),
  onAnswer: PropTypes.func.isRequired,
  loading: PropTypes.bool,
};

export default QuestionCard;
