import numpy as np

class Employee:
    def __init__(self, emp_id, name, age, position, salary):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.position = position
        self.salary = salary

    def calculate_bonus(self):
        """Base method to calculate bonus, overridden in subclasses."""
        return self.salary * 0.1

    def display(self):
        return f"ID: {self.emp_id}, Name: {self.name}, Position: {self.position}, Salary: {self.salary}"

class Manager(Employee):
    def calculate_bonus(self):
        return self.salary * 0.2

class Engineer(Employee):
    def calculate_bonus(self):
        return self.salary * 0.15

class Intern(Employee):
    def calculate_bonus(self):
        return 500  # Flat bonus for interns

class EmployeeManagementSystem:
    def __init__(self):
        self.employees = {}  # Dictionary to store employees: {id: Employee}

    def add_employee(self, employee):
        if employee.emp_id in self.employees:
            raise ValueError("Employee ID already exists.")
        self.employees[employee.emp_id] = employee

    def remove_employee(self, emp_id):
        if emp_id not in self.employees:
            raise KeyError("Employee ID not found.")
        del self.employees[emp_id]

    def view_all_employees(self):
        if not self.employees:
            print("No employees found.")
        else:
            for emp in self.employees.values():
                print(emp.display())

    def calculate_payroll(self):
        salaries = [emp.salary for emp in self.employees.values()]
        total_payroll = np.sum(salaries)
        avg_salary = np.mean(salaries) if salaries else 0
        return total_payroll, avg_salary

    def recent_employees(self, count=3):
        ids = list(self.employees.keys())[-count:]
        return [self.employees[i] for i in ids]

def main():
    system = EmployeeManagementSystem()

    while True:
        print("\n1. Add Employee")
        print("2. Remove Employee")
        print("3. View All Employees")
        print("4. Calculate Payroll")
        print("5. View Recent Employees")
        print("6. Exit")

        try:
            choice = int(input("Choose an option: "))
            if choice == 1:
                emp_id = int(input("Enter ID: "))
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                position = input("Enter position (Manager/Engineer/Intern): ")
                salary = float(input("Enter salary: "))

                if position.lower() == "manager":
                    employee = Manager(emp_id, name, age, position, salary)
                elif position.lower() == "engineer":
                    employee = Engineer(emp_id, name, age, position, salary)
                elif position.lower() == "intern":
                    employee = Intern(emp_id, name, age, position, salary)
                else:
                    raise ValueError("Invalid position.")

                system.add_employee(employee)
                print("Employee added successfully.")

            elif choice == 2:
                emp_id = int(input("Enter employee ID to remove: "))
                system.remove_employee(emp_id)
                print("Employee removed successfully.")

            elif choice == 3:
                print("All Employees:")
                system.view_all_employees()

            elif choice == 4:
                total_payroll, avg_salary = system.calculate_payroll()
                print(f"Total Payroll: {total_payroll}, Average Salary: {avg_salary}")

            elif choice == 5:
                count = int(input("Enter number of recent employees to view: "))
                recent_emps = system.recent_employees(count)
                print("Recent Employees:")
                for emp in recent_emps:
                    print(emp.display())

            elif choice == 6:
                print("Exiting the system. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as ve:
            print(f"Value Error: {ve}")
        except KeyError as ke:
            print(f"Key Error: {ke}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
