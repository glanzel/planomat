import os
import django
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'economic_comparison.settings')
django.setup()


from comparison.models import Economic, Question, Answer, UserAnswer


# Django-Umgebung einrichten

fake = Faker()

def create_economics(num=5):
    economics = []
    for _ in range(num):
        economic = Economic.objects.create(
            name=fake.company(),
            description=fake.paragraph()
        )
        economics.append(economic)
    return economics

def create_questions(num=10):
    questions = []
    for _ in range(num):
        question = Question.objects.create(
            text=fake.sentence()[:-1] + "?",  # Satz in Frage umwandeln
            description=fake.paragraph()
        )
        questions.append(question)
    return questions

def create_answers(economics, questions):
    answers = []
    for economic in economics:
        for question in questions:
            answer = Answer.objects.create(
                economic=economic,
                question=question,
                answer=random.choice(['agree', 'neutral', 'disagree']),
                description=fake.sentence()
            )
            answers.append(answer)
    return answers

def create_user_answers(questions, num_sessions=3):
    user_answers = []
    for _ in range(num_sessions):
        session_uuid = fake.uuid4()
        for question in questions:
            user_answer = UserAnswer.objects.create(
                question=question,
                answer=random.choice(['agree', 'neutral', 'disagree']),
                session_uuid=session_uuid
            )
            user_answers.append(user_answer)
    return user_answers

def main():
    print("Creating test data...")
    
    # Economics erstellen
    economics = create_economics()
    print(f"Created {len(economics)} economics")
    
    # Questions erstellen
    questions = create_questions()
    print(f"Created {len(questions)} questions")
    
    # Answers erstellen
    answers = create_answers(economics, questions)
    print(f"Created {len(answers)} answers")
    
    # UserAnswers erstellen
    user_answers = create_user_answers(questions)
    print(f"Created {len(user_answers)} user answers")
    
    print("Test data creation complete!")

if __name__ == "__main__":
    main()