# -*- coding: utf-8 -*-

import os
import json
from http.cookies import SimpleCookie

from get_page import get_page
from zhihu_models import create_question, create_answer, create_question_answer, session, Question, Answer

base_dir = os.getcwd()
_session = get_page()

cookie = SimpleCookie()
with open('cookie.txt') as f:
    cookie.load(f.read())

cookies = {}
for key, morsel in cookie.items():
    cookies[key] = morsel.value

headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
}


LIMIT = 20
SESSION_TOKEN = '2a914f410e80943084a555456f97d915'
SEARCH_PAGE = 'https://www.zhihu.com/api/v3/feed/topstory/recommend?session_token={session_token}&desktop=true&page_number={page_number}&limit=6&action=down&after_id={after_id}'
ANSWER_PAGE = 'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={limit}&offset={offset}&platform=desktop&sort_by=default'


def crawl_feed(url):
    ''''爬取首页feed流'''
    s = []
    r = _session.get(url, headers=headers, cookies=cookies)
    if not r:
        return

    data = r.json().get('data')
    for i in data:

        question_item = i['target'].get('question')
        if not question_item:
            continue
        question_id = question_item['id']
        title = question_item['title']
        answer_count = question_item['answer_count']
        follower_count = question_item['follower_count']

        url = f'https://www.zhihu.com/question/{question_id}'

        item = {
            'question_id': question_id,
            'title': title,
            'url': url,
            'answer_count': answer_count,
            'follower_count': follower_count,
        }
        create_question(**item)
        s.append((question_id, answer_count))
    return s


def crawl_answer(url, question_id):
    r = _session.get(url, headers=headers, cookies=cookies)
    if not r:
        return
    data = r.json().get('data')
    for i in data:
        answer_id = i['id']
        content = i['excerpt']
        voteup_count = i['voteup_count']

        item = {
            'answer_id': answer_id,
            'content': content,
            'url': f'https://www.zhihu.com/question/{question_id}/answer/{answer_id}',
            'voteup_count': voteup_count,
        }
        create_answer(**item)
        qid = session.query(Question).filter_by(
            question_id=question_id).first().id
        aid = session.query(Answer).filter_by(answer_id=answer_id).first().id
        create_question_answer(question_id=qid, answer_id=aid)


def get_after_id(page):
    return (page - 2) * 6 + 5


def main():
    for page in range(2, 4):
        url = SEARCH_PAGE.format(
            session_token=SESSION_TOKEN, page_number=page, after_id=get_after_id(page))
        for question_id, answer_count in crawl_feed(url):

            # for i in range(1, answer_count//LIMIT):
            for i in range(1, 5):
                url = ANSWER_PAGE.format(
                    question_id=question_id, limit=LIMIT, offset=i*5)
                crawl_answer(url, question_id)


if __name__ == '__main__':
    main()
