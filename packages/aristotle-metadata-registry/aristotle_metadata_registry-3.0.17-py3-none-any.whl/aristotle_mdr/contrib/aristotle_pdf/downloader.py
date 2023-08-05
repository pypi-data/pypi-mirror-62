import os
from io import BytesIO

from django.conf import settings
from django.template.loader import select_template, get_template, render_to_string
from django.core.files.base import File

from aristotle_mdr.downloader import HTMLDownloader
from aristotle_mdr.utils import fetch_aristotle_settings

import logging
import weasyprint
from PyPDF2 import PdfFileMerger
from tempfile import NamedTemporaryFile
import pdfkit

PDF_STATIC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pdf_static')

logger = logging.getLogger(__name__)
logger.debug("Logging started for " + __name__)


class GenericPDFDownloader(HTMLDownloader):
    """
    Generic pdf downloader with wrapping support
    Subclassed below, cannot be used as a downloader itself
    """
    download_type = "pdf"
    file_extension = 'pdf'
    metadata_register = '__all__'
    label = "PDF"
    mime_type = 'application/pdf'
    icon_class = "fa-file-pdf-o"
    description = "Downloads for various content types in the PDF format"
    allow_wrapper_pages = True

    def wrap_file(self, generated_bytes: bytes) -> BytesIO:
        if self.has_wrap_pages:
            merger = PdfFileMerger()
            pages = self.get_wrap_pages()
            pages.insert(1, generated_bytes)
            for page_bytes in pages:
                if page_bytes is not None:
                    merger.append(BytesIO(page_bytes), import_bookmarks=False)
            final_file = BytesIO()
            merger.write(final_file)
            merger.close()  # Close all files given to the merger
            return final_file
        else:
            return BytesIO(generated_bytes)


class PythonPDFDownloader(GenericPDFDownloader):
    """Pure python weasyprint based pdf downloader"""

    def generate_outline_str(self, bookmarks, indent=0):
        outline_str = ""
        for i, (label, (page, _, _), children) in enumerate(bookmarks, 1):
            outline_str += ('<div>%s %d. %s ..... <span style="float:right"> %d </span> </div>' % (
                '&nbsp;' * indent * 2, i, label.lstrip('0123456789. '), page + 1))
            outline_str += self.generate_outline_str(children, indent + 1)
        return outline_str

    def generate_outline_tree(self, bookmarks, depth=1):
        return [
            {'label': label, "depth": depth, "page": page + 1, "children": self.generate_outline_tree(children, depth + 1)}
            for i, (label, (page, _, _), children) in enumerate(bookmarks, 1)
        ]

    def render_to_pdf(self, template_src, context_dict,
                      preamble_template='aristotle_mdr/downloads/pdf/title.html') -> bytes:
        """Render to pdf using weasyprint"""
        # If the request template doesnt exist, we will give a default one.
        template = select_template([
            template_src,
            'aristotle_mdr/downloads/html/managedContent.html'
        ])

        document = weasyprint.HTML(
            string=template.render(context_dict),
            base_url=PDF_STATIC_PATH
        ).render()

        if not context_dict.get('tableOfContents', False):
            return document.write_pdf()

        toc = get_template('aristotle_mdr/downloads/html/toc.html').render(
            {
                "toc_tree": self.generate_outline_tree(document.make_bookmark_tree())
            }
        )

        table_of_contents_document = weasyprint.HTML(
            string=toc,
            base_url=PDF_STATIC_PATH
        ).render()

        for i, table_of_contents_page in enumerate(table_of_contents_document.pages):
            document.pages.insert(i, table_of_contents_page)

        if preamble_template:
            title_pages = weasyprint.HTML(
                string=get_template(preamble_template).render(context_dict),
                base_url=PDF_STATIC_PATH
            ).render().pages
            for i, page in enumerate(title_pages):
                document.pages.insert(i, page)

        return document.write_pdf()

    def create_file(self):
        template = self.get_template()
        context = self.get_context()

        byte_string = self.render_to_pdf(template, context)
        final_file = self.wrap_file(byte_string)
        return File(final_file)


class PDFDownloader(GenericPDFDownloader):
    """Wkhtmltopdf based pdf downloader"""
    download_type = "pdf"

    default_wk_options = {
        '--margin-top': '10mm',
        '--margin-bottom': '5mm',
    }

    preamble_template = 'aristotle_mdr/downloads/pdf/title.html'
    # Footer used when cover page is on
    cover_footer_template = 'aristotle_mdr/downloads/html/cover_footer.html'
    # Standard footer
    footer_template = 'aristotle_mdr/downloads/html/footer.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set dynamic options
        self.wk_options = self.default_wk_options.copy()
        # Get path to footer templates
        self.cover_footer_path = os.path.abspath(
            os.path.join(settings.MDR_BASE_DIR, 'templates', self.cover_footer_template)
        )
        self.footer_path = os.path.abspath(
            os.path.join(settings.MDR_BASE_DIR, 'templates', self.footer_template)
        )

        # Set pdf page size
        aristotle_settings = fetch_aristotle_settings()
        if 'DOWNLOAD_OPTIONS' in aristotle_settings:
            self.wk_options['--page-size'] = aristotle_settings['DOWNLOAD_OPTIONS'].get('PDF_PAGE_SIZE', 'A4')

        # Create configuration object so we can set wkhtmltopdf binary location
        if settings.WKHTMLTOPDF_LOCATION is not None:
            self.wk_config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_LOCATION)
        else:
            self.wk_config = pdfkit.configuration()

    def create_file(self):
        template = self.get_template()
        context = self.get_context()

        # Main document string
        html_string = render_to_string(template, context=context)

        # Whether to create a title page & toc or not
        table_of_contents = context['tableOfContents']

        final_options = self.wk_options.copy()
        toc_options = {}
        title_temp_file = None
        cover = None

        # If we are making a title
        if table_of_contents:
            # Add toc option so toc is generated
            toc_options['--toc-header-text'] = 'Table Of Contents'

            # Render preamble string
            preamble_string = render_to_string(self.preamble_template, context=context)

            # Write preamble temp file
            title_temp_file = NamedTemporaryFile(suffix='.html')
            title_temp_file.write(preamble_string.encode('utf-8'))

            # Set cover
            cover = title_temp_file.name

            # Set options for fixing page numbers with 2 page cover
            final_options['--page-offset'] = -1
            final_options['--footer-html'] = self.cover_footer_path
        else:
            # If there is no cover / toc use standard footer
            # otherwise page numbers will be incorrect
            final_options['--footer-html'] = self.footer_path

        # Convert to pdf
        pdf: bytes = pdfkit.from_string(
            html_string,
            False,
            cover=cover,
            cover_first=True,
            configuration=self.wk_config,
            options=final_options,
            toc=toc_options
        )

        # Close the temp file if it exists
        if title_temp_file is not None:
            title_temp_file.close()

        final_file = self.wrap_file(pdf)
        return File(final_file)
