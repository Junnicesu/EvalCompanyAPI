import logging
import os

import httpx
import xmltodict
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Mount the images directory
app.mount("/images", StaticFiles(directory="images"), name="images")

# Serve the favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/images/MW-sj.ico")

# default
BASE_XML_URL = (
    "https://raw.githubusercontent.com/MiddlewareNewZealand/"
    "evaluation-instructions/main/xml-api/"
)

# read from the env
BASE_XML_URL = os.getenv("BASE_XML_URL", BASE_XML_URL)

logging.info(f"Using BASE_XML_URL: {BASE_XML_URL}")  # Debugging purpose
logging.info(f"Using BASE_XML_URL: {BASE_XML_URL}")

BASE_XML_URL += "{id}.xml"


class Company(BaseModel):
    id: int
    name: str
    description: str


class ErrorResponse(BaseModel):
    error: str
    error_description: str


@app.get(
    "/companies/{id}", response_model=Company, responses={404: {"model": ErrorResponse}}
)
async def get_company(id: int):
    xml_url = BASE_XML_URL.format(id=id)
    logging.info(f"Fetching XML from: {xml_url}")

    async with httpx.AsyncClient() as client:
        response = await client.get(xml_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to fetch XML"
        )

    # Debugging: Print raw XML response
    logging.info("Raw XML Response:")
    logging.info(response.text)

    try:
        xml_data = xmltodict.parse(response.text)
        logging.info("Parsed XML Data:")
        logging.info(xml_data)  # Log parsed data
        logging.info(xml_data)

        company = xml_data.get("Data")
        if not company:
            raise HTTPException(status_code=404, detail="Company not found in XML")

        return Company(
            id=int(company["id"]),
            name=company["name"],
            description=company["description"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing XML: {str(e)}")


# Run the server with: uvicorn src.main:app --reload
        raise HTTPException(status_code=500, detail=f"Error processing XML: {str(e)}")
