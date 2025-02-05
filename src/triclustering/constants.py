import yaml as yy
from yaml.loader import Loader


def get_config(config_file):
    s = open(config_file, 'r')
    cfs = yy.load(s, Loader=Loader)
    globals().update(cfs)

    global BASELINE_DIR_S
    global BASELINE_DIR_T
    global TAB_DIR
    global TRICLUSTERS_DIR
    global BICLUSTERS_DIR
    global MATRICES_DIR_T
    global MATRICES_DIR_S
    global RESULTS_DIR
    global RESULTS_BASELINE_DIR
    global RESULTS_DIR_TRIC
    global TRAJECTORY_DIR
    global VISUALIZATION_DIR
    global TOP_FOLDER # output folder path
    global DATA_FILE # csv file containing data
    global MIN_APP # minimum number of appointments
    global SNAPSHOTS_FILE
    global N_CLUST # number of clusters
    global REF_FEATURE # feature to identify each patient (patient_id)
    global INCLUDE_STATIC # boolean : True if we include static data, False otherwise

    BASELINE_DIR_S = TOP_FOLDER + "baselines/static/"
    BASELINE_DIR_T = TOP_FOLDER + "baselines/temporal/"

    TAB_DIR = TOP_FOLDER + "tab_files/"
    TRICLUSTERS_DIR = TOP_FOLDER + "triclusters/"
    BICLUSTERS_DIR = TOP_FOLDER + "biclusters/"

    MATRICES_DIR_T = TOP_FOLDER + "matrices/trics/"
    MATRICES_DIR_S = TOP_FOLDER + "matrices/bics/"

    RESULTS_DIR = TOP_FOLDER + "results/bictric/"
    RESULTS_DIR_TRIC = TOP_FOLDER + "results/tric-based/"

    RESULTS_BASELINE_DIR = TOP_FOLDER + "results/baseline/"

    TRAJECTORY_DIR = TOP_FOLDER + "trajectories/"
    VISUALIZATION_DIR = TOP_FOLDER + "visualization/"
