import pandas as pd
import numpy as np
import requests
from geopy.geocoders import Nominatim
import mysql.connector



class Extraction:
    
    def __init__(self, country):
        self.country = country

    def create_dataframe(self):
        '''
        Función que accede a la API "Universities Hipolabs" y extrae información relacionada con la lista de paises deseados, facilitados en el constructor de la clase
        Parametros: una lista de paises (se facilita en el constructor de la clase)
        Return: Un dataframe con la información de todos los paises solicitados
        '''
        df = pd.DataFrame()
        for c in self.country:
            country = requests.get(url = f'http://universities.hipolabs.com/search?country={c}')
            df_country = pd.json_normalize(country.json())
            df = pd.concat([df, df_country], axis=0, ignore_index = True)
        return df



class Clean_Dataframe:  
    
    def __init__(self, df):
        self.df = df

    def clean_df(self):
        '''
        Función que limpia el dataframe cambiando el formato de algunas columnas, eliminando columnas necesarias o duplicadas, cambiando nulos por strings para facilitar su
        análisis y cambiando el orden de las columnas por otro más legible.
        Parametros: utiliza el fataframe, facilitado en el constructor de la clase
        Return: El dataframe limpio según necesidades específicas
        '''
        # drop 'domains' column
        (self.df).drop(columns = 'domains', inplace = True)

        clean_columns = {col:col.replace('-', '_').strip() for col in (self.df).columns}
        (self.df).rename(columns=clean_columns, inplace=True)

        # separate web_pages and drop duplicates by university name 
        self.df = (self.df).explode('web_pages', ignore_index=False)
        (self.df).drop_duplicates(subset = ['name'], inplace = True)

        # unify state names using external function
        self.df['state_province'] = self.df['state_province'].apply(change_states)

        # replace None for 'Uknown'
        self.df['state_province'] = self.df['state_province'].apply(lambda dato: 'Uknown' if dato == None else dato)

        col_order = ['country', 'state_province', 'name', 'web_pages', 'alpha_two_code']
        self.df = (self.df).reindex( columns = col_order)

        return self.df

    def lat_lon(self, application):
        '''
        Función que accede a la APY de geopy para extraer la latitud y la longitud de cada una de las localizaciones del dataframe (según los estados/provincias)
        Parametros: el nombre que queramos utilizar para acceder a la API geopy
        Return: El dataframe con una nueva columna con la información de latitud y longitud en función del estado o provincia
        '''
        self.application = application
        geolocator = Nominatim(user_agent=application)
        
        list_prov_country = []
        for _, c in self.df[['state_province', 'country']].iterrows():
            prov_count = (c[0]+ ', '+ c[1])
            list_prov_country.append(prov_count)
        list_pc = pd.DataFrame(list_prov_country)[0].unique()
        
        dict_provinces = {}
        for p in list_pc: 
            try: 
                location = geolocator.geocode(p)
                coord = (location.latitude, location.longitude)
                dict_provinces[p.split(',')[0]] = coord 
            except:
                dict_provinces[p.split(',')[0]]= 'Unknown' 
        self.df['coordinates'] = self.df['state_province'].map(dict_provinces, na_action="ignore")
        return self.df
    
    def clean_univesity_name(self, uni):
        '''
        Función específica de la columna de nombres de las universidades que sirve para unificar el formato y facilitar su inserción en la base de datos.
        Se aplicará con un apply
        Parametros: cada uno de los nombres de las universidades
        Return: El dataframe con la columna de nombres de universidades en el formato deseado
        '''
        self.uni = uni
        return uni.replace("'", "").replace('"', '')
        
    def save_df(self, save_name):
        '''
        Función que sirve para guardar el dataframe generado en formato csv
        Parametros: el nombre del dataframe
        Return: Un dataframe con la información de todos los paises solicitados
        '''
        self.save_name = save_name
        return (self.df).to_csv(f'../data/{save_name}.csv')

