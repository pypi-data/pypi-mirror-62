# Copyright 2019 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for The Walrus quantum functions"""
# pylint: disable=no-self-use,redefined-outer-name

import numpy as np
from thewalrus.quantum import density_matrix, state_vector


def test_cubic_phase():
    """Test that all the possible ways of obtaining a cubic phase state using the different methods agree"""
    mu = np.array([-0.50047867, 0.37373598, 0.01421683, 0.26999427, 0.04450994, 0.01903583])

    cov = np.array(
        [
            [1.57884241, 0.81035494, 1.03468307, 1.14908791, 0.09179507, -0.11893174],
            [0.81035494, 1.06942863, 0.89359234, 0.20145142, 0.16202296, 0.4578259],
            [1.03468307, 0.89359234, 1.87560498, 0.16915661, 1.0836528, -0.09405278],
            [1.14908791, 0.20145142, 0.16915661, 2.37765137, -0.93543385, -0.6544286],
            [0.09179507, 0.16202296, 1.0836528, -0.93543385, 2.78903152, -0.76519088],
            [-0.11893174, 0.4578259, -0.09405278, -0.6544286, -0.76519088, 1.51724222],
        ]
    )

    cutoff = 7
    # the Fock state measurement of mode 0 to be post-selected
    m1 = 1
    # the Fock state measurement of mode 1 to be post-selected
    m2 = 2

    psi = state_vector(mu, cov, post_select={0: m1, 1: m2}, cutoff=cutoff, hbar=2)
    psi_c = state_vector(mu, cov, cutoff=cutoff, hbar=2)[m1, m2, :]
    rho = density_matrix(mu, cov, post_select={0: m1, 1: m2}, cutoff=cutoff, hbar=2)
    rho_c = density_matrix(mu, cov, cutoff=cutoff, hbar=2)[m1, m1, m2, m2, :, :]
    assert np.allclose(np.outer(psi, psi.conj()), rho)
    assert np.allclose(np.outer(psi_c, psi_c.conj()), rho)
    assert np.allclose(rho_c, rho)
