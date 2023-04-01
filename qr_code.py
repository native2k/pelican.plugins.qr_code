import base64
import logging
from io import BytesIO

import qrcode
from pelican import signals

logger = logging.getLogger(__name__)


def default_settings():
    return {
        "QR_IMAGE_FORMAT": "png",
        "QR_IMAGE_URL_DIR": True,
        "QR_IMAGE_SIZE": 10,
        "QR_IMAGE_BORDER": 4,
        "QR_IMAGE_FILL_COLOR": "black",
        "QR_IMAGE_BACK_COLOR": "white",
    }


def addQRCodePage(page_generator, content):
    logger.debug(
        f"addQRCodePage called with page_generator: {page_generator} content: {content}"
    )

    settings = default_settings()
    settings.update(page_generator.settings)

    # build url of the page
    url = f"{content.get_siteurl()}/{content.save_as}"
    if settings["QR_IMAGE_URL_DIR"]:
        url = "/".join(url.split("/")[:-1])

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=settings["QR_IMAGE_SIZE"],
        border=settings["QR_IMAGE_BORDER"],
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(
        fill_color=settings["QR_IMAGE_FILL_COLOR"],
        back_color=settings["QR_IMAGE_BACK_COLOR"],
    )

    buffer = BytesIO()
    img.save(buffer, format=settings["QR_IMAGE_FORMAT"])
    content.qrcode = "data:image/{};base64,{}".format(
        settings["QR_IMAGE_FORMAT"].lower(),
        base64.b64encode(buffer.getvalue()).decode("utf-8"),
    )
    logger.info(f"Added QRCode ({url}) to {content}")


def register():
    signals.page_generator_write_page.connect(addQRCodePage)
