# DO NOT EDIT
# Autogenerated from the notebook statespace_concentrated_scale.ipynb.
# Edit the notebook and then sync the output with this file.
#
# flake8: noqa
# DO NOT EDIT

#!/usr/bin/env python
# coding: utf-8

# ## State space models - concentrating the scale out of the likelihood
# function

import numpy as np
import pandas as pd
import statsmodels.api as sm

dta = sm.datasets.macrodata.load_pandas().data
dta.index = pd.date_range(start='1959Q1', end='2009Q4', freq='Q')

# ### Introduction
#
# (much of this is based on Harvey (1989); see especially section 3.4)
#
# State space models can generically be written as follows (here we focus
# on time-invariant state space models, but similar results apply also to
# time-varying models):
#
# $$
# \begin{align}
# y_t & = Z \alpha_t + \varepsilon_t, \quad \varepsilon_t \sim N(0, H) \\
# \alpha_{t+1} & = T \alpha_t + R \eta_t \quad \eta_t \sim N(0, Q)
# \end{align}
# $$
#
# Often, some or all of the values in the matrices $Z, H, T, R, Q$ are
# unknown and must be estimated; in statsmodels, estimation is often done by
# finding the parameters that maximize the likelihood function. In
# particular, if we collect the parameters in a vector $\psi$, then each of
# these matrices can be thought of as functions of those parameters, for
# example $Z = Z(\psi)$, etc.
#
# Usually, the likelihood function is maximized numerically, for example
# by applying quasi-Newton "hill-climbing" algorithms, and this becomes more
# and more difficult the more parameters there are. It turns out that in
# many cases we can reparameterize the model as $[\psi_*', \sigma_*^2]'$,
# where $\sigma_*^2$ is the "scale" of the model (usually, it replaces one
# of the error variance terms) and it is possible to find the maximum
# likelihood estimate of $\sigma_*^2$ analytically, by differentiating the
# likelihood function. This implies that numerical methods are only required
# to estimate the parameters $\psi_*$, which has dimension one less than
# that of $\psi$.

# ### Example: local level model
#
# (see, for example, section 4.2 of Harvey (1989))
#
# As a specific example, consider the local level model, which can be
# written as:
#
# $$
# \begin{align}
# y_t & = \alpha_t + \varepsilon_t, \quad \varepsilon_t \sim N(0,
# \sigma_\varepsilon^2) \\
# \alpha_{t+1} & = \alpha_t + \eta_t \quad \eta_t \sim N(0, \sigma_\eta^2)
# \end{align}
# $$
#
# In this model, $Z, T,$ and $R$ are all fixed to be equal to $1$, and
# there are two unknown parameters, so that $\psi = [\sigma_\varepsilon^2,
# \sigma_\eta^2]$.

# #### Typical approach
#
# First, we show how to define this model without concentrating out the
# scale, using statsmodels' state space library:


class LocalLevel(sm.tsa.statespace.MLEModel):
    _start_params = [1., 1.]
    _param_names = ['var.level', 'var.irregular']

    def __init__(self, endog):
        super(LocalLevel, self).__init__(endog,
                                         k_states=1,
                                         initialization='diffuse')

        self['design', 0, 0] = 1
        self['transition', 0, 0] = 1
        self['selection', 0, 0] = 1

    def transform_params(self, unconstrained):
        return unconstrained**2

    def untransform_params(self, unconstrained):
        return unconstrained**0.5

    def update(self, params, **kwargs):
        params = super(LocalLevel, self).update(params, **kwargs)

        self['state_cov', 0, 0] = params[0]
        self['obs_cov', 0, 0] = params[1]


# There are two parameters in this model that must be chosen: `var.level`
# $(\sigma_\eta^2)$ and `var.irregular` $(\sigma_\varepsilon^2)$. We can use
# the built-in `fit` method to choose them by numerically maximizing the
# likelihood function.
#
# In our example, we are applying the local level model to consumer price
# index inflation.

mod = LocalLevel(dta.infl)
res = mod.fit(disp=False)
print(res.summary())

# We can look at the results from the numerical optimizer in the results
# attribute `mle_retvals`:

print(res.mle_retvals)

# #### Concentrating out the scale

# Now, there are two ways to reparameterize this model as above:
#
# 1. The first way is to set $\sigma_*^2 \equiv \sigma_\varepsilon^2$ so
# that $\psi_* = \psi / \sigma_\varepsilon^2 = [1, q_\eta]$ where $q_\eta =
# \sigma_\eta^2 / \sigma_\varepsilon^2$.
# 2. The second way is to set $\sigma_*^2 \equiv \sigma_\eta^2$ so that
# $\psi_* = \psi / \sigma_\eta^2 = [h, 1]$ where $h = \sigma_\varepsilon^2 /
# \sigma_\eta^2$.
#
# In the first case, we only need to numerically maximize the likelihood
# with respect to $q_\eta$, and in the second case we only need to
# numerically maximize the likelihood with respect to $h$.
#
# Either approach would work well in most cases, and in the example below
# we will use the second method.

