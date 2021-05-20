def pr_corr(E_out, irradiance, temp_cell,
            temp_coeff=-0.003, temp_amb=25.0,
            irradiance_ref=1000, p0=450, modules=1):
    '''
    Performance ratio corrected with the temperature effect

    Parameters
    ----------
    E_out : TYPE
        DESCRIPTION.
    irradiance : TYPE
        DESCRIPTION.
    temp_cell : TYPE
        DESCRIPTION.
    temp_coeff : TYPE, optional
        DESCRIPTION. The default is -0.003.
    temp_amb : TYPE, optional
        DESCRIPTION. The default is 25.0.
    irradiance_ref : TYPE, optional
        DESCRIPTION. The default is 1000.
    p0 : TYPE, optional
        DESCRIPTION. The default is 450.
    modules : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------
    pr_corr*100.

    '''

    pr_corr = (E_out/(p0*modules)) / (modules*(irradiance/irradiance_ref)
                                      * (1+temp_coeff*(temp_cell-temp_amb)))

    return pr_corr*100


def pr(E_out, irradiance,
       irradiance_ref=1000, p0=450, modules=1):
    '''
    Performance ratio for a pv system

    Parameters
    ----------
    E_out : TYPE
        Energie out in AC.
    irradiance : TYPE
        irradiance.
    irradiance_ref : TYPE, optional
        Irradiance in STC. The default is 1000.
    p0 : TYPE, optional
        Peak power. The default is 450.
    modules : TYPE, optional
        Number of modules. The default is 1.

    Returns
    -------
    pr*100.

    '''
    pr = (E_out/(p0*modules))/(modules*(irradiance/irradiance_ref))

    return pr*100
