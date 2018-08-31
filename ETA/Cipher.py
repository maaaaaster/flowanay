ciphers = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '000A', '000C', '000D', '000F', '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018', '0019', '001A', '001B', '002F', '0030', '0031', '0032', '0033', '0034', '0035', '0036', '0037', '0038', '0039', '003A', '003B', '003C', '003D', '003E', '003F', '0040', '0041', '0042', '0043', '0044', '0045', '0046', '0060', '0061', '0062', '0063', '0064', '0065', '0066', '0067', '0068', '0069', '006A', '006B', '006C', '006D', '0084', '0085', '0086', '0087', '0088', '0089', '008A', '008B', '008C', '008D', '008E', '008F', '0090', '0091', '0092', '0093', '0094', '0095', '0096', '0097', '0098', '0099', '009A', '009B', '009C', '009D', '009E', '009F', '00A0', '00A1', '00A2', '00A3', '00A4', '00A5', '00A6', '00A7', '00AE', '00AF', '00B2', '00B3', '00B6', '00B7', '00BA', '00BD', '00BE', '00C0', '00C3', '00C4', '00FF', '0A0A', '1301', '1302', '1303', '1A1A', '2A2A', '3A3A', '4A4A', '5600', '5A5A', '6A6A', '7A7A', '8A8A', '9A9A', 'AAAA', 'BABA', 'C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C00A', 'C00B', 'C00C', 'C00D', 'C00E', 'C00F', 'C010', 'C011', 'C012', 'C013', 'C014', 'C015', 'C016', 'C017', 'C018', 'C019', 'C01A', 'C01B', 'C01C', 'C01D', 'C01E', 'C01F', 'C020', 'C021', 'C022', 'C023', 'C024', 'C025', 'C026', 'C027', 'C028', 'C029', 'C02A', 'C02B', 'C02C', 'C02D', 'C02E', 'C02F', 'C030', 'C031', 'C032', 'C033', 'C034', 'C035', 'C036', 'C037', 'C038', 'C072', 'C073', 'C076', 'C077', 'C07A', 'C07B', 'C07C', 'C07D', 'C086', 'C087', 'C08A', 'C08B', 'C09C', 'C09D', 'C09E', 'C09F', 'C0A0', 'C0A1', 'C0A2', 'C0A3', 'C0AC', 'C0AD', 'C0AE', 'C0AF', 'CACA', 'CC13', 'CC14', 'CC15', 'CCA8', 'CCA9', 'CCAA', 'DADA', 'E003', 'E013', 'EAEA', 'FAFA', 'FEFF']

def cipher2features(cipher):
    result = dict((x, 0) for x in ciphers)
    for i in range(0, len(cipher), 4):
        key = cipher[i:i + 4]
        if key in result:
            result[key] = 1
    return result