# To reformulate the model to take advantage of the concentrated
# likelihood function, we need to write the model in terms of the parameter
# vector $\psi_* = [g, 1]$. Because this parameter vector defines
# $\sigma_\eta^2 \equiv 1$, we now include a new line `self['state_cov', 0,
# 0] = 1` and the only unknown parameter is $h$. Because our parameter $h$
# is no longer a variance, we renamed it here to be `ratio.irregular`.
#
# The key piece that is required to formulate the model so that the scale
# can be computed from the Kalman filter recursions (rather than selected
# numerically) is setting the flag `self.ssm.filter_concentrated = True`.


class LocalLevelConcentrated(sm.tsa.statespace.MLEModel):
    _start_params = [1.]
    _param_names = ['ratio.irregular']

    def __init__(self, endog):
        super(LocalLevelConcentrated, self).__init__(endog,
                                                     k_states=1,
                                                     initialization='diffuse')

        self['design', 0, 0] = 1
        self['transition', 0, 0] = 1
        self['selection', 0, 0] = 1
        self['state_cov', 0, 0] = 1

        self.ssm.filter_concentrated = True

    def transform_params(self, unconstrained):
        return unconstrained**2

    def untransform_params(self, unconstrained):
        return unconstrained**0.5

    def update(self, params, **kwargs):
        params = super(LocalLevelConcentrated, self).update(params, **kwargs)
        self['obs_cov', 0, 0] = params[0]


# Again, we can use the built-in `fit` method to find the maximum
# likelihood estimate of $h$.

mod_conc = LocalLevelConcentrated(dta.infl)
res_conc = mod_conc.fit(disp=False)
print(res_conc.summary())

# The estimate of $h$ is provided in the middle table of parameters
# (`ratio.irregular`), while the estimate of the scale is provided in the
# upper table. Below, we will show that these estimates are consistent with
# those from the previous approach.

# And we can again look at the results from the numerical optimizer in the
# results attribute `mle_retvals`. It turns out that two fewer iterations
# were required in this case, since there was one fewer parameter to select.
# Moreover, since the numerical maximization problem was easier, the
# optimizer was able to find a value that made the gradient for this
# parameter slightly closer to zero than it was above.

print(res_conc.mle_retvals)

# #### Comparing estimates
#
# Recall that $h = \sigma_\varepsilon^2 / \sigma_\eta^2$ and the scale is
# $\sigma_*^2 = \sigma_\eta^2$. Using these definitions, we can see that
# both models produce nearly identical results:

print('Original model')
print('var.level     = %.5f' % res.params[0])
print('var.irregular = %.5f' % res.params[1])

print('\nConcentrated model')
print('scale         = %.5f' % res_conc.scale)
print('h * scale     = %.5f' % (res_conc.params[0] * res_conc.scale))

# ### Example: SARIMAX
#
# By default in SARIMAX models, the variance term is chosen by numerically
# maximizing the likelihood function, but an option has been added to allow
# concentrating the scale out.

# Typical approach
mod_ar = sm.tsa.SARIMAX(dta.cpi, order=(1, 0, 0), trend='ct')
res_ar = mod_ar.fit(disp=False)

# Estimating the model with the scale concentrated out
mod_ar_conc = sm.tsa.SARIMAX(dta.cpi,
                             order=(1, 0, 0),
                             trend='ct',
                             concentrate_scale=True)
res_ar_conc = mod_ar_conc.fit(disp=False)

# These two approaches produce about the same loglikelihood and
# parameters, although the model with the concentrated scale was able to
# improve the fit very slightly:

print('Loglikelihood')
print('- Original model:     %.4f' % res_ar.llf)
print('- Concentrated model: %.4f' % res_ar_conc.llf)

print('\nParameters')
print('- Original model:     %.4f, %.4f, %.4f, %.4f' % tuple(res_ar.params))
print('- Concentrated model: %.4f, %.4f, %.4f, %.4f' %
      (tuple(res_ar_conc.params) + (res_ar_conc.scale, )))

# This time, about 1/3 fewer iterations of the optimizer are required
# under the concentrated approach:

print('Optimizer iterations')
print('- Original model:     %d' % res_ar.mle_retvals['iterations'])
print('- Concentrated model: %d' % res_ar_conc.mle_retvals['iterations'])
