"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Plus, DollarSign } from "lucide-react";
import { apiFetch } from "@/lib/api";

interface Matricula {
  id: number;
  turma_nome: string;
  modalidade_nome: string;
  status: string;
}

interface Mensalidade {
  id: number;
  matricula_id: number | null;
  mes_referencia: string;
  data_vencimento: string;
  valor_previsto: number;
  valor_pago: number | null;
  status: string;
  modalidade_nome?: string;
}

interface PessoaDetalhe {
  id: number;
  nome: string;
  email: string | null;
  matriculas: Matricula[];
}

interface Turma {
  id: number;
  nome: string;
  modalidade_nome: string;
  modalidade_id: number;
}

export default function PessoaDetalhePage() {
  const { id } = useParams();
  const [pessoa, setPessoa] = useState<PessoaDetalhe | null>(null);
  const [mensalidades, setMensalidades] = useState<Mensalidade[]>([]);
  const [turmas, setTurmas] = useState<Turma[]>([]);
  const [selectedTurma, setSelectedTurma] = useState("");
  const [loading, setLoading] = useState(true);

  const load = async () => {
    if (!id) return;
    setLoading(true);
    try {
      const [p, allMens, t] = await Promise.all([
        apiFetch<PessoaDetalhe>(`/pessoas/${id}`),
        apiFetch<Mensalidade[]>(`/mensalidades/`),
        apiFetch<Turma[]>(`/turmas/`),
      ]);
      setPessoa(p);
      const matriculaIds = new Set(p.matriculas.map((mat) => mat.id));
      setMensalidades(allMens.filter((mens) => mens.matricula_id && matriculaIds.has(mens.matricula_id)));
      setTurmas(t);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [id]);

  const handleAddMatricula = async () => {
    if (!selectedTurma || !id) return;
    await apiFetch("/matriculas/", {
      method: "POST",
      body: JSON.stringify({ pessoa_id: Number(id), turma_id: Number(selectedTurma) }),
    });
    setSelectedTurma("");
    load();
  };

  const handleAddMensalidade = async (matriculaId: number) => {
    const hoje = new Date();
    const mes = hoje.toLocaleString("pt-BR", { month: "long" });
    await apiFetch("/mensalidades/", {
      method: "POST",
      body: JSON.stringify({
        matricula_id: matriculaId,
        mes_referencia: `${mes.charAt(0).toUpperCase() + mes.slice(1)}/${hoje.getFullYear()}`,
        data_vencimento: hoje.toISOString().split("T")[0],
        valor_previsto: 50,
        status: "Pendente",
      }),
    });
    load();
  };

  if (loading) return <div className="p-8 text-center text-slate-500">A carregar...</div>;
  if (!pessoa) return <div className="p-8 text-center text-red-600">Pessoa não encontrada</div>;

  const turmasDisponiveis = turmas.filter(
    (t) => !pessoa.matriculas.some((m) => m.turma_nome === t.nome && m.modalidade_nome === t.modalidade_nome)
  );

  return (
    <div className="page-container">
      <Link href="/pessoas" className="flex items-center gap-2 text-slate-600 hover:text-slate-900 mb-4 font-medium">
        <ArrowLeft size={18} /> Voltar
      </Link>

      <div className="card p-6 mb-6">
        <h1 className="text-2xl font-bold text-slate-900">{pessoa.nome}</h1>
        {pessoa.email && <p className="text-slate-500 mt-1">{pessoa.email}</p>}
      </div>

      <div className="card p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4 text-slate-900">Matrículas</h2>
        {pessoa.matriculas.length === 0 ? (
          <p className="text-slate-400">Sem matrículas activas</p>
        ) : (
          <div className="space-y-3">
            {pessoa.matriculas.map((m) => (
              <div key={m.id} className="flex justify-between items-center border border-slate-200 rounded-lg p-3 bg-slate-50">
                <div className="text-slate-900">
                  <span className="font-medium">{m.modalidade_nome}</span>
                  <span className="text-slate-500 ml-2">— {m.turma_nome}</span>
                  <span className={`ml-3 text-xs px-2 py-0.5 rounded-full ${
                    m.status === "Ativa" ? "bg-green-100 text-green-700" : "bg-slate-100 text-slate-600"
                  }`}>{m.status}</span>
                </div>
                <button
                  onClick={() => handleAddMensalidade(m.id)}
                  className="flex items-center gap-1 text-sm text-blue-600 hover:underline"
                >
                  <DollarSign size={14} /> Nova mensalidade
                </button>
              </div>
            ))}
          </div>
        )}

        {turmasDisponiveis.length > 0 && (
          <div className="mt-4 flex gap-2 flex-wrap items-center border-t pt-4">
            <Plus size={18} className="text-slate-400" />
            <select
              className="input flex-1 min-w-[200px]"
              value={selectedTurma}
              onChange={(e) => setSelectedTurma(e.target.value)}
            >
              <option value="">Adicionar matrícula em...</option>
              {turmasDisponiveis.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.modalidade_nome} — {t.nome}
                </option>
              ))}
            </select>
            <button
              onClick={handleAddMatricula}
              disabled={!selectedTurma}
              className="btn-primary disabled:opacity-50"
            >
              Matricular
            </button>
          </div>
        )}
      </div>

      <div className="card p-6">
        <h2 className="text-lg font-semibold mb-4 text-slate-900">Mensalidades</h2>
        <table className="w-full text-sm">
          <thead className="table-head">
            <tr>
              <th className="text-left py-2">Referência</th>
              <th className="text-left py-2">Vencimento</th>
              <th className="text-right py-2">Valor</th>
              <th className="text-right py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {mensalidades.length === 0 ? (
              <tr><td colSpan={4} className="py-4 text-center text-slate-400">Sem mensalidades</td></tr>
            ) : (
              mensalidades.map((mens) => (
                <tr key={mens.id} className="border-b border-slate-100">
                  <td className="table-cell">{mens.mes_referencia}</td>
                  <td className="table-cell">{mens.data_vencimento}</td>
                  <td className="table-cell text-right">R$ {mens.valor_previsto.toFixed(2)}</td>
                  <td className="table-cell text-right">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      mens.status === "Pago" || mens.status === "Quitado"
                        ? "bg-green-100 text-green-700"
                        : "bg-amber-100 text-amber-700"
                    }`}>{mens.status}</span>
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
