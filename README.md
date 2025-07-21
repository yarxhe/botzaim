# 💰 Telegram Debt Tracker Bot

<div align="center">

![Bot Photo](static/bot_photo.jpg)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26a5e4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/dolgovoi69bot)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003b57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

### 🌐 Language
[![EN](https://img.shields.io/badge/🇺🇸-English-blue?style=for-the-badge)](#english-version)
[![RU](https://img.shields.io/badge/🇷🇺-Русский-red?style=for-the-badge)](#русская-версия)

</div>

---

## Русская-версия

### 📋 Описание

Простой, но мощный Telegram-бот для отслеживания личных долгов и дебиторской задолженности. Помогает не забыть, кому должны вы и кто должен вам.

### ✨ Основные функции

- 🔄 **Двусторонний учет**: Отслеживайте как свои долги (`Я должен`), так и долги вам (`Мне должны`)
- 💳 **Гибкое погашение**: Закрывайте долги полностью или вносите частичные платежи
- ⏰ **Автоматические уведомления**: Ежедневные проверки и напоминания за 3 дня до срока погашения
- 🎯 **Интуитивный интерфейс**: Вся навигация через удобные инлайн-кнопки
- 📊 **Детальная статистика**: Общие суммы и подробности по каждому должнику
- 💾 **Надежное хранение**: База данных SQLite с автоматическим резервным копированием

### 🏗️ Структура проекта

```
debt-bot/
├── 📄 .dockerignore
├── 📋 .env.example        # Шаблон переменных окружения
├── 🚫 .gitignore
├── 🗄️ debts.db           # База данных SQLite
├── 🐳 dockerfile
├── 🚀 main.py             # Точка входа
├── 📦 requirements.txt
├── 📖 README.md
├── 📁 src/
│   ├── ⚙️ config.py       # Конфигурация
│   ├── 🗄️ database.py     # Работа с БД
│   ├── 🎮 handlers.py     # Обработчики команд
│   ├── ⌨️ keyboards.py    # Клавиатуры
│   └── ⏱️ scheduler.py    # Планировщик задач
└── 🖼️ static/
    ├── bot_photo.jpg
    ├── photo_receivable.jpg
    └── photo_dolg.jpg
```

### 🚀 Установка и запуск

#### 📋 Предварительные требования

- 🐍 Python 3.10+
- 🔧 Git
- 🐳 Docker и Docker Compose (для контейнеризации)

#### 🖥️ Локальный запуск

<details>
<summary>👆 Нажмите для развертывания инструкций</summary>

1. **Клонирование репозитория:**
   ```bash
   git clone <https://github.com/yarxhe/botzaim.git>
   cd debt-bot
   ```

2. **Создание виртуального окружения:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройка окружения:**
   ```bash
   cp .env.example .env
   # Отредактируйте .env и добавьте ваш BOT_TOKEN
   ```

5. **Запуск:**
   ```bash
   python main.py
   ```

</details>

#### 🐳 Docker-запуск (Рекомендуется)

<details>
<summary>👆 Нажмите для развертывания инструкций</summary>

1. **Подготовка:**
   ```bash
   git clone <https://github.com/yarxhe/botzaim.git>
   cd debt-bot
   cp .env.example .env
   # Отредактируйте .env
   ```

2. **Сборка образа:**
   ```bash
   docker build -t debt-tracker-bot .
   ```

3. **Запуск контейнера:**
   ```bash
   docker run -d --name my-debt-bot \
     --env-file .env \
     -v "$(pwd)/debts.db:/app/debts.db" \
     debt-tracker-bot
   ```

4. **Управление контейнером:**
   ```bash
   # Просмотр логов
   docker logs -f my-debt-bot
   
   # Остановка
   docker stop my-debt-bot
   
   # Перезапуск
   docker restart my-debt-bot
   ```

</details>

### 💻 Использование

1. 🔍 Найдите вашего бота в Telegram
2. 🚀 Отправьте `/start` для активации главного меню
3. 🎮 Используйте инлайн-кнопки для навигации
4. ➕ Добавляйте и управляйте долгами через интуитивный интерфейс

### 🛠️ Технологический стек

- **Backend**: Python 3.10+
- **Bot Framework**: python-telegram-bot
- **Database**: SQLite
- **Deployment**: Docker
- **Scheduler**: APScheduler

---

## English-version

### 📋 Description

A simple yet powerful Telegram bot for tracking personal debts and receivables. Never forget who owes you money and whom you owe.

### ✨ Key Features

- 🔄 **Bilateral Tracking**: Monitor both your debts (`I Owe`) and money owed to you (`Owed to Me`)
- 💳 **Flexible Payments**: Close debts completely or make partial payments
- ⏰ **Smart Notifications**: Daily checks with reminders 3 days before due dates
- 🎯 **Intuitive Interface**: Complete navigation through convenient inline buttons
- 📊 **Detailed Analytics**: Total amounts and details for each debtor/creditor
- 💾 **Reliable Storage**: SQLite database with automatic backup

### 🏗️ Project Structure

```
debt-bot/
├── 📄 .dockerignore
├── 📋 .env.example        # Environment variables template
├── 🚫 .gitignore
├── 🗄️ debts.db           # SQLite database
├── 🐳 dockerfile
├── 🚀 main.py             # Application entry point
├── 📦 requirements.txt
├── 📖 README.md
├── 📁 src/
│   ├── ⚙️ config.py       # Configuration
│   ├── 🗄️ database.py     # Database operations
│   ├── 🎮 handlers.py     # Command handlers
│   ├── ⌨️ keyboards.py    # Keyboards
│   └── ⏱️ scheduler.py    # Task scheduler
└── 🖼️ static/
    ├── bot_photo.jpg
    ├── photo_receivable.jpg
    └── photo_dolg.jpg
```

### 🚀 Installation & Setup

#### 📋 Prerequisites

- 🐍 Python 3.10+
- 🔧 Git
- 🐳 Docker and Docker Compose (for containerization)

#### 🖥️ Local Development

<details>
<summary>👆 Click to expand instructions</summary>

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/yarxhe/botzaim.git>
   cd debt-bot
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup:**
   ```bash
   cp .env.example .env
   # Edit .env and add your BOT_TOKEN
   ```

5. **Run the bot:**
   ```bash
   python main.py
   ```

</details>

#### 🐳 Docker Deployment (Recommended)

<details>
<summary>👆 Click to expand instructions</summary>

1. **Preparation:**
   ```bash
   git clone <https://github.com/yarxhe/botzaim.git>
   cd debt-bot
   cp .env.example .env
   # Edit .env file
   ```

2. **Build image:**
   ```bash
   docker build -t debt-tracker-bot .
   ```

3. **Run container:**
   ```bash
   docker run -d --name my-debt-bot \
     --env-file .env \
     -v "$(pwd)/debts.db:/app/debts.db" \
     debt-tracker-bot
   ```

4. **Container management:**
   ```bash
   # View logs
   docker logs -f my-debt-bot
   
   # Stop container
   docker stop my-debt-bot
   
   # Restart container
   docker restart my-debt-bot
   ```

</details>

### 💻 Usage

1. 🔍 Find your bot in Telegram
2. 🚀 Send `/start` to activate the main menu
3. 🎮 Use inline buttons for navigation
4. ➕ Add and manage debts through the intuitive interface

### 🛠️ Tech Stack

- **Backend**: Python 3.10+
- **Bot Framework**: python-telegram-bot
- **Database**: SQLite
- **Deployment**: Docker
- **Scheduler**: APScheduler

---

<div align="center">

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


### 🐛 Issues

Found a bug? Please create an issue [here](https://github.com/yarxhe/botzaim/issues).

---

**Made with ❤️ for better debt management**

</div>
