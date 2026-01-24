import csv
import json
import math

from typing import Optional

import config


provinces = [
    "安徽",
    "北京",
    "福建",
    "甘肃",
    "广东",
    "广西",
    "贵州",
    "海南",
    "河北",
    "河南",
    "黑龙江",
    "湖北",
    "湖南",
    "吉林",
    "江苏",
    "江西",
    "辽宁",
    "内蒙古",
    "山东",
    "山西",
    "陕西",
    "上海",
    "四川",
    "天津",
    "新疆",
    "浙江",
    "重庆",
    "宁夏",
    "云南",
    "澳门",
    "香港",
    "青海",
    "西藏",
    "台湾",
]

award_levels = [
    "金牌",
    "银牌",
    "铜牌",
    "一等奖",
    "二等奖",
    "三等奖",
    "国际金牌",
    "国际银牌",
    "国际铜牌",
    "前5%",
    "前15%",
    "前25%",
]


class Record(object):
    def __init__(self, data: list[str], contest_names: list[str]):
        contest_id = int(data[0])
        self.contest = (
            contest_names[contest_id]
            if contest_id < len(contest_names)
            else str(contest_id)
        )
        self.school_id = int(data[1])
        self.score = float(data[2]) if data[2] else math.nan
        self.rank = int(data[3])
        self.province = provinces[int(data[4])]
        self.award_level = award_levels[int(data[5])]

    def __repr__(self):
        return (
            f"Record(name={self.contest}, "
            f"score={self.score}, "
            f"rank={self.rank}, "
            f"province={self.province}, "
            f"award_level={self.award_level})"
        )


class Oier(object):
    def __init__(self, data: list[str], contest_names: list[str]):
        self.uid = int(data[0])
        self.initials = data[1]
        self.name = data[2]
        self.gender = data[3]
        self.enroll_middle = data[4]
        self.oierdb_score = float(data[5])
        self.ccf_score = float(data[6])
        self.ccf_level = int(data[7])
        self.records = [
            Record(record.strip().replace(";", ":").split(":"), contest_names)
            for record in data[8].strip().split("/")
            if record
        ]

    def __repr__(self):
        return (
            f"Oier(uid={self.uid}, "
            f"initials={self.initials}, "
            f"name={self.name}, "
            f"oierdb_score={self.oierdb_score}, "
            f"ccf_score={self.ccf_score}, "
            f"ccf_level={self.ccf_level}, "
            f"records={self.records})"
        )


class OierDB(object):
    def __init__(
        self,
        oier_file: Optional[str] = None,
        contest_file: Optional[str] = None,
    ):
        self.contests: list[str] = []
        if contest_file is not None:
            with open(contest_file, "r", encoding="utf-8") as f:
                contest_json = json.load(f)
                for contest in contest_json:
                    self.contests.append(f"{contest['type']}-{contest['year']}")
        self.oiers: list[Oier] = []
        if oier_file is not None:
            with open(oier_file, "r", encoding="utf-8") as f:
                for row in csv.reader(f):
                    self.oiers.append(Oier(row, self.contests))


oierdb = OierDB(oier_file=config.oierdb_result, contest_file=config.oierdb_contests)
