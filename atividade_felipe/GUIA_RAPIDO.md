# 🚀 GUIA RÁPIDO · Marmita Solidária 2026

## ✨ O que foi criado/melhorado

### ✅ Arquivo script.js (13 KB)
Funcionalidades JavaScript completas:

```
├─ 🎯 Menu Responsivo
│  ├─ Toggle hamburger (mobile)
│  ├─ Navegação com links
│  └─ Efeito navbar ao scroll
│
├─ 📝 Formulário Inteligente
│  ├─ Validação de todos os campos
│  ├─ Mensagens de erro personalizadas
│  ├─ Verificação de email duplicado
│  └─ Feedback visual
│
├─ 💾 localStorage
│  ├─ Salva inscrições de voluntários
│  ├─ Limite: 50 voluntários
│  ├─ Persiste no navegador
│  └─ Sem recarregar página
│
├─ 📊 Contador Dinâmico
│  ├─ Animação de números
│  ├─ Barra de progresso
│  ├─ Atualização em tempo real
│  └─ Mostrado em 2 seções
│
├─ 👁️ Reveal Animations
│  ├─ IntersectionObserver otimizado
│  ├─ Elementos aparecem ao scroll
│  ├─ Zero scroll listeners
│  └─ Performance garantida
│
└─ 🛠️ Funções Extras
   ├─ exportVolunteerData() → CSV
   ├─ clearAllVoluneers() → limpar tudo
   └─ Debugging no console
```

---

## 🎨 CSS Otimizado

✅ **Acessibilidade**
- focus-visible em todos os interativos
- prefers-reduced-motion respeitado
- Contraste de cores verificado

✅ **Performance**
- will-change nas animações
- Cubic-bezier otimizado
- Hardware acceleration

✅ **Responsividade**
- 3 breakpoints principais
- Mobile-first approach
- Touch-friendly

---

## 📱 Como Usar o Site

### 1. Abrir
```bash
python3 -m http.server 8000
# http://localhost:8000
```

### 2. Menu Responsivo
- **Desktop**: Links sempre visíveis
- **Mobile**: Clique no ☰ (hamburger)
- Links fecham o menu automaticamente

### 3. Preencher Formulário
```
Nome completo *
Idade * (10-99)
E-mail * (deve ser único)
Turma (opcional)
Como contribuir * (escolha 1+)
Observações (opcional)
```

### 4. Após Enviar
✅ Se novo → Sucesso + volta em 5s
⚠️ Se duplicado → Mostra msg + opção cancelar

### 5. Verificar Inscrições
Console do navegador (F12):
```javascript
// Ver todos
JSON.parse(localStorage.getItem('marmita-voluntarios'))

// Exportar CSV
exportVolunteerData()

// Limpar tudo
clearAllVoluneers()
```

---

## 🎯 Funcionalidades Por Seção

### 🏠 Hero
- Animação de blobs
- Contador de voluntários
- Botões CTA

### 📚 Voluntariado
- Cards informativos
- Texto com contexto global
- Animações ao scroll

### 🌍 Causa
- Estatísticas (70.3mi, 21mi, 1 em 3)
- Dados sobre insegurança alimentar
- Citação inspiradora

### 📋 Projeto
- Grid com detalhes
- Timeline interativa
- Meta e público-alvo

### 📝 Formulário
- Validação completa
- localStorage automático
- Mensagens personalizadas
- Contador em tempo real

### 👨‍💻 Desenvolvedor
- Seu nome: André Zauli
- Turma, data, tecnologias
- Sobre o localStorage

### 🔗 Footer
- Brand info
- Citação do projeto
- Créditos

---

## 🎓 Tecnologias

| Tech | Uso |
|------|-----|
| HTML5 | Semântica, accessibility |
| CSS3 | Layout, animations, responsive |
| JavaScript | Interatividade, validações |
| localStorage | Persistência de dados |
| SVG | Gráficos vetoriais |
| Google Fonts | Tipografia elegante |

---

## 📊 Estrutura localStorage

```json
{
  "marmita-voluntarios": [
    {
      "nome": "José Silva",
      "idade": 17,
      "email": "jose@email.com",
      "turma": "2º ano A",
      "contribuicao": ["arrecadar", "distribuir"],
      "obs": "Disponível sábado",
      "timestamp": "12/05/2026, 14:30:00"
    }
  ]
}
```

---

## ✅ Validações Implementadas

| Campo | Validação |
|-------|-----------|
| Nome | Obrigatório, mín 3 caracteres |
| Idade | Obrigatória, 10-99 anos |
| Email | Obrigatório, formato válido, único |
| Contribuição | Obrigatório, mín 1 opção |
| Obs | Opcional |

---

## 🎨 Design System

### Cores
- 🟠 Laranja: `#F97316` (primária)
- 🔵 Azul: `#1e3a8a` (secundária)
- ⚪ Branco: `#ffffff` (neutro)
- 🟤 Warm BG: `#fff9f5` (fundo)

### Fontes
- Titles: Playfair Display (serif)
- Body: Nunito Sans (sans-serif)

### Radius
- Padrão: 16px
- Buttons: 50px
- Subtle: 10px

### Shadows
- Normal: `0 4px 24px rgba(0,0,0,0.10)`
- Grande: `0 12px 48px rgba(0,0,0,0.15)`

---

## 📈 Performance

| Item | Tamanho |
|------|---------|
| HTML | 23.88 KB |
| CSS | 23.11 KB |
| JS | 13.32 KB |
| **Total** | **60.31 KB** |
| Minificado | ~45 KB |
| Gzipped | ~15 KB |

**Tempo de carregamento:** < 1s (em boa conexão)

---

## 🔧 Extensões Possíveis

- [ ] Backend (Node/Python) para banco de dados
- [ ] Envio de email aos inscritos
- [ ] Dashboard administrativo
- [ ] Autenticação de usuários
- [ ] Sistema de avaliações
- [ ] Galeria de fotos do evento
- [ ] Chat de voluntários
- [ ] Geolocalização
- [ ] QR code para check-in

---

## 🆘 Troubleshooting

### Formulário não funciona
- F12 → Console → verificar erros
- Testar em outro navegador
- Limpar cache (Ctrl+Shift+Del)

### localStorage não salva
- Verificar se cookies habilitados
- Testar em modo privado
- Limpar dados do site

### Menu não abre (mobile)
- Recarregar página
- Limpar cache do navegador
- Testar em outro dispositivo

### Contador não atualiza
- Recarregar página
- Verificar localStorage (F12 → Application)
- Testar function: `updateCounters()`

---

## 📞 Contato & Suporte

**Desenvolvido por:** André Zauli  
**Ano:** 2026  
**Projeto:** Marmita Solidária  
**Escola:** Paulo de Tarso

---

## 🎉 Status do Projeto

```
[████████████████████] 100% Completo

✅ HTML5 Semântico
✅ CSS3 Responsivo
✅ JavaScript Funcional
✅ Acessibilidade
✅ Performance
✅ Documentação
✅ Testado
```

---

_Desenvolvido com ❤️ para fazer diferença._
