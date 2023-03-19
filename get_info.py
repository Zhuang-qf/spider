import execjs
import time
import requests
from fake_useragent import UserAgent


class get_data(object):

    def __init__(self):
        self.headers = {
            "User-Agent": UserAgent().random,
            "Cookie": "PI=44; Hm_lvt_2610e5c202b60841b30a62960fbef0ad=1677210289,1678465539,1678521155; "
                      "Hm_lpvt_2610e5c202b60841b30a62960fbef0ad=1678525165"
        }

    # 拼接参数得到参数相关字符串
    def params(self):
        timestamp = int(time.time()) * 1000
        str1_list = []
        str2_list = []
        # 获取前20页数据
        for page in range(1, 3):
            # page = 1
            app_id = '98357f659cf8fb6001cff80f7c6b85f2'
            str_1 = f"app_id={app_id}&diploma_id=7&page={page}&page_len=20&platform=desktop&ts={timestamp}&v=210&wenli=0"
            str_2 = "{" + str_1 + "}" + "&key=146fd1e66513611ac7af69f21f1d7725"
            str1_list.append(str_1)
            str2_list.append(str_2)
        return str1_list, str2_list

    # 读取js文件获取到加密参数sign
    def js_jiami(self, str_1):
        js_text = open("./jiami.js", mode="r").read()
        ctx = execjs.compile(js_text)
        a = ctx.call("Et", str_1).upper()
        return a

    # 请求获取到数据
    def get_info(self, key1, sign, flag):
        if flag == "高校排名":
            url = f"https://www.jizhy.com/open/sch/rank-list?{key1}&sign={sign}"
            self.headers["Referer"] = "https://www.jizhy.com/44/rank/school"
            response = requests.get(url=url, headers=self.headers)
            json_data = response.json()
            data_list = json_data["data"]['sch_list']
            # 返回响应数据, 提交到gui模块
            sch_pm_list = []
            for data in data_list:
                school_pm = {}
                school_pm['name'] = data['sch_name']
                school_pm['num'] = data['sch_rank']
                school_pm['score'] = data['sch_rank_score']
                print(school_pm)
                sch_pm_list.append(school_pm)
            return sch_pm_list
        if flag == "高校薪资":
            url = f"https://www.jizhy.com/open/sch/salary-rank-list?{key1}&sign={sign}"
            self.headers["Referer"] = "https://www.jizhy.com/44/rank/school-pay"
            response_salary = requests.get(url=url, headers=self.headers)
            json_salary = response_salary.json()
            data_list = json_salary['data']
            sch_gx_list = []
            for data in data_list:
                school_gx = {}
                school_gx['rank'] = data['sch_rank']
                school_gx['name'] = data['sch_name']
                school_gx['salary'] = str("￥") + str(data['salary'])
                print(school_gx)
                sch_gx_list.append(school_gx)
            return sch_gx_list

    def run(self, flag):
        key1_list, key2_list = self.params()
        # flag = input("请输入: ")
        for key1, key2 in zip(key1_list, key2_list):
            sign = self.js_jiami(key2)
            self.get_info(key1, sign, flag)


# if __name__ == '__main__':
#     gui = get_data()
#     flag = "高校排名"
#     gui.run(flag)
