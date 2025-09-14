from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pathlib, json, time, uuid, os

app = FastAPI(title='History & Metadata')
DB = pathlib.Path('/data/history.json')
DB.parent.mkdir(parents=True, exist_ok=True)
if not DB.exists():
    DB.write_text('[]')

class Project(BaseModel):
    job_id: str | None = None
    poem: str | None = None
    style: str | None = None
    audio: str | None = None
    midi: str | None = None

@app.post('/projects')
async def create_project(p: Project):
    data = json.loads(DB.read_text())
    entry = {'id': p.job_id or str(uuid.uuid4()), 'poem': p.poem, 'style': p.style, 'audio': p.audio, 'midi': p.midi, 'created_at': time.time()}
    data.append(entry)
    DB.write_text(json.dumps(data))
    return {'ok': True, 'id': entry['id']}

@app.get('/projects')
async def list_projects():
    return json.loads(DB.read_text())

@app.get('/projects/{project_id}')
async def get_project(project_id: str):
    data = json.loads(DB.read_text())
    for e in data:
        if e['id'] == project_id:
            return e
    raise HTTPException(status_code=404, detail='not found')