from pelican import signals
from io import BytesIO

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
# from qrcode.image.styles.colormasks import RadialGradiantColorMask

import base64

import logging

logger = logging.getLogger(__name__)

QR_IMAGE_FORMAT = 'png'
QR_IMAGE_SIZE = 10
QR_IMAGE_BORDER = 4

def addQRCodePage(page_generator, content):

    for page in page_generator.pages:

        # build url of the page
        url = f'{page.get_siteurl()}/{page.save_as}'

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=QR_IMAGE_SIZE,
            border=QR_IMAGE_BORDER,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())

        buffer = BytesIO()
        img.save(buffer, format=QR_IMAGE_FORMAT)
        page.qrcode = 'data:image/{};base64,{}'.format(
            QR_IMAGE_FORMAT.lower(),
            base64.b64encode(buffer.getvalue()).decode('utf-8')
        )
        logger.info(f'Added QRCode ({url}) to {page}')

def register():
    signals.page_generator_write_page.connect(addQRCodePage)
