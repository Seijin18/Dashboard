'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { 
  ArrowLeft, 
  User, 
  FileText, 
  Calendar, 
  CheckCircle2, 
  Clock, 
  AlertCircle,
  DollarSign,
  ChevronRight
} from 'lucide-react';
import Link from 'next/link';

interface Mensalidade {
  id: number;
  contrato_num: string | null;
  mes_referencia: string;
  data_vencimento: string;
  data_pagamento: string | null;
  valor_previsto: number;
  valor_pago: number | null;
  status: string;
}

interface Aluno {
  id: number;
  nome_cliente: string;
  dependente: string | null;
  grupo_inscricao: string;
  status_matricula: string;
  mensalidades: Mensalidade[];
}

export default function AlunoDetalhes() {
  const { id } = useParams();
  const router = useRouter();
  const [aluno, setAluno] = useState<Aluno | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAluno() {
      try {
        const res = await fetch(`http://localhost:8000/alunos/${id}`);
        if (!res.ok) throw new Error('Falha ao carregar dados do aluno');
        const data = await res.json();
        setAluno(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro desconhecido');
      } finally {
        setLoading(false);
      }
    }

    if (id) fetchAluno();
  }, [id]);

  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>
  );

  if (error || !aluno) return (
    <div className="p-8 text-center">
      <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
      <h2 className="text-2xl font-bold text-gray-800">Erro ao carregar aluno</h2>
      <p className="text-gray-600 mb-6">{error}</p>
      <button 
        onClick={() => router.back()}
        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition"
      >
        Voltar para Lista
      </button>
    </div>
  );

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pago': return 'bg-green-100 text-green-700 border-green-200';
      case 'atrasado': return 'bg-red-100 text-red-700 border-red-200';
      case 'pendente': return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header Navigation */}
        <div className="mb-8 flex items-center justify-between">
          <Link 
            href="/" 
            className="flex items-center text-gray-600 hover:text-blue-600 transition group"
          >
            <ArrowLeft className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" />
            Voltar para o Dashboard
          </Link>
          <div className="flex space-x-2">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${
              aluno.status_matricula === 'Ativa' ? 'bg-green-100 text-green-700 border-green-200' : 'bg-red-100 text-red-700 border-red-200'
            }`}>
              {aluno.status_matricula}
            </span>
          </div>
        </div>

        {/* Profile Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 md:p-8 mb-8">
          <div className="flex flex-col md:flex-row md:items-center">
            <div className="h-20 w-20 rounded-full bg-blue-600 flex items-center justify-center text-white mb-4 md:mb-0 md:mr-6">
              <User className="w-10 h-10" />
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-1">{aluno.dependente || aluno.nome_cliente}</h1>
              {aluno.dependente && (
                <p className="text-gray-500 mb-2 flex items-center">
                  <span className="font-semibold text-gray-700 mr-2">Titular:</span> {aluno.nome_cliente}
                </p>
              )}
              <div className="flex flex-wrap gap-4 mt-2">
                <span className="flex items-center text-sm text-gray-600">
                  <FileText className="w-4 h-4 mr-1 text-gray-400" />
                  ID: {aluno.id}
                </span>
                <span className="flex items-center text-sm text-gray-600">
                  <Calendar className="w-4 h-4 mr-1 text-gray-400" />
                  Grupo: {aluno.grupo_inscricao}
                </span>
              </div>
            </div>
            <div className="mt-6 md:mt-0 flex flex-col items-end">
              <p className="text-sm font-medium text-gray-500 mb-1">Total de Mensalidades</p>
              <p className="text-2xl font-bold text-gray-900">{aluno.mensalidades.length}</p>
            </div>
          </div>
        </div>

        {/* History Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-xl font-bold text-gray-900">Histórico de Mensalidades</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-gray-50 text-gray-500 text-xs font-semibold uppercase tracking-wider">
                  <th className="px-6 py-4">Ref/Vencimento</th>
                  <th className="px-6 py-4">Contrato</th>
                  <th className="px-6 py-4">Valor Previsto</th>
                  <th className="px-6 py-4">Valor Pago</th>
                  <th className="px-6 py-4">Data Pagto</th>
                  <th className="px-6 py-4">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {aluno.mensalidades
                  .sort((a, b) => new Date(b.data_vencimento).getTime() - new Date(a.data_vencimento).getTime())
                  .map((m) => (
                  <tr key={m.id} className="hover:bg-gray-50 transition">
                    <td className="px-6 py-4">
                      <div className="text-sm font-semibold text-gray-900">{m.mes_referencia}</div>
                      <div className="text-xs text-gray-500">{new Date(m.data_vencimento).toLocaleDateString('pt-BR')}</div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {m.contrato_num || <span className="text-gray-300 italic">S/N</span>}
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      R$ {m.valor_previsto.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {m.valor_pago ? `R$ ${m.valor_pago.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}` : '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {m.data_pagamento ? new Date(m.data_pagamento).toLocaleDateString('pt-BR') : '-'}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(m.status)}`}>
                        {m.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {aluno.mensalidades.length === 0 && (
            <div className="p-12 text-center text-gray-500 italic">
              Nenhuma mensalidade registrada para este aluno.
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
