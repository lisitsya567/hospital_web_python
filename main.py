from flask import Flask, request, render_template, redirect, url_for
import pymysql

app = Flask(__name__)

# Подключение к базе данных MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="A02032178a",
    database="test"
)
cursor = db.cursor()


# Создание таблицы для хранения информации о пациентах
cursor.execute("""CREATE TABLE IF NOT EXISTS patients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    patronymic VARCHAR(255),
                    passport_number VARCHAR(20),
                    birth_date DATE,
                    gender ENUM('Male', 'Female', 'Other'),
                    address VARCHAR(255),
                    phone_number VARCHAR(20),
                    email VARCHAR(255),
                    medical_card_number VARCHAR(20),
                    medical_card_issue_date DATE,
                    last_visit_date DATE,
                    next_visit_date DATE,
                    insurance_policy_number VARCHAR(20),
                    insurance_policy_expiry_date DATE,
                    diagnosis TEXT,
                    medical_history TEXT
                )""")

# Создание таблицы для хранения информации о направлениях пациентов
cursor.execute("""CREATE TABLE IF NOT EXISTS referrals (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT,
                    date DATE,
                    time TIME,
                    room_number VARCHAR(10),
                    diagnosis TEXT,
                    procedure_name VARCHAR(255),
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )""")

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        # Получение данных из формы
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        patronymic = request.form['patronymic']
        passport_number = request.form['passport_number']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        medical_card_number = request.form['medical_card_number']
        medical_card_issue_date = request.form['medical_card_issue_date']
        last_visit_date = request.form['last_visit_date']
        next_visit_date = request.form['next_visit_date']
        insurance_policy_number = request.form['insurance_policy_number']
        insurance_policy_expiry_date = request.form['insurance_policy_expiry_date']
        diagnosis = request.form['diagnosis']
        medical_history = request.form['medical_history']

        # Вставка данных в базу данных
        cursor.execute("""INSERT INTO patients (first_name, last_name, patronymic, passport_number, birth_date, 
                                                gender, address, phone_number, email, medical_card_number, 
                                                medical_card_issue_date, last_visit_date, next_visit_date, 
                                                insurance_policy_number, insurance_policy_expiry_date, 
                                                diagnosis, medical_history) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (first_name, last_name, patronymic, passport_number, birth_date, gender, address,
                        phone_number, email, medical_card_number, medical_card_issue_date, last_visit_date,
                        next_visit_date, insurance_policy_number, insurance_policy_expiry_date, diagnosis,
                        medical_history))
        db.commit()

        return 'Пациент успешно зарегистрирован!'
    else:
        return render_template('register_patient.html')

@app.route('/view_patients')
def view_patients():
    # Получение всех пациентов из базы данных
    cursor.execute("SELECT id, first_name, last_name FROM patients")
    patients = cursor.fetchall()
    return render_template('view_patients.html', patients=patients)


@app.route('/refer_patient', methods=['GET', 'POST'])
def refer_patient():
    if request.method == 'POST':
        # Получение данных из формы и сохранение их в базе данных
        patient_id = request.form['patient_id']
        date = request.form['date']
        time = request.form['time']
        room_number = request.form['room_number']
        diagnosis = request.form['diagnosis']
        procedure_name = request.form['procedure_name']

        # Вставка данных в базу данных
        cursor.execute("""INSERT INTO referrals (patient_id, date, time, room_number, diagnosis, procedure_name)
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                       (patient_id, date, time, room_number, diagnosis, procedure_name))
        db.commit()

        return 'Пациент успешно направлен на лечебно-диагностическое мероприятие!'
    else:
        return render_template('refer_patient.html')

@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
def view_patient(patient_id):
    if request.method == 'POST':
        # Обработка изменения данных пациента и обновление в базе данных
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        patronymic = request.form['patronymic']
        passport_number = request.form['passport_number']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        medical_card_number = request.form['medical_card_number']
        medical_card_issue_date = request.form['medical_card_issue_date']
        last_visit_date = request.form['last_visit_date']
        next_visit_date = request.form['next_visit_date']
        insurance_policy_number = request.form['insurance_policy_number']
        insurance_policy_expiry_date = request.form['insurance_policy_expiry_date']
        diagnosis = request.form['diagnosis']
        medical_history = request.form['medical_history']

        # Обновление данных пациента в базе данных
        cursor.execute("""UPDATE patients SET first_name=%s, last_name=%s, patronymic=%s, passport_number=%s,
                          birth_date=%s, gender=%s, address=%s, phone_number=%s, email=%s, medical_card_number=%s,
                          medical_card_issue_date=%s, last_visit_date=%s, next_visit_date=%s,
                          insurance_policy_number=%s, insurance_policy_expiry_date=%s, diagnosis=%s,
                          medical_history=%s WHERE id=%s""",
                       (first_name, last_name, patronymic, passport_number, birth_date, gender, address,
                        phone_number, email, medical_card_number, medical_card_issue_date, last_visit_date,
                        next_visit_date, insurance_policy_number, insurance_policy_expiry_date, diagnosis,
                        medical_history, patient_id))
        db.commit()
        return redirect(url_for('view_patients'))
    else:
        # Получение информации о выбранном пациенте по его ID
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        return render_template('view_patient.html', patient=patient)


@app.route('/view_referrals')
def view_referrals():
    # Получение всех направлений из базы данных
    cursor.execute("SELECT * FROM referrals")
    referrals = cursor.fetchall()
    return render_template('view_referrals.html', referrals=referrals)


@app.route('/referral/<int:referral_id>', methods=['GET', 'POST'])
def view_referral(referral_id):
    if request.method == 'POST':
        # Обработка изменения данных направления и обновление в базе данных
        date = request.form['date']
        time = request.form['time']
        room_number = request.form['room_number']
        diagnosis = request.form['diagnosis']
        procedure_name = request.form['procedure_name']

        # Обновление данных направления в базе данных
        cursor.execute("""UPDATE referrals SET date=%s, time=%s, room_number=%s, diagnosis=%s,
                          procedure_name=%s WHERE id=%s""",
                       (date, time, room_number, diagnosis, procedure_name, referral_id))
        db.commit()
        return redirect(url_for('view_referrals'))
    else:
        # Получение информации о выбранном направлении по его ID
        cursor.execute("SELECT * FROM referrals WHERE id = %s", (referral_id,))
        referral = cursor.fetchone()
        return render_template('view_referral.html', referral=referral)




# @app.route('/')
# def index():
#     return 'Добро пожаловать! Для регистрации пациента перейдите по адресу /register_patient'


if __name__ == '__main__':
    app.run(debug=True)

