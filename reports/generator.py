from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import win32com.client as win32
import os
from datetime import datetime
from engine.config import REPORT_PASSWORD, TEMPLATE_PATH

class ReportGenerator:
    def __init__(self, filename, dut_info, test_results, operator_name, logs=None, images=None):
        """
        filename: target output path (usually .pdf or .docx)
        dut_info: dict with DUT parameters
        test_results: list of dicts {'name': str, 'status': str, 'details': str}
        operator_name: str
        logs: Full execution logs (string)
        images: list of dicts {'name': str, 'path': str}
        """
        self.filename = filename
        self.dut_info = dut_info
        self.test_results = test_results
        self.operator_name = operator_name
        self.logs = logs
        self.images = images or []
        
    def generate_pdf(self):
        """
        Generates DOCX via template and converts to PDF using a single Word session.
        """
        # 1. Generate the rendered DOCX first (without Word yet)
        docx_path = self._render_docx()
        if not docx_path:
            raise Exception("DOCX rendering failed.")
            
        docx_abs_path = os.path.abspath(docx_path)
        pdf_abs_path = os.path.abspath(self.filename)
        if not pdf_abs_path.lower().endswith(".pdf"):
            pdf_abs_path += ".pdf"
            
        print(f"Opening Word for protection and PDF conversion...")
        
        word = None
        try:
            os.makedirs(os.path.dirname(pdf_abs_path), exist_ok=True)
            word = win32.Dispatch("Word.Application")
            word.Visible = False
            
            # Open the raw rendered file
            doc_word = word.Documents.Open(docx_abs_path)
            
            # 2. Apply "Password to Open" (Encryption)
            # Setting the .Password property is the most reliable way 
            # for "Password to Open" in Word automation.
            print(f"Applying Password to Open: {REPORT_PASSWORD}")
            doc_word.Password = REPORT_PASSWORD
            
            # 3. Save protected DOCX
            print(f"Saving password-protected DOCX: {docx_abs_path}")
            doc_word.SaveAs2(docx_abs_path)
            
            # 4. Save PDF
            print(f"Generating PDF: {pdf_abs_path}")
            doc_word.SaveAs(pdf_abs_path, FileFormat=17) # 17 = PDF
            
            doc_word.Close()
            print("Successfully generated both encrypted DOCX and PDF.")
            return pdf_abs_path
        except Exception as e:
            print(f"Word operations failed: {e}")
            raise Exception(f"Report Generation Failed: {str(e)}")
        finally:
            if word:
                try:
                    word.Quit()
                except:
                    pass

    def generate_word(self):
        """
        Generates DOCX report, adds password to open, and returns the path.
        """
        docx_path = self._render_docx()
        if not docx_path:
            return None
            
        docx_abs_path = os.path.abspath(docx_path)
        word = None
        try:
            print(f"Applying password to open to {docx_abs_path}...")
            word = win32.Dispatch("Word.Application")
            word.Visible = False
            wdoc = word.Documents.Open(docx_abs_path)
            # Correct property for "Password to Open"
            wdoc.Password = REPORT_PASSWORD
            wdoc.SaveAs2(docx_abs_path)
            wdoc.Close()
            print("Password to open applied successfully.")
            return docx_path
        except Exception as e:
            print(f"Failed to apply password: {e}")
            return docx_path
        finally:
            if word:
                try:
                    word.Quit()
                except:
                    pass

    def _render_docx(self):
        """
        Internal helper to render the template into a DOCX file using docxtpl.
        """
        if not os.path.exists(TEMPLATE_PATH):
            err_msg = f"CRITICAL: Template '{TEMPLATE_PATH}' not found."
            print(err_msg)
            raise Exception(err_msg)
            
        try:
            doc = DocxTemplate(TEMPLATE_PATH)
            
            # Prepare context
            tests_summary = []
            items_detail = []
            
            # Use raw execution logs if provided, otherwise fallback to per-test details
            if self.logs:
                all_logs = self.logs
            else:
                all_logs = "\n".join([f"{res.get('name', 'Test')}: {res.get('details', '')}" for res in self.test_results])

            for i, res in enumerate(self.test_results, 1):
                name = res.get('name', 'Test')
                status = res.get('status', 'FAIL')
                desc = res.get("description", "Verification of " + name)
                
                # We provide both direct keys AND a nested 't' object 
                # to handle both {{ item.name }} and {{ t.name }} depending on loop style
                item_data = {
                    "sNo": i,
                    "name": name,
                    "result": status,
                    "Test_description": desc,
                    "input_voltage": self.dut_info.get("Input Nominal V", "70-125 V"),
                    "output_load": "100%",
                    "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                }
                # Add 't' sub-dict for templates using {{ t.sNo }} inside {% for t in items %}
                item_data["t"] = item_data.copy()
                
                tests_summary.append(item_data)
                items_detail.append(item_data)

            context = {
                "model_name": self.dut_info.get("Project Name", "PowerSafe-X"),
                "dut_name": self.dut_info.get("Converter Type", "DC/DC Converter"),
                "part_number": self.dut_info.get("Part Number", "TPS1030004A"),
                "dut_rev": self.dut_info.get("Build Version", "V1.0"),
                "dut_checksum": self.dut_info.get("FW Checksum", "0x0000"),
                "test_date": datetime.now().strftime("%d-%m-%Y"),
                "test_person": self.operator_name,
                "Log_with_timestamp": all_logs,
                "tests": tests_summary,
                "items": items_detail,
                # Compatibility for single-item templates
                "sNo": tests_summary[0]["sNo"] if tests_summary else "",
                "name": tests_summary[0]["name"] if tests_summary else "",
                "result": tests_summary[0]["result"] if tests_summary else "",
                "Test_description": items_detail[0]["Test_description"] if items_detail else ""
            }
            # Special case: if template uses {{ t.name }} globally, let's provide a 't' if possible
            if tests_summary:
                context["t"] = tests_summary[0]
            
            # Add images to context
            # We assume the template might have placeholders like {{ image_1 }}, {{ image_2 }}
            # or we iterate over images {% for img in images %} {{ img.file }} {{ img.caption }} {% endfor %}
            img_list = []
            for i, img_data in enumerate(self.images, 1):
                path = img_data.get('path', '')
                if os.path.exists(path):
                    # Create InlineImage
                    inline_img = InlineImage(doc, path, width=Mm(150))
                    
                    # Add to context as both indexed key and list item
                    context[f"image_{i}"] = inline_img
                    context[f"image_{i}_caption"] = img_data.get('name', f'Screenshot {i}')
                    
                    img_list.append({
                        "file": inline_img,
                        "caption": img_data.get('name', f'Screenshot {i}')
                    })
            
            context["images"] = img_list
            
            doc.render(context)
            
            docx_path = self.filename
            if docx_path.lower().endswith(".pdf"):
                docx_path = docx_path[:-4] + ".docx"
            
            doc.save(docx_path)
            print(f"Rendered DOCX: {docx_path}")
            return docx_path
            
        except Exception as e:
            print(f"Template rendering failed: {e}")
            return None
