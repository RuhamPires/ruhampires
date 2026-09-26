# Computer vision · Technical review

**Independent engineering reference · Ruham Pires's portfolio**

[Profile](../README.md) · [Runnable evaluation lab](../examples/evaluation-lab/README.md) · [Português](#português)

## Start with the evidence

| Portfolio artifact | What it lets you examine | Evidence boundary |
| --- | --- | --- |
| [SnapSupply](projects/snapsupply.md) | Industrial use case, end-to-end contribution, previously reported deployment scope | Professional case study; no production dataset or telemetry is included |
| [LensPart](projects/lenspart.md) | Product direction, documented stack and deployment considerations | Proprietary implementation; public product overview |
| [Evaluation lab](../examples/evaluation-lab/README.md) | Executable metric definitions, input validation and tests | Synthetic binary decisions; no model inference |
| [Visual validation](visual-validation.md) | Design questions around image quality, matching and review | Reference design |
| [AI delivery](ai-delivery.md) | Acceptance criteria, integration and operational monitoring | Reference note |

## Questions I use to structure an evaluation

### 1. What decision does the system support?

Define the input, expected output, consumer and cost of an incorrect decision. Separate candidate retrieval, final identification and image-to-description validation: each needs a clear acceptance criterion. An attractive demonstration is a starting point for investigation, not a measurement protocol.

### 2. What does the evaluation set represent?

Record provenance and labeling rules. Review duplicates and related images before defining the split. Include difficult capture conditions: blur, illumination, angle, occlusion and visually similar components. Keep disagreement visible and document how labels are adjudicated.

### 3. What happens when the system is uncertain?

Define the review outcome explicitly. Report automated-decision quality alongside coverage, review rate and the denominator used for each metric. The included lab makes this distinction concrete: choosing to review difficult cases changes what an accuracy number represents.

### 4. How can someone reproduce the comparison?

Record the dataset version, configuration, model or retrieval settings, preprocessing and decision rules. Preserve individual outputs and failure categories. Describe compute and latency measurement conditions before comparing performance. A threshold selected on development data should be assessed on a separate evaluation set.

### 5. What changes after integration?

Check input contracts, error handling, application behavior and human review. Decide which quality, latency, cost and usage signals to monitor. Define an acceptance owner and a recovery path before treating a deployment as operationally accepted.

## Inspect the runnable artifact

From the repository root:

```bash
python3 examples/evaluation-lab/evaluate.py
python3 -m unittest discover -s examples/evaluation-lab -p 'test_*.py' -v
```

Read the [fixture and metric definitions](../examples/evaluation-lab/README.md) with the output. The invented observations illustrate evaluator behavior and cannot substantiate accuracy, throughput or business impact for a real system.

## Português

Esta referência organiza uma revisão técnica em cinco perguntas: qual decisão o sistema apoia, o que a base de avaliação representa, como a incerteza é tratada, como reproduzir a comparação e o que muda após a integração.

O portfólio diferencia estudos profissionais, apresentações de produtos, demos e código executável. O laboratório usa dados sintéticos e permite verificar definições de métricas e testes; ele não mede a precisão dos projetos profissionais.

[Voltar ao perfil](../README.pt-BR.md)
