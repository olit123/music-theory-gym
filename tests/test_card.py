from card import CardSB, Points
import pytest

#TODO: TestCardSNB
#TODO: TestCardScorer

class TestCardSB():
    q = "wakey wakey"
    a = "eggs and bakey"
    c = CardSB(q, a)

    def test_get_q(self):
        assert self.c.get_q() == "wakey wakey"

    def test_default_points(self):
        # answer correctly
        r = self.c.answer("eggs and bakey")
        assert r.correct == True
        assert r.points == 1
        assert r.correct_answer == None

        # answer incorrectly
        r = self.c.answer("bacon and eggey")
        assert r.correct == False
        assert r.points == 0
        assert r.correct_answer == "eggs and bakey"

        # skip
        r = self.c.skip()
        assert r.correct == None
        assert r.points == 0
        assert r.correct_answer == "eggs and bakey"
    
    def test_answer_custom_points(self):
        c = CardSB(self.q, self.a, Points(5, -5.3, 1))

        # answer correctly
        r = c.answer("eggs and bakey")
        assert r.points == 5

        # answer incorrectly
        r = c.answer("rise and shine")
        assert r.points == -5.3

        # skip
        r = c.skip()
        assert r.points == 1

class TestPoints():
    def test_allowed_values(self):
        Points(10, -10.0, 1)

    def test_not_allowed_types(self):
        with pytest.raises(TypeError):
            Points("ten", False, "egg")
    
    def test_not_allowed_values(self):
        with pytest.raises(ValueError):
            Points(10.1, -5, -1)
            Points(8, -20)
    
    def test_get_points(self):
        p = Points(4, -4, 1)
        correct = p.get_correct()
        incorrect = p.get_incorrect()
        unanswered = p.get_unanswered()
        assert correct == 4
        assert incorrect == -4
        assert unanswered == 1
