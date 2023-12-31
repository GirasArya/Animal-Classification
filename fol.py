from logic import *
from utils import *
import os


def clear_terminal():
    os.system('cls')


class FolKB(KB):
    def __init__(self, initial_clauses=[]):
        self.clauses = []
        for clause in initial_clauses:
            self.tell(clause)

    def tell(self, sentence):
        if is_definite_clause(sentence):
            self.clauses.append(sentence)
        else:
            raise Exception("Not a definite clause: {}".format(sentence))

    def ask_generator(self, query):
        q = expr(query)
        test_variables = variables(q)
        answers = fol_bc_ask(self, q)
        return sorted([dict((x, v) for x, v in list(a.items())
                            if x in test_variables)
                       for a in answers], key=repr)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        return self.clauses

#query input to knowledge base
def get_characteristics(animal_name, kb):
    query = f'Characteristics({animal_name.lower()}, x)'
    result = kb.ask_generator(query)
    return result

#User input for characteristics of animal
def update_kb_with_new_animal(animal_name, kb):
    characteristics = []
    print(f"Let's add {animal_name} to our knowledge base.")

    has_fur = input("Does it have fur? (yes/no): ").lower() == 'yes'
    gives_milk = input("Does it give milk? (yes/no): ").lower() == 'yes'
    warm_blooded = input("Is it warm-blooded? (yes/no): ").lower() == 'yes'
    cold_blooded = input("Is it cold-blooded? (yes/no): ").lower() == 'yes'
    has_wings = input("Does it have wings? (yes/no): ").lower() == 'yes'
    lays_eggs = input("Does it lay eggs? (yes/no): ").lower() == 'yes'
    has_scales = input("Does it have scales? (yes/no): ").lower() == 'yes'
    has_exoskeleton = input("Does it have an exoskeleton? (yes/no): ").lower() == 'yes'
    has_slimy_skin = input("Does it have slimy skin? (yes/no): ").lower() == 'yes'
    live_land = input("Does it live in land? (yes/no): ").lower() == 'yes'
    live_water = input("Does it live in water? (yes/no): ").lower() == 'yes'
    #live_hybrid = input("Does it live in 2 places? (yes/no): ").lower() == 'yes'


    if has_fur:
        kb.tell(expr(f'HasFur({animal_name.lower()})'))
        characteristics.append('HasFur')
    if gives_milk:
        kb.tell(expr(f'GivesMilk({animal_name.lower()})'))
        characteristics.append('GivesMilk')
    if warm_blooded:
        kb.tell(expr(f'WarmBlooded({animal_name.lower()})'))
        characteristics.append('WarmBlooded')
    if cold_blooded:
        kb.tell(expr(f'ColdBlooded({animal_name.lower()})'))
        characteristics.append('ColdBlooded')
    if has_wings:
        kb.tell(expr(f'HasWings({animal_name.lower()})'))
        characteristics.append('HasWings')
    if lays_eggs:
        kb.tell(expr(f'LaysEggs({animal_name.lower()})'))
        characteristics.append('LaysEggs')
    if has_scales:
        kb.tell(expr(f'HasScales({animal_name.lower()})'))
        characteristics.append('HasScales')
    if has_exoskeleton:
        kb.tell(expr(f'HasExoskeleton({animal_name.lower()})'))
        characteristics.append('HasExoskeleton')
    if has_slimy_skin:
        kb.tell(expr(f'SlimySkin({animal_name.lower()})'))
        characteristics.append('SlimySkin')
    if live_land:
        kb.tell(expr(f'LiveLand({animal_name.lower()})'))
        characteristics.append('LiveLand')
    if live_water:
        kb.tell(expr(f'LiveWater({animal_name.lower()})'))
        characteristics.append('LiveWater')
    #if live_hybrid:
    #    kb.tell(expr(f'LiveHybrid({animal_name.lower()})'))
    #    characteristics.append('LiveHybrid')
    kb.tell(expr(f'Animal({animal_name.lower()})'))
    return characteristics


def determine_class(animal_name, kb):
    classes = ("Mammal", "Bird", "Reptile", "Fish", "Insect", "Amphibians")
    for c in classes:
        query = f'{c}({animal_name.lower()})'
        if kb.ask_generator(query):
            return c
    return None

def display_animal_table(animal_dict):
    animals = list(animal_dict.keys())
    num_rows = (len(animals) + 4) // 5  # Calculate the number of rows needed for 5x5 display

    print("\nTable of Animals:")
    for i in range(num_rows):
        row_start = i * 5
        row_end = min(row_start + 5, len(animals))
        row_animals = animals[row_start:row_end]
        print("".join("{:<20}".format(animal) for animal in row_animals))

