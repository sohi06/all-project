from abc import ABC, abstractmethod
import datetime

class User(ABC):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def verify_password(self, password):
        return self.__password == password

    def get_username(self):
        return self.__username

    @abstractmethod
    def display_panel(self):
        pass


class Animal:
    def __init__(self, animal_id, name, species, health_status, enclosure, birth_date=None, parents=None, disease=None):
        self.__animal_id = animal_id
        self.__name = name
        self.__species = species
        self.__health_status = health_status
        self.__enclosure = enclosure
        self.__birth_date = birth_date if birth_date else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__parents = parents if parents else []
        self.__disease = disease

    def get_animal_id(self):
        return self.__animal_id

    def get_name(self):
        return self.__name

    def get_species(self):
        return self.__species

    def get_health_status(self):
        return self.__health_status

    def update_health_status(self, status):
        self.__health_status = status

    def get_enclosure(self):
        return self.__enclosure

    def update_disease(self, disease):
        self.__disease = disease

    def get_disease(self):
        return self.__disease

    def get_birth_date(self):
        return self.__birth_date

    def get_parents(self):
        return self.__parents

    def display(self):
        return f"ID: {self.__animal_id}, Name: {self.__name}, Species: {self.__species}, Health: {self.__health_status}, Enclosure: {self.__enclosure}, Birth Date: {self.__birth_date}, Disease: {self.__disease if self.__disease else 'N/A'}, Parents: {', '.join(self.__parents) if self.__parents else 'N/A'}"


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.__animals = {}
        self.__dead_animals = []
        self.__missing_animals = []

        # Add default animals to the zoo
        self.add_default_animals()

    def add_default_animals(self):
        # Adding 5 default animals with all required values
        default_animals = [
            Animal(1, "Lionel", "Lion", "Healthy", "Savannah", "2020-01-01", [], "None"),
            Animal(2, "Zara", "Zebra", "Healthy", "Grassland", "2021-02-15", [], "None"),
            Animal(3, "Ella", "Elephant", "Sick", "Savannah", "2019-03-25", [], "None"),
            Animal(4, "Milo", "Monkey", "Healthy", "Jungle", "2022-04-10", [], "None"),
            Animal(5, "Tina", "Tiger", "Healthy", "Forest", "2018-08-20", [], "None")
        ]

        for animal in default_animals:
            self.__animals[animal.get_animal_id()] = animal

    def add_animal(self, animal):
        if animal.get_animal_id() in self.__animals:
            raise ValueError("Animal ID already exists.")
        self.__animals[animal.get_animal_id()] = animal
        return f"Animal {animal.get_name()} added successfully."

    def add_newborn_animal(self, animal_id, name, species, health_status, enclosure, parents):
        birth_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        animal = Animal(animal_id, name, species, health_status, enclosure, birth_date, parents)
        return self.add_animal(animal)

    def mark_animal_missing(self, animal_id):
        if animal_id not in self.__animals:
            raise KeyError("Animal ID not found.")
        animal = self.__animals.pop(animal_id)
        self.__missing_animals.append(animal)
        return f"Animal {animal.get_name()} marked as missing."

    def found_missing_animal(self, animal_id):
        animal = None
        for i, missing_animal in enumerate(self.__missing_animals):
            if missing_animal.get_animal_id() == animal_id:
                animal = missing_animal
                del self.__missing_animals[i]
                break
        if not animal:
            raise KeyError("Missing Animal ID not found.")
        self.__animals[animal.get_animal_id()] = animal
        return f"Animal {animal.get_name()} found and moved back to main list."

    def view_animals(self):
        if not self.__animals:
            return "No animals in the zoo."
        return "\n".join([animal.display() for animal in self.__animals.values()])

    def view_dead_animals(self):
        if not self.__dead_animals:
            return "No dead animals."
        return "\n".join([f"ID: {animal.get_animal_id()}, Name: {animal.get_name()}, Species: {animal.get_species()}, Date of Death: {death_date}"
                          for animal, death_date in self.__dead_animals])

    def update_health_status(self, animal_id, status):
        if animal_id not in self.__animals:
            raise KeyError("Animal ID not found.")
        animal = self.__animals[animal_id]
        animal.update_health_status(status)

        if status.lower() == "dead":
            date_of_death = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.__dead_animals.append((animal, date_of_death))
            del self.__animals[animal_id]
            return f"Animal {animal.get_name()} marked as dead on {date_of_death}."

        return f"Updated health status of {animal.get_name()} to {status}."

    def update_disease(self, animal_id, disease):
        if animal_id not in self.__animals:
            raise KeyError("Animal ID not found.")
        animal = self.__animals[animal_id]
        animal.update_disease(disease)
        return f"Disease updated for {animal.get_name()} to {disease}."

    def search_animals(self, search_term):
        found_animals = []
        for animal in self.__animals.values():
            if search_term.lower() in animal.get_name().lower() or (animal.get_disease() and search_term.lower() in animal.get_disease().lower()):
                found_animals.append(animal)
        return "\n".join([animal.display() for animal in found_animals]) if found_animals else "No animals found."

    def display_panel(self):
        while True:
            print("\nAdmin Panel")
            print("1. Add Animal")
            print("2. Add Newborn Animal")
            print("3. View Animals")
            print("4. Update Animal Health Status")
            print("5. Update Animal Disease")
            print("6. View Dead Animals")
            print("7. Mark Animal Missing")
            print("8. Found Missing Animal")
            print("9. Search Animals by Name or Disease")
            print("10. Logout")
            admin_choice = input("Choose an option: ")

            if admin_choice == "1":
                try:
                    animal_id = int(input("Animal ID: "))
                    name = input("Name: ")
                    species = input("Species: ")
                    health_status = input("Health Status: ")
                    enclosure = input("Enclosure: ")
                    animal = Animal(animal_id, name, species, health_status, enclosure)
                    print(self.add_animal(animal))
                except ValueError as e:
                    print(f"Error: {e}")

            elif admin_choice == "2":
                try:
                    animal_id = int(input("Animal ID: "))
                    name = input("Name: ")
                    species = input("Species: ")
                    health_status = input("Health Status: ")
                    enclosure = input("Enclosure: ")
                    parents = input("Parents' Names (comma separated): ").split(",")
                    print(self.add_newborn_animal(animal_id, name, species, health_status, enclosure, parents))
                except ValueError as e:
                    print(f"Error: {e}")

            elif admin_choice == "3":
                print(self.view_animals())

            elif admin_choice == "4":
                try:
                    animal_id = int(input("Animal ID: "))
                    health_status = input("New Health Status: ")
                    print(self.update_health_status(animal_id, health_status))
                except KeyError as e:
                    print(f"Error: {e}")

            elif admin_choice == "5":
                try:
                    animal_id = int(input("Animal ID: "))
                    disease = input("Disease: ")
                    print(self.update_disease(animal_id, disease))
                except KeyError as e:
                    print(f"Error: {e}")

            elif admin_choice == "6":
                print(self.view_dead_animals())

            elif admin_choice == "7":
                try:
                    animal_id = int(input("Animal ID: "))
                    print(self.mark_animal_missing(animal_id))
                except KeyError as e:
                    print(f"Error: {e}")

            elif admin_choice == "8":
                try:
                    animal_id = int(input("Animal ID: "))
                    print(self.found_missing_animal(animal_id))
                except KeyError as e:
                    print(f"Error: {e}")

            elif admin_choice == "9":
                search_term = input("Enter name or disease to search: ")
                print(self.search_animals(search_term))

            elif admin_choice == "10":
                print("Logging out...")
                break

            else:
                print("Invalid choice.")


class ZooManagementSystem:
    def __init__(self):
        self.__users = {}

    def add_user(self, username, password, user_type):
        if username in self.__users:
            raise ValueError("Username already exists.")
        if user_type == "admin":
            self.__users[username] = Admin(username, password)
        else:
            raise ValueError("Invalid user type.")

    def login(self, username, password):
        if username not in self.__users:
            return None, "Username not found."
        user = self.__users[username]
        if not user.verify_password(password):
            return None, "Incorrect password."
        return user, f"Welcome {username}!"

    def sign_up(self, username, password):
        if username in self.__users:
            raise ValueError("Username already exists.")
        self.__users[username] = Admin(username, password)  # Default to Admin for simplicity
        print(f"User {username} signed up successfully.")


def main():
    zoo_system = ZooManagementSystem()

    # Predefined admin account
    zoo_system.add_user("admin", "admin123", "admin")

    while True:
        print("\n*** Zoo Management System ***")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user, message = zoo_system.login(username, password)
            print(message)

            if user:
                user.display_panel()

        elif choice == "2":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            try:
                zoo_system.sign_up(username, password)
            except ValueError as e:
                print(e)

        elif choice == "3":
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
