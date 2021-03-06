#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Sprint Info
# uuid = PrimaryKey(uuid.UUID, default=uuid.uuid4)
# name = Required(str)
# project = Required(Project)
# version = Required(str)  # sprint version tag
# requirements = Required(StrArray)  # list(): req1, req2
# rcs = Required(StrArray)  # RC tags list: RC1, RC2
# issue = Optional(Json)  # dict(): keys: types, found_since, statuses, categories
# case = Optional(Json)
# queries = Optional(Json)  # dict(): issue: jql,  ...  case: xx
# status = Required(str, default='active')  # active, disable, delete

import logging


def generate_jqls(project_key: str, sprint_info: dict):
    """
    Generate JQL for Sprint
    :param project_key:
    :param sprint_info:
    :return:
    """
    jqls = {
        'overall': dict(),
        'categories': dict(),
        'rcs': dict(),
        'issue_found_since': dict(),
    }

    # 定义customer bug jql, 它不应该局限在 sprint 过程
    jqls['issue_found_since']['customer'] = ' AND '.join([
        'project = "%s"' % project_key,
        'issuetype in (%s)' % ', '.join(sprint_info['issue']['types']),
        'labels = "%s"' % sprint_info.get('version'),
        'labels = "Customer"',
        ])

    # 定义 jql base, 用于后面的所有 jql
    jql_base = ' AND '.join([
        'project = "%s"' % project_key,
        'issuetype in (%s)' % ', '.join(sprint_info['issue']['types']),
        'Sprint = "%s"' % sprint_info.get('name'),
        'labels = "%s"' % sprint_info.get('version'),
    ])

    logging.info('Generate JQL for overall')
    for k, v in sprint_info['issue']['statuses'].items():
        jqls['overall'][k] = ' AND '.join([
            jql_base,
            'status in (%s)' % ', '.join(v)
        ])

    logging.info('Generate JQL for requirements')
    for req in sprint_info.get('requirements'):
        jql_req_base = ' AND '.join([
            jql_base,
            'labels = "%s"' % req,
        ])
        jqls[req] = dict()
        for k, v in sprint_info['issue']['statuses'].items():
            jqls[req][k] = ' AND '.join([
                jql_req_base,
                'status in (%s)' % ', '.join(v)
            ])

    logging.info('Generate JQL for categories')
    # if sprint_info['issue'].get('categories') is None:
    #     sprint_info['issue_categories'] = ['Regression', 'Previous', 'NewFeature', 'Others']
    for category in sprint_info['issue']['categories']:
        # Others 的类别将在下面进行处理
        if category == 'Others':
            continue
        jql_category = ' AND '.join([
            jql_base,
            'labels = "%s"' % category,
        ])
        jqls['categories'][category.lower()] = jql_category
    # Others 是除了 Regression, Previous, NewFeature 的类别
    # 实际中可能没有标记，这里不做jql不带任何相关标记，先获取总数，用于后面函数处理时候计算得出 others
    jqls['categories']['others'] = jql_base

    logging.info('Generate JQL for rcs')
    for rc in sprint_info['rcs']:
        jql_rc = ' AND '.join([
            jql_base,
            'labels = "%s"' % rc,
        ])
        jqls['rcs'][rc] = jql_rc

    logging.info('Generate JQL for issue found since')
    # if sprint_info.get('issue_found_since') is None:
    #     sprint_info['issue_found_since'] = ['RegressionImprove', 'QAMissed', 'NewFeature', 'Customer']
    for since in sprint_info['issue']['found_since']:
        # 来自 customer 的缺陷已经在一开始就生成了 jql，所以这里跳过
        if since == 'Customer':
            continue
        jql_issue_found_since = ' AND '.join([
            jql_base,
            'labels = "%s"' % since,
        ])
        jqls['issue_found_since'][since.lower()] = jql_issue_found_since
    logging.info('Complete to generate all JQLs')
    return jqls

