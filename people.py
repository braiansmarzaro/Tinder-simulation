import random
from names import get_full_name


class Person:
    def __init__(self, name, attractiveness, remaining_likes, like_probability, gender):
        self.like_probability = like_probability
        self.remaining_likes = remaining_likes
        self.attractiveness = attractiveness
        self.gender = gender
        self.name = name
        self.views = 0
        self.liked_people: set[Person] = set()
        self.liked_me: set[Person] = set()
        self.match: set[Person] = set()
        # Next improvements based on user location and self defined max range
        self.geo_position = None

    def single_swipe(self, person: 'Person', mode=0):
        #print(person.name)
        person.views+=1
        if mode == 0:
            if self.like_probability > random.random():
                self.liked_people.add(person)
                person.liked_me.add(self)
                self.remaining_likes -= 1
                #print('Liked')
        elif mode == 1:  # Considera attractiveness
            if self.like_probability*person.attractiveness > random.random():
                self.liked_people.add(person)
                person.liked_me.add(self)
                self.remaining_likes -= 1
                #print('Liked')
        

    def swipe(self, people_list):
        index = 0
        people = random.sample(people_list, k=len(people_list))
        while self.remaining_likes > 0 and index < len(people):
            self.single_swipe(people[index])
            index += 1

    def __str__(self) -> str:
        return self.name
    __repr__ = __str__

    def __gt__(self, other: 'Person'):
        return self.name > other.name

    def __lt__(self, other):
        return self.name < other.name


if __name__ == "__main__":
    users: dict[str, list[Person]] = {'m': [], 'f': []}
    for _ in range(10):
        users['f'].append(Person(get_full_name(gender='female'),
                          random.random(), 5, random.random(), 'f'))
        users['m'].append(Person(get_full_name(gender='male'),
                          random.random(), 5, random.random(), 'f'))
