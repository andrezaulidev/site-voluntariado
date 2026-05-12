/* ═══════════════════════════════════════════════════════
   MARMITA SOLIDÁRIA · script.js
   Funcionalidades: Menu responsivo, Formulário, localStorage, Animações
═══════════════════════════════════════════════════════ */

/* ── Constantes e seletores ── */
const STORAGE_KEY = 'marmita-voluntarios';
const MAX_VOLUNTEERS = 50;

// Elementos da navbar
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
const navLinksArray = navLinks.querySelectorAll('a');

// Elementos do formulário
const volunteerForm = document.getElementById('volunteerForm');
const formBox = document.getElementById('formBox');
const alreadyMsg = document.getElementById('alreadyMsg');
const successMsg = document.getElementById('successMsg');
const cancelBtn = document.getElementById('cancelBtn');

// Contadores
const heroCounter = document.getElementById('heroCounter');
const formCounter = document.getElementById('formCounter');
const vcFill = document.getElementById('vcFill');

/* ════════════════════════════════════════
   1. NAVBAR · ScrollEffect + MenuToggle
════════════════════════════════════════ */

// Efeito de navbar ao scroll
window.addEventListener('scroll', () => {
  if (window.scrollY > 20) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// Toggle menu responsivo
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  // Animar ícones (hamburger → X)
  const spans = navToggle.querySelectorAll('span');
  if (navLinks.classList.contains('open')) {
    spans[0].style.transform = 'rotate(45deg) translateY(12px)';
    spans[1].style.opacity = '0';
    spans[2].style.transform = 'rotate(-45deg) translateY(-10px)';
  } else {
    spans[0].style.transform = '';
    spans[1].style.opacity = '';
    spans[2].style.transform = '';
  }
});

// Fechar menu ao clicar em um link
navLinksArray.forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    const spans = navToggle.querySelectorAll('span');
    spans.forEach(span => span.style.transform = '');
    spans[1].style.opacity = '';
  });
});

/* ════════════════════════════════════════
   2. localStorage · Gerenciar Inscrições
════════════════════════════════════════ */

// Carregar voluntários do localStorage
function loadVolunteers() {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
}

// Salvar voluntários no localStorage
function saveVolunteers(volunteers) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(volunteers));
}

// Verificar se email já existe
function emailExists(email) {
  const volunteers = loadVolunteers();
  return volunteers.some(v => v.email.toLowerCase() === email.toLowerCase());
}

// Recuperar dados de um email
function getVolunteerByEmail(email) {
  const volunteers = loadVolunteers();
  return volunteers.find(v => v.email.toLowerCase() === email.toLowerCase());
}

/* ════════════════════════════════════════
   3. FORMULÁRIO · Validação
════════════════════════════════════════ */

// Limpar mensagens de erro
function clearErrors() {
  document.querySelectorAll('.field-err').forEach(el => el.textContent = '');
  document.querySelectorAll('input, textarea').forEach(el => el.classList.remove('err'));
}

// Validar formulário
function validateForm(data) {
  clearErrors();
  let isValid = true;

  // Validar nome
  if (!data.nome.trim()) {
    document.getElementById('err-nome').textContent = '✗ Nome é obrigatório';
    document.getElementById('nome').classList.add('err');
    isValid = false;
  } else if (data.nome.trim().length < 3) {
    document.getElementById('err-nome').textContent = '✗ Nome deve ter pelo menos 3 caracteres';
    document.getElementById('nome').classList.add('err');
    isValid = false;
  }

  // Validar idade
  if (!data.idade) {
    document.getElementById('err-idade').textContent = '✗ Idade é obrigatória';
    document.getElementById('idade').classList.add('err');
    isValid = false;
  } else if (data.idade < 10 || data.idade > 99) {
    document.getElementById('err-idade').textContent = '✗ Idade deve estar entre 10 e 99';
    document.getElementById('idade').classList.add('err');
    isValid = false;
  }

  // Validar email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!data.email) {
    document.getElementById('err-email').textContent = '✗ E-mail é obrigatório';
    document.getElementById('email').classList.add('err');
    isValid = false;
  } else if (!emailRegex.test(data.email)) {
    document.getElementById('err-email').textContent = '✗ E-mail inválido';
    document.getElementById('email').classList.add('err');
    isValid = false;
  }

  // Validar contribuição
  const checkboxes = document.querySelectorAll('input[name="contribuicao"]');
  const hasChecked = Array.from(checkboxes).some(cb => cb.checked);
  if (!hasChecked) {
    document.getElementById('err-contrib').textContent = '✗ Escolha ao menos uma forma de contribuir';
    isValid = false;
  }

  return isValid;
}

