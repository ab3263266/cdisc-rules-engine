from cdisc_rules_engine.models.dataset import PandasDataset


class DataReaderInterface:
    """
    Interface for reading binary data from different file typs into pandas dataframes
    """

    def __init__(self, dataset_class=PandasDataset):
        """
        :param dataset_class DatasetInterface: The dataset type to return.
        """
        self.dataset_class = dataset_class

    def read(self, data):
        """
        Function for reading data from a specific file type and returning a
        pandas dataframe of the data.
        """
        raise NotImplementedError

    def from_file(self, file_path):
        raise NotImplementedError
