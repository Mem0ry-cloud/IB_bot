import sqlite3


class Message:
    def __init__(self, filename):
        f = open(filename, 'r', encoding="utf8")
        self.messages = f.read().split("\kn")

    def get_message(self, index):
        return self.messages[index - 1]


class DataBase:
    def __init__(self):
        self.name = 'DataBases.db'

    def convert_date(self, date):
        year = date[-2] + date[-1]
        month = "".join(date[3:5])
        day = "".join(date[0:2])
        return f"{year}.{month}.{day}"

    def get_teacher(self, x):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        res = list(cursor.execute(f'select access, subjects from people where name = "{str(x)}"').fetchall())
        conn.close()
        return [list(i) for i in res]

    def add_teacher(self, x, subjects):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        subjects = ",".join(subjects)
        cursor.execute(f'insert into people (name, access, subjects) VALUES("{str(x)}", {2}, "{subjects}")')
        conn.commit()

    def add_admin(self, x):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute(f"insert into people (name, access) VALUES({str(x)}, {1})")
        conn.commit()

    def delete_homework(self, subject, date, grade):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        date = self.convert_date(date)
        subject = list(cursor.execute(f'select id from subjects where name == "{subject}"').fetchone())[0]
        line = f'delete from hometasks where subject={subject} and grade={grade} and date="{date}"'
        cursor.execute(line)
        conn.commit()

    def edit_homework(self, text, subject, date, grade):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        date = self.convert_date(date)
        subject = list(cursor.execute(f'select id from subjects where name == "{subject}"').fetchone())[0]
        line = f'delete from hometasks where subject={subject} and grade={grade} and date="{date}"'
        cursor.execute(line)
        line = f'insert into hometasks(task, subject, grade, date) VALUES("{text}", {subject}, {grade}, "{date}")'
        cursor.execute(line)
        conn.commit()

    def get_homework(self, subject, date, grade):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        date = self.convert_date(date)
        subject = list(cursor.execute(f'select id from subjects where name == "{subject}"').fetchone())[0]
        line = f'select task, subject from hometasks where grade={grade} AND date="{date}" AND subject={subject}'
        l = list(cursor.execute(line).fetchone())[0]
        conn.close()
        return l

    def get_homework_date(self, date, grade):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        date = self.convert_date(date)
        line = f'select task, subject from hometasks where grade={grade} AND date="{date}"'
        l = [list(j) for j in list(cursor.execute(line).fetchall())]
        subjects = [list(i)[0] for i in list(cursor.execute(f"select name from subjects").fetchall())]
        for i in range(len(l)):
            l[i][1] = subjects[l[i][1] - 1]
        conn.close()
        return l

    def get_homework_subject(self, subject, grade):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        today = sqlite3.Date.today()
        year = "".join(str(today.year)[2:4])
        month = str(today.month) if len(str(today.month)) == 2 else "0" + str(today.month)
        day = str(today.day) if len(str(today.day)) == 2 else "0" + str(today.day)
        date = f"{year}.{month}.{day}"
        subj = list(cursor.execute(f'select id from subjects where name = "{subject}"').fetchone())[0]
        line = f'select task, date from hometasks where grade={grade} AND date>="{date}" AND subject={subj}'
        res = list(cursor.execute(line).fetchall())
        conn.close()
        return res

    def get_subjects_people(self, x):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        all_subjects = [list(i)[0] for i in list(cursor.execute(f"select name from subjects").fetchall())]
        subject = list(cursor.execute(f'select subjects from people where name="{x}"').fetchone())
        if subject[0] is None:
            subject = all_subjects
        else:
            print(subject[0])
            subject = subject[0].split(",")
        conn.close()
        return subject

    def get_all_subjects(self):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        res = [list(i)[0] for i in list(cursor.execute(f"select name from subjects").fetchall())]
        conn.close()
        return res

    def add_homework(self, text, subject, grade, date):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        date = self.convert_date(date)
        subject = list(cursor.execute(f'select id from subjects where name == "{subject}"').fetchone())[0]
        line = f'insert into hometasks(task, subject, grade, date) VALUES("{text}", {subject}, {grade}, "{date}")'
        cursor.execute(line)
        conn.commit()

    def check_subject(self, subject):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        result = list(cursor.execute(f'select id from subjects where name = "{subject}"').fetchone())
        return len(result) > 0

    def test(self, x):
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        print(list(cursor.execute(f'select access, subjects from people where name = "{str(x)}"').fetchone()))
        conn.close()
