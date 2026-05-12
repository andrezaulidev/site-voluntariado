# 🚀 Estrutura Expandida - Marmita Solidária Backend

## 📁 Estrutura do Projeto

```
backend/
├── run.py                      # Aplicação principal
├── config.py                   # Configurações
├── requirements.txt            # Dependências Python
├── .env.example               # Variáveis de ambiente
│
├── app/
│   ├── __init__.py            # Factory app + extensões
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── user.py           # Usuários (admin, voluntários)
│   │   ├── volunteer.py      # Dados dos voluntários
│   │   ├── checkin.py        # Check-in/Check-out
│   │   └── qrcode_session.py # Sessões de QR code
│   │
│   ├── routes/                # APIs RESTful
│   │   ├── __init__.py
│   │   ├── auth_bp.py        # Autenticação (login, registro)
│   │   ├── volunteers_bp.py  # CRUD voluntários
│   │   ├── admin_bp.py       # Painel administrativo
│   │   └── qrcode_bp.py      # QR code e geolocalização
│   │
│   ├── utils/                 # Utilitários
│   │   ├── __init__.py
│   │   └── geolocation.py    # Cálculo de distâncias (Haversine)
│   │
│   ├── templates/             # HTML
│   │   └── dashboard.html    # Dashboard administrativo
│   │
│   └── static/                # CSS, JS, imagens
```

---

## ✨ Funcionalidades Implementadas

### 1️⃣ **Autenticação (JWT)**
- ✅ Registro de usuários
- ✅ Login com geração de token JWT
- ✅ Verificação de senha com hash (Werkzeug)
- ✅ Mudança de senha
- ✅ Roles: admin, volunteer, coordinator

### 2️⃣ **Banco de Dados (SQLite)**

**Users** (Usuários)
- id, name, email, password_hash, role, is_active
- email_verified, created_at, last_login

**Volunteers** (Dados de voluntários)
- Dados pessoais (age, phone, class_year)
- Contribuições (contributions array)
- Geolocalização (latitude, longitude, address)
- Status (enrolled, confirmed, attended, cancelled)
- Horas contribuídas

**CheckIn** (Presença via QR code)
- user_id, session_id
- check_in_time, check_out_time
- Horas trabalhadas calculadas
- Localização no momento do check-in

**QRCodeSession** (Eventos)
- Nome, descrição, data/hora
- Localização (lat, lon)
- Token de QR code único
- Contador de presentes

### 3️⃣ **APIs RESTful**

#### Auth
- `POST /api/auth/register` - Novo usuário
- `POST /api/auth/login` - Login + JWT
- `GET /api/auth/me` - Dados do usuário atual
- `POST /api/auth/change-password` - Alterar senha

#### Volunteers
- `GET /api/volunteers` - Listar voluntários
- `GET /api/volunteers/<id>` - Dados específicos
- `POST /api/volunteers` - Criar/atualizar perfil
- `GET /api/volunteers/stats/summary` - Estatísticas
- `GET /api/volunteers/geolocation` - Mapa com geolocalização

#### Admin
- `GET /api/admin/dashboard` - Dados do dashboard
- `GET /api/admin/users` - Gerenciar usuários
- `POST /api/admin/users/<id>/toggle-active` - Ativar/desativar
- `GET /api/admin/sessions` - Gerenciar sessões
- `POST /api/admin/sessions` - Criar nova sessão
- `GET /api/admin/reports/volunteers` - Exportar CSV
- `GET /api/admin/reports/checkins` - Exportar CSV

#### QR Code
- `GET /api/qrcode/sessions/<id>/qrcode` - Gerar imagem QR
- `POST /api/qrcode/checkin` - Check-in com validação GPS
- `POST /api/qrcode/checkout` - Check-out
- `GET /api/qrcode/sessions/<id>/checkins` - Histórico

### 4️⃣ **Geolocalização**

- ✅ Cálculo de distância (Haversine formula)
- ✅ Validação de GPS (máx 100m do local)
- ✅ Mapa com todos os voluntários
- ✅ Check-in/out com localização automática

### 5️⃣ **QR Code**

- ✅ Geração dinâmica de QR codes
- ✅ Tokens únicos por sessão
- ✅ Validação de token + GPS
- ✅ Check-in/out automático
- ✅ Cálculo de horas trabalhadas

### 6️⃣ **Emails Automáticos**

- ✅ Boas-vindas (welcome)
- ✅ Confirmação de inscrição
- ✅ Lembretes de eventos
- ✅ Relatórios de participação
- ✅ Configurável via .env

### 7️⃣ **Dashboard Administrativo**

- ✅ Estatísticas em tempo real
- ✅ Gerenciamento de voluntários
- ✅ Gerenciamento de usuários
- ✅ Criação de sessões de QR code
- ✅ Exportação de relatórios em CSV
- ✅ Aba de sessões e check-ins

---

## 🚀 Como Configurar

### 1. Instalar dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar variáveis

```bash
cp .env.example .env
# Editar .env com suas configurações
```

### 3. Inicializar banco

```bash
FLASK_APP=run.py flask init-db
```

### 4. Seed dados de teste

```bash
FLASK_APP=run.py flask seed-db
```

### 5. Iniciar servidor

```bash
python run.py
```

Será disponível em: `http://localhost:5000`

---

## 📡 Usando as APIs

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d {
    "email": "admin@marmita.local",
    "password": "admin123"
  }
```

Retorna:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "name": "Admin",
    "email": "admin@marmita.local",
    "role": "admin"
  }
}
```

### Criar Voluntário

```bash
curl -X POST http://localhost:5000/api/volunteers \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d {
    "age": 17,
    "phone": "11999999999",
    "class_year": "2º ano B",
    "contributions": ["arrecadar", "preparar"],
    "latitude": -23.5505,
    "longitude": -46.6333
  }
```

### Check-in com QR Code

```bash
curl -X POST http://localhost:5000/api/qrcode/checkin \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d {
    "qrcode_token": "...",
    "latitude": -23.5505,
    "longitude": -46.6333
  }
```

---

## 🔐 Segurança

- ✅ Senhas com hash (Werkzeug)
- ✅ JWT para autenticação
- ✅ CORS configurado
- ✅ Validação de entrada
- ✅ Geolocalização para fraude
- ✅ Roles e permissões

---

## 📊 Próximos Passos

- [ ] Dashboard HTML/CSS completo
- [ ] Integração com Google Maps
- [ ] Mobile app com React/Flutter
- [ ] Integração com plataforma de pagamento
- [ ] System de certificados
- [ ] Notificações push
- [ ] Analytics avançado

---

## 📖 Documentação Adicional

Ver [DOCUMENTACAO_API.md](../DOCUMENTACAO_API.md) para referência completa das APIs.

---

_Desenvolvido para Marmita Solidária 2026 💛_
