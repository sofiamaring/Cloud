import boto3
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import urllib.request
from io import BytesIO

# Función para descargar y cargar los datos reales desde la URL
def get_real_data():
    # URL proporcionada
    url = "https://www.datos.gov.co/resource/hk5x-635y.csv"
   
    # Leer los datos directamente desde la URL
    df = pd.read_csv(url)
   
    # Filtrar las columnas que nos interesan
    df = df[['municipio', 'a_o_2023']]
    return df

# Función para generar la gráfica
def generar_grafica(df):
    # Contar el número de colegios por año en cada municipio
    df_grouped = df.groupby(['municipio', 'a_o_2023']).size().reset_index(name='cantidad')
   
    # Crear la gráfica con Plotly
    fig = go.Figure()

    # Colores para cada año (puedes personalizar los colores si lo deseas)
    colores = ['red', 'orange', 'yellow', 'green', 'blue']

    # Agregar una traza por cada año
    for i, a_o_2023 in enumerate(df_grouped['a_o_2023'].unique()):
        # Filtrar el DataFrame para el año actual
        df_filtrado = df_grouped[df_grouped['a_o_2023'] == a_o_2023]

        fig.add_trace(go.Bar(
            x=df_filtrado['municipio'],
            y=df_filtrado['cantidad'],
            name=f'Clasificacion {a_o_2023}',
            marker_color=colores[i % len(colores)]
        ))

    # Configurar el layout de la gráfica
    fig.update_layout(
        title='Distribución por Municipio y Año',
        xaxis_title='Municipio',
        yaxis_title='Cantidad',
        barmode='stack',
        hovermode="x"
    )
   
    # Guardar la gráfica como archivo PNG en un objeto en memoria
    img_bytes = pio.to_image(fig, format='png')
    return img_bytes

# Función para subir la imagen a S3
def subir_a_s3(img_bytes, bucket_name, file_name):
    # Crear un cliente de S3
    s3 = boto3.client('s3')
   
    # Subir la imagen al bucket S3
    s3.upload_fileobj(
        BytesIO(img_bytes),
        Bucket=bucket_name,
        Key=file_name,
        ExtraArgs={'ContentType': 'image/png'}
    )
    print(f'Imagen subida a {bucket_name}/{file_name}')

# Código principal
if __name__ == '__main__':
    # Obtener los datos
    df = get_real_data()

    # Generar la gráfica
    img_bytes = generar_grafica(df)

    # Subir la imagen a S3
    bucket_name = 'parcial-bucket-danielsofia-1718'
    file_name = 'grafica_municipios_a_o_2023.png'
    subir_a_s3(img_bytes, bucket_name, file_name)