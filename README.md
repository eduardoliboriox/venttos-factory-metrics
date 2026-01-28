# Venttos – Factory Metrics

**Venttos – Factory Metrics** é um sistema web de **inteligência operacional industrial**, desenvolvido para **engenharia, produção, PCP, RH e liderança**, com foco em **controle de absenteísmo**, **análise de headcount**, **indicadores executivos** e **visualização de dados inspirada no Power BI**.

O projeto foi concebido para **uso real em ambiente fabril**, priorizando:

* Confiabilidade dos dados
* Baixo erro operacional
* Leitura executiva clara
* Arquitetura limpa, escalável e de fácil manutenção

---

## 🎯 Finalidade do Sistema

* Lançamento estruturado de **absenteísmo**
* Cálculo automático de **HC real**
* Consolidação de faltas por **linha, setor e cargo**
* **Dashboard operacional**
* **Visão executiva estilo Power BI**
* **Relatórios analíticos sob demanda**
* Base sólida para decisões de **PCP, RH, Produção e Diretoria**

---

## 🔐 Autenticação & Controle de Acesso

O sistema possui **autenticação completa**, com múltiplos provedores e controle administrativo.

### Métodos de login suportados

* ✅ **Login local (usuário e senha)**
* ✅ **Google OAuth 2.0**
* ✅ **GitHub OAuth**

### Cadastro de usuários (login local)

* Usuários podem se **cadastrar via formulário**
* Novos usuários entram como **pendentes**
* Apenas **administradores** podem aprovar ou negar acessos
* O **primeiro usuário do sistema** é criado automaticamente como **admin**

### Controle de permissões

* Autenticação via **Flask-Login**
* Decorators para rotas administrativas
* Separação clara entre:

  * Usuários ativos
  * Usuários pendentes
  * Administradores

📌 *Objetivo:* garantir segurança, rastreabilidade e controle de acesso em ambiente corporativo.

---

## 🧠 Conceitos-Chave do Projeto

* **Setor → Linha dependente** (select dinâmico)
* Eliminação de digitação manual crítica
* Dados padronizados (menos ruído, mais decisão)
* **Services** concentram regras de negócio
* **Repositories isolam SQL**
* **Rotas HTML separadas de rotas REST (API)**
* Autenticação desacoplada da lógica de domínio
* Arquitetura inspirada em **DDD leve + Clean Architecture**

---

## 📊 Funcionalidades Principais

### 📌 Lançamento de Absenteísmo

* Seleção de:

  * Data
  * Filial
  * Setor
  * Linha (dinâmica)
  * Turno
* Definição de **HC padrão**
* Cálculo automático de **HC real**
* Registro de faltas por **cargo**
* Envio estruturado via **API REST**

---

### 📊 Dashboard Operacional

* KPIs consolidados de absenteísmo
* Indicadores por período
* Base operacional para acompanhamento diário
* Cards objetivos e leitura rápida

---

### 📈 Power BI – Visão Executiva

Tela dedicada com **experiência inspirada no Power BI**, sem dependência externa:

* KPIs executivos
* Ranking de linhas por absenteísmo
* Gráficos de barras verticais (ranking)
* Gráficos horizontais (distribuição)
* Interação por **clique nas barras**
* **Mini-modal analítico por linha**
* Visual corporativo, escuro e consistente

📌 *Objetivo:* permitir decisão rápida sem abrir ferramentas externas.

---

### 📄 Relatórios Analíticos

Tela exclusiva para geração de relatórios:

* Filtros por:

  * Setor
  * Tipo (Semanal / Mensal / Anual)
* Geração sob demanda via **API**
* Ranking **Top 10 linhas com absenteísmo**
* Identificação de **cargo crítico global**
* Identificação de **cargo crítico por linha**
* Cálculo de **percentual de impacto dentro da linha**
* Texto analítico pronto para leitura executiva

---

## 📱 Interface & UX

* Totalmente responsiva
* Desktop e mobile
* Login mobile com **fluxo próprio**
* Layout mobile inspirado em **app nativo**
* Sidebar no desktop
* Hierarquia visual focada em dados e decisão

---

## ☁️ Infraestrutura

