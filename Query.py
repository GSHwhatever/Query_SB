"""

"""
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
        :param: name 姓名
        :param: idcard 身份证号
        :param: org_code 机构代码
        :return: None
        """
        login_res = self.login(name, idcard)
        # print(login_res)
        if (login_res and org_code) and login_res != org_code:
            self.change_org(org_code)
            self.login(name, idcard)
    
    def dyff_query(self):
        """
        待遇发放明细查询
        """
        dyff_url = '/business/m0027/EntryDatagrid'
        dyff_data = {
            "aac002": "23030419730102402X",     # 社会保障号
            "aae041": "",                 # 开始年月
            "aae042": "",                 # 终止年月
            "aac001": "2303000314840",                       # 个人编号
            "page": 1,
            "rows": 10
        }
        dyff_res = self.relay_request(method='post', url=dyff_url, data=dyff_data)
        if dyff_res:
            print(dyff_res.text)

    # def dyff_query(self):
    #     """
    #     待遇发放明细查询
    #     """
    #     pass

    # def dyff_query(self):
    #     """
    #     待遇发放明细查询
    #     """
    #     pass

    # def dyff_query(self):
    #     """
    #     待遇发放明细查询
    #     """
    #     pass

    # def dyff_query(self):
    #     """
    #     待遇发放明细查询
    #     """
    #     pass

    # def dyff_query(self):
    #     """
    #     待遇发放明细查询
    #     """
    #     pass


if __name__ == "__main__":
    Q = Query()
    Q.login_main(org_code='23030111')
    Q.dyff_query()
