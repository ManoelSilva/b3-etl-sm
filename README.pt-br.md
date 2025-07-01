# [English Version](README.md)

# Projeto ETL S3 → Glue com Step Functions

Este projeto implementa um pipeline ETL orquestrado por Step Functions na AWS, disparado por eventos de persistência em um bucket S3. A infraestrutura é provisionada via Terraform.

## Arquitetura

- **S3 Trigger**: Ao persistir um arquivo no bucket S3, um evento dispara uma Lambda.
- **Lambda**: Responsável por iniciar uma Step Function.
- **Step Function**: Orquestra 3 jobs sequenciais no AWS Glue.
- **Glue Jobs**: Cada job representa uma etapa do ETL.
- **Terraform**: Provisiona Lambda, Step Function, Glue Jobs e triggers.

## Estrutura de Diretórios

```
infra/           # Infraestrutura como código (Terraform)
lambda/          # Código da função Lambda
jobs/            # Scripts dos jobs Glue
```

## Como usar

1. Configure variáveis no Terraform conforme seu ambiente.
2. Faça deploy da infraestrutura com Terraform.
3. Faça upload de arquivos no bucket S3 para disparar o pipeline. 