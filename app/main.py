from flask import Flask, render_template, url_for, request
from database import Database

app = Flask(__name__)
db = Database()


@app.route('/', methods=['GET'])
def index():
    machines = db.get_machines()
    machines_pr = db.get_machines_prob()
    problems = db.get_problems()
    products = db.get_products(1)
    return render_template('index.html', machines=machines, problems=problems, products=products, machines_pr=machines_pr)
    

@app.route('/problem', methods=['POST'])
def problem():
    machine = request.form['select-machine']
    problem = request.form['select-problem']
    text = request.form['problem-desc']
    db.set_break(automat_id=machine, break_id=problem, desc_break=text)
    return render_template('confirm-page.html', head="Вы успешно отправили жалобу на автомат!", text=f"Жалоба на автомат {machine} была успешно направлена на рассмотрение!", btn_text="Вернуться на главную", href="/")
    
    
@app.route('/order', methods=['POST'])
def order():
    machine = request.form['select-machine-to-buy']
    product = request.form['select-product']
    print(machine, problem)
    return render_template('confirm-page.html', head="Вы успешно приобрели товар!", text=f"Товар {product} был успешно приобретен в автомате №{machine}!", btn_text="Вернуться на главную", href="/")

@app.route('/admin', methods=['GET'])
def admin():
    machines = db.get_machines_prob()
    all_products = db.get_all_products()
    return render_template('admin.html', machines=machines, products=all_products)
        
@app.route('/admin/machine', methods=['POST'])
def admin_machine():
    geo = request.form['geo-machine']
    geo_desc = request.form['geo-decs-machine']
    ins_date = request.form['install-date']
    max_prod = request.form['max-products']
    db.new_machine(geo, geo_desc, ins_date, max_prod)
    return render_template('confirm-page.html', head=f"Автомат был успешно добавлен!", text=f"Вы успешно добавили автомат по адресу {geo},"
                           f" дата установки: {ins_date}, максимально продуктов: {max_prod}", btn_text="В Админ-Панель", href="/admin")

@app.route('/admin/product', methods=['POST'])
def admin_product():
    prod = request.form['prod']
    price = request.form['price-prod']
    desc = request.form['desc']
    added = request.form['date-added']
    before = request.form['before']
    db.new_product(prod, price, desc, added, before)
    return render_template('confirm-page.html', head=f"Продукт был успешно добавлен!", text=f"Вы успешно добавили продукт {prod},"
                           f" цена: {price}, описание: {desc}, дата добавления: {added}, срок годности: {before}", btn_text="В Админ-Панель", href="/admin")
    
@app.route('/admin/load', methods=['POST'])
def admin_load():
    machine = request.form['select-machine']
    product = request.form['select-product']
    num = request.form['prod-num']
    print(f'{machine} - {product} - {num}')
    db.add_product_to_machine(automat_id=int(machine), product_id=int(product), amount=int(num))
    return render_template('confirm-page.html', head=f"Продукт был успешно загружен!", text=f"Вы успешно добавили продукт №{product},"
                           f" в автомат №{machine} в количестве {num} штук.", btn_text="В Админ-Панель", href="/admin")
    

if __name__ == '__main__':
    app.run()