import telebot
import datetime
from classes import Message, DataBase


def violation_message(message):
    bot.send_message(message.chat.id, access_violation)


def check_permittion(id, level):
    if len(data_base.get_teacher(id)) == 0:
        return False
    return int(data_base.get_teacher(id)[0][0]) <= level


def convert_grade(x):
    x = int(x)
    if not(x in [10, 11]):
        raise Exception
    return x


def convert_to_str_date(date):
    year = "".join(str(date.year)[2:4])
    month = str(date.month) if len(str(date.month)) == 2 else "0" + str(date.month)
    day = str(date.day) if len(str(date.day)) == 2 else "0" + str(date.day)
    return f"{day}.{month}.{year}"


def convert_to_date(x):
    example = list("11.11.11")
    x = list(x)
    if len(example) > len(x):
        raise Exception
    for i in range(len(x)):
        if example[i] == "1":
            example[i] = str(int(x[i]))
        elif example[i] != x[i]:
            raise Exception
    return "".join(example)


def convert_date(x):
    year = "".join(x[0:2])
    month = "".join(x[3:5])
    day = "".join(x[6:8])
    return f"{day}.{month}.{year}"


def get_dates():
    dates_mark = telebot.types.ReplyKeyboardMarkup(True, False)
    today = datetime.date.today()
    res = []
    for i in range(0, 10):
        res.append(convert_to_str_date(today.__add__(datetime.timedelta(days=i))))
    dates_mark.row(convert_to_str_date(today), res[1], res[2])
    dates_mark.row(res[3], res[4], res[5])
    dates_mark.row(res[6], res[7], res[8])
    return dates_mark


command_get_homework_by_subject = "hw_by_subject"
command_get_homework_by_date = "hw_by_date"
command_add_admin = "add_admin"
command_add_teacher = "add_teacher"
command_add_homework = "add_hw"
command_edit_homework = "edit_hw"
main_menu = "main menu:"
go_back = "go back"
messages = Message("messages.txt")
data_base = DataBase()
token = '5727527989:AAGlxBkN1U_FfaIVlYsHhcvdUwYAZ4He21I'
start_text = messages.get_message(1)
access_violation = messages.get_message(2)
discipline_text = "Select the discipline🔎"
grade_text = "Choose the grade🗄"
date_text = "Select the date📅"
task_text = "Write your task📝(text only)"
success_text = "Success✅"
error_text = "Sorry, I haven't learned how to do it 😢"
user_mark = telebot.types.ReplyKeyboardMarkup(True, False)
user_mark.row(f"/{command_get_homework_by_date}", f"/{command_get_homework_by_subject}")
user_mark.row(f"/{command_add_homework}", f"/{command_edit_homework}")
nothing_mark = telebot.types.ReplyKeyboardMarkup(True, False)
nothing_mark.row("nothing")
heap = dict()


def add_to_heap(id, key, info):
    if not (id in heap.keys()):
        heap[id] = dict()
        heap[id]["subject"] = ""
        heap[id]["grade"] = 0
        heap[id]["date"] = "101"
        heap[id]["task"] = ""
        heap[id]["task_prev"] = ""
        heap[id]["choice"] = ""
        heap[id]["access"] = []
    heap[id][key] = info

print("start")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['get_id'])
def get_id(message):
    bot.send_message(message.chat.id, f"your id in telegram is {message.chat.id}")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, start_text, reply_markup=user_mark)


@bot.message_handler(commands=[command_add_homework])
def add_homework(message):
    if not check_permittion(message.chat.id, 2):
        return bot.send_message(message.chat.id, access_violation)
    variants = data_base.get_subjects_people(message.chat.id)
    add_to_heap(message.chat.id, "access", variants)
    homework_mark = telebot.types.ReplyKeyboardMarkup(True, False)
    for i in range(int(len(variants) / 4)):
        homework_mark.row(variants[i * 4], variants[i * 4 + 1], variants[i * 4 + 2], variants[i * 4 + 3])
    for i in range(len(variants) % 4):
        homework_mark.row(variants[-i - 1])
    homework_mark.row(go_back)
    bot.send_message(message.chat.id, discipline_text, reply_markup=homework_mark)
    bot.register_next_step_handler(message, add_homework_2)


