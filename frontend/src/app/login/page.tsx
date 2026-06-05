"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@kannondo.local");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const data = await apiFetch<{ access_token: string }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      localStorage.setItem("token", data.access_token);
      router.push("/");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao iniciar sessão");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[70vh] p-6 bg-slate-50">
      <form onSubmit={handleLogin} className="card p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-2 text-center text-slate-900">Login</h1>
        <p className="text-sm text-slate-500 text-center mb-6">Acesso de administrador</p>
        {error && <p className="text-red-600 text-sm mb-4 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</p>}
        <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
        <input
          type="email"
          className="input w-full mb-4"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
        <input
          type="password"
          className="input w-full mb-6"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit" className="btn-primary w-full py-2.5">
          Entrar
        </button>
        <p className="text-xs text-slate-500 mt-4 text-center">Default: admin@kannondo.local / admin123</p>
      </form>
    </div>
  );
}
