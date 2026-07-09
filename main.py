# Admission Number: C027-01-0827/2024

from typing import Optional, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ----------------------------
# Student Information
# ----------------------------

ADMISSION_NUMBER = "C027-01-0827/2024"

CATEGORIES = ["Development", "Design", "Writing"]
CURRENCY = "KES"

app = FastAPI(
    title=f"GigHub API",
    description=f"Nairobi Freelance Gigs Platform\nAdmission Number: {ADMISSION_NUMBER}",
    version="1.0.0"
)

# ----------------------------
# Initial Dataset (9 gigs)
# ----------------------------

gigs_db = [
    {
        "id": 1,
        "title": "Build React Dashboard",
        "description": "Build a responsive React dashboard for a fintech company with modern UI components.",
        "category": "Development",
        "budget": 25000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Company Logo Design",
        "description": "Design a professional company logo suitable for digital and print branding materials.",
        "category": "Design",
        "budget": 12000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Mwangi"
    },
    {
        "id": 3,
        "title": "Blog Article Writing",
        "description": "Write high quality SEO articles for a technology website targeting African startups.",
        "category": "Writing",
        "budget": 8000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Grace Wanjiku"
    },
    {
        "id": 4,
        "title": "Portfolio Website",
        "description": "Develop a modern responsive portfolio website using HTML CSS JavaScript and FastAPI.",
        "category": "Development",
        "budget": 30000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Otieno"
    },
    {
        "id": 5,
        "title": "Poster Design",
        "description": "Create attractive promotional posters for a university technology conference event.",
        "category": "Design",
        "budget": 10000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Lucy Atieno"
    },
    {
        "id": 6,
        "title": "Product Description",
        "description": "Write engaging product descriptions for an online electronics store with SEO optimization.",
        "category": "Writing",
        "budget": 7000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Kevin Maina"
    },
    {
        "id": 7,
        "title": "API Integration",
        "description": "Integrate payment APIs into an existing ecommerce application securely and efficiently.",
        "category": "Development",
        "budget": 35000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Brian Kimani"
    },
    {
        "id": 8,
        "title": "Business Card Design",
        "description": "Design elegant business cards for a startup company with printable high resolution files.",
        "category": "Design",
        "budget": 5000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Faith Njeri"
    },
    {
        "id": 9,
        "title": "Technical Report Writing",
        "description": "Prepare a detailed technical report documenting software testing procedures and outcomes.",
        "category": "Writing",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Samuel Kiptoo"
    }
]

# ----------------------------
# Pydantic Models
# ----------------------------

class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20, max_length=500)
    category: Literal["Development", "Design", "Writing"]
    budget: float = Field(..., gt=0)
    client_name: str = Field(..., min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None


# ----------------------------
# Home Endpoint
# ----------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to GigHub API",
        "admission_number": ADMISSION_NUMBER
    }


# ----------------------------
# Get All Gigs (with filtering)
# ----------------------------

@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):
    results = gigs_db

    if category:
        results = [
            gig for gig in results
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] <= max_budget
        ]

    return results


# ----------------------------
# Search Gigs
# ----------------------------

@app.get("/gigs/search")
def search_gigs(q: str):
    return [
        gig
        for gig in gigs_db
        if q.lower() in gig["title"].lower()
    ]


# ----------------------------
# Get One Gig
# ----------------------------

@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):

    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


# ----------------------------
# Create Gig
# ----------------------------

@app.post("/gigs", status_code=201)
def create_gig(gig: GigCreate):

    new_gig = gig.model_dump()

    new_gig["id"] = len(gigs_db) + 1
    new_gig["currency"] = CURRENCY
    new_gig["status"] = "Open"

    gigs_db.append(new_gig)

    return new_gig


# ----------------------------
# Update Gig
# ----------------------------

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, update: GigUpdate):

    for gig in gigs_db:

        if gig["id"] == gig_id:

            if update.budget is not None:
                gig["budget"] = update.budget

            if update.status is not None:
                gig["status"] = update.status

            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


# ----------------------------
# Delete Gig
# ----------------------------

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "deleted_gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")