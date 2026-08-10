"""Utils for algorithms."""

import logging
import warnings

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import pairwise_distances_chunked
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")
logger = logging.getLogger(__name__)


def compute_pairwise_centroid_distances(
    group_a: gpd.GeoDataFrame,
    group_b: gpd.GeoDataFrame,
    id_col_a: str = "div_id",
    id_col_b: str = "div_id",
) -> pd.DataFrame:
    """Compute pairwise distances between centroids of two GeoDataFrames.

    Parameters
    ----------
    group_a : gpd.GeoDataFrame
        The first GeoDataFrame containing geometries and IDs.
    group_b : gpd.GeoDataFrame
        The second GeoDataFrame containing geometries and IDs.
    id_col_a : str, optional
        The name of the ID column in group_a. Default is "div_id".
    id_col_b : str, optional
        The name of the ID column in group_b. Default is "div_id".

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the centroid distances between each pair of polygons from the two GeoDataFrames in (km),
        where the columns are indexed by polygon ids from group_a, and the rows are indexed by polygon ids from group_b.

    """
    a_ids = group_a[id_col_a].values
    b_ids = group_b[id_col_b].values

    centroids_a = group_a.to_crs(5070).geometry.centroid
    x = np.array([centroids_a.x.values, centroids_a.y.values]).T / 1000
    del centroids_a

    centroids_b = group_b.to_crs(5070).geometry.centroid
    y = np.array([centroids_b.x.values, centroids_b.y.values]).T / 1000
    del centroids_b

    x = downscale(x)
    y = downscale(y)
    data = pairwise_distances_chunked(x, y, metric="sqeuclidean")
    del x
    del y
    ds = []
    for i in data:
        ds.append(np.sqrt(i).astype(np.uint16))
    data = np.concatenate(ds)
    del ds
    data = pd.DataFrame(
        data,
        columns=[str(c) for c in b_ids],
        index=[str(i) for i in a_ids],
    ).T

    data = data.sort_index(axis=0)
    data = data.sort_index(axis=1)
    return data


def downscale(arr):
    """Downscale a NumPy array to a smaller integer type if possible."""
    max_val = arr.flatten().max()
    for i in [np.uint8, np.uint16, np.uint32]:
        if max_val <= np.iinfo(i).max:
            return arr.round().astype(i)


def compute_distances_for_a(
    centroid_a: Point,
    centroids_b: gpd.GeoSeries,
    distance_threshold: int | float | None,
) -> list:
    """Compute distance between a point and a series of points."""
    distances = centroids_b.distance(centroid_a)

    result = []
    for dist in distances:
        if distance_threshold is None or dist <= distance_threshold:
            result.append(round(dist / 1000))  # Convert to km
        else:
            result.append(None)
    return result


def get_valid_attrs(
    recs0: list,
    recs1: list,
    df_attr0: pd.DataFrame,
    attrs: list,
    config: dict,
    id_col: str = "div_id",
) -> pd.DataFrame:
    """Get valid attributes based on the first eligible receiver."""
    non_attr_cols = config.get("non_attr_cols", [])

    # Step 1: filter candidate receivers
    mask = (
        (~df_attr0["is_donor"])
        & (df_attr0[id_col].isin(recs0))
        & (~df_attr0[id_col].isin(recs1))
    )
    candidates = df_attr0.loc[mask]

    if candidates.empty:
        logger.warning("No matching receivers found.")
        return pd.DataFrame()

    # Step 2: take first valid receiver
    row = candidates.iloc[0]

    # Step 3: determine valid attributes (non-null)
    valid_attr_cols = [
        col for col in row.index if col not in non_attr_cols and pd.notna(row[col])
    ]

    # Step 4: combine with non-attribute columns
    selected_cols = non_attr_cols + valid_attr_cols

    # Step 5: filter to attributes used in this round
    selected_attrs = [col for col in selected_cols if col in attrs]
    excluded_attrs = [col for col in attrs if col not in selected_attrs]

    if selected_attrs:
        if excluded_attrs:
            logger.info(
                f"Excluding {len(excluded_attrs)} attributes: {','.join(excluded_attrs)}"
            )
        else:
            logger.info("Using all attributes")

    # Step 6: subset dataframe
    df_attr = df_attr0[selected_cols]

    # Step 7: drop rows with NA in required attributes
    required_attrs = [col for col in attrs if col not in excluded_attrs]
    df_attr = df_attr.dropna(subset=required_attrs)

    if df_attr.empty:
        logger.warning("No valid attributes found after filtering.")

    return df_attr


