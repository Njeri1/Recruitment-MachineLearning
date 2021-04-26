import os
import re
from collections import Counter
from io import StringIO
from pathlib import Path

import pandas as pd
import spacy
from flask import Flask, render_template, request, url_for, redirect, send_file
from gensim.models import Word2Vec
from spacy.matcher import PhraseMatcher
from werkzeug.utils import secure_filename

#from . import
from resume import *
from BlackBoxCode  import Engine
import en_core_web_sm
nlp = en_core_web_sm.load()
#nlp = spacy.load('en_core_web_lg')

app = Flask(__name__)

app.secret_key = "super secret key"

app.config['UPLOAD_RESUME'] = 'Resumes'

app.config['UPLOAD_JD'] = 'Job_description'    # JobDescription path


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jd/upload')
def jd_upload():
    return render_template('jobdescription.html')


@app.route('/jd_uploaded', methods=['POST', 'GET'])
def jd_uploaded():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_JD'], filename))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('try_again'))


@app.route('/try_again')
def try_again():
    return render_template('try_again.html')

@app.route('/resume/<id>')
def open_file(id):
    path = app.config['UPLOAD_RESUME'] + '/' + id
    return send_file(path, attachment_filename=id)

@app.route('/resume/upload')
def upload_files():
    return render_template('resumes.html')


@app.route('/resumes_uploaded', methods=['POST', 'GET'])
def res_uploaded():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename_jd = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_RESUME'], filename_jd))
        return redirect(url_for('index'))
    else:
        return redirect(url_for('try_again'))


@app.route('/resume/compare' , methods=['GET'])
def compare_to_jds():

    flag = 0
    jd_path = app.config['UPLOAD_JD']
    paths = Path(jd_path).glob('*.txt')
    for path in paths:
        jd_path = path
        flag += 1
        break
    paths = Path(app.config['UPLOAD_RESUME']).glob('*.pdf')
    for path in paths:
        flag += 1
        break
    if flag != 2:
        return "<h1>Please upload both JobDescription and Resumes</h1>"
    else:
        path_id = list()
        my_list = list()
        jd = JobDescription(jd_path)
        id_list = list()
        temp_list = list()
        divide_obj = DividePaths(app.config['UPLOAD_RESUME'])
        for file in divide_obj.path_list:
            resume = Resume(file)
            resume.compare_with(jd)
            id_list.append(resume.id())
            my_list.append(resume.name)
        sort_id = SortId()
        scores = sort_id.sort_scores(id_list, my_list)
        for path in scores:
            a = re.sub(app.config['UPLOAD_RESUME'] + '/', '', path[1][0])
            a = a + '.pdf'
            path_id.append(a)
            print(path)
        for temp in scores:
            print(temp)
            temp_list.append([temp[0], temp[1][1]])

        temp_dict = {'score': temp_list, 'paths': path_id}
        return temp_dict
        #return render_template('id_score.html', result=temp_dict)
@app.route('/resume/getAnalysis')
def getSocialRanking():
    # https: // github.com / fzaninotto
    # https: // www.linkedin.com / in / fzaninotto /
    # https: // github.com / jaredpalmer
    # https: // www.linkedin.com / in / jaredlpalmer /
    #https://in.linkedin.com/in/meghna-lohani-12794414a
    #https://in.linkedin.com/in/aman44

    #df = Engine.getCall("Json/johncscott19.json","https://api.github.com/users/devillarry/repos")
    df1 = Engine.getCall("Json/ashutosh-roy95.json","https://api.github.com/users/devillarry/repos")
    df2 = Engine.getCall("Json/aniket-pawar.json","https://api.github.com/users/jaredpalmer/repos")
    df3 = Engine.getCall("Json/fzaninotto.json","https://api.github.com/users/fzaninotto/repos")
    df2['Id'][0]=2
    df3['Id'][0] = 3
    df2['Name'][0]="Aniket"
    df3['Name'][0]="Fzanion"
    #print(type(df))
    # print(df1.to_dict())
    # print(df2.to_dict())
    # print(df3.to_dict())

    # df1.append(df2)
    # df1.append(df3)
    print(pd.concat([df1,df2,df3]))

    temp_dict = {'1': df1.to_dict(), '2': df2.to_dict(), '3':df3.to_dict()}
    #print(df1.append(df2))
    #return  pd.concat([df1,df2,df3]).to_dict()
    return  temp_dict



app.run()
