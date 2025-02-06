import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

class PDFExtractor:
    """
    A class to extract text from PDFs using Tesseract OCR.
    """

    def __init__(self, tesseract_path=None):
        """
        Initialize the extractor.
        :param tesseract_path: Path to the Tesseract executable (if not in PATH).
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def extract_text_from_image(self, image):
        """
        Extract text from an image using Tesseract OCR.
        :param image: PIL Image object.
        :return: Extracted text as a string.
        """
        # Use Tesseract to extract text
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()

    def extract_text_from_pdf(self, pdf_path, dpi=300):
        """
        Extract text from a PDF file.
        :param pdf_path: Path to the PDF file.
        :param dpi: DPI for image conversion (higher DPI improves accuracy but slows down processing).
        :return: Dictionary with page numbers as keys and extracted text as values.
        """
        try:
            # Convert PDF to a list of images
            images = convert_from_path(pdf_path, dpi=dpi)

            extracted_text = {}
            for i, image in enumerate(images):
                # Extract text from each image
                text = self.extract_text_from_image(image)
                extracted_text[i + 1] = text  # Page numbers start from 1

            return extracted_text

        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Path to the PDF file
    pdf_path = "Financial-Examples-for-I20.pdf"

    # Initialize the PDFExtractor
    extractor = PDFExtractor("C:/Program Files/Tesseract-OCR/tesseract.exe")

    # Extract text from the PDF
    try:
        extracted_text = extractor.extract_text_from_pdf(pdf_path)
        for page_num, text in extracted_text.items():
            print(f"Page {page_num}:\n{text}\n{'-' * 40}")
    except Exception as e:
        print(f"Error: {str(e)}")