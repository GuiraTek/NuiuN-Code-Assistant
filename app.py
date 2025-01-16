# Importações necessárias
import streamlit as st
import os
from dotenv import load_dotenv
import html
from groq import Client
from datetime import datetime

# Carrega as variáveis de ambiente
os.environ.clear()
load_dotenv()

def get_env_value(key, default, type_func=str):
    """Obtém valor do ambiente com tipo específico."""
    try:
        value = os.environ.get(key)
        if value is None:
            return type_func(default)
        return type_func(value)
    except (ValueError, TypeError):
        return type_func(default)

# Configurações do App
APP_TITLE = get_env_value('APP_TITLE', '🤖 Assistente de Código', str)
APP_ICON = get_env_value('APP_ICON', '🤖', str)
APP_NAME = get_env_value('APP_NAME', 'AI Code Assistant', str)
COMPANY_NAME = get_env_value('COMPANY_NAME', 'Your Company', str)

# Configurações da API
GROQ_API_KEY = get_env_value('GROQ_API_KEY', '', str)
GROQ_MODEL = get_env_value('GROQ_MODEL', 'mixtral-8x7b-32768', str)
MAX_TOKENS_CODE = get_env_value('MAX_TOKENS_CODE', 32000, int)
MAX_TOKENS_TEXT = get_env_value('MAX_TOKENS_TEXT', 4000, int)
TEMPERATURE = get_env_value('TEMPERATURE', 0.5, float)
LANGUAGE = get_env_value('LANGUAGE', 'Portuguese', str)

