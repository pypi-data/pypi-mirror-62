#! /usr/bin/env python3

from .base_metric_loss_function import BaseMetricLossFunction
import numpy as np
import torch
from ..utils import loss_and_miner_utils as lmu

class AngularLoss(BaseMetricLossFunction):
    """
    Implementation of https://arxiv.org/abs/1708.01682
    Args:
        alpha: The angle (as described in the paper), specified in degrees.
    """
    def __init__(self, alpha, triplets_per_anchor=100, **kwargs):
        super().__init__(**kwargs)
        self.alpha = torch.tensor(np.radians(alpha))
        self.triplets_per_anchor = triplets_per_anchor
        self.add_to_recordable_attributes(list_of_names=["num_anchors", "average_angle"])
        
    def compute_loss(self, embeddings, labels, indices_tuple):
        anchors, positives, negatives = self.set_stats_get_triplets(embeddings, labels, indices_tuple)
        if anchors is None: return 0
        sq_tan_alpha = torch.tan(self.alpha) ** 2
        term1 = 4 * sq_tan_alpha * torch.sum((anchors + positives) * negatives, dim=1, keepdim=True)
        term2 = 2 * (1 + sq_tan_alpha) * torch.sum(anchors * positives, dim=1, keepdim=True)
        final_form = term1-term2
        final_form = self.maybe_modify_loss(final_form)
        return torch.mean(lmu.logsumexp(final_form, add_one=True))

    def set_stats_get_triplets(self, embeddings, labels, indices_tuple):
        anchor_idx, positive_idx, negative_idx = lmu.convert_to_triplets(indices_tuple, labels, self.triplets_per_anchor)
        self.num_anchors = len(anchor_idx)
        if self.num_anchors == 0:
            return [None]*4
        anchors, positives, negatives = embeddings[anchor_idx], embeddings[positive_idx], embeddings[negative_idx]
        centers = (anchors + positives) / 2
        ap_dist = torch.nn.functional.pairwise_distance(anchors, positives, 2)
        nc_dist = torch.nn.functional.pairwise_distance(negatives, centers, 2)
        self.average_angle = np.degrees(torch.mean(torch.atan(ap_dist / (2*nc_dist))).item())
        return anchors, positives, negatives

    def create_learnable_parameter(self, init_value):
        return super().create_learnable_parameter(init_value, unsqueeze=True)

    def maybe_modify_loss(self, x):
        return x