animal_kb = FolKB(
    map(expr, [
       '(HasFur(m) & GivesMilk(m) & WarmBlooded(m) & LiveLand(m)) ==> Mammal(m)',
        '(HasWings(b) & LaysEggs(b) & WarmBlooded(b) & LiveLand(b)) ==> Bird(b)',
        '(HasScales(r) & LaysEggs(r) & ColdBlooded(r) & LiveLand(r)) ==> Reptile(r)',
        '(SlimySkin(a) & LaysEggs(a) & ColdBlooded(a) & LiveLand(a) & LiveWater(a)) ==> Amphibians(a)',
        '(HasScales(f) & LaysEggs(f) & ColdBlooded(f) & LiveWater(f)) ==> Fish(f)',
        '(HasExoskeleton(i) & LaysEggs(i) & ColdBlooded(i) & LiveLand(i)) ==> Insect(i)',
        ])
)


#Animal Dictionary
characteristics_dict = {
    'cow': ['HasFur', 'GivesMilk', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'dog': ['HasFur', 'GivesMilk', 'WarmBlooded', 'Carnivore', 'Mammal'],
    'cat': ['HasFur', 'GivesMilk', 'WarmBlooded', 'Carnivore', 'Mammal'],
    'monkey': ['HasFur', 'WarmBlooded', 'Omnivore', 'Mammal'],
    'zebra': ['HasStripes', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'giraffe': ['HasSpots', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'panda': ['HasBlackAndWhiteFur', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'penguin': ['HasFeathers', 'WarmBlooded', 'Carnivore', 'Bird'],
    'kangaroo': ['HasFur', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'lion': ['HasFur', 'WarmBlooded', 'Carnivore', 'Mammal'],
    'dolphin': ['HasSkin', 'WarmBlooded', 'Carnivore', 'Fins', 'Echolocation', 'Mammal'],
    'owl': ['HasFeathers', 'LaysEggs', 'Nocturnal', 'Carnivore', 'Bird'],
    'snake': ['HasScales', 'ColdBlooded', 'Carnivore','Venomous', 'Reptile'],
    'fish': ['HasScales', 'LaysEggs', 'ColdBlooded', 'Omnivore/Carnivore', 'Fins', 'Fish'],
    'butterfly': ['HasWings', 'ColdBlooded', 'Herbivore', "Insect"],
    'wolf': ['HasFur', 'WarmBlooded', 'Carnivore', 'Mammal'],
    'bear': ['HasFur', 'WarmBlooded', 'Omnivore', 'Hibernation', 'Mammal'],
    'horse': ['HasFur', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'elephant': ['HasSkin', 'WarmBlooded', 'Herbivore', 'Mammal'],
    'tiger': ['HasStripes', 'WarmBlooded', 'Carnivore', 'Mammal'],
    'frog': ['HasSmoothSkin', 'ColdBlooded', 'Insectivore', 'Amphibious', "Amphibians"],
    'turtle': ['HasShell', 'ColdBlooded', 'Herbivore/Omnivore', "Reptile"],
}

choose = 0

#Driver Code
while choose != '4':
    clear_terminal()
    print("\nWelcome to the animal classification app!!\n")
    print("What are we gonna do today:")
    print("1.) Animalia Class")
    print("2.) Identify Animal")
    print("3.) Animal Dictionary")
    print("4.) Exit")
    choose = input("Your choice (1/2/3): ")
    if choose == '1':
        print("- Amphibians are vertebrates known for their dual life stages, starting in water as larvae with gills and transitioning to land as adults with lungs, moist skin, and typically undergoing metamorphosis.")
        print("- Aves, or birds, are characterized by feathers, beaks, and laying hard-shelled eggs.")
        print("- Fish are aquatic vertebrates with gills, fins, and scales, utilizing these adaptations for respiration, movement, and protection in their underwater habitat.")
        print("- Insects, the largest class of arthropods, are characterized by six legs, a three-part body (head, thorax, and abdomen), and often wings, playing crucial roles in pollination, decomposition, and various ecological processes.")
        print('- Mammals are distinguished by their possession of fur or hair, the ability to produce milk for their young, and being warm-blooded.')
        print('- Reptiles are cold-blooded animals with scales or scutes, and they typically lay eggs for reproduction.')
        input("\nPress Enter to continue...")
    if choose == '2':
        animal_name = input("Enter the name of the animal: ")
        characteristics = update_kb_with_new_animal(animal_name, animal_kb)
        if characteristics:
            print("\n")
            print(f"{animal_name} has been added with the following characteristics:")
            for char in characteristics:
                print(f"- {char}")
        else:
            print(f"Unable to add '{animal_name}' to the knowledge base.")
        animal_class = determine_class(animal_name, animal_kb)
        print(f"The class of {animal_name} is: {animal_class}")
        input("\nPress Enter to continue...")
        clear_terminal()
        exec(open('fol.py').read())

    if choose == "3":
        display_animal_table(characteristics_dict)
        dictInput = input("\nWhat kind of species do you want to know? ").lower()
        animal_class = determine_class(dictInput, animal_kb)
        animalDictionary = characteristics_dict.get(dictInput)
        last_characteristic = characteristics_dict[dictInput][-1]
        if animalDictionary:
            print(f"\n{dictInput} has the following characteristics:")
            for char in animalDictionary:
                print(f"- {char}")
            print(f"\nThe class of {dictInput} is: {last_characteristic}")
        else:
            print(f"{dictInput} is not recognized in the knowledge base.")
        input("\nPress Enter to continue...")
        
