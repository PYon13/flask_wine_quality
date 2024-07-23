from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    id = HiddenField('WineId')
    fixed_acidity = FloatField('Фиксированная кислотность')
    volatile_acidity = FloatField('Летучая кислотность')
    critic_acid = FloatField('Лимонная кислота')
    residual_sugar = FloatField('Остаточный сахар')
    chlorides = FloatField('Хлориды')
    free_sulfur_dioxide = FloatField('Свободный диоксид серы')
    total_sulfur_dioxide = FloatField('Общий диоксид серы')
    density = FloatField('Плотность')
    pH = FloatField('Водородный показатель')
    sulphates = FloatField('Сульфаты')
    alcohol = FloatField('Алкоголь')
    quality = IntegerField('Оценка')
    submit = SubmitField('Сохранить')
    predict = SubmitField('Предсказать')
