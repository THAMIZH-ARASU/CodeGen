
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from prometheus_client import make_asgi_app

app = FastAPI()

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class Review(BaseModel):
    id: int
    project_name: str
    issues: List[Dict[str, Any]]
    status: str # pending, approved, rejected

reviews_db: List[Review] = []
next_review_id = 0

@app.get("/reviews", response_model=List[Review])
def list_reviews():
    return reviews_db

@app.post("/reviews/{review_id}/approve")
def approve_review(review_id: int):
    for review in reviews_db:
        if review.id == review_id:
            review.status = "approved"
            return {"message": f"Review {review_id} approved."}
    return {"error": "Review not found"}, 404

@app.post("/reviews/{review_id}/reject")
def reject_review(review_id: int, feedback: Dict[str, str]):
    for review in reviews_db:
        if review.id == review_id:
            review.status = "rejected"
            # In a real implementation, this feedback would be sent to a fixer agent.
            print(f"Feedback for review {review_id}: {feedback}")
            return {"message": f"Review {review_id} rejected."}
    return {"error": "Review not found"}, 404

def add_review(project_name: str, issues: List[Dict[str, Any]]) -> int:
    global next_review_id
    review = Review(
        id=next_review_id,
        project_name=project_name,
        issues=issues,
        status="pending"
    )
    reviews_db.append(review)
    next_review_id += 1
    return review.id

def get_review_status(review_id: int) -> str:
    for review in reviews_db:
        if review.id == review_id:
            return review.status
    return "not_found"
