# DroneRoute

**Simulador modular de otimização de entregas por drones.**

O DroneRoute é um projeto de simulação computacional que busca estudar e desenvolver estratégias de otimização para operações de entrega utilizando drones.

## Objetivo

Desenvolver um sistema modular capaz de representar operações de entrega, considerando:

- Capacidade máxima de carga.
- Autonomia energética.
- Consumo de energia conforme distância e peso transportado.
- Distribuição de clientes entre drones.
- Estações de recarga.
- Retorno ao centro de distribuição.

## Arquitetura

O projeto utiliza uma organização modular:

- `models`: representação dos elementos do sistema.
- `algorithms`: implementação dos algoritmos de otimização.
- `simulation`: regras e execução das simulações.
- `visualization`: representação gráfica dos resultados.
- `tests`: testes automatizados.

## Estratégia de otimização planejada

O projeto prevê a utilização de duas meta-heurísticas:

**Algoritmo Genético (AG)**

Responsável pela distribuição dos clientes entre os drones, utilizando população, seleção, cruzamento e mutação.

**Otimização por Colônia de Formigas (ACO)**

Responsável pela construção e otimização das sequências de visitas, utilizando feromônios e informações heurísticas.

**Abordagem híbrida**

Integração entre AG e ACO para combinar distribuição de entregas e otimização de rotas.

Os algoritmos ainda estão em desenvolvimento.

## Modelo energético inicial

A primeira versão utiliza um modelo simplificado de consumo:

`Consumo = distância × (consumo base + peso × fator de carga)`

Os coeficientes são parâmetros ilustrativos, destinados à experimentação computacional.

A distância é calculada em um plano cartesiano com coordenadas expressas em quilômetros.

## Tecnologias

- Python
- Git
- GitHub
- Visual Studio Code

## Executando

Ative o ambiente virtual e execute:

```bash
python -m droneroute.main
```

Para executar os testes:

```bash
python -m unittest discover -s tests -v
```

## Desenvolvimento

O sistema está sendo desenvolvido de maneira modular, permitindo ampliar a quantidade de drones, clientes e estações de recarga.

Futuras versões poderão incorporar cenários urbanos de maior escala e coordenadas geográficas.

## Observação

O DroneRoute é um simulador computacional. Seus resultados não representam autorização ou validação operacional para voos reais.