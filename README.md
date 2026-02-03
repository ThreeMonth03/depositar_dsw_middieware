# Depositar API Service

## Quick Start
Clone this repository, and start the service by docker compse.

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

Configure integration question in knowledge model editor of [DSW](https://github.com/ds-wizard). See [example](./template/depositar/).