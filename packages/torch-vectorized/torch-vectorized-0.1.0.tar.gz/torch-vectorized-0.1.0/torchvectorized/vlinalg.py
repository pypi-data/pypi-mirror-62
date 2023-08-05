from math import pi

import torch


def _compute_eigen_values(input):
    b, c, d, h, w = input.size()
    a11 = input[:, 0, :, :, :].double()
    a12 = input[:, 1, :, :, :].double()
    a13 = input[:, 2, :, :, :].double()
    a22 = input[:, 4, :, :, :].double()
    a23 = input[:, 5, :, :, :].double()
    a33 = input[:, 8, :, :, :].double()
    eig_vals = torch.zeros(b, 3, d, h, w).to(input.device).double()

    nd = torch.pow(a12, 2) + torch.pow(a13, 2) + torch.pow(a23, 2)

    q = (a11 + a22 + a33) / 3.0
    p = torch.pow((a11 - q), 2) + torch.pow((a22 - q), 2) + torch.pow((a33 - q), 2) + 2.0 * nd
    p = torch.sqrt(p / 6.0)

    r = torch.pow((1.0 / p), 3) * ((a11 - q) * ((a22 - q) * (a33 - q) - a23 * a23) - a12 * (
            a12 * (a33 - q) - a13 * a23) + a13 * (a12 * a23 - a13 * (a22 - q))) / 2.0

    phi = torch.acos(r) / 3.0
    phi[r <= -1] = pi / 3
    phi[r >= 1] = 0

    eig_vals[:, 0, :, :, :] = q + 2 * p * torch.cos(phi)
    eig_vals[:, 2, :, :, :] = q + 2 * p * torch.cos(phi + pi * (2.0 / 3.0))
    eig_vals[:, 1, :, :, :] = 3 * q - eig_vals[:, 0, :, :, :] - eig_vals[:, 2, :, :, :]

    return eig_vals


def _compute_eigen_vectors(input, eigen_values):
    a11 = input[:, 0, :, :, :].unsqueeze(1).expand(eigen_values.size()).double()
    a12 = input[:, 1, :, :, :].unsqueeze(1).expand(eigen_values.size()).double()
    a13 = input[:, 2, :, :, :].unsqueeze(1).expand(eigen_values.size()).double()
    a22 = input[:, 4, :, :, :].unsqueeze(1).expand(eigen_values.size()).double()
    a23 = input[:, 5, :, :, :].unsqueeze(1).expand(eigen_values.size()).double()

    u0 = a12 * a23 - a13 * (a22 - eigen_values)
    u1 = a12 * a13 - a23 * (a11 - eigen_values)
    u2 = (a11 - eigen_values) * (a22 - eigen_values) - a12 * a12
    norm = torch.sqrt(torch.pow(u0, 2) + torch.pow(u1, 2) + torch.pow(u2, 2))
    u0 = u0 / norm
    u1 = u1 / norm
    u2 = u2 / norm

    return torch.cat([u0.unsqueeze(1), u1.unsqueeze(1), u2.unsqueeze(1)], dim=1)


def vSymeig(input, eigen_vectors=False, flatten_output=False):
    eig_vals = _compute_eigen_values(input)

    if eigen_vectors:
        eig_vecs = _compute_eigen_vectors(input, eig_vals)
    else:
        eig_vecs = None

    if flatten_output:
        b, c, d, h, w = input.size()
        eig_vals = eig_vals.permute(0, 2, 3, 4, 1).reshape(b * d * h * w, 3)
        eig_vecs = eig_vecs.permute(0, 3, 4, 5, 1, 2).reshape(b * d * h * w, 3, 3) if eigen_vectors else eig_vecs

    return eig_vals.float(), eig_vecs.float() if eig_vecs is not None else None
