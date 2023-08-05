import tensorflow.keras as keras
import tensorflow.keras.backend as K
import numpy as np
import tensorflow as tf

import fsph
import fsph.tf_ops


def _xyz_to_phitheta(xyz):
    r = tf.linalg.norm(xyz, axis=-1)
    phi = tf.math.acos(K.clip(xyz[..., 2]/r, -1, 1))
    theta = tf.math.atan2(xyz[..., 1], xyz[..., 0])

    phitheta = K.stack([phi, theta], -1)
    return phitheta


class SphericalHarmonics(keras.layers.Layer):
    """Compute the (complex) spherical harmonic decomposition given a set of cartesian coordinates

    For an input of shape `(..., 3)`, `SphericalHarmonics` will
    produce an output of shape `(..., num_sphs)`, where `num_sphs` is
    the number of spherical harmonics produced given the `lmax` and
    `negative_m` arguments.

    :param lmax: maximum spherical harmonic degree to compute
    :param negative_m: If True, consider m=-l to m=l for each spherical harmonic l; otherwise, consider m=0 to m=l
    """ # noqa
    def __init__(self, lmax, negative_m=False, **kwargs):
        self.lmax = int(lmax)
        self.negative_m = bool(negative_m)

        self.num_sphs = len(fsph.get_LMs(self.lmax, self.negative_m))

        super().__init__(**kwargs)

    def build(self, input_shape):
        assert input_shape[-1] == 3, 'SphericalHarmonics must take an array of (x, y, z) values'
        super().build(input_shape)

    def call(self, xyz):
        self.diagonal_phitheta = _xyz_to_phitheta(xyz)
        self.spherical_harmonics = fsph.tf_ops.spherical_harmonic_series(
            self.diagonal_phitheta, self.lmax, self.negative_m)

        symbolic_shape = K.shape(self.spherical_harmonics)
        shape = K.int_shape(self.spherical_harmonics)[:-1]
        full_shape = ([v if v is not None else symbolic_shape[i] for (i, v) in enumerate(shape)] +
                      [self.num_sphs])
        self.spherical_harmonics = K.reshape(self.spherical_harmonics, full_shape)

        return self.spherical_harmonics

    def compute_output_shape(self, input_shape):
        # (..., 3) -> (..., num_sphs)
        shape = list(input_shape)
        shape[-1] = self.num_sphs
        return tuple(shape)

    def get_config(self):
        config = super().get_config()
        config.update(dict(lmax=self.lmax,
                           negative_m=self.negative_m))
        return config


class NeighborAverage(keras.layers.Layer):
    """Compute a weighted average an array of complex-valued spherical harmonics over all points in a neighborhood

    Given an input of shape `(..., num_rotations, num_neighbors,
    num_sphs)`, `NeighborAverage` will produce an output of shape
    `(..., num_rotations, num_sphs)`. Each neighbor from each rotation
    is assigned a learnable weight to contribute to the sum.
    """ # noqa
    def build(self, input_shape):
        # (rotations, neighbors)
        shape = (input_shape[-3], input_shape[-2],)
        weight_scale = 1.0/input_shape[-2]
        self.neighbor_weights = self.add_weight(
            'neighbor_weights', shape, trainable=True,
            initializer=keras.initializers.RandomUniform(-weight_scale, weight_scale))

        self.times_to_expand = len(input_shape) - 3

        super().build(input_shape)

    def call(self, inputs):
        neighbor_weights_expanded = K.expand_dims(self.neighbor_weights, -1)

        for _ in range(self.times_to_expand):
            neighbor_weights_expanded = K.expand_dims(neighbor_weights_expanded, 0)

        self.neighbor_sum = K.sum(inputs*K.cast(neighbor_weights_expanded, tf.complex64), -2)
        return self.neighbor_sum

    def compute_output_shape(self, input_shape):
        # (..., num_neighbors, num_sphs) -> (..., num_sphs)
        shape = list(input_shape)
        shape.pop(-2)
        return tuple(shape)


