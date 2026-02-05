# Configure DSW Integration Question

## Quick Start
1. Import [Common DSW Knowledge Model
](https://registry.ds-wizard.org/knowledge-models/dsw:root:latest) to DSW.

2. Add new integration and fill the information, you could refer the following template:

```yaml
## Configuration
Type: API
Name: DepositarApi
Request: GET http://host.docker.internal:5002/get_project_list={{q}}
Advanced Request Configuration: 
    Accept: application/json
    ## You need to configure Depositar-Api-Key to secrets, which can be
    ## obtained [here](https://data.depositar.io/user/{ID}/api-tokens).
    Depositar-Api-Key: {{ secrets.depositarApiKey }}
Response List Field: result.results
```

```jinja
{# item_template.j2 #}
[{{ item.title }}](https://data.depositar.io/dataset/{{ item.name }})
( 產製者: {{ item.author }} )
![](https://img.shields.io/badge/type-{{ item.state }}-blue)
```