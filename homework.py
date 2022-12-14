class InfoMessage:
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

    def get_message(self):
        return f'Тип тренировки: {self.training_type};' \
               f' Длительность: {self.duration:.3f} ч.;' \
               f' Дистанция: {self.distance:.3f} км;' \
               f' Ср. скорость: {self.speed:.3f} км/ч;' \
               f' Потрачено ккал: {self.calories:.3f}.'


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_name: str = "Тип не задан"

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_covered = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_covered

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        average_speed = self.get_mean_speed()
        spent_calories = \
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * average_speed
             + self.CALORIES_MEAN_SPEED_SHIFT) \
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H

        return spent_calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        average_speed = self.get_mean_speed()
        spent_calories = \
            ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
              + ((average_speed * self.KMH_IN_MSEC) ** 2
                 / self.height * self.CM_IN_M)
              * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
             * self.duration * self.MIN_IN_H)
        return spent_calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN_SPEED_SHIFT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        average_speed = \
            self.length_pool * self.count_pool / self.M_IN_KM \
            / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        speed = self.get_mean_speed()
        spent_calories = \
            (speed + self.CALORIES_MEAN_SPEED_MULTIPLIER) * \
            self.CALORIES_MEAN_SPEED_SHIFT * \
            self.weight * self.duration
        return spent_calories

    def show_training_info(self) -> InfoMessage:
        return super().show_training_info()


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training: dict[str, Training()] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    if workout_type in types_of_training:
        return types_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
