from typing import Optional, Sequence, Union

import larq as lq
import tensorflow as tf
from zookeeper import ComponentField, Field, factory, task

from larq_zoo import utils
from larq_zoo.model_factory import ModelFactory
from larq_zoo.train import TrainLarqZooModel


@factory
class BiRealNetFactory(ModelFactory):
    """Implementation of [Bi-Real Net](https://arxiv.org/abs/1808.00278)"""

    filters: int = Field(64)

    input_quantizer = Field("approx_sign")
    kernel_quantizer = Field("magnitude_aware_sign")
    kernel_constraint = Field("weight_clip")

    kernel_initializer: Union[tf.keras.initializers.Initializer, str] = Field(
        "glorot_normal"
    )

    def residual_block(
        self, x, double_filters: bool = False, filters: Optional[int] = None
    ) -> tf.Tensor:
        assert not (double_filters and filters)

        # Compute dimensions
        in_filters = x.get_shape().as_list()[-1]
        out_filters = filters or in_filters if not double_filters else 2 * in_filters

        shortcut = x

        if in_filters != out_filters:
            shortcut = tf.keras.layers.AvgPool2D(2, strides=2, padding="same")(shortcut)
            shortcut = tf.keras.layers.Conv2D(
                out_filters,
                (1, 1),
                kernel_initializer=self.kernel_initializer,
                use_bias=False,
            )(shortcut)
            shortcut = tf.keras.layers.BatchNormalization(momentum=0.8)(shortcut)

        x = lq.layers.QuantConv2D(
            out_filters,
            (3, 3),
            strides=1 if out_filters == in_filters else 2,
            padding="same",
            input_quantizer=self.input_quantizer,
            kernel_quantizer=self.kernel_quantizer,
            kernel_initializer=self.kernel_initializer,
            kernel_constraint=self.kernel_constraint,
            use_bias=False,
        )(x)
        x = tf.keras.layers.BatchNormalization(momentum=0.8)(x)

        return tf.keras.layers.add([x, shortcut])

    def build(self) -> tf.keras.models.Model:
        # Layer 1
        out = tf.keras.layers.Conv2D(
            self.filters,
            (7, 7),
            strides=2,
            kernel_initializer=self.kernel_initializer,
            padding="same",
            use_bias=False,
        )(self.image_input)
        out = tf.keras.layers.BatchNormalization(momentum=0.8)(out)
        out = tf.keras.layers.MaxPool2D((3, 3), strides=2, padding="same")(out)

        # Layer 2
        out = self.residual_block(out, filters=self.filters)

        # Layer 3 - 5
        for _ in range(3):
            out = self.residual_block(out)

        # Layer 6 - 17
        for _ in range(3):
            out = self.residual_block(out, double_filters=True)
            for _ in range(3):
                out = self.residual_block(out)

        # Layer 18
        if self.include_top:
            out = tf.keras.layers.GlobalAvgPool2D()(out)
            out = tf.keras.layers.Dense(self.num_classes, activation="softmax")(out)

        model = tf.keras.Model(inputs=self.image_input, outputs=out, name="birealnet18")

        # Load weights.
        if self.weights == "imagenet":
            # Download appropriate file
            if self.include_top:
                weights_path = utils.download_pretrained_model(
                    model="birealnet",
                    version="v0.3.0",
                    file="birealnet_weights.h5",
                    file_hash="6e6efac1584fcd60dd024198c87f42eb53b5ec719a5ca1f527e1fe7e8b997117",
                )
            else:
                weights_path = utils.download_pretrained_model(
                    model="birealnet",
                    version="v0.3.0",
                    file="birealnet_weights_notop.h5",
                    file_hash="5148b61c0c2a1094bdef811f68bf4957d5ba5f83ad26437b7a4a6855441ab46b",
                )
            model.load_weights(weights_path)
        elif self.weights is not None:
            model.load_weights(self.weights)
        return model


def BiRealNet(
    *,  # Keyword arguments only
    input_shape: Optional[Sequence[Optional[int]]] = None,
    input_tensor: Optional[tf.Tensor] = None,
    weights: Optional[str] = "imagenet",
    include_top: bool = True,
    num_classes: int = 1000,
) -> tf.keras.models.Model:
    """Instantiates the Bi-Real Net architecture.
    Optionally loads weights pre-trained on ImageNet.
    ```netron
    birealnet-v0.3.0/birealnet.json
    ```
    ```plot-altair
    /plots/birealnet.vg.json
    ```
    # Arguments
    input_shape: optional shape tuple, only to be specified if `include_top` is False,
        otherwise the input shape has to be `(224, 224, 3)`.
        It should have exactly 3 inputs channels.
    input_tensor: optional Keras tensor (i.e. output of `layers.Input()`) to use as
        image input for the model.
    weights: one of `None` (random initialization), "imagenet" (pre-training on
        ImageNet), or the path to the weights file to be loaded.
    include_top: whether to include the fully-connected layer at the top of the network.
    num_classes: optional number of classes to classify images into, only to be
        specified if `include_top` is True, and if no `weights` argument is specified.
    # Returns
    A Keras model instance.
    # Raises
    ValueError: in case of invalid argument for `weights`, or invalid input shape.
    # References
    - [Bi-Real Net: Enhancing the Performance of 1-bit CNNs With Improved
      Representational Capability and Advanced Training
      Algorithm](https://arxiv.org/abs/1808.00278)
    """
    return BiRealNetFactory(
        include_top=include_top,
        weights=weights,
        input_tensor=input_tensor,
        input_shape=input_shape,
        num_classes=num_classes,
    ).build()


@task
class TrainBiRealNet(TrainLarqZooModel):
    model = ComponentField(BiRealNetFactory)

    epochs = Field(300)
    batch_size = Field(512)

    learning_rate: float = Field(5e-3)
    decay_schedule: str = Field("linear")

    @Field
    def optimizer(self):
        if self.decay_schedule == "linear_cosine":
            lr = tf.keras.experimental.LinearCosineDecay(self.learning_rate, 750684)
        elif self.decay_schedule == "linear":
            lr = tf.keras.optimizers.schedules.PolynomialDecay(
                self.learning_rate, 750684, end_learning_rate=0, power=1.0
            )
        else:
            lr = self.learning_rate
        return tf.keras.optimizers.Adam(lr)
