import streamlit as st, json, time, random, os



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




def main_game():
    global data, user_index, stavka
    st.title("🎰 Lucky Depper")

    # Создаем сайдбар
    st.sidebar.title("🎰 Lucky Depper")
    st.sidebar.header("Профиль")

    # Информация о пользователе
    if user_index is not None and data["users"][user_index].get("last_login", False) == True:
        st.sidebar.write(f"👤 Пользователь: {data['users'][user_index]['login']}")
        st.sidebar.write(f"💰 Баланс: {float(data['users'][user_index]['balance'])}")

    # Кнопка выхода из аккаунта
    if st.sidebar.button("🚪 Выйти из аккаунта", type="primary"):
        if user_index is not None and data["users"][user_index].get("last_login", False) == True:
            for user in data["users"]:
                if user["login"] == data["users"][user_index]["login"]:
                    user["last_login"] = False
                    break
            
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
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
        



    if user_index is not None:
        if num_dep > data["users"][user_index]["balance"]:
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
                print(dep_ran)
                user_dep_chance = stavka[user_dep][1]
                if dep_ran + user_dep_chance >= 100:
                    data["users"][user_index]["balance"] += num_dep * (stavka[user_dep][0]) 
                    st.session_state.last_toast_message = f"Поздравляем! Ваш баланс: {data['users'][user_index]['balance']} деп коинов"
                    st.session_state.last_toast_icon = "✅"
                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    data["users"][user_index]["balance"] -= num_dep
                    st.session_state.last_toast_message = f"Делай ДОДЕП ты проиграл :( Ваш баланс: {data['users'][user_index]['balance']} деп коинов"
                    st.session_state.last_toast_icon = "❌"
                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                
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
            with open('data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            if data["users"]:
                copy_user = any(user["login"] == input_user_name for user in data["users"])
                if copy_user:
                    st.toast("Такой пользователь уже существует!", icon="❌")  
                else:
                    data["users"].append({
                        "login": input_user_name,
                        "password": input_password,
                        "balance": 1000.0,
                        "last_login": False
                    })  
                    with open("data.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    st.toast(f"Пользователь {input_user_name} успешно зарегистрирован!", icon="✅")
                    print(st.session_state.show_register)
                    time.sleep(3)
                    st.session_state.show_register = False
                    st.rerun()
                    
            else:
                data["users"].append({
                        "login": input_user_name,
                        "password": input_password,
                        "balance": 1000.0,
                        "last_login": False
                    })  
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                st.toast(f"Пользователь {input_user_name} успешно зарегистрирован!", icon="✅")
                print(st.session_state.show_register)
                time.sleep(3)
                st.session_state.show_register = False
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
        # Проверяем всех пользователей
        user_found = False
        for user in data["users"]:
            if user["login"] == input_user_name and user["password"] == input_password:
                user["last_login"] = True        
                with open("data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                st.toast(f'Добро пожаловать, {input_user_name}!', icon="✅")
                user_found = True
                time.sleep(1)
                st.rerun()
                 
                
        
        # Показываем ошибку только если пользователь не найден
        if not user_found:
            st.toast("Неверные данные пользователя!  Возможно стоит перезагрузить страницу или кликнуть по одной из строк ввода данных!", icon="❌")

    
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
    
    




data = {
    "users": [        
    ] 
}


if not os.path.exists("data.json"):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



with open("data.json", "r", encoding="utf-8") as f:
       data = json.load(f)







if "users" not in data:
    st.error("Файл data.json повреждён или не содержит пользователей!")
    st.stop()


for user in data["users"]:
    if "last_login" not in user:
        user["last_login"] = False
    if "balance" not in user:
        user["balance"] = 0.0



user_index = None

for i, user in enumerate(data["users"]):
    if user.get("last_login", False) == True:
        user_index = i
        break

stavka = {
    "1": [1.5, 40],#лист из 1: x , 2: процент
    "5": [2, 20],
    "10": [2.5, 10],
    "К": [3, 5],
    "З": [5, 1]
}







if user_index == None or data["users"][user_index].get("last_login", False) == False:
    if  st.session_state.show_register:
        registr()
    elif user_index == None or data["users"][user_index].get("last_login", False) == False:
        login()
else:
    main_game()

        
    





