from fastapi import APIRouter, Request, HTTPException, File, UploadFile
from fastapi.concurrency import run_in_threadpool
import aiofiles, os, tempfile

from app.models.api_models import ValidationResponse
from app.services.xml_validator import XMLValidatorService
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
XSD_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "..", "schemas", "standard.xsd")
if not os.path.exists(XSD_PATH):
    XSD_PATH = "/app/schemas/standard.xsd"
validator_service = XMLValidatorService(XSD_PATH)
router = APIRouter()

@router.post("/validate", response_model=ValidationResponse)
async def validate_xml(
    request: Request,
    file: UploadFile = File(...)
    ):
    """
    Receives an XML file via multipart/form-data, saves it to a 
    temporary location, and validates it against the XSD.
    """
    file_descriptor, temp_path = tempfile.mkstemp(suffix=".xml")
    os.close(file_descriptor)

    try: 
        async with aiofiles.open(temp_path, "wb") as out_file:
            while chunk := await file.read(1024 * 1024):
                await out_file.write(chunk)

        errors_list = await run_in_threadpool(validator_service.validate_file, temp_path)
    
        current_status = "success" if len(errors_list) == 0 else "failed"

        return ValidationResponse(
            status=current_status,
            total_errors=len(errors_list),
            errors=errors_list
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)