import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import shap
import matplotlib.pyplot as plt
from telegram import Bot
from config import settings
from user_config import user_settings

def find_shap(gt, target):
    # Загружаем данные из Google Sheet в DataFrame
    df = gt._load_data_as_dataframe(googlesheet_url=settings["TABLE_URL"], sheet_name="Sheet1")
    
    # Преобразуем данные в правильные типы (float для всех столбцов)
    try:
        df = df.astype(float)
    except ValueError as e:
        print(f"Error converting to float: {e}")
    
    # Печатаем первые строки DataFrame для проверки
    #print(df.head())
    
    # Целевая переменная и признаки
    y = df[target]
    X = df.drop(columns=[target])
    
    # Разделение данных на обучающую и тестовую выборки
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Инициализация и обучение модели случайного леса
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    # Создание объекта Explainer и вычисление SHAP значений
    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_test)
    
    # Визуализация важности признаков и сохранение графика
    plt.figure()
    shap.summary_plot(shap_values, X_test, show=False)
    plt.savefig('shap_summary_plot.png')
    
def send_image_to_user(image_path):
    bot = Bot(token=settings["TOKEN"])
    chat_id = user_settings["CHAT_ID"]
    with open(image_path, 'rb') as image_file:
        bot.send_photo(chat_id=chat_id, photo=image_file)
