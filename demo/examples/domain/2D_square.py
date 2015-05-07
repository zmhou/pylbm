# Authors:
#     Loic Gouarin <loic.gouarin@math.u-psud.fr>
#     Benjamin Graille <benjamin.graille@math.u-psud.fr>
#
# License: BSD 3 clause

"""
Example of a square in 2D
"""
import pyLBM
dico = {
    'box':{'x': [0, 1], 'y': [0, 1], 'label': [0,1,2,3]},
    'space_step':0.1,
    'schemes':[{'velocities':range(9)}],
}
dom = pyLBM.Domain(dico)
dom.visualize(opt=0)
dom.visualize(opt=1)
