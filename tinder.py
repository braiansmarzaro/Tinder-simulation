from people import Person
from names import get_full_name
import random
import pandas as pd


class Tinder:
    class Statistics:
        @classmethod
        def total_likes_received(cls, tinder):
            total = total_f = total_m = 0
            for u in sum(tinder.users.values(), start=[]):
                total += len(u.liked_me)
                if u.gender == 'f':
                    total_f += len(u.liked_me)
                elif u.gender == 'm':
                    total_m += len(u.liked_me)

            cls.totals = {'total': total, 'f': total_f, 'm': total_m}
            return cls.totals

        @classmethod
        def average_likes_received(cls, tinder):
            f_avg = cls.totals['f']/len(tinder.users['f'])
            m_avg = cls.totals['m']/len(tinder.users['m'])
            return {'f':round(f_avg,3),'m':round(m_avg,3)}

        @classmethod
        def matches_count(cls,tinder):
            f_matches = sum([len(u.match) for u in tinder.users['f']])
            m_matches = sum([len(u.match) for u in tinder.users['m']])
            cls.matches = {'f':f_matches,'m':m_matches}
            return cls.matches

        @classmethod
        def average_matches(cls,tinder):
            f_avg = cls.matches['f']/len(tinder.users['f'])
            m_avg = cls.matches['m']/len(tinder.users['m'])
            return {'f':round(f_avg,3),'m':round(m_avg,3)}
        
    def call_statistics(self):
        print('total likes received:',self.Statistics.total_likes_received(self))
        print('avg likes received:',self.Statistics.average_likes_received(self))
        print('total matches:',self.Statistics.matches_count(self))
        print('avg total matches:',self.Statistics.average_matches(self))

    def __init__(self, males=10, females=10,male_likes = 10, female_likes = 10) -> None:
        """
        Initialize a Tinder object.

        Parameters:
        - pool (int): The number of users to create in the Tinder pool.

        Returns:
        None
        """
        self.users: dict[str, list[Person]] = {'m': [], 'f': []}
        for _ in range(females):
            self.users['f'].append(Person(get_full_name(gender='female'),
                                          remaining_likes=male_likes,
                                          attractiveness=random.random(),
                                          like_probability=0.25,
                                          gender='f'))

        for _ in range(males):
            self.users['m'].append(Person(get_full_name(gender='male'),
                                          remaining_likes=female_likes,
                                          attractiveness=random.random(),
                                          like_probability=0.25,
                                          gender='m'))

        self.matches = pd.DataFrame(index=sorted(self.users['m']),
                                    columns=sorted(self.users['f']))

    def daily_swipe(self):
        """
        Perform daily swiping for all users.

        Parameters:
        None

        Returns:
        None
        """
        # Call the swipe for each person
        for f in self.users['f']:
            f.swipe(self.users['m'])
        for m in self.users['m']:
            m.swipe(self.users['f'])

    def get_match(self):
        """
        Calculate the matches between users.

        Parameters:
        None

        Returns:
        None
        """
        for people in self.users.values():
            for p in people:
                # self.matches.loc[p,p] = 0
                for other in p.liked_people:
                    if p in other.liked_people:
                        p.match.add(other)
                        other.match.add(p)

                        if p.gender == 'm':
                            self.matches.loc[p, other] = 1
                        elif p.gender == 'f':
                            self.matches.loc[other, p] = 1



if __name__ == "__main__":
    tinder = Tinder(males=500, females=500,
                    male_likes=100,female_likes=100)
    tinder.daily_swipe()
    tinder.get_match()
    #print(tinder.matches)
    #print(tinder.users)
    tinder.call_statistics()
