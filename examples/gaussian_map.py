#!/usr/bin/env python
"""
Probability model
    Posterior: (1-dimensional) Gaussian
Variational model
    Likelihood: Mean-field Gaussian
"""
import tensorflow as tf
import blackbox as bb

from blackbox.stats import norm
from blackbox.util import get_dims
from blackbox.models import PythonModel

class Gaussian(PythonModel):
    """
    p(x, z) = p(z) = p(z | x) = Gaussian(z; mu, Sigma)
    """
    def __init__(self, mu, Sigma):
        self.mu = mu
        self.Sigma = Sigma
        #self.num_vars = get_dims(mu)[0]
        self.num_vars = 1

    def log_prob(self, xs, zs):
        log_prior = tf.pack([norm.logpdf(z, mu, Sigma)
                        for z in tf.unpack(zs)])
        # log_lik = tf.pack([
        #     tf.reduce_sum(norm.logpdf(x, zs[:,0], Sigma)) \
        #     for x in tf.unpack(xs)])
        log_lik = tf.pack([
            tf.reduce_sum(norm.logpdf(xs, z, 0*xs+Sigma)) \
            for z in tf.unpack(zs)])
        return log_lik + log_prior

bb.set_seed(42)
mu = tf.constant(3.0)
Sigma = tf.constant(0.1)
model = Gaussian(mu, Sigma)
data = bb.Data(tf.constant((3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0, 1, 0, 0, 0, 0, 0, 0, 0, 1), dtype=tf.float32))
variational = bb.PMGaussian(1)
inference = bb.MAP(model,variational,data)
#variational = bb.MFGaussian(1)
#inference = bb.MFVI(model,variational,data)
inference.run(n_iter=1000)
