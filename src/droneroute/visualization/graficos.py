
import math
import matplotlib.pyplot as plt


def formatar_numero(valor, casas=2):
    return (
        f"{valor:,.{casas}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def mostrar_graficos(
    centro,
    clientes,
    rotas,
    historico_energia,
    historico_melhor_fitness,
    historico_fitness_medio
):

    pontos = [centro] + clientes

    cores = [
        "#2878B5",  # D1 - Azul
        "#E47739",  # D2 - Laranja
        "#269B82",  # D3 - Verde
        "#9563B8",  # D4 - Roxo
        "#BF8B30"   # D5 - Dourado
    ]

    # 1. Montagem da janela.

    fig = plt.figure(
        figsize=(16, 9),
        facecolor="#F3F6FA",
        constrained_layout=True
    )

    grade = fig.add_gridspec(
        2, 2,
        width_ratios=[1.25, 1],
        height_ratios=[1.2, 0.8]
    )

    ax_mapa = fig.add_subplot(grade[:, 0])
    ax_evolucao = fig.add_subplot(grade[0, 1])
    ax_resumo = fig.add_subplot(grade[1, 1])

    fig.suptitle(
        "DRONEROUTE | OTIMIZACAO HIBRIDA AG + ACO",
        fontsize=18,
        fontweight="bold",
        color="#17365D"
    )

    # 2. MAPA DAS ROTAS.

    for indice_drone, rota in enumerate(rotas):

        if len(rota) < 2:
            continue

        cor = cores[indice_drone % len(cores)]

        xs = [pontos[i].x for i in rota]
        ys = [pontos[i].y for i in rota]

        ax_mapa.plot(
            xs,
            ys,
            color=cor,
            linewidth=2.3,
            alpha=0.85,
            label=f"Drone D{indice_drone + 1}",
            zorder=2,
            clip_on=True
        )

        # Setas indicando o sentido dos voos.

        for origem, destino in zip(rota, rota[1:]):

            p1 = pontos[origem]
            p2 = pontos[destino]

            anotacao = ax_mapa.annotate(
                "",
                xy=(p2.x, p2.y),
                xytext=(p1.x, p1.y),
                arrowprops=dict(
                    arrowstyle="->",
                    color=cor,
                    lw=1.5,
                    shrinkA=15,
                    shrinkB=15
                ),
                annotation_clip=False,
                zorder=3
            )

            # Mantem a seta dentro da area do mapa.

            if anotacao.arrow_patch is not None:

                anotacao.arrow_patch.set_clip_on(True)

                anotacao.arrow_patch.set_clip_path(
                    ax_mapa.patch
                )

    # Deposito.

    ax_mapa.scatter(
        centro.x,
        centro.y,
        color="#17365D",
        marker="s",
        s=190,
        edgecolors="white",
        linewidths=1.5,
        label="Deposito",
        zorder=5,
        clip_on=True
    )

    ax_mapa.annotate(
        "DEPOSITO",
        (centro.x, centro.y),
        xytext=(9, -19),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color="#17365D",
        annotation_clip=True,
        clip_on=True
    )

    # Clientes.

    for indice, cliente in enumerate(clientes):

        ax_mapa.scatter(
            cliente.x,
            cliente.y,
            color="#26A69A",
            edgecolors="white",
            linewidths=1.3,
            s=115,
            label="Clientes" if indice == 0 else None,
            zorder=5,
            clip_on=True
        )

        ax_mapa.annotate(
            cliente.client_id,
            (cliente.x, cliente.y),
            xytext=(5, 6),
            textcoords="offset points",
            fontsize=8,
            fontweight="bold",
            color="#263746",
            bbox=dict(
                boxstyle="round,pad=0.18",
                facecolor="white",
                edgecolor="none",
                alpha=0.8
            ),
            annotation_clip=True,
            clip_on=True
        )

    ax_mapa.set_title(
        "Distribuicao das rotas",
        fontsize=13,
        fontweight="bold",
        color="#17365D",
        pad=12
    )

    ax_mapa.set_xlabel("Coordenada X (km)")
    ax_mapa.set_ylabel("Coordenada Y (km)")

    ax_mapa.set_aspect("equal", adjustable="box")

    ax_mapa.grid(True, alpha=0.18)
    ax_mapa.margins(0.12)

    ax_mapa.legend(
        loc="best",
        fontsize=8,
        frameon=True,
        framealpha=0.95
    )

    # 3. EVOLUCAO DO ALGORITMO GENETICO.

    geracoes = list(
        range(1, len(historico_melhor_fitness) + 1)
    )

    ax_evolucao.plot(
        geracoes,
        historico_melhor_fitness,
        color="#2878B5",
        marker="o",
        markersize=6,
        linewidth=2.5,
        label="Melhor fitness acumulado",
        clip_on=True
    )

    ax_evolucao.plot(
        geracoes,
        historico_fitness_medio,
        color="#E47739",
        marker="s",
        markersize=5,
        linewidth=1.8,
        linestyle="--",
        label="Fitness medio",
        clip_on=True
    )

    # Identifica as geracoes em que houve melhoria.

    for i in range(1, len(historico_melhor_fitness)):

        if historico_melhor_fitness[i] > historico_melhor_fitness[i - 1]:

            ax_evolucao.scatter(
                geracoes[i],
                historico_melhor_fitness[i],
                color="#269B82",
                s=95,
                edgecolors="white",
                linewidths=1,
                zorder=5,
                clip_on=True
            )

    ax_evolucao.set_title(
        "Evolucao da populacao",
        fontsize=13,
        fontweight="bold",
        color="#17365D",
        pad=12
    )

    ax_evolucao.set_xlabel("Geracao")
    ax_evolucao.set_ylabel("Fitness")

    ax_evolucao.set_xticks(geracoes)
    ax_evolucao.set_ylim(bottom=0)

    ax_evolucao.ticklabel_format(
        axis="y",
        style="sci",
        scilimits=(0, 0)
    )

    ax_evolucao.grid(True, alpha=0.2)

    ax_evolucao.legend(
        loc="best",
        fontsize=8
    )

    # 4. INDICADORES DA SIMULACAO.

    ax_resumo.set_facecolor("#F3F6FA")

    ax_resumo.set_xlim(0, 1)
    ax_resumo.set_ylim(0, 1)

    ax_resumo.axis("off")

    energia_final = historico_energia[-1]

    energias_validas = [
        energia for energia in historico_energia
        if math.isfinite(energia)
    ]

    if energias_validas and energias_validas[0] > 0:

        energia_inicial = energias_validas[0]

        reducao = (
            (energia_inicial - energia_final)
            / energia_inicial
        ) * 100

    else:
        reducao = 0.0

    fitness_final = historico_melhor_fitness[-1]

    drones_ativos = sum(
        1 for rota in rotas if len(rota) > 2
    )

    ax_resumo.text(
        0.02,
        0.94,
        "RESUMO DA SIMULACAO",
        fontsize=12,
        fontweight="bold",
        color="#17365D",
        transform=ax_resumo.transAxes
    )

    indicadores = [
        (
            0.02, 0.53,
            "CONSUMO FINAL",
            f"{formatar_numero(energia_final)} Wh"
        ),
        (
            0.52, 0.53,
            "FITNESS FINAL",
            f"{fitness_final:.6e}"
        ),
        (
            0.02, 0.08,
            "REDUCAO ENERGETICA",
            f"{formatar_numero(reducao)}%"
        ),
        (
            0.52, 0.08,
            "DRONES UTILIZADOS",
            f"{drones_ativos}/{len(rotas)}"
        )
    ]

    for x, y, titulo, valor in indicadores:

        ax_resumo.text(
            x,
            y,
            f"{titulo}\n{valor}",
            transform=ax_resumo.transAxes,
            fontsize=11,
            fontweight="bold",
            color="#17365D",
            verticalalignment="center",
            bbox=dict(
                boxstyle="round,pad=0.75",
                facecolor="white",
                edgecolor="#D8E1EC",
                linewidth=1.1
            )
        )

    # 5. ACABAMENTO VISUAL.

    for ax in (ax_mapa, ax_evolucao):

        ax.set_facecolor("white")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.spines["left"].set_color("#D8E1EC")
        ax.spines["bottom"].set_color("#D8E1EC")

    # Abre a janela de visualizacao.

    plt.show()