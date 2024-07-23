from app import app, db
from app.ml_model import ml_predict
from app.forms import EditForm
from flask import render_template, redirect, request
from prometheus_client import start_http_server, generate_latest
from app.ml_model import ml_predict, PREDICTION_COUNTER, PREDICTION_SCORE_HISTOGRAM
from app.models import Wine
from sqlalchemy import func


start_http_server(8000)


@app.route('/metrics')
def metrics():
    return generate_latest()


@app.route('/')
@app.route('/index')
@app.route('/wines', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        db_wines = Wine.query.all()
        wines = []
        for w in db_wines:
            wines.append({
                'id': w.id,
                'fixed_acidity': w.fixed_acidity,
                'volatile_acidity': w.volatile_acidity,
                'critic_acid': w.critic_acid,
                'residual_sugar': w.residual_sugar,
                'chlorides': w.chlorides,
                'free_sulfur_dioxide': w.free_sulfur_dioxide,
                'total_sulfur_dioxide': w.total_sulfur_dioxide,
                'density': w.density,
                'pH': w.pH,
                'sulphates': w.sulphates,
                'alcohol': w.alcohol,
                'quality': w.quality
            })
        return render_template('home.html', title='Home', wines=wines)

    elif request.method == 'POST':
        wine_id = request.form['WineId']
        res = Wine.query.filter(Wine.id == wine_id).first()
        wine = {'id': wine_id,
                'fixed_acidity': res.fixed_acidity,
                'volatile_acidity': res.volatile_acidity,
                'critic_acid': res.critic_acid,
                'residual_sugar': res.residual_sugar,
                'chlorides': res.chlorides,
                'free_sulfur_dioxide': res.free_sulfur_dioxide,
                'total_sulfur_dioxide': res.total_sulfur_dioxide,
                'density': res.density,
                'pH': res.pH,
                'sulphates': res.sulphates,
                'alcohol': res.alcohol,
                'quality': res.quality}
        return render_template('wine.html', title='Home', wine=wine)


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        form = EditForm()
        if 'id' in request.args:
            form.id = request.args['id']
            wine = Wine.query.filter(Wine.id == request.args['id']).first()
            form.fixed_acidity.data = wine.fixed_acidity
            form.volatile_acidity.data = wine.volatile_acidity
            form.critic_acid.data = wine.critic_acid
            form.residual_sugar.data = wine.residual_sugar
            form.chlorides.data = wine.chlorides
            form.free_sulfur_dioxide.data = wine.free_sulfur_dioxide
            form.total_sulfur_dioxide.data = wine.total_sulfur_dioxide
            form.density.data = wine.density
            form.pH.data = wine.pH
            form.sulphates.data = wine.sulphates
            form.alcohol.data = wine.alcohol
            form.quality.data = wine.quality

        else:
            max_id = db.session.query(func.max(Wine.id)).scalar()
            if max_id is None:
                wine_id = 0

            else:
                wine_id = max_id + 1
            form.id = wine_id
        return render_template('edit.html', title='Home', form=form)

    elif request.method == 'POST':
        args = dict(request.form)
        fixed_acidity = args['fixed_acidity']
        volatile_acidity = args['volatile_acidity']
        critic_acid = args['critic_acid']
        residual_sugar = args['residual_sugar']
        chlorides = args['chlorides']
        free_sulfur_dioxide = args['free_sulfur_dioxide']
        total_sulfur_dioxide = args['total_sulfur_dioxide']
        density = args['density']
        pH = args['pH']
        sulphates = args['sulphates']
        alcohol = args['alcohol']
        quality = args['quality']
        wine_id = int(args['WineId'])

        ids = [i[0] for i in Wine.query.with_entities(Wine.id).all()]
        if wine_id in ids:
            wine = Wine.query.filter(Wine.id == wine_id).first()
            wine.fixed_acidity = fixed_acidity
            wine.volatile_acidity = volatile_acidity
            wine.critic_acid = critic_acid
            wine.residual_sugar = residual_sugar
            wine.chlorides = chlorides
            wine.free_sulfur_dioxide = free_sulfur_dioxide
            wine.total_sulfur_dioxide = total_sulfur_dioxide
            wine.density = density
            wine.pH = pH
            wine.sulphates = sulphates
            wine.alcohol = alcohol
            wine.quality = quality
            db.session.commit()

        else:
            new_wine = Wine(id=wine_id,
                            fixed_acidity=fixed_acidity,
                            volatile_acidity=volatile_acidity,
                            critic_acid=critic_acid,
                            residual_sugar=residual_sugar,
                            chlorides=chlorides,
                            free_sulfur_dioxide=free_sulfur_dioxide,
                            total_sulfur_dioxide=total_sulfur_dioxide,
                            density=density,
                            pH=pH,
                            sulphates=sulphates,
                            alcohol=alcohol,
                            quality=quality)
            db.session.add(new_wine)
            db.session.commit()
        return redirect('/index')

    else:
        return redirect('/index')


@app.route('/delete', methods=['GET'])
def del_wine():
    form_id = request.args['id']
    Wine.query.filter(Wine.id == form_id).delete()
    db.session.commit()
    return redirect('/index')


@app.route('/predictions', methods=['GET', 'POST'])
def get_prediction():
    if request.method == 'GET':
        form = EditForm()
        return render_template('predict.html', form=form, quality='')

    elif request.method == 'POST':
        args = request.form
        fixed_acidity = args['fixed_acidity']
        volatile_acidity = args['volatile_acidity']
        critic_acid = args['critic_acid']
        residual_sugar = args['residual_sugar']
        chlorides = args['chlorides']
        free_sulfur_dioxide = args['free_sulfur_dioxide']
        total_sulfur_dioxide = args['total_sulfur_dioxide']
        density = args['density']
        pH = args['pH']
        sulphates = args['sulphates']
        alcohol = args['alcohol']

        form = EditForm()
        form.fixed_acidity.data = fixed_acidity
        form.volatile_acidity.data = volatile_acidity
        form.critic_acid.data = critic_acid
        form.residual_sugar.data = residual_sugar
        form.chlorides.data = chlorides
        form.free_sulfur_dioxide.data = free_sulfur_dioxide
        form.total_sulfur_dioxide.data = total_sulfur_dioxide
        form.density.data = density
        form.pH.data = pH
        form.sulphates.data = sulphates
        form.alcohol.data = alcohol

        return render_template('predict.html', form=form, quality=str(ml_predict(
            fixed_acidity, volatile_acidity, critic_acid, residual_sugar, chlorides, free_sulfur_dioxide,
            total_sulfur_dioxide, density, pH, sulphates, alcohol)))


@app.route('/quality')
def quality():
    wine_id = request.args['id']
    wine = Wine.query.filter(Wine.id == wine_id).first()
    fixed_acidity = wine.fixed_acidity
    volatile_acidity = wine.volatile_acidity
    critic_acid = wine.critic_acid
    residual_sugar = wine.residual_sugar
    chlorides = wine.chlorides
    free_sulfur_dioxide = wine.free_sulfur_dioxide
    total_sulfur_dioxide = wine.total_sulfur_dioxide
    density = wine.density
    pH = wine.pH
    sulphates = wine.sulphates
    alcohol = wine.alcohol

    form = EditForm()
    form.fixed_acidity.data = fixed_acidity
    form.volatile_acidity.data = volatile_acidity
    form.critic_acid.data = critic_acid
    form.residual_sugar.data = residual_sugar
    form.chlorides.data = chlorides
    form.free_sulfur_dioxide.data = free_sulfur_dioxide
    form.total_sulfur_dioxide.data = total_sulfur_dioxide
    form.density.data = density
    form.pH.data = pH
    form.sulphates.data = sulphates
    form.alcohol.data = alcohol

    return render_template('quality.html', form=form, quality=str(ml_predict(
        fixed_acidity, volatile_acidity, critic_acid, residual_sugar, chlorides, free_sulfur_dioxide,
        total_sulfur_dioxide, density, pH, sulphates, alcohol)))


@app.route('/reset_db')
def reset_db():
    try:
        # Удалить все записи из таблицы Wine
        num_rows_deleted = db.session.query(Wine).delete()
        db.session.commit()
        return f"Deleted {num_rows_deleted} rows from Wine table."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"


@app.route('/reset_schema')
def reset_schema():
    try:
        # Удалить все таблицы и создать их заново
        db.drop_all()
        db.create_all()
        db.session.commit()
        return "Database schema has been reset."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}"