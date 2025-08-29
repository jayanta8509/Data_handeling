from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import pandas as pd
import csv
import requests
import os
import time
import logging
from datetime import datetime
from typing import List, Optional
import uvicorn

from Woocommerce import save_id_name_to_csv
from exl_file import artist_title_to_csv
from compare import compare_csv_texts_vectorized

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title="CSV Data Processor API",
    description="Production-ready API for processing Excel and WooCommerce data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

class ProcessResponse(BaseModel):
    status: int
    message: str
    unique_ids: Optional[List[int]] = None
    unique_count: Optional[int] = None
    processing_time: Optional[float] = None


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

# Main processing endpoint
@app.get("/process")
async def process_data():
    """
    Main endpoint that:
    1. Processes Excel file to CSV
    2. Processes WooCommerce API data to CSV  
    3. Compares both CSV files to find unique items
    """
    try:
        start_time = time.time()
        logger.info("Starting data processing workflow")
        
        # Step 1: Process Excel file
        excel_link = "https://www.cobraside.com/catalog/instock/STK_With_QTY.xlsx"


        excel_result = artist_title_to_csv(excel_link)
        if isinstance(excel_result, dict):
            raise HTTPException(status_code=500, detail=f"Excel CSV generation failed: {excel_result}")
        excel_path = excel_result
        
        # Step 2: Process WooCommerce API
        Woocommerec_link = "https://workflows.poptechstudio.ai/webhook/get-woo-data"

        woo_result = save_id_name_to_csv(Woocommerec_link)
        if not isinstance(woo_result, dict) or woo_result.get("Status") != 200:
            raise HTTPException(status_code=500, detail=f"WooCommerce CSV generation failed: {woo_result}")
        woo_path = woo_result["message"]

        # Step 3: Compare the CSV files
        comparison_result = compare_csv_texts_vectorized(
            excel_path,woo_path
        )
        
        total_time = time.time() - start_time
        
        
        
        logger.info(f"Complete workflow finished in {total_time:.3f} seconds")
        
        return ProcessResponse(
            status=200,
            message="Data processing completed successfully",
            unique_ids=comparison_result,
            unique_count= len(comparison_result),
            processing_time=total_time,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in process_data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    


# Production server runner
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Set to False for production
        workers=1,     # Increase for production based on CPU cores
        log_level="info"
    )