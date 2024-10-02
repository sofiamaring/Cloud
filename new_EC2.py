import boto3

# Crear cliente EC2
ec2 = boto3.client('ec2')

# Verificar si el grupo de seguridad ya existe
def get_or_create_security_group():
    group_name = 'lab4-security-group'
    
    # Verificar si el grupo de seguridad ya existe
    try:
        response = ec2.describe_security_groups(GroupNames=[group_name])
        security_group_id = response['SecurityGroups'][0]['GroupId']
        print(f'El grupo de seguridad {group_name} ya existe: {security_group_id}')
        return security_group_id
    except ec2.exceptions.ClientError as e:
        if 'InvalidGroup.NotFound' in str(e):
            print(f'El grupo de seguridad {group_name} no existe, se va a crear uno nuevo.')
        else:
            raise

    # Crear un grupo de seguridad que permita tráfico en SSH, HTTP, HTTPS y puerto 5000
    sg_response = ec2.create_security_group(
        Description='Permitir SSH, HTTP, HTTPS y puerto 5000',
        GroupName=group_name
    )
    security_group_id = sg_response['GroupId']
    print(f'Grupo de seguridad creado: {security_group_id}')
    
    # Agregar reglas de ingreso para SSH (22), HTTP (80), HTTPS (443) y puerto 5000
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Permitir SSH desde cualquier IP
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Permitir HTTP desde cualquier IP
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 443,
                'ToPort': 443,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Permitir HTTPS desde cualquier IP
            },
            {
                'IpProtocol': 'tcp',
                'FromPort': 5000,
                'ToPort': 5000,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Permitir puerto 5000 desde cualquier IP
            }
        ]
    )
    print(f'Reglas de seguridad añadidas al grupo {security_group_id}')
    
    return security_group_id

# Lanzar una instancia EC2 con IP pública
def launch_ec2_instance(security_group_id):
    user_data_script = '''#!/bin/bash
    sudo apt-get update -y
    sudo apt-get install -y apache2
    sudo systemctl start apache2
    sudo systemctl enable apache2
    '''
    
    response = ec2.run_instances(
        ImageId='ami-09a1c459d70c72b96',  # AMI de Ubuntu
        InstanceType='t2.micro',
        KeyName='vockey',  # Cambia por el nombre de tu par de claves
        MinCount=1,
        MaxCount=1,
        NetworkInterfaces=[
            {
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,  # Asignar una IP pública dinámica
                'Groups': [security_group_id]      # Grupo de seguridad
            }
        ],
      
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'Parcial-d-s'}]  # Cambia el nombre aquí
            }
        ],
        UserData=user_data_script,
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    print(f'Instancia EC2 lanzada: {instance_id}')
    return instance_id

def main():
    # Paso 1: Verificar o crear el grupo de seguridad
    security_group_id = get_or_create_security_group() 
    # Paso 2: Lanzar una instancia EC2 con IP pública
    instance_id = launch_ec2_instance(security_group_id)

    print(f'Todo configurado. Instancia EC2 {instance_id} está en ejecución.')

if __name__ == '__main__':
    main()
