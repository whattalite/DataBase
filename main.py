import sqlite3
from datetime import datetime, timedelta

def create_database():
    conn = sqlite3.connect('photomaterials_orders.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS partners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS manufacturers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        country TEXT,
        website TEXT,
        contact_info TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        manufacturer_id INTEGER,
        type_id INTEGER,
        article TEXT UNIQUE,
        price DECIMAL(10, 2) NOT NULL,
        shelf_life_days INTEGER,
        stock_quantity INTEGER DEFAULT 0,
        description TEXT,
        FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
        FOREIGN KEY (type_id) REFERENCES product_types(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        partner_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        required_date DATE,
        status TEXT DEFAULT 'Новая',
        total_amount DECIMAL(10, 2) DEFAULT 0,
        notes TEXT,
        FOREIGN KEY (partner_id) REFERENCES partners(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK(quantity > 0),
        price_per_unit DECIMAL(10, 2) NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        expiry_date DATE,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("База данных создана")

def insert_initial_data():
    conn = sqlite3.connect('photomaterials_orders.db')
    cursor = conn.cursor()
    
    product_types = [
        ('Пленка фотографическая', 'Пленка для фотоаппаратов'),
        ('Фотобумага', 'Бумага для печати'),
        ('Химические реактивы', 'Проявители, фиксажи'),
        ('Фотоаппараты', 'Цифровые и пленочные'),
        ('Объективы', 'Сменная оптика'),
        ('Аксессуары', 'Сумки, штативы')
    ]
    
    for type_name, desc in product_types:
        cursor.execute('INSERT OR IGNORE INTO product_types (name, description) VALUES (?, ?)', (type_name, desc))
    
    manufacturers = [
        ('Kodak', 'США', 'www.kodak.com', '+1-800-123-4567'),
        ('Fujifilm', 'Япония', 'www.fujifilm.com', '+81-3-1234-5678'),
        ('Canon', 'Япония', 'www.canon.com', '+81-3-5678-1234'),
        ('Nikon', 'Япония', 'www.nikon.com', '+81-3-9012-3456'),
        ('Ilford', 'Великобритания', 'www.ilfordphoto.com', '+44-20-1234-5678')
    ]
    
    for name, country, website, contact in manufacturers:
        cursor.execute('INSERT OR IGNORE INTO manufacturers (name, country, website, contact_info) VALUES (?, ?, ?, ?)', (name, country, website, contact))
    
    partners = [
        ('ФотоМир', 'Спиридонов Матвей', '+7-123-456-78-90', 'info@fotomir.ru', 'ул. Фотографическая, 10'),
        ('Цифра+', 'Керсанов Николай', '+7-098-765-43-21', 'sales@cifraplus.ru', 'пр. Мира, 25'),
        ('Тоо', 'Аомине Дайки', '+81-3-4821-9482', 'orders@too.photo.su', 'ул. Фукумы, 4')
    ]
    
    for name, contact, phone, email, address in partners:
        cursor.execute('INSERT OR IGNORE INTO partners (name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?)', (name, contact, phone, email, address))
    
    products = [
        ('Kodak Portra 400', 1, 1, 'KP400-135', 850.00, 365, 50, 'Цветная негативная пленка'),
        ('Fujifilm Velvia 50', 2, 1, 'FV50-120', 1200.00, 365, 30, 'Слайдовая пленка'),
        ('Fujifilm Instax Mini', 2, 2, 'INST-MN-10', 650.00, 730, 100, 'Мгновенная фотобумага'),
        ('Ilford HP5 Plus', 5, 1, 'HP5-400', 780.00, 540, 45, 'Черно-белая пленка'),
        ('Kodak Professional Endura', 1, 2, 'ENDURA-S', 3200.00, 1095, 25, 'Профессиональная фотобумага'),
        ('Canon EOS R5', 3, 4, 'CAN-R5-24', 350000.00, 730, 5, 'Беззеркальный фотоаппарат'),
        ('Nikon Z 7II', 4, 4, 'NIK-Z7II', 320000.00, 730, 3, 'Беззеркальный фотоаппарат'),
        ('Kodak D-76', 1, 3, 'KD76-1L', 450.00, 540, 20, 'Проявитель'),
        ('Fujifilm Fujichrome', 2, 1, 'FUJI-RDP3', 1650.00, 450, 15, 'Профессиональная слайдовая пленка'),
    ]
    
    for name, man_id, type_id, article, price, shelf_life, stock, desc in products:
        cursor.execute('''
            INSERT OR IGNORE INTO products 
            (name, manufacturer_id, type_id, article, price, shelf_life_days, stock_quantity, description) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, man_id, type_id, article, price, shelf_life, stock, desc))
    
    orders = [
        ('ORD-2024-001', 1, '2024-01-15', '2024-02-01', 'В обработке', 4250.00, 'Срочная заявка'),
        ('ORD-2024-002', 2, '2024-01-20', '2024-02-10', 'Новая', 7800.00, ''),
        ('ORD-2024-003', 3, '2024-01-25', '2024-02-15', 'Готова к отгрузке', 323200.00, 'Проверить сроки')
    ]
    
    for number, partner_id, order_date, req_date, status, total, notes in orders:
        cursor.execute('''
            INSERT OR IGNORE INTO orders 
            (order_number, partner_id, order_date, required_date, status, total_amount, notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (number, partner_id, order_date, req_date, status, total, notes))
    
    order_items = [
        (1, 1, 3, 850.00, 2550.00, '2025-01-15'),
        (1, 4, 2, 780.00, 1560.00, '2025-06-20'),
        (1, 8, 2, 450.00, 900.00, '2025-07-01'),
        (2, 2, 5, 1200.00, 6000.00, '2025-02-10'),
        (2, 3, 3, 650.00, 1950.00, '2026-01-15'),
        (3, 6, 1, 350000.00, 350000.00, '2026-01-20'),
        (3, 7, 1, 320000.00, 320000.00, '2026-01-20'),
        (3, 9, 2, 1650.00, 3300.00, '2025-05-15')
    ]
    
    for order_id, product_id, quantity, price, total, exp_date in order_items:
        cursor.execute('''
            INSERT OR IGNORE INTO order_items 
            (order_id, product_id, quantity, price_per_unit, total_price, expiry_date) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (order_id, product_id, quantity, price, total, exp_date))
    
    conn.commit()
    conn.close()
    print("Начальные данные загружены")

class PhotomaterialsOrderSystem:
    def __init__(self, db_name='photomaterials_orders.db'):
        self.db_name = db_name
    
    def _get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def get_all_orders(self, status=None):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT o.id, o.order_number, p.name as partner_name, 
                   o.order_date, o.required_date, o.status, o.total_amount
            FROM orders o
            JOIN partners p ON o.partner_id = p.id
        '''
        params = []
        
        if status:
            query += ' WHERE o.status = ?'
            params.append(status)
        
        query += ' ORDER BY o.order_date DESC'
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': o[0],
                'number': o[1],
                'partner': o[2],
                'order_date': o[3],
                'required_date': o[4],
                'status': o[5],
                'total': float(o[6])
            }
            for o in orders
        ]
    
    def get_order_items(self, order_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.name, p.article, m.name as manufacturer, 
                   oi.quantity, oi.price_per_unit, oi.total_price,
                   oi.expiry_date
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            JOIN manufacturers m ON p.manufacturer_id = m.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        
        items = cursor.fetchall()
        conn.close()
        
        return [
            {
                'product_name': i[0],
                'article': i[1],
                'manufacturer': i[2],
                'quantity': i[3],
                'price': float(i[4]),
                'total': float(i[5]),
                'expiry_date': i[6]
            }
            for i in items
        ]
    
    def create_order(self, order_data, items_data):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            order_number = f"ORD-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            cursor.execute('''
                INSERT INTO orders 
                (order_number, partner_id, required_date, notes, status, total_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                order_number,
                order_data['partner_id'],
                order_data['required_date'],
                order_data.get('notes', ''),
                'Новая',
                0
            ))
            
            order_id = cursor.lastrowid
            total_amount = 0
            
            for item in items_data:
                cursor.execute('SELECT price FROM products WHERE id = ?', (item['product_id'],))
                product = cursor.fetchone()
                if product:
                    price = float(product[0])
                    total_price = price * item['quantity']
                    total_amount += total_price
                    
                    cursor.execute('''
                        INSERT INTO order_items
                        (order_id, product_id, quantity, price_per_unit, total_price, expiry_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        order_id,
                        item['product_id'],
                        item['quantity'],
                        price,
                        total_price,
                        item.get('expiry_date')
                    ))
            
            cursor.execute('UPDATE orders SET total_amount = ? WHERE id = ?', (total_amount, order_id))
            conn.commit()
            return {'success': True, 'order_number': order_number}
            
        except Exception as e:
            conn.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            conn.close()
    
    def get_all_products(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.id, p.name, p.article, m.name, p.price, p.stock_quantity
            FROM products p
            JOIN manufacturers m ON p.manufacturer_id = m.id
            ORDER BY p.name
        ''')
        
        products = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': p[0],
                'name': p[1],
                'article': p[2],
                'manufacturer': p[3],
                'price': float(p[4]),
                'stock': p[5]
            }
            for p in products
        ]
    
    def get_all_partners(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name FROM partners ORDER BY name')
        partners = cursor.fetchall()
        conn.close()
        
        return [{'id': p[0], 'name': p[1]} for p in partners]

def run_demo():
    print("\n" + "="*60)
    print("Система управления заявками на фотоматериалы")
    print("="*60)
    
    system = PhotomaterialsOrderSystem()
    
    print("\n1. Текущие заявки:")
    print("-"*40)
    orders = system.get_all_orders()
    for order in orders:
        print(f"  № {order['number']} | {order['partner']} | {order['status']} | {order['total']:.2f} руб.")
    
    if orders:
        print(f"\n2. Продукция в заявке № {orders[0]['number']}:")
        print("-"*40)
        items = system.get_order_items(orders[0]['id'])
        for item in items:
            print(f"  • {item['product_name']} ({item['manufacturer']})")
            print(f"    {item['quantity']} шт. x {item['price']:.2f} = {item['total']:.2f} руб.")
            if item['expiry_date']:
                print(f"    Срок годности: {item['expiry_date']}")
    
    print("\n3. СОЗДАНИЕ НОВОЙ ЗАЯВКИ:")
    print("-"*40)
    
    partners = system.get_all_partners()
    products = system.get_all_products()
    
    if partners and products:
        new_order = {
            'partner_id': partners[0]['id'],
            'required_date': '2024-03-01',
            'notes': 'Тестовая заявка'
        }
        
        new_items = [
            {'product_id': products[0]['id'], 'quantity': 2, 'expiry_date': '2025-12-31'},
            {'product_id': products[1]['id'], 'quantity': 1, 'expiry_date': '2025-06-30'}
        ]
        
        result = system.create_order(new_order, new_items)
        if result['success']:
            print(f"Новая заявка создана. Номер: {result['order_number']}")
            
            print("\n4. Обновленный список заявок:")
            print("-"*40)
            orders = system.get_all_orders()
            for order in orders[:3]:
                print(f"  № {order['number']} | {order['partner']} | {order['status']} | {order['total']:.2f} руб.")
    
    print("\n" + "="*60)
    print("Система работает корректно.")
    print("="*60)

if __name__ == '__main__':
    print("Инициализация системы...")
    create_database()
    insert_initial_data()
    run_demo()
