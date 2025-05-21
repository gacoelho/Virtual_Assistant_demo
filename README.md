# Virtual Assistant Demo

# 💼 Assistente Virtual da Vale — Demo Local com Ollama

Este é um protótipo de **assistente virtual corporativo** desenvolvido para simular interações internas na empresa **Vale**, com foco em tarefas como:

- Solicitação de férias  
- Reembolso de viagens  
- Atualização de perfil do empregado  
- Consulta de benefícios  

---

## 🧠 Tecnologias Utilizadas

| Tecnologia  | Função Principal                                  |
|-------------|---------------------------------------------------|
| [`Ollama`]  |Execução local do modelo LLM                       |
| `gradio`    | Interface web interativa em formato de chat       |
| `rapidfuzz` | Fuzzy matching entre perguntas e base de intenções|
| `json`      | Armazenamento da base de dados e logs             |

---

## 🛠️ Requisitos

- Python 3.8+
- `ollama` instalado e funcional (com o modelo `gemma:2b` puxado)
- Ambiente virtual Python (recomendado)

---

## 🚀 Como Executar

### 1. Instale o [Ollama](https://ollama.com/download)

Siga as instruções do site oficial para seu sistema (Linux, macOS, Windows).

### 2. Baixe o modelo `gemma:2b`

```bash
ollama pull gemma:2b

obs: "gemm:2b é um modelo de linguagme grande '(LLM)' de 2 Bilhões de parâmetros que necessita de pelo menos 3.1 GB de mémoria RAM para funcionar. Antes de rodar o programa use o comando no termina: ollama run gemma:2b e verifica sé há algum problema com a o requerimento de RAM. Depois de crtl + d para sair do prompt do gemma."

### 3, Baixa o requirement.txt 

pip install -r requirement.txt

### 4, Rode o progrma 

python main.py

'entre no URL gerado pelo Gradio:' http://127.0.0.1:7860


