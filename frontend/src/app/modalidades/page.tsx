"use client";

import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { apiFetch } from "@/lib/api";

interface Modalidade {
  id: number;
  nome: string;
  slug: string;
  ativa: boolean;
}

export default function ModalidadesPage() {
  const [modalidades, setModalidades] = useState<Modalidade[]>([]);
  const [nome, setNome] = useState("");
  const [slug, setSlug] = useState("");
  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    const data = await apiFetch<Modalidade[]>("/modalidades/");
    setModalidades(data);
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await apiFetch("/modalidades/", {
      method: "POST",
      body: JSON.stringify({ nome, slug, ativa: true, associacao_id: 1 }),
    });
    setNome("");
    setSlug("");
    setShowForm(false);
    load();
  };

  return (
    <div className="page-container">
      <div className="flex justify-between items-center mb-6">
        <h1 className="page-title">Modalidades</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus size={18} /> Nova modalidade
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card p-4 mb-6 flex gap-3 flex-wrap items-end">
          <div className="flex flex-col gap-1 flex-1 min-w-[180px]">
            <label className="text-sm font-medium text-slate-700">Nome</label>
            <input
              className="input"
              placeholder="ex.: Pilates"
              value={nome}
              onChange={(e) => {
                setNome(e.target.value);
                setSlug(e.target.value.toLowerCase().replace(/\s+/g, "-").normalize("NFD").replace(/[\u0300-\u036f]/g, ""));
              }}
              required
            />
          </div>
          <div className="flex flex-col gap-1 flex-1 min-w-[140px]">
            <label className="text-sm font-medium text-slate-700">Slug</label>
            <input className="input" placeholder="pilates" value={slug} onChange={(e) => setSlug(e.target.value)} required />
          </div>
          <button type="submit" className="btn-success">Criar</button>
        </form>
      )}

      <div className="grid gap-3 sm:grid-cols-2">
        {modalidades.map((m) => (
          <div key={m.id} className="card p-4 flex justify-between items-center">
            <div>
              <h3 className="font-semibold text-lg">{m.nome}</h3>
              <p className="text-muted text-sm">{m.slug}</p>
            </div>
            <span className={`text-xs px-3 py-1 rounded-full font-medium ${m.ativa ? "bg-emerald-100 text-emerald-800" : "bg-slate-100 text-slate-600"}`}>
              {m.ativa ? "Activa" : "Inactiva"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
