# 💼 Assistente Virtual da Vale — Demo Local com Ollama

Este é um protótipo de **assistente virtual corporativo** desenvolvido para simular interações internas na empresa **Vale**, com foco em tarefas como:

- Solicitação de férias  
- Reembolso de viagens  
- Atualização de perfil do empregado  
- Consulta de benefícios  

---

## 🧠 Tecnologias Utilizadas

| Tecnologia     | Função Principal                                  |
|----------------|---------------------------------------------------|
| [`Ollama`](https://ollama.com/) | Execução local do modelo LLM (`gemma:2b`)           |
| `gradio`       | Interface web interativa em formato de chat       |
| `rapidfuzz`    | Fuzzy matching entre perguntas e base de intenções|
| `json`         | Armazenamento da base de dados e logs             |

---

## 🛠️ Requisitos

- Python 3.8+
- Ollama instalado
- Modelo `gemma:2b` baixado via Ollama
- Ambiente virtual Python (opcional, mas recomendado)

---

## 🚀 Como Executar

### 1. Instale o Ollama

Baixe o Ollama para seu sistema operacional em:  
👉 [https://ollama.com/download](https://ollama.com/download)

---

### 2. Baixe o modelo `gemma:2b`

Execute no terminal:

```bash
ollama pull gemma:2b
```

#### ⚠️ Observação:

> `gemma:2b` é um modelo de linguagem grande (LLM) com cerca de **2 bilhões de parâmetros**, que exige **pelo menos 3.1 GB de memória RAM disponível**.  
>  
> Antes de rodar o sistema, teste o modelo com:

```bash
ollama run gemma:2b
```

Se ele iniciar corretamente, pressione `Ctrl + D` para sair do prompt.

---

### 3. Instale as dependências do projeto

Com o ambiente virtual ativado (opcional), rode:

```bash
pip install -r requirements.txt
```

---

### 4. Execute o assistente

```bash
python main.py
```

Após a execução, o Gradio abrirá um link local. Acesse no navegador:  
👉 [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 📄 Licença

Este projeto é distribuído sob a licença MIT.  
Uso exclusivo para fins **educacionais e demonstrativos**.