# Document submission
## Quick start
1. Go to the page of dsw document submission settings, and the default url is `http://localhost:8080/wizard/settings/submission`.
2. Add new service, which configuration looks like:
```yaml
ID: depositar
Name: depositar
Supported Formats: 
    template: dsw:rda-madmp # you might import this document template at first.
                            # see https://registry.ds-wizard.org/document-templates/dsw:rda-madmp:1.27.1 .
    version: 1.27.1 # or other version
    format: RDF/XML
Request:
    Method: POST
    URL: http://host.docker.internal:5002/submit_questionnaire
    Headers:
        Content-Type: application/rdf+xml
        Depositar-Api-Key: $your_depositar_api_key # see https://data.depositar.io/user/{ID}/api-tokens
```