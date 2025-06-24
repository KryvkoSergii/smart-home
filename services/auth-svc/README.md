Install dependencies
```bash
poetry install
``` 
Active environment
```bash
poetry shell
``` 

Generate models:
cd to `.\services\auth-svc`

```powershell
python -m datamodel_code_generator `
    --input "..\..\shared\user-spec.yaml" `
    --input-file-type openapi `
    --output ".\app\schemas\user_schemas.py" `
    --output-model-type pydantic.BaseModel `
    --target-python-version 3.13 `
    --use-standard-collections `
    --field-constraints
```

```powershell
python -m datamodel_code_generator `
    --input "..\..\shared\shared-spec.yaml" `
    --input-file-type openapi `
    --output ".\app\schemas\shared_schemas.py" `
    --output-model-type pydantic.BaseModel `
    --target-python-version 3.13 `
    --use-standard-collections `
    --field-constraints
```