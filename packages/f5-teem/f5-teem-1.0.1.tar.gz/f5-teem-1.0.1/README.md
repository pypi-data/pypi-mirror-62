# Introduction

Python library providing an interface for F5's TEEM infrastructure to provide usage analytics to F5.

## Usage (Anonymous API)

```python
from f5teem import AnonymousDeviceClient

client_info = {
    'name': 'f5-example-product',
    'version': '1.0.0',
    'id': '<asset UUID>'
}
telemetry_client = AnonymousDeviceClient(client_info, api_key='<API KEY>')
telemetry_client.report(
    {
        'foo': 'bar'
    },
    telemetry_type='Installation Usage',
    telemetry_type_version='1'
)
```

By default, this library will include in the report telemetry client properties including:

- The type of Operating System where telemetry is sent from (for example, 'Linux')

### Example Telemetry Record

```json
{
    "digitalAssetName": "f5-example-product",
    "digitalAssetVersion": "1.0.0",
    "digitalAssetId": "<asset UUID>",
    "documentType": "Installation Usage",
    "documentVersion": "1",
    "observationStartTime": "",
    "observationEndTime": "",
    "epochTime": "",
    "telemetryId": "",
    "telemetryRecords": [
        {
            "foo": "bar",
            "telemetryClientProperties": {
                "os": "linux"
            }
        }
    ]
}
```

## Use TEEM staging environment

- Set environment variable
    ```bash
    export TEEM_API_ENVIRONMENT='staging'
    ```

## Notes

- This library is similar to the node-based f5-teem library (https://www.npmjs.com/package/@f5devcentral/f5-teem).

## Future Improvements

- f5-teem-python should support Reg Key API when running on BIG-IP (similar to node based f5-teem library)
- f5-teem-python should honor the phone home setting when running on BIG-IP. `tmsh modify sys software update auto-phonehome disabled`
