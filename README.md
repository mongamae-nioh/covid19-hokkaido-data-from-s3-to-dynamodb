# 概要
- Code for Sapporoのリポジトリで公開されている新型コロナウイルス(COVID-19)のデータ (https://github.com/codeforsapporo/covid19/blob/development/data/*.json) をS3へアップロードすると発火されるLambda用のPythonスクリプト
- S3のデータ更新 > Lambda発火 > DynamoDBへ保存される
- バケット名はユニークなのでLambdaの環境変数を使用
- LambdaのIAMへS3とDynamoDBのアクセス権を与える
- データにより更新日時が異なるためDynamoDBのパーティションキーは日付ではなくidとした
- あとからデータがいろいろ追加されるかもしれないのでスキーマを気にしなくて良いDynamoDBを使用
- Alexaがこのデータを参照して最新状況を伝えるため過去データはDynamoDBへ保存せず常に最新の1アイテムだけを保存する(id:1のアイテムを上書き。コスト的にも良い)
- 患者数の推移は「JUST道IT」の有志の方々が公開しているまとめサイト (https://stopcovid19.hokkaido.dev/) を参照してほしい

# DynamoDBのテーブル設定
パーティションキー:id(number)のみ指定し他はデフォルトで作成

```
{
    "Table": {
        "TableArn": "arn:aws:dynamodb:ap-northeast-1:nnnnnnnnnnn:table/COVID-19_Hokkaido", 
        "AttributeDefinitions": [
            {
                "AttributeName": "id", 
                "AttributeType": "N"
            }
        ], 
        "ProvisionedThroughput": {
            "NumberOfDecreasesToday": 0, 
            "WriteCapacityUnits": 5, 
            "ReadCapacityUnits": 5
        }, 
        "TableSizeBytes": 280, 
        "TableName": "COVID-19_Hokkaido", 
        "TableStatus": "ACTIVE", 
        "TableId": "nnnnnnnn", 
        "KeySchema": [
            {
                "KeyType": "HASH", 
                "AttributeName": "id"
            }
        ], 
        "ItemCount": 1, 
        "CreationDateTime": nnnnnnn
    }
}
```

# DynamoDBのアイテム説明
|  項目名  |  データ  |
| ---- | ---- |
| contacts_subtotal | 新型コロナコールセンター相談件数(札幌市保健所値)(1日分)  |
| discharges_subtotal | 治療終了者数(1日分) |
| discharges_total | 治療終了者数(累計) |
| id | DynamoDBのパーティションキー |
| inspections_subtotal | 検査数累計(1日分) |
| inspections_total | 検査数累計(累計) |
| latest_patients_subtotal | 現在の患者数(治療終了者反映)(1日分) |
| latest_patients_total | 現在の患者数(治療終了者反映)(合計) |
| patients_residential | 陽性患者の居住地(リスト) |
| patients_subtotal | 陽性患者数(1日分) |
| patients_total | 陽性患者数(累計) |
| querents_subtotal | 帰国者・接触者電話相談センター相談件数(札幌市保健所値)(1日分) |
| update_date | データ更新日 |
| update_time | データ更新時間 |


# 実際のアイテム例
以下のようになっている。
これをAlexaのLambdaから参照して戻り値を発話で使っている。

```
{
    "Count": 1, 
    "Items": [
        {
            "update_date": {
                "S": "2020-03-15"
            }, 
            "update_time": {
                "S": "11:35"
            }, 
            "patients_subtotal": {
                "N": "7"
            }, 
            "latest_patients_subtotal": {
                "N": "4"
            }, 
            "patients_residential": {
                "L": [
                    {
                        "S": "札幌市"
                    }
                ]
            }, 
            "patients_total": {
                "N": "144"
            }, 
            "querents_subtotal": {
                "N": "172"
            }, 
            "contacts_subtotal": {
                "N": "504"
            }, 
            "discharges_total": {
                "N": "58"
            }, 
            "discharges_subtotal": {
                "N": "3"
            }, 
            "inspections_total": {
                "N": "1393"
            }, 
            "latest_patients_total": {
                "N": "82"
            }, 
            "inspections_subtotal": {
                "N": "70"
            }, 
            "id": {
                "N": "1"
            }
        }
    ], 
    "ScannedCount": 1, 
    "ConsumedCapacity": null
}
```
