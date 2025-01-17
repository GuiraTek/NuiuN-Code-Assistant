# 🤖 NuiuN Code Assistant

Um assistente de código inteligente construído com Python e Streamlit, utilizando a API Groq para sugestões de código e correções.

## 📋 Índice

- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API](#-api)
- [Contribuição](#-contribuição)
- [Suporte](#-suporte)
- [Licença](#-licença)

## 🔧 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git
- Conta na Groq (para API key)

## 📥 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/nuin-code-assistant.git
cd nuin-code-assistant
```

2. **Crie e ative um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. **Configure as variáveis de ambiente**
   - Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edite o arquivo `.env` com suas configurações:
   ```env
   GROQ_API_KEY=sua_api_key_aqui
   GROQ_MODEL=mixtral-8x7b-32768
   MAX_TOKENS=32000
   TEMPERATURE=0.7
   ```

2. **Obtenha uma API Key da Groq**
   - Acesse [Groq](https://www.groq.com)
   - Crie uma conta ou faça login
   - Vá para configurações de API
   - Gere uma nova API key
   - Copie a key para o arquivo `.env`

## 🚀 Uso

1. **Inicie o aplicativo**
```bash
streamlit run app.py
```

2. **Acesse a interface**
   - Abra seu navegador em `http://localhost:8501`
   - A interface será carregada automaticamente

3. **Utilizando o assistente**
   - **Sugerir Código**: Digite sua pergunta ou requisito e clique em "Sugerir Código"
   - **Corrigir Erros**: Cole seu código e clique em "Corrigir Erros"
   - As respostas serão exibidas na área principal

## 📁 Estrutura do Projeto

```
nuiun-code-assistant/
├── app.py              # Aplicativo principal
├── requirements.txt    # Dependências
├── .env               # Configurações (não versionado)
├── .env.example       # Exemplo de configurações
├── README.md          # Esta documentação
└── venv/              # Ambiente virtual (não versionado)
```

### Componentes Principais

- `app.py`: Contém toda a lógica do aplicativo
  - Interface do usuário (Streamlit)
  - Integração com API Groq
  - Processamento de respostas
  - Estilização e layout

## 🔌 API

### Groq API

O aplicativo utiliza a API Groq para:
- Geração de código
- Análise de código
- Correção de erros
- Sugestões de melhorias

### Endpoints Principais

```python
def suggest_code(user_input):
    """
    Gera sugestões de código baseadas no input do usuário.
    
    Parâmetros:
    - user_input (str): Pergunta ou requisito do usuário
    
    Retorna:
    - str: Resposta formatada com sugestões
    """

def correct_errors(user_input):
    """
    Analisa e corrige erros no código fornecido.
    
    Parâmetros:
    - user_input (str): Código para análise
    
    Retorna:
    - str: Resposta formatada com correções
    """
```

## 🔄 Fluxo de Trabalho

1. **Entrada do Usuário**
   - Digite pergunta ou cole código
   - Selecione a ação desejada

2. **Processamento**
   - O input é enviado para a API Groq
   - O modelo processa a requisição
   - A resposta é formatada

3. **Exibição**
   - Resposta exibida na interface
   - Formatação markdown para código
   - Destaque de sintaxe

## 📊 Métricas

O aplicativo monitora:
- Tokens utilizados
- Requisições feitas
- Tempo de resposta
- Taxa de sucesso

## 🤝 Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Siga o estilo de código existente
- Atualize a documentação conforme necessário
- Adicione testes para novas funcionalidades
- Mantenha o código limpo e bem documentado

## 🐛 Reportando Bugs

Use o sistema de Issues do GitHub:
1. Verifique se o bug já foi reportado
2. Abra uma nova issue
3. Descreva claramente o problema
4. Inclua passos para reprodução
5. Adicione logs e screenshots relevantes

## 📝 Licença

Este projeto está sob a licença Apache 2.0. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

- Abra uma issue para bugs
- Use as discussions para dúvidas
- Email: suporte@guiratek.com.br

## 🙏 Agradecimentos

- Equipe Groq pela API
- Comunidade Streamlit
- Todos os contribuidores

---

Desenvolvido com ❤️ pela equipe GuiraTek
