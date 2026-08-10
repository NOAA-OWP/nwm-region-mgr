"""Unsupervised Random Forest.

For an unsupervised random forest, the set up is as follows:

1) A joint distribution of the explanatory variables is constructed and draws are taken from this distribution to create synthetic data. In most cases the same number of draws as in the real data set will be taken.
2) The real and synthetic data are combined. A label is then created, say 1 for the real data and 0 for the synthetic data.
3) The random forest model then works in the same way, building a set of weak learners and determining whether or not observation i is real or synthetic.

The key output is a similarity/dissimilarity matrix, which will be used by the regionalization algorithm to assign donors to receivers.

"""

import warnings

import numpy as np
from joblib import Parallel, delayed
from numba import njit
from sklearn.ensemble import RandomForestClassifier

from nwm_region_mgr.parreg import synthetic_data

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")


class URF(object):
    """Unsupervised Random Forest (URF)."""

    def __init__(
        self, n_trees=100, synthetic_data_type=None, max_features="sqrt", max_depth=None
    ):
        """Initialize Unsupervised Random Forest (URF) class."""
        self.n_trees = n_trees
        self.synthetic_data_type = synthetic_data_type
        self.max_features = max_features
        self.max_depth = max_depth

        return

    def get_random_forest(self):
        """Run random forest on x."""
        x_total, y_total = synthetic_data.create_synthetic_data(
            self.x, self.synthetic_data_type
        )

        rf = RandomForestClassifier(
            n_jobs=-1,
            n_estimators=self.n_trees,
            max_features=self.max_features,
            max_depth=self.max_depth,
        )
        rf.fit(x_total, y_total)

        return rf

    def get_leafs(self):
        """Get leafs."""
        rf = self.get_random_forest()
        rf_leafs = rf.apply(self.x)

        is_good = is_good_matrix_get(rf, self.x)
        return rf_leafs, is_good

    def get_xs(self, x):
        """Get xs."""
        try:
            objnum = x.shape[0]
            xs = x
        except:
            # TODO handle a specific Exception here
            xs = x.copy()
            x = np.hstack(xs)
            objnum = x.shape[0]

        csize = 10
        start = np.arange(1 + int(objnum / csize)) * csize
        end = start + csize
        fe = np.vstack([start, end]).T
        fe[-1][1] = objnum

        self.fe = fe
        self.xs = xs
        self.x = x

        return

    def get_distance(self, x, njob=1, donor_idx=None, receiver_idx=None):
        """Get the dissimilarity matrix produced by the random forest model."""
        self.get_xs(x)
        leafs, is_good = self.get_leafs()

        if donor_idx is None:
            donor_idx = np.arange(x.shape[0])
        if receiver_idx is None:
            receiver_idx = np.arange(x.shape[0])

        # Parallel over receiver_idx blocks
        blocks = Parallel(n_jobs=njob)(
            delayed(build_distance_matrix_slow)(
                leafs,
                is_good,
                np.array([ri], dtype=np.int32),  # single receiver per task
                np.array(donor_idx, dtype=np.int32),
            )
            for ri in receiver_idx
        )

        # Stack into final (receivers × donors)
        dist = np.vstack(blocks)

        return dist

    def get_anomaly_score(self, x, mean_over=2500, knn=None, njob=1):
        """Get anomaly score."""
        self.get_xs(x)
        rf_leafs, is_good = self.get_leafs()

        nof_objects = x.shape[0]

        if knn is not None:
            mean_over = nof_objects
            knn = int(knn)

        if mean_over < nof_objects:
            distance_to_objects = np.random.choice(
                nof_objects, mean_over, replace=False
            )
        else:
            distance_to_objects = np.arange(nof_objects)

        anomaly_score = Parallel(n_jobs=njob)(
            delayed(get_anomaly_score_slow)(
                knn, distance_to_objects, rf_leafs, is_good, se
            )
            for se in self.fe
        )

        anomaly_score = np.concatenate(anomaly_score)

        return anomaly_score


def is_good_vec(tree, x):
    """Determine good vec."""
    return tree.predict_proba(x)[:, 0] > 0.5


def is_good_matrix_get(forest, x, njob=1):
    """Determine good matrix."""
    is_good_matrix = Parallel(n_jobs=njob, verbose=0)(
        delayed(is_good_vec)(tree, x) for tree in forest.estimators_
    )
    is_good_matrix = np.vstack(is_good_matrix)
    is_good_matrix = is_good_matrix.T

    return is_good_matrix


@njit
def get_anomaly_score_slow(knn, distance_to_objects, leafs, is_good, fe):
    """Get anomaly score."""
    start = fe[0]
    end = fe[1]

    # obs_num = leafs.shape[0]
    tree_num = leafs.shape[1]
    anomaly_score = np.zeros(end - start)
    dists = np.zeros(distance_to_objects.shape)

    for i in range(start, end):
        for j_idx, j in enumerate(distance_to_objects):
            same_leaf = 0
            good_trees = 0
            for k in range(tree_num):
                if (is_good[i, k] == 1) and (is_good[j, k] == 1):
                    good_trees = good_trees + 1
                    if leafs[i, k] == leafs[j, k]:
                        same_leaf = same_leaf + 1
            if good_trees == 0:
                dis = 1
            else:
                dis = 1 - float(same_leaf) / good_trees

            dists[j_idx] = dis
        if knn is None:
            anomaly_score[i - start] = np.sum(dists)
        else:
            anomaly_score[i - start] = np.sort(dists)[knn]

    return anomaly_score


@njit
def build_distance_matrix_slow(leafs, is_good, receiver_idx, donor_idx):
    """Compute the n_receiver x n_donor block of the distance matrix.

    To save memory for large VPU calculations, this function avoids computing the full
    (n_receiver+n_donor) x (n_receiver+n_donor) distance matrix, and uses float32 for dtype.

    leafs:      (N x T)   int32
    is_good:    (N x T)   int8 (0/1)
    receiver_idx: list/array of indices to compute rows for
    donor_idx:    list/array of indices to compute columns for
    """
    n_rec = len(receiver_idx)
    n_donor = len(donor_idx)
    tree_num = leafs.shape[1]

    # use float32 (rather than float64 to save memory for large VPUs)
    out = np.ones((n_rec, n_donor), dtype=np.float32)

    for ri in range(n_rec):
        i = receiver_idx[ri]
        for dj in range(n_donor):
            j = donor_idx[dj]

            same_leaf = 0
            good_trees = 0

            for k in range(tree_num):
                if is_good[i, k] == 1 and is_good[j, k] == 1:
                    good_trees += 1
                    if leafs[i, k] == leafs[j, k]:
                        same_leaf += 1

            if good_trees == 0:
                out[ri, dj] = 1.0
            else:
                out[ri, dj] = 1.0 - same_leaf / good_trees

    return out
