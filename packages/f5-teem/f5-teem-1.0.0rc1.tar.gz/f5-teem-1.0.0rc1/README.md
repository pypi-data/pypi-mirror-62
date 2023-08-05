# Introduction

Python library providing an interface for F5's TEEM infrastructure to provide usage analytics to F5.

Note: Similar to node-based f5-teem library (https://www.npmjs.com/package/@f5devcentral/f5-teem).

## Usage (Anonymous API)

```python
from f5teem import AnonymousDeviceClient

client_info = {
    'name': 'f5-sdk-python',
    'version': '1.0.0',
    'id': '<ID of the machine>'
}
telemetry_client = AnonymousDeviceClient(client_info, api_key='API KEY')
telemetry_client.report({ 'foo': 'bar' }, telemetry_type='Installation Usage', telemetry_type_version='1')
```

By default, f5-teem will send a report that includes

- The type of Operating System where telemetry is sent from (for example, 'Linux')

### Example Telemetry Record

```json
{
    "digitalAssetName": "f5-sdk-python",
    "digitalAssetVersion": "1.0.0",
    "digitalAssetId": "",
    "documentType": "Installation Usage",
    "documentVersion": "1",
    "observationStartTime": "",
    "observationEndTime": "",
    "epochTime": "",
    "telemetryId": "",
    "telemetryRecords": [
        {
            "foo": "bar",
            "clientProperties": {
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

## Future Improvements

- f5-teem-python should support Reg Key API when running on BIG-IP (similar to node based f5-teem library)
- f5-teem-python should honor the phone home setting when running on BIG-IP. `tmsh modify sys software update auto-phonehome disabled`
