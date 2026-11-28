import json,re,sys,urllib.request,urllib.parse
src=open('index.html',encoding='utf-8').read()
KEY=re.search(r'AIza[0-9A-Za-z_-]+',src).group(0)
ROOT=re.search(r"DRIVE_FOLDER\s*=\s*'([^']+)'",src).group(1)
FOLDER='application/vnd.google-apps.folder'
def get(u):
    req=urllib.request.Request(u,headers={'Referer':'https://weichi2001.github.io/taigi-ktv/'})
    with urllib.request.urlopen(req,timeout=30) as r: return r.read().decode('utf-8')
def q(pid):
    out=[];tok=''
    while True:
        u='https://www.googleapis.com/drive/v3/files?q='+urllib.parse.quote("'%s' in parents and trashed=false"%pid)+'&fields='+urllib.parse.quote('nextPageToken,files(id,name,mimeType,size,md5Checksum,createdTime)')+'&pageSize=1000&key='+KEY+('&pageToken='+tok if tok else '')
        j=json.loads(get(u));out+=j.get('files',[]);tok=j.get('nextPageToken','')
        if not tok:return out
root=q(ROOT);lst=[];dirs=[m for m in root if m['mimeType']==FOLDER]
for m in root:
    if m['mimeType']!=FOLDER: lst.append({**m,'rel':'KTV/'+m['name']})
for d in dirs:
    for m in q(d['id']):
        if m['mimeType']!=FOLDER: lst.append({**m,'rel':'KTV/%s/%s'%(d['name'],m['name'])})
texts={}
for m in lst:
    if m['name'].lower().endswith('.json'):
        t=get('https://www.googleapis.com/drive/v3/files/%s?alt=media&key=%s'%(m['id'],KEY))
        texts[m['id']]={'m':m.get('md5Checksum',''),'t':t}
json.dump({'at':0,'list':lst,'texts':texts},open('drive-snapshot.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'),sort_keys=True)
print(len(lst),'files',len(texts),'json')
