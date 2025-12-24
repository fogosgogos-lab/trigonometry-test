import streamlit as st
import time

# Вопросы и варианты ответов для ВТОРОГО теста
questions = [
    ("Введите ваше имя:", "name"),  # Специальный для имени
    ("1. Чему равен cos(300°)?", ["-1/2", "1/2", "√3/2", "-√3/2"]),
    ("2. Вычислите: sin²(10°) + cos²(10°) - 1", ["1", "2sin(10°)", "0", "-1"]),
    ("3. Чему равен arctg(1)?", ["30° (π/6)", "45° (π/4)", "60° (π/3)", "90° (π/2)"]),
    ("4. Упростите: cos²(15°) - sin²(15°)", ["1/2", "√3/2", "1", "√2/2"]),
    ("5. Вычислите: sin(π) + cos(2π)", ["0", "1", "-1", "2"]),
    ("6. Найдите наименьший положительный корень уравнения 2cos(x) = √3", ["π/6", "π/3", "π/4", "5π/6"]),
    ("7. Сколько корней имеет уравнение sin(x) = π?", ["Один", "Два", "Бесконечно много", "Ни одного"]),
    ("8. Чему равен arcsin(sin(150°))?", ["150°", "-30°", "30°", "Не существует"]),
    ("9. Найдите максимальное значение функции y = 2 - sin(x)", ["1", "2", "3", "4"]),
    ("10. Упростите выражение: tg(x) · cos(x)", ["1", "sin(x)", "ctg(x)", "cos²(x)"]),
]

# Индексы правильных ответов (0-based): А=0, Б=1, В=2, Г=3
# Согласно твоему списку правильных:
correct_indices = [None, 1, 2, 1, 1, 1, 0, 3, 2, 2, 1]
#                     1:Б   2:В   3:Б   4:Б   5:Б   6:А   7:Г   8:В   9:В   10:Б

# Баллы за вопросы: 1-й вопрос — 1 балл, 2-й — 2 балла, ..., 10-й — 10 баллов
points = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
max_points = sum(points[1:])  # 55

TIME_LIMIT = 7 * 60  # 7 минут в секундах

# Инициализация состояния сессии
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'answers' not in st.session_state:
    st.session_state.answers = [-1] * len(questions)  # -1 = нет ответа
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'test_finished' not in st.session_state:
    st.session_state.test_finished = False

# Функция обновления таймера
def update_timer():
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TIME_LIMIT - elapsed)
    minutes = remaining // 60
    seconds = remaining % 60
    return f"Осталось: {minutes:02d}:{seconds:02d}", remaining

# Основное приложение
st.title("Тест по тригонометрии №2")

if not st.session_state.test_finished:
    # Таймер
    timer_text, remaining = update_timer()
    st.markdown(f"<h3 style='color: #d32f2f; text-align: center;'>{timer_text}</h3>", unsafe_allow_html=True)

    if remaining <= 0:
        st.warning("⏰ Время вышло! Тест завершён автоматически.")
        st.session_state.test_finished = True
        st.rerun()

    # Вопросы
    for i, (question_text, options) in enumerate(questions):
        st.markdown("---")
        if i == 0:  # Имя
            st.subheader(question_text)
            st.session_state.name = st.text_input("Ваше имя", value=st.session_state.name, key="name_input")
        else:
            st.subheader(question_text)
            labels = ['А', 'Б', 'В', 'Г']
            options_with_labels = [f"{labels[j]}) {opt}" for j, opt in enumerate(options)]
            selected_index = st.session_state.answers[i] if st.session_state.answers[i] != -1 else None
            selected = st.radio(
                "Выберите ответ:",
                options_with_labels,
                index=selected_index,
                key=f"q{i}"
            )
            if selected:
                st.session_state.answers[i] = options_with_labels.index(selected)

    # Кнопка завершения
    st.markdown("---")
    if st.button("Завершить тест", type="primary", use_container_width=True):
        st.session_state.test_finished = True
        st.rerun()

    # Автообновление таймера
    time.sleep(1)
    if remaining > 0:
        st.rerun()

else:
    # Подсчёт результатов
    name = st.session_state.name.strip() or "Участник"
    correct_count = 0
    wrong_count = 0
    no_answer_count = 0
    total_score = 0

    for i in range(1, len(questions)):
        user_ans = st.session_state.answers[i]
        if user_ans == -1:
            no_answer_count += 1
        elif user_ans == correct_indices[i]:
            correct_count += 1
            total_score += points[i]
        else:
            wrong_count += 1

    percent = round(total_score / max_points * 100, 1)

    result_text = f"""
**{name}, вы набрали {percent}%**

Заданий верно решено: **{correct_count}**  
Заданий неверно решено: **{wrong_count}**  
Нет ответа: **{no_answer_count}**  
Ваш балл: **{total_score}** из {max_points}
"""

    st.success("🎉 Тест завершён!")
    st.markdown(result_text, unsafe_allow_html=True)

    if st.button("Пройти тест заново"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()