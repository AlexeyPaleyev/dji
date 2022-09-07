import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from mysql.connector import errorcode
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import db_config
from tasks import tasks, sal
from tasks import grafs

def cn_init():

    try:
        cnx = mysql.connector.connect(user=db_config["mysql"]["user"],
                                      password=db_config["mysql"]["pw"],
                                      host=db_config["mysql"]["server"],
                                      database=db_config["mysql"]["db"])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx


def cn_al():
    try:
        str_con = 'mysql://{0}:{1}@{2}/{3}'.format(db_config["mysql"]["user"],
                                                   db_config["mysql"]["pw"],
                                                   db_config["mysql"]["server"],
                                                   db_config["mysql"]["db"])
        cna = create_engine(str_con)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
    else:
        return cna


def task(cn, sql_str, data):
    r = 0
    cursor = cn.cursor()
    for result in cursor.execute(sql_str, data, multi=True):
        if result.with_rows:
            row = result.fetchall()
            r = row[-1][-1]
    cursor.close()
    return r

def graf_plt(cna, sql_graf, data):
    sql_query = pd.read_sql_query(sql_graf, cna, params=data)
    df = pd.DataFrame(sql_query)
    d = df.groupby(["primary_keyword_candidate"]).sum()
    d = d.sort_values(by=["cnt"], ascending=False)
    npkw = d.index.to_numpy()
    npen = ['fluent', 'upper', 'intermediate', 'pre', 'basic', 'no english', '']
    for kw in npkw:
        ypoints = []
        for lng in npen:
            d = df.loc[(df["en_level_candidate"] == lng) & (df["primary_keyword_candidate"] == kw)]
            if not d.empty:
                ypoints.append(d.iloc[0][0])
            else:
                ypoints.append(0)
        fig = plt.figure(figsize=(7, 4))
        ax = fig.add_subplot()

        fig.suptitle(f'Кількість наймів кандидатів {kw} з досвідом до 1 р  включно')
        ax.bar(npen, ypoints)
        plt.savefig(f'{kw}.png')
        plt.show()


def graf_sal_diff(cna, sql_graf, data):
    sql_query = pd.read_sql_query(sql_graf, cna, params=data)
    df = pd.DataFrame(sql_query)
    ypoints = df[["salary_diff"]].values
    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot()

    fig.suptitle('Розподілення зміни компенсації')
    ax.hist(ypoints, 27)
    ax.minorticks_on()
    plt.grid()
    plt.savefig('diff.png')
    plt.show()


if __name__ == '__main__':
    cn = cn_init()
    cna = cn_al()
    for item in tasks:
        print (item["text"] , task(cn, item["sql_str"], item["par"]))
    graf_plt(cna, grafs["sql_str"], grafs["par"])
    graf_sal_diff(cna, sal["sql_str"], sal["par"])

    cn.close()


