# [English Version](README.md)

# Projeto ETL S3 → Glue com Step Functions

Este projeto implementa um pipeline ETL orquestrado por Step Functions na AWS, disparado por eventos de persistência em um bucket S3. A infraestrutura é provisionada via Terraform.

## Arquitetura

- **S3 Trigger**: Ao persistir um arquivo no bucket S3, um evento dispara uma Lambda.
- **Lambda**: Responsável por iniciar a execução da Step Function.
- **Step Function**: Orquestra 3 jobs sequenciais no AWS Glue (extract, transform, load).
- **Glue Jobs**:
  - **extract.py**: Cria a tabela Glue e registra partições a partir do bucket raw.
  - **transform.py**: Lê, limpa e transforma os dados, gera estatísticas móveis e grava no bucket refined.
  - **load.py**: Registra os dados transformados em uma nova tabela Glue e atualiza as partições.
- **Terraform**: Provisiona Lambda, Step Function, Glue Jobs, buckets S3 e triggers.
- **Notebook**: Notebook de visualização Athena para análise e dashboards dos dados.

## Estrutura de Diretórios

```
infra/           # Infraestrutura como código (Terraform)
lambda/          # Código da função Lambda (inicia Step Function)
jobs/            # Scripts dos jobs Glue (extract, transform, load)
notebook/        # Notebook de visualização Athena
```

## Como usar

1. Configure as variáveis no Terraform conforme seu ambiente (veja `infra/variables.tf`).
2. Faça deploy da infraestrutura com Terraform:
   ```sh
   cd infra
   terraform init
   terraform apply
   ```
3. Faça upload de arquivos no bucket S3 raw para disparar o pipeline.
4. A função Lambda (`lambda/start_step.py`, dependência: `boto3`) iniciará a execução da Step Function.
5. A Step Function executará os jobs Glue em sequência:
   - **extract.py**: Cria/atualiza a tabela Glue e partições para os dados brutos.
   - **transform.py**: Limpa e transforma os dados, calcula estatísticas móveis e grava no bucket refined.
   - **load.py**: Registra os dados refinados em uma nova tabela Glue e atualiza as partições.
6. (Opcional) Utilize o notebook Jupyter em `notebook/athena_visualization.ipynb` para analisar e visualizar os dados processados com Athena.

## Dependências da Lambda

- A função Lambda requer `boto3` (veja `lambda/requirements.txt`).

## Visualização com Notebook

- O notebook requer: `PyAthena`, `pandas`, `plotly`, `boto3`, `sqlalchemy`.
- Instale as dependências no seu ambiente Jupyter:
  ```python
  %pip install PyAthena pandas plotly boto3 sqlalchemy
  ```
- Ajuste as configurações de conexão no notebook conforme necessário (região AWS, S3 staging dir, nomes de banco/tabela).
- Execute o notebook para gerar dashboards e análises a partir dos dados processados.

## Observações

- Toda a infraestrutura é gerenciada via módulos Terraform em `infra/`.
- Os jobs Glue e o código da Lambda estão em `jobs/` e `lambda/` respectivamente.
- O pipeline é totalmente orientado a eventos: o upload de um arquivo no bucket S3 raw dispara automaticamente todo o processo ETL. 