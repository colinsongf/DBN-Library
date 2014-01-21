import unittest
from dbnlib.dbn import DBN
from dbnlib.rbm import RBM

class TestDBN(unittest.TestCase):
    # DBN tests
    def test_one_layer_constructor(self):
        layer_sizes = [10]
        d = DBN(layer_sizes, 1)

    def test_negative_dimension_constructor(self):
        layer_sizes = [-10, 500]
        with self.assertRaises(ValueError):
            d = DBN(layer_sizes, 1)

    def test_empty_config_constructor(self):
        layer_sizes = []
        with self.assertRaises(IndexError):
            d = DBN(layer_sizes, 1)

    def test_number_layers_setup_correct(self):
        # Test that the number of layers corrosponds to the number of RBMs given
        # in the initial config. In this example there are 3 layers / RBMs because
        # the stacked RBMs share indivdual layers, so the first RBM is 144, 50.
        # The second is 50, 50 etc.
        layer_sizes = [144, 50, 50, 2000]
        d = DBN(layer_sizes, 1)
        self.assertEquals(d.number_layers, 3)

    def test_number_inputs_setup_correct(self):
        # The first layer in the layer sizes corrosponds to the inputs.
        layer_sizes = [144, 50, 50, 2000]
        d = DBN(layer_sizes, 1)
        self.assertEquals(d.number_inputs, 144)

    def test_rbms_list_setup_correct(self):
        layer_sizes = [144, 50, 50, 2000]
        d = DBN(layer_sizes, 1)
        self.assertEquals(len(d._rbms), d.number_layers)

    def test_get_topology_constructs(self):
        # get_topology should return the layer_sizes with the number of labels
        # on the end of the list.
        layer_sizes = [144, 50, 50, 2000]
        number_labels = 1
        d = DBN(layer_sizes, number_labels)
        layer_sizes.append(number_labels)
        self.assertListEqual(d.get_topology(), layer_sizes)

    def test_pre_train_correct_data_size(self):
        layer_sizes = [5, 20, 10]
        d = DBN(layer_sizes, 10)
        data = [[1,1,1,1,1], [1,1,1,1,1]]
        d.pre_train(data, 1 , 1)

    def test_pre_train_wrong_data_size(self):
        layer_sizes = [5, 20]
        d = DBN(layer_sizes, 10)
        data = [[1,1,1,1,1,1,1]]
        with self.assertRaises(ValueError):
            d.pre_train(data, 1, 1)

    def test_pre_train_negative_batch(self):
        layer_sizes = [5, 20, 10]
        d = DBN(layer_sizes, 10)
        data = [[1,1,1,1,1], [1,1,1,1,1]]
        with self.assertRaises(ValueError):
            d.pre_train(data, 1 , -1)

    def test_train_labels(self):
        layer_sizes = [5, 20, 10]
        d = DBN(layer_sizes, 2)
        data = [[1,1,1,1,1], [1,1,1,1,1]]
        labels = [[1,0], [0,1]]
        d.train_labels(data, labels, 1, 1)

    def test_train_labels_wrong_label_size(self):
        layer_sizes = [5, 20, 10]
        d = DBN(layer_sizes, 2)
        data = [[1,1,1,1,1], [1,1,1,1,1]]
        labels = [[1,0], [0,1,1]]
        with self.assertRaises(ValueError):
            d.train_labels(data, labels, 1, 1)

    def test_train_labels_no_labels(self):
        layer_sizes = [5, 20, 10]
        d = DBN(layer_sizes, 2)
        data = [[1,1,1,1,1], [1,1,1,1,1]]
        labels = []
        with self.assertRaises(ValueError):
            d.train_labels(data, labels, 1, 1)