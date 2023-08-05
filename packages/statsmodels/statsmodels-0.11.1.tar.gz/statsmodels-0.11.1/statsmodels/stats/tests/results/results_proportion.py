# -*- coding: utf-8 -*-
"""

Created on Fri Mar 01 14:48:59 2013

Author: Josef Perktold
"""

import collections
import numpy as np

from statsmodels.tools.testing import Holder

# numbers from R package `pwr` pwr.chisq.test
res_binom = collections.defaultdict(Holder)
res_binom_methods = ["agresti-coull", "asymptotic", "bayes",  "cloglog",
                     "exact", "logit", "probit", "profile", "lrt", "prop.test",
                     "wilson"]


# > bci = binom.confint(x = c(18), n = 20, tol = 1e-8)
# > mkarray2(bci$lower, "res_binom[(18, 20)].ci_low")
res_binom[(18, 20)].ci_low = np.array([
    0.6867561125596077, 0.768521618913513, 0.716146742695748,
    0.656030707261567, 0.6830172859809176, 0.676197991611287,
    0.7027685414174645, 0.722052946372325, 0.7220576251734515,
    0.668722403162941, 0.6989663547715128
    ])
# > mkarray2(bci$upper, "res_binom[(18, 20)].ci_upp")
res_binom[(18, 20)].ci_upp = np.array([
    0.984343760998137, 1.031478381086487, 0.97862751197755,
    0.974010174395775, 0.9876514728297052, 0.974866415649319,
    0.978858461808406, 0.982318186566456, 0.982639913376776,
    0.982487361226571, 0.972133518786232
    ])
# >
# > bci = binom.confint(x = c(4), n = 20, tol = 1e-8)
# > mkarray2(bci$lower, "res_binom[(4, 20)].ci_low")
res_binom[(4, 20)].ci_low = np.array([
    0.0749115102767071, 0.0246954918846837, 0.07152005247873425,
    0.0623757232566298, 0.05733399705003284, 0.0771334546771001,
    0.0710801045992076, 0.0668624655835687, 0.0668375191189685,
    0.0661062308910436, 0.0806576625797981
    ])
# > mkarray2(bci$upper, "res_binom[(4, 20)].ci_upp")
res_binom[(4, 20)].ci_upp = np.array([
    0.4217635845549845, 0.3753045081153163, 0.4082257625169254,
    0.393143902056907, 0.436614002996668, 0.427846901518118,
    0.4147088121599544, 0.405367872119342, 0.405364309586823,
    0.442686245059445, 0.4160174322518935
    ])
# >
# > bci = binom.confint(x = c(4), n = 200, tol = 1e-8)
# > mkarray2(bci$lower, "res_binom[(4, 200)].ci_low")
res_binom[(4, 200)].ci_low = np.array([
    0.005991954548218395, 0.000597346459104517, 0.00678759879519299,
    0.006650668467968445, 0.005475565879556443, 0.00752663882411158,
    0.00705442514086136, 0.00625387073493174, 0.00625223049303646,
    0.00642601313670221, 0.00780442641634947
    ])
# > mkarray2(bci$upper, "res_binom[(4, 200)].ci_upp")
res_binom[(4, 200)].ci_upp = np.array([
    0.0520995587739575, 0.0394026535408955, 0.0468465669668423,
    0.04722535678688564, 0.05041360908989634, 0.05206026227201098,
    0.04916362085874019, 0.04585048214247203, 0.0458490848884339,
    0.0537574613520185, 0.05028708690582643
    ])
# > bci = binom.confint(x = c(190), n = 200, tol = 1e-8)
# Warning message:
# In binom.bayes(x, n, conf.level = conf.level, ...) :
#  1 confidence interval failed to converge (marked by '*').
#  Try changing 'tol' to a different value.
# JP: I replace 0.02094150654714356 by np.nan in Bayes
# > mkarray2(bci$lower, "res_binom[(190, 200)].ci_low")
res_binom[(190, 200)].ci_low = np.array([
    0.909307307911624, 0.919794926420966, np.nan,
    0.909066091776046, 0.9099724622986486, 0.9095820742314172,
    0.9118101288857796, 0.913954651984184, 0.913956305842353,
    0.9073089225133698, 0.910421851861224
    ])
# > mkarray2(bci$upper, "res_binom[(190, 200)].ci_upp")
res_binom[(190, 200)].ci_upp = np.array([
    0.973731898348837, 0.980205073579034, 1, 0.972780587302479,
    0.975765834527891, 0.9728891271086528, 0.973671370402242,
    0.974623779100809, 0.974626983311416, 0.974392083257476,
    0.972617354399236
    ])

# > bci = binom.confint(x = c(1), n = 30, tol = 1e-8)
res_binom[(1, 30)].ci_low = np.array([
    -8.305484e-03, -3.090070e-02,  6.903016e-05, 2.494567e-03,
    8.435709e-04,  4.675346e-03,  3.475014e-03, 3.012987e-03,
    1.932430e-03,  1.742467e-03,  5.908590e-03])

res_binom[(1, 30)].ci_upp = np.array([
    0.18091798, 0.09756737, 0.12314380, 0.14513807,
    0.17216946, 0.20200244, 0.16637241, 0.13868254,
    0.13868375, 0.19053022, 0.16670391])

# > bci = binom.confint(x = c(29), n = 30, tol = 1e-8)
res_binom[(29, 30)].ci_low = np.array([
    0.8190820, 0.9024326, 0.8768562, 0.7860836,
    0.8278305, 0.7979976, 0.8336276, 0.8613175,
    0.8613162, 0.8094698, 0.8332961])
res_binom[(29, 30)].ci_upp = np.array([
    1.0083055, 1.0309007, 0.9999310, 0.9952363,
    0.9991564, 0.9953247, 0.9965250, 0.9969870,
    0.9980676, 0.9982575, 0.9940914])

# > bci = binom.confint(x = c(0), n = 30, tol = 1e-8)
# Note: this ci_low clips one negative value to 0
res_binom[(0, 30)].ci_low = np.zeros(11)
res_binom[(0, 30)].ci_upp = np.array([
    0.13471170, 0.00000000, 0.06151672, 0.11570331,
    0.11570331, 0.11570331, 0.11570331, 0.10402893,
    0.06201781, 0.14132048, 0.11351339])

# > bci = binom.confint(x = c(30), n = 30, tol = 1e-8)
res_binom[(30, 30)].ci_low = np.array([
    0.8652883, 1.0000000, 0.9384833, 0.8842967,
    0.8842967, 0.8842967, 0.8842967, 0.8959711,
    0.9379822, 0.8586795, 0.8864866])
# Note: this ci_upp clips one value > 1
res_binom[(30, 30)].ci_upp = np.ones(11)
