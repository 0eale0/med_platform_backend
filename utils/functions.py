from datetime import datetime, date

CONSTANTS_FOR_MALE_OR_FEMALE = {'male': [66.5, 13.75, 5.003, 6.775], 'female': [655.1, 9.563, 1.85, 4.676]}
CONSTANTS_FOR_ACTIVITY_LEVEL = {
    'почти нет активности': 1.2,
    'умеренные нагрузки': 1.375,
    'тренировки 3-5 раз в неделю': 1.55,
    'интенсивные нагрузки': 1.725,
    'профессиональные спортсмены': 1.9,
}


def calculate_cpfc(height: float, weight: float, activity_level: str, birth_date: date, sex: str) -> tuple:
    age = (datetime.now().date() - birth_date).days // 365
    constants = CONSTANTS_FOR_MALE_OR_FEMALE[sex]
    calories = round(
        CONSTANTS_FOR_ACTIVITY_LEVEL[activity_level]
        * (constants[0] + weight * constants[1] + height * constants[2] - age * constants[3])
    )
    protein = round(calories * 0.3 / 4)
    fat = round(calories * 0.3 / 9)
    carbohydrate = round(calories * 0.1)
    return calories, protein, fat, carbohydrate
