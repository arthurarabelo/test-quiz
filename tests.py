import pytest
from model import Question

@pytest.fixture
def data():
    question = Question(title='q1')
    question.add_choice('a', is_correct=True)
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d', is_correct=True)
    return question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct
    
def test_create_choice_with_invalid_text():
    question = Question(title='q1')
    
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a'*101)
    with pytest.raises(Exception):
        question.add_choice('a'*200)
    
def test_remove_choice():
    question = Question(title='q1')
    
    question.add_choice('a')
    
    choice = question.choices[0]
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0
    
def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    
    question.add_choice('a')
    question.add_choice('b')
    choice = question.choices[0]
    
    with pytest.raises(Exception):
        question.remove_choice_by_id(3)
    
    
def test_remove_all_choices():
    question = Question(title='q1')
    
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    
    question.remove_all_choices()
    assert len(question.choices) == 0
    
def test_set_correct_choices_with_invalid_id():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    
    with pytest.raises(Exception):
        question.set_correct_choices([1, 3, 5])
        
def test_set_correct_choices():
    question = Question(title='q1')

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    
    question.set_correct_choices([1, 3])
    
    correct_choices = [choice for choice in question.choices if choice.is_correct]
    
    assert len(correct_choices) == 2
    assert correct_choices[0].id == 1
    assert correct_choices[1].id == 3
        
def test_set_all_correct_choices():
    question = Question(title='q1', max_selections=4)

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    
    question.set_correct_choices([1, 2, 3, 4])
    
    correct_choices = question.correct_selected_choices([1, 2, 3, 4])
    
    assert len(correct_choices) == len(question.choices)
    
def test_more_than_maximum_selections():
    question = Question(title='q1', max_selections=1)
    
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')
    
    choiceA = question.choices[0]
    choiceC = question.choices[2]
    selected_choices = [choiceA.id, choiceC.id]
        
    with pytest.raises(Exception):
        question.correct_selected_choices(selected_choices)
        
def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)

    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    question.add_choice('d')

    choiceA = question.choices[0]
    choiceC = question.choices[2]
    selected_choices = [choiceA.id, choiceC.id] 

    question.set_correct_choices([choiceC.id])
    correct_choices = question.correct_selected_choices(selected_choices)
    
    assert len(correct_choices) == 1
    assert correct_choices[0] ==  choiceC.id
    
def test_complete_selection():
    question = Question(title="What is 2+2?", points=5, max_selections=1)
    
    question.add_choice("a")
    question.add_choice("b", is_correct=True)
    question.add_choice("c")
    question.add_choice("d")
    
    correct_choices = question.correct_selected_choices([2])
    assert len(correct_choices) == 1
    assert correct_choices[0] == 2

def test_correct_selected_with_fixture(data):
    correct_choices = data.correct_selected_choices([1])
    assert len(correct_choices) == 1
    assert correct_choices[0] == 1

def test_set_correct_choices_with_fixture(data):
    data.set_correct_choices([2, 3])
    
    new_correct = [choice.id for choice in data.choices if choice.is_correct]
    assert new_correct == [1, 2, 3, 4]
        
    