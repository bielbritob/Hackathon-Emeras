import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [pdfFile, setPdfFile] = useState(null)
  const [canSendFile, setCanSendFile] = useState(true)
  const [responseData, setResponseData] = useState(null)
  return (
      <>
        <div className=" text-white flex w-full h-screen bg-slate-900 gap-4 p-4">

          {/* Lado esquerdo*/}
          <div className="flex flex-col flex-1">
            <header className="px-6 py-4 border-b ">
              <h2 className="text-lg font-semibold text-white">Upload do Documento</h2>
            </header>
            <div className="flex flex-col items-center justify-center flex-1 px-6 pt-6 pb-0">
              <label className="flex flex-col items-center justify-center flex-1 w-full border-2 border-dashed border-gray-500 rounded-xl cursor-pointer hover:bg-gray-800 transition-colors">

                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  {pdfFile ? (
                      // Se já tiver um PDF selecionado
                      <>
                        <svg className="w-10 h-10 mb-3 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        <p className="mb-2 text-sm text-green-400 font-semibold">Arquivo carregado com sucesso!</p>
                        <p className="text-xs text-gray-400">{pdfFile.name}</p>
                      </>
                  ) : (
                      // Se não tiver nenhum arquivo
                      <>
                        <svg className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                        <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Clique para enviar</span> ou arraste o PDF</p>
                        <p className="text-xs text-gray-400">Apenas arquivos PDF</p>
                      </>
                  )}
                </div>

                {/* O input que havia sumido voltou pra cá com a função onChange certa */}
                <input
                    type="file"
                    accept=".pdf"
                    className="hidden"
                    disabled={!canSendFile}
                    onChange={async (e) => {
                      if (e.target.files && e.target.files.length > 0) {
                        setPdfFile(e.target.files[0]);
                        setCanSendFile(false)

                        const formData = new FormData();

                        formData.append('file', e.target.files[0]);

                        const response = await fetch('http://localhost:8000/documentos', {
                          method: 'POST',
                          body: formData,
                        });

                        if (!response.ok) {
                          const errorData = await response.json();
                          throw new Error(errorData.detail || 'Erro ao processar o PDF.');
                        }

                        // 4. Recebe o JSON estruturado direto do response.parsed do Gemini
                        const data = await response.json();
                        setResponseData(data);


                      }
                    }}
                />
              </label>
            </div>



          </div>

          {/* Divisor//*/}
          <div className="relative flex flex-col h-full w-px items-center justify-center">

            {/* Linha vertical inteira de fundo */}
            <div className="absolute inset-0 w-full bg-white rounded-md shadow-lg overflow-hidden blur-sm" />
            <div className="absolute inset-0 w-full bg-white rounded-md shadow-lg overflow-hidden " />

            {/* Container dos tracinhos (ele fica por cima da linha e limpa o fundo com 'bg-slate-900') */}
            <div className="flex">

              {/* Tracinho 1 */}
              <div className="w-0.5 h-7 bg-white rotate-55 transform mb-2 blur-xs" />
              <div className="w-0.5 h-7 bg-white rotate-55 transform mb-2 " />

              {/* Tracinho 2 */}
              <div className="w-0.5 h-7 bg-white rotate-55 transform mt-2 blur-xs" />
              <div className="w-0.5 h-7 bg-white rotate-55 transform mt-2 " />

            </div>
          </div>

          {/* Lado direito */}
          <div className="flex flex-col flex-1 bg-slate-900 border border-gray-200 rounded-2xl shadow-sm overflow-hidden">

            <header className="px-6 py-4 border-b ">
              <h2 className="text-lg font-semibold text-white">Resultado da Análise</h2>
            </header>

            <div className="flex flex-col flex-1 p-6 justify-between">
              <div className="text-sm text-gray-400">
                {responseData === null ? (
                    <p>O resultado do processamento do seu PDF vai aparecer aqui...</p>
                ) : (
                    // Agora renderiza os dados formatados do seu Pydantic!
                    <div className="space-y-3 text-sm text-gray-300">
                      <p><strong className="text-white">Resumo do Caso:</strong> {responseData.resumo_caso}</p>
                      <p><strong className="text-white">Valor da Causa:</strong> R$ {responseData.valor_causa}</p>
                      <p><strong className="text-white">Urgência:</strong> {responseData.urgencia}</p>
                      <p><strong className="text-white">Jurisprudência Sugerida:</strong> {responseData.jurisprudencia_sugerida}</p>
                      <div>
                        <strong className="text-white">Documentos Faltantes:</strong>
                        <ul className="list-disc pl-5 mt-1 text-gray-400">
                          {responseData.documentos_faltantes?.map((doc, index) => (
                              <li key={index}>{doc}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                )}
              </div>

              {/* Botão/Link de Ação no final */}
              <a
                  href="#download"
                  className="block w-full py-3 text-center font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl transition-colors shadow-sm"
              >
                Baixar Relatório
              </a>
            </div>

          </div>

        </div>
      </>
  )
}

export default App
