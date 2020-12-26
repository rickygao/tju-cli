from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image


class ClassesClient:
    def __init__(self):
        self._session = requests.Session()

    def authenticate(self, username, password, captcha_callback):
        response = self._session.get('https://sso.tju.edu.cn/cas/login')

        bs = BeautifulSoup(response.text, 'html.parser')
        execution = bs.select_one('input[name="execution"]')['value']

        while True:
            captcha_image = self._retrieve_captcha()
            captcha_result = captcha_callback(captcha_image)
            if captcha_result is not None:
                break

        response = self._session.post('https://sso.tju.edu.cn/cas/login', data={
            'username': username,
            'password': password,
            'captcha': captcha_result,
            'execution': execution,
            '_eventId': 'submit',
        })

    def _retrieve_captcha(self):
        response = self._session.get('https://sso.tju.edu.cn/cas/images/kaptcha.jpg')
        captcha_image = Image.open(BytesIO(response.content))
        return captcha_image

    def retrieve_grade(self):
        response = self._session.post(
            url='http://classes.tju.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action',
            data={'projectType': 'MAJOR'}
        )

        bs = BeautifulSoup(response.text, 'html.parser')
        semester_table = bs.select_one('table:nth-child(2)')
        course_table = bs.select_one('table:nth-child(4)')

        semester_keys, semesters = _parse_table(semester_table)
        _, courses = _parse_table(course_table)

        overall_keys = semester_keys[2:]
        overall_values = [cell.text for cell in semester_table.select('tr:nth-last-child(2)>th')[1:]]
        overall = dict(zip(overall_keys, overall_values))

        return {'overall': overall, 'semesters': semesters, 'courses': courses}

    @property
    def authenticated(self):
        return self._session.cookies.get('TGC') is not None

    @property
    def session(self):
        return self._session


TRANSLATION_TABLE = {
    '门数': 'num_courses',
    '总学分': 'credit',
    '平均绩点': 'grade_point',
    '加权平均成绩': 'grade',
    '学年度': 'year',
    '学期': 'semester',
    '学年学期': 'year_semester',
    '课程代码': 'code',
    '课程序号': 'no',
    '课程名称': 'name',
    '课程类别': 'type',
    '学分': 'credit',
    '考试情况': 'exam_status',
    '最终': 'grade',
    '绩点': 'grade_point',
}

def _try_translation(text):
    return TRANSLATION_TABLE.get(text, text)

CONVERTION_TABLE = {
    'num_courses': int,
    'credit': float,
    'grade_point': float,
    'grade': float,
    'no': int,
}

NO_CONVERTION = lambda x: x

def _try_convertion(pair):
    key, value = pair
    value = CONVERTION_TABLE.get(key, NO_CONVERTION)(value)
    return key, value

def _extract_row_text(row):
    return [cell.text.strip() for cell in row.select('th, td')]

def _parse_table(table):
    keys = _extract_row_text(table.select_one('thead>tr'))
    values = map(_extract_row_text, table.select('tbody>tr'))

    # filter out abnormal row
    values = [vs for vs in values if len(vs) == len(keys)]

    # try to translate
    keys = [_try_translation(k) for k in keys]
    values = [[_try_translation(v) for v in vs] for vs in values]

    dicts = [dict(map(_try_convertion, zip(keys, values_per_row))) for values_per_row in values]
    return keys, dicts
