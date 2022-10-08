from typing import Dict, List, Type


class InfoMessage():
    """Информационное сообщение о тренировке."""

    def __init__(self, 
                 training_type: str, 
                 duration: float, 
                 distance: float, 
                 speed: float, 
                 calories: float 
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        """Возвращает сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000 
    LEN_STEP: float = 0.65 
    M_IN_H: int = 60

    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight: float
                 ) -> None:
        self.action = action 
        self.duration = duration 
        self.weight = weight 

    def get_distance(self) -> float:
        """Расчёт дистанции, которую пользователь преодолел за тренировку."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости движения во время тренировки."""
        distance = self.get_distance()
        return distance / self.duration 
    
    def get_spent_calories(self):
        """Расчет количества затраченных калорий во время тренировки."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Сообщение о выполненой тренировке."""
        return InfoMessage(self.__class__.__name__, 
                                   self.duration, 
                                   self.get_distance(), 
                                   self.get_mean_speed(),
                                   self.get_spent_calories()
                                   )


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Расход калорий для бега."""
        coeff_calorie_1 = 18 
        coeff_calorie_2 = 20 
        speed = self.get_mean_speed() 
        return ((coeff_calorie_1 * speed - coeff_calorie_2) * self.weight / 
                 Training.M_IN_KM * self.duration * Training.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_3: float = 0.035 
    COEFF_CALORIE_4: float = 0.029 

    def __init__(self, 
                 action, 
                 duration, 
                 weight, 
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height 

    def get_spent_calories(self) -> float:
        """Расчёт калорий при спортивной ходьбе."""
        
        average_speed = self.get_mean_speed() 
        return ((self.COEFF_CALORIE_3 * self.weight + (average_speed**2 // 
                 self.height) * self.COEFF_CALORIE_4 * self.weight) * 
                 self.duration * Training.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self, 
                 action, 
                 duration, 
                 weight, 
                 length_pool: float, 
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight) 
        self.length_pool = length_pool 
        self.count_pool = count_pool #сколько раз пользователь переплыл бассейн
    
    def get_mean_speed(self) -> float:
        """Расчет средней скорости пловца."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration
    
    def get_distance(self) -> float:
        """Расчёт дистанции, которую пользователь преодолел за тренировку."""
        return self.action * Swimming.LEN_STEP / Training.M_IN_KM 

    def get_spent_calories(self) -> float:
        """Расчёт калорий во время занятия плаванием."""
        coeff_calorie_5 = 1.1 
        average_speed = self.get_mean_speed() 
        return (average_speed + coeff_calorie_5) * 2 * self.weight


TRAINING: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running, 
        'WLK': SportsWalking
    }  

def read_package(workout_type: str, data: List[int]) -> Training:
    """Считывает данные полученные с датчиков."""
   
    if workout_type not in TRAINING:
        raise ValueError(f'Тренировка {workout_type} не обнаружена.')
    return TRAINING[workout_type](*data)

def main(training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [        
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training) 
