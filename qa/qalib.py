#!/usr/bin/env python3
import os
import sys
import csv
import json
import time
import shutil
import requests
import itertools
import subprocess
import datetime
from pprint import pprint
from os.path import expanduser
from urllib.parse import urlparse
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'applibs'))
from nspvlib import *
from mm2lib import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))
from kmdlib import *

# Get and set config
cwd = os.getcwd()
home = expanduser("~")

CI_app_list = { 'mm2':{'repo':'https://github.com/KomodoPlatform/atomicDEX-API',
                        'branch':'mm2',
                        'ip':'http://127.0.0.1',
                        'port':'7783'},
                'nspv':{'repo':'https://github.com/jl777/libnspv',
                        'branch':'jl777',
                        'ip':'http://127.0.0.1',
                        'port':'7777'},
                'kmd-master':{'repo':'https://github.com/KomodoPlatform/komodo',
                        'branch':'master',
                        'ip':'http://127.0.0.1',
                        'port':'7771'},
                'kmd-jl777-beta':{'repo':'https://github.com/jl777/komodo',
                        'branch':'beta',
                        'ip':'http://127.0.0.1',
                        'port':'7771'}
                }

qa_folder = home+"/qa"
if not os.path.exists(qa_folder):
    os.mkdir(qa_folder)

def launch_chain(chain, paramlist, kmd_path, pubkey=''):
    if pubkey != '':
        paramlist.append("-pubkey="+pubkey)
    rpc[chain] = def_creds(chain)
    try:
        blocks = int(rpc[chain].getinfo()['blocks'])
        rpc[chain].stop()
        print("Stopping "+chain)
        time.sleep(60)
    except:
        pass
    commit = get_commit_hash(kmd_path)
    test_log = chain+"_"+commit+".log"
    test_output = open(test_log,'w+')
    print(paramlist)
    subprocess.Popen([kmd_path+"/komodod"]+paramlist, stdout=test_output, stderr=test_output, universal_newlines=True)
    loop = 0
    try:
        blocks = int(rpc[chain].getinfo()['blocks'])
    except:
        blocks = 0
        pass
    while blocks == 0:
        time.sleep(20)
        loop += 1
        try:
            blocks = int(rpc[chain].getinfo()['blocks'])
        except:
            blocks = 0
            pass
        if loop > 20:
            print("Something went wrong. Chain probably already running.")
            break
    print(" Use tail -f "+kmd_path+"/"+test_log+" for "+chain+" console messages")



def build_commit(app, branch=False, commit=False):
    repo_url = CI_app_list[app]['repo']
    repo_parse = urlparse(repo_url)
    repo_name = repo_parse.path.split('/')[-1]
    print("Building "+app+" binary from "+repo_url)
    apps_path = qa_folder+"/"+app
    repo_path = apps_path+"/"+repo_name
    tests_path = apps_path+"/tests"
    logs_path = apps_path+"/logs"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    if not os.path.exists(apps_path):
        os.mkdir(apps_path)
    if not os.path.exists(tests_path):
        os.mkdir(tests_path)
    if not os.path.exists(logs_path):
        os.mkdir(logs_path)
    os.chdir(apps_path)
    clone_proc = subprocess.run(['git', 'clone', '-n', repo_url], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    print(clone_proc.stdout)
    os.chdir(repo_path)
    if commit is not False:
        checkout_proc = subprocess.run(['git', 'checkout', commit], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(checkout_proc.stdout)
    elif branch is not False:
        checkout_proc = subprocess.run(['git', 'checkout', branch], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(checkout_proc.stdout)
    elif 'branch' in CI_app_list[app]:
        checkout_proc = subprocess.run(['git', 'checkout', CI_app_list[app]['branch']], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(checkout_proc.stdout)
    commit = get_commit_hash(repo_path)
    test_log = logs_path+"/"+app+"_build_"+commit+".log"
    test_output = open(test_log,'w+')
    if app == 'mm2':
        try:
            stop_mm2() # TODO: rename func in mm2lib
        except:
            pass
        #TODO: confirm this works after merging
        os.chdir(repo_path)
        build_proc = subprocess.run(['cargo', 'build', '--features', 'native', '-vv'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        shutil.move(qa_path+"/config/MM2.json", repo_path+"/target/debug/MM2.json")
        os.chdir(repo_path+"/target/debug/")
        subprocess.Popen([repo_path+"/target/debug/mm2"], stdout=test_output, stderr=test_output, universal_newlines=True)
    elif app == 'kmd-jl777-beta':
        try:
            rpc['KMD'].stop()
        except:
            pass
        os.chdir(repo_path)
        zparam_proc = subprocess.run(['./zcutil/fetch-params.sh'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(zparam_proc.stdout)
        build_proc = subprocess.run(['./zcutil/build.sh', '-j8'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        subprocess.Popen([repo_path+"/src/komodod"], stdout=test_output, stderr=test_output, universal_newlines=True)
    elif app == 'nspv':
        try:
            nspv_stop(nspv_ip, 'userpass') # TODO: rename func in nspvlib
        except:
            pass
        build_proc = subprocess.run([repo_path+'/autogen.sh'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        build_proc = subprocess.run([repo_path+'/configure'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(build_proc.stdout)
        os.chdir(repo_path)
        make_proc = subprocess.run(['make'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        #make_proc = subprocess.run(['make', 'check'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(make_proc.stdout)
        os.chdir(tests_path)
        subprocess.Popen([repo_path+"/nspv", "KMD", "-p", CI_app_list[app]['port']], stdout=test_output, stderr=test_output, universal_newlines=True)
    print("Build complete, "+app+" started.")
    print(" Use tail -f "+test_log+" for "+app+" console messages")
    return repo_path

def check_releases_list(app):
    if app not in CI_app_list:
        print("App "+app+" not in CI list ("+str(CI_app_list)+")")
        sys.exit(0)
    commits_list = []
    if app == 'mm2':
        r = requests.get("https://vsrm.dev.azure.com/ortgma/Marketmaker/_apis/release/approvals?api-version=5.0")
    # add other apps with elif here
    pending_releases_list = r.json()
    print(pending_releases_list)
    if pending_releases_list["count"] > 0:
        for release in pending_releases_list["value"]:
            release_info = requests.get("https://vsrm.dev.azure.com/ortgma/Marketmaker/_apis/release/releases/{}?api-version=5.0".format(str(release["release"]["id"])))
            commit = release_info.json()["artifacts"][0]["definitionReference"]["sourceVersion"]["id"]
            repo = "https://github.com/"+release_info.json()["artifacts"][0]["definitionReference"]["repository"]["name"]
            commits_list.append([repo,commit])
        print(commits_list)
    else:
        print("No "+app+" releases listed!")
        sys.exit(0)
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
def get_csv_filename(test_type, repo_path):
#    md5hash = get_md5sum(home+"/mm2_autotests/mm2")
    commit_hash = get_commit_hash(repo_path)
    time_obj = datetime.date.today()
    time_string = time_obj.strftime("%d")+"-"+time_obj.strftime("%B")+"-"+time_obj.strftime("%Y")
    csv_filename = test_type+"_"+time_string+"_"+commit_hash+".csv"
    return csv_filename

def upload_csv(file):
    url = 'http://oracle.earth/upload_csv/'
    files = {'file': open(file, 'rb')}
    r = requests.post(url, files=files)
    print(file+" uploaded to http://oracle.earth/qa_reports/")