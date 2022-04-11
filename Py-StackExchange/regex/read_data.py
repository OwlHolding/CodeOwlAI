import sqlite3 as db
import sys
import re  

def read_sqlite(db_path,exectCmd):
    conn = db.connect(db_path)  
    cursor=conn.cursor()        
    conn.row_factory=db.Row    
    cursor.execute(exectCmd)  
    rows=cursor.fetchall()     
    return rows

def filter_comment(testStr):
    first = ''
    if '#' in testStr:
        # split last
        first = testStr.rsplit('#')[0].strip()
    elif '//' in testStr:
        first = testStr.rsplit('//')[0].strip()
    else:
        pass
    if first.endswith("$") or first.endswith("$/") or first.endswith("$\"") or first.endswith("$/\""):
        return first
    else:
        return ''

def find_regex(c, result):
    if len(c) > 2 :
        # Assign
        if len(c.split('=')) == 2:
            c = c.split('=')[1].strip()
    
        # java pattern?
        # python match?
        # JavaScript?
        if c.startswith("^") or c.startswith("/^") or c.startswith("\"/^") or c.startswith("\"^"):
            if len(filter_comment(c)) > 0:
                c = filter_comment(c)
            c = c.strip().replace("&gt;",">").replace("&lt;","<")
            if c not in result:
                result.add(c)
            print c
        else:
            pass
            

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        print('Too many args...')
    
    dbName = "../data/regex.db"
    cmd = "select * from answer"
    rows = read_sqlite(dbName, cmd)
    result = set()
    count = 0
    for r in rows:
        if r[2] <= 0:
            count += 1
            continue
        #  print count, ', ', r[1]
        print count
        codeList = re.findall(r'<code>(.*?)</code>', r[1],re.DOTALL)
        for c in codeList:
            clist = c.split('\n')
            for _str in clist:
                find_regex(_str.strip(),result)
        count += 1
    print result
