"""Пользовательские интерфейсы для AI ассистента трейдера"""

import streamlit as st
from typing import Optional
import time

def setup_purple_theme() -> None:
    """Настройка расширенной фиолетовой темы для Streamlit"""
    
    # Кастомный CSS для фиолетовой темы
    st.markdown("""
    <style>
    /* Основные цвета темы */
    :root {
        --primary: #8B5CF6;
        --primary-dark: #7C3AED;
        --primary-light: #A78BFA;
        --secondary: #C4B5FD;
        --accent: #F59E0B;
        --background: #F8FAFC;
        --surface: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
    }
    
    /* Главный контейнер */
    .main {
        background: var(--background);
    }
    
    /* Верхняя навигационная панель */
    .header-container {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
    }
    
    .main-header {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subheader {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Карточки */
    .feature-card {
        background: var(--surface);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid var(--primary);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
    }
    
    .stat-card {
        background: linear-gradient(135deg, var(--primary-light), var(--secondary));
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: var(--text-primary);
        margin: 0.5rem;
    }
    
    /* Боковая панель */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
    }
    
    .sidebar .sidebar-content * {
        color: white !important;
    }
    
    /* Кнопки */
    .stButton>button {
        background: linear-gradient(45deg, var(--primary), var(--primary-light));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, var(--primary-dark), var(--primary));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
    }
    
    .btn-secondary {
        background: linear-gradient(45deg, var(--secondary), var(--primary-light)) !important;
    }
    
    /* Поля ввода */
    .stTextInput>div>div>input {
        border: 2px solid var(--secondary);
        border-radius: 12px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
    }
    
    /* Чат сообщения */
    .stChatMessage {
        padding: 1.25rem;
        border-radius: 18px;
        margin: 0.75rem 0;
        border: none;
    }
    
    /* Сообщения пользователя */
    .stChatMessage[data-testid="user"] {
        background: linear-gradient(135deg, var(--primary-light), var(--secondary));
        margin-left: 2rem;
    }
    
    /* Сообщения ассистента */
    .stChatMessage[data-testid="assistant"] {
        background: var(--surface);
        margin-right: 2rem;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.1);
        border: 1px solid var(--secondary);
    }
    
    /* Спиннер и индикаторы */
    .stSpinner>div {
        border-color: var(--primary) transparent transparent transparent;
    }
    
    .header-container .emoji {
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    font-size: 3rem !important;
    display: block;
    margin-bottom: 0.5rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .header-container *[role="img"] {
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }

    .status-online {
        background: var(--success);
    }
    
    .status-offline {
        background: var(--error);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--secondary);
        color: var(--text-primary);
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .streamlit-expanderContent {
        background: var(--surface);
        border-radius: 0 0 12px 12px;
        padding: 1rem;
    }
    
    /* Уведомления */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1rem 1.5rem;
    }
    
    .stAlert[data-testid="stInfo"] {
        background: linear-gradient(135deg, #C4B5FD, #DDD6FE);
        color: var(--text-primary);
        border-left: 4px solid var(--primary);
    }
    
    .stAlert[data-testid="stWarning"] {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        color: var(--text-primary);
        border-left: 4px solid var(--warning);
    }
    
    .stAlert[data-testid="stError"] {
        background: linear-gradient(135deg, #FECACA, #FCA5A5);
        color: var(--text-primary);
        border-left: 4px solid var(--error);
    }
    
    .stAlert[data-testid="stSuccess"] {
        background: linear-gradient(135deg, #A7F3D0, #6EE7B7);
        color: var(--text-primary);
        border-left: 4px solid var(--success);
    }
    
    /* Разделитель */
    .stMarkdown hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        margin: 2rem 0;
    }
    
    /* Прогресс бар */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
    }
    
    /* Нижний статус бар */
    .status-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--surface);
        padding: 0.5rem 1rem;
        border-top: 1px solid var(--secondary);
        font-size: 0.8rem;
        color: var(--text-secondary);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Анимации */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Адаптивность */
    @media (max-width: 768px) {
        .header-container {
            padding: 1rem;
            border-radius: 0 0 15px 15px;
        }
        
        .main-header {
            font-size: 2rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

def create_status_bar() -> None:
    """Создать нижнюю статусную панель"""
    st.markdown("""
    <div class="status-bar">
        <div>
            <span class="status-indicator status-online"></span>
            AI Трейдер • 
            <span id="current-time"></span>
        </div>
        <div>
            🤖 Powered by Finam TradeAPI & OpenRouter
        </div>
    </div>
    
    <script>
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = 
                now.toLocaleTimeString('ru-RU');
        }
        setInterval(updateTime, 1000);
        updateTime();
    </script>
    """, unsafe_allow_html=True)

def create_feature_cards() -> None:
    """Создать карточки возможностей"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card fade-in">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="margin: 0 0 0.5rem 0; color: var(--primary);">Анализ рынка</h3>
            <p style="margin: 0; color: var(--text-secondary);">Реальная цена акций, стаканы, графики и технический анализ</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card fade-in">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💼</div>
            <h3 style="margin: 0 0 0.5rem 0; color: var(--primary);">Управление</h3>
            <p style="margin: 0; color: var(--text-secondary);">Портфель, ордера, баланс и история сделок</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card fade-in">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌆</div>
            <h3 style="margin: 0 0 0.5rem 0; color: var(--primary);">AI Ассистент</h3>
            <p style="margin: 0; color: var(--text-secondary);">Интеллектуальный анализ и рекомендации</p>
        </div>
        """, unsafe_allow_html=True)

def create_quick_stats() -> None:
    """Создать быструю статистику"""
    st.markdown("### 📈 Быстрая статистика")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.5rem; font-weight: bold;">50+</div>
            <div>Инструментов</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.5rem; font-weight: bold;">24/7</div>
            <div>Доступность</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.5rem; font-weight: bold;">0.1с</div>
            <div>Задержка API</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 1.5rem; font-weight: bold;">AI</div>
            <div>Аналитика</div>
        </div>
        """, unsafe_allow_html=True)

