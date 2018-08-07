from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch
import unittest
from gpytorch.means import ConstantMean, ZeroMean, MultitaskMean


class TestMultitaskMean(unittest.TestCase):
    def setUp(self):
        self.mean = MultitaskMean(
            [ConstantMean(), ZeroMean(), ZeroMean(), ConstantMean()], n_tasks=4
        )
        self.mean.base_means[0].constant.data.fill_(5)
        self.mean.base_means[3].constant.data.fill_(7)

    def test_forward(self):
        a = torch.Tensor([[1, 2], [2, 4]])
        res = self.mean(a)
        self.assertEqual(tuple(res.size()), (2, 4))
        self.assertTrue(res[:, 0].eq(5).all())
        self.assertTrue(res[:, 1].eq(0).all())
        self.assertTrue(res[:, 2].eq(0).all())
        self.assertTrue(res[:, 3].eq(7).all())

    def test_forward_batch(self):
        a = torch.Tensor([[[1, 2], [1, 2], [2, 4]], [[2, 3], [2, 3], [1, 3]]])
        res = self.mean(a)
        self.assertEqual(tuple(res.size()), (2, 3, 4))
        self.assertTrue(res[:, :, 0].eq(5).all())
        self.assertTrue(res[:, :, 1].eq(0).all())
        self.assertTrue(res[:, :, 2].eq(0).all())
        self.assertTrue(res[:, :, 3].eq(7).all())


class TestMultitaskMeanSameMean(unittest.TestCase):
    def setUp(self):
        self.mean = MultitaskMean(ZeroMean(), n_tasks=4)

    def test_forward(self):
        a = torch.Tensor([[1, 2], [2, 4]])
        res = self.mean(a)
        self.assertEqual(tuple(res.size()), (2, 4))
        self.assertTrue(res.eq(0).all())

    def test_forward_batch(self):
        a = torch.Tensor([[[1, 2], [1, 2], [2, 4]], [[2, 3], [2, 3], [1, 3]]])
        res = self.mean(a)
        self.assertEqual(tuple(res.size()), (2, 3, 4))
        self.assertTrue(res.eq(0).all())
