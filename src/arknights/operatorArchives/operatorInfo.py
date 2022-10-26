import os
import re
import jieba

from core import log
from core.util import chinese_to_digits, remove_punctuation
from core.resource.arknightsGameData import ArknightsGameData

from .initData import InitData

curr_dir = os.path.dirname(__file__)


class OperatorInfo:
    skins_table = {}
    skins_keywords = []

    stories_title = []

    skill_map = {}
    skill_operator = {}

    operator_keywords = []
    operator_list = []
    operator_map = {}
    operator_one_char_list = []

    @staticmethod
    async def init_operator():
        log.info('building operator info and skills keywords dict...')

        keywords = ['%s 500 n' % key for key in InitData.voices]

        def append_word(text):
            OperatorInfo.operator_keywords.append(text)
            dict_word = '%s 500 n' % text
            if dict_word not in keywords:
                keywords.append(dict_word)

        for key in InitData.skill_index_list:
            append_word(key)

        for key in InitData.skill_level_list:
            append_word(key)

        for name, item in ArknightsGameData.operators.items():
            e_name = remove_punctuation(item.en_name).lower()
            append_word(name)
            append_word(e_name)

            OperatorInfo.operator_list.append(name)
            OperatorInfo.operator_map[e_name] = name

            if len(name) == 1:
                OperatorInfo.operator_one_char_list.append(name)

            skills = item.skills()[0]

            for skl in skills:
                skl_name = remove_punctuation(skl['skill_name'])
                append_word(skl_name)

                OperatorInfo.skill_map[skl_name] = skl['skill_name']
                OperatorInfo.skill_operator[skl['skill_name']] = name

        with open(f'{curr_dir}/operators.txt', mode='w', encoding='utf-8') as file:
            file.write('\n'.join(keywords))
        jieba.load_userdict(f'{curr_dir}/operators.txt')

    @staticmethod
    async def init_stories_titles():
        log.info('building operator stories keywords dict...')
        stories_title = {}
        stories_keyword = []

        for name, item in ArknightsGameData.operators.items():
            stories = item.stories()
            stories_title.update(
                {chinese_to_digits(item['story_title']): item['story_title'] for item in stories}
            )

        for index, item in stories_title.items():
            item = re.compile(r'？+', re.S).sub('', item)
            if item:
                stories_keyword.append(item + ' 500 n')

        OperatorInfo.stories_title = list(stories_title.keys()) + [i for k, i in stories_title.items()]

        with open(f'{curr_dir}/stories.txt', mode='w', encoding='utf-8') as file:
            file.write('\n'.join(stories_keyword))
        jieba.load_userdict(f'{curr_dir}/stories.txt')

    @staticmethod
    async def init_skins_table():
        log.info('building operator skins keywords dict...')
        skins_table = {}
        skins_keywords = [] + InitData.skins

        for name, item in ArknightsGameData.operators.items():
            skins = item.skins()
            skins_table[item.name] = skins
            skins_keywords += [n['skin_name'] for n in skins]

        OperatorInfo.skins_table = skins_table
        OperatorInfo.skins_keywords = skins_keywords

        with open(f'{curr_dir}/skins.txt', mode='w', encoding='utf-8') as file:
            file.write('\n'.join([n + ' 500 n' for n in skins_keywords]))
        jieba.load_userdict(f'{curr_dir}/skins.txt')