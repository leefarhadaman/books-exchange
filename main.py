from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from routes import auth, books, wishlist, requests, messages
from database import engine
from models import user, book, wishlist, request, message

app = FastAPI(title="Used Books Exchange")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-app.vercel.app"],  # Update with Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(wishlist.router)
app.include_router(requests.router)
app.include_router(messages.router)

@app.on_event("startup")
def startup():
    user.Base.metadata.create_all(bind=engine)
    book.Base.metadata.create_all(bind=engine)
    wishlist.Base.metadata.create_all(bind=engine)
    request.Base.metadata.create_all(bind=engine)
    message.Base.metadata.create_all(bind=engine)

@app.get("/")
@limiter.limit("100/minute")
async def root():
    return {"message": "Welcome to Used Books Exchange"}