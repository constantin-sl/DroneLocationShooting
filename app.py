import cProfile

from flask import Flask, jsonify, render_template, request, redirect, session
from models import db, LocationObj
from drone import Drone

app = Flask(__name__)
app.secret_key = 'qwerty'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///points.db'
db.init_app(app)
drone = Drone("База",(0.000000,0.000000))

# проход по всем локациям
def process_locations():
    location_objects = LocationObj.query.all()
    for loc in location_objects:
        drone.fly_to(loc.name, loc.coords)
        drone.panoramic_shot(loc.name)
        loc.status = True
        db.session.commit()


# Маршрут для начала миссии
@app.route('/start_mission')
def start_mission():
    # сбрасываем статус всех локаций
    location_objects = LocationObj.query.all()
    for loc in location_objects:
        loc.status = False
        db.session.commit()

    # начало миссии - взлетаем
    drone.takeoff(15)

    # отработка локации
    process_locations()

    # все локации пройдены, летим на базу
    drone.fly_to("База",drone.base_coords)
    drone.land()

    result_list = [{
        'name': loc.name,
        'coords': loc.coords,
        'status':loc.status
    } for loc in location_objects]
    return jsonify(result_list)



# Маршрут для главной страницы
@app.route('/')
def index():
    location_objects = LocationObj.query.all()
    if 'username' in session:
        return render_template('index.html', location_objects=location_objects)
    else:
        return redirect('/login')

# Добавление локации
@app.route('/add', methods=['GET', 'POST'])
def add_location_object():
    if request.method == 'POST':
        name = request.form['name']
        coords = request.form['coords']
        location_object = LocationObj(name=name, coords=coords, status=0)
        db.session.add(location_object)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


# Редактирование локации
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_location_object(id):
    location_object = LocationObj.query.get_or_404(id)
    if request.method == 'POST':
        location_object.name = request.form['name']
        location_object.coords = request.form['coords']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', location_object=location_object)


# Удаление локации
@app.route('/delete/<int:id>', methods=['POST'])
def delete_location_object(id):
    location_object = LocationObj.query.get_or_404(id)
    db.session.delete(location_object)
    db.session.commit()
    return redirect('/')


# Маршрут для страницы миссии
@app.route('/mission')
def mission():
    if 'username' in session:
        return render_template('mission.html')
    else:
        return redirect('/login')


# Маршрут для формы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'qwerty':
            session['username'] = username
            return redirect('/')  # Перенаправление на главную страницу после успешного входа
        else:
            error = "Неправильный логин или пароль. Пожалуйста, попробуйте снова."
    return render_template('login.html', error=error)


# Маршрут для выхода из системы
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
    cProfile.run('start_mission()')