# 👗 Niéli Moda Casual - Sistema de Gestão

Um sistema completo de gestão para loja de moda casual, desenvolvido em Python com interface gráfica intuitiva usando Tkinter. O sistema permite gerenciar clientes, produtos, vendas, contas a receber, promoções, créditos e muito mais.

## 📋 Características Principais

- **Gestão de Clientes**: Cadastro, atualização e exclusão de clientes com telefone e histórico de data
- **Gestão de Produtos**: Controle completo de estoque com descrição, tamanho, preço de custo e venda
- **Sistema de Vendas**: Registro de vendas com seleção de clientes e produtos, cálculo automático de totais
- **Contas a Receber**: Acompanhamento de pagamentos, registro de créditos e gestão de cobranças
- **Promoções**: Gerenciamento de produtos em promoção com preços especiais
- **Sistema de Créditos**: Emissão e controle de créditos para clientes
- **Bags**: Funcionalidade para criar "bags" (lista de desejos) de produtos para clientes
- **Dashboard**: Visualização de indicadores principais (clientes, vendas, receita, etc.)
- **Banco de Dados SQLite**: Armazenamento persistente de todos os dados

## 🛠 Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter** - Interface gráfica
- **SQLite3** - Banco de dados
- **Pillow (PIL)** - Processamento de imagens
- **PyWhatKit** - Integração com WhatsApp
- **PyAutoGUI** - Automação de GUI
- **Wikipedia** - Integração com Wikipedia
- **Requests** - Requisições HTTP

## 📁 Estrutura do Projeto

```
Nieli-Moda-Casual/
├── main.py                 # Arquivo principal - inicializa a aplicação
├── requirements.txt        # Dependências do projeto
├── PyWhatKit_DB.txt       # Banco de dados do PyWhatKit
│
├── Assets/                # Recursos visuais
│   ├── Background.png
│   ├── Clientes.png
│   ├── Produtos.png
│   ├── Vendas.png
│   ├── Relatorios.png
│   ├── ContasAReceber.png
│   ├── Promocoes.png
│   ├── Bags.png
│   └── iconbitmap.png
│
├── Database/              # Gestão de banco de dados
│   ├── __init__.py
│   └── database.py       # Criação e configuração do SQLite
│
├── Gui/                  # Interface gráfica principal
│   ├── __init__.py
│   └── gui.py           # Janela principal e menu de navegação
│
├── Clientes/             # Módulo de gestão de clientes
│   ├── __init__.py
│   └── clientes.py      # Cadastro, atualização e exclusão de clientes
│
├── Produtos/             # Módulo de gestão de produtos
│   ├── __init__.py
│   └── produtos.py      # Cadastro e controle de estoque
│
├── Vendas/               # Módulo de registro de vendas
│   ├── __init__.py
│   └── vendas.py        # Processamento de vendas e itens
│
├── ContasAReceber/       # Módulo de contas a receber
│   ├── __init__.py
│   └── contasareceber.py # Registro de pagamentos e gestão de créditos
│
├── Promocoes/            # Módulo de promoções
│   ├── __init__.py
│   └── promocoes.py     # Gestão de produtos em promoção
│
├── Bags/                 # Módulo de bags (lista de desejos)
│   ├── __init__.py
│   └── bags.py          # Criação e gestão de bags
│
└── Dashboard/            # Módulo de relatórios
    ├── __init__.py
    └── dashboard.py     # Indicadores e visualizações
```

## 🗄 Estrutura do Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas principais:

### Tabelas Principais

| Tabela | Descrição |
|--------|-----------|
| `clientes` | Dados de clientes (nome, telefone, data de cadastro) |
| `produtos` | Informações de produtos (descrição, tamanho, preços, estoque) |
| `vendas` | Registro de vendas com cliente e valor total |
| `itens_venda` | Itens individuais de cada venda |
| `pagamentos` | Registro de pagamentos de vendas |
| `creditos` | Créditos disponíveis para clientes |
| `bags` | Listas de desejos/bags de clientes |
| `itens_bag` | Produtos dentro de cada bag |

### Relacionamentos
- `clientes` ↔ `vendas` (1:N)
- `vendas` ↔ `itens_venda` (1:N)
- `produtos` ↔ `itens_venda` (1:N)
- `clientes` ↔ `pagamentos` (1:N)
- `clientes` ↔ `creditos` (1:N)
- `clientes` ↔ `bags` (1:N)

