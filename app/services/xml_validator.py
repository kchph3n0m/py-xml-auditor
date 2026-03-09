import xmlschema
import logging

logger = logging.getLogger(__name__)

class XMLValidatorService:
    def __init__(self, xsd_file_path):
        self.xsd_path = xsd_file_path
        try:
            self.schema = xmlschema.XMLSchema(self.xsd_path)

        except FileNotFoundError:
            logger.error(f"The XSD file: {self.xsd_path} not found.")
            raise

        except xmlschema.XMLSchemaException as e:
            logger.error(f"Critical: The XSD file is invalid or malformed. {e}")
            raise

        except Exception as e:
            logger.error(f"Error: {e}")
            raise

    def validate_file(self, xml_file_path):
        """
        Action: Runs every time we hit the API endpoint.
        """
        validation_errors = []
        for error in self.schema.iter_errors(xml_file_path):
            line_num = error.sourceline
            element = error.elem.tag if error.elem is not None else "Unknown"
            path = error.path
            reason = error.reason

            error_dict = {
                "line": line_num,
                "element": element,
                "path": path,
                "message": reason
            }
            validation_errors.append(error_dict)
        return validation_errors
