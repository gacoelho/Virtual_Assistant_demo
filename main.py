import gradio as gr
import subprocess
import json

# Carregando base de dados simulada (JSON)
with open("db_demo.json", "r") as f:
    base_dados = json.load(f)

SYSTEM_PROMPT = """Você é um assistente virtual corporativo da empresa Vale. 
Ajude os empregados a realizarem tarefas internas, consultarem informações, entenderem processos e automatizarem ações básicas. 
Seja formal, direto e sempre útil."""

def buscar_resposta_no_banco(mensagem):
    msg_lower = mensagem.lower()
    # Busca simples por palavras-chave para simular RAG
    if "reembolso" in msg_lower and "viagem" in msg_lower:
        return base_dados.get("reembolso_viagem")
    elif "férias" in msg_lower or "ferias" in msg_lower:
        return base_dados.get("solicitacao_ferias")
    else:
        return None

def chat_with_assistant(message, history):
    # Tenta buscar resposta na base de dados
    resposta_banco = buscar_resposta_no_banco(message)
    
    if resposta_banco:
        # Se achou no banco, formata uma resposta estruturada
        resposta_formatada = f"{resposta_banco['descricao']}\n\nPassos:\n"
        for i, passo in enumerate(resposta_banco["etapas"], 1):
            resposta_formatada += f"{i}. {passo}\n"
        resposta_formatada += f"\nPrazo: {resposta_banco['prazo']}"
        return resposta_formatada

    # Se não achou no banco, manda para o modelo Ollama
    full_prompt = SYSTEM_PROMPT + "\n\n"
    for user_msg, assistant_msg in history:
        full_prompt += f"Usuário: {user_msg}\nAssistente: {assistant_msg}\n"
    full_prompt += f"Usuário: {message}\nAssistente:"

    try:
        result = subprocess.run(
            ["ollama", "run", "tinyllama"],
            input=full_prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        response = result.stdout.decode().strip()
        return response
    except subprocess.TimeoutExpired:
        return "O modelo demorou demais para responder."
    except Exception as e:
        return f"Erro: {str(e)}"

gr.ChatInterface(
    fn=chat_with_assistant,
    title="💼 Assistente Virtual - Vale (com Base de Dados)",
    description="Converse com o assistente da Vale para apoio em processos e tarefas internas.",
    theme="soft",
).launch()


