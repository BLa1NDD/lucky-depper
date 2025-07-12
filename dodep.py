import streamlit as st, json, time, random, os, uuid



st.set_page_config(
    page_title="Lucky Depper",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Принудительно показываем сайдбар
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
    }
    .css-1d391kg {
        display: block !important;
    }
    
    /* CSS для анимации горизонтальной спирали */
    @keyframes wave {
        0%, 100% { transform: translateY(0px); }
        25% { transform: translateY(-5px); }
        75% { transform: translateY(5px); }
    }
    
    .horizontal-spiral {
        display: inline-block;
        width: 30px;
        height: 8px;
        margin-left: 10px;
        position: relative;
    }
    
    .spiral-dot {
        width: 6px;
        height: 6px;
        background: #3498db;
        border-radius: 50%;
        position: absolute;
        animation: wave 1.5s ease-in-out infinite;
    }
    
    .spiral-dot:nth-child(1) { left: 0px; animation-delay: 0s; }
    .spiral-dot:nth-child(2) { left: 8px; animation-delay: 0.1s; }
    .spiral-dot:nth-child(3) { left: 16px; animation-delay: 0.2s; }
    .spiral-dot:nth-child(4) { left: 24px; animation-delay: 0.3s; }
    
    /* CSS для анимации вращающегося колеса */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .spinning-wheel {
        display: inline-block;
        width: 150px;
        height: 150px;
        border: 18px solid #e0e0e0;
        border-top: 18px solid #ff6b6b;
        border-right: 18px solid #4ecdc4;
        border-bottom: 18px solid #45b7d1;
        border-left: 18px solid #96ceb4;
        border-radius: 50%;
        margin: 15px auto;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Инициализация сессии только если её нет


if "show_toast_until" not in st.session_state:
    st.session_state.show_toast_until = 0
if "last_toast_message" not in st.session_state:
    st.session_state.last_toast_message = ""
if "last_toast_icon" not in st.session_state:
    st.session_state.last_toast_icon = ""
if "show_register" not in st.session_state:
    st.session_state.show_register = False
if "show_spinning_animation" not in st.session_state:
    st.session_state.show_spinning_animation = False
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

def generate_user_id():
    #Создает уникальный ID для пользователя
    return str(uuid.uuid4())

def save_user_to_file(user_id, login, password, balance=1000.0):
    """Сохраняет пользователя в отдельный файл"""
    user_data = {
        "id": user_id,
        "login": login,
        "password": password,
        "balance": balance,
        "last_login": False
    }
    filename = f"user_{user_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)

def load_user_from_file(user_id):
    """Загружает пользователя из файла по ID"""
    filename = f"user_{user_id}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def find_user_by_login(login):
    """Ищет пользователя по логину среди всех файлов"""
    for filename in os.listdir("."):
        if filename.startswith("user_") and filename.endswith(".json"):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    if user_data.get("login") == login:
                        return user_data
            except:
                continue
    return None

def main_game(current_user):
    global stavka
    
    # Очищаем контейнер для надежного скрытия формы логина
    st.empty()
    
    st.title("🎰 Lucky Depper")

    # Создаем сайдбар
    st.sidebar.title("🎰 Lucky Depper")
    st.sidebar.header("Профиль")

    # Информация о пользователе
    st.sidebar.write(f"👤 Пользователь: {current_user['login']}")
    st.sidebar.write(f"💰 Баланс: {float(current_user['balance'])}")

    # Кнопка выхода из аккаунта
    if st.sidebar.button("🚪 Выйти из аккаунта"):
        current_user["last_login"] = False
        save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"])
        # Очищаем session_state
        if hasattr(st.session_state, 'user_logged_in'):
            del st.session_state.user_logged_in
        if hasattr(st.session_state, 'logged_in_user'):
            del st.session_state.logged_in_user
        st.rerun()

    # Разделитель
    st.sidebar.divider()

    # Дополнительные настройки
    st.sidebar.subheader("Статистика")
    st.sidebar.write("🎯 Вероятности выигрыша:")
    st.sidebar.write("• 1 - 1.5x = 40%")
    st.sidebar.write("• 5 - 2x = 20%") 
    st.sidebar.write("• 10 - 2.5x = 10%")
    st.sidebar.write("• К - 3x = 5%")
    st.sidebar.write("• З - 5x = 1%")

    options = ["1", "5", "10", "К", "З"]

    user_dep = st.selectbox("Ваша ставка ", options)
    num_dep = st.number_input("Размер депа ", step=0.1)

    now = time.time()

    if st.session_state.show_toast_until > now:
        st.toast(st.session_state.last_toast_message, icon=st.session_state.last_toast_icon)
        st.toast("Надо что-то депнуть скорее!", icon="💰")
        



    if num_dep > current_user["balance"]:
        st.toast("У тебя нет денег на ДЕП ", icon="❌")
    else:
        if st.button("ДЕПНУТЬ"):
            # Показываем анимацию вращения
            st.session_state.show_spinning_animation = True
            st.rerun()
        
        # Показываем вращающееся колесо после нажатия кнопки
        if st.session_state.show_spinning_animation:
            # Генерируем случайное время вращения от 3 до 6 секунд
            spin_time = random.uniform(3, 6)
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 10px;">
                <div class="spinning-wheel" style="animation: spin {spin_time}s linear infinite;"></div>
                <p style="color: #666; margin-top: 15px; font-size: 16px;">🎰 Крутим колесо удачи...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Имитируем обработку - используем то же случайное время
            time.sleep(spin_time)
            
            # Выполняем логику игры
            dep_ran = random.randint(1 + random.randint(5, 30), 95)
            user_dep_chance = stavka[user_dep][1]
            if dep_ran + user_dep_chance >= 100:
                current_user["balance"] += num_dep * (stavka[user_dep][0]) 
                st.session_state.last_toast_message = f"Поздравляем! Ваш баланс: {current_user['balance']} деп коинов"
                st.session_state.last_toast_icon = "✅"
                save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"])
            else:
                current_user["balance"] -= num_dep
                st.session_state.last_toast_message = f"Делай ДОДЕП ты проиграл :( Ваш баланс: {current_user['balance']} деп коинов"
                st.session_state.last_toast_icon = "❌"
                save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"])
            
            st.session_state.show_toast_until = time.time() + 2
            st.session_state.show_spinning_animation = False
            st.rerun()






def registr():
    
    # Заголовок с горизонтальной спиралью
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center;">
        <h1 style="margin: 0;">register please</h1>
        <div class="horizontal-spiral">
            <div class="spiral-dot"></div>
            <div class="spiral-dot"></div>
            <div class="spiral-dot"></div>
            <div class="spiral-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    input_user_name = st.text_input("👤 login", placeholder="Введите login", max_chars=18)
    input_password = st.text_input("🔒 password", type="password", placeholder="Введите password", max_chars=30)
    input_password_confirm = st.text_input("🔒 password confirm", type="password", placeholder="Подтвердите пароль", max_chars=30)
    if st.button("Зарегистрироваться"):  
        if not input_user_name or not input_password:
            st.toast("Заполните все поля!", icon="❌")
        elif input_password != input_password_confirm:
            st.toast("Пароли отличаются!", icon="❌") 
        elif len(input_user_name) < 3 or len(input_password) < 3:
            st.toast("Логин и пароль должны не менее 3 символов!", icon="❌")
        
        else:
            existing_user = find_user_by_login(input_user_name)
            if existing_user:
                st.toast("Такой пользователь уже существует!", icon="❌")  
            else:
                user_id = generate_user_id()
                save_user_to_file(user_id, input_user_name, input_password, 1000.0)
                st.toast(f"Пользователь {input_user_name} успешно зарегистрирован!", icon="✅")
                st.session_state.show_register = False
                time.sleep(1)
                st.rerun()
                
            



    if st.button("🔄 Назад"):
        st.session_state.show_register = False
        st.rerun()






def login():
    
    st.markdown("""
    <style>
        @keyframes wave {
            0%, 100% { transform: translateY(0px); }
            25% { transform: translateY(-5px); }
            75% { transform: translateY(5px); }
        }
        
        .horizontal-spiral {
            display: inline-block;
            width: 30px;
            height: 8px;
            margin-left: 10px;
            position: relative;
        }
        
        .spiral-dot {
            width: 6px;
            height: 6px;
            background: #3498db;
            border-radius: 50%;
            position: absolute;
            animation: wave 1.5s ease-in-out infinite;
        }
        
        .spiral-dot:nth-child(1) { left: 0px; animation-delay: 0s; }
        .spiral-dot:nth-child(2) { left: 8px; animation-delay: 0.1s; }
        .spiral-dot:nth-child(3) { left: 16px; animation-delay: 0.2s; }
        .spiral-dot:nth-child(4) { left: 24px; animation-delay: 0.3s; }
    </style>
    """, unsafe_allow_html=True)
    
    # Заголовок с горизонтальной спиралью
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center;">
        <h1 style="margin: 0;">Hello</h1>
        <div class="horizontal-spiral">
            <div class="spiral-dot"></div>
            <div class="spiral-dot"></div>
            <div class="spiral-dot"></div>
            <div class="spiral-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.title("login please")
    input_user_name = st.text_input("👤 login", placeholder="Введите логин", max_chars=18)
    input_password = st.text_input("🔒 password", type="password", placeholder="Введите пароль", max_chars=30)
    if st.button("Войти"):     
        # Ищем пользователя по логину
        user = find_user_by_login(input_user_name)

        if user and user["password"] == input_password:
            # Обновляем статус входа
            user["last_login"] = True
            save_user_to_file(user["id"], user["login"], user["password"], user["balance"])
            
            # Сохраняем информацию о входе в session_state
            st.session_state.logged_in_user = user
            st.session_state.user_logged_in = True
    
            st.toast(f'Добро пожаловать, {input_user_name}!', icon="✅")
            time.sleep(1)
            st.rerun()
        else:
            st.toast("Неверные данные пользователя!", icon="❌")
    
    st.markdown("---")
    
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; padding: 15px; background-color: #242434; border-radius: 8px;">
        <p style="color: #666; font-size: 14px; margin-bottom: 8px;">Нет аккаунта?</p>
        <p style="color: #1f77b4; font-size: 16px; font-weight: bold; margin: 0;">
           📝 Зарегистрируйся
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Кнопка прямо под текстом
    col1, col2, col3 = st.columns([2.1, 1, 1.5])
    with col2:
        if st.button("📝 Зарегистрироваться", key="register_btn", help="Создать новый аккаунт"):
            st.session_state.show_register = True
            st.rerun()
    
    




stavka = {
    "1": [1.5, 40],#лист из 1: x , 2: процент
    "5": [2, 20],
    "10": [2.5, 10],
    "К": [3, 5],
    "З": [5, 1]
}

# Проверяем, есть ли активный пользователь
active_user = None

# Сначала проверяем session_state
if hasattr(st.session_state, 'user_logged_in') and st.session_state.user_logged_in:
    active_user = st.session_state.logged_in_user

# Если нет в session_state, ищем в файлах
if not active_user:
    for filename in os.listdir("."):
        if filename.startswith("user_") and filename.endswith(".json"):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    if user_data.get("last_login", False):
                        active_user = user_data
                        # Обновляем session_state
                        st.session_state.logged_in_user = user_data
                        st.session_state.user_logged_in = True
                        break
            except Exception as e:
                continue

# Показываем соответствующую страницу
if active_user and not st.session_state.get('show_register', False):
    # Очищаем любые остатки формы логина
    st.empty()
    main_game(active_user)
    st.stop()
else:
    if st.session_state.show_register:
        registr()
    else:
        login()

        
    





