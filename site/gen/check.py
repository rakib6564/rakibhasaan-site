import re,sys,subprocess,os
bad=0
for f in sys.argv[1:]:
    s=open(f).read()
    body=s[s.index('<x-dc>'):s.index('</x-dc>')]
    body=re.sub(r'<style>.*?</style>','',body,flags=re.S)
    for t in ['div','section','header','footer','nav','a','span','sc-if','sc-for','button','dl','svg','h1','h2','h3','p','ul','ol','li','details','summary','form','label','table','figure','blockquote','main','select','textarea']:
        o=len(re.findall(r'<'+t+r'[\s>]',body)); c=body.count('</'+t+'>')
        if o!=c: print(f,'MISMATCH',t,o,c); bad+=1
    holes=set(re.findall(r'\{\{\s*([a-zA-Z_]\w*)',body))
    js=s[s.index('class Component'):s.index('</script>',s.index('class Component'))]
    open('/tmp/claude-2225/-home-rakilluy-public-html/063f74fe-a12d-42fa-8970-1725619182d8/scratchpad/niche/c.js','w').write('class DCLogic{constructor(){this.state={}}setState(){}}\nvar sessionStorage={getItem(){return null},setItem(){}};\n'+js+'\nvar c=new Component();var v=c.renderVals();console.log(JSON.stringify(Object.keys(v)));')
    r=subprocess.run(['node','/tmp/claude-2225/-home-rakilluy-public-html/063f74fe-a12d-42fa-8970-1725619182d8/scratchpad/niche/c.js'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
    if r.returncode: print(f,'JS ERR',r.stderr[:400]); bad+=1; continue
    import json; keys=set(json.loads(r.stdout.strip().splitlines()[-1]))
    loopvars={'it','f','c','s','o','t','m','w','im','p','r','x'}
    missing=[h for h in holes if h not in keys and h not in loopvars]
    if missing: print(f,'MISSING HOLES',missing); bad+=1
print('problems:',bad)
