import mysql.connector


class DatabaseHandler():

    HOST = "michael.iran.liara.ir"
    PORT = 31234
    USER = "root"
    PASSWORD = "jNcpS3aeeSriKVv4m81kgB7y"
    DATABASE = "confident_bassi"

    def __init__(self):
        self.db = self.connect()
        self.cursor = self.db.cursor(dictionary=True)
        self.create_table()

    def connect(self):
        return mysql.connector.connect(
            host=self.HOST, 
            port=self.PORT, 
            user=self.USER,
            password=self.PASSWORD, 
            database=self.DATABASE
        )

    def is_table_exists(self, table_name:str):
        try:
            self.cursor.execute(f"SHOW TABLES LIKE '{table_name.upper()}'")
            result = self.cursor.fetchone()
            if result is not None:
                return True
        except:
            pass
        return False

    def create_table(self):
        if not self.is_table_exists('uploads'):
            self.cursor.execute(
                f'CREATE TABLE UPLOADS ('
                f'    id INT NOT NULL AUTO_INCREMENT,'
                f'    email VARCHAR(255),'
                f'    inputs VARCHAR(255),'
                f'    language VARCHAR(255),'
                f'    enable BOOLEAN DEFAULT 0,'
                f'    PRIMARY KEY (id)'
                f');'
            )
        
        if not self.is_table_exists('jobs'):
            self.cursor.execute(
                f'CREATE TABLE JOBS ('
                f'    id INT AUTO_INCREMENT PRIMARY KEY,'
                f'    upload_id INT,'
                f'    job VARCHAR(255),'
                f'    executed BOOLEAN DEFAULT 0,'
                f'    FOREIGN KEY (upload_id) REFERENCES UPLOADS(id)'
                f');'
            )

        if not self.is_table_exists('results'):
            self.cursor.execute(
                f'CREATE TABLE RESULTS ('
                f'    id INT AUTO_INCREMENT PRIMARY KEY,'
                f'    job_id INT,'
                f'    output VARCHAR(255),'
                f'    done BOOLEAN DEFAULT 0,'
                f'    execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,'
                f'    FOREIGN KEY (job_id) REFERENCES JOBS(id)'
                f');'
            )
        
    def insert_uploads(self, email='', inputs='', language=''):
        sql = 'INSERT INTO UPLOADS (email, inputs, language) VALUES (%s, %s, %s)'
        val = (email, inputs, language)
        self.cursor.execute(sql, val)

        self.db.commit()
        print(self.cursor.rowcount, "record inserted to UPLOADS.")
        return self.cursor.lastrowid

    def insert_results(self, job_id):
        sql = 'INSERT INTO RESULTS (job_id) VALUES (%s)'
        val = (job_id,)
        self.cursor.execute(sql, val)

        self.db.commit()
        print(self.cursor.rowcount, "record inserted to RESULTS.")
        return self.cursor.lastrowid

    def insert_jobs(self, upload_id, job):
        sql = 'INSERT INTO JOBS (upload_id, job) VALUES (%s, %s)'
        val = (upload_id, job)
        self.cursor.execute(sql, val)

        self.db.commit()
        print(self.cursor.rowcount, "record inserted to JOBS.")
        return self.cursor.lastrowid

    def find(self, table_name, row_id, column_list='*'):
        if column_list == '*':
            sql = f"SELECT * FROM {table_name} WHERE ID = {row_id}"
        else:
            sql = f"SELECT {', '.join(column_list)} FROM {table_name} WHERE ID = {row_id}"
        self.cursor.execute(sql)

        return self.cursor.fetchone()

    def find_all(self, table_name, column_list='*'):
        if column_list == '*':
            sql = f"SELECT * FROM {table_name}"
        else:
            sql = f"SELECT {', '.join(column_list)} FROM {table_name}"
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def update(self, table_name, row_id, column_list, column_value):

        def pair2str(key, value):
            if isinstance(key, str):
                return f"{key}='{value}'"
            return f"{key}={value}"
        
        column_dict = dict(zip(column_list, column_value))
        assign_list = [pair2str(k, v) for k, v in column_dict.items()]
        sql = f"UPDATE {table_name} SET {', '.join(assign_list)} WHERE id = {row_id}"
        self.cursor.execute(sql)
        print(f'pairs updated: {assign_list}')

        self.db.commit()

    def delete(self, table_name, row_id):
        sql = f'DELETE FROM {table_name} WHERE ID = {row_id}'
        self.cursor.execute(sql)

        self.db.commit()
