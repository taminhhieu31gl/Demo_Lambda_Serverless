import json
import os, re, base64
import boto3

def lambda_handler(event, context):
    
    mypage = page_router(event['httpMethod'],event['queryStringParameters'],event['body'])
    
    return mypage


def page_router(httpmethod,querystring,formbody):

    if httpmethod == 'GET':
        htmlFile = open('contactus.html', 'r')
        htmlContent = htmlFile.read()
        return {
        'statusCode': 200, 
        'headers': {"Content-Type":"text/html"},
        'body': htmlContent
        }
    
    if httpmethod == 'POST':
        
        insert_record(formbody)
        
        htmlFile = open('confirm.html', 'r')
        htmlContent = htmlFile.read()
        return {
        'statusCode': 200, 
        'headers': {"Content-Type":"text/html"},
        'body': htmlContent
        }    

def insert_record(formbody):
    
    formbody = formbody.replace("=", "' : '")
    formbody = formbody.replace("&", "', '")
    formbody = "INSERT INTO webtable value {'" + formbody +  "'}"
    
    client = boto3.client('dynamodb')
    client.execute_statement(Statement= formbody)
