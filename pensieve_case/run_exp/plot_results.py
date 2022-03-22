import os
import numpy as np
import matplotlib.pyplot as plt


RESULTS_FOLDER = "./results/"
PLOTS_FOLDER = "./plots/"
NUM_BINS = 100
BITS_IN_BYTE = 8.0
MILLISEC_IN_SEC = 1000.0
M_IN_B = 1000000.0
VIDEO_LEN = 64
VIDEO_BIT_RATE = [350, 600, 1000, 2000, 3000]
COLOR_MAP = plt.cm.jet  # nipy_spectral, Set1,Paired
SIM_DP = "sim_dp"
SCHEMES = [
    "BB",
    "RB",
    # "FIXED",
    # "FESTIVE",
    # "BOLA",
    "pensieve",
    "metis",
    "emperor",
    # "sim_rl",
    # SIM_DP,
]

if not os.path.exists(PLOTS_FOLDER):
    os.makedirs(PLOTS_FOLDER)


def main():
    time_all = {}
    bit_rate_all = {}
    buff_all = {}
    bw_all = {}
    raw_reward_all = {}

    files_with_errors = 0

    for scheme in SCHEMES:
        time_all[scheme] = {}
        raw_reward_all[scheme] = {}
        bit_rate_all[scheme] = {}
        buff_all[scheme] = {}
        bw_all[scheme] = {}

    log_files = os.listdir(RESULTS_FOLDER)
    for log_file in log_files:

        time_ms = []
        bit_rate = []
        buff = []
        bw = []
        reward = []

        # print(log_file)

        with open(RESULTS_FOLDER + log_file, "rb") as f:
            if SIM_DP in log_file:
                for line in f:
                    parse = line.split()
                    if len(parse) == 1:
                        reward = float(parse[0])
                    elif len(parse) >= 6:
                        time_ms.append(float(parse[3]))
                        bit_rate.append(VIDEO_BIT_RATE[int(parse[6])])
                        buff.append(float(parse[4]))
                        bw.append(float(parse[5]))

            else:
                for line in f:
                    parse = line.split()
                    if len(parse) <= 1:
                        break
                    time_ms.append(float(parse[0]))
                    bit_rate.append(int(parse[1]))
                    buff.append(float(parse[2]))
                    bw.append(
                        float(parse[4])
                        / float(parse[5])
                        * BITS_IN_BYTE
                        * MILLISEC_IN_SEC
                        / M_IN_B
                    )
                    reward.append(float(parse[6]))

        if SIM_DP in log_file:
            time_ms = time_ms[::-1]
            bit_rate = bit_rate[::-1]
            buff = buff[::-1]
            bw = bw[::-1]

        if not time_ms:
            files_with_errors += 1
            print("ERROR:", log_file)
            # if file is empty, just skip it
            continue

        time_ms = np.array(time_ms)
        time_ms -= time_ms[0]

        for scheme in SCHEMES:
            if scheme in log_file:
                time_all[scheme][log_file[len("log_" + str(scheme) + "_") :]] = time_ms
                bit_rate_all[scheme][
                    log_file[len("log_" + str(scheme) + "_") :]
                ] = bit_rate
                buff_all[scheme][log_file[len("log_" + str(scheme) + "_") :]] = buff
                bw_all[scheme][log_file[len("log_" + str(scheme) + "_") :]] = bw
                raw_reward_all[scheme][
                    log_file[len("log_" + str(scheme) + "_") :]
                ] = reward
                break

    print("ERRORS:", files_with_errors)
    # ---- ---- ---- ----
    # Reward records
    # ---- ---- ---- ----

    log_file_all = []
    reward_all = {}
    for scheme in SCHEMES:
        reward_all[scheme] = []

    for l in time_all[SCHEMES[0]]:
        schemes_check = True
        for scheme in SCHEMES:
            if l not in time_all[scheme] or len(time_all[scheme][l]) < VIDEO_LEN:
                schemes_check = False
                break

        if schemes_check:
            log_file_all.append(l)
            for scheme in SCHEMES:
                if scheme == SIM_DP:
                    reward_all[scheme].append(raw_reward_all[scheme][l])
                else:
                    reward_all[scheme].append(
                        np.sum(raw_reward_all[scheme][l][1:VIDEO_LEN])
                    )

    mean_rewards = {}
    for scheme in SCHEMES:
        mean_rewards[scheme] = np.mean(reward_all[scheme])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for scheme in SCHEMES:
        ax.plot(reward_all[scheme])

    SCHEMES_REW = []
    for scheme in SCHEMES:
        SCHEMES_REW.append("{}: {:.4f}".format(scheme, mean_rewards[scheme]))

    colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(ax.lines))]
    for i, j in enumerate(ax.lines):
        j.set_color(colors[i])

    ax.legend(SCHEMES_REW, loc=4)

    plt.ylabel("total reward")
    plt.xlabel("trace index")
    # plt.show()
    # plt.tight_layout()
    plt.savefig("{}/rewards_by_trace.pdf".format(PLOTS_FOLDER))

    # ---- ---- ---- ----
    # CDF
    # ---- ---- ---- ----

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for scheme in SCHEMES:
        values, base = np.histogram(reward_all[scheme], bins=NUM_BINS)
        cumulative = np.cumsum(values)
        ax.plot(base[:-1], cumulative)

    colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(ax.lines))]
    for i, j in enumerate(ax.lines):
        j.set_color(colors[i])

    ax.legend(SCHEMES_REW, loc=2)

    plt.ylabel("CDF")
    plt.xlabel("total reward")
    # plt.show()
    # plt.tight_layout()
    plt.savefig("{}/cdf.pdf".format(PLOTS_FOLDER))

    # ---- ---- ---- ----
    # check each trace
    # ---- ---- ---- ----

    for l in time_all[SCHEMES[0]]:
        schemes_check = True
        for scheme in SCHEMES:
            if l not in time_all[scheme] or len(time_all[scheme][l]) < VIDEO_LEN:
                schemes_check = False
                break

        print(
            l,
            scheme,
            schemes_check,
            len(time_all[scheme][l]) if l in time_all[scheme] else None,
        )
        if schemes_check:
            fig = plt.figure()

            ax = fig.add_subplot(311)
            for scheme in SCHEMES:
                ax.plot(
                    time_all[scheme][l][:VIDEO_LEN], bit_rate_all[scheme][l][:VIDEO_LEN]
                )
            colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(ax.lines))]
            for i, j in enumerate(ax.lines):
                j.set_color(colors[i])
            plt.yticks(np.arange(0, 5, 1))
            plt.title(l)
            plt.ylabel("bit rate \nselection (kbps)")

            ax = fig.add_subplot(312)
            for scheme in SCHEMES:
                ax.plot(
                    time_all[scheme][l][:VIDEO_LEN], buff_all[scheme][l][:VIDEO_LEN]
                )
            colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(ax.lines))]
            for i, j in enumerate(ax.lines):
                j.set_color(colors[i])
            plt.ylabel("buffer size (ms)")

            ax = fig.add_subplot(313)
            for scheme in SCHEMES:
                ax.plot(time_all[scheme][l][:VIDEO_LEN], bw_all[scheme][l][:VIDEO_LEN])
            colors = [COLOR_MAP(i) for i in np.linspace(0, 1, len(ax.lines))]
            for i, j in enumerate(ax.lines):
                j.set_color(colors[i])
            plt.ylabel("bandwidth (mbps)")
            plt.xlabel("time (ms)")

            SCHEMES_REW = []
            for scheme in SCHEMES:
                if scheme == SIM_DP:
                    SCHEMES_REW.append(
                        "{}: {:.4f}".format(scheme, raw_reward_all[scheme][l])
                    )
                else:
                    SCHEMES_REW.append(
                        "{}: {:.4f}".format(
                            scheme, np.sum(raw_reward_all[scheme][l][1:VIDEO_LEN])
                        )
                    )

            ax.legend(
                SCHEMES_REW,
                loc=9,
                bbox_to_anchor=(0.5, -0.5),
                ncol=int(np.ceil(len(SCHEMES) / 2.0)),
            )
            # plt.show()
            plt.tight_layout()
            plt.savefig("{}/bit_rate_{}.pdf".format(PLOTS_FOLDER, l))


if __name__ == "__main__":
    main()
