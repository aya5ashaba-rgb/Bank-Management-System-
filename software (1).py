from datetime import datetime, timedelta
import re

DEFAULT_LOAN_INTEREST_RATE = 0.2

class Name:
    def __init__(self, first_name, last_name):
        if not first_name or not last_name:
            raise ValueError("First and last name cannot be empty.")
        self.first_name = first_name
        self.last_name = last_name

class Address:
    def __init__(self, city, country):
        city = city.title()
        country = country.title()
        if not city or not country:
            raise ValueError("City and country cannot be empty.")
        self.city = city
        self.country = country

class DateOfBirth:
    def __init__(self, day, month, year):
        if not (1 <= day <= 31 and 1 <= month <= 12 and year > 1900):
            raise ValueError("Invalid date of birth.")
        self.day = day
        self.month = month
        self.year = year



class Card:
    def __init__(self, card_id, expiry_date, card_type):
        card_type = card_type.title()
        if card_type not in ["Debit", "Credit"]:
            raise ValueError("Invalid card type.")
        try:
            expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Expiry date must be in YYYY-MM-DD format.")
        self.card_id = card_id
        self.expiry_date = expiry_date
        self.card_type = card_type

    def is_expired(self):
        today = datetime.today().date()
        expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
        return today > expiry

    def renew(self, years=3):
        if years <= 0:
            raise ValueError("Renewal period must be positive.")
        expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
        new_expiry = expiry + timedelta(days=years * 365)
        self.expiry_date = new_expiry.strftime("%Y-%m-%d")

class Transaction:
    def __init__(self, transaction_id, date, transaction_type, amount):
        transaction_type = transaction_type.title()
        if transaction_type not in ["Deposit", "Withdrawal"]:
            raise ValueError("Invalid transaction type.")
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
        self.transaction_id = transaction_id
        self.date = date
        self.transaction_type = transaction_type
        self.amount = amount

class Loan:
    def __init__(self, loan_id, amount, loan_type):
        loan_type = loan_type.title()
        if amount <= 0:
            raise ValueError("Loan amount must be positive.")
        if loan_type not in ["Personal", "Mortgage", "Auto"]:
            raise ValueError("Invalid loan type.")
        self.loan_id = loan_id
        self.amount = amount
        self.loan_type = loan_type
        self.interest_rate = 0.2

# --- Branch ---

class Branch:
    def __init__(self, branch_id, branch_name, location):
        if not branch_id or not branch_name or not location:
            raise ValueError("Branch ID, name, and location cannot be empty.")
        self.branch_id = branch_id
        self.branch_name = branch_name
        self.location = location
        self.employees = []

    def add_employee(self, employee):
        if not isinstance(employee, Employee):
            raise TypeError("employee must be an Employee object.")
        if employee in self.employees:
            raise ValueError("Employee already assigned to this branch.")
        self.employees.append(employee)

class Customer:
    customer_id_counter = 1000

    def __init__(self, name, email, phone, address, date_of_birth):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address.")
        if not phone.isdigit() or len(phone) < 7:
            raise ValueError("Invalid phone number.")
        if not isinstance(name, Name):
            raise TypeError("name must be a Name object.")
        if not isinstance(address, Address):
            raise TypeError("address must be an Address object.")
        if not isinstance(date_of_birth, DateOfBirth):
            raise TypeError("date_of_birth must be a DateOfBirth object.")
        Customer.customer_id_counter += 1
        self.customer_id = Customer.customer_id_counter
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
        self.accounts = []

    def add_account(self, account):
        if not isinstance(account, Account):
            raise TypeError("account must be an Account object.")
        self.accounts.append(account)



class Account:
    account_id_counter = 10000

    def __init__(self, customer, balance, account_type, card, password, branch):
        account_type = account_type.title()
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        if account_type not in ["Checking", "Savings"]:
            raise ValueError("Invalid account type.")
        if not isinstance(card, Card):
            raise TypeError("card must be a Card object.")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if not isinstance(branch, Branch):
            raise TypeError("branch must be a Branch object.")
        if not isinstance(customer, Customer):
            raise TypeError("customer must be a Customer object.")
        Account.account_id_counter += 1
        self.account_id = Account.account_id_counter
        self.customer = customer
        self.balance = balance
        self.account_type = account_type
        self.card = card
        self.password = password
        self.branch = branch
        self.transactions = []
        self.loans = []

    def check_password(self, password):
        return self.password == password

    def add_transaction(self, transaction, password):
        if not self.check_password(password):
            raise PermissionError("Incorrect password. Transaction denied.")
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction object.")

        if transaction.transaction_type == "Deposit":
            self.balance += transaction.amount
        elif transaction.transaction_type == "Withdrawal":
            if transaction.amount > self.balance:
                raise ValueError("Insufficient funds for withdrawal.")
            self.balance -= transaction.amount
        self.transactions.append(transaction)

    def add_loan(self, loan, password):
        if not self.check_password(password):
            raise PermissionError("Incorrect password. Loan request denied.")
        if not isinstance(loan, Loan):
            raise TypeError("loan must be a Loan object.")
        self.loans.append(loan)

    def remove_account(self, password):

        if not self.check_password(password):
            raise PermissionError("Incorrect password. Account removal denied.")
        if self.loans:
            raise ValueError("Cannot remove account with outstanding loans.")
        return True

    def remove_loan(self, loan_id, password):

        if not self.check_password(password):
            raise PermissionError("Incorrect password. Loan removal denied.")
        for loan in self.loans:
            if loan.loan_id == loan_id:
                self.loans.remove(loan)
                return True
        raise ValueError("Loan not found.")


class Employee:
    employee_id_counter = 1000
    def __init__(self, name, position, branch, allow_manager=False):
        if not isinstance(name, Name):
            raise TypeError("name must be a Name object.")
        if not position:
            raise ValueError("Position cannot be empty.")
        if position.strip().lower() == "manager" and not allow_manager:
            raise ValueError("Cannot create an Employee with position 'Manager'. Use the Manager class instead.")
        if not isinstance(branch, Branch):
            raise TypeError("branch must be a Branch object.")
        self.employee_id = Employee.employee_id_counter
        Employee.employee_id_counter += 1
        self.name = name
        self.position = position
        self.branch = branch
        self.managers = []

    def add_manager(self, manager):
        if not isinstance(manager, Employee):
            raise TypeError("manager must be an Employee object.")
        if manager == self:
            raise ValueError("Employee cannot be their own manager.")
        if manager in self.managers:
            raise ValueError("Manager already assigned.")
        self.managers.append(manager)

    def remove_manager(self, manager):
        if manager not in self.managers:
            raise ValueError("Manager not found.")
        self.managers.remove(manager)

    def display_info(self):
        print(f"Employee ID: {self.employee_id}")
        print(f"Name: {self.name.first_name} {self.name.last_name}")
        print(f"Position: {self.position}")
        print(f"Branch: {self.branch.branch_name}")


class Manager(Employee):
    def __init__(self, name, branch):
        super().__init__(name, "Manager", branch, allow_manager=True)