def show_enhanced_instructions() -> None:
    """Показать улучшенные инструкции"""
    
    st.markdown("""
    <div class="header-container">
        <div class="emoji">🤖</div>
        <h1 class="main-header">🎯 Начните работу с AI Трейдером</h1>
        <p class="subheader">Ваш интеллектуальный помощник для успешной торговли</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Карточки возможностей
    create_feature_cards()
    
    # Быстрая статистика
    create_quick_stats()
    
    # Инструкции в аккордеоне
    with st.expander("🚀 **Быстрый старт**", expanded=True):
        st.markdown("""
        ### 3 простых шага чтобы начать:
        
        1. **🔑 Настройте API доступ** в боковой панели
        2. **💬 Задайте вопрос** в чате ниже
        3. **📊 Анализируйте результаты** с помощью AI
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 Подробная инструкция", use_container_width=True):
                st.session_state.show_detailed_instructions = True
        with col2:
            if st.button("🎯 Примеры запросов", use_container_width=True):
                st.session_state.show_examples = True
    
    if st.session_state.get('show_detailed_instructions'):
        show_detailed_instructions()
    
    if st.session_state.get('show_examples'):
        show_examples_section()

def show_detailed_instructions() -> None:
    """Показать детальные инструкции"""
    st.markdown("---")
    
    tabs = st.tabs(["📋 Настройка", "💬 Общение", "🔧 API", "🚨 Помощь"])
    
    with tabs[0]:
        st.markdown("""
        ### 🔑 Настройка доступа
        
        **Finam API Токен:**
        - Получите токен в личном кабинете Finam
        - Введите его в боковой панели
        - Или установите переменную окружения `FINAM_ACCESS_TOKEN`
        
        **ID Счета:**
        - Укажите для доступа к портфелю
        - Оставьте пустым для просмотра общих данных
        """)
    
    with tabs[1]:
        st.markdown("""
        ### 💬 Эффективное общение
        
        **Лучшие практики:**
        - Используйте конкретные тикеры (SBER, GAZP)
        - Указывайте временные периоды
        - Задавайте четкие вопросы
        
        **Примеры:**
        - ❌ _"Что с акциями?"_
        - ✅ _"Какая цена Сбербанка и динамика за неделю?"_
        """)
    
    with tabs[2]:
        st.markdown("""
        ### 🔍 Работа с API
        
        **Автоматические запросы:**
        - AI сам определяет нужные эндпоинты
        - Показывает сырые данные API
        - Анализирует и структурирует ответ
        
        **Доступные методы:**
        - Получение котировок
        - Анализ портфеля
        - Просмотр ордеров
        - Исторические данные
        """)
    
    with tabs[3]:
        st.markdown("""
        ### 🚨 Решение проблем
        
        **Частые вопросы:**
        
        **Токен не работает:**
        - Проверьте срок действия токена
        - Убедитесь в правильности ввода
        - Проверьте доступы в личном кабинете Finam
        
        **Данные не загружаются:**
        - Проверьте интернет-соединение
        - Убедитесь в работоспособности Finam API
        - Попробуйте другой запрос
        """)

def show_examples_section() -> None:
    """Показать секцию с примерами"""
    st.markdown("---")
    st.markdown("### 💡 Популярные запросы")
    
    examples = [
        {"emoji": "📈", "text": "Какая текущая цена Сбербанка?", "category": "Котировки"},
        {"emoji": "💼", "text": "Покажи мой инвестиционный портфель", "category": "Портфель"},
        {"emoji": "🔍", "text": "Что в стакане по Газпрому?", "category": "Анализ"},
        {"emoji": "📊", "text": "График YNDX за последнюю неделю", "category": "Графики"},
        {"emoji": "⚡", "text": "Мои активные ордера", "category": "Торговля"},
        {"emoji": "🤔", "text": "Найди тикер Лукойла", "category": "Поиск"},
    ]
    
    cols = st.columns(2)
    for idx, example in enumerate(examples):
        with cols[idx % 2]:
            if st.button(
                f"{example['emoji']} {example['text']}",
                help=f"Категория: {example['category']}",
                use_container_width=True
            ):
                st.session_state.example_query = example['text']
                st.rerun()

def create_welcome_screen() -> None:
    """Создать улучшенный приветственный экран"""
    show_enhanced_instructions()
    create_status_bar()

def initialize_app() -> None:
    """Инициализировать приложение с расширенной фиолетовой темой"""
    setup_purple_theme()
    
    # Инициализируем состояние приложения
    if "app_initialized" not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.show_detailed_instructions = False
        st.session_state.show_examples = False

# Экспортируемые функции
__all__ = [
    'setup_purple_theme',
    'create_status_bar',
    'create_feature_cards',
    'create_quick_stats',
    'show_enhanced_instructions',
    'create_welcome_screen',
    'initialize_app'
]