/* ════════════════════════════════════════
   4. ENVIO DO FORMULÁRIO
════════════════════════════════════════ */

// Submeter formulário
volunteerForm.addEventListener('submit', (e) => {
  e.preventDefault();

  // Coletar dados
  const formData = {
    nome: document.getElementById('nome').value,
    idade: parseInt(document.getElementById('idade').value),
    email: document.getElementById('email').value,
    turma: document.getElementById('turma').value || 'Não informado',
    contribuicao: Array.from(
      document.querySelectorAll('input[name="contribuicao"]:checked')
    ).map(cb => cb.value),
    obs: document.getElementById('obs').value,
    timestamp: new Date().toLocaleString('pt-BR')
  };

  // Validar
  if (!validateForm(formData)) {
    // Rolar até a seção de erro
    volunteerForm.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    return;
  }

  // Verificar se já existe
  if (emailExists(formData.email)) {
    showAlreadyInscribed(formData.email);
    formBox.scrollIntoView({ behavior: 'smooth' });
    return;
  }

  // Verificar limite
  const volunteers = loadVolunteers();
  if (volunteers.length >= MAX_VOLUNTEERS) {
    alert('😔 Desculpe! Já atingimos o limite de ' + MAX_VOLUNTEERS + ' voluntários. Mas continuamos recebendo manifestações de interesse!');
    return;
  }

  // Enviar para Formspree
  const formDataToSend = new FormData();
  formDataToSend.append('nome', formData.nome);
  formDataToSend.append('idade', formData.idade);
  formDataToSend.append('email', formData.email);
  formDataToSend.append('turma', formData.turma);
  formDataToSend.append('contribuicao', formData.contribuicao.join(', '));
  formDataToSend.append('obs', formData.obs);

  fetch('https://formspree.io/f/xgodddog', {
    method: 'POST',
    body: formDataToSend
  })
  .then(response => {
    if (response.ok) {
      // Salvar nova inscrição no localStorage
      volunteers.push(formData);
      saveVolunteers(volunteers);

      // Mostrar sucesso
      showSuccess(formData.nome);
      updateCounters();
    } else {
      alert('Erro ao enviar formulário. Tente novamente.');
    }
  })
  .catch(error => {
    console.error('Erro:', error);
    alert('Erro de conexão. Tente novamente.');
  });
});

/* ════════════════════════════════════════
   5. UI · Mensagens de Sucesso/Já Inscrito
════════════════════════════════════════ */

