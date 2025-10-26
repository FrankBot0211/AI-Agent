from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import fitz
class PDFReaderInput(BaseModel):
    """Input schema for the PDF Reader tool."""
    folder_path: str = Field(..., description="The path to the PDF file to read.")


class PDFReaderTool(BaseTool):
    name: str = "PDF Folder Reader"
    description: str = "Reads and extracts text from all PDF files in a folder."
    args_schema: Type[BaseModel] = PDFReaderInput

    def _run(self, folder_path: str) -> str:
        if not os.path.exists(folder_path):
            return f"Error: Folder not found at path {folder_path}"
        if not os.path.isdir(folder_path):
            return f"Error: {folder_path} is not a folder"

        all_text = ""
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

        if not pdf_files:
            return "No PDF files found in the specified folder."

        for pdf_file in pdf_files:
            file_path = os.path.join(folder_path, pdf_file)
            try:
                doc = fitz.open(file_path)
                text = ""
                for page in doc:
                    text += page.get_text("text")
                doc.close()
                all_text += f"\n\n--- {pdf_file} ---\n{text.strip()}"
            except Exception as e:
                all_text += f"\n\nError reading {pdf_file}: {str(e)}"

        return all_text.strip() or "No readable text found in PDFs."