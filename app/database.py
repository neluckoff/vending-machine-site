import pymysql
import time

class Database:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='Dmitry9260304',
                database='vending_workbench'
            )
        except Exception as ex:
            print(ex)
            
        self.machines = self.__generate_machines()
        self.problems = self.__generate_problems()
            
    def __generate_machines(self):
        machines = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT `id`, `geo` FROM `automat`")
            rows = cursor.fetchall()
            for row in rows:
                machines.append([row[0], row[1]])
        return machines        

    def __generate_problems(self):
        problems = []
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT `id_code`, `name` FROM `break_codes`")
            rows = cursor.fetchall()
            for row in rows:
                problems.append([row[0], row[1]])
        return problems
    
    def get_machines(self):
        return self.machines
    
    def get_problems(self):
        return self.problems
    
    def set_break(self, automat_id: int, break_id: int, desc_break: str):
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
            
    def get_products(self, automat_id: int):
        with self.connection.cursor() as cursor:
            products = []
            cursor.execute(f'SELECT  product.id, product.name, product.description FROM product '
                            f'INNER JOIN automat_products ON automat_products.product_id = product.id '
                            f'WHERE automat_products.automat_id = {automat_id}')
            
            for row in cursor.fetchall():
                products.append([row[0], f'{row[1]} ({row[2]})'])
                
            return products