* Deploy em **Railway**
* Banco **PostgreSQL**
* Gunicorn em produção
* Variáveis de ambiente via `.env`
* Estrutura pronta para CI/CD

---

## 🧱 Estrutura do Projeto

```text

project/
├─ app/
│   ├─ __init__.py            # create_app()
│   ├─ config.py              # Configurações / env
│   ├─ extensions.py          # DB (psycopg)
│   │
│   ├─ auth/
│   │   ├─ __init__.py   (vazio)
│   │   ├─ decorators.py
│   │   ├─ models.py
│   │   ├─ repository.py
│   │   ├─ routes.py
│   │   └─ service.py
│   │
│   ├─ repositories/          # Acesso ao banco (SQL)
│   │   ├─ __init__.py
│   │   ├─ atestados_repository.py
│   │   ├─ cargos_repository.py
│   │   ├─ hc_linhas_repository.py
│   │   ├─ lancamentos_repository.py
│   │   └─ modelos_repository.py
│   │  
│   ├─ routes/
│   │   ├─ __init__.py
│   │   ├─ api.py             # Rotas REST (JSON)
│   │   └─ pages.py           # Rotas HTML
│   │
│   ├─ services/              # Regras de negócio
│   │   ├─ __init__.py
│   │   ├─ atestados_service.py
│   │   ├─ cargos_service.py
│   │   ├─ hc_linhas_service.py
│   │   ├─ lancamentos_service.py
│   │   ├─ modelos_service.py
│   │   ├─ pcp_service.py
│   │   └─ relatorios_service.py
│   │
│   ├─ templates/             # Jinja2
│   │   ├─ auth/
│   │   │   ├─ login.html  
│   │   │   └─ users_admin.html
│   │   │   └─ users_all.html 
│   │   │
│   │   ├─ layouts/
│   │   │   ├─ mobile/
│   │   │   │    └─ login_choice.html
│   │   │   │    └─ login_form.htm
│   │   │   │    └─ register_form.htm
│   │   │   │      
│   │   │   └─ app.html
│   │   │   └─ auth.html
│   │   │
│   │   ├─ atestados.html
│   │   ├─ base.html    (vou apagar, conteudo passou para app.html)
│   │   ├─ cargos.html
│   │   ├─ dashboard.html
│   │   ├─ hclinhas.html
│   │   ├─ inicio.html
│   │   ├─ lancamento.html
│   │   ├─ powerbi.html
│   │   ├─ relatorios.html
│   │
│   └─ static/
│       ├─ css/
│       │   ├─ auth.css
│       │   ├─ powerbi.css
│       │   └─ style.css
│       │
│       ├─ js/
│       │   ├─ dashboard-live.js
│       │   ├─ main.js
│       │   ├─ pcp.js
│       │   ├─ powerbi-live.js
│       │   ├─ powerbi.js
│       │   └─ relatorios.js
│       │
│       ├─ images/
│       └─ fonts/inter.woff2
│
├─ migrations/                # Alembic (ainda não utilizado)
├─ tests/                     # pytest
├─ run.py                     # Entrypoint
├─ requirements.txt
├─ LICENSE
├─ Procfile                   # Railway
├─ README.md
├─ .env                       # NÃO versionar
├─ .gitignore
└─ pyproject.toml
```

---

## ⚙️ Tecnologias Utilizadas

* Python 3
* Flask
* Flask-Login
* Authlib (OAuth)
* Jinja2
* HTML5 / CSS3
* JavaScript (Vanilla)
* PostgreSQL
* Bootstrap 5
* Railway

---

## ▶️ Como Rodar Localmente

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/venttos-factory-metrics.git
cd venttos-factory-metrics
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar `.env`

```env
SECRET_KEY=supersecretkey
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

### 5️⃣ Executar

```bash
python run.py
```

Acesse:

```
http://127.0.0.1:5000
```

---

## 👨‍💻 Autor

Desenvolvido por **Eduardo Libório**
Junior Backend Developer

📧 [eduardosolenomorizliborio@gmail.com](mailto:eduardosolenomorizliborio@gmail.com)

---

## 📄 Licença

Projeto de uso **privado / interno**.

