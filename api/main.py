from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
import pandas as pd
from dotenv import load_dotenv
from api.models import License, LicenseUpdate, CategorySummary
from api.config import Settings
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="License Classification API",
    description="API for classifying software licenses using Open AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_settings():
    return Settings()


@app.get("/")
async def root():
    return {"message": "License Classification API"}


@app.get("/licenses", response_model=List[License])
async def get_licenses(settings: Annotated[Settings, Depends(get_settings)]):
    """Get all classified licenses"""
    if not os.path.exists(settings.output_licenses_csv):
        return []
    df = pd.read_csv(settings.output_licenses_csv)
    return df.to_dict("records")


@app.get("/summary", response_model=List[CategorySummary])
async def get_summary(settings: Annotated[Settings, Depends(get_settings)]):
    """Get aggregated metrics by category"""
    if not os.path.exists(settings.output_licenses_csv):
        return []
    df = pd.read_csv(settings.output_licenses_csv)
    summary = df.groupby("category").agg({
        "license_id": "count",
        "manually_validated": "sum"
    }).reset_index()
    summary.columns = ["category", "count", "validated_count"]
    return summary.to_dict("records")


@app.put("/licenses/{license_id}", response_model=License)
async def update_license(
    settings: Annotated[Settings, Depends(get_settings)],
    license_id: int,
    update: LicenseUpdate):
    """Update a license classification"""
    if not os.path.exists(settings.output_licenses_csv):
        raise HTTPException(status_code=404, detail="No licenses found")
    
    df = pd.read_csv(settings.output_licenses_csv)
    if license_id not in df["license_id"].values:
        raise HTTPException(status_code=404, detail="License not found")
    
    # Update the license
    mask = df["license_id"] == license_id
    df.loc[mask, "category"] = update.category
    df.loc[mask, "explanation"] = update.explanation
    df.loc[mask, "manually_validated"] = True
    
    # Save the updated data
    df.to_csv(settings.output_licenses_csv, index=False)
    return df[df["license_id"] == license_id].to_dict("records")[0]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 