import unittest
import numpy as np

from sklearn.datasets import load_iris
from sklearn.metrics import confusion_matrix

from unittest.mock import patch

from annotlib.standard import StandardAnnot
from annotlib.base import BaseAnnot


class TestBaseAnnot(unittest.TestCase):

    def setUp(self):
        self.X, self.y_true = load_iris(return_X_y=True)
        self.C = np.random.uniform(0, 1, len(self.X)*3).reshape((len(self.X), 3))
        self.y_missing = np.full(len(self.X), np.nan)
        self.annot = StandardAnnot(X=self.X, Y=np.array([self.y_true, self.y_true, self.y_missing]).T, C=self.C)

    @patch.multiple(BaseAnnot, __abstractmethods__=set())
    def test_interface(self):
        base_annot = BaseAnnot()
        base_annot.n_annotators()
        base_annot.n_queries()
        base_annot.queried_samples()
        base_annot.class_labels(X=None, annotator_ids=None, query_value=None)
        base_annot.confidence_scores(X=None, annotator_ids=None)

    def test_labelling_performance(self):
        # test accuracy as default measure of labelling performance
        accuracies = self.annot.labelling_performance(X=self.X, y_true=self.y_true)
        np.testing.assert_array_equal([1, 1, np.nan], accuracies)

        # test confusion matrix as measure of labelling performance
        conf_matrices = self.annot.labelling_performance(X=self.X, y_true=self.y_true, perf_func=confusion_matrix)
        correct_matrix = np.array([[50, 0, 0],
                                   [0, 50, 0],
                                   [0, 0, 50]])
        self.assertEqual(len(conf_matrices), self.annot.n_annotators())
        np.testing.assert_array_equal(correct_matrix, conf_matrices[0])
        np.testing.assert_array_equal(correct_matrix, conf_matrices[1])
        np.testing.assert_array_equal(np.nan, conf_matrices[2])

    def test_plot_labelling_accuracy(self):
        # test wrong annotator ids
        self.assertRaises(ValueError, self.annot.plot_labelling_accuracy, self.X, self.y_true, [-1])

        # test correct annotator ids
        fig, ax = self.annot.plot_labelling_accuracy(X=self.X, y_true=self.y_true, figsize=(5, 5))
        self.assertEqual(5, fig.get_figheight())
        self.assertEqual(5, fig.get_figwidth())
        np.testing.assert_array_equal([0, 1, 2], ax.get_xticks())

    def test_plot_labelling_confusion_matrices(self):
        # test wrong annotator ids
        self.assertRaises(ValueError, self.annot.plot_labelling_confusion_matrices, self.X, self.y_true,
                          np.unique(self.y_true), [-1])

        # test correct annotator ids
        fig, ax = self.annot.plot_labelling_confusion_matrices(X=self.X, y_true=self.y_true,
                                                               y_unique=np.unique(self.y_true), figsize=(5,5))
        self.assertEqual(5, fig.get_figwidth())
        self.assertEqual(5*self.annot.n_annotators(), fig.get_figheight())
        self.assertEqual(self.annot.n_annotators(), len(ax))

    def test_plot_class_labels(self):
        # test wrong annotator ids
        self.assertRaises(ValueError, self.annot.plot_class_labels, self.X, None, [-1])

        # test wrong feature ids
        self.assertRaises(ValueError, self.annot.plot_class_labels, self.X, [-1])

        # test different options of correct usage
        fig, ax = self.annot.plot_class_labels(X=self.X, y_true=self.y_true, plot_confidences=True,
                                               figsize=(5, 5))
        self.assertEqual(5, fig.get_figwidth())
        self.assertEqual(self.annot.n_annotators() * 5, fig.get_figheight())
        self.assertEqual(self.annot.n_annotators(), len(ax))

        fig, ax = self.annot.plot_class_labels(X=self.X, y_true=None, plot_confidences=True,
                                               figsize=(5, 5))
        self.assertEqual(5, fig.get_figwidth())
        self.assertEqual(self.annot.n_annotators() * 5, fig.get_figheight())
        self.assertEqual(self.annot.n_annotators(), len(ax))

        fig, ax = self.annot.plot_class_labels(X=self.X, y_true=self.y_true, plot_confidences=False,
                                               figsize=(5, 5))
        self.assertEqual(5, fig.get_figwidth())
        self.assertEqual(self.annot.n_annotators() * 5, fig.get_figheight())
        self.assertEqual(self.annot.n_annotators(), len(ax))

        fig, ax = self.annot.plot_class_labels(X=self.X, y_true=self.y_true, plot_confidences=True, features_ids=[0],
                                               figsize=(5, 5))
        self.assertEqual(5, fig.get_figwidth())
        self.assertEqual(self.annot.n_annotators() * 5, fig.get_figheight())
        self.assertEqual(self.annot.n_annotators(), len(ax))


if __name__ == '__main__':
    unittest.main()
