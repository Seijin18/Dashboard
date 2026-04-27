"use client";

import { useState, useEffect } from "react";
import { Upload, Users, FileText, DollarSign, RefreshCw, AlertCircle } from "lucide-react";

interface Aluno {
  id: number;
  nome: string;
  contrato: string;
  modalidade: string;
  plano: string;
  status: string;
  valor: number;
  pre_inscricao?: boolean;
}

export default function Dashboard() {
  const [alunos, setAlunos] = useState<Aluno[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Estados do Modal de Pré-visualização
  const [previewData, setPreviewData] = useState<any>(null);
  const [isConfirming, setIsConfirming] = useState(false);

  const fetchAlunos = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/alunos/");
      if (!res.ok) throw new Error("Erro ao buscar dados dos alunos.");
      const data = await res.json();
      setAlunos(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Erro de conexão com a API.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlunos();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setIsUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload-pdf-preview/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Falha ao analisar o arquivo PDF.");
      
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      setPreviewData(data); // Abre o modar mostrando novos e atualizados

    } catch (err: any) {
      console.error(err);
      setError(err.message || "Erro ao processar o upload.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleConfirmUpload = async () => {
    if (!previewData) return;
    setIsConfirming(true);

    try {
      // Misturar os novos e atualizados para enviar ao backend para salvar
      const pl = [...previewData.novos, ...previewData.atualizados];
      const res = await fetch("http://localhost:8000/upload-pdf-confirm/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(pl),
      });

      if (!res.ok) throw new Error("Falha ao confirmar o salvamento do PDF.");
      
      const data = await res.json();
      if (data.error) throw new Error(data.error);

      alert(`Sucesso! ${data.status}`);
      setFile(null);
      setPreviewData(null);
      fetchAlunos(); // Atualiza a tabela com as modificações finais

    } catch (err: any) {
      console.error(err);
      setError(err.message || "Erro ao salvar definitivamente os registros.");
    } finally {
      setIsConfirming(false);
    }
  };

  // Métricas do Dashboard
  const activeContracts = alunos.filter(a => (a.status || "").toLowerCase() !== "cancelado");
  const totalRevenue = activeContracts.reduce((acc, aluno) => acc + (aluno.valor || 0), 0);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <header className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard KannonDo</h1>
            <p className="text-gray-500 mt-1">Gerenciamento financeiro através dos relatórios Galileu.</p>
          </div>
          <button 
            onClick={fetchAlunos} 
            className="flex items-center gap-2 px-4 py-2 bg-white border shadow-sm rounded-md hover:bg-gray-50 transition"
          >
            <RefreshCw size={18} className={isLoading ? "animate-spin" : ""} />
            Atualizar Dados
          </button>
        </header>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-md flex items-center gap-3">
            <AlertCircle className="text-red-500" />
            <p className="text-red-700 font-medium">{error}</p>
          </div>
        )}

        {/* MÉTRICAS (CARDS) */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className="p-4 bg-blue-50 text-blue-600 rounded-lg">
              <Users size={28} />
            </div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Total de Alunos</p>
              <h3 className="text-2xl font-bold text-gray-900">{alunos.length}</h3>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className="p-4 bg-green-50 text-green-600 rounded-lg">
              <FileText size={28} />
            </div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Contratos Ativos</p>
              <h3 className="text-2xl font-bold text-gray-900">{activeContracts.length}</h3>
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
            <div className="p-4 bg-emerald-50 text-emerald-600 rounded-lg">
              <DollarSign size={28} />
            </div>
            <div>
              <p className="text-sm text-gray-500 font-medium">Receita Prevista (Ativos)</p>
              <h3 className="text-2xl font-bold text-gray-900">
                {totalRevenue.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}
              </h3>
            </div>
          </div>
        </section>

        {/* UPLOAD AREA */}
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
            <Upload size={20} className="text-blue-500" />
            Importar Relatório Galileu
          </h2>
          <form onSubmit={handleUpload} className="flex items-center gap-4">
            <input 
              type="file" 
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 transition-colors"
            />
            <button 
              type="submit" 
              disabled={!file || isUploading}
              className="px-6 py-2.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {isUploading ? "Processando..." : "Importar PDF"}
            </button>
          </form>
        </section>

        {/* TABLE */}
        <section className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
            <h2 className="font-bold text-gray-800">Listagem de Alunos Extraídos</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-gray-600">
              <thead className="bg-gray-50/50 text-gray-500 border-b">
                <tr>
                  <th className="px-6 py-3 font-medium">Nome do Aluno</th>
                  <th className="px-6 py-3 font-medium">Contrato</th>
                  <th className="px-6 py-3 font-medium">Modalidade / Plano</th>
                  <th className="px-6 py-3 font-medium">Status</th>
                  <th className="px-6 py-3 font-medium text-right">Valor R$</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {isLoading ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-gray-400">Carregando dados...</td>
                  </tr>
                ) : alunos.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-gray-400">Nenhum dado encontrado. Faça a importação de um PDF.</td>
                  </tr>
                ) : (
                  alunos.map((aluno) => (
                    <tr key={aluno.id} className="hover:bg-gray-50/50 transition">
                      <td className="px-6 py-3 font-medium text-gray-800">
                        {aluno.nome}
                        {aluno.pre_inscricao && (
                          <span className="ml-2 inline-flex items-center px-1.5 py-0.5 rounded-full text-[10px] font-medium bg-purple-100 text-purple-800" title="Passou por processo de Pré-inscrição">
                            Pré-inscrição
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-3">{aluno.contrato}</td>
                      <td className="px-6 py-3">
                        <span className="block">{aluno.modalidade || "Não inf."}</span>
                        <span className="text-xs text-gray-400">{aluno.plano}</span>
                      </td>
                      <td className="px-6 py-3">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                          (aluno.status || "").toLowerCase().includes("ativo") 
                            ? 'bg-green-100 text-green-800' 
                            : (aluno.status || "").toLowerCase().includes("cancelado") 
                            ? 'bg-red-100 text-red-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {aluno.status || "N/A"}
                        </span>
                      </td>
                      <td className="px-6 py-3 text-right font-medium">
                        {(aluno.valor || 0).toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

      </div>

      {/* Modal de Pré-visualização do PDF */}
      {previewData && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
            <div className="px-6 py-4 border-b flex justify-between items-center bg-gray-50">
              <h3 className="text-xl font-bold text-gray-900">Revisão de Importação</h3>
              <button onClick={() => setPreviewData(null)} className="text-gray-400 hover:text-gray-600">✕ Cancelar</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1 space-y-6">
              <div className="flex gap-4 items-center p-4 bg-blue-50 text-blue-800 rounded-lg">
                <AlertCircle size={24} />
                <p>
                  O arquivo contém <strong>{previewData.total_encontrados} registros</strong>.
                  <br />- <strong>{previewData.novos.length}</strong> são novos.
                  <br />- <strong>{previewData.atualizados.length}</strong> possuem atualizações (mensalidades pagas ou mudanças de status).
                  <br />- <strong>{previewData.inalterados.length}</strong> itens já existem no banco e não sofreram mutações neste arquivo.
                </p>
              </div>

              {previewData.atualizados.length > 0 && (
                <div>
                  <h4 className="font-semibold text-orange-600 border-b pb-2 mb-3">Registros Modificados (Avisos de Atualização)</h4>
                  <div className="space-y-3">
                    {previewData.atualizados.map((at: any, i: number) => (
                      <div key={i} className="p-3 bg-orange-50 border border-orange-100 rounded-md text-sm text-gray-700 flex justify-between items-center">
                        <div>
                          <strong>{at.aluno.dependente || at.aluno.nome_cliente}</strong> - Ref: {at.mensalidade.mes_referencia}
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="line-through opacity-70">
                            {at._old_status}
                          </span>
                          <span>→</span>
                          <span className="font-medium text-orange-700 bg-orange-200 px-2 py-0.5 rounded">
                            {at.mensalidade.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {previewData.novos.length > 0 && (
                <div>
                  <h4 className="font-semibold text-green-600 border-b pb-2 mb-3">Novos Registros a Inserir</h4>
                  <ul className="list-disc pl-5 text-sm text-gray-600 grid grid-cols-1 md:grid-cols-2 gap-2">
                    {previewData.novos.map((nv: any, i: number) => (
                      <li key={i}>{nv.aluno.dependente || nv.aluno.nome_cliente} <span className="text-gray-400">({nv.mensalidade.mes_referencia})</span></li>
                    ))}
                  </ul>
                </div>
              )}

              {previewData.novos.length === 0 && previewData.atualizados.length === 0 && (
                <div className="text-center text-gray-500 py-8">
                  Nenhuma alteração a ser salva. Todos os dados deste PDF já estão atualizados no banco de dados.
                </div>
              )}
            </div>

            <div className="p-4 border-t bg-gray-50 flex justify-end gap-3">
              <button 
                onClick={() => setPreviewData(null)}
                className="px-5 py-2 text-gray-600 hover:text-gray-800 font-medium"
              >
                Descartar
              </button>
              <button 
                onClick={handleConfirmUpload}
                disabled={isConfirming || (previewData.novos.length === 0 && previewData.atualizados.length === 0)}
                className="px-6 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {isConfirming ? "Salvando..." : "Confirmar Atualizações"}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

