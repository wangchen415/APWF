from SALib.analyze import morris
# from wc_global import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import os

def _sort_Si(Si, key, sortby="mu_star"):
    return np.array([Si[key][x] for x in np.argsort(Si[sortby])])


def _sort_Si_by_index(Si, key, index):
    return np.array([Si[key][x] for x in index])


def horizontal_bar_plot(ax, Si, opts=None, sortby="mu_star", unit=""):
    """Updates a matplotlib axes instance with a horizontal bar plot
    of mu_star, with error bars representing mu_star_conf.
    """
    assert sortby in ["mu_star", "mu_star_conf", "sigma", "mu"]

    if opts is None:
        opts = {}

    # Sort all the plotted elements by mu_star (or optionally another
    # metric)
    names_sorted = _sort_Si(Si, "names", sortby)
    mu_star_sorted = _sort_Si(Si, "mu_star", sortby)
    mu_star_conf_sorted = _sort_Si(Si, "mu_star_conf", sortby)

    # Plot horizontal barchart
    y_pos = np.arange(len(mu_star_sorted))
    plot_names = names_sorted

    out = ax.barh(
        y_pos,
        mu_star_sorted,
        xerr=mu_star_conf_sorted,
        align="center",
        ecolor="black",
        **opts
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(plot_names)
    ax.set_xlabel(r"$\mu^\star$" + unit)

    ax.set_ylim(min(y_pos) - 1, max(y_pos) + 1)

    return out


def covariance_plot(ax, Si, opts=None, unit=""):
    """Plots mu* against sigma or the 95% confidence interval"""
    if opts is None:
        opts = {}

    if Si["sigma"] is not None:
        # sigma is not present if using morris groups
        y = Si["sigma"]
        out = ax.scatter(Si["mu_star"], y, c="k", marker="o", **opts)
        ax.set_ylabel(r"$\sigma$")

        ax.set_xlim(
            0,
        )
        ax.set_ylim(
            0,
        )

        x_axis_bounds = np.array(ax.get_xlim())

        (line1,) = ax.plot(x_axis_bounds, x_axis_bounds, "k-")
        (line2,) = ax.plot(x_axis_bounds, 0.5 * x_axis_bounds, "k--")
        (line3,) = ax.plot(x_axis_bounds, 0.1 * x_axis_bounds, "k-.")

        ax.legend(
            (line1, line2, line3),
            (
                r"$\sigma / \mu^{\star} = 1.0$",
                r"$\sigma / \mu^{\star} = 0.5$",
                r"$\sigma / \mu^{\star} = 0.1$",
            ),
            loc="best",
        )

    else:
        y = Si["mu_star_conf"]
        out = ax.scatter(Si["mu_star"], y, c="k", marker="o", **opts)
        ax.set_ylabel(r"$95\% CI$")

    ax.set_xlabel(r"$\mu^\star$ " + unit)
    ax.set_ylim(
        0 - (0.01 * np.array(ax.get_ylim()[1])),
    )

    return out


import matplotlib.pyplot as plt

def sample_histograms(fig, input_sample, problem, opts=None):
    """Plots a set of subplots of histograms of the input sample"""
    if opts is None:
        opts = {}

    num_vars = problem["num_vars"]
    names = problem["names"]

    framing = 100 + (num_vars * 10)

    out = []

    for variable in range(num_vars):
        ax = fig.add_subplot(framing + variable + 1)  # 修改这里，使子图从1开始编号
        out.append(
            ax.hist(
                input_sample[:, variable],
                bins='auto',  # 自动确定直方图的bin数量
                density=False,
                label=None,
                **opts
            )
        )

        ax.set_title("%s" % (names[variable]))
        ax.tick_params(
            axis="x",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            bottom="off",  # ticks along the bottom edge are off
            top="off",  # ticks along the top edge are off
            labelbottom="off",
        )  # labels along the bottom edge off)
        if variable > 0:
            ax.tick_params(
                axis="y",  # changes apply to the y-axis
                which="both",  # both major and minor ticks affected
                labelleft="off",
            )  # labels along the left edge off)

    return out

def Build_problem(parfile):
    par={}
    count=0
    with open(parfile) as fh:
        for ln in fh:
            if len(ln.strip())==0:
                continue
            if count<2:
                res=re.findall('\s*(\d+)\s*:.*',ln)
                if res is None:
                    print("error")
                else:
                    if count==0:
                        par["par_num"]=int(res[0])
                        # print(par)
                    else:
                        par["sim_num"]=int(res[0])
                        # print(par)
                    count+=1
            else:
                res=re.findall('\s*([0-9a-zA-Z_\{\}\.\(\),-]+)\s*([0-9\.\-]+)\s*([0-9\.\-]+)',ln)
                if res is None:
                    print("error")
                else:
                    # print(par)
                    par[res[0][0]]={"min":float(res[0][1]),"max":float(res[0][2])}
                    count+=1
            if count-2==par["par_num"]:
                break
    names=[]
    bounds=[]
    for i in list(par.keys())[2:]:
        names.append(re.findall(r'[a-z]+__([A-Za-z0-9()_\-{}]*).?',i)[0])
        bounds.append([par[i]['min'],par[i]['max']])
    problem = {
    'num_vars': len(list(par.keys())[2:]),
    'names':names,
    'bounds': bounds}
    return problem
def Morris_analysis(exog,endog,parfile,picpath,cp):
    endog=pd.read_csv(endog,index_col=0)
    exog=pd.read_csv(exog,index_col=0)
    # Generate samples
    problem=Build_problem(parfile)
    X = exog.values
    stds = np.std(X, axis=0)
    cols_to_keep = np.where(stds > 0)[0]
    X = X[:, cols_to_keep]
    # Mock function
    Y = endog['r_square'].values
    # Calculate morris
    print(problem)
    Si = morris.analyze(problem, X, Y, conf_level=0.95,
                        print_to_console=True)
    # Drawing
    # Create a figure with two subplots, with horizontal spacing controlled by the hspace parameter
    fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'wspace': 0.4})
    # Call horizontal_bar_plot to draw a horizontal bar chart
    horizontal_bar_plot(ax1, Si, {}, sortby='mu_star', unit=r"")
    # Call covariance_plot to plot sensitivity index relationship
    covariance_plot(ax2, Si, {}, unit=r"")
    # plt.tight_layout()
    # plt.gcf().canvas.setWindowTitle('Sensitivity Analysis')
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.savefig(os.path.join(picpath,'Sensitivity Analysis(%s).jpg'%(cp+1)))
    plt.show()
####
if __name__ == "__main__":
    cp=0
    swatcup_parfile_path=r'D:\wangchen\APWF\PSO\input\parfile'
    LHS_path=r'D:\wangchen\APWF\PSO\output_qingyang\sensitivity analysis\ET'
    picpath=r'D:\wangchen\APWF\PSO\output_qingyang\sensitivity analysis\ET'
    file_inpar0=os.path.join(swatcup_parfile_path,'parfile.txt')
    exogfile='PSO_exog_%d.csv'
    endogfile="PSO_endog_%d.csv"
    # for cp in range(loop): 
    #     if cp == 0:
    swatcup_parfile=os.path.join(swatcup_parfile_path,'parfile.txt')
        # else:
        #     swatcup_parfile=os.path.join(SUFI_path,pathfile%(cp))
    exog_file=os.path.join(LHS_path,exogfile%(cp+1))
    endog_file=os.path.join(LHS_path,endogfile%(cp+1))
    Morris_analysis(exog_file,endog_file,swatcup_parfile,picpath,cp)
