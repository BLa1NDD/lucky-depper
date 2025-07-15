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
if "session_id" not in st.session_state:
    # Пытаемся восстановить состояние из файлов пользователей
    restored_session = None
    
    # Ищем файлы состояния пользователей
    for filename in os.listdir("."):
        if filename.startswith("user_state_") and filename.endswith(".json"):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    state_data = json.load(f)
                    if state_data.get("is_logged_in", False):
                        restored_session = state_data.get("session_id")
                        break
            except:
                continue
    
    if restored_session:
        st.session_state.session_id = restored_session
    else:
        # Генерируем уникальный session_id с временной меткой и случайным числом
        st.session_state.session_id = f"{str(uuid.uuid4())}_{int(time.time())}_{random.randint(1000, 9999)}"

# Инициализация остальных переменных сессии
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
if "show_welcome_message" not in st.session_state:
    st.session_state.show_welcome_message = False
if "welcome_message_time" not in st.session_state:
    st.session_state.welcome_message_time = 0
if "is_registration_message" not in st.session_state:
    st.session_state.is_registration_message = False


def generate_user_id():
    #Создает уникальный ID для пользователя
    return str(uuid.uuid4())

def save_user_to_file(user_id, login, password, balance=1000.0, session_id=None, history_win=None):
    """Сохраняет пользователя в отдельный файл"""
    if history_win is None:
        history_win = [None, None, None]
    user_data = {
        "id": user_id,
        "login": login,
        "password": password,
        "balance": balance,
        "session_id": session_id,
        "history_win": history_win
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

def save_user_state(user_id, is_logged_in=False):
    """Сохраняет состояние пользователя (вход/выход)"""
    state_file = f"user_state_{user_id}.json"
    state_data = {
        "user_id": user_id,
        "is_logged_in": is_logged_in,
        "session_id": st.session_state.session_id if is_logged_in else None,
        "timestamp": int(time.time())
    }
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state_data, f, ensure_ascii=False, indent=2)

def load_user_state(user_id):
    """Загружает состояние пользователя"""
    state_file = f"user_state_{user_id}.json"
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return None

def main_game():
    global stavka
    
    
    def hidtory_columns_show(show_col1, show_col2, show_col3):
        with col1:
            if show_col1 is not None:
                show_col1()
        with col2:
            if show_col2 is not None:
                show_col2()
        with col3:
            if show_col3 is not None:
                show_col3()
    

    def show_letter_W():#показывет победу
        st.markdown("""
        <div style="
            display: inline-block;
            color: #28a745;
            font-size: 24px;
            font-weight: bold;
            border: 3px solid #28a745;
            padding: 8px 12px;
            border-radius: 8px;
            margin: 2px;
        ">W</div>
        """, unsafe_allow_html=True)

    def show_letter_L():#показывет проигрыш
        st.markdown("""
        <div style="
            display: inline-block;
            color: #dc3545;
            font-size: 24px;
            font-weight: bold;
            border: 3px solid #dc3545;
            padding: 8px 12px;
            border-radius: 8px;
            margin: 2px;
        ">L</div>
        """, unsafe_allow_html=True)
        
    def show_none():
        st.write("")

        

    # Очищаем контейнер для предотвращения смешивания с формой логина
    st.empty()
    
    # Получаем текущего пользователя из файлов по session_id
    current_user = None
    for filename in os.listdir("."):
        if filename.startswith("user_") and filename.endswith(".json"):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                    if user_data.get("session_id") == st.session_state.session_id:
                        current_user = user_data
                        break
            except:
                continue
    
    if not current_user:
        st.error("Пользователь не найден!")
        st.rerun()
    
    def change_stat_win(state_win_or_lose):
        nonlocal show_col2, show_col3
        col2 = None
        col3 = None
        if show_col2 is not None and show_col2 != show_none:
            if show_col2 == show_letter_W: col2 = True 
            else: col2 = False
        if show_col3 is not None and show_col3 != show_none:
            if show_col3 == show_letter_W: col3 = True
            else: col3 = False
        
        new_history_win = [col2, col3, state_win_or_lose]


        save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"], current_user["session_id"], new_history_win)
        save_user_state(current_user["id"], True)


    history_win = current_user["history_win"]#это ЛИСТ из 3 BOOL элементов 
    print(current_user["history_win"])
    if history_win[0] is not None:
        if history_win[0]:
            show_col1 = show_letter_W
        else:
            show_col1 = show_letter_L
    else:
        show_col1 = show_none
    if history_win[1] is not None:
        if history_win[1]:
            show_col2 = show_letter_W
        else:
            show_col2 = show_letter_L
    else:
        show_col2 = show_none
    if history_win[2] is not None:
        if history_win[2]:
            show_col3 = show_letter_W
        else:
            show_col3 = show_letter_L
    else:
        show_col3 = show_none

    
    st.title("🎰 Lucky Depper")
    col1, col2, col3, col4 = st.columns([0.1, 0.1, 0.1, 3.7])
    
    hidtory_columns_show(show_col1, show_col2, show_col3)
    




    # Создаем сайдбар
    st.sidebar.title("🎰 Lucky Depper")
    st.sidebar.header("Профиль")

    # Информация о пользователе
    st.sidebar.write(f"👤 Пользователь: {current_user['login']}")
    st.sidebar.write(f"💰 Баланс: {float(current_user['balance'])}")

    # Кнопка выхода из аккаунта
    if st.sidebar.button("🚪 Выйти из аккаунта"):
        current_user["session_id"] = None
        save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"], None, current_user["history_win"])
        
        # Сохраняем состояние пользователя (выход)
        save_user_state(current_user["id"], False)
        
        st.rerun()

    # Разделитель
    st.sidebar.divider()

    # Дополнительные настройки
    st.sidebar.subheader("Статистика")
    st.sidebar.write("🎯 Вероятности выигрыша:")
    st.sidebar.write("• 1 - 1.5x = 60%")
    st.sidebar.write("• 5 - 2x = 30%") 
    st.sidebar.write("• 10 - 2.5x = 15%")
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
            spin_time = random.uniform(2, 4)
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 10px;">
                <div class="spinning-wheel" style="animation: spin {spin_time}s linear infinite;"></div>
                <p style="color: #666; margin-top: 15px; font-size: 16px;">🎰 Крутим колесо удачи...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Имитируем обработку - используем то же случайное время
            time.sleep(spin_time)
            # Выполняем логику игры
            win_chance = stavka[user_dep][1]
            if random.randint(1, 100) <= win_chance:
                current_user["balance"] += num_dep * (stavka[user_dep][0]) 
                st.session_state.last_toast_message = f"Поздравляем! Ваш баланс: {current_user['balance']} деп коинов"
                st.session_state.last_toast_icon = "✅"
                save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"], current_user["session_id"])
                change_stat_win(True)
            else:
                current_user["balance"] -= num_dep
                st.session_state.last_toast_message = f"Делай ДОДЕП ты проиграл :( Ваш баланс: {current_user['balance']} деп коинов"
                st.session_state.last_toast_icon = "❌"
                save_user_to_file(current_user["id"], current_user["login"], current_user["password"], current_user["balance"], current_user["session_id"])
                change_stat_win(False)
            st.session_state.show_toast_until = time.time() + 2
            st.session_state.show_spinning_animation = False
            st.rerun()






