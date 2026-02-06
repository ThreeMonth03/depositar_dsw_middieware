# Depositar Dsw Middleware

## Quick Start
1. Clone this repository, and start the service by docker compse.

```yaml
services:
  depositar_dsw_middieware:
    build: ./depositar_dsw_middieware
    image: depositar/depositar_dsw_middieware
    env_file: ./example.env #Need to configure DSW_ROOT_KEY to legally using DSW api
    restart: unless-stopped
    ports:
      - 5002:5002
    extra_hosts:
      - host.docker.internal:host-gateway
```

2. Based on the usages of apis, read the following article and configure the corresponding settings. 
    - Configure integration question in knowledge model of [DSW](https://github.com/ds-wizard).
    See [template/dsw_integration_question/README.md](./template/dsw_integration_question/README.md).
    - Submit questionnaire from dsw to depositar. See 
    [template/dsw_questionnaire_submission/README.md](./template/dsw_questionnaire_submission/README.md).