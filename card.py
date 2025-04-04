from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import final, Any

type AnsFeedback = Any | None

# CARD PROPERTIES

class CardScorer(ABC):
    @abstractmethod #?
    def __init__(self):
        pass
    
    @abstractmethod #?
    def _compute_fractional_score(self, ans) -> tuple[float, AnsFeedback]:
        # When not overidden default behaviour could be to iterate through ans and marking strings and work out the fractional score from the length of the marking string and number of character matches? (e.g. if len is 100 and there are 95 matches the fractional score returned will be 0.95)
        # Overriden behaviours could include deriving from: a provided subscore / from number of regex matches / scored by AI 
        pass
    
    @final
    def get_fractional_score(self, ans) -> tuple[float, AnsFeedback]:
        fs, af = self._compute_fractional_score(ans)
        if fs < -1.0 or fs > 1.0:
            raise ValueError("Fractional score must range from -1.0 to 1.0 (inclusive)")
        return fs, af
    
class Points():
    def __init__(
            self, 
            correct: int | float = 1,
            incorrect: int | float = 0,
            unanswered: int | float = 0
    ):
        if (
            (not isinstance(correct, (int, float))) or
            (not isinstance(incorrect, (int, float))) or
            (not isinstance(unanswered, (int, float)))
        ):
            raise TypeError("Point types must be an int or float")
        if (
            (max(correct, incorrect, unanswered) > 10) or 
            (min(correct, incorrect, unanswered) < -10)
        ):
            raise ValueError("Point values must range from -10 to 10 (inclusive)")
        self.__correct = correct
        self.__incorrect = incorrect
        self.__unanswered = unanswered
    
    def get_correct(self):
        return self.__correct

    def get_incorrect(self):
        return self.__incorrect
    
    def get_unanswered(self):
        return self.__unanswered

@dataclass
class AnswerResult:
    correct: bool | None
    points: int | float
    correct_answer: Any | None

# CARD CLASSES

class Card(ABC):
    @abstractmethod
    def __init__(
        self, 
        q,
        points: Points,
    ):
        if not isinstance(points, Points): 
            raise TypeError("The points parameter must be an object of class 'Points'")
        self.__points = points
        self.__q = q
    
    @abstractmethod
    def answer(self, ans):
        pass

    @abstractmethod
    def skip(self):
        pass
    
    @final
    def get_q(self):
        return self.__q
    
    @final
    def _get_points(self):
        return self.__points

class CardSB(Card):
    def __init__(self, q, a, points: Points = Points()):
        super().__init__(q, points)
        self.__a = a
    
    def answer(self, ans):
        if ans != self.__a:
            return AnswerResult(False, self._get_points().get_incorrect(), self.__a)
        return AnswerResult(True, self._get_points().get_correct(), None)

    def skip(self):
        return AnswerResult(None, self._get_points().get_unanswered(), self.__a)

class CardSNB(Card):
    def __init__(self, q, scorer: CardScorer, points):
        if not isinstance(scorer, CardScorer): 
            raise TypeError("The scorer parameter must be an object of class 'CardScorer'")
        super().__init__(q, points)
        self.__scorer = scorer

    def answer(self, ans):
        # Get fractional score and answer feedback
        fs, af = self.__scorer.get_fractional_score(ans)
        if fs > 0:
            return self.__points * fs, af
        if fs < 0:
            return self.__points * abs(fs), af

# Rather than a 'Question and Answer' pair could a card be a 'Challenge'? (more abstract)
# Could there be a card class variant for exercises with non fixed times?

"""
Card Kinds
==========
- Basic
- MultipleChoice
- PinpointText
- AudioBasic
- ImageBasic
- ImagePinpoint
"""

"""
Card Classes
============
- SimpleCard
- ComplexCard
"""    
