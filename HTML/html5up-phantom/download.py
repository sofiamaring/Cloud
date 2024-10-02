import urllib.request
import boto3
from datetime import datetime

# Función para descargar datos desde la URL
def descargar_datos(url, output_file):
    response = urllib.request.urlopen(url)
    data = response.read()
    with open(output_file, 'wb') as file:
        file.write(data)

# Función para subir datos a S3
def subir_a_s3(bucket_name, file_name, s3_file_name):
    s3 = boto3.client('s3')
    s3.upload_file(file_name, bucket_name, s3_file_name)
    print(f"Archivo {s3_file_name} subido a S3 en el bucket {bucket_name}.")

if __name__ == "__main__":
    url_datos = "https://www.datos.gov.co/resource/hk5x-635y.csv"
    
    archivo_local = f"datos_estaciones_{datetime.now().strftime('%Y-%m-%d')}.csv"
    bucket_s3 = 'parcial-bucket-danielsofia-1718'
    archivo_s3 = f"datos_estaciones_{datetime.now().strftime('%Y-%m-%d')}.csv"
    descargar_datos(url_datos, archivo_local)
    subir_a_s3(bucket_s3, archivo_local, archivo_s3)