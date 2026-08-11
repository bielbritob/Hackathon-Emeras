# Hackathon-Emeras



## Getting started
##### planned logic:

```mermaid
flowchart TD
    %% Decisão inicial
    INPUT_DECISION{"tipo do input"}
    INPUT_DECISION -->|else| INVALID["Formato inválido"]
    
    INPUT_DECISION -->|if| DOCX["docx"]
    INPUT_DECISION -->|if| PDF["pdf"]
    INPUT_DECISION -->|if| IMG["png, jpg"]
    INPUT_DECISION -->|if| XLSX["xlsx"]

    %% Extração de texto
    DOCX --> TEXT_CHECK{"contem texto?"}
    PDF --> TEXT_CHECK

    TEXT_CHECK -->|sim| DOCX2TXT["pip docx2txt"]
    TEXT_CHECK -->|sim| PYPDF["pymypDF"]
    TEXT_CHECK -->|não| OCR["ocr"]
    IMG --> OCR
    XLSX --> PANDAS["pip pandas"]

    DOCX2TXT --> TEXTO["texto"]
    PYPDF --> TEXTO
    OCR --> TEXTO
    PANDAS --> TEXTO

    %% Processamento e DB
    TEXTO --> REGEX["Regex"]
    REGEX --> CLASSIFICACAO["Classificação"]
    CLASSIFICACAO --> DB["Cruzamento e relacionamento com o DB"]
    
    LOGICA_DB["Lógica: criar ou relacionar a uma ação educacionais já existente"]
    DB -.- LOGICA_DB

    %% Validação e Saída
    DB -->|resposta| EXISTE{"Existe?"}
    
    EXISTE -->|if| NOVA_ACAO["cria uma nova ação educacional"]
    EXISTE -->|Else| ATUALIZA["atualiza a documentação"]
    
    VERIFICA_INCONSISTENCIAS["Verifica inconsistencias e tratamento dos outros inputs"]
    ATUALIZA -.- VERIFICA_INCONSISTENCIAS

    IA["IA"] --> DOSSIE["Gera o dossiê"]
    ATUALIZA --> DOSSIE

```

To make it easy for you to get started with GitLab, here's a list of recommended next steps.


## Test and Deploy
Use the built-in docker-compose.yml to deploy all in 2times

```bash
git clone https://gitlab.com/hackathon-group6750332/hackathon-emeras.git
docker compose --build
```
That's it!

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.


## License
For open source projects, say how it is licensed.