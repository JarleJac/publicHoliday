class Person:
    def __init__(self, name, address) -> None:
        self.name = name
        self.address = address
    def printMe(self):
        print(self.name, self.address)
        
        
class Student(Person):
    def __init__(self, name, address, courses) -> None:
        super().__init__(name, address)
        self.courses = courses
    def printMe(self):
        super().printMe()
        print(self.courses)
        
def printPerson(person: Person):
    person.printMe()
        
jarle = Person("Jarle Jacobsen", "Hjemme")
emil = Student("Emil Jacobsen", "Hos Jarle", ["Programming", "Python"])


printPerson(emil)
printPerson(jarle)