def add_homework_2(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    id = message.chat.id
    add_to_heap(id, "subject", message.text)
    if not(heap[id]["subject"] in heap[id]["access"]):
        bot.send_message(id, "incorrect subject", reply_markup=user_mark)
        return
    grade_mark = telebot.types.ReplyKeyboardMarkup(True, False)
    grade_mark.row("10", '11')
    grade_mark.row(go_back)
    bot.send_message(message.chat.id, grade_text, reply_markup=grade_mark)
    bot.register_next_step_handler(message, add_homework_3)


def add_homework_3(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    try:
        add_to_heap(message.chat.id, "grade", convert_grade(message.text))
        bot.send_message(message.chat.id, f"{date_text}: day.month.year (example: 02.11.22 )", reply_markup=get_dates())
        bot.register_next_step_handler(message, add_homework_4)
    except Exception:
        bot.send_message(message.chat.id, "incorrect grade, it can be only 10 or 11", reply_markup=user_mark)


def add_homework_4(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    try:
        add_to_heap(message.chat.id, "date", convert_to_date(message.text))
        bot.send_message(message.chat.id, task_text, reply_markup=nothing_mark)
        bot.register_next_step_handler(message, save_homework)
    except Exception:
        bot.send_message(message.chat.id, "the date is wrong", reply_markup=user_mark)


def save_homework(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    id = message.chat.id
    add_to_heap(id, "task", message.text)
    try:
        add_to_heap(id, "task_prev", data_base.get_homework(heap[id]["subject"], heap[message.chat.id]["date"], heap[id]["grade"]))
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.add("edit", "add")
        markup.row(go_back)
        bot.send_message(id, f"homework:{heap[id]['task_prev']}. add or edit?", reply_markup=markup)
        bot.register_next_step_handler(message, save_homework_2)
        return
    except Exception:
        pass
    try:
        data_base.add_homework(heap[id]["task"], heap[id]["subject"], int(heap[id]["grade"]), heap[id]["date"])
        bot.send_message(id, f"{success_text} {heap[id]['subject']}, {heap[id]['grade']}th grade to {heap[id]['date']}: {heap[id]['task']}", reply_markup=user_mark)
    except Exception:
        bot.send_message(id, "incorrect data, can't add hometask", reply_markup=user_mark)


def save_homework_2(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    id = message.chat.id
    choice = message.text
    if choice == "add":
        data_base.edit_homework(heap[id]['task_prev'] + "; " + heap[id]['task'], heap[id]['subject'], heap[id]['date'], heap[id]['grade'])
        bot.send_message(id, success_text, reply_markup=user_mark)
    elif choice == "edit":
        data_base.edit_homework(heap[id]['task'], heap[id]['subject'], heap[id]['date'], heap[id]['grade'])
        bot.send_message(id, success_text, reply_markup=user_mark)
    else:
        bot.send_message(id, "incorrect data!", reply_markup=user_mark)


@bot.message_handler(commands=[command_edit_homework])
def edit_homework(message):
    if not check_permittion(message.chat.id, 2):
        return bot.send_message(message.chat.id, access_violation)
    subject_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    variants = data_base.get_subjects_people(message.chat.id)
    add_to_heap(message.chat.id, "access", variants)
    for i in range(int(len(variants) / 4)):
        subject_markup.row(variants[i * 4], variants[i * 4 + 1], variants[i * 4 + 2], variants[i * 4 + 3])
    for i in range(len(variants) % 4):
        subject_markup.row(variants[-i - 1])
    subject_markup.row(go_back)
    bot.send_message(message.chat.id, discipline_text, reply_markup=subject_markup)
    bot.register_next_step_handler(message, edit_homework_2)


def edit_homework_2(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    id = message.chat.id
    add_to_heap(id, "subject", message.text)
    if not(heap[id]["subject"] in heap[id]["access"]):
        bot.send_message(id, "incorrect subject", reply_markup=user_mark)
        return
    bot.send_message(message.chat.id, f"{date_text}: day.month.year (example: 02.11.22 )", reply_markup=get_dates())
    bot.register_next_step_handler(message, edit_homework_3)


def edit_homework_3(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    try:
        add_to_heap(message.chat.id, "date", convert_to_date(message.text))
    except Exception:
        bot.send_message(message.chat.id, "the date is wrong", reply_markup=user_mark)
        return
    grade_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    grade_markup.row('10', '11')
    bot.send_message(message.chat.id, grade_text, reply_markup=grade_markup)
    bot.register_next_step_handler(message, edit_homework_4)


def edit_homework_4(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    id = message.chat.id
    try:
        add_to_heap(id, "grade", convert_grade(message.text))
        homework = data_base.get_homework(heap[id]["subject"], heap[id]["date"], heap[id]["grade"])
    except Exception:
        bot.send_message(message.chat.id, "nothing has been found", reply_markup=user_mark)
        return
    choice_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    choice_markup.add("delete", "edit", "add")
    choice_markup.row(go_back)
    bot.send_message(message.chat.id, f"homework is:{homework}. Select what to do", reply_markup=choice_markup)
    bot.register_next_step_handler(message, edit_homework_res)


def edit_homework_res(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    id = message.chat.id
    add_to_heap(id, "choice", message.text)
    choice = heap[id]["choice"]
    if choice == "add" or choice == "edit":
        bot.send_message(id, task_text, reply_markup=nothing_mark)
        bot.register_next_step_handler(message, edit_homework_res_2)
    elif choice == "delete":
        data_base.delete_homework(heap[id]["subject"], heap[id]["date"], heap[id]["grade"])
        bot.send_message(id, success_text + "the homework has been deleted!", reply_markup=user_mark)
    else:
        bot.send_message(id, "incorrect data!", reply_markup=user_mark)


def edit_homework_res_2(message):
    id = message.chat.id
    choice = heap[id]["choice"]
    subject = heap[id]["subject"]
    date = heap[id]["date"]
    grade = heap[id]["grade"]
    if choice == "add":
        data_base.edit_homework(heap[id]["task_prev"] + "; " + message.text, subject, date, grade)
    elif choice == "edit":
        data_base.edit_homework(message.text, subject, date, grade)
    bot.send_message(id, success_text, reply_markup=user_mark)


@bot.message_handler(commands=['get_all_subjects'])
def show_subjects(message):
    bot.send_message(message.chat.id, ", ".join(data_base.get_all_subjects()))


@bot.message_handler(commands=[command_add_teacher])
def add_teacher(message):
    if not check_permittion(message.chat.id, 1):
        return bot.send_message(message.chat.id, access_violation)
    try:
        i, subjects = message.text.split('.')[1], [j.lower() for j in message.text.split('.')[2].split(",")]
        flag = False
        for subject in subjects:
            if not(subject in data_base.get_all_subjects()):
                bot.send_message(message.chat.id, f"couldn't find subject {subject}")
                flag = True
                return
        if flag:
            return
        data_base.add_teacher(i, subjects)
        bot.send_message(message.chat.id, f'{success_text} teacher of {subjects} with id {i} has been added', reply_markup=user_mark)
    except Exception:
        bot.send_message(message.chat.id, 'an error occured, example of input: /add_teacher .-2.tok,math_ai_sl', reply_markup=user_mark)


@bot.message_handler(commands=[command_add_admin])
def add_admin(message):
    if not check_permittion(message.chat.id, 1):
        return bot.send_message(message.chat.id, access_violation)
    try:
        i = message.text.split('.')[1]
        data_base.add_admin(i)
        bot.send_message(message.chat.id, f'{success_text} added admin with id {i}', reply_markup=user_mark)
    except Exception:
        bot.send_message(message.chat.id, 'an error occured, example of input: /add_admin .-2', reply_markup=user_mark)


@bot.message_handler(commands=[command_get_homework_by_subject])
def check_homework_subject(message):
    subject_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    variants = data_base.get_all_subjects()
    subject_markup.row(go_back)
    for i in range(int(len(variants) / 4)):
        subject_markup.row(variants[i * 4], variants[i * 4 + 1], variants[i * 4 + 2], variants[i * 4 + 3])
    for i in range(len(variants) % 4):
        subject_markup.row(variants[-i - 1])
    bot.send_message(message.chat.id, discipline_text, reply_markup=subject_markup)
    bot.register_next_step_handler(message, check_homework_subject_2)


def check_homework_subject_2(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    add_to_heap(message.chat.id, "subject", message.text)
    grade_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    grade_markup.row(go_back)
    grade_markup.row('10', '11')

    bot.send_message(message.chat.id, grade_text, reply_markup=grade_markup)
    bot.register_next_step_handler(message, send_homework_subject)


def send_homework_subject(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    subject = heap[message.chat.id]["subject"]
    try:
        grade = convert_grade(message.text)
        new_message = f"{subject} tasks for {grade}th grade \n"
        if data_base.check_subject(subject):
            result = data_base.get_homework_subject(subject, grade)
            for i in [list(j) for j in result]:
                new_message += f"{convert_date(i[1])}: \n {i[0]} \n"
            if new_message == f"{subject} tasks for {grade}th grade \n":
                new_message = f"there aren't tasks for {subject} for {grade}th grade"
            bot.send_message(message.chat.id, new_message, reply_markup=user_mark)
        else:
            raise BaseException
    except Exception:
        bot.send_message(message.chat.id, "incorrect data", reply_markup=user_mark)


@bot.message_handler(commands=[command_get_homework_by_date])
def check_homework_date(message):
    bot.send_message(message.chat.id, f"{date_text}: day.month.year (example: 02.11.22 )", reply_markup=get_dates())
    bot.register_next_step_handler(message, check_homework_date_2)


def check_homework_date_2(message):
    if message.text == go_back:
        bot.send_message(message.chat.id, main_menu, reply_markup=user_mark)
        return
    txt = message.text
    try:
        add_to_heap(message.chat.id, "date", convert_to_date(message.text))
    except Exception:
        bot.send_message(message.chat.id, "date is wrong", reply_markup=user_mark)
        return
    grade_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    grade_markup.row('10', '11')
    bot.send_message(message.chat.id, grade_text, reply_markup=grade_markup)
    bot.register_next_step_handler(message, send_homework_date)


def send_homework_date(message):
    date = heap[message.chat.id]["date"]
    try:
        grade = convert_grade(message.text)
        new_message = f"tasks to {date} for {grade}th grade \n"
        result = data_base.get_homework_date(date, grade)
        for i in [list(j) for j in result]:
            new_message += f"{i[1]}: \n {i[0]} \n"
        if new_message == f"tasks to {date} for {grade}th grade \n":
            new_message = f"no tasks to {date} for {grade}th grade"
        bot.send_message(message.chat.id, new_message, reply_markup=user_mark)
    except:
        bot.send_message(message.chat.id, "incorrect data", reply_markup=user_mark)


bot.infinity_polling()
