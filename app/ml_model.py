import pickle
import pandas as pd
import numpy as np
from prometheus_client import Counter, Histogram

PREDICTION_COUNTER = Counter('wine_predictions_total', 'Total number of wine quality predictions')
PREDICTION_SCORE_HISTOGRAM = Histogram('wine_prediction_score', 'Histogram of predicted wine quality scores')


def ml_predict(fixed_acidity, volatile_acidity,
               critic_acid, residual_sugar, chlorides, free_sulfur_dioxide,
               total_sulfur_dioxide, density, pH, sulphates, alcohol):

    with open('loan_model_2.pkl', 'rb') as f:
        model = pickle.load(f)

    df = pd.DataFrame([[float(fixed_acidity), float(volatile_acidity),
               float(critic_acid), float(residual_sugar), float(chlorides), float(free_sulfur_dioxide),
               float(total_sulfur_dioxide), float(density), float(pH), float(sulphates), float(alcohol)]],
                      columns=['fixed_acidity', 'volatile_acidity',
               'critic_acid', 'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
               'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol'])

    predict = np.argmax(model.predict(df))

    PREDICTION_COUNTER.inc()
    PREDICTION_SCORE_HISTOGRAM.observe(predict)

    if predict > 5:
        return 'Вино хорошего качества, предсказанная оценка: {}/10'.format(predict)
    else:
        return 'Вино плохого качества, предсказанная оценка: {}/10'.format(predict)
