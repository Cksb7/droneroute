
# DroneRoute

### Hybrid Drone Delivery Optimization

O DroneRoute é um projeto de desenvolvimento de um simulador de otimização de entregas por drones, utilizando algoritmos de inteligência computacional para encontrar soluções eficientes de roteamento e distribuição de entregas.

## Objetivo

Desenvolver um sistema modular capaz de otimizar operações de entrega por drones, considerando restrições como:

- Capacidade máxima de carga.
- Autonomia energética.
- Consumo de energia conforme o peso transportado.
- Distribuição de clientes entre drones.
- Necessidade de estações de recarga.
- Retorno ao centro de distribuição.

## Algoritmos

O projeto utilizará duas meta-heurísticas principais:

**Algoritmo Genético (AG)**

Responsável pela distribuição dos clientes entre os drones, utilizando população, seleção, cruzamento e mutação.

**Otimização por Colônia de Formigas (ACO)**

Responsável pela construção e otimização das rotas, utilizando feromônios e informações heurísticas.

**Abordagem híbrida**

Integração entre AG e ACO para combinar a distribuição de entregas com a otimização das rotas.

## Tecnologias

- Python
- Git
- GitHub
- Visual Studio Code

## Desenvolvimento

O sistema será desenvolvido de forma modular, permitindo aumentar a quantidade de drones, clientes e estações de recarga sem depender de alterações estruturais nos algoritmos.

A primeira versão utilizará um cenário pequeno e controlado. Futuras versões poderão incorporar coordenadas geográficas e cenários urbanos de maior escala.

## Status

Em desenvolvimento — estruturação inicial do projeto.

## Observação

O DroneRoute é um simulador computacional. Seus resultados não representam autorização ou validação operacional para voos reais.
