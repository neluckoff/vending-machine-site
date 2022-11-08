import pymysql
import time

class Database:
    def __init__(self) -> None:
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='Dmitry9260304',
            database='vending_workbench'
        )
            
        self.machines_normal = self.__generate_machines()
        self.machines_problem = self.__generate_machines_with_problems()
        self.problems = self.__generate_problems()
            
    def __generate_machines(self) -> list:
        machines = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT `id`, `geo` FROM `automat` WHERE `condition` = 0")
            rows = cursor.fetchall()
            for row in rows:
                machines.append([row[0], row[1]])
        return machines  
    
    def __generate_machines_with_problems(self) -> list:
        machines = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT `id`, `geo` FROM `automat`")
            rows = cursor.fetchall()
            for row in rows:
                machines.append([row[0], row[1]])
        return machines        

    def __generate_problems(self) -> list:
        problems = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT `id_code`, `name` FROM `break_codes`")
            rows = cursor.fetchall()
            for row in rows:
                problems.append([row[0], row[1]])
        return problems
    
    def get_machines(self) -> list:
        return self.machines_normal
    
    def get_machines_prob(self) -> list:
        return self.machines_problem
    
    def get_problems(self) -> list:
        return self.problems
    
    def set_break(self, automat_id: int, break_id: int, desc_break: str) -> None:
        with self.connection.cursor() as cursor:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            id_breakdown = None
            cursor.execute(f'INSERT INTO `breakdowns` (break_code_id, descriprion, date)' 
                           f'VALUES ({break_id}, "{desc_break}", "{now}")')
            self.connection.commit()
            cursor.execute(f'SELECT `id` FROM `breakdowns` WHERE break_code_id = {break_id} AND descriprion = "{desc_break}"')
            for row in cursor.fetchall():
                id_breakdown = row[0]
            
            cursor.execute(f'INSERT INTO `break_history` (automat_id, breakdowns_id)' 
                           f'VALUES ({automat_id}, {id_breakdown})')
            self.connection.commit()
            
    def get_products(self, automat_id: int) -> list:
        with self.connection.cursor() as cursor:
            products = []
            cursor.execute(f'SELECT  product.id, product.name, product.description FROM product '
                            f'INNER JOIN automat_products ON automat_products.product_id = product.id '
                            f'WHERE automat_products.automat_id = {automat_id}')
            
            for row in cursor.fetchall():
                products.append([row[0], f'{row[1]} ({row[2]})'])
                
            return products
        
    def get_all_products(self) -> list:
        with self.connection.cursor() as cursor:
            products = []
            cursor.execute(f'SELECT product.id, product.name, product.description FROM product')
            
            for row in cursor.fetchall():
                products.append([row[0], f'{row[1]} ({row[2]})'])
                
            return products
        
    def new_machine(self, geo: str, geo_desc: str, install_date: str, max_products: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO `automat` (`geo`, `geo_description`, `installation_date`, `condition`, `max_number_products`)'
                           f'VALUES ("{geo}", "{geo_desc}", "{install_date}", {0}, "{max_products}")')
            self.connection.commit()
            
    def new_product(self, name: str, price: float, desc: str, date_added: str, before_date: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO `product` (`name`, `price`, `description`, `date_added`, `best_before_date`) '
                           f'VALUES ("{name}", {price}, "{desc}", "{date_added}", "{before_date}")')
            self.connection.commit()
            
    def add_product_to_machine(self, product_id: int, automat_id: int, amount: int) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT `automat_id`, `product_id` FROM `automat_products` WHERE `automat_id` = {automat_id} AND `product_id` = {product_id}')
            result = cursor.fetchall()
            if len(result) > 0:
                cursor.execute(f'SELECT `amount` FROM `automat_products` WHERE `automat_id` = {automat_id} AND `product_id` = {product_id}')
                old_amount = cursor.fetchall()[0][0]
                res_amount = old_amount + amount
                cursor.execute(f'UPDATE `automat_products` SET `amount` = {res_amount} WHERE `automat_id` = {automat_id} AND `product_id` = {product_id}')
            else:
                cursor.execute(f'INSERT INTO `automat_products` (`product_id`, `automat_id`, `amount`) VALUES ({product_id}, {automat_id}, {amount})')
            self.connection.commit()