import { create } from "zustand";
import { startAssessment, submitAnswer, fetchResult } from "./api";

export const useAssessmentStore = create((set, get) => ({
  view: "landing",
  sessionId: null,
  queue: [],
  currentQuestion: null,
  answers: {},
  result: null,
  loading: false,
  error: null,

  fetchInitial: async () => {
    set({ loading: true, error: null });
    try {
      const data = await startAssessment();
      set({
        view: "test",
        sessionId: data.session_id,
        queue: data.questions,
        currentQuestion: data.questions[0] ?? null,
        answers: {},
        result: null,
        loading: false,
      });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  answerQuestion: async (value) => {
    const { sessionId, currentQuestion, queue, answers } = get();
    if (!sessionId || !currentQuestion) {
      return;
    }
    set({ loading: true, error: null });
    try {
      const payload = {
        session_id: sessionId,
        question_id: currentQuestion.id,
        answer_value: value,
      };
      const response = await submitAnswer(payload);
      const newAnswers = { ...answers, [currentQuestion.id]: value };
      const nextQueue = queue.slice(1);
      if (response.next_question) {
        nextQueue.push(response.next_question);
      }
      const nextCurrent = nextQueue[0] ?? null;
      set({
        queue: nextQueue,
        currentQuestion: nextCurrent,
        answers: newAnswers,
        loading: false,
      });
      if (response.completed) {
        await get().loadResult();
      }
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  loadResult: async () => {
    const { sessionId } = get();
    if (!sessionId) return;
    set({ loading: true, error: null });
    try {
      const data = await fetchResult({ session_id: sessionId });
      set({ result: data, view: "result", loading: false });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  reset: () => {
    set({
      view: "landing",
      sessionId: null,
      queue: [],
      currentQuestion: null,
      answers: {},
      result: null,
      loading: false,
      error: null,
    });
  },
}));
