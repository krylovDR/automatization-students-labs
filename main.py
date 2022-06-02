import sys

import csv
import gspread
import cpplint


class ErrorCollector(object):
    _ERROR_CATEGORIES = cpplint._ERROR_CATEGORIES
    _SEEN_ERROR_CATEGORIES = {}

    def __init__(self):
        self._errors = []
        cpplint.ResetNolintSuppressions()

    def __call__(self, unused_filename, linenum,
                 category, confidence, message):
        self._SEEN_ERROR_CATEGORIES[category] = 1
        if cpplint._ShouldPrintError(category, confidence, linenum):
            if confidence > 3:
                self._errors.append('%d: %s  [%s] [%d]' % (linenum + 1, message, category, confidence))

    def results(self):
        if len(self._errors) < 2:
            return ''.join(self._errors)  # Most tests expect to have a string.
        else:
            return self._errors  # Let's give a list if there is more than one.

    def result_list(self):
        return self._errors

    def verify_all_categories_are_seen(self):
        for category in self._ERROR_CATEGORIES:
            if category not in self._SEEN_ERROR_CATEGORIES:
                sys.exit('FATAL ERROR: There are no tests for category "%s"' % category)

    def remove_if_present(self, substr):
        for (index, error) in enumerate(self._errors):
            if error.find(substr) != -1:
                self._errors = self._errors[0:index] + self._errors[(index + 1):]
                break


def perform_multiline_lint(code):
    error_collector = ErrorCollector()
    lines = code.split('\n')
    cpplint.RemoveMultiLineComments('main.cpp', lines, error_collector)
    lines = cpplint.CleansedLines(lines)
    nesting_state = cpplint.NestingState()

    for i in range(lines.NumLines()):
        nesting_state.Update('main.cpp', lines, i, error_collector)
        cpplint.CheckStyle('main.cpp', lines, i, 'cpp', nesting_state, error_collector)
        cpplint.CheckForNonStandardConstructs('main.cpp', lines, i, nesting_state, error_collector)
    nesting_state.CheckCompletedBlocks('main.cpp', error_collector)

    return error_collector.result_list()


sa = gspread.service_account(filename="credentials.json")  # используем ключ сервисного аккаунта
sh = sa.open("Vedomost")  # открываем таблицу с ведомостью
wks = sh.worksheet("баллы")  # открываем необходимый лист в таблице ведомости

logins = wks.get('AG5:AG201')  # считывание диапазона ячеек с логинами
marks = []  # таблица с оценками

# считывание таблицы с оценками (первый индекс - номер лабы, второй индекс - номер студента)
marks.append(wks.get('D5:D201'))  # 0 лаба
marks.append(wks.get('E5:E201'))  # 1 лаба
marks.append(wks.get('F5:F201'))  # 2 лаба
marks.append(wks.get('G5:G201'))  # 3 лаба
marks.append(wks.get('H5:H201'))  # 4 лаба
marks.append(wks.get('I5:I201'))  # 5 лаба
marks.append(wks.get('J5:J201'))  # 6 лаба

# из-за пустых ячеек в таблице размер массива может быть меньше чем общее количество студентов (197)
for i in range(0, 7):
    while len(marks[i]) < 197:
        marks[i].append([])
while len(logins) < 197:
    logins.append([])

# обработка первой таблицы результатов
with open("1.csv", encoding='utf-8') as r_file:
    file_reader = csv.DictReader(r_file, delimiter=",")  # Создаем объект DictReader, указываем символ-разделитель ","
    # Считывание данных из CSV файла
    for row in file_reader:
        student_number = logins.index([row["login"]])  # определяем порядковый номер студента по логину

        # если лаба сдана, то прибавить 0.4 балла за тесты, если уже проставлено максимум за оформление
        if row["1(0_lab_1)"].find("+") >= 0:
            print("flag 1")
            if marks[0][student_number] == []:
                marks[0][student_number] = [str(0.4)]
                print("flag 2")
            elif float(marks[0][student_number][0].replace(',', '.')) < 0.39:
                marks[0][student_number] = [str(float(marks[0][student_number][0].replace(',', '.')) + 0.4)]
        if row["2(0_lab_2)"].find("+") >= 0:
            print("flag 3")
            if marks[1][student_number] == []:
                marks[1][student_number] = [str(0.4)]
                print("flag 4")
            elif float(marks[1][student_number][0].replace(',', '.')) < 0.39:
                marks[1][student_number] = [str(float(marks[1][student_number][0].replace(',', '.')) + 0.4)]

# обработка творой таблицы результатов
with open("2.csv", encoding='utf-8') as r_file:
    file_reader = csv.DictReader(r_file, delimiter=",")  # Создаем объект DictReader, указываем символ-разделитель ","
    # Считывание данных из CSV файла
    for row in file_reader:
        student_number = logins.index([row["login"]])  # определяем порядковый номер студента по логину

        # если лаба сдана, то прибавить 0.4 балла за тесты, если уже проставлено максимум за оформление
        if row["A(0_lab_3)"].find("+") >= 0:
            print("flag 5")
            if marks[2][student_number] == []:
                marks[2][student_number] = [str(0.4)]
                print("flag 6")
            elif float(marks[2][student_number][0].replace(',', '.')) < 0.39:
                marks[2][student_number] = [str(float(marks[2][student_number][0].replace(',', '.')) + 0.4)]
        if row["B(0_lab_4)"].find("+") >= 0:
            print("flag 7")
            if marks[3][student_number] == []:
                marks[3][student_number] = [str(0.4)]
                print("flag 8")
            elif float(marks[3][student_number][0].replace(',', '.')) < 0.39:
                marks[3][student_number] = [str(float(marks[3][student_number][0].replace(',', '.')) + 0.4)]


# обработка и учёт результатов линтера (Иванов 3 лаба)
st_num_lint = 196  # студент Иванов (демо)

f = open('main_no_err.cpp', 'r')
errors = perform_multiline_lint(f.read())

# если лаба сдана, то прибавить 0.4 балла за тесты, если уже проставлено максимум за оформление
if len(errors) == 0:
    if marks[2][st_num_lint] == []:
        marks[2][st_num_lint] = [str(0.3)]
    elif 0.31 < float(marks[2][st_num_lint][0].replace(',', '.')) < 0.69:
        marks[2][st_num_lint] = [str(float(marks[2][st_num_lint][0].replace(',', '.')) + 0.3)]


# обновление данных в таблице
wks.update('D5:D201', marks[0])  # 0 лаба
wks.update('E5:E201', marks[1])  # 1 лаба
wks.update('F5:F201', marks[2])  # 2 лаба
wks.update('G5:G201', marks[3])  # 3 лаба
wks.update('H5:H201', marks[4])  # 4 лаба
wks.update('I5:I201', marks[5])  # 5 лаба
wks.update('J5:J201', marks[6])  # 6 лаба
