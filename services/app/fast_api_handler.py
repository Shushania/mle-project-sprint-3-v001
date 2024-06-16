# coding: utf-8
"""Класс FastApiHandler, который обрабатывает запросы API."""
import os
import dill
import pandas as pd

REQUIRED_PARAMS = [
    'floor', 'is_apartment', 'kitchen_area', 'living_area', 'rooms',
    'total_area', 'building_id', 'build_year', 'building_type_int', 
    'latitude', 'longitude', 'ceiling_height', 'flats_count', 'floors_total', 
    'has_elevator'
]

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""
        self.model_path = os.path.join(os.getcwd(), 'models', 'model.pkl')
        self.model = self.load_model()
        self.required_model_params = REQUIRED_PARAMS

    def load_model(self):
        """Загружаем обученную модель.
        Args:
            model_path (str): Путь до модели.
        """
        try:
            print(os.path.join(os.getcwd(), 'models', 'model.pkl'))
            with open(self.model_path, 'rb') as model_file:
                return dill.load(model_file)
        except Exception as e:
            print(f"Failed to load model: {e}")
            raise e

    def price_predict(self, model_params: dict) -> float:
        df_sample = pd.DataFrame(model_params, index=[0])
        return self.model.predict(df_sample)[0]
        
    
    def validate_params(self, params: dict) -> bool:
        """Разбираем запрос и проверяем его корректность.
        """
        if set(params.keys()) == set(self.required_model_params):
            print("There are all model params")
        else:
            print("There are not all model params")
            return False
        return True
		
    def handle(self, params):
        """Функция для обработки запросов API параметров входящего запроса.
    
        Args:
            params (dict): Словарь параметров запроса.
    
        Returns:
            - **dict**: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                predicted_price = self.price_predict(params)
                response = {"score": predicted_price}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response

if __name__ == "__main__":

    # Создаем тестовый запрос
    test_params = {
        'floor': 5,
        'is_apartment': 1,
        'kitchen_area': 9.96964507713912,
        'living_area': 35.86870401552872,
        'rooms': 2,
        'total_area': 50.88379993853673,
        'building_id': 720,
        'build_year': 1950,
        'building_type_int': 7,
        'latitude': 55.01683339518647,
        'longitude': 37.700019545033655,
        'ceiling_height': 1.5778684705378447,
        'flats_count': 215,
        'floors_total': 39,
        'has_elevator': 0
 }

    # Создаем обработчик запросов для API
    handler = FastApiHandler()

    # Делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")
