import json
import boto3
#this script lives on an aws lambda function added to github for documentation 
client = boto3.client('iot-data', region_name='eu-west-2')

def unsnap(currentRev, angleToMove):
    if ((currentRev + angleToMove) >= 360):
        angleToMove = angleToMove - 360

    elif ((currentRev + angleToMove) <= -360):
        angleToMove = angleToMove + 360
    

    return angleToMove

def shortest_angle(targetAngle,currentAngle):
    num1 = targetAngle - currentAngle
    num2 = targetAngle - currentAngle + 360
    num3 = targetAngle - currentAngle - 360
    angleToMove = 0
    #smallest absolute value of the 3 numbers is the angle to move in
    if abs(num1) < abs(num2) and abs(num1) < abs(num3):
        angleToMove = num1
    elif abs(num2) < abs(num1) and abs(num2) < abs(num3):
        angleToMove = num2
    elif abs(num3) < abs(num1) and abs(num3) < abs(num1):
        angleToMove = num3
    else:
        angleToMove = 180

    return angleToMove
    
def high_wind_speed(winddirection, currentAngle, currentRev):
    ang1 = shortest_angle((winddirection + 90) % 360, currentAngle)
    ang2 = shortest_angle((winddirection - 90) % 360, currentAngle)
    result = 0
    if (abs(ang1) < abs(ang2)):
        result = ang1
    elif (abs(ang2) < abs(ang1)):
        result = ang2
    else:
        result = ang1
    
    result = unsnap(currentRev, result)
    currentAngle = (currentAngle + result) % 360
    currentRev += result
    return currentRev, result, currentAngle

def lambda_handler(event, context):
    if (event['speed'] < 50):
        atm = shortest_angle(event['direction'], event['currentAngle'])
        atm = unsnap(event['currentRev'], atm)
        ca = (event['currentAngle'] + atm) % 360
        cr = event['currentRev'] + atm
    else:
        cr, atm, ca = high_wind_speed(event['direction'], event['currentAngle'], event['currentRev'])
        
    data = {
        'currentRev' : cr,
        'angleToMove' : atm,
        'currentAngle' : ca
    }
    
    response = client.publish(
        topic= 'topic_4',
        qos=1,
        payload=json.dumps(data)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Published to topic_')
    }
