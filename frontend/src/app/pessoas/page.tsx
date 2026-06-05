"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Search, ChevronRight, UserPlus } from "lucide-react";
import { apiFetch } from "@/lib/api";

interface Pessoa {
  id: number;
  nome: string;
  email: string | null;
  telefone: string | null;
}

export default function PessoasPage() {
  const [pessoas, setPessoas] = useState<Pessoa[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const q = search ? `?q=${encodeURIComponent(search)}` : "";
      const data = await apiFetch<Pessoa[]>(`/pessoas${q}`);
      setPessoas(data);
    } catch {
      setPessoas([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    load();
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await apiFetch("/pessoas/", {
      method: "POST",
      body: JSON.stringify({ nome, email: email || null }),
    });
    setNome("");
    setEmail("");
    setShowForm(false);
    load();
  };

  return (
    <div className="page-container max-w-6xl">
      <div className="flex justify-between items-center mb-6">
        <h1 className="page-title">Pessoas</h1>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2">
          <UserPlus size={18} />
          Nova pessoa
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card p-4 mb-6 flex gap-3 flex-wrap items-end">
          <div className="flex flex-col gap-1 flex-1 min-w-[200px]">
            <label className="text-sm font-medium text-slate-700">Nome</label>
            <input className="input" placeholder="Nome completo" value={nome} onChange={(e) => setNome(e.target.value)} required />
          </div>
          <div className="flex flex-col gap-1 flex-1 min-w-[200px]">
            <label className="text-sm font-medium text-slate-700">Email</label>
            <input className="input" placeholder="Opcional" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <button type="submit" className="btn-success">Guardar</button>
        </form>
      )}

      <form onSubmit={handleSearch} className="relative mb-4">
        <Search className="absolute left-3 top-2.5 text-slate-400" size={18} />
        <input
          className="input w-full pl-10"
          placeholder="Buscar por nome..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </form>

      <div className="card overflow-hidden">
        <table className="w-full text-left">
          <thead className="table-head">
            <tr>
              <th className="px-4 py-3">Nome</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={3} className="table-cell text-center text-slate-500 py-8">A carregar...</td></tr>
            ) : pessoas.length === 0 ? (
              <tr><td colSpan={3} className="table-cell text-center text-slate-500 py-8">Nenhuma pessoa encontrada</td></tr>
            ) : (
              pessoas.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50">
                  <td className="table-cell font-medium">{p.nome}</td>
                  <td className="table-cell text-slate-500">{p.email || "—"}</td>
                  <td className="table-cell text-right">
                    <Link href={`/pessoas/${p.id}`} className="text-blue-600 hover:text-blue-800 font-medium flex items-center justify-end gap-1">
                      Ver perfil <ChevronRight size={16} />
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
