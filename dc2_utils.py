import GCRCatalogs
from GCR import GCRQuery
import numpy as np

def load_catalogs(ra_min=52.3, ra_max=57.9, dec_min=-32.2, dec_max=-27.3):
    # coordinate box defaul is set from looking at plots general_analysis.ipynb
    truth = GCRCatalogs.load_catalog("dc2_truth_run1.2_static")
    objects = GCRCatalogs.load_catalog("dc2_object_run1.2p")


    coord_filter = [
                'ra >= {}'.format(ra_min), 
                'ra < {}'.format(ra_max), 
                'dec >= {}'.format(dec_min), 
                'dec < {}'.format(dec_max),
                ]


    object_filter = [
                GCRQuery('clean'),
                (np.isfinite, 'mag_r'),
                (np.isfinite, 'magerr_r'),
                (np.isfinite, 'mag_r_cModel'),
                (np.isfinite, 'mag_g'),
                (np.isfinite, 'magerr_g'),
                (np.isfinite, 'extendedness'),
                ]

    #star_thresh = 0.0164 # see object_gcr_1_intro.ipynb
    star_filter = [
                GCRQuery('extendedness == 0'),
                #GCRQuery('mag_r - mag_r_cModel < {}'.format(star_thresh)),
                #GCRQuery('magerr_r < 0.1'),
                ]

    object_all = objects.get_quantities(['objectId', 'ra', 'dec', 'mag_r', 'magerr_r', 'mag_r_cModel', 'mag_g', 'magerr_g', 'mag_g_cModel', 'extendedness'],  
                                              filters = coord_filter + object_filter)
    object_stars = objects.get_quantities(['objectId', 'ra', 'dec', 'mag_r', 'magerr_r', 'mag_r_cModel', 'mag_g', 'magerr_g', 'mag_g_cModel'], 
                                              filters = coord_filter + object_filter + star_filter)

    len_object_all = len(object_all['ra'])
    len_object_stars = len(object_stars['ra'])

    object_data = object_all, len_object_all, object_stars, len_object_stars

    truth_filters = [(np.isfinite, 'r'), (np.isfinite, 'g')]

    truth_all = truth.get_quantities(['ra', 'dec', 'mag_true_r', 'mag_true_g'],
                                           native_filters = coord_filter,  
                                           filters = truth_filters)
    truth_stars = truth.get_quantities(['ra', 'dec', 'mag_true_r', 'mag_true_g'],
                                           native_filters = coord_filter + ['star == 1'],
                                           filters = truth_filters)
    len_truth_all = len(truth_all['ra'])
    len_truth_stars = len(truth_stars['ra'])

    truth_data = truth_all, len_truth_all, truth_stars, len_truth_all

    print("Coadd objects:", len_object_all, ", Coadd stars:", len_object_stars)
    print("Truth objects:", len_truth_all, ", Truth stars:", len_truth_stars)

    return object_data, truth_data

