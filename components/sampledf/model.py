import pandas as pd

# df_costos = pd.read_csv('./data/dfsample/costos.csv')

# df_opsales = pd.read_csv('./data/dfsample/opsales.csv')

df_markers = pd.read_csv('./data/dfsample/table_top_speed.csv')

# df_table_top_speed = pd.read_csv('table_top_speed.csv', engine='pyarrow')
# dataset de prueba para el mapa
datatest = {
    '#': ['1', '2', '3', '4'],
    'MES': ['FEBRERO', 'DICIEMBRE', 'MARZO', 'JUNIO'],
    'PLACA': ['ABC12x', 'BCD452', 'PCL124', 'PER85Y'],
    'KM/h': ['186', '145', '123', '112'],
    'DEPARTAMENTO': ['SANTANDER', 'ANTIOQUIA', 'CUNDINAMARCA', 'BOYACA'],
    'COUNT': [99, 900, 9000, 900000],
    'COD_DPTO': ['68', '05', '25', '15']}

df_maptest = pd.DataFrame.from_dict(datatest)
