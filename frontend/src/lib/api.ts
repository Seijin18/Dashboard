function resolveApiUrl(): string {
  if (typeof window !== "undefined") {
    return process.env.NEXT_PUBLIC_FASTAPI_URL || "http://localhost:8000";
  }
  return (
    process.env.FASTAPI_URL ||
    process.env.NEXT_PUBLIC_FASTAPI_URL ||
    "http://localhost:8000"
  );
}

const API_URL = resolveApiUrl();

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${resolveApiUrl()}${path}`;

  let res: Response;
  try {
    res = await fetch(url, { ...options, headers });
  } catch {
    throw new Error(
      `Não foi possível ligar à API em ${url}. Verifique se o backend está a correr (porta 8000).`
    );
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Erro na API");
  }
  return res.json();
}

export { API_URL, resolveApiUrl };
