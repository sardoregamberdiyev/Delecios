from django.shortcuts import render
from collections import OrderedDict
from contextlib import closing

from django.db import connection

from base.db import dict_fetchall, dict_fetchone


def get_recipe_list():
    sql = """
        SELECT rec.id, rec.name, rec.steps, rec.date, rec.prep, rec.cook,
        rec.yields, rec.img, ctg.content as ctg_name, rec.rate
        from recipe_recipe rec
        inner join recipe_category ctg ON ctg.id = rec.ctg_id
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = []
        for i in dict_fetchall(cursor):
            result.append(_format(i))

    return result


def get_recipe_one(pk):
    sql = """
     SELECT rec.id, rec.name, rec.steps, rec.date, rec.prep, rec.cook,
     rec.yields, rec.img, ctg.content as ctg_name, rec.rate
     from recipe_recipe rec
     inner join recipe_category ctg ON ctg.id = rec.ctg_id
     where rec.id = %s
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, [pk])
        data = dict_fetchone(cursor)
        if data:
            result = _format(data)
        else:
            result = None

    return result


def delete(id):
    sql = 'delete from recipe_recipe where id=%s'
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql, [id])


def _format(data):
    return OrderedDict([
        ('id', data['id']),
        ('name', data['name']),
        ('steps', data['steps']),
        ('date', data['date']),
        ('prep', data['prep']),
        ('cook', data['cook']),
        ('yields', data['yields']),
        ('img', data['img']),
        ('ctg_name', data['ctg_name']),
        ('rate', data['rate'])

    ])