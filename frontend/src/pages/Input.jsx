import React, { useState, useEffect, useRef } from 'react';
import './Input.css';

const PROCESS_STEPS = [
    "Arquivo recebido",
    "Conversão",
    "OCR",
    "Identificação",
    "Classificação",
    "Extração",
    "Validação",
    "Associação à ação"
];

function Input() {
    const [isDragging, setIsDragging] = useState(false);
    const [file, setFile] = useState(null);
    const [currentStep, setCurrentStep] = useState(-1);
    const [error, setError] = useState(null); // Estado para controlar o erro
    const fileInputRef = useRef(null);

    // Simula o progresso visual
    useEffect(() => {
        if (file && currentStep < PROCESS_STEPS.length) {
            const timer = setTimeout(() => {
                setCurrentStep((prev) => prev + 1);
            }, 1500);
            return () => clearTimeout(timer);
        }
    }, [file, currentStep]);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            iniciarUpload(e.dataTransfer.files[0]);
        }
    };

    const handleFileSelect = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            iniciarUpload(e.target.files[0]);
        }
    };

    // --- NOVA FUNÇÃO DE VALIDAÇÃO ---
    const validarFormato = (arquivo) => {
        // Pega a extensão final do arquivo e deixa em minúsculo
        const extensao = arquivo.name.split('.').pop().toLowerCase();

        // Extensões permitidas com base na sua imagem (incluí xlsx que é o padrão do excel)
        const permitidos = ['pdf','docx', 'png', 'jpg', 'jpeg', 'xslx', 'xlsx','txt'];

        return permitidos.includes(extensao);
    };

    // --- FUNÇÃO DE UPLOAD ATUALIZADA COM FETCH ---
    const iniciarUpload = async (arquivoSelecionado) => {
        setError(null); // Limpa erros anteriores

        // 1. Faz a validação
        if (!validarFormato(arquivoSelecionado)) {
            setError("Formato inválido. Apenas PDF, DOCX, PNG, JPG e XLSX são permitidos.");
            // Limpa o input de arquivo para permitir selecionar o mesmo arquivo novamente
            if (fileInputRef.current) fileInputRef.current.value = '';
            return;
        }

        // 2. Prepara o visual (inicia a animação de loading)
        setFile(arquivoSelecionado);
        setCurrentStep(0);

        // 3. Prepara os dados para o Backend
        const formData = new FormData();
        formData.append("file", arquivoSelecionado); // Você pode mudar "file" para o nome do campo que sua API espera

        // 4. Envia o POST para a API
        try {
            const response = await fetch("/api/v1/documents/upload", {
                method: "POST",
                body: formData,
                // Não adicione 'Content-Type': 'multipart/form-data', o navegador faz isso automaticamente com o Boundary correto
            });

            if (!response.ok) {
                console.error("Erro ao enviar o documento para a API:", response.status);
                // Opcional: tratar o erro visualmente aqui depois
            } else {
                const data = await response.json();
                console.log("Upload com sucesso!", data);
            }
        } catch (err) {
            console.error("Erro na requisição de upload:", err);
        }
    };

    return (
        <div className="app-layout">
            {/* BARRA LATERAL (MENU) */}
            <aside className="sidebar">
                <div>
                    <div className="sidebar-header">
                        <div className="logo">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
                            EMERON
                        </div>
                    </div>

                    <ul className="sidebar-menu">
                        <li className="menu-item">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                            Documentos
                        </li>
                    </ul>
                </div>

                <div className="sidebar-footer">
                    <div className="user-profile">
                        <div className="avatar">M</div>
                        <div className="user-info">
                            <div className="name">Maria Silva</div>
                            <div className="role">Gestora Educacional</div>
                        </div>
                    </div>
                    <button className="btn-sair">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                        Sair
                    </button>
                </div>
            </aside>

            {/* ÁREA PRINCIPAL */}
            <main className="main-content">
                <header className="page-header">
                    <h1 className="page-title">Central de Documentos</h1>
                    <p className="page-subtitle">Envie seus documentos. O sistema organiza, identifica e associa automaticamente à ação correspondente.</p>
                </header>

                {/* Lógica de exibição */}
                {!file ? (
                    <div
                        className={`dropzone-container ${isDragging ? 'drag-active' : ''}`}
                        onDragOver={handleDragOver}
                        onDragLeave={handleDragLeave}
                        onDrop={handleDrop}
                    >
                        <svg className="upload-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                        <h3 className="dropzone-title">Arraste seus arquivos aqui</h3>
                        <span className="dropzone-ou">ou</span>

                        <button className="btn-selecionar" onClick={() => fileInputRef.current.click()}>
                            Selecionar arquivos
                        </button>
                        {/* O "accept" já barra a maioria pelo seletor de arquivos do sistema operacional */}
                        <input
                            type="file"
                            ref={fileInputRef}
                            style={{ display: 'none' }}
                            accept=".docx,.png,.jpg,.jpeg,.xlsx,.xslx"
                            onChange={handleFileSelect}
                        />

                        <span className="dropzone-hints">Word, Excel e Imagens - até 25MB</span>

                        {/* MENSAGEM DE ERRO NA TELA SE O FORMATO FOR INVÁLIDO */}
                        {error && (
                            <div className="error-message">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                                {error}
                            </div>
                        )}
                    </div>
                ) : (
                    /* CARD DE PROCESSAMENTO */
                    <div className="processing-card">
                        <div className="processing-header">
                            <svg className="file-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
                            <div className="file-details">
                                <span className="file-name">{file.name}</span>
                                <span className="file-status">
                  {currentStep >= PROCESS_STEPS.length ? "Concluído" : "Processando documento..."}
                </span>
                            </div>
                        </div>

                        <div className="steps-list">
                            {PROCESS_STEPS.map((step, index) => {
                                let status = 'pending';
                                if (index < currentStep) status = 'completed';
                                if (index === currentStep) status = 'active';

                                return (
                                    <div key={index} className={`step-item ${status}`}>
                                        <div className="icon-circle">
                                            {status === 'completed' && (
                                                <svg className="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                                            )}
                                            {status === 'active' && <div className="icon-spinner" />}
                                            {status === 'pending' && <div className="icon-empty" />}
                                        </div>
                                        <span>{step}</span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default Input;