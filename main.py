import gradio as gr
import subprocess
import os
import datetime
import json

# Carrega base de dados simulada (JSON)
with open("db_demo.json", "r") as f:
    base_dados = json.load(f)

SYSTEM_PROMPT = """Você é um assistente virtual corporativo da empresa Vale. 
Ajude os empregados a realizarem tarefas internas, consultarem informações, entenderem processos e automatizarem ações básicas. 
Seja formal, direto e sempre útil."""

def buscar_resposta_no_banco(mensagem):
    msg_lower = mensagem.lower()
    for chave, dados in base_dados.items():
        # Busca simples por palavra-chave dentro da chave e descrição
        if any(palavra in msg_lower for palavra in chave.split("_")) or any(palavra in msg_lower for palavra in dados.get("descricao", "").lower().split()):
            return dados
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

def chamar_ollama(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "gemma:2b"],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        resposta = result.stdout.decode().strip()
        if not resposta:
            # fallback caso stdout esteja vazio
            resposta = "Desculpe, não consegui gerar uma resposta."
        return resposta
    except subprocess.TimeoutExpired:
        return "O modelo demorou demais para responder."
    except Exception as e:
        return f"Erro ao chamar o modelo: {str(e)}"

def enriquecer_resposta_com_llm(mensagem_usuario, info_base):
    prompt = f"""
{SYSTEM_PROMPT}

O usuário perguntou: "{mensagem_usuario}"

Aqui estão as informações internas relevantes:
Descrição: {info_base['descricao']}
Passos:
"""
    for i, passo in enumerate(info_base["etapas"], 1):
        prompt += f"{i}. {passo}\n"
    prompt += f"Prazo: {info_base['prazo']}\n\n"
    prompt += "Com base nessas informações, formule uma resposta clara, formal e direta para o usuário."

    return chamar_ollama(prompt)

def chat_with_assistant(message, history):
    resposta_banco = buscar_resposta_no_banco(message)

    if resposta_banco:
        resposta = enriquecer_resposta_com_llm(message, resposta_banco)
        salvar_log(message, resposta, prompt="Resposta enriquecida com base no banco")
        return resposta

    # Caso não encontre no banco, gera direto com o LLM
    full_prompt = SYSTEM_PROMPT + "\n\n"
    for user_msg, assistant_msg in history:
        full_prompt += f"Usuário: {user_msg}\nAssistente: {assistant_msg}\n"
    full_prompt += f"Usuário: {message}\nAssistente:"

    resposta = chamar_ollama(full_prompt)
    salvar_log(message, resposta, prompt=full_prompt)
    return resposta

gr.ChatInterface(
    fn=chat_with_assistant,
    title="💼 Assistente Virtual - Vale",
    description="Converse com o assistente da Vale para apoio em processos e tarefas internas.",
    theme=gr.themes.Soft(primary_hue="blue", font="monospace")
).launch()