class ComplexProjection(keras.layers.Layer):
    """Compute one or more linear projections of a complex-valued function

    Given an input of shape `(..., num_rotations, num_sphs)`,
    `ComplexProjection` produces an output of shape `(..,
    num_rotations, num_projections)`.

    Outputs are converted to real numbers by taking the absolute value
    of the projection output by default, but the real or imaginary
    components can also be taken instead.

    :param num_projections: Number of projections (i.e. number of neurons) to create for each rotation
    :param conversion: Method to make the projection output real: 'abs' (absolute value), 'angle' (complex phase), 'real' (real component), 'imag' (imaginary component), or a comma-separated list of these values (i.e. 'real,imag')
    :param activation: Keras activation function for the layer
    :param kernel_initializer: Keras initializer for the projection weights matrix
    :param bias_initializer: Keras initializer for the projection bias matrix
    """ # noqa
    def __init__(self, num_projections=1, conversion='abs', activation=None,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='random_normal', **kwargs):
        self.num_projections = int(num_projections)
        self.conversion = conversion
        self.activation = keras.activations.get(activation)
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer

        super().__init__(**kwargs)

    def build(self, input_shape):
        # (rotations, spherical_harmonics, projections)
        shape = (input_shape[-2], input_shape[-1], self.num_projections)
        self.projection = self.add_weight(
            'projection', shape, trainable=True,
            initializer=keras.initializers.get(self.kernel_initializer))
        num_conversions = len(self.conversion.split(','))
        # (rotations, projections*conversions)
        bias_shape = (input_shape[-2], self.num_projections*num_conversions)
        self.bias = self.add_weight(
            'bias', bias_shape, trainable=True,
            initializer=keras.initializers.get(self.bias_initializer))

        for _ in range(len(shape), len(input_shape)):
            self.projection = K.expand_dims(self.projection, 0)

        super().build(input_shape)

    def call(self, inputs):
        # inputs::(..., rotations, spherical_harmonics)
        self.sph_projected = K.sum(
            K.expand_dims(inputs, -1)*K.cast(self.projection, tf.complex64), -2)

        conversions = self.conversion.split(',')
        result = []
        for conversion in conversions:
            conversion = conversion.strip()
            if conversion == 'abs':
                result.append(K.abs(self.sph_projected))
            elif conversion == 'angle':
                result.append(tf.math.angle(self.sph_projected))
            elif conversion == 'real':
                result.append(tf.math.real(self.sph_projected))
            elif conversion == 'imag':
                result.append(tf.math.imag(self.sph_projected))
            else:
                raise NotImplementedError('Unknown conversion {}'.format(conversion))

        if len(conversions) > 1:
            self.projected = K.stack(result, -1)
            int_shape = K.int_shape(self.projected)
            new_shape = [v if v else -1 for v in int_shape[:-2]] + [int_shape[-2]*int_shape[-1]]
            self.projected = K.reshape(self.projected, new_shape)
        else:
            self.projected = result[0]

        return self.activation(self.projected + self.bias)

    def compute_output_shape(self, input_shape):
        # (..., num_sphs) -> (..., num_projections)
        shape = list(input_shape)
        shape[-1] = self.num_projections*len(self.conversion.split(','))
        return tuple(shape)

    def get_config(self):
        config = super().get_config()
        config.update(dict(
            num_projections=self.num_projections,
            conversion=self.conversion,
            activation=keras.activations.serialize(self.activation),
            kernel_initializer=keras.initializers.serialize(self.kernel_initializer),
            bias_initializer=keras.initializers.serialize(self.bias_initializer),
        ))
        return config


class ComplexDropout(keras.layers.Dropout):
    """Dropout layer for complex outputs.

    Randomly sets the given fraction of inputs to 0 during
    training. This layer is specialized to work for complex values,
    since the standard dropout layer in keras only works for
    floating-point values. Interface is identical to
    :py:class:`keras.layers.Dropout`.

    """ # noqa
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            noise_shape = K.int_shape(inputs)
        else:
            noise_shape = self.noise_shape

        symbolic_shape = K.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape
                       for axis, shape in enumerate(noise_shape)]
        return tuple(noise_shape)

    def call(self, inputs, training=None):
        if 0. < self.rate < 1.:
            noise_shape = self._get_noise_shape(inputs)

            def dropped_inputs():
                seed = self.seed
                if seed is None:
                    seed = np.random.randint(10e6)

                # filt indicates where to pass values through
                filt = K.random_uniform(noise_shape, seed=seed) > self.rate
                scale_and_filt = K.cast(filt, tf.complex64)/(1 - self.rate)

                return inputs*scale_and_filt

            return K.in_train_phase(dropped_inputs, inputs,
                                    training=training)
        return inputs
