#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
from os.path import expanduser
from urllib.parse import urlparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'applibs'))
from nspvlib import *
from mm2lib import *

# Get and set config
cwd = os.getcwd()
home = expanduser("~")

CI_app_list = {'mm2':{'repo':'https://github.com/getthislater'},
                'nspv':{'repo':'https://github.com/jl777/libnspv'}}
                
qa_folder = home+"/qa"
if not os.path.exists(qa_folder):
    os.mkdir(qa_folder)

def build_commit(app, branch=False, commit=False):
    repo_url = CI_app_list[app]['repo']
    repo_parse = urlparse(repo_url)
    repo_name = repo_parse.path.split('/')[-1]
    print("Building "+app+" binary from "+repo_url)
    app_path = qa_folder+"/"+app+"/"+repo_parse.path
    if os.path.exists(app_path):
        shutil.rmtree(qa_folder+"/"+app+"/")
    os.chdir(qa_folder+"/"+app)
    clone_proc = subprocess.run(['git', 'clone', '-n', repo_url], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    print(clone_proc.stdout)
    os.chdir(app_path)
    if commit is not False:
        checkout_proc = subprocess.run(['git', 'checkout', commit], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(checkout_proc.stdout)
    elif branch is not False:
        checkout_proc = subprocess.run(['git', 'checkout', branch], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(checkout_proc.stdout)
    commit = get_commit_hash(app_path)
    test_log = qa_folder+"/logs/"+app+"_build_"+commit+".log"
    test_output = open(test_log,'w+')
    if app == 'mm2':
        try:
            stop_mm2() # TODO: rename func in mm2lib
        except:
            pass
        #TODO: confirm this works after merging
        build_proc = subprocess.run(['cargo', 'build', '--features', 'native', '-vv'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        if os.path.exists(home+"/mm2_autotests/mm2"):
            os.remove(home+"/mm2_autotests/mm2")
        shutil.move(home+"/mm2_autotests/tests/SuperNET/target/debug/mm2", home+"/mm2_autotests/mm2")
        os.chdir(home+"/mm2_autotests/")
        Popen([home+"/mm2_autotests/mm2"], stdout=test_output, stderr=test_output, universal_newlines=True)
    elif app == 'nspv':
        try:
            nspv_stop() # TODO: rename func in nspvlib
        except:
            pass
        build_proc = subprocess.run(['autogen.sh'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        build_proc = subprocess.run(['configure'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        build_proc = subprocess.run(['make', 'check'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        os.chdir(qa_folder+"/"+app+"/tests")
        Popen([app_path+"/nspv", "KMD"], stdout=test_output, stderr=test_output, universal_newlines=True)
    print("Build complete, "+app+" started.")
       print(" Use tail -f "+test_log+" for "+app+" console messages")

def check_releases_list(app):
    if app not in CI_app_list:
        print("App "+app+" not in CI list ("+str(CI_app_list)+")")
    commits_list = []
    if app == 'mm2':
        r = requests.get("https://vsrm.dev.azure.com/ortgma/Marketmaker/_apis/release/approvals?api-version=5.0")
    # add other apps with elif here
    pending_releases_list = r.json()
    if pending_releases_list["count"] > 0:
        for release in pending_releases_list["value"]:
            release_info = requests.get("https://vsrm.dev.azure.com/ortgma/Marketmaker/_apis/release/releases/{}?api-version=5.0".format(str(release["release"]["id"])))
            commit = release_info.json()["artifacts"][0]["definitionReference"]["sourceVersion"]["id"]
            repo = "https://github.com/"+release_info.json()["artifacts"][0]["definitionReference"]["repository"]["name"]
            commits_list.append([repo,commit])
    return commits_list

def get_md5sum(file):
    proc = subprocess.run(['md5sum', file], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = proc.stdout
    return output.split()[0]

def get_commit_hash(repo_path):
    os.chdir(repo_path)
    proc = subprocess.run(['git', 'log', '-n', '1'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = proc.stdout
    return output.split()[1]
    
# Output filename format | Base | test type | date | commit |
def get_csv_filename(test_type, repo):
#    md5hash = get_md5sum(home+"/mm2_autotests/mm2")
    commit_hash = get_commit_hash(home+repo)
    time_obj = datetime.date.today()
    time_string = time_obj.strftime("%d")+"-"+time_obj.strftime("%B")+"-"+time_obj.strftime("%Y")
    csv_filename = test_type+"_"+time_string+"_"+commit_hash+".csv"
    return csv_filename
