Frequently Asked Questions
--------------------------

.. dropdown:: What is nwm_region_mgr?

    nwm_region_mgr is a command line utility for identifying optimized NextGen
    formulations and parameter values in ungauged catchments.

.. dropdown:: What is a formulation?

    A NextGen formulation is any single model or combination of models and/or
    modules running in a basin to simulate that location's hydrology. A formulation
    may include one more hydrologic models and modules, plus a streamflow routing
    module, a coastal model, and other supporting routines.

    For more information on the available models/modules, please see
    https://github.com/NOAA-OWP/NextGen-Info

.. dropdown:: What are parameters in this context?

    Every model or module utilizes parameters to reflect physical attributes of
    a location when making predictions of hydrologic behavior. Parameters might
    measure physical quantities such as drainage area, they could be dimensionless
    indices such as topographic wetness index, or they may be non-interpretable
    quantities such as weights and activation functions in a neural network. Each
    model or module will require different sets of parameters to make predictions.

    During calibration in gauged catchments, parameter values are tuned to create
    the "best" recreation of observed data for a given model.

.. dropdown:: In what areas of the world can I run this?

    Regionalization is currently supported for CONUS, Alaska, Hawaii, and Puerto
    Rico and the Virgin Islands.  The spatial domain is set in config_general.yaml
    under the general:domain field, where values can be conus, ak, hi, prvi,
    respectively.

.. dropdown:: What watershed delineations are used?

    Regionalization relies on the NextGen Hydrofabric.

.. dropdown:: What spatial unit are parameters assigned to?

    Regionalization is flexible, and users can set the level that parameters are
    assigned using the spatial_unit field in config_formreg.yaml.

.. dropdown:: How does nwm_region_mgr find optimal formulations?

    Optimal formulations are determined based on formulation computational cost and user-specified performance metrics (
    ex. Nash–Sutcliffe efficiency (nse), Kling-Gupta efficiency (KGE), bias, or correlation (cor))


.. dropdown:: How does nwm_region_mgr find optimal parameter values?

    Parameter values are assigned to each hydrofabric divide by identifying calibrated catchments that are close to the
    divide in either mapped location or physiographic characteristics.

.. dropdown:: How do I start using this tool?

    Check out the `User Guide <user_guide.html>`_ to get started.
