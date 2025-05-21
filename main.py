import gradio as gr
import os
import datetime
import json
from rapidfuzz import fuzz
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Carrega base de dados simulada (JSON)

SYSTEM_PROMPT = """Você é um assistente virtual corporativo da empresa Vale.
Ajude os funcionários a entender processos, consultar políticas internas e executar tarefas simples.
Seja sempre claro, objetivo e educado.
Nunca invente respostas. Se não souber, diga que não sabe.
Nunca forneça dados pessoais, confidenciais ou especulativos."""


#fuzzy matching no banco de dados demo
def buscar_resposta_no_banco(mensagem):
    msg_lower = mensagem.lower()

    with open("db_demo.json", "r", encoding="utf-8") as f:
        intents = json.load(f)  # Aqui é uma lista, não um dicionário

    melhor_match = None
    maior_score = 0
    LIMIAR = 75  # Sensibilidade da correspondência

    for intent in intents:  # Correto para listas
        for palavra_chave in intent.get("palavras_chave", []):
            score = fuzz.partial_ratio(palavra_chave.lower(), msg_lower)
            if score > maior_score:
                maior_score = score
                melhor_match = intent

    if melhor_match and maior_score >= LIMIAR:
        return melhor_match  # Retorna o dicionário inteiro

    return None


def salvar_log(mensagem, resposta, prompt=None):
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "mensagem": mensagem,
        "resposta": resposta,
    }
    if prompt:
        log["prompt"] = prompt

    log_file = "log.json"
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump([log], f, ensure_ascii=False, indent=2)
    else:
        with open(log_file, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(log)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()

def gerar_resposta_transformers(prompt):
    try:
        resposta = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)[0]["generated_text"]
        return resposta.strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

def enriquecer_resposta_com_llm(mensagem_usuario, info_base):
    if not isinstance(info_base, dict):
        return "Desculpe, não encontrei informações estruturadas para responder sua pergunta."

    prompt = f"""{SYSTEM_PROMPT}

    O usuário: "{mensagem_usuario}"

    Aqui estão as informações internas relevantes:

    Descrição: {info_base.get('descricao', 'Não disponível')}

    Passos: 
    """
    for i, passo in enumerate(info_base.get("etapas", []), 1):
        prompt += f"{i}. {passo}\n"

    prompt += f"\nPrazo: {info_base.get('prazo', 'Não informado')}\n\n"
    prompt += "Com base nessas informações, formule uma resposta clara, formal e direta para o usuário."

    return gerar_resposta_transformers(prompt)

def responder_com_llm_direto(mensagem_usuario):
    prompt = f"""
    {SYSTEM_PROMPT}

    O usuário perguntou: "{mensagem_usuario}"

    Não há informações estruturadas no banco de dados sobre isso.
    Por favor, responda de forma clara, educada e útil ao usuário.
    """
    return gerar_resposta_transformers(prompt)

def chat_with_assistant(message, history):
    resposta_base = buscar_resposta_no_banco(message)

    if resposta_base:
        resposta = enriquecer_resposta_com_llm(message, resposta_base)
        salvar_log(message, resposta, prompt="Resposta gerada com base no banco de dados")
    else:
        # Montar prompt com histórico para o modelo direto
        full_prompt = SYSTEM_PROMPT + "\n\n"
        for user_msg, assistant_msg in history[-3:]:  # usar só os últimos 3 para não poluir
            full_prompt += f"Usuário: {user_msg}\nAssistente: {assistant_msg}\n"
        full_prompt += f"Usuário: {message}\nAssistente:"

        resposta = gerar_resposta_transformers(full_prompt)
        salvar_log(message, resposta, prompt=full_prompt)

    return resposta

gr.ChatInterface(
    fn=chat_with_assistant,
    title="💼 Assistente Virtual - Vale",
    description="Converse com o assistente da Vale para apoio em processos e tarefas internas.",
    theme=gr.themes.Soft(primary_hue="blue", font="monospace")
).launch()

