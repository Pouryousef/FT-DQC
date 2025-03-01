import numpy as np
import random
import time
from joblib import Parallel, delayed
from surface_code_utils import *

num_cores = 28
dist_list = [4,6,8,10,12]
bandwidth = 8
gen_coh_ratio_list = np.logspace(-3,-1,8)
Niter = 1000
Nrep = 28*4

p_err = {
    "bulk_stab" : 0.01,
    "bdy_qubit" : 0.1,
    "bdy_stab" : 0.1
}
start_t = time.time()
for i_d, d in enumerate(dist_list):
    dy = d
    dx = 2 * d
    code_details = surface_code_plaquette(dx,dy)
    # logical_err_rate = perf_sim(d, bandwidth, code_details, gen_coh_ratio_list, p_err, Niter= Niter)

    def runner(i_rep):
        tic = time.time()
        logical_err_rate = perf_sim(d, bandwidth, code_details, gen_coh_ratio_list, p_err, Niter= Niter)
        out_dir = "results/joint_meas/"
        fname = f"d_{d}_plaq_bw_{bandwidth}_r_{i_rep}.npz"
        toc = time.time()
        print(f"{fname}, elapsed time {toc-tic:.2f} sec")
        np.savez(out_dir + fname, gen_coh_ratio_list, logical_err_rate)
    # runner(1)
    results = Parallel(n_jobs=num_cores)(delayed(runner)(i_rep) for i_rep in range(Nrep))

print(f"Job finished in {time.time()-start_t} seconds ")
