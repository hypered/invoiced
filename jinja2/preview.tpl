<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Display</title>
    <style>
        .container {
            display: flex;
            flex-wrap: wrap;
        }
        .left {
            flex: 1;
        }
        .left img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        .right {
            flex: 1;
            max-width: 24em;
        }
        .data {
            position: -webkit-sticky;
            position: sticky;
            top: 10px;
        }
        .qr-code {
            width: 200px;
            height: 200px;
        }
        .text-info {
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <img src="{{ image_url }}" alt="Invoice preview">
        </div>
        <div class="right">
            <div class="data">
                <img class="qr-code" src="{{ qr_code_url }}" alt="QR Code">
                <div class="text-info">
                    <p><strong>Amount:</strong> {{ amount }}</p>
                    <p><strong>IBAN:</strong> {{ iban }}</p>
                    <p><strong>Reference:</strong> {{ reference }}</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
