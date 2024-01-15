import random
from names import get_full_name


class Person:
    def __init__(self, name, attractiveness, remaining_likes, like_probability, gender):
        """
        Initialize a Person object.

        Args:
            name (str): The name of the person.
            attractiveness (float): The attractiveness level of the person.
            remaining_likes (int): The number of remaining likes the person has.
            like_probability (float): The probability of the person liking another person.
            gender (str): The gender of the person.
        """
        self.like_probability = like_probability
        self.remaining_likes = remaining_likes
        self.attractiveness = attractiveness
        self.gender = gender
        self.name = name
        self.views = 0
        self.liked_people: set[Person] = set()
        self.liked_me: set[Person] = set()
        # self.match: set[Person] = set()
        # Next improvements based on user location and self defined max range
        self.geo_position = None
        self.max_range = None

    def single_swipe(self, person: 'Person', mode=0):
        """
        Perform a single swipe on another person.

        Args:
            person (Person): The person to swipe on.
            mode (int, optional): The swipe mode. Defaults to 0.
        """
        person.views += 1
        if mode == 0:
            if self.like_probability > random.random():
                self.liked_people.add(person)
                person.liked_me.add(self)
                self.remaining_likes -= 1
        elif mode == 1:  # Consider attractiveness
            if self.like_probability*person.attractiveness > random.random():
                self.liked_people.add(person)
                person.liked_me.add(self)
                self.remaining_likes -= 1

    def swipe(self, people_list):
        """
        Swipe on a list of people.

        Args:
            people_list (list[Person]): The list of people to swipe on.
        """
        index = 0
        people = random.sample(people_list, k=len(people_list))
        print(len(people))
        while self.remaining_likes > 0 and index < len(people):
            self.single_swipe(people[index])
            index += 1

    @property
    def match(self):
        """
        Get the set of people who have mutually liked each other.

        Returns:
            set[Person]: The set of matched people.
        """
        return self.liked_people.intersection(self.liked_me)

    def __str__(self) -> str:
        return self.name
    
    __repr__ = __str__

    def __gt__(self, other: 'Person'):
        return self.name > other.name

    def __lt__(self, other: 'Person'):
        return self.name < other.name


if __name__ == "__main__":
    users: dict[str, list[Person]] = {'m': [], 'f': []}
    for _ in range(500):
        users['f'].append(Person(get_full_name(gender='female'),
                          random.random(), 5, random.random(), 'f'))
        users['m'].append(Person(get_full_name(gender='male'),
                          random.random(), 5, random.random(), 'f'))
