import csv
import gspread


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

# обновление данных в таблице
wks.update('D5:D201', marks[0])  # 0 лаба
wks.update('E5:E201', marks[1])  # 1 лаба
wks.update('F5:F201', marks[2])  # 2 лаба
wks.update('G5:G201', marks[3])  # 3 лаба
wks.update('H5:H201', marks[4])  # 4 лаба
wks.update('I5:I201', marks[5])  # 5 лаба
wks.update('J5:J201', marks[6])  # 6 лаба
