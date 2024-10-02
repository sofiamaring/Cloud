import boto3

# Crear cliente S3
s3 = boto3.client('s3')

# Crear un bucket
def create_s3_bucket(bucket_name, region=None):
    try:
        # Si la región es us-east-1, no usar LocationConstraint
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f'Bucket {bucket_name} creado exitosamente.')
    except Exception as e:
        print(f'Error al crear el bucket: {e}')

# Ejemplo de uso
bucket_name = "parcial-bucket-danielsofia-1718"
region = "us-east-1"  # Región us-east-1 no necesita LocationConstraint
create_s3_bucket(bucket_name, region)