## 🚀 Como Executar

### Requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório** (se estiver no GitHub)
```bash
git clone https://github.com/seu-usuario/Nieli-Moda-Casual.git
cd Nieli-Moda-Casual
```

2. **Crie um ambiente virtual** (opcional, mas recomendado)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python main.py
```

## 📦 Dependências

| Pacote | Versão | Função |
|--------|--------|--------|
| `pillow` | - | Processamento de imagens (PIL) |
| `pywhatkit` | - | Integração com WhatsApp para envio de mensagens |
| `pyautogui` | - | Automação de GUI para interações automatizadas |
| `wikipedia` | - | Acesso a informações da Wikipedia |
| `requests` | - | Requisições HTTP para APIs externas |

## 💻 Funcionalidades por Módulo

### 1. **Clientes**
- ✅ Cadastrar novo cliente (nome, telefone)
- ✅ Atualizar dados de cliente (duplo clique na linha)
- ✅ Excluir cliente (pressionar Delete ou botão)
- ✅ Visualizar lista de todos os clientes
- ✅ Histórico de data de cadastro

### 2. **Produtos**
- ✅ Cadastrar novo produto (descrição, detalhe, tamanho, preços)
- ✅ Controle de estoque em tempo real
- ✅ Preço de custo e preço de venda
- ✅ Integração com promoções
- ✅ Preço promocional opcional

### 3. **Vendas**
- ✅ Buscar cliente por nome
- ✅ Buscar produto por descrição
- ✅ Adicionar itens à venda com quantidade
- ✅ Visualização de estoque disponível
- ✅ Cálculo automático do valor total
- ✅ Histórico de todas as vendas

### 4. **Contas a Receber**
- ✅ Registrar pagamentos de vendas
- ✅ Acompanhar vendas pendentes
- ✅ Sistema de créditos para clientes
- ✅ Usar créditos em novas compras
- ✅ Relatório de cobranças

### 5. **Promoções**
- ✅ Aplicar desconto a produtos específicos
- ✅ Definir preço promocional
- ✅ Visualizar produtos em promoção
- ✅ Gerenciar datas de promoção

### 6. **Bags (Lista de Desejos)**
- ✅ Criar bag para cliente
- ✅ Adicionar produtos à bag
- ✅ Atualizar status dos itens
- ✅ Visualizar bags por cliente

### 7. **Dashboard**
- 📊 Total de clientes cadastrados
- 📊 Quantidade de vendas realizadas
- 📊 Receita total gerada
- 📊 Produtos mais vendidos
- 📊 Indicadores gerenciais

## 🎨 Interface do Usuário

A aplicação possui uma interface intuitiva com:
- **Resolução**: 1200x740 pixels
- **Tema Visual**: Cores neutras (bege #E4E1DC) com destaque em verde, azul e vermelho
- **Navegação**: Menu lateral com 7 botões principais
- **Componentes**: Formulários, tabelas (Treeview), abas (Notebook)
- **Ícone**: Logo da Niéli Moda Casual

## 📝 Notas Importantes

- O banco de dados é criado automaticamente no primeiro acesso em `Database/database.db`
- As imagens estão localizadas na pasta `Assets/`
- O sistema suporta integração com WhatsApp via PyWhatKit para notificações
- Todos os dados são persistidos no SQLite
- A interface é responsiva e se adapta ao redimensionamento da janela

## 🔐 Segurança

- Utilize senhas fortes para acesso ao sistema (considere adicionar autenticação no futuro)
- Faça backups regulares do banco de dados
- Valide entradas de usuário para evitar injeção SQL

## 🚧 Melhorias Futuras

- [ ] Sistema de autenticação com usuários e senhas
- [ ] Relatórios em PDF/Excel
- [ ] Integração com APIs de pagamento
- [ ] Temas personalizáveis
- [ ] Backup automático de dados
- [ ] Modo escuro
- [ ] Suporte multi-idioma
- [ ] Sincronização em nuvem

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto, entre em contato com o desenvolvedor.

## 📄 Licença

Este projeto é de código aberto. Você é livre para usar, modificar e distribuir conforme necessário.

---

**Desenvolvido com ❤️ para Niéli Moda Casual**

Última atualização: 22 de dezembro de 2025
