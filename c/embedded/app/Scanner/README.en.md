## Scanner program description

### function

This program is used to scan the QR code or barcode of the MAC hardware address. That is, the format is `xx:xx:xx;xx:xx:xx`, and it is recorded in the specified file.

For QR codes or barcodes in other formats, you only need to simply modify the data logic processing part of the scanner.

### Principle

The data input of the scanner is of the same type as the keyboard input, and the corresponding data can be detected and read through the corresponding input device node under the system.

The data conversion of the scanner is the same as the key value conversion of the keyboard. After the data is obtained, the data type and data value can be filtered to filter out unnecessary information.

Scan node location: `/dev/input/event*`

