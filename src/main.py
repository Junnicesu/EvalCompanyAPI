from fastapi import FastAPI, HTTPException
import requests
import xmltodict
from pydantic import BaseModel
import logging
import os

app = FastAPI()

# BASE_XML_URL = "https://raw.githubusercontent.com/MiddlewareNewZealand/evaluation-instructions/main/xml-api/{id}.xml"
# read from the env
BASE_XML_URL = os.getenv("BASE_XML_URL", "https://raw.githubusercontent.com/MiddlewareNewZealand/evaluation-instructions/main/xml-api/")

logging.info(f"Using BASE_XML_URL: {BASE_XML_URL}")  # Debugging purpose

BASE_XML_URL += "{id}.xml"

class Company(BaseModel):
    id: int
    name: str
    description: str

class ErrorResponse(BaseModel):
    error: str
    error_description: str

@app.get("/companies/{id}", response_model=Company, responses={404: {"model": ErrorResponse}})
def get_company(id: int):
    xml_url = BASE_XML_URL.format(id=id)
    logging.info(f"Fetching XML from: {xml_url}")

    response = requests.get(xml_url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch XML")

    # Debugging: Print raw XML response
    logging.info("Raw XML Response:")
    logging.info(response.text)

    try:
        xml_data = xmltodict.parse(response.text)
        print("Parsed XML Data:", xml_data)  # Print parsed data

        company = xml_data.get("Data")
        if not company:
            raise HTTPException(status_code=404, detail="Company not found in XML")

        return Company(
            id=int(company["id"]),
            name=company["name"],
            description=company["description"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing XML: {str(e)}")


# Run the server with: uvicorn main:app --reload
