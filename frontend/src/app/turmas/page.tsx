"use client";

import { useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { apiFetch } from "@/lib/api";

interface Modalidade {
  id: number;
  nome: string;
}

interface Turma {
  id: number;
  nome: string;
  horario: string | null;
  modalidade_id: number;
  modalidade_nome: string;
}

export default function TurmasPage() {
  const [turmas, setTurmas] = useState<Turma[]>([]);
  const [modalidades, setModalidades] = useState<Modalidade[]>([]);
  const [nome, setNome] = useState("");
  const [horario, setHorario] = useState("");
  const [modalidadeId, setModalidadeId] = useState("");
  const [showForm, setShowForm] = useState(false);

  const load = async () => {
    const [t, m] = await Promise.all([
      apiFetch<Turma[]>("/turmas/"),
      apiFetch<Modalidade[]>("/modalidades/"),
    ]);
    setTurmas(t);
    setModalidades(m);
    if (m.length && !modalidadeId) setModalidadeId(String(m[0].id));
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await apiFetch("/turmas/", {
      method: "POST",
      body: JSON.stringify({
        modalidade_id: Number(modalidadeId),
        nome,
        horario: horario || null,
      }),
    });
    setNome("");
    setHorario("");
    setShowForm(false);
    load();
  };

  return (
    <div className="page-container">
      <div className="flex justify-between items-center mb-6">
        <h1 className="page-title">Turmas</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus size={18} /> Nova turma
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card p-4 mb-6 flex gap-3 flex-wrap items-end">
          <div className="flex flex-col gap-1 min-w-[160px]">
            <label className="text-sm font-medium text-slate-700">Modalidade</label>
            <select className="input" value={modalidadeId} onChange={(e) => setModalidadeId(e.target.value)}>
              {modalidades.map((m) => (
                <option key={m.id} value={m.id}>{m.nome}</option>
              ))}
            </select>
          </div>
          <div className="flex flex-col gap-1 flex-1 min-w-[180px]">
            <label className="text-sm font-medium text-slate-700">Nome da turma</label>
            <input className="input" placeholder="Ter/Qui 20h" value={nome} onChange={(e) => setNome(e.target.value)} required />
          </div>
          <div className="flex flex-col gap-1 flex-1 min-w-[160px]">
            <label className="text-sm font-medium text-slate-700">Horário</label>
            <input className="input" placeholder="Opcional" value={horario} onChange={(e) => setHorario(e.target.value)} />
          </div>
          <button type="submit" className="btn-success">Criar</button>
        </form>
      )}

      <div className="card overflow-hidden">
        <table className="w-full text-left">
          <thead className="table-head">
            <tr>
              <th className="px-4 py-3">Modalidade</th>
              <th className="px-4 py-3">Turma</th>
              <th className="px-4 py-3">Horário</th>
            </tr>
          </thead>
          <tbody>
            {turmas.length === 0 ? (
              <tr>
                <td colSpan={3} className="table-cell text-center text-slate-500 py-8">
                  Nenhuma turma registada. Crie a primeira acima.
                </td>
              </tr>
            ) : (
              turmas.map((t) => (
                <tr key={t.id} className="hover:bg-slate-50">
                  <td className="table-cell">{t.modalidade_nome}</td>
                  <td className="table-cell font-medium">{t.nome}</td>
                  <td className="table-cell text-slate-500">{t.horario || "—"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
