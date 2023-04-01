# qr_code

Pelican Plugin to the url of the page as qr code.

## Parameters

`QR_IMAGE_FORMAT` which image format should be used (defaults to `png`)

`QR_IMAGE_URL_DIR` use directory not file as data for code (defaults to `True`)

`QR_IMAGE_SIZE` size of the generated image (defaults to `10`)

`QR_IMAGE_BORDER` size of the image border (defaults to `4`)

`QR_IMAGE_FILL_COLOR` fill color of the image (defaults to `black`)

`QR_IMAGE_BACK_COLOR` background color of the image (defaults to `white`)
## Usage

The plugins generate a qr code and adds it to `page.qrcode` which can be used in the template.

```
<img src="{{ page.qrcode }}" alt="QRCode with the decoded url of the site"/>
```
