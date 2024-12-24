"""

"""
from pprint import pprint
import requests, inspect


class Query:

    def __init__(self) -> None:
        self.host = 'http://10.64.2.100:30010'
        self.Session = requests.Session()
        self.Session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
            # "Access-Token": "2224de48-b30b-420e-8b9d-f23bdd2e0e7e"
        })

    def relay_request(self, method, url, **kwargs):
        """
        发送请求并处理响应状态码。
        :param method: HTTP 方法，如 'GET'、'POST' 等
        :param url: 请求的 URL
        :param kwargs: 其他请求参数，如 headers, json, params 等
        :return: 如果响应状态码为200,则返回响应对象,否则打印错误信息并返回 None
        """
        try:
            # 发送请求
            response = self.Session.request(method, self.host + url, **kwargs)
            # 检查响应状态码
            if response.status_code == 200:
                frame = inspect.currentframe().f_back
                file_name = frame.f_code.co_filename.split("\\")[-1]
                print(f"调用位置: {file_name}\{frame.f_code.co_name}\{frame.f_lineno}行\n请求成功:{response.status_code}")
                return response
            else:
                print(f"请求失败:{response.status_code}\n{response.text}")
                return None
        except requests.RequestException as e:
            # 捕获请求异常并打印
            print(f"请求异常: {e}")
            return None

    def change_org(self, org_code):
        """
        发送请求切换机构
        :param org_code: 机构代码，
            "23002311": "中直鸡西矿区养老保险"
            "23030111": "市直养老保险"
            "23030191": "城乡居民养老保险"
            "23030211": "中直行业下放养老保险"
        :return: None
        """
        url = f'/main/works/updateUserinfo?aab034={org_code}'
        res = self.relay_request(method="post", url=url, json={"aab034": org_code})
        if res:
            print(res.text)
    
    def login(self, name=None, idcard=None):
        """
        登录
        :param name: 姓名，
        :param idcard: 身份证号
        :return: None
        """
        query_url = '/portal/queryUserInfoWithChannel'
        login_url = '/api/auth/channel/login'
        query_data = {
            "aac002": idcard,
            "aac003": name
        }
        query_res = self.relay_request(method='post', url=query_url, data=query_data)
        if query_res:
            UserInfo = query_res.json()
            login_data = {
                "password": UserInfo.get('ua0102'),
                "username": UserInfo.get('ua0100')
            }
            login_res = self.relay_request(method='post', url=login_url, json=login_data, headers={"Content-Type": "application/json"})
            if login_res:
                map = login_res.json().get('map')
                if map:
                    self.Session.headers.update(map)
                    entrydatagrid_url = '/user/s9010202/entrydatagrid'
                    entrydatagrid_res = self.relay_request(method='post', url=entrydatagrid_url)
                    if entrydatagrid_res:
                        entrydatagrid_data = entrydatagrid_res.json()
                        print(entrydatagrid_data.get('aab300'))
                        return entrydatagrid_data.get('aab034')

    def login_main(self, name='岳琳', idcard='230304198302014020', org_code=None):
        """
        登录并切换指定机构
        :param name: 姓名
        :param idcard: 身份证号
        :param org_code: 机构代码
        :return: None
        """
        login_res = self.login(name, idcard)
        # print(login_res)
        if (login_res and org_code) and login_res != org_code:
            self.change_org(org_code)
            self.login(name, idcard)
    
    def dyff_info(self, idcard="", person_id="", start_date="", end_date="", page=1, rows=10):
        """
        待遇发放明细查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param start_date: 开始年月
        :param end_date: 终止年月
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        dyff_url = '/business/m0027/EntryDatagrid'
        dyff_data = {
            "aac002": idcard,       # 社会保障号
            "aae041": start_date,   # 开始年月
            "aae042": end_date,     # 终止年月
            "aac001": person_id,    # 个人编号
            "page": page,
            "rows": rows
        }
        dyff_res = self.relay_request(method='post', url=dyff_url, data=dyff_data)
        if dyff_res:
            datas = dyff_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
        
    def rycb_query(self, idcard="", person_id="", org_id="", ins_kind="", page=1, rows=10):
        """
        人员参保信息查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param org_id: 单位编号
        :param ins_kind: 险种
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        rycb_url = '/business/m5906/entry21'
        rycb_data = {
            "aac001": person_id,    # 个人编号
            "aab001": org_id,       # 单位编号
            "aae140": ins_kind,     # 险种
            "aac002": idcard,       # 社会保障号
            "page": page,
            "rows": rows
        }
        rycb_res = self.relay_request(method='post', url=rycb_url, data=rycb_data)
        if rycb_res:
            datas = rycb_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
        
    def rysj_query(self, idcard="", person_id="", org_id="", start_date="", end_date="", page=1, rows=10):
        """
        人员实缴信息查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param org_id: 单位编号
        :param start_date: 开始年月
        :param end_date: 终止年月
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        rysj_url = '/business/m5908/entry21'
        rysj_data = {
            "aac001": person_id,    # 个人编号
            "aab001": org_id,       # 单位编号
            "aac002": idcard,       # 社会保障号
            "aae041": start_date,   # 开始年月
            "aae042": end_date,     # 终止年月
            "page": page,
            "rows": rows
        }
        rysj_res = self.relay_request(method='post', url=rysj_url, data=rysj_data)
        if rysj_res:
            datas = rysj_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
        
    def dqdy_query(self, idcard="", person_id="", page=1, rows=10):
        """
        定期待遇信息查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        dqdy_url = '/business/m5914/Entry21'
        dqdy_data = {
            "aac002": idcard,       # 社会保障号
            "aac001": person_id,    # 个人编号
            "page": page,
            "rows": rows
        }
        dqdy_res = self.relay_request(method='post', url=dqdy_url, data=dqdy_data)
        if dqdy_res:
            datas = dqdy_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
    
    def dyff_query(self, idcard="", person_id="", page=1, rows=10):
        """
        待遇发放信息查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        dyff_url = '/business/m5918/entrydatagrid'
        dyff_data = {
            "aac002": idcard,       # 社会保障号
            "aac001": person_id,    # 个人编号
            "page": page,
            "rows": rows
        }
        dyff_res = self.relay_request(method='post', url=dyff_url, data=dyff_data)
        if dyff_res:
            datas = dyff_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
        
    def rzxx_query(self, idcard="", person_id="", start_date="", end_date="", auth_way="", page=1, rows=10):
        """
        认证信息查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param start_date: 开始年月
        :param end_date: 终止年月
        :param auth_way: 认证方式
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        rzxx_url = '/business/m5919/entrydatagrid'
        rzxx_data = {
            "aac002": idcard,       # 社会保障号
            "aac001": person_id,    # 个人编号
            "aae041": start_date,   # 开始年月
            "aae042": end_date,     # 终止年月
            "aaa135": auth_way,     # 认证方式
            "page": page,
            "rows": rows
        }
        rzxx_res = self.relay_request(method='post', url=rzxx_url, data=rzxx_data)
        if rzxx_res:
            datas = rzxx_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows

    def ryzh_query(self, idcard="", person_id="", name="", org_id="", page=1, rows=10):
        """
        人员账户查询
        :param idcard: 社会保障号
        :param person_id: 个人编号
        :param name: 姓名
        :param org_id: 单位编号
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        ryzh_url = '/business/m5924/queryPersonInfo'
        ryzh_data = {
            "queryParams[aac001]": person_id,   # 个人编号
            "queryParams[aac002]": idcard,      # 社会保障号
            "queryParams[aac003]": name,        # 姓名
            "queryParams[aab001]": org_id,      # 单位编号
            "queryParams[sa0200]": 111592421,
            "timeout": 1000000,
            "page": page,
            "rows": rows
        }
        ryzh_res = self.relay_request(method='post', url=ryzh_url, data=ryzh_data)
        if ryzh_res:
            datas = ryzh_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
        
    def ywbl_query(self, mode_id="", status="", idcard="", name="", start_date="", end_date="", do_people="", org_id="", org_name="", page=1, rows=10):
        """
        人员账户查询
        :param mode_id: 模块编号
        :param status: 业务状态
        :param idcard: 社会保障号
        :param name: 姓名
        :param start_date: 开始日期
        :param end_date: 终止日期
        :param do_people: 经办人
        :param org_id: 单位编号
        :param org_name: 单位名称
        :param page: 页码
        :param rows: 每页显示数量
        :return: 明细数据
        """
        ywbl_url = '/business/m0001/entryDatagrid'
        ywbl_data = {
            "sa0200": mode_id,      # 模块编号
            "da0001": status,       # 业务状态
            "applyID": idcard,      # 申请人ID
            "applyName": name,      # 申请人姓名
            "aae041": start_date,   # 开始日期
            "aae042": end_date,     # 终止日期
            "ua0100": do_people,    # 经办人
            "aab001": org_id,       # 单位编号
            "aab004": org_name,     # 单位名称
            "page": page,
            "rows": rows
        }
        ywbl_res = self.relay_request(method='post', url=ywbl_url, data=ywbl_data)
        if ywbl_res:
            datas = ywbl_res.json()
            data_rows = datas.get('rows')
            pprint(data_rows)
            return data_rows
    


if __name__ == "__main__":
    Q = Query()
    Q.login_main(org_code='23030111')
    Q.ywbl_query(idcard='23030419730102402X', start_date='20210901', end_date='20240915')
