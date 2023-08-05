import requests
import re
import os
import sqlparse
import prettytable as pt
import json
from .sparkvar import savejson


class HueCreator(object):
    def __init__(self):
        self.__session = requests.session()
        self.__query = {}
        self.__session.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
        }

        ini = os.path.expanduser('~') + '/.sparktool.json'
        with open(ini, 'r') as f:
            cfg = dict(json.load(f))
        username = cfg['hue'].get('username', '')
        password = cfg['hue'].get('password', '')
        self.__url = cfg['hue_editor']
        if username and password:
            self.__param = {'username': username, 'password': password}
            self.__login()
            self.__getquery()
        else:
            raise Exception(
                'please use switch_hue to set username and password')

    def __login(self):
        url = self.__url + '/accounts/login/'
        r = self.__session.get(url)
        csr = re.findall(r"name='csrfmiddlewaretoken' value='(.*?)'", r.text)
        if csr:
            self.__param['csrfmiddlewaretoken'] = csr[0]
            self.__param['next'] = '/'
        temp = self.__session.post(url, data=self.__param)
        csr2 = re.findall(
            r"name='csrfmiddlewaretoken' value='(.*?)'", temp.text)
        self.__session.headers['X-CSRFToken'] = csr2[0]

    def __getquery(self):
        r = self.__session.get(self.__url + '/desktop/api2/doc/')
        rjson = r.json()
        for children in rjson['children']:
            idd = children['id']
            last_modified = children['last_modified']
            name = children['name']
            description = children['description']
            if name != '.Trash':
                self.__query[idd] = {
                    'last_modified': last_modified,
                    'name': name,
                    'description': description
                }
    
    def __searchquery(self, name):
        uuid = None
        matchlist = []
        for query in self.__query:
            if name == self.__query[query]['name']:
                matchlist.append(query)

        if not matchlist:
            print('File not be found, file list is as below')
            self.hue_printlist(ifrefresh=False)
        elif len(matchlist) > 1:
            print('Multiple file was found, please add param uuid')
            self.hue_printlist(ifrefresh=False)
        else:
            uuid = matchlist[0]
        
        return uuid

    def hue_printlist(self, ifrefresh=True):
        if ifrefresh:
            self.__getquery()
        tb = pt.PrettyTable()
        tb.field_names = ["id", "name", "description", 'last_modified']

        if self.__query:
            for query in self.__query:
                idd = query
                name = self.__query[query]['name']
                description = self.__query[query]['description']
                last_modified = self.__query[query]['last_modified']
                tb.add_row([idd, name, description, last_modified])
            print(tb)
        else:
            'There is no query saved'

    def hue_getscript(self, name, uuid=None, ifreplacendv=True, ifprint=False):
        self.__getquery()
        if uuid:
            uuid = int(uuid)
            if uuid not in self.__query:
                print('File not be found, file list is as below')
                self.hue_printlist(ifrefresh=False)
        else:
            uuid = self.__searchquery(name)

        if uuid:
            r = self.__session.get(
                self.__url + '/desktop/api2/doc/?uuid={0}&data=true&dependencies=true'.format(uuid))

            rjson = r.json()
            scr = rjson['data']['snippets'][0]['statement_raw']

            if ifreplacendv:
                scr = scr.replace('ndv(', 'count(')

            scr_b = sqlparse.format(
                scr, reindent=True, keyword_case='lower', identifier_case='lower', strip_comments=True)

            if ifprint:
                print(scr_b)

            return scr

    def hue_setscript(self, sql, name, uuid=None, savejson=savejson):
        name = str(name)
        a = []
        b = []
        ss = sqlparse.split(sql)
        for i in range(len(ss)):
            if ss[i]:
                raw = ss[i].replace('\n', '\\n')
                a.append(raw) if i == 0 else a.append('\\n'+raw)
                b.append('"'+raw+'"') if i == 0 else b.append('"\\n'+raw+'"')
        sqlraw = ''.join(a)
        sqllist = ','.join(b)
        sqllast = a[-1]
        savejson = savejson.replace('{name}', name)
        savejson = savejson.replace('{sqlraw}', sqlraw)
        savejson = savejson.replace('{sqllist}', sqllist)
        savejson = savejson.replace('{sqllast}', sqllast)
        if not uuid:
            param = {
                "type": "impala",
                "directory_uuid": ""
                }
            r = self.__session.post(
                self.__url + '/notebook/api/create_notebook', data=param).json()
            session_uuid = r["notebook"]["uuid"]
            savejson = savejson.replace('{id}', 'null')
        else:
            self.__getquery()
            uuid = int(uuid)
            if uuid not in self.__query:
                print('File not be found, file list is as below')
                self.hue_printlist(ifrefresh=False)
            else:
                r = self.__session.get(
                    self.__url + '/desktop/api2/doc/?uuid={0}&data=true&dependencies=true'.format(uuid)).json()
                session_uuid = r['document']['uuid']
                savejson = savejson.replace('{id}', str(uuid))

        savejson = savejson.replace('{uuid}', session_uuid)
        data = {
            'notebook': savejson,
            'editorMode': 'true'
            }
        r2 = self.__session.post(self.__url + '/notebook/api/notebook/save', data=data).json()
        try:
            print('File has been saved as id: %s, name: %s' %(r2['id'], r2['name']))
        except Exception:
            print('Error: ', r2)