// Mostrar mensagem de sucesso
function showSuccess(nome) {
  volunteerForm.reset();
  clearErrors();
  volunteerForm.style.display = 'none';
  successMsg.style.display = 'block';
  document.getElementById('successName').textContent = `Obrigado, ${nome}! 🎉`;
  
  // Scroll suave para a mensagem
  setTimeout(() => {
    successMsg.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 300);

  // Voltar ao formulário depois de 5 segundos
  setTimeout(() => {
    resetFormBox();
  }, 5000);
}

// Mostrar mensagem de já inscrito
function showAlreadyInscribed(email) {
  const volunteer = getVolunteerByEmail(email);
  formBox.style.display = 'none';
  alreadyMsg.style.display = 'block';
  if (volunteer) {
    document.getElementById('alreadyName').textContent = 
      `Obrigado por se inscrever, ${volunteer.nome}! Sua vaga está garantida. 💛`;
  }
}

// Botão para cancelar inscrição
cancelBtn.addEventListener('click', () => {
  const email = getVolunteerByEmail(
    document.getElementById('email').value
  )?.email;
  
  if (email) {
    if (confirm(`Tem certeza que deseja cancelar sua inscrição?`)) {
      let volunteers = loadVolunteers();
      volunteers = volunteers.filter(v => v.email !== email);
      saveVolunteers(volunteers);
      updateCounters();
      resetFormBox();
      alert('✓ Inscrição cancelada com sucesso.');
    }
  }
});

// Resetar formulário para estado inicial
function resetFormBox() {
  formBox.style.display = 'block';
  volunteerForm.style.display = 'block';
  alreadyMsg.style.display = 'none';
  successMsg.style.display = 'none';
  volunteerForm.reset();
  clearErrors();
}

/* ════════════════════════════════════════
   6. COUNTER · Atualizar Contadores
════════════════════════════════════════ */

// Atualizar contadores
function updateCounters() {
  const volunteers = loadVolunteers();
  const count = volunteers.length;
  const percentage = (count / MAX_VOLUNTEERS) * 100;

  // Animar contador
  animateCounter(heroCounter, count);
  animateCounter(formCounter, count);

  // Atualizar barra de progresso
  vcFill.style.width = percentage + '%';
}

// Animar contador com efeito de transição
function animateCounter(element, targetValue) {
  const duration = 600; // ms
  const startTime = performance.now();
  const startValue = parseInt(element.textContent) || 0;

  function animate(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const value = Math.floor(startValue + (targetValue - startValue) * progress);
    element.textContent = value;

    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }

  requestAnimationFrame(animate);
}

// Verificar se há voluntário pré-inscrito
function checkPreFilledVolunteer() {
  const email = document.getElementById('email').value;
  if (email && emailExists(email)) {
    showAlreadyInscribed(email);
  }
}

/* ════════════════════════════════════════
   7. REVEAL · Animar elementos com Scroll
════════════════════════════════════════ */

// Intersection Observer para animações reveal
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Desobservar após animar (otimização)
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observar todos os elementos com classe 'reveal'
document.querySelectorAll('.reveal').forEach((el) => {
  observer.observe(el);
});

/* ════════════════════════════════════════
   8. INICIALIZAÇÃO
════════════════════════════════════════ */

// Inicializar na carga
document.addEventListener('DOMContentLoaded', () => {
  updateCounters();
});

// Monitorar mudanças no email todo segundo (para UX melhor)
document.getElementById('email').addEventListener('blur', checkPreFilledVolunteer);

/* ════════════════════════════════════════
   9. UTILITÁRIOS
════════════════════════════════════════ */

// Função para exportar dados (útil para admin)
window.exportVolunteerData = function() {
  const volunteers = loadVolunteers();
  const csv = 'Nome,Idade,Email,Turma,Contribuição,Observações,Data\n' +
    volunteers.map(v => 
      `"${v.nome}","${v.idade}","${v.email}","${v.turma}","${v.contribuicao.join('; ')}","${v.obs}","${v.timestamp}"`
    ).join('\n');
  
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  const url = URL.createObjectURL(blob);
  link.setAttribute('href', url);
  link.setAttribute('download', 'marmita-voluntarios.csv');
  link.click();
  console.log('📥 Dados exportados com sucesso!');
};

// Função para limpar dados (apenas para testes)
window.clearAllVoluneers = function() {
  if (confirm('⚠️ Tem certeza? Isso vai deletar todos os dados de inscritos.')) {
    localStorage.removeItem(STORAGE_KEY);
    updateCounters();
    resetFormBox();
    console.log('🗑️  Dados limpos!');
  }
};

console.log('✅ Script carregado com sucesso! Marmita Solidária 2026');
