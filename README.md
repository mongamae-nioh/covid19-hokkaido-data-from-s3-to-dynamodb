# 概要
- Code for Sapporoのリポジトリで公開されている新型コロナウイルス(COVID19)のデータ(https://github.com/codeforsapporo/covid19/blob/development/data/*.json)をS3へアップロードすると発火されるLambda用のPythonスクリプト
- S3のデータ更新 > Lambda発火 > DynamoDBへ保存される
- バケット名はユニークなのでLambdaの環境変数を使用した
- LambdaのIAMへS3とDynamoDBのアクセス権を与える
- データにより更新日時が異なるためDynamoDBのパーティションキーは日付ではなくidとした
- Alexaがこのデータを参照して最新状況を伝えるため過去データはDynamoDBへ保存せず常に最新の1アイテムだけを保存する(id:1のアイテムを上書き。コスト的にも良い)
- 患者数の推移は「JUST道IT」の有志の方々が公開しているまとめサイト(https://stopcovid19.hokkaido.dev/)を参照してほしい