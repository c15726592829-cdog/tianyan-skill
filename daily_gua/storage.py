"""Atomic daily reservations and private per-person location preferences."""
import json,sqlite3
from contextlib import contextmanager
from pathlib import Path

class GuaStore:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS gua(scope TEXT,day TEXT,payload TEXT NOT NULL,PRIMARY KEY(scope,day))")
            db.execute("CREATE TABLE IF NOT EXISTS locations(scope TEXT PRIMARY KEY,city TEXT,timezone TEXT)")
    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.path,timeout=15)
        try:
            with db:yield db
        finally:db.close()
    def get(self,scope,day):
        with self.connect() as db:row=db.execute("SELECT payload FROM gua WHERE scope=? AND day=?",(scope,str(day))).fetchone()
        return json.loads(row[0]) if row else None
    def reserve(self,scope,day,payload):
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            cur=db.execute("INSERT OR IGNORE INTO gua VALUES(?,?,?)",(scope,str(day),json.dumps(payload,ensure_ascii=False)))
            row=db.execute("SELECT payload FROM gua WHERE scope=? AND day=?",(scope,str(day))).fetchone()
            return cur.rowcount==1,json.loads(row[0])
    def patch(self,scope,day,**fields):
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row=db.execute("SELECT payload FROM gua WHERE scope=? AND day=?",(scope,str(day))).fetchone()
            if not row:raise ValueError("没有可更新的原卦")
            data=json.loads(row[0]);data.update(fields)
            db.execute("UPDATE gua SET payload=? WHERE scope=? AND day=?",(json.dumps(data,ensure_ascii=False),scope,str(day)))
            return data
    def location(self,scope):
        with self.connect() as db:row=db.execute("SELECT city,timezone FROM locations WHERE scope=?",(scope,)).fetchone()
        return {'city':row[0],'timezone':row[1]} if row else None
    def set_location(self,scope,city,timezone):
        with self.connect() as db:db.execute("INSERT INTO locations VALUES(?,?,?) ON CONFLICT(scope) DO UPDATE SET city=excluded.city,timezone=excluded.timezone",(scope,city,timezone))
