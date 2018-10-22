# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 09:54:20 2018

@author: ayadav
"""

#Dataset For Blinks Template
Blink=[0.1,0.1]
Blink[0]=([-8.42063169e-03,  6.29578815e-02,  1.53503221e-02, -3.91155308e-02,
       -1.14877220e-02,  7.67198335e-02,  1.08396680e-01, -1.09572546e-02,
       -1.05465955e-01, -6.15312294e-02,  2.46403478e-02,  4.74253989e-02,
       -6.57579474e-03, -5.85548317e-02, -1.27395291e-01, -1.92307921e-01,
       -1.74103192e-01, -1.10561123e-01, -3.50814559e-02, -6.67501427e-04,
       -1.40283385e-03, -2.79179123e-02, -1.08882557e-01, -1.77882437e-01,
       -2.65648955e-01, -3.31118270e-01, -3.48606792e-01, -4.81622707e-01,
       -7.05799969e-01, -9.32454053e-01, -1.11703209e+00, -1.28321696e+00,
       -1.51207283e+00, -1.72716404e+00, -1.91586998e+00, -2.06006449e+00,
       -2.07359062e+00, -1.99653467e+00, -1.88369690e+00, -1.83139500e+00,
       -1.80002259e+00, -1.69937284e+00, -1.56698499e+00, -1.35346271e+00,
       -1.17520125e+00, -1.07958892e+00, -9.13952525e-01, -7.10992557e-01,
       -5.13575004e-01, -3.71876386e-01, -2.42879438e-01, -7.35852564e-02,
        5.10989321e-02,  1.74061653e-01,  2.44334157e-01,  2.95926167e-01,
        4.74781655e-01,  6.60709743e-01,  8.16583407e-01,  9.46905667e-01,
        1.04776578e+00,  1.13612022e+00,  1.14362585e+00,  1.16034371e+00,
        1.19033852e+00,  1.22447974e+00,  1.31030469e+00,  1.31984351e+00,
        1.29758689e+00,  1.31748192e+00,  1.38477807e+00,  1.47743443e+00,
        1.49449851e+00,  1.50374105e+00,  1.47081480e+00,  1.39759323e+00,
        1.41094479e+00,  1.42604446e+00,  1.42814112e+00,  1.40722458e+00,
        1.38096224e+00,  1.40359004e+00,  1.37685249e+00,  1.34237619e+00,
        1.30488664e+00,  1.27911788e+00,  1.33998996e+00,  1.37560868e+00,
        1.35750494e+00,  1.25718953e+00,  1.16855819e+00,  1.21407738e+00,
        1.21551885e+00,  1.15799759e+00,  1.10210058e+00,  1.09710551e+00,
        1.17984237e+00,  1.16095892e+00,  1.01229995e+00,  8.54400593e-01,
        8.26592760e-01,  9.05052990e-01,  8.39198878e-01,  6.88963897e-01,
        6.20696242e-01,  6.54428001e-01,  7.08042116e-01,  6.42779352e-01,
        5.34511408e-01,  4.48742398e-01,  4.12867687e-01,  4.03826989e-01,
        3.34846706e-01,  3.09693404e-01,  2.84102613e-01,  2.36013029e-01,
        2.76027463e-01,  3.14254636e-01,  3.23449999e-01,  2.50154263e-01,
        1.18352278e-01,  5.22003742e-02, -6.78925299e-03, -3.88379568e-02,
       -1.07796793e-01, -2.13581884e-01, -2.05375103e-01, -1.38219343e-01,
       -6.91098476e-02, -9.22914229e-02, -1.69943477e-01, -1.84595371e-01,
       -2.02785544e-01, -1.75702426e-01, -1.66745965e-01, -2.27153644e-01,
       -2.47868247e-01, -2.91715551e-01, -3.58112450e-01, -4.33559476e-01,
       -4.73244069e-01, -4.67772066e-01, -5.76163784e-01, -5.68739198e-01,
       -2.93339666e-01, -1.79069668e-01, -5.14783916e-01, -1.03472598e+00,
       -1.33768955e+00, -1.49053091e+00])

Blink_Bad=[0.1,0.1]
Blink_Bad[0]=([-2.25996384, -1.38211301, -0.70334075, -1.21189412, -2.26605792,
               -2.35259529, -1.1118049 ,  0.02661181, -0.32983774, -1.5042672 ,
               -1.71631316, -0.4345517 ,  0.87435519,  0.61141436, -0.61930513,
               -0.85387761,  0.55460405,  1.98634729,  1.67948607,  0.29421557,
               -0.08037687,  1.23144563,  2.56248914,  2.13047974,  0.67834567,
                0.3526184 ,  1.74480083,  3.08798209,  2.59528898,  1.0181522 ,
                0.53377214,  1.84705914,  3.25070366,  2.85136279,  1.28093287,
                0.76922549,  2.08578785,  3.43744346,  2.92372922,  1.30626241,
                0.78155029,  2.05427548,  3.44059892,  3.03338134,  1.45552806,
                0.8618069 ,  2.01504765,  3.32387058,  2.91303718,  1.34737261,
                0.72217669,  1.77131053,  2.95361911,  2.53165618,  1.07532809,
                0.55811878,  1.67044535,  2.89021884,  2.48063946,  1.01349177,
                0.44628505,  1.42716991,  2.48536967,  2.0352659 ,  0.68974635,
                0.24954983,  1.24894994,  2.32331972,  2.01125875,  0.80651463,
                0.32289577,  1.1437355 ,  2.07242961,  1.71676103,  0.53287762,
                0.0324303 ,  0.78397935,  1.74109009,  1.55439861,  0.53647662,
                0.11062598,  0.82284351,  1.66653514,  1.44824003,  0.51324284,
                0.114929  ,  0.74660837,  1.48809652,  1.21356873,  0.33966805,
                0.05712121,  0.6687126 ,  1.2754072 ,  0.99862805,  0.26763507,
                0.01385748,  0.49621492,  1.04154062,  0.83974148,  0.15578827,
               -0.13074885,  0.31652679,  0.84020612,  0.61946742, -0.05942606,
               -0.28911973,  0.23251397,  0.78105259,  0.54487083, -0.14453126,
               -0.43897983, -0.10951339,  0.28982474,  0.1965507 , -0.17232878,
               -0.30866358, -0.01708287,  0.36530308,  0.3245389 , -0.00503994,
               -0.13606612,  0.12615209,  0.43841204,  0.3525758 ,  0.04350264,
               -0.12051049,  0.02504367,  0.30596033,  0.30071906,  0.0638388 ,
               -0.04212167,  0.11852015,  0.28877758,  0.15575332, -0.08589691,
               -0.17480821, -0.04776565,  0.15310386,  0.11889553, -0.0738218 ,
               -0.20436404, -0.17456259])