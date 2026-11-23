# DroneRoute

**Simulador de otimização de entregas por drones utilizando Algoritmo Genético (AG) e Otimização por Colônia de Formigas (ACO).**

O DroneRoute simula a distribuição de entregas e a otimização de rotas de uma frota de drones. O sistema combina duas meta-heurísticas: o Algoritmo Genético, responsável pela distribuição dos clientes entre os drones, e a Otimização por Colônia de Formigas, utilizada na construção das rotas de cada drone.

A simulação considera a capacidade de carga, o consumo energético durante os deslocamentos e a autonomia da bateria, buscando encontrar soluções com menor consumo total de energia.

## Como funciona

O sistema utiliza uma abordagem híbrida, dividida em três etapas principais.

**1. Algoritmo Genético (AG)**

O AG determina quais clientes serão atendidos por cada drone. Cada indivíduo da população representa uma possível distribuição dos clientes entre os drones. Cada posição corresponde a um cliente, e o valor indica qual drone será responsável por sua entrega.

A evolução da população utiliza:

- Geração da população inicial.
- Avaliação de fitness e validação da capacidade de carga.
- Seleção dos indivíduos.
- Cruzamento entre soluções.
- Mutação.
- Elitismo e formação de novas gerações.

**2. Otimização por Colônia de Formigas (ACO)**

Após a distribuição dos clientes, o ACO constrói e otimiza a sequência de visitas de cada drone.

O algoritmo utiliza:

- Matriz de feromônios para representar a intensidade das conexões.
- Distâncias entre os pontos para calcular a atratividade dos destinos.
- Escolha probabilística do próximo cliente.
- Evaporação dos feromônios.
- Depósito de feromônios nas conexões percorridas.

Rotas com menor consumo energético contribuem com depósitos maiores de feromônio, favorecendo essas conexões nas iterações seguintes.

**3. Integração dos algoritmos**

O AG gera diferentes distribuições de clientes, enquanto o ACO constrói e avalia as rotas correspondentes a cada drone.

O consumo energético das rotas é utilizado para avaliar a qualidade de cada distribuição. Soluções que excedem a capacidade de carga ou a autonomia disponível são consideradas inviáveis.

Dessa forma, os dois algoritmos trabalham em conjunto para buscar uma distribuição de clientes e um conjunto de rotas com menor consumo energético.

## Modelo energético

O consumo de energia é calculado considerando a distância percorrida e o peso transportado pelo drone.

A equação utilizada é:

`E = d × (Cbase + m × Ccarga)`

Onde:

- `E`: energia consumida em Wh.
- `d`: distância percorrida em km.
- `Cbase`: consumo energético base por quilômetro.
- `m`: peso da carga transportada em kg.
- `Ccarga`: fator adicional de consumo por quilômetro e quilograma.

Os valores padrão utilizados no modelo são:

| Parâmetro | Valor |
|---|---:|
| Consumo base | 40 Wh/km |
| Fator de carga | 10 Wh/km/kg |
| Capacidade máxima | 10 kg |
| Capacidade da bateria | 3.500 Wh |

A carga transportada diminui conforme as entregas são realizadas, influenciando o consumo energético dos trechos seguintes.

As distâncias são calculadas em um plano cartesiano, utilizando coordenadas expressas em quilômetros e matrizes de distâncias euclidianas.

Os coeficientes são parâmetros simplificados para experimentação computacional, não representando medições de uma aeronave real.

## Tecnologias utilizadas

- **Python:** implementação da simulação e dos algoritmos.
- **NumPy:** operações matriciais, indexação, cálculos vetorizados e atualização de feromônios.
- **Matplotlib:** visualização das rotas e da evolução dos resultados.
- **unittest:** execução dos testes automatizados.
- **Git e GitHub:** controle de versão e armazenamento do projeto.

O NumPy é utilizado principalmente no processamento das matrizes de distâncias e feromônios. Algumas etapas continuam sequenciais por dependerem do estado atual da rota, como a construção da sequência de visitas e a atualização da carga após cada entrega. O cálculo da atratividade dos destinos, por exemplo, utiliza operações vetorizadas.

## Estrutura do projeto