def registr():
    
    # Очищаем контейнер для предотвращения смешивания с игрой
    st.empty()
    
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
                save_user_to_file(user_id, input_user_name, input_password, 1000.0, None)
                
                # Сохраняем состояние пользователя (не в системе)
                save_user_state(user_id, False)
                
                # Устанавливаем время показа сообщения
                st.session_state.show_register = False
                st.session_state.show_welcome_message = True
                st.session_state.is_registration_message = True
                st.session_state.welcome_message_time = time.time() + 2
                
                # Добавляем небольшую задержку для гарантии сохранения файла
                time.sleep(0.1)
                st.rerun()


    if st.button("🔄 Назад"):
        st.session_state.show_register = False
        st.rerun()






def login():
    
    # Очищаем контейнер для предотвращения смешивания с игрой
    st.empty()
    
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
            # Обновляем статус входа с уникальным session_id
            user["session_id"] = st.session_state.session_id
            save_user_to_file(user["id"], user["login"], user["password"], user["balance"], st.session_state.session_id, user["history_win"])
            
            # Сохраняем состояние пользователя
            save_user_state(user["id"], True)
    
            # Устанавливаем время показа сообщения
            st.session_state.show_welcome_message = True
            st.session_state.is_registration_message = False
            st.session_state.welcome_message_time = time.time() + 2
            
            # Добавляем небольшую задержку для гарантии сохранения файла
            time.sleep(0.1)
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
    "1": [1.5, 60],#лист из 1: x , 2: процент
    "5": [2, 30],
    "10": [2.5, 15],
    "К": [3, 5],
    "З": [5, 1]
}

# Проверяем, есть ли активный пользователь
active_user = None
for filename in os.listdir("."):
    if filename.startswith("user_") and filename.endswith(".json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                if user_data.get("session_id") == st.session_state.session_id:
                    # Проверяем состояние пользователя
                    user_state = load_user_state(user_data["id"])
                    if user_state and user_state.get("is_logged_in", False):
                        active_user = user_data
                        break
        except Exception as e:
            print(f"Ошибка чтения файла {filename}: {e}")
            # Если файл поврежден, удаляем его
            try:
                os.remove(filename)
            except:
                pass
            continue

# Показываем соответствующую страницу
if active_user:  
    # Показываем приветственное сообщение если нужно
    if st.session_state.show_welcome_message and time.time() < st.session_state.welcome_message_time:
        st.toast(f'Добро пожаловать, {active_user["login"]}!', icon="✅")
    elif st.session_state.show_welcome_message and time.time() >= st.session_state.welcome_message_time:
        st.session_state.show_welcome_message = False
        st.session_state.is_registration_message = False
    st.empty()
    main_game()
    
else:
    # Очищаем предыдущий контент
    st.empty()
    
    if st.session_state.show_register:
        registr()
    else:
        # Показываем сообщение о регистрации если нужно
        if st.session_state.show_welcome_message and st.session_state.is_registration_message and time.time() < st.session_state.welcome_message_time:
            st.toast("Пользователь успешно зарегистрирован!", icon="✅")
        elif st.session_state.show_welcome_message and time.time() >= st.session_state.welcome_message_time:
            st.session_state.show_welcome_message = False
            st.session_state.is_registration_message = False
        
        login()

        
    





