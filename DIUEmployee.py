class Employee:
    def __init__(self, name, job_title, salary):
        self.name = name
        self.job_title = job_title
        self.salary = salary
    def getName(self):
        return self.nameper
    def display(self):
        print("Name:", self.name)
        print("Job Title:", self.job_title)
        print("Salary:", self.salary)

    def Raise(self, per):
        self.salary += (per / 100) * self.salary

emp1 = Employee("Franziska Waltraud", "HR Manager", 40000.0)
emp2 = Employee("Hubertus Andrea", "Software Engineer", 60000.0)

print("**********DIU Salary Management System**************\n")
print("Employee Details:")
emp1.display()
emp2.display()

emp1.Raise(8)
emp2.Raise(12)

print("After raising salary:\n")
print(f"8% for {emp1.getName()}")
emp1.display()

print(f"12% for {emp2.getName()}")
emp2.display()
