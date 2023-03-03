from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

try:
    conn = psycopg2.connect(host= 'http://43.204.112.112:8000', database = 'fAPI', user = 'postgres', password = 'Shikarpur', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successfull")
except Exception as error:
    print("Connection to database failed")
    print("Error: ", error)

my_posts = [{"tittle":"IPL","content":"Indian","id":1},{"tittle":"BBL","content":"Australia","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get('/',tags=['Blogs'])
def get_user():
    return {'message':'Sagar'}

@app.get('/posts',tags=['Blogs'])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post('/posts', status_code= status.HTTP_201_CREATED,tags=['Blogs'])
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}",tags=['Blogs'])
def get_post(id:str):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id{id} was not found")
    return {"post-details":post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id{id} was not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}',tags=['Blogs'])
def update_post(id:int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """,
                   (post.title,post.content,post.published, str(id)))
    updated_posts = cursor.fetchone()
    conn.commit()
    if updated_posts == None:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id{id} was not found")
    
    return {"data":updated_posts}

