# 📖 Documentação Técnica · script.js

Guia completo das funcionalidades JavaScript do projeto Marmita Solidária.

---

## 📋 Índice

1. [Constantes e Seletores](#constantes)
2. [Navbar](#navbar)
3. [localStorage](#localstorage)
4. [Formulário](#formulário)
5. [Validação](#validação)
6. [UI](#ui)
7. [Contadores](#contadores)
8. [Reveal Animations](#reveal)
9. [Funções Úteis](#utilitários)

---

## <a id="constantes"></a>🔧 Constantes e Seletores

```javascript
const STORAGE_KEY = 'marmita-voluntarios';
const MAX_VOLUNTEERS = 50;
```

Todas as variáveis globais e seletores de DOM são definidas no início do arquivo para fácil acesso e manutenção.

---

## <a id="navbar"></a>🎯 Navbar e Menu Responsivo

### Efeito de Navbar ao Scroll

```javascript
window.addEventListener('scroll', () => {
  if (window.scrollY > 20px) {
    navbar.classList.add('scrolled');
  }
});
```

**O que faz:** 
- Detecta quando o usuário rola 20px para baixo
- Ativa a classe `.scrolled` na navbar
- CSS muda cor de fundo, sombra e cores dos links

### Toggle Menu (Hamburger)

```javascript
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  // Anima os spans do hamburger
});
```

**O que faz:**
- Abre/fecha menu ao clicar no hamburger
- Anima os 3 spans (linhas) para transformar em X
- Rotação de 45° e -45°

### Fechar Menu ao Navegar

```javascript
navLinksArray.forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
  });
});
```

**O que faz:**
- Menu fecha automaticamente ao clicar em um link
- Volta as linhas do hamburger ao normal
- UX melhor em mobile

---

## <a id="localstorage"></a>💾 Gerenciamento com localStorage

### Carregar Voluntários

```javascript
function loadVolunteers() {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
}
```

- Recupera string JSON do localStorage
- Converte para array de objetos
- Retorna array vazio se não houver dados

### Salvar Voluntários

```javascript
function saveVolunteers(volunteers) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(volunteers));
}
```

- Converte array em string JSON
- Salva na chave `STORAGE_KEY`
- Persiste no navegador

### Verificar Email Duplicado

```javascript
function emailExists(email) {
  const volunteers = loadVolunteers();
  return volunteers.some(v => 
    v.email.toLowerCase() === email.toLowerCase()
  );
}
```

- Busca email ignorando maiúsculas/minúsculas
- Retorna true se existe, false caso contrário

### Recuperar Dados de Voluntário

```javascript
function getVolunteerByEmail(email) {
  const volunteers = loadVolunteers();
  return volunteers.find(v => 
    v.email.toLowerCase() === email.toLowerCase()
  );
}
```

- Encontra sempre desconsiderando case
- Retorna objeto do voluntário ou undefined

---

## <a id="formulário"></a>📝 Envio e Processamento de Formulário

### Estrutura de Dados Coletados

```javascript
const formData = {
  nome: "José Silva",
  idade: 17,
  email: "jose@email.com",
  turma: "2º ano A",
  contribuicao: ["arrecadar", "distribuir"],
  obs: "Tenho disponibilidade de sábado",
  timestamp: "12/05/2026, 14:30:00"
};
```

### Fluxo de Envio

1. **Validar** dados do formulário
2. **Verificar** email duplicado
3. **Verificar** limite de voluntários
4. **Salvar** no localStorage
5. **Mostrar** mensagem de sucesso
6. **Atualizar** contadores

### Event Listener do Form

```javascript
volunteerForm.addEventListener('submit', (e) => {
  e.preventDefault(); // Previne envio padrão
  
  // Coleta dados
  // Valida
  // Verifica duplicações
  // Salva e mostra sucesso
});
```

---

## <a id="validação"></a>✅ Validação de Formulário

### Função Principal

```javascript
function validateForm(data) {
  clearErrors(); // Limpa mensagens anteriores
  let isValid = true;
  
  // Validações...
  
  return isValid;
}
```

### Validações Implementadas

#### Nome
```javascript
if (!data.nome.trim()) {
  // Mostra erro: "Nome é obrigatório"
} else if (data.nome.trim().length < 3) {
  // Mostra erro: "Mínimo 3 caracteres"
}
```

#### Idade
```javascript
if (!data.idade) {
  // Mostra erro: "Idade é obrigatória"
} else if (data.idade < 10 || data.idade > 99) {
  // Mostra erro: "Idade entre 10 e 99"
}
```

#### Email
```javascript
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(data.email)) {
  // Mostra erro: "E-mail inválido"
}
```

#### Contribuição
```javascript
const hasChecked = Array.from(checkboxes)
  .some(cb => cb.checked);
if (!hasChecked) {
  // Mostra erro: "Escolha ao menos uma opção"
}
```

### Limpeza de Erros

```javascript
function clearErrors() {
  document.querySelectorAll('.field-err')
    .forEach(el => el.textContent = '');
  document.querySelectorAll('input, textarea')
    .forEach(el => el.classList.remove('err'));
}
```

---

## <a id="ui"></a>🎨 Interface e Mensagens

### Mensagem de Sucesso

```javascript
function showSuccess(nome) {
  volunteerForm.style.display = 'none';
  successMsg.style.display = 'block';
  // Volta ao formulário após 5 segundos
  setTimeout(() => resetFormBox(), 5000);
}
```

### Mensagem de Já Inscrito

```javascript
function showAlreadyInscribed(email) {
  alreadyMsg.style.display = 'block';
  // Simula reinscrita automática
}
```

### Cancelar Inscrição

```javascript
cancelBtn.addEventListener('click', () => {
  if (confirm('Tem certeza?')) {
    // Remove do array
    // Salva mudanças
    // Atualiza UI
  }
});
```

---

## <a id="contadores"></a>📊 Contadores Dinâmicos

### Atualizar Contadores

```javascript
function updateCounters() {
  const volunteers = loadVolunteers();
  const count = volunteers.length;
  const percentage = (count / MAX_VOLUNTEERS) * 100;
  
  animateCounter(heroCounter, count);
  animateCounter(formCounter, count);
  vcFill.style.width = percentage + '%';
}
```

### Animação de Números

```javascript
function animateCounter(element, targetValue) {
  const duration = 600; // ms
  const startTime = performance.now();
  const startValue = parseInt(element.textContent) || 0;
  
  function animate(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const value = Math.floor(
      startValue + (targetValue - startValue) * progress
    );
    element.textContent = value;
    
    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }
  
  requestAnimationFrame(animate);
}
```

**O que faz:**
- Transição suave do valor anterior para o novo
- Usa `requestAnimationFrame` para melhor performance
- Duração: 600ms (configurável)

---

## <a id="reveal"></a>👁️ Animações Reveal (Aparecimento)

### Intersection Observer

```javascript
const observerOptions = {
  threshold: 0.1,       // 10% visível
  rootMargin: '0px 0px -100px 0px' // 100px antes do fold
};

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Desativa após animar
      }
    });
  },
  observerOptions
);

document.querySelectorAll('.reveal')
  .forEach((el) => observer.observe(el));
```

**O que faz:**
- Monitora quando elementos `.reveal` entram na viewport
- Adiciona classe `.visible` para ativar animação CSS
- Para de observar após animar (economiza memória)
- Suporta scroll suave em toda a página

---

## <a id="utilitários"></a>🛠️ Funções Utilitárias

### Exportar Dados (CSV)

```javascript
window.exportVolunteerData = function() {
  const volunteers = loadVolunteers();
  const csv = 'Nome,Idade,Email,Turma,...\n' +
    volunteers.map(v => `"${v.nome}",...`).join('\n');
  
  const blob = new Blob([csv], 
    { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'marmita-voluntarios.csv';
  link.click();
}
```

**Uso no Console:**
```javascript
exportVolunteerData()
```

### Limpar Dados (Testes)

```javascript
window.clearAllVoluneers = function() {
  if (confirm('Tem certeza?')) {
    localStorage.removeItem(STORAGE_KEY);
    updateCounters();
    resetFormBox();
  }
}
```

**Uso no Console:**
```javascript
clearAllVoluneers() // ⚠️ Deleta tudo!
```

---

## 🔄 Fluxo Completo de Inscrição

```
1. Usuário preenche formulário
   ↓
2. Clica em "Confirmar minha inscrição"
   ↓
3. JavaScript previne envio padrão (preventDefault)
   ↓
4. Coleta dados do formulário
   ↓
5. Valida cada campo (nome, idade, email, contribuição)
   ↓
6. Se inválido → mostra erros e scroll para cima
   ↓
7. Se válido → verifica email duplicado
   ↓
8. Se duplicado → mostra mensagem "Já inscrito"
   ↓
9. Se novo → verifica limite (50 voluntários)
   ↓
10. Se limite → mostra alerta
    ↓
11. Se OK → salva em localStorage
    ↓
12. Mostra mensagem de sucesso
    ↓
13. Atualiza contadores com animação
    ↓
14. Volta ao formulário vazio após 5 segundos
```

---

## 🎯 Performance & Otimizações

### Técnicas Implementadas

✅ **Intersection Observer** – Evita scroll listeners contínuos  
✅ **requestAnimationFrame** – Animações sincronizadas com tela  
✅ **Event Delegation** – Um listener para múltiplos elementos  
✅ **localStorage** – Sem requisições de rede  
✅ **Memoização** – Reutiliza dados carregados  
✅ **Z-index Management** – Sem conflicts de camadas  

### Tamanho do Script

- **Comprimido:** ~13.3 KB
- **Minificado seria:** ~8-9 KB
- **Gzipped seria:** ~3-4 KB

---

## 📝 Resumo das Funcionalidades

| Funcionalidade | Método | Evento |
|---|---|---|
| Menu toggle | `navToggle.addEventListener` | click |
| Navbar scroll | `window.addEventListener` | scroll |
| Envio form | `volunteerForm.addEventListener` | submit |
| Reveal anim | `IntersectionObserver` | intersection |
| Counter anim | `requestAnimationFrame` | load/update |
| LocalStorage | `localStorage.getItem/setItem` | - |

---

## 🐛 Debugging

### Ver Console
- Abra DevTools (F12)
- Aba "Console"
- Veja mensagens logs

### Comandos Úteis

```javascript
// Ver todos os voluntários
JSON.parse(localStorage.getItem('marmita-voluntarios'))

// Ver quantidade
loadVolunteers().length

// Procurar por email
loadVolunteers().find(v => v.email === 'seu@email.com')

// Deletar tudo
localStorage.clear()
```

---

Desenvolvido para **Marmita Solidária 2026** 💛
