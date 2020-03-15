import return_data
import boto3
import json
import os

# S3に保存したファイルを読み込んでjsonで返す
s3 = boto3.client('s3')
def getfile_from_s3(bucket_name,file_name):
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    body = response['Body'].read()
    bodystr = body.decode('utf-8')
    jsn = json.loads(bodystr)

    return jsn

# S3のバケット名はユニークなので公開せずLambdaの環境変数で定義
backet_name = os.environ['VAR_BUCKET_NAME']

# データをまとめる(タプルで返ってくる)(ファイル名やフォーマットは各地域で異なるはずなので適宜修正して使ってください)
contacts_data = getfile_from_s3(backet_name,'covid19-development/data/contacts.json')
latest_patients_data = getfile_from_s3(backet_name,'covid19-development/data/current_patients.json')
discharges_data = getfile_from_s3(backet_name,'covid19-development/data/discharges_summary.json')
inspections_data = getfile_from_s3(backet_name,'covid19-development/data/inspections.json')
last_update_str = getfile_from_s3(backet_name,'covid19-development/data/last_update.json')
patients_attribute_data = getfile_from_s3(backet_name,'covid19-development/data/patients.json')
patients_data = getfile_from_s3(backet_name,'covid19-development/data/patients_summary.json')
querents_data = getfile_from_s3(backet_name,'covid19-development/data/querents.json')

# インスタンス作成(ReturnDataクラス参照)
rd = return_data.ReturnData()

# 各データの計算
lpd = rd.count_latest_patients(input=latest_patients_data) # 現在の患者数(治療終了者反映)
pd = rd.count_patients(input=patients_data) # 陽性患者数
cd = rd.count_callcenter_call(input=contacts_data) # 新型コロナコールセンター相談件数(札幌市保健所値) 
dd = rd.count_discharges(input=discharges_data) # 治療終了者数
qd = rd.count_querents_call(input=querents_data) # 帰国者・接触者電話相談センター相談件数(札幌市保健所値)
insd = rd.count_inspections(input=inspections_data) # 検査数累計
pad = rd.list_patients_attribute(input=patients_attribute_data) # 陽性患者の居住地
lud = rd.check_last_update(input=last_update_str) # データ更新日時

# DynamoDBへの保存(テーブル名、リージョンは適宜変えてください)
table_name = 'COVID-19_Hokkaido'
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table(table_name)

# DynamoDBには直近のデータがあれば良いのでパーティションキーは固定でデータ上書き
# Alexaから呼び出すと15分くらい更新前のデータで返ってくるのでどこかにキャッシュしている可能性あり
def store_dynamodb(tablename):
    table = dynamodb.Table(tablename)
    with table.batch_writer(overwrite_by_pkeys=['id']) as batch:
        batch.put_item(
            Item={
                "id": 1,
                "latest_patients_subtotal": lpd[1],
                "latest_patients_total": lpd[2],
                "patients_subtotal": pd[1],
                "patients_total": pd[2],
                "discharges_subtotal": dd[1],
                "discharges_total": dd[2],
                "contacts_subtotal": cd[1],
                "querents_subtotal": qd[1],
                "inspections_subtotal": insd[1],
                "inspections_total": insd[2],
                "patients_residential": pad,
                "update_date": lud[0],
                "update_time": lud[1]
            }
        )

def lambda_handler(event, context):
    # TODO implement
    store_dynamodb(table_name)