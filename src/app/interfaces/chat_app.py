#!/usr/bin/env python3
"""
Streamlit веб-интерфейс для AI ассистента трейдера

Использование:
    poetry run streamlit run src/app/chat_app.py
    streamlit run src/app/chat_app.py
"""

import json
import datetime

import streamlit as st

from src.app.interfaces.__init__ import *
from src.app.utils import get_asset_from_text
from src.app.adapters import FinamAPIClient
from src.app.core import call_llm, get_settings
from src.app.core.llm import extract_api_request, create_system_prompt


def main() -> None:  # noqa: C901
    """Главная функция Streamlit приложения"""
    initialize_app()
    
    st.set_page_config(
        page_title="AI Трейдер (Finam)", 
        page_icon="🤖", 
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Заголовок
    # Показываем приветственный экран если нет сообщений, иначе обычный интерфейс
    if "messages" not in st.session_state or len(st.session_state.messages) == 0:
        create_welcome_screen()
    else:
    # Показать улучшенный заголовок когда есть история
        st.markdown("""
        <div class="header-container">
            <h1 class="main-header">🤖 AI Ассистент Трейдера</h1>
            <p class="subheader">Режим реального времени • Аналитика • Управление</p>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar с настройками
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <div style="font-size: 2rem;">⚙️</div>
            <h2>Панель управления</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Карточка с моделью
        settings = get_settings()
        st.markdown(f"""
        <div class="sidebar-card">
            <div style="font-size: 0.9rem; opacity: 0.8;">AI Модель</div>
            <div style="font-size: 1.1rem; font-weight: 600;">{settings.openrouter_model}</div>
        </div>
        """, unsafe_allow_html=True)

        # Быстрые действия
        st.markdown("### 🚀 Быстрые действия")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Очистить", use_container_width=True, help="Очистить историю диалога"):
                st.session_state.messages = []
                st.rerun()
        with col2:
            if st.button("🔄 Обновить", use_container_width=True, help="Обновить данные"):
                st.rerun()

        # Настройки API
        with st.expander("🔐 API Настройки", expanded=False):
            api_token = st.text_input(
                "Access Token",
                type="password",
                placeholder="Введите ваш токен...",
            )
            api_base_url = st.text_input("API URL", value="https://api.finam.ru", help="API URL")
            account_id = st.text_input("ID счета", value="", help="Необязательно для заполнения")

        # Статус подключения
        finam_client = FinamAPIClient(access_token=api_token or None, base_url=api_base_url if api_base_url else None)
        
        if not finam_client.access_token:
            st.markdown("""
            <div style="background: rgba(239,68,68,0.2); padding: 0.75rem; border-radius: 10px; border-left: 4px solid #EF4444;">
                <div style="font-weight: 600;">⚠️ API не подключен</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">Введите токен для доступа</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(16,185,129,0.2); padding: 0.75rem; border-radius: 10px; border-left: 4px solid #10B981;">
                <div style="font-weight: 600;">✅ API подключен</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">Доступ к данным активен</div>
            </div>
            """, unsafe_allow_html=True)


        # Быстрые команды
        st.markdown("---")
        st.markdown("### 💬 Быстрые запросы")

        quick_queries = {
            "💰 Цена Сбербанка": "Какая текущая цена акций Сбербанка?",
            "📊 Мой портфель": "Покажи мой инвестиционный портфель и баланс", 
            "🔍 Стакан Газпрома": "Что в стакане по акциям Газпрома?",
            "📈 Свечи YNDX": "Покажи свечной график YNDX за последние 5 дней",
            "⚡ Активные ордера": "Какие у меня активные ордера?",
            "👤 Данные сессии": "Покажи информацию о моей торговой сессии"
        }

        for display_text, actual_query in quick_queries.items():
            if st.button(display_text, use_container_width=True, key=f"quick_{display_text}"):
                # Сразу добавляем запрос в историю сообщений
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": actual_query})
                st.rerun()

        # Статистика (опционально)
        st.markdown("---")
        st.markdown("### 📊 Статистика")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Сообщения", len(st.session_state.get('messages', [])))
        with col2:
            st.metric("Сессия", "Активна" if finam_client.access_token else "Неактивна")


    # Инициализация состояния
    if "messages" not in st.session_state:
        st.session_state.messages = []

        
    # Инициализация Finam API клиента
    finam_client = FinamAPIClient(access_token=api_token or None, base_url=api_base_url if api_base_url else None)

    # Проверка токена
    if not finam_client.access_token:
        st.sidebar.warning(
            "⚠️ Finam API токен не установлен. Установите в переменной окружения FINAM_ACCESS_TOKEN или введите выше."
        )
    else:
        st.sidebar.success("✅ Finam API токен установлен")

    # Отображение истории сообщений
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Показываем API запросы
            if "api_request" in message:
                with st.expander("🔍 API запрос"):
                    st.code(f"{message['api_request']['method']} {message['api_request']['path']}", language="http")
                    st.json(message["api_request"]["response"])


    # Основное поле ввода
    if prompt := st.chat_input("Напишите ваш вопрос..."):
        
        
        # Добавляем сообщение пользователя
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Формируем историю для LLM
        conversation_history = [{"role": "system", "content": create_system_prompt()}]
        for msg in st.session_state.messages:
            conversation_history.append({"role": msg["role"], "content": msg["content"]})

        # Получаем ответ от ассистента
        with st.chat_message("assistant"), st.spinner("Думаю..."):
            try:
                response = call_llm(conversation_history, temperature=0.3)
                assistant_message = response["choices"][0]["message"]["content"]

                # Проверяем API запрос
                method, path = extract_api_request(assistant_message)

                api_data = None
                for _ in range(3):
                    if method is None and path is None:
                        break
                    # Подставляем account_id если есть
                    if account_id and "{account_id}" in path:  # noqa: RUF027
                        path = path.replace("{account_id}", account_id)

                    if "{symbol:" in path:
                        start = path.index("{symbol:") + len("{symbol:")
                        end = path.index("}")
                        name = path[start: end]
                        asset = get_asset_from_text(name, finam_client)
                        path = path.replace(f"{{symbol:{name}}}", asset)

                    # Показываем что делаем запрос
                    st.info(f"🔍 Выполняю запрос: `{method} {path}`")

                    # Выполняем API запрос
                    api_response = finam_client.execute_request(method, path)

                    # Проверяем на ошибки
                    if "error" in api_response:
                        st.error(f"⚠️ Ошибка API: {api_response.get('error')}")
                        if "details" in api_response:
                            st.error(f"Детали: {api_response['details']}")

                    # Показываем результат
                    with st.expander("📡 Ответ API", expanded=False):
                        st.json(api_response)

                    api_data = {"method": method, "path": path, "response": api_response}

                    # Добавляем результат в контекст
                    conversation_history.append({"role": "assistant", "content": assistant_message})
                    conversation_history.append({
                        "role": "user",
                        "content": f"Эндпоинт: {path}\nРезультат API: {json.dumps(api_response, ensure_ascii=False)[:8192]}\n\nПроанализируй.\n Также ты можешь отправить другой запрос.",
                    })

                    # Получаем финальный ответ
                    response = call_llm(conversation_history, temperature=0.3)
                    assistant_message = response["choices"][0]["message"]["content"]

                    method, path = extract_api_request(assistant_message)

                st.markdown(assistant_message)

                # Сохраняем сообщение ассистента
                message_data = {"role": "assistant", "content": assistant_message}
                if api_data:
                    message_data["api_request"] = api_data
                st.session_state.messages.append(message_data)

            except Exception as e:
                st.error(f"❌ Ошибка: {e}")

    create_status_bar()

if __name__ == "__main__":
    main()