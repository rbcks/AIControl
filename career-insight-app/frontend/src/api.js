const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "API error");
  }
  return response.json();
}

export async function startAssessment() {
  const res = await fetch(`${API_BASE}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  return handleResponse(res);
}

export async function submitAnswer(payload) {
  const res = await fetch(`${API_BASE}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function fetchResult(payload) {
  const res = await fetch(`${API_BASE}/result`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}
