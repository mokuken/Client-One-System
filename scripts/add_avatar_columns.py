import sqlite3, os, sys
candidates = ['instance/site.db','site.db']
for p in candidates:
    if os.path.exists(p):
        db = p
        break
else:
    print('No DB file found in expected locations:', candidates)
    sys.exit(1)
print('Using DB:', db)
conn = sqlite3.connect(db)
cur = conn.cursor()
for table in ('owner','user'):
    cur.execute("PRAGMA table_info('%s')" % table)
    cols = [r[1] for r in cur.fetchall()]
    print(table, 'columns before:', cols)
    if 'avatar' not in cols:
        try:
            cur.execute("ALTER TABLE %s ADD COLUMN avatar VARCHAR(300)" % table)
            print('Added avatar column to', table)
        except Exception as e:
            print('Failed to add column to', table, 'error:', e)
    else:
        print('avatar already present on', table)
conn.commit()
cur.execute("PRAGMA table_info('owner')")
print('owner columns after:', [r[1] for r in cur.fetchall()])
cur.execute("PRAGMA table_info('user')")
print('user columns after:', [r[1] for r in cur.fetchall()])
conn.close()