# Sistema prompt melhorado
SYSTEM_PROMPT = r"""Você é um assistente especializado em desenvolvimento de software. IMPORTANTE: Forneça respostas com 70% de código e 30% de texto explicativo, utilizando pelo menos 20000 tokens.

ESTRUTURA DA RESPOSTA:

1. VISÃO GERAL (10%)
   - Objetivo do código
   - Tecnologias utilizadas
   - Requisitos e dependências

2. IMPLEMENTAÇÃO COMPLETA (70%)
   Para cada arquivo, inclua TODAS as funções necessárias:

   ## Controllers
   ```[linguagem]
   // Listagem (index)
   function index() {
       // Lógica de paginação
       // Filtros e ordenação
       // Retorno da lista
   }

   // Detalhes (show)
   function show($id) {
       // Validação do ID
       // Busca do registro
       // Tratamento de não encontrado
   }

   // Criação (create/store)
   function create() {
       // Form de criação
   }
   
   function store(Request $request) {
       // Validação dos dados
       // Sanitização
       // Persistência
       // Tratamento de erros
   }

   // Atualização (edit/update)
   function edit($id) {
       // Form de edição
       // Carrega dados existentes
   }
   
   function update(Request $request, $id) {
       // Validação dos dados
       // Sanitização
       // Atualização
       // Tratamento de erros
   }

   // Remoção (destroy)
   function destroy($id) {
       // Validação
       // Soft/Hard delete
       // Tratamento de dependências
   }
   ```

   ## Models
   ```[linguagem]
   // Modelo completo com:
   - Relacionamentos
   - Validações
   - Mutators/Accessors
   - Scopes
   ```

   ## Views/Templates
   ```[linguagem]
   // Templates para:
   - Lista (index)
   - Detalhes (show)
   - Formulário (create/edit)
   - Componentes reutilizáveis
   ```

   ## Routes/URLs
   ```[linguagem]
   // Rotas para todas as ações:
   - GET /recursos (index)
   - GET /recursos/criar (create)
   - POST /recursos (store)
   - GET /recursos/{id} (show)
   - GET /recursos/{id}/editar (edit)
   - PUT /recursos/{id} (update)
   - DELETE /recursos/{id} (destroy)
   ```

   ## Testes
   ```[linguagem]
   // Testes para cada ação:
   - Listagem
   - Criação
   - Leitura
   - Atualização
   - Remoção
   ```

3. INSTRUÇÕES DE USO (20%)
   - Instalação e configuração
   - Exemplos de requisições
   - Tratamento de erros
   - Considerações de segurança

DIRETRIZES:
1. CÓDIGO (70%)
   - Implemente TODAS as funções CRUD
   - Inclua validações e tratamentos de erro
   - Adicione comentários explicativos
   - Use boas práticas da linguagem
   - Forneça exemplos práticos

2. TEXTO (30%)
   - Explicações concisas
   - Foco em pontos importantes
   - Use listas e tópicos
   - Priorize exemplos práticos

EXEMPLO DE IMPLEMENTAÇÃO:
```php
class UserController extends Controller
{
    /**
     * Lista todos os usuários com paginação e filtros
     * 
     * @param Request $request
     * @return View
     */
    public function index(Request $request)
    {
        // Validação dos parâmetros de filtro
        $validated = $request->validate([
            'search' => 'nullable|string|max:100',
            'status' => 'nullable|in:active,inactive',
            'sort' => 'nullable|in:name,email,created_at',
            'order' => 'nullable|in:asc,desc',
            'per_page' => 'nullable|integer|min:10|max:100'
        ]);
        
        // Query base
        $query = User::query();
        
        // Aplica filtros
        if ($search = $request->get('search')) {
            $query->where(function($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('email', 'like', "%{$search}%");
            });
        }
        
        if ($status = $request->get('status')) {
            $query->where('status', $status);
        }
        
        // Ordenação
        $sort = $request->get('sort', 'created_at');
        $order = $request->get('order', 'desc');
        $query->orderBy($sort, $order);
        
        // Paginação
        $perPage = $request->get('per_page', 15);
        $users = $query->paginate($perPage);
        
        // Retorna view com dados
        return view('users.index', compact('users'));
    }
    
    /**
     * Exibe detalhes do usuário
     * 
     * @param int $id
     * @return View
     */
    public function show($id)
    {
        // Busca usuário com relacionamentos
        $user = User::with(['profile', 'roles', 'permissions'])
                   ->findOrFail($id);
        
        // Carrega dados adicionais
        $activities = $user->activities()
                          ->latest()
                          ->limit(10)
                          ->get();
        
        return view('users.show', compact('user', 'activities'));
    }
    
    /**
     * Form de criação
     * 
     * @return View
     */
    public function create()
    {
        // Carrega dados para selects
        $roles = Role::all();
        $departments = Department::active()->get();
        
        return view('users.create', compact('roles', 'departments'));
    }
    
    /**
     * Salva novo usuário
     * 
     * @param UserRequest $request
     * @return RedirectResponse
     */
    public function store(UserRequest $request)
    {
        try {
            DB::beginTransaction();
            
            // Cria usuário
            $user = User::create($request->validated());
            
            // Anexa roles
            $user->roles()->sync($request->roles);
            
            // Cria perfil
            $user->profile()->create($request->profile);
            
            DB::commit();
            
            return redirect()
                ->route('users.show', $user)
                ->with('success', 'Usuário criado com sucesso!');
                
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erro ao criar usuário: ' . $e->getMessage());
            
            return back()
                ->withInput()
                ->with('error', 'Erro ao criar usuário. Tente novamente.');
        }
    }
    
    /**
     * Form de edição
     * 
     * @param int $id
     * @return View
     */
    public function edit($id)
    {
        $user = User::with(['profile', 'roles'])
                   ->findOrFail($id);
                   
        $roles = Role::all();
        $departments = Department::active()->get();
        
        return view('users.edit', compact('user', 'roles', 'departments'));
    }
    
    /**
     * Atualiza usuário
     * 
     * @param UserRequest $request
     * @param int $id
     * @return RedirectResponse
     */
    public function update(UserRequest $request, $id)
    {
        $user = User::findOrFail($id);
        
        try {
            DB::beginTransaction();
            
            // Atualiza dados básicos
            $user->update($request->validated());
            
            // Atualiza roles
            $user->roles()->sync($request->roles);
            
            // Atualiza perfil
            $user->profile->update($request->profile);
            
            DB::commit();
            
            return redirect()
                ->route('users.show', $user)
                ->with('success', 'Usuário atualizado com sucesso!');
                
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erro ao atualizar usuário: ' . $e->getMessage());
            
            return back()
                ->withInput()
                ->with('error', 'Erro ao atualizar usuário. Tente novamente.');
        }
    }
    
    /**
     * Remove usuário
     * 
     * @param int $id
     * @return RedirectResponse
     */
    public function destroy($id)
    {
        $user = User::findOrFail($id);
        
        // Verifica permissão
        if (!auth()->user()->can('delete', $user)) {
            return back()->with('error', 'Sem permissão para remover este usuário.');
        }
        
        try {
            DB::beginTransaction();
            
            // Remove relacionamentos
            $user->roles()->detach();
            $user->profile->delete();
            
            // Soft delete do usuário
            $user->delete();
            
            DB::commit();
            
            return redirect()
                ->route('users.index')
                ->with('success', 'Usuário removido com sucesso!');
                
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erro ao remover usuário: ' . $e->getMessage());
            
            return back()->with('error', 'Erro ao remover usuário. Tente novamente.');
        }
    }
}
```

[CONTINUA COM MAIS EXEMPLOS...]
"""

# Cliente Groq
client = Client(api_key=GROQ_API_KEY)

