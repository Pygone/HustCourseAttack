import os.path
import sys
import time
from datetime import datetime

from requests import post, JSONDecodeError, get
import logging

file_handler = logging.FileHandler("log.log", mode='a', encoding="utf8")
file_handler.setFormatter(logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s"
    , datefmt="%Y-%m-%d %H:%M:%S"
))
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    fmt="%(message)s"
    , datefmt="%Y-%m-%d %H:%M:%S"
))
console_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler], )


class Course:
    def __init__(self, Cookie, userId, course: dict):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/111.0.0.0 "
                          "Safari/537.36 Edg/111.0.0.0 ",
            "Cookie": Cookie
        }
        self.userId = userId
        self.course = course
        self.requestList = {}
        self.XQH = None
        self.KTBH = []
        self.GetCourse()
        self.GetClassId()
        self.Post()

    def GetCourse(self):
        data = {"page": 1, "limit": 10, "fzxkfs": "", "xkgz": 1}
        res = post(url="http://wsxk.hust.edu.cn/zyxxk/Stuxk/getXsFaFZkc", headers=self.headers, data=data)
        try:
            res_json = res.json()
        except JSONDecodeError:
            logging.error("Cookie 无效!")
            sys.exit(-1)
        for i in res_json["data"]:
            for j in self.course.keys():
                if i["KCMC"] == j:
                    ID = i["ID"]
                    KCBH = i["KCBH"]
                    FZID = i["FZID"]
                    self.XQH = i["XQH"]
                    self.requestList[j] = list([ID, KCBH, FZID])

    def GetClassId(self):
        for j in self.course.keys():
            data = {"page": 1, "limit": 10, "fzid": self.requestList[j][2], "kcbh": self.requestList[j][1],
                    "sfid": self.userId, "faid": self.requestList[j][0], "id": self.requestList[j][0]}
            res = post(url="http://wsxk.hust.edu.cn/zyxxk/Stuxk/getFzkt", data=data, headers=self.headers)
            for i in res.json()["data"]:
                if i["XM"] == self.course[j]:
                    self.requestList[j].append(i["KTBH"])

    def Post(self):
        for i in self.course.keys():
            data = {
                "ktbh": self.requestList[i][3],
                "xqh": self.XQH,
                "kcbh": self.requestList[i][1],
                "fzid": self.requestList[i][2],
                "faid": self.requestList[i][0],
                "sfid": self.userId
            }
            res = post(url="http://wsxk.hust.edu.cn/zyxxk/Stuxk/addStuxkIsxphx", headers=self.headers, data=data)
            if res.json()["code"] == "0":
                logging.info(f"学号为{self.userId}的同学, 您已抢到{i}:{self.course[i]}")
            else:
                logging.info(res.json()["msg"])


def CheckCookie(Cookie):
    if not (os.path.isfile(sys.argv[2]) and os.path.isfile(sys.argv[3])):
        logging.error("路径有误!")
        sys.exit(-1)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/111.0.0.0 "
                      "Safari/537.36 Edg/111.0.0.0 ",
        "Cookie": Cookie
    }
    res = get("http://wsxk.hust.edu.cn/zyxxk/Stuxk/getStuNowXkfs", headers=headers)
    if len(res.history) == 0:
        return True
    elif res.history[0].status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    course = {}
    with open(sys.argv[2], encoding="utf8") as f:
        List = f.readlines()
        for i in List:
            line = i.split(":") if ":" in i else i.split("：")
            course[line[0]] = line[1]
    with open(sys.argv[3], encoding="utf8") as f:
        Cookie = f.read().strip()
        if CheckCookie(Cookie):
            logging.info("Cookie 正常!")
        else:
            logging.error("Cookie 无效, 请及时检查Cookie!")
            sys.exit(-1)
    if len(sys.argv) > 4:
        while True:
            date = datetime.strptime(str(datetime.today().year) + "/" + sys.argv[4], '%Y/%m/%d/%H/%M')
            diff = (datetime.now() - date)
            diff = diff.days * 86400 + diff.seconds
            if diff > 0:
                example = Course(Cookie, sys.argv[1], course)
                break
            else:
                logging.info("等待中")
                if -diff > 10:
                    time.sleep(-diff - 10)
                else:
                    time.sleep(1)
                continue
