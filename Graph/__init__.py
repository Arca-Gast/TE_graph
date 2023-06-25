import matplotlib.pyplot as plt


def start(command, data):
    if command == '1':
        graph_Seebeck_Electrical_conductivity(data)
    elif command == '2':
        graph_ZT_from_compound(data)
    elif command == '3':
        graph_Parameters_from_temperature(data)


def graph_Seebeck_Electrical_conductivity(data):
    x = [value['Electrical_conductivity(S/m)'] for value in data]
    y = [value['Seebeck_coefficient(μV/K)'] for value in data]
    labels = [value['Formula'] for value in data]
    c = [value['ZT'] for value in data]

    fig, ax = plt.subplots()
    scatters = ax.scatter(x, y, c=c, cmap='magma')
    plt.colorbar(scatters, ax=ax)

    ax.set_xscale('log')

    ax.set_title("Seebeck coefficient - Electrical conductivity")
    ax.set_ylabel("Seebeck coefficient(μV/K)")
    ax.set_xlabel("Electrical conductivity(S/m)")
    fig.tight_layout()

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"))
    annot.set_visible(False)

    def update_annot(ind):

        pos = scatters.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "ZT:{}; Formula: {}".format(", ".join([str(c[n]) for n in ind["ind"]]),
               ", ".join([labels[n] for n in ind["ind"]]))
        annot.set_text(text)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = scatters.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', hover)
    plt.show()


def graph_ZT_from_compound(data):
    fig, ax = plt.subplots(figsize=[15, 4])
    x = [i for i in range(len(data))]

    plt.xticks(x, [value for value in data.keys()])
    i = 0
    scatters = []
    for value in data.values():
        y = [temp['ZT'] for temp in value]
        scatters.append(ax.scatter([i]*len(y), y, s=25))
        i += 1

    ax.set_xlabel("Compound")
    ax.set_ylabel("ZT")

    fig.tight_layout()

    annot = ax.annotate("", xy=(0, 0), xytext=(0, -20), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"))
    annot.set_visible(False)

    def update_annot(x, scatter, ind):
        i = 0
        for value in data.values():
            if i == x:
                hover_date = value
            i+=1

        annot.xy = [x, hover_date[ind["ind"][0]]["ZT"]]

        text = "ZT:{}; Formula: {}; Temperature: {}".format(", ".join([str(hover_date[n]["ZT"]) for n in ind["ind"]]),
                                                            ", ".join([hover_date[n]['Formula'] for n in ind["ind"]]),
                                                            ", ".join([str(hover_date[n]['Temperature(K)']) for n in ind["ind"]]))
        annot.set_text(text)


    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            i = 0
            check = True
            for scatter in scatters:
                cont, ind = scatter.contains(event)
                if cont:
                    check = False
                    update_annot(i, scatter, ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()

                if check:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()
                i += 1
            check = True

    fig.canvas.mpl_connect('motion_notify_event', hover)

    plt.show()


def graph_Parameters_from_temperature(data):

    fig, ax = plt.subplots(nrows=2, ncols=2)


    x = [value['Temperature(K)'] for value in data]
    y1 = [value['ZT'] for value in data]
    y2 = [value['Seebeck_coefficient(μV/K)'] for value in data]
    y3 = [value['Electrical_conductivity(S/m)'] for value in data]
    y4 = [value['Thermal_conductivity(W/mK)'] for value in data]

    ax[0][0].scatter(x, y1)
    ax[0][1].scatter(x, y2)
    ax[1][0].scatter(x, y3)
    ax[1][1].scatter(x, y4)

    ax[0][0].set_title( "{}".format(data[0]["Formula"]) )

    ax[0][0].set_ylabel("ZT")
    ax[0][1].set_ylabel("Seebeck coefficient(μV/K)")
    ax[1][0].set_ylabel("Electrical conductivity(S/m)")
    ax[1][0].set_xlabel("Temperature(K)")
    ax[1][1].set_ylabel("Thermal conductivity(W/mK)")
    ax[1][1].set_xlabel("Temperature(K)")

    fig.tight_layout()
    plt.show()
