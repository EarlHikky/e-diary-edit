import random

from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Subject, Teacher, Commendation


def get_schoolkid(name):
    return Schoolkid.objects.get(full_name__contains=name)


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lte=3).update(points=5)


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
    return Subject.objects.get(title=title, year_of_study=year_of_study)


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

    except Schoolkid.DoesNotExist:
        print(f'Неверно введено имя: "{name}" нет в базе данных.')
    except Schoolkid.MultipleObjectsReturned:
        print('Неверно введено имя: найдено несколько человек. Уточните запрос.')

    except Subject.DoesNotExist:
        print(f'Неверно введено название предмета: "{subject_title}" нет в базе данных.')
    except Subject.MultipleObjectsReturned:
        print('Найдено несколько предметов с одинаковым названием.')

    except Teacher.DoesNotExist:
        print('Учитель не найден в базе данных.')
    except Teacher.MultipleObjectsReturned:
        print('Найдено несколько учителей с одинаковым id.')

    except Lesson.DoesNotExist:
        print('Урок не найден в базе данных.')
    except Lesson.MultipleObjectsReturned:
        print('Найдено несколько одинаковых уроков.')

    except Mark.DoesNotExist:
        print('Не найдено оценок в базе данных.')
    except Mark.MultipleObjectsReturned:
        print('Найдено несколько одинаковых оценок.')

    except Chastisement.DoesNotExist:
        print('Замечание не найдено в базе данных.')
    except Chastisement.MultipleObjectsReturned:
        print('Найдено несколько одинаковых замечаний.')

    except FileNotFoundError:
        print('Не найден файл с рекомендациями.')
