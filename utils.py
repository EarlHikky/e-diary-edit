import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Subject, Teacher, Commendation


def get_schoolkid(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print(f'Неверно введено имя: "{name}" нет в базе данных.')
    except MultipleObjectsReturned:
        print('Неверно введено имя: найдено несколько человек. Уточните запрос.')


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for mark in bad_marks:
        mark.points = random.choice((4, 5))
        mark.save()


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def get_lesson(year_of_study, group_letter, subject):
    return Lesson.objects.filter(subject=subject,
                                 year_of_study=year_of_study,
                                 group_letter=group_letter
                                 ).order_by('-date').first()


def get_commendation_text():
    with open('commendations.txt', 'r', encoding='utf-8') as file:
        commendations = list((_.strip().split('.')[1] for _ in list(file)))
    return random.choice(commendations)


def get_subject(title, year_of_study):
    try:
        return Subject.objects.get(title=title, year_of_study=year_of_study)
    except ObjectDoesNotExist:
        print(f'Неверно введено название предмета: "{title}" нет в базе данных.')


def get_teacher(lesson):
    return Teacher.objects.get(pk=lesson.teacher_id)


def create_commendation(schoolkid, lesson, subject):
    text = get_commendation_text()
    created = lesson.date
    teacher = get_teacher(lesson)
    Commendation.objects.create(text=text,
                                created=created,
                                schoolkid=schoolkid,
                                subject=subject,
                                teacher=teacher
                                )


def main(name, subject_title):
    try:
        schoolkid = get_schoolkid(name)
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        year_of_study = schoolkid.year_of_study
        group_letter = schoolkid.group_letter
        subject = get_subject(subject_title, year_of_study)
        lesson = get_lesson(year_of_study, group_letter, subject)
        create_commendation(schoolkid, lesson, subject)
        print('Скрипт завершил работу успешно.')
    except AttributeError:
        print('Возникла проблема при выполнении скрипта.')


