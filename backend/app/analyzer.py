import ast
import re
from collections import Counter

SKIP={'.git','node_modules','vendor','dist','build','__pycache__','coverage'}
EXT={'.py':'Python','.js':'JavaScript','.jsx':'JavaScript','.ts':'TypeScript','.tsx':'TypeScript','.java':'Java','.go':'Go','.rs':'Rust','.md':'Markdown','.json':'JSON','.yml':'YAML','.yaml':'YAML','.toml':'TOML'}

def analyze(files):
    langs=Counter(); findings=[]; entries=[]; deps=[]; count=0
    rules=[
        (re.compile(r'''(?i)(api[_-]?key|secret|password)\s*=\s*["'][^"']{8,}["']'''),'high','Possible hardcoded secret','Move the value to a secret manager or environment variable.'),
        (re.compile(r'(?i)pickle\.loads?\s*\('),'high','Unsafe deserialization pattern','Do not deserialize untrusted pickle data; use a safe, schema-validated format.'),
        (re.compile(r'(?i)subprocess\.(run|call|Popen)\s*\([^\n]*shell\s*=\s*True'),'medium','Shell-enabled subprocess call','Avoid shell=True and pass an argument list; validate untrusted inputs.'),
        (re.compile(r'''(?i)execute\s*\(\s*f["']'''),'high','Potential SQL built with interpolation','Use parameterized queries and bind variables.')]
    for f in files:
        path=f.get('path',''); content=f.get('content','')
        if not content or any(x in path.split('/') for x in SKIP): continue
        count+=1; ext='.'+path.rsplit('.',1)[-1].lower() if '.' in path else ''; langs[EXT.get(ext,'Other')]+=1
        if path.lower() in {'main.py','app.py','index.js','index.ts','server.js','manage.py','cmd/main.go'}: entries.append(path)
        if path.lower().endswith(('requirements.txt','pyproject.toml','package.json','pom.xml','go.mod')): deps.append(path)
        for i,line in enumerate(content.splitlines(),1):
            for pattern,sev,desc,fix in rules:
                if pattern.search(line): findings.append({'path':path,'line':i,'severity':sev,'category':'security heuristic','confidence':0.72,'description':desc,'evidence':line.strip()[:500],'recommendation':fix,'verification_status':'unverified heuristic'})
        if ext=='.py':
            try:
                tree=ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and len(node.body)>30:
                        findings.append({'path':path,'line':node.lineno,'severity':'low','category':'maintainability','confidence':0.65,'description':f"Long function '{node.name}' ({len(node.body)} top-level statements)",'evidence':f"Function spans approximately {getattr(node,'end_lineno',node.lineno)-node.lineno+1} lines.",'recommendation':'Consider extracting cohesive operations into smaller functions.','verification_status':'unverified heuristic'})
            except SyntaxError: pass
    summary=f"Inspected {count} text files. Detected {len(langs)} language categories and {len(findings)} heuristic findings. Entry points: {', '.join(entries) if entries else 'not identified'}; dependency manifests: {', '.join(deps) if deps else 'not identified'}."
    return {'file_count':count,'languages':dict(langs),'entry_points':entries,'dependency_files':deps,'findings':findings,'summary':summary}

def chunks(files,max_chars=3500):
    result=[]
    for f in files:
        text=f.get('content',''); lines=text.splitlines(); start=0
        while start<len(lines):
            end=start; size=0
            while end<len(lines) and size+len(lines[end])+1<max_chars: size+=len(lines[end])+1; end+=1
            result.append({'path':f['path'],'start_line':start+1,'end_line':max(start+1,end),'content':'\n'.join(lines[start:end])})
            start=max(end,start+1)
    return result

def retrieve(files,question,k=5):
    terms={x.lower() for x in re.findall(r'[A-Za-z_][A-Za-z0-9_]{2,}',question)}
    scored=[]
    for c in chunks(files):
        body=c['content'].lower(); score=sum(body.count(t) for t in terms)
        if score: scored.append((score,c))
    return [c for _,c in sorted(scored,key=lambda x:x[0],reverse=True)[:k]]
