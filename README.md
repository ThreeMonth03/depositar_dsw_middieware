# Depositar Dsw Middleware

## Quick Start
1. Clone this repository, and start the service by docker compse.

```yaml
services:
    depositar_api:
        build: ./depositar_api_service/
        image: depositar/depositar_api_service
        restart: unless-stopped
        ports:
            - 5002:5002
        extra_hosts:
            - host.docker.internal:host-gateway
```

2. Based on the usages of apis, read the following article and configure the corresponding settings. 
    - Configure integration question in knowledge model of [DSW](https://github.com/ds-wizard).
    See [template/dsw_integration_question/README.md](./template/dsw_integration_question/README.md).