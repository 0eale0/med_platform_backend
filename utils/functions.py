from datetime import datetime, date

from sentry_sdk import capture_exception

CONSTANTS_FOR_MALE_OR_FEMALE = {'male': [66.5, 13.75, 5.003, 6.775], 'female': [655.1, 9.563, 1.85, 4.676]}
CONSTANTS_FOR_ACTIVITY_LEVEL = {
    'почти нет активности': 1.2,
    'умеренные нагрузки': 1.375,
    'тренировки 3-5 раз в неделю': 1.55,
    'интенсивные нагрузки': 1.725,
    'профессиональные спортсмены': 1.9,
}


def calculate_cpfc(height: float, weight: float, activity_level: str, birth_date: date, sex: str) -> tuple:
    try:
        age = (datetime.now().date() - birth_date).days // 365
        constants = CONSTANTS_FOR_MALE_OR_FEMALE[sex]
        calories = round(
            CONSTANTS_FOR_ACTIVITY_LEVEL[activity_level]
            * (constants[0] + weight * constants[1] + height * constants[2] - age * constants[3])
        )
        protein = round(calories * 0.2 / 4)
        fat = round(calories * 0.3 / 9)
        carbohydrate = round(calories * 0.5 / 4)
        return calories, protein, fat, carbohydrate
    except Exception as error:
        capture_exception(error)
        return None, None, None, None


# Functions for history
def changed_fields_with_values(history_obj, fields):
    changes = {}
    if history_obj.prev_record:
        delta = history_obj.diff_against(history_obj.prev_record)
        for change in delta.changes:
            if change.field in fields:
                changes["param_name"] = change.field
                changes["old"] = change.old
                changes["new"] = change.new
        return changes
    return None


def get_dict_with_changes(obj, max_count_of_changes, fields):
    result = []
    history_obj = obj.history.first()
    for i in range(max_count_of_changes):
        changes = changed_fields_with_values(history_obj, fields)
        if not changes:
            break
        date_value = history_obj.history_date.strftime("%Y-%m-%d %H:%M:%S")
        changes["date"] = date_value
        history_obj = history_obj.prev_record
        result.append(changes)

    return result
