from datetime import datetime

FILE_NAME = "employees.txt"
LOGIN_FILE = "users.txt"

class Login:
    def __init__(self, user_id, password, authorization):
        self.user_id = user_id
        self.password = password
        self.authorization = authorization


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%m/%d/%Y")
        return True
    except ValueError:
        return False


def get_date(prompt):
    while True:
        date_input = input(prompt)
        if validate_date(date_input):
            return date_input
        print("Invalid date format. Use mm/dd/yyyy.")


def get_name():
    return input("Enter employee name (or type End): ")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid number. Please try again.")


def get_tax_rate():
    return get_float("Enter income tax rate (example: 20 for 20%): ") / 100


def calculate_pay(hours, rate, tax_rate):
    gross = round(hours * rate, 2)
    tax = round(gross * tax_rate, 2)
    net = round(gross - tax, 2)
    return gross, tax, net


def save_record(from_date, to_date, name, hours, rate, tax_rate):
    with open(FILE_NAME, "a") as file:
        file.write(f"{from_date}|{to_date}|{name}|{hours}|{rate}|{tax_rate}\n")


def get_report_date():
    while True:
        report_date = input("\nEnter FROM date for report (mm/dd/yyyy) or All: ")
        if report_date.lower() == "all":
            return "All"
        if validate_date(report_date):
            return report_date
        print("Invalid date format.")


def process_file(report_date):
    totals = {"employees": 0, "hours": 0, "tax": 0, "net": 0}

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                record = line.strip().split("|")

                if len(record) != 6:
                    continue

                from_date, to_date, name, hours, rate, tax_rate = record
                hours = float(hours)
                rate = float(rate)
                tax_rate = float(tax_rate)

                if report_date == "All" or from_date == report_date:
                    gross, tax, net = calculate_pay(hours, rate, tax_rate)

                    print("\nEmployee Payroll")
                    print("From Date:", from_date)
                    print("To Date:", to_date)
                    print("Name:", name)
                    print("Hours Worked:", round(hours, 2))
                    print("Hourly Rate:", round(rate, 2))
                    print("Gross Pay:", gross)
                    print("Income Tax Rate:", tax_rate)
                    print("Income Tax:", tax)
                    print("Net Pay:", net)

                    totals["employees"] += 1
                    totals["hours"] += hours
                    totals["tax"] += tax
                    totals["net"] += net

    except FileNotFoundError:
        print("No employee file found.")
        return totals

    totals["hours"] = round(totals["hours"], 2)
    totals["tax"] = round(totals["tax"], 2)
    totals["net"] = round(totals["net"], 2)

    return totals


def display_totals(totals):
    print("\nPayroll Totals")
    print("Total Employees:", totals["employees"])
    print("Total Hours:", totals["hours"])
    print("Total Income Tax:", totals["tax"])
    print("Total Net Pay:", totals["net"])


def create_users():
    with open(LOGIN_FILE, "a") as file:

        user_ids = []

        try:
            with open(LOGIN_FILE, "r") as readfile:
                for line in readfile:
                    user_ids.append(line.split("|")[0])
        except FileNotFoundError:
            pass

        while True:

            user_id = input("Enter User ID (or End): ")

            if user_id == "End":
                break

            if user_id in user_ids:
                print("User ID already exists.")
                continue

            password = input("Enter Password: ")
            auth = input("Enter Authorization (Admin/User): ")

            if auth not in ["Admin", "User"]:
                print("Authorization must be Admin or User.")
                continue

            file.write(f"{user_id}|{password}|{auth}\n")
            user_ids.append(user_id)


def login():

    user_ids = []
    passwords = []
    auths = []

    with open(LOGIN_FILE, "r") as file:
        for line in file:
            user_id, password, auth = line.strip().split("|")

            user_ids.append(user_id)
            passwords.append(password)
            auths.append(auth)

    user_id = input("Enter User ID: ")

    if user_id not in user_ids:
        print("User does not exist.")
        return None

    index = user_ids.index(user_id)

    password = input("Enter Password: ")

    if password != passwords[index]:
        print("Incorrect password.")
        return None

    return Login(user_ids[index], passwords[index], auths[index])


create_users()

login_user = login()

if login_user is None:
    exit()

print("\nLogged in user:", login_user.user_id)
print("Authorization:", login_user.authorization)

if login_user.authorization == "Admin":

    while True:
        from_date = get_date("\nEnter FROM date (mm/dd/yyyy): ")
        to_date = get_date("Enter TO date (mm/dd/yyyy): ")

        name = get_name()
        if name == "End":
            break

        hours = get_float("Enter hours worked: ")
        rate = get_float("Enter hourly rate: ")
        tax_rate = get_tax_rate()

        save_record(from_date, to_date, name, hours, rate, tax_rate)

else:
    print("\nUser access: payroll entry not allowed.")

print("\nData entry complete.")

report_date = get_report_date()

totals = process_file(report_date)

display_totals(totals)