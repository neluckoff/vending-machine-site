from flask import Flask, render_template, url_for, request
from database import Database

app = Flask(__name__)
db = Database()


@app.route('/', methods=['GET'])
def index():
    machines = db.get_machines()
    problems = db.get_problems()
    products = db.get_products(1)
    return render_template('index.html', machines=machines, problems=problems, products=products)
    

@app.route('/problem', methods=['POST'])
def problem():
    machine = request.form['select-machine']
    problem = request.form['select-problem']
    text = request.form['problem-desc']
    # db.set_break(automat_id=machine, break_id=problem, desc_break=text)
    return "Жалоба отправлена!"
    
    
@app.route('/order', methods=['POST'])
def order():
    machine = request.form['select-machine-to-buy']
    product = request.form['select-product']
    print(machine, problem)
    return render_template('confirm-page.html', head="Вы успешно приобрели товар!", text=f"Товар {product} был успешно приобретен в автомате №{machine}!", btn_text="Вернуться на главную")

@app.route('/admin', methods=['GET'])
def admin():
    machines = db.get_machines()
    problems = db.get_problems()
    products = db.get_products(1)
    return render_template('admin.html', machines=machines, problems=problems, products=products)
        
@app.route('/admin/machine', methods=['POST'])
def admin_machine():
    return "Автомат добавлен!"

@app.route('/admin/product', methods=['POST'])
def admin_product():
    return "Продукт добавлен!"

if __name__ == '__main__':
    app.run()