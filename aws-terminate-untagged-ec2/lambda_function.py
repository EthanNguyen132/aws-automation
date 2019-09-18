import boto3
import re, os

# ignore resources that are provisioned by pipeline, jenkins, automation script, etc.
DELIMITER = os.getenv('USER_DELIMITER') if os.getenv('USER_DELIMITER') else ','
USER_LIST = os.getenv('USER_LIST').split(DELIMITER) if os.getenv('USER_LIST') else ['pipeline']

def lambda_handler(event, context):
    # trigger by cloudtrail event
    user_arn = instances = event.get('detail').get('userIdentity').get('arn')
    instances = event.get('detail').get('responseElements').get('instancesSet').get('items')
    instances = filter(lambda instance: not is_created_by_pipeline(user_arn, USER_LIST) , instances)
    instance_info = list(map(lambda instance: 
        {
            'instance_id': instance.get('instanceId'),
            'tags': instance.get('tagSet').get('items') if instance.get('tagSet') else []
        }
    , instances))
    print('instance_info {}'.format(instance_info))
    ec2 = boto3.resource('ec2', region_name='ap-southeast-1')
    ec2_client = ec2.meta.client

    for instance in instance_info:
        tags = instance.get('tags')
        instance_id = instance.get('instance_id')
        for tag in tags:
            if tag.get('key') == 'PC-code':
                pc_code = tag.get('value') 
                if is_valid_pc_code(pc_code):
                    return
        print('Terminate instance {}'.format(instance.get('instance_id')))
        ec2.instances.filter(InstanceIds=[instance_id]).terminate()


def is_valid_pc_code(pc_code):
    pattern = re.compile("^[A-Za-z0-9]{4}$")
    return pattern.match(pc_code)

def is_created_by_pipeline(arn, excluded_user_list):
    if arn:
        bankId = arn.rsplit('/',1)[1]
        found = [username for username in excluded_user_list if bankId == username]
        return len(found) > 0
    # kill instances anyway if not found 1bank in arn
    return False