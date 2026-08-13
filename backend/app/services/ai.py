import os
import json
from dotenv import load_dotenv
from google import genai
from fastapi import HTTPException

# Carrega as variáveis do .env à força para garantir que a API Key é lida
load_dotenv()

class AIService:
    """
    Comentário: Serviço responsável pela integração com a nova SDK do Google Gemini (google-genai).
    Isola a lógica de IA para proteger o restante do sistema (Clean Architecture).
    """

    def __init__(self):
        self.__api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.__api_key:
            raise ValueError("ERRO CRÍTICO: GEMINI_API_KEY não encontrada no arquivo .env")

        # Comentário: Na nova SDK, usamos 'Client' em vez de instanciar o modelo diretamente
        self.__client = genai.Client(api_key=self.__api_key)
        self.__model_id = 'gemma-4-31b-it'

    async def extract_and_classify(self, raw_text: str) -> dict:
        """
        Comentário: Analisa o texto bruto, classifica a categoria do documento 
        e extrai os campos estruturados em JSON.
        """
        prompt = f"""
        Você é a Inteligência Artificial central do sistema 'EMERON Gestão Inteligente'.
        Sua tarefa é ler o texto bruto de um documento enviado, classificá-lo 
        exatamente em uma das categorias do sistema e extrair as informações em formato JSON.
        
        REGRAS CRÍTICAS:
        1. Devolva APENAS um JSON válido. Não use formatação markdown (como ```json).
        2. Não adicione nenhum texto antes ou depois das chaves.
        3. Nem todos os documentos terão todos os campos. Se a informação não existir no texto (por exemplo, procurar 'vagas' em uma lista de presença), retorne null, mas verifique.
        
        CATEGORIAS PERMITIDAS (Use EXATAMENTE estas strings):
        - "Plano de curso"
        - "Programação"
        - "Lista de participantes"
        - "Lista de presença"
        - "Avaliação"
        - "Relatório final"
        - "Outros"
        
        TEXTO BRUTO DO DOCUMENTO:
        {raw_text}
        
        ESTRUTURA JSON EXIGIDA:
        {{
            "document_category": "string (escolha uma das categorias permitidas)",
            "requesting_unit": "string",
            "training_need": "string",
            "expected_profile": "string",
            "modality": "string",
            "vacancies": integer ou null,
            "workload_hours": integer ou null,
            "syllabus": "string",
            "target_audience": "string",
            "hiring_type": "string",
            "suggested_provider": "string",
            "justification": "string"
        }}
        """
        
        try:
            # Comentário: Esta é a forma de pedir a geração de texto a AI
            response = self.__client.models.generate_content(
                model=self.__model_id,
                contents=prompt,
            )
            
            # Comentário: Higienização agressiva para garantir que o Python leia o JSON
            cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned_response)
            
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="A Inteligência Artificial não retornou um JSON válido.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")