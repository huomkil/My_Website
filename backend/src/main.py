import uvicorn
from fastapi import FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware

# 创建 FastAPI 应用
app = FastAPI(
    title="My API",
    description="简单的 API 服务",
    version="0.1.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路径
@app.get("/u")
async def root(u: str = Header(...)):
    return {"u": u}

@app.get("/")
async def root(request: Request):
    return {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path": request.url.path,
        "client": str(request.client),
        "cookies": request.cookies,
    }

# 传递用户数据
@app.get("/user/{user}")
async def get_root(user: int):
    return user

@app.get("/user")
async def get_user(page: int = 1,size: int =10):
    return {"page": page,"size": size}

# 直接运行 
# irm http://127.0.0.1:8000/
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)