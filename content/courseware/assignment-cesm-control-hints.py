# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Additional hints and guidance for CESM budgets assignment
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# %% [markdown]
# ## Preface
#
# In the homework assignment you are asked to compute various terms in the global-average energy budget from the CESM control simulation and compare them to the observations.
#
# In the lecture notes, we walked through how to open the dataset and compute the time- and global averages.
#
# The main challenge here is just understanding how to relate the diagnostic fields in the CESM output dataset to the quantities you are asked to calculate. I give some additional guidance here.

# %% [markdown]
# ## What do we mean by "upwelling", "downwelling", "net"?
#
# To understand these terms, just picture the beam of radiation traveling between the surface of the Earth and the top of that atmosphere. “Downwelling” means traveling downward (i.e. toward the surface), and “upwelling” means traveling upward.
#
# The beam of shortwave (solar) radiation arrives from the sun at the top of the atmosphere and travels downward. Some of that beam is reflected back upward. So the quantity we have denoted as Q in our notes, the total sunlight incident upon the Earth, is the downwelling shorwave flux at the top of the atmosphere. The upwelling shortwave flux at the top of the atmosphere is a number that is smaller than Q and represents the reflection.
#
# For the longwave beam, it’s the same idea — there is a beam moving upward, or “upwelling”, and a beam moving downward, or “downwelling”. The difference is that this beam is generated by the Earth and the atmosphere itself.
# The upwelling flux at the surface is the surface emission. The downwelling flux at the surface is the radiation absorbed by the surface (originating somewhere in the atmosphere).
#
# The "net" flux is the difference between the upwelling and downwelling beams. We have to be careful about sign conventions! In the CESM data, "net" means net upward for longwave radiation, but net downward for shortwave radiation.
#
# The net longwave flux at the top of the atmosphere is what we have called the Outgoing Longwave Radiation.
#
# The net shortwave flux at the top of the atmosphere is what we have called the Absorbed Shortwave Radiation.

# %% [markdown]
# ## From the lecture notes -- CESM naming conventions
#
# Reproduced from the lecture notes:
#
# The model output contains lots of diagnostics about the radiative fluxes. Here are some CESM naming conventions to help you find the appropriate output fields:
#
# - All variables whose names being with `'F'` are an **energy flux** of some kind. 
# - Most have a four-letter code, e.g. `'FLNT'`
# - `'FL'` means **longwave flux** (i.e. terrestrial)
# - `'FS'` means **shortwave flux** (i.e. solar)
# - The third letter indicates **direction** of the flux:
#     - `'U'` = up
#     - `'D'` = down
#     - `'N'` = net
# - The fourth letter indicates the **location** of the flux:
#     - `'T'` = top of atmosphere
#     - `'S'` = surface
# - So `'FLNT'` means 'net longwave flux at the top of atmosphere', i.e. the outgoing longwave radiation or OLR.
#
# You wil see that these are all 240 x 96 x 144 -- i.e. a two-dimensional grid for every month in the simulation.

# %% [markdown]
# The one exception to this naming convention is that, as we saw in the lecture notes, the incoming solar radiation (or insolation) is **not** called `FSDT` ("Flux of Shortwave radiation Downward at the Top") in the dataset but instead called `SOLIN`.

# %% [markdown]
# ## Load the data and take a quick look

# %%
import xarray as xr

cesm_data_path = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
atm_control = xr.open_dataset(cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")

# %% [markdown]
# Based on the above name conventions, we should be able to find the downwelling longwave radiation at the surface as `atm_control.FLDS`, since it is "Flux of Longwave traveling Downward at the Surface":

# %%
atm_control.FLDS

# %% [markdown]
# So that works!
#
# Now, let's see if we can find the reflected shortwave radiation at the top of the atmosphere as `atm_control.FSUT`, since it is "Flux of Shortwave traveling Upward at the Top".

# %%
atm_control.FSUT

# %% [markdown]
# This field is apparently not in the dataset!

# %% [markdown]
# ## Calculating fields that are missing from the dataset
#
# Some of the fields we need are not directly stored in the dataset. 
#
# But that's ok, because we have enough information to calculate them using simple arithmetic with the fields we do have.
#
# In the case of our missing `FSUT` field, the key point is that we do have the "Net" field `FSNT` and the downwelling field `SOLIN`.
#
# Since the Net Flux is the difference:
#
# `FSNT = SOLIN - FSUT`
#
# (i.e. the difference between what's coming in and what's going out!)
#
# then we can rearrange this to solve for our unknown field:
#
# `FSUT = SOLIN - FSNT`
#
# We can do this kind of arithmetic with the xarray datasets:

# %%
#  Take the difference between the downwelling shortwave flux at the net shortwave flux at the top of atmosphere
#  The result is the upwelling flux, i.e. the reflected shortwave flux
#   Store this difference in a new variable called FSUT
FSUT = atm_control.SOLIN - atm_control.FSNT

# %% [markdown]
# ### A few other derived field examples
#
# In the homework I ask you calculate the longwave "Upward emission from the surface". That should be `FLUS`

# %%
atm_control.FLUS

# %% [markdown]
# Same problem as above, and same solution. 
#
# We have the downwelling flux `FLDS` (positive down), and the net flux `FLNS` (positive up). The net flux is defined as
#
# `FLNS = FLUS - FLDS`
#
# We get the upward flux by rearranging:
#
# `FLUS = FLNS + FLDS`

# %%
FLUS = atm_control.FLDS + atm_control.FLNS

# %% [markdown]
# All of us get confused about these sign conventions! It's helpful to draw yourself a sketch of the fluxes going up and down.
#
# We should also verify that our results make sense physically. If I take the global, time average of the `FLUS` field, it should be a large positive number! 
#
# Remember that we are comparing to the observations, where the value is 396 W/m2.

# %%
#  don't forget to take the area-weighted average!
weight_factor2 = atm_control.gw / atm_control.gw.mean(dim='lat')
#  I'm going to calculate the average and print it out, rounded to the second decimal place
myvalue = (FLUS*weight_factor2).mean(dim=('time','lat','lon')).values  
# note that adding .values at the end of the expression gives me just the number without the metadata
print('Downwelling longwave radiation at the surface: {:.2f} W/m2'.format(myvalue))   
# This is an example of a formatted print statement in Python

# %% [markdown]
# This apparently very close to the observed value, which is a good indicator that we did the calculation correctly.

# %% [markdown]
# ____________
#
# ## Credits
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.
#
# It is licensed for free and open consumption under the
# [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.
#
# Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
# ____________

# %%