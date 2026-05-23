export class ApiError extends Error {
  status: number;
  details: unknown;
  constructor(message: string, status: number, details?: unknown) {
    super(message);
    this.status = status;
    this.details = details;
  }
}

export async function api<T = any>(path: string, options: RequestInit = {}): Promise<T> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 120000);
  try {
    const response = await fetch(path, {
      ...options,
      signal: controller.signal,
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    });
    const text = await response.text();
    let data: any = null;
    if (text) {
      try { data = JSON.parse(text); } catch { data = text; }
    }
    if (!response.ok) {
      const message = typeof data === 'object' && data?.detail
        ? Array.isArray(data.detail) ? data.detail.map((x: any) => x.msg || JSON.stringify(x)).join('; ') : String(data.detail)
        : `Ошибка API ${response.status}`;
      throw new ApiError(message, response.status, data);
    }
    return data as T;
  } finally {
    window.clearTimeout(timeout);
  }
}

export const getScenarioTemplates=()=>api<any[]>('/api/scenarios/templates');
export const startDialog=(scenarioTemplateId:string)=>api<any>('/api/dialog/start',{method:'POST',body:JSON.stringify({scenario_template_id:scenarioTemplateId})});
export const answerDialog=(sessionState:any,questionId:string,answer:any)=>api<any>('/api/dialog/answer',{method:'POST',body:JSON.stringify({session_state:sessionState,question_id:questionId,answer})});
export const getDialogPreview=(sessionState:any)=>api<any>('/api/dialog/preview',{method:'POST',body:JSON.stringify({session_state:sessionState})});
export const analyzeGuided=(sessionState:any)=>api<any>('/api/analyze/guided',{method:'POST',body:JSON.stringify({session_state:sessionState})});
