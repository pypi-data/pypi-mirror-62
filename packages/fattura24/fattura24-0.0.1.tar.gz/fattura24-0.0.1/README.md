# Python SDK for fattura24 api

### API Reference

https://www.fattura24.com/api-documentazione/

### Installation

`pip install fattura24`

### Usage

    import fattura24
    
    fe = fattura24.FEDocument(api_key=settings.FATTURA24_API_KEY)
    
    res = fe.send()
    
    if res.findtext('returnCode') == '0':
        doc_number = res.findtext('docNumber')
        doc_id = res.findtext('docId')