```text
DroneRoute/
│
├── src/
│   └── droneroute/
│       ├── algorithms/
│       │   ├── ant_colony/
│       │   │   ├── aco_01_feromonios.py
│       │   │   ├── aco_02_escolha.py
│       │   │   ├── aco_03_rota.py
│       │   │   ├── aco_04_atualizacao.py
│       │   │   └── aco_05_otimizacao.py
│       │   │
│       │   └── genetic_algorithm/
│       │       ├── ag_01_population.py
│       │       ├── ag_02_fitness.py
│       │       ├── ag_03_selection.py
│       │       ├── ag_04_crossover.py
│       │       ├── ag_05_mutation.py
│       │       ├── ag_06_evolution.py
│       │       ├── ag_07_avaliacao.py
│       │       └── ag_08_execucao.py
│       │
│       ├── models/
│       │   ├── client.py
│       │   ├── distribution_center.py
│       │   └── drone.py
│       │
│       ├── simulation/
│       │   └── geometry.py
│       │
│       ├── visualization/
│       │   └── graficos.py
│       │
│       └── main.py
│
├── tests/
│   ├── test_genetic_algorithm.py
│   ├── test_geometry.py
│   ├── test_hybrid.py
│   └── test_models.py
│
├── .gitignore
├── pyproject.toml
└── README.md
```

### Organização dos módulos

| Diretório | Responsabilidade |
|---|---|
| `models` | Representação de drones, clientes e centro de distribuição. |
| `algorithms/genetic_algorithm` | Implementação e execução do Algoritmo Genético. |
| `algorithms/ant_colony` | Construção e otimização das rotas pelo ACO. |
| `simulation` | Cálculos geométricos e matrizes de distâncias. |
| `visualization` | Geração dos gráficos da simulação. |
| `tests` | Testes automatizados dos modelos e algoritmos. |

## Instalação e execução

**Requisitos**

- Python 3.11 ou superior.
- Git.

**1. Clone o repositório**

```bash
git clone https://github.com/Cksb7/droneroute.git
cd droneroute
```

**2. Crie e ative o ambiente virtual**

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Instale o projeto e suas dependências**

```bash
python -m pip install -e .
```

O arquivo `pyproject.toml` gerencia as dependências necessárias, incluindo NumPy e Matplotlib.

**4. Execute a simulação**

```bash
python -m droneroute.main
```

A execução apresenta a distribuição encontrada, o consumo energético, as rotas dos drones e o histórico de evolução, além de abrir a visualização gráfica dos resultados.

## Testes automatizados

O projeto utiliza `unittest` para verificar o funcionamento dos modelos, dos operadores genéticos, dos cálculos geométricos e da integração entre os algoritmos.

Para executar todos os testes:

```bash
python -m unittest discover -s tests -v
```

Atualmente, os 20 testes automatizados estão passando.

## Configuração da simulação

Os principais parâmetros podem ser ajustados no arquivo `src/droneroute/main.py`.

Na configuração utilizada atualmente:

| Parâmetro | Valor |
|---|---:|
| Clientes | 20 |
| Drones | 5 |
| Tamanho da população | 30 |
| Gerações | 40 |
| Taxa de mutação | 0.1 |
| Formigas por execução do ACO | 10 |
| Iterações do ACO | 20 |

Os resultados podem variar entre execuções, pois os algoritmos utilizam operações aleatórias.

Para reproduzir um experimento, é possível definir um valor inteiro para `SEED` no arquivo `main.py`. Mantidas as mesmas condições e versões das dependências, isso permite repetir a sequência aleatória.

## Próximas etapas

A estrutura atual permite ampliar o modelo e experimentar novas estratégias de otimização.

Algumas possibilidades de desenvolvimento são:

- Implementação de estações de recarga e planejamento de paradas.
- Ampliação do modelo energético e dos parâmetros de voo.
- Utilização de coordenadas geográficas e cenários urbanos.
- Avaliação de diferentes parâmetros e estratégias para AG e ACO.
- Otimização do tempo de processamento para cenários maiores.

O modelo de drone já possui um método de recarga de bateria (`recarregar_bateria()`), mantido para uma possível integração futura com as estações de recarga. Essa funcionalidade ainda não está integrada ao fluxo atual da simulação.

## Observação

O DroneRoute é um simulador computacional. Os modelos energéticos e as soluções encontradas são simplificações matemáticas e não representam validação ou autorização operacional para voos reais.