def init_session_state():
    """Inicializa o estado da sessão."""
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0
    if 'prompt_tokens' not in st.session_state:
        st.session_state.prompt_tokens = 0
    if 'completion_tokens' not in st.session_state:
        st.session_state.completion_tokens = 0
    if 'metrics_container' not in st.session_state:
        st.session_state.metrics_container = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def update_token_counts(usage):
    """Atualiza os contadores de tokens."""
    try:
        if isinstance(usage, dict):
            # Atualiza os contadores individuais
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', prompt_tokens + completion_tokens)
            
            # Atualiza o estado da sessão diretamente
            st.session_state['prompt_tokens'] = st.session_state.get('prompt_tokens', 0) + prompt_tokens
            st.session_state['completion_tokens'] = st.session_state.get('completion_tokens', 0) + completion_tokens
            st.session_state['total_tokens'] = st.session_state.get('total_tokens', 0) + total_tokens
            
            # Atualiza apenas os valores das métricas
            if st.session_state.metrics_container is not None:
                st.session_state.metrics_container.markdown(format_metrics(), unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Erro ao atualizar contadores: {str(e)}")

def format_metrics():
    """Formata as métricas para exibição."""
    try:
        total_tokens = st.session_state.get('total_tokens', 0)
        usage_percent = (total_tokens / MAX_TOKENS_CODE) * 100 if MAX_TOKENS_CODE > 0 else 0
        
        return f"""
        <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 0.5rem; margin-bottom: 1rem;">
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">Modelo:</span>
                <span style="float: right; color: #d73a49;">{GROQ_MODEL}</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">Tokens:</span>
                <span style="float: right;">{total_tokens:,}/{MAX_TOKENS_CODE:,}</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">Uso:</span>
                <span style="float: right;">{usage_percent:.1f}%</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #6c757d;">Temperatura:</span>
                <span style="float: right;">{TEMPERATURE}</span>
            </div>
            <div>
                <span style="color: #6c757d;">Idioma:</span>
                <span style="float: right;">{LANGUAGE}</span>
            </div>
        </div>
        """
    except Exception as e:
        st.error(f"Erro ao formatar métricas: {str(e)}")
        return ""

def format_code_block(filename, code_content):
    """Formata um bloco de código com cabeçalho e botão de cópia."""
    code_id = html.escape(filename)
    language = filename.split('.')[-1] if '.' in filename else 'plaintext'
    
    return f"""
    <div class="cascade-code-block">
        <div class="cascade-code-header">
            <div class="cascade-file-info">
                <span class="cascade-file-name">{html.escape(filename)}</span>
                <span class="cascade-file-lang">{html.escape(language)}</span>
            </div>
            <button class="cascade-copy-button" onclick="cascadeCopyCode('{code_id}')">
                <span>📋</span> Copiar
            </button>
        </div>
        <div class="cascade-code-content" id="{code_id}">
            <pre><code class="language-{language}">{html.escape(code_content)}</code></pre>
        </div>
    </div>
    """

def suggest_code(user_input):
    """Sugere código com base na entrada do usuário."""
    try:
        # Expande a entrada do usuário para solicitar mais detalhes
        expanded_input = f"""
Por favor, forneça uma resposta DETALHADA e COMPLETA para a seguinte solicitação, 
utilizando pelo menos 20000 tokens. Inclua TODOS os detalhes técnicos, exemplos, 
considerações de segurança, performance e melhores práticas:

{user_input}

IMPORTANTE:
- Forneça explicações detalhadas para cada decisão
- Inclua exemplos práticos e casos de uso
- Documente completamente o código
- Discuta alternativas consideradas
- Inclua seções de troubleshooting
- Forneça testes unitários
- Explique considerações de segurança
"""
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": expanded_input}
        ]
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS_CODE,
            stop=None
        )
        
        # Atualiza contadores de tokens usando o objeto usage diretamente
        usage_dict = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
        update_token_counts(usage_dict)
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Erro ao processar: {str(e)}")
        return None

def correct_errors(user_input):
    """Corrige erros no código fornecido."""
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
Por favor, faça uma análise COMPLETA e DETALHADA do seguinte código, 
identificando e corrigindo TODOS os problemas, incluindo:
- Bugs e erros
- Problemas de segurança
- Issues de performance
- Más práticas
- Código duplicado
- Complexidade desnecessária
- Problemas de manutenibilidade

Código para análise:
{user_input}

