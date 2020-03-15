import json
from datetime import datetime

latest_patients_data = {}
patients_data = {}
discharges_data = {}
contact_data = {}
querents_data = {}
inspections_data = {}
patients_attribute_data = {}
last_update_str = ""

class ReturnData:
    def __init__(self):
        pass

    # 現在の患者数(治療終了者反映)
    def count_latest_patients(self, input=None):
        self.input = input
        if len(self.input) > 0:
            self.latest_patients_date = self.input['data'][-1]['date'][:10]
            self.latest_patients_subtotal = self.input['data'][-1]['subtotal']

            latest_patients_total = 0
            for i in self.input['data']:
                latest_patients_total += i['subtotal']

            return self.latest_patients_date,self.latest_patients_subtotal,latest_patients_total

    # 陽性患者数(累計)
    def count_patients(self, input=None):
        self.input = input
        if len(self.input) > 0:
            self.patients_date = self.input['data'][-1]['date'][:10]
            self.patient_subtotal = self.input['data'][-1]['subtotal']

            patients_total = 0
            for i in self.input['data']:
                patients_total += i['subtotal']

            return self.patients_date,self.patient_subtotal,patients_total

    # 治療終了者
    def count_discharges(self, input=None):
        self.input = input
        if len(self.input) > 0:
            self.discharges_date = self.input['data'][-1]['date'][:10]
            self.discharges_subtotal = self.input['data'][-1]['subtotal']

            discharges_total = 0
            for i in self.input['data']:
                discharges_total += i['subtotal']

            return self.discharges_date,self.discharges_subtotal,discharges_total

    # 新型コロナコールセンター相談件数
    def count_callcenter_call(self, input=None):
        self.input = input
        if len(self.input) > 0:
            self.contacts_date = self.input['data'][-1]['date'][:10]
            self.contacts_subtotal = self.input['data'][-1]['subtotal']

            return self.contacts_date,self.contacts_subtotal

    # 帰国者・接触者電話相談センター相談件数
    def count_querents_call(self, input=None):
        self.input = input
        if len(self.input) > 0:
            self.querents_date = self.input['data'][-1]['date'][:10]
            self.querents_subtotal = self.input['data'][-1]['subtotal']

            return self.querents_date,self.querents_subtotal
    
    # 検査数
    def count_inspections(self, input=None):
        self.input = input
        if len(self.input) > 0:
            self.inspections_date = self.input['data'][-1]['date'][:10]
            self.inspections_subtotal = self.input['data'][-1]['subtotal']

            inspections_total = 0
            for i in self.input['data']:
                inspections_total += i['subtotal']
                
            return self.inspections_date,self.inspections_subtotal,inspections_total
    
    # 患者属性
    def list_patients_attribute(self, input=None):
        self.input = input
        tmp_residential_list = []
        self.list_date = self.input['data'][-1]['date'][:10]

        if len(self.input) > 0:
            for i in self.input['data']:
                if self.list_date == i['date'][:10]:
                    tmp_residential_list.append(i['place'])
            
            is_set = set(tmp_residential_list)
            patients_residential_list = list(is_set)

            return patients_residential_list
    
    # データ最終更新日時
    def check_last_update(self, input=None):
        self.input = input
        t = datetime.strptime(self.input[0:-6],'%Y-%m-%dT%H:%M:%S.%f')
        self.update_date = t.strftime('%Y-%m-%d')
        self.update_time = t.strftime('%H:%M')

        return self.update_date,self.update_time
        