def apply_pca(data0: pd.DataFrame, min_var: float = 0.8) -> pd.DataFrame:
    """Apply Principal Component Analysis to the attributes."""
    # standardize the data
    scaled_data = StandardScaler().fit_transform(data0)

    # perform PCA given the required minimum total explained variance
    pca = PCA(min_var, svd_solver="auto", random_state=7777)
    pca.fit(scaled_data)
    n1 = pca.n_components_

    logger.info(f"Number of PCs selected: {n1}")
    logger.info(
        f"PCA total portion of variance explained ... {sum(pca.explained_variance_ratio_)}"
    )
    x_pca = pca.transform(scaled_data)

    # standardize the reduced data (comment out because it is not necessary)
    # x_pca = StandardScaler().fit_transform(x_pca)

    # convert to dataframe
    strs1 = ["pc"] * n1
    strs2 = list(map(str, list(range(1, n1 + 1))))
    cols = [i + j for i, j in zip(strs1, strs2)]
    x_pca = pd.DataFrame(x_pca, columns=cols)

    # weights for chosen PCs are proportional to the variances they explained
    w1 = pca.explained_variance_ratio_ / sum(pca.explained_variance_ratio_)

    # return scores and weights
    return x_pca, w1


def apply_donor_constraints(
    rec: str,
    donors: list,
    dists: pd.DataFrame,
    config: dict,
    df_attr: pd.DataFrame,
    id_col: str = "div_id",
) -> tuple:
    """Apply a few additional constraints to donors identified (e.g., via Gower's distance or other techniques)."""
    # 1. narrow down to donors with the same snowiness category
    # get receiver's snowiness
    try:
        snowy = df_attr.loc[df_attr[id_col] == rec, "snowy"].values[0]
    except IndexError:
        raise ValueError(f"Receiver '{rec}' not found in attribute dataframe.")

    # Get donor snowiness in same order as donor list
    try:
        donor_index = pd.Index(donors)
        donor_rows = df_attr.set_index(id_col).loc[donor_index]
    except KeyError as e:
        raise ValueError(f"Some donors not found in attribute dataframe: {e}")

    snowy1 = donor_rows["snowy"].values

    # Apply constraint
    ix1 = np.isin(snowy1, snowy)
    if ix1.sum() > 0:
        donors = donor_index[ix1].tolist()
        dists = np.array(dists)[ix1]

    # 2. further narrow down to those donors within maximum spatial distance defined
    ix1 = dists <= config["max_spa_dist"]
    if sum(ix1) > 0:
        dists = np.array(dists)[ix1]
        donors = np.array(donors)[ix1]

    return donors, dists


def assign_donors(
    scenario: str,
    donors: list,
    receivers: list,
    config: dict,
    dist_attr: pd.DataFrame,
    dist_spatial: pd.DataFrame,
    df_attr: pd.DataFrame,
    id_col: str = "div_id",
) -> pd.DataFrame:
    """Assign donors based on clusters and spatial distance and apply additional constrains."""
    df_donor = pd.DataFrame()
    for receiver in receivers:
        # get spatial distances
        dists1 = dist_spatial.loc[receiver, donors].to_numpy()
        donors1 = donors.copy()

        # apply additional donor constraints1
        if df_attr is not None:
            donors1, dists1 = apply_donor_constraints(
                receiver, donors1, dists1, config, df_attr, id_col
            )

        # if applicable, choose donor with the smallest attribute distances
        if dist_attr is not None:
            ix0 = [donors.index(i) for i in donors1]
            dist_attr = [dist_attr.iloc[i] for i in ix0]
            ix1 = np.argsort(dist_attr)[
                range(min(len(dist_attr), config["n_donor_max"]))
            ]
            dist_attr1 = np.array(dist_attr)[ix1]
            dists1 = dists1[ix1]
            donors1 = np.array(donors1)[ix1]

        # order donors by spatial distance
        ix1 = np.argsort(dists1)
        # dists1 = dists1.iloc[ix1]
        dists1 = dists1[ix1]
        donors1 = np.array(donors1)[ix1]

        # if the number of donors is greater than nDonorMax, ignore the additional donors
        nd_max = min(len(dists1), config["n_donor_max"])
        dists1 = dists1[range(nd_max)]
        donors1 = donors1[range(nd_max)]

        # add the donor/receiver pair to the pairing table
        if len(donors1) > 0:
            pair1 = {
                id_col: receiver,
                "tag": scenario,
                "donor": donors1[0],
                "distSpatial": dists1[0],
                "donors": ",".join(donors1),
                "distSpatials": ",".join(map(str, pd.Series(dists1))),
            }

            # add attribute distance if applicable (e.g., for Gower & URF)
            if dist_attr is not None:
                dist_attr1 = np.array(dist_attr1)[
                    ix1
                ]  # sort according to spatial distance
                dist_attr1 = dist_attr1[
                    range(nd_max)
                ]  # ignore unneeded donor (likely not necessary given the treatment above)
                pair1["distAttr"] = dist_attr1[0]
                pair1["distAttrs"] = ",".join(map(str, pd.Series(dist_attr1)))

            df_donor = pd.concat((df_donor, pd.DataFrame(pair1, index=[0])), axis=0)

    return df_donor