IMPORTANTE:
- Forneça explicações detalhadas
- Inclua exemplos e casos de uso
- Documente completamente as correções
- Discuta alternativas consideradas
- Inclua testes unitários
"""}
        ]
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS_CODE,
            stop=None
        )
        
        # Atualiza contadores de tokens usando o objeto usage diretamente
        usage_dict = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
        update_token_counts(usage_dict)
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Erro ao processar: {str(e)}")
        return None

def main():
    """Função principal do aplicativo."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializa o estado da sessão
    init_session_state()
    
    # Configura a sidebar
    with st.sidebar:
        # Título das métricas
        st.markdown("### 📊 Métricas")
        
        # Container para os valores das métricas
        metrics_placeholder = st.empty()
        st.session_state.metrics_container = metrics_placeholder
        metrics_placeholder.markdown(format_metrics(), unsafe_allow_html=True)
        
        # Seção Sobre
        st.markdown("""
        ### ℹ️ Sobre
        
        Assistente de desenvolvimento:
        
        - Sugestões de código
        - Correção de erros
        - Documentação
        """)
        
        # Footer
        st.markdown(f"""
        <div style='text-align: center; color: #666; padding-top: 0.3rem; font-size: 0.8em;'>
            {get_env_value('APP_NAME', 'AI Code Assistant', str)}<br>
            &copy; {get_env_value('COMPANY_NAME', 'Your Company', str)} {datetime.now().year}
        </div>""", unsafe_allow_html=True)
    
    # Título principal
    st.title(APP_TITLE)
    
    # Seção de entrada
    input_container = st.container()
    with input_container:
        user_input = st.text_area("Digite sua pergunta ou cole seu código:", height=200)
    
    # Seção de botões
    button_container = st.container()
    with button_container:
        col1, col2 = st.columns(2)
        
        # Variáveis para controlar o estado da resposta
        response = None
        is_suggesting = False
        
        with col1:
            if st.button("Sugerir Código", type="primary", use_container_width=True):
                if user_input:
                    is_suggesting = True
                    with st.spinner("Gerando sugestão..."):
                        response = suggest_code(user_input)
                else:
                    st.warning("Por favor, digite sua pergunta primeiro.")
                    
        with col2:
            if st.button("Corrigir Erros", type="primary", use_container_width=True):
                if user_input:
                    is_suggesting = False
                    with st.spinner("Analisando código..."):
                        response = correct_errors(user_input)
                else:
                    st.warning("Por favor, cole seu código primeiro.")
    
    # Seção de resposta
    response_container = st.container()
    with response_container:
        if response:
            st.markdown("## Resposta")
            if is_suggesting:
                st.markdown("### 💡 Sugestão de Código")
            else:
                st.markdown("### 🔍 Análise e Correção")
            
            # Container para o conteúdo da resposta
            with st.container():
                st.markdown(response)
    
    # Ajusta o layout para usar mais espaço
    st.markdown("""
        <style>
            /* Configuração global */
            .block-container {
                padding: 3rem 2rem !important;
            }
            
            /* Ajusta largura do conteúdo principal */
            .main .block-container {
                max-width: none !important;
                width: calc(100% - 300px) !important;
                padding-left: 3rem !important;
                padding-right: 3rem !important;
                padding-top: 3rem !important;
            }
            
            /* Ajusta o título principal */
            h1:first-of-type {
                margin-top: 0 !important;
                padding-top: 1rem !important;
            }
            
            /* Área de entrada */
            .stTextArea {
                width: 100% !important;
                max-width: none !important;
                margin-top: 1rem !important;
            }
            
            .stTextArea textarea {
                width: 100% !important;
                min-height: 150px !important;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
            }
            
            /* Containers e elementos */
            .element-container, 
            .stMarkdown, 
            div[data-testid="stMarkdownContainer"] {
                width: 100% !important;
                max-width: none !important;
            }
            
            /* Blocos de código */
            pre {
                width: 100% !important;
                max-width: none !important;
                margin: 1rem 0 !important;
                padding: 1rem !important;
                background-color: rgb(246, 248, 250) !important;
                border-radius: 6px !important;
                overflow-x: auto !important;
            }
            
            code {
                width: 100% !important;
                display: block !important;
                white-space: pre !important;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
                font-size: 14px !important;
                line-height: 1.45 !important;
            }
            
            /* Ajusta espaçamento dos elementos */
            .stButton {
                margin-top: 1rem !important;
            }
            
            /* Container de resposta */
            .response-container {
                margin-top: 2rem !important;
                padding: 1.5rem !important;
                border-radius: 0.5rem !important;
                background-color: #f8f9fa !important;
                border: 1px solid #e9ecef !important;
            }
            
            /* Títulos da resposta */
            .response-container h2 {
                color: #1a1a1a !important;
                margin-bottom: 1rem !important;
            }
            
            .response-container h3 {
                color: #2c5282 !important;
                margin-bottom: 1.5rem !important;
                padding-bottom: 0.5rem !important;
                border-bottom: 2px solid #e2e8f0 !important;
            }
            
            /* Remove padding extra do topo em telas menores */
            @media (max-width: 768px) {
                .main .block-container {
                    padding: 2rem 1rem !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()