def change_states(state):
    '''
    Función que unifica los nombres de algunops de los es de USA y Argentina en función de las especificaciones solicitadas por el cliente. Se utilizará con un apply sobre la columna del dataframe
    Parametros: cada uno de los estados de la columna creada
    Return: cada uno de los nombres de los estados en el formato deseado
    '''
    if state == 'NV':
        return 'Nevada'
    elif state == 'TX':
        return 'Texas'
    elif state == 'CA':
        return 'California'
    elif state == 'VA':
        return 'Virginia'
    elif state == 'NY':
        return 'New York'
    elif state == 'MI':
        return 'Michigan'
    elif state == 'IN':
        return 'Indicanapolis'
    elif state == 'GA':
        return 'Georgia'
    elif state == 'ND':
        return 'North Dacota'
    elif state == 'New York, NY':
        return 'New York'
    elif state == 'Ciudad Autónoma de Buenos Aires':
        return 'Buenos Aires'
    else:
        return state

class Create_Database:
    
    def __init__(self, name_ddbb = 'country_universities', my_pass = 'AlumnaAdalab'):
        self.name_ddbb = name_ddbb
        self.my_pass = my_pass

    def create_ddbb(self):
        '''
        Función para crear una base de datos enMySQL Workbench.
        Parametros: Utiliza los parámetros por defecto faiclitados en el consructor (nombre de la base de datos y contraseña)
        Return: Base de datos creada en MySQL Workbench
        '''
        mydb = mysql.connector.connect(host="localhost", user="root", password=f'{self.my_pass}') 
        print("Connected to MySQL")
        
        mycursor = mydb.cursor()

        try:
            mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.name_ddbb};")
            print('Data Base created correctly')
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)

    def insert_table(self, query):
        '''
        Función que sirve para insertar tablas y datos a través de querys en la base de datos
        Parametros: Utiliza los parámetros por defecto faiclitados en el consructor (nombre de la base de datos y contraseña) y la query que deseemos utilizar
        Return: El resultado de la query facilitada
        '''
        self.query = query
        cnx = mysql.connector.connect(user='root', password=f"{self.my_pass}", host='localhost', database=f"{self.name_ddbb}")
        mycursor = cnx.cursor()
    
        try: 
            mycursor.execute(query)
            cnx.commit() 
            
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)    

    def get_idstate(self, state):
        '''
        Función para extraer los ids de los estados generados en la inserción de los datos de manera aut-incremental
        Parametros: Utiliza los parámetros por defecto faiclitados en el consructor (nombre de la base de datos y contraseña) y el nombre de cada estado
        Return: El (IDs) del estado de la tabla 'countries' solicitado
        '''
        self.state = state

        cnx = mysql.connector.connect(user='root', password=f"{self.my_pass}", host='localhost', database=f"{self.name_ddbb}")
        mycursor = cnx.cursor()
        
        try:
            query_get_idstate = f'SELECT idstate FROM countries WHERE state_name = "{state}"'
            mycursor.execute(query_get_idstate)

            id_ = mycursor.fetchone()[0]
            return id_
        
        except: 
            return 'State not in database'
        

# QUERYS de creación de las tablas según las especificaciones solicitadas por el cliente
query_country = ''' CREATE TABLE IF NOT EXISTS `country_universities`.`countries` (
                    `idstate` INT NOT NULL AUTO_INCREMENT,
                    `country_name`VARCHAR (45),
                    `state_name` VARCHAR (45),
                    `latitud` FLOAT,
                    `longitud` FLOAT,
                    PRIMARY KEY (`idstate`))
                    ENGINE = InnoDB;
                    '''

query_universities = ''' CREATE TABLE IF NOT EXISTS `country_universities`.`university` (
                    `iduniversity` INT NOT NULL AUTO_INCREMENT,
                    `university_name`VARCHAR (100),
                    `web_page` VARCHAR (100),
                    `idstate` INT,
                    PRIMARY KEY (`iduniversity`),
                    CONSTRAINT `fk_univ_country`
                            FOREIGN KEY (`idstate`)
                            REFERENCES `country_universities`.`countries` (`idstate`)
                    ) ENGINE = InnoDB;
                    '''