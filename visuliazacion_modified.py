import boto3
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
from io import BytesIO

# Función para descargar y cargar los datos reales desde la URL
def get_real_data():
    # URL proporcionada
    url = "https://www.datos.gov.co/resource/hk5x-635y.csv"
   
    # Leer los datos directamente desde la URL
    df = pd.read_csv(url)
   
    # Obtener el nombre de la última columna
    ultima_columna = df.columns[-1]
   
    # Filtrar las columnas que nos interesan (municipio y última columna)
    df = df[['municipio', ultima_columna]]
    return df, ultima_columna

# Función para generar la gráfica
def generar_grafica(df, ultima_columna):
    # Contar el número de colegios por año en cada municipio
    df_grouped = df.groupby(['municipio', ultima_columna]).size().reset_index(name='cantidad')
   
    # Crear la gráfica con Plotly
    fig = go.Figure()

    # Colores para cada año (puedes personalizar los colores si lo deseas)
    colores = ['red', 'orange', 'yellow', 'green', 'blue']

    # Agregar una traza por cada valor en la última columna
    for i, valor in enumerate(df_grouped[ultima_columna].unique()):
        # Filtrar el DataFrame para el valor actual
        df_filtrado = df_grouped[df_grouped[ultima_columna] == valor]

        fig.add_trace(go.Bar(
            x=df_filtrado['municipio'],
            y=df_filtrado['cantidad'],
            name=f'Clasificacion {valor}',
            marker_color=colores[i % len(colores)]
        ))

    # Configurar el layout de la gráfica
    fig.update_layout(
        title=f'Distribución por Municipio y {ultima_columna}',
        xaxis_title='Municipio',
        yaxis_title='Cantidad',
        barmode='stack',
        hovermode="x"
    )
   
    # Guardar la gráfica como archivo PNG en un objeto en memoria
    img_bytes = BytesIO(pio.to_image(fig, format='png'))
    return img_bytes

# Función para subir la imagen a S3
def subir_a_s3(img_bytes, bucket_name, file_name):
    # Crear un cliente de S3
    s3 = boto3.client('s3')
   
    # Subir la imagen al bucket S3
    img_bytes.seek(0)  # Asegurarse de que el puntero esté al principio
    s3.upload_fileobj(
        img_bytes,
        Bucket=bucket_name,
        Key=file_name,
        ExtraArgs={'ContentType': 'image/png'}
    )
    print(f'Imagen subida a {bucket_name}/{file_name}')

# Código principal
if __name__ == '__main__':
    # Obtener los datos y la última columna
    df, ultima_columna = get_real_data()

    # Generar la gráfica
    img_bytes = generar_grafica(df, ultima_columna)

    # Subir la imagen a S3
    bucket_name = 'parcial-bucket-danielsofia-1718'
    file_name = f'grafica_municipios_{ultima_columna}.png'
    subir_a_s3(img_bytes, bucket_name, file_name)
