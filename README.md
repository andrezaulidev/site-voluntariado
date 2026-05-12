# 🍽️ Marmita Solidária · Escola Paulo de Tarso

Um website moderno e responsivo desenvolvido para promover o projeto **Marmita Solidária** — uma iniciativa de voluntariado para combater a insegurança alimentar na comunidade local.

---

## 🎯 Projeto

O site foi desenvolvido como atividade prática da disciplina de Desenvolvimento Web, transformando conhecimento técnico em impacto social concreto.

**Desenvolvido por:** André Zauli  
**Turma:** 2º Ano B · Escola Paulo de Tarso  
**Ano:** 2026 · Ano Internacional dos Voluntários para o Desenvolvimento Sustentável

---

## ✨ Funcionalidades

### 🎨 **Interface Visual**
- Design moderno e responsivo (mobile-first)
- Paleta de cores: Laranja, Azul, Branco
- Tipografia elegante (Playfair Display + Nunito Sans)
- Animações suaves e presença web otimizada
- Acessibilidade (prefers-reduced-motion)

### 📱 **Responsividade**
- Menu hamburger para dispositivos menores
- Layout adaptável para desktop, tablet e mobile
- Touch-friendly buttons e inputs

### 🎓 **Menu de Navegação**
- Navbar fixa com efeito de scroll (mudança de cor)
- Menu responsivo com animação de hamburger toggle
- Links de navegação suave (smooth scroll)
- Call-to-action dinâmico

### 📝 **Formulário Inteligente**
- Validação de campos em tempo real
- Verificação de email duplicado
- Sugestão de contribuição (6 opções com emojis)
- Mensagens de erro personalizadas
- Feedback visual ao preencher

### 📊 **Sistema de Voluntários**
- **localStorage** para persistência de dados
- Contador dinâmico de inscritos
- Limite máximo de 50 voluntários
- Verificação automática de reinscrita
- Exportação de dados (CSV) para administradores
- Cancelamento de inscrição

### ✋ **Animações e Interatividade**
- Efeitos de blur/glassmorphism
- Animações de entrada (reveal animations)
- Intersection Observer para performance otimizada
- Transições fluidas em todos os elementos
- Blobs e gráficos animados no hero

### 📍 **Seções do Site**
1. **Hero** – Introdução com chamada principal
2. **Ano do Voluntariado** – Contexto global da iniciativa
3. **A Causa** – Dados sobre insegurança alimentar
4. **O Projeto** – Detalhes, timeline e metas
5. **Formulário** – Inscrição de voluntários
6. **Desenvolvedor** – Sobre o criador e tecnologias
7. **Footer** – Informações e créditos

---

## 🛠️ Tecnologias Utilizadas

Desenvolvido com stack moderno:

- **HTML5** – Semântico e acessível
- **CSS3** – Grid, Flexbox, Cascata otimizada
- **JavaScript (ES6+)** – Funcionalidades interativas
- **localStorage API** – Persistência de dados
- **SVG** – Gráficos vetoriais escaláveis
- **Google Fonts** – Tipografia web

---

## 📂 Estrutura de Arquivos

```
site-voluntariado/
├── index.html       # Página principal (HTML5 semântico)
├── style.css        # Estilos completos (23 KB)
├── script.js        # Funcionalidades JavaScript (13 KB)
└── README.md        # Este arquivo
```

---

## 🚀 Como Usar

### 1️⃣ **Abrir o Site Localmente**

#### Opção A: Python (recomendado)
```bash
cd /workspaces/site-voluntariado
python3 -m http.server 8000 --bind 127.0.0.1
# Acesse: http://localhost:8000
```

#### Opção B: Node.js
```bash
npx http-server .
```

#### Opção C: Live Server (VS Code)
Instale a extensão "Live Server" e clique em "Go Live"

---

### 2️⃣ **Funcionalidades do JavaScript**

#### Menu Responsivo
- Click no hamburger (📱) para abrir/fechar menu
- Links fecham automaticamente ao clicar
- Animação suave de transformação

#### Formulário com Validação
- Preencha nome, idade, email
- Escolha suas formas de contribuição
- Clique em "Confirmar minha inscrição"
- Dados salvos em `localStorage` automaticamente

#### Verificação de Inscrição
- Se tentar se inscrever com e-mail já cadastrado, verá mensagem personalizada
- Opção para cancelar inscrição anterior

#### Contador Dinâmico
- Atualiza em tempo real ao se inscrever
- Barra de progresso visual (meta: 50 voluntários)
- Animação de números

---

### 3️⃣ **Funções Úteis (Console)**

Abra o Console do Navegador (F12 → Console) e use:

#### Exportar dados dos voluntários em CSV
```javascript
exportVolunteerData()
```
Baixa um arquivo `marmita-voluntarios.csv` com todos os inscritos

#### Limpar dados (apenas testes)
```javascript
clearAllVoluneers()
```
⚠️ **Cuidado:** Deleta todos os dados salvos

#### Ver dados no localStorage
```javascript
JSON.parse(localStorage.getItem('marmita-voluntarios'))
```

---

## 🎯 Melhorias Implementadas

✅ **Menu Responsivo** com animação hamburger  
✅ **Validação Completa** de formulário com mensagens  
✅ **localStorage** para persistência de voluntários  
✅ **Contador Dinâmico** com animações  
✅ **Reveal Animations** com Intersection Observer  
✅ **Acessibilidade** (focus-visible, prefers-reduced-motion)  
✅ **Performance** (will-change, transitions otimizadas)  
✅ **Design Responsivo** (CSS Grid, Flexbox)  
✅ **Efeitos Visuais** (blur, glassmorphism, hover states)  
✅ **Funcionalidades Extras** (exportar dados, cancelar inscrição)  

---

## 📱 Responsividade

O site é totalmente responsivo com breakpoints:

- **Desktop:** 1440px+ (versão completa)
- **Tablet:** 860px–1024px (layout adaptado)
- **Mobile:** até 860px (menu hamburger, colunas únicas)

---

## ♿ Acessibilidade

- ✓ Contraste adequado de cores
- ✓ Texto alt em imagens/SVG
- ✓ Focus states visíveis
- ✓ Suporte a prefers-reduced-motion
- ✓ Navegação por teclado funcional
- ✓ Labels associadas em formulários

---

## 🔐 Privacidade & Dados

Os dados dos voluntários são salvos **localmente** no seu navegador via `localStorage`:
- Nenhuma informação é enviada para servidores externos
- Dados persistem enquanto o cache não for limpo
- Funciona offline após primeira visita

---

## 📋 Próximas Melhorias Sugeridas

- [ ] Backend para sincronização de dados
- [ ] Envio de formulário por email
- [ ] Dashboard para administradores
- [ ] Autenticação e gestão de usuários
- [ ] Integração com calendário de eventos
- [ ] Geolocalização para voluntários próximos

---

## 📄 Licença

Projeto desenvolvido para fins educacionais.  
© 2026 Escola Paulo de Tarso

---

## 🤝 Suporte

Dúvidas? Favor contactar que desenvolveu!

**Marmita Solidária 2026**  
_"Uma marmita pode mudar um dia. Muitos voluntários mudam vidas."_