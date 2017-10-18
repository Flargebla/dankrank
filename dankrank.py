from DankSucc import DankSucc
from PIL import Image
import numpy as np
import tensorflow as tf

# Succ all the memes
succr = DankSucc("me_irl")
succr.succ()
succr.persist()

# Normalize the images
print("Number of danks(pre):",str(len(succr.grab_danks())))
for d in succr.grab_danks():
    dank_dir = "danks/"
    try:
        img = Image.open(dank_dir+d.filename)
        img = img.resize((64,64))
        img.save(dank_dir+d.filename, d.filetype)
    except PermissionError:
        print("PermissionError, Failed to open:",dank_dir+d.filename)
        succr.kill_dank(d)
    except OSError:
        print("OSError, Invalid image format:",dank_dir+d.filename) 
        succr.kill_dank(d)
print("Number of danks(post):",str(len(succr.grab_danks())))

# Feed memes into the CNN
def cnn_model_fn(features, labels, mode):
    i_layer = tf.reshape(features["x"], [-1,64,64,3])
    conv1 = tf.layers.conv2d(inputs=i_layer,
                             filters=32,
                             kernel_size=[5,5],
                             padding="same",
                             activation=tf.nn.relu)
    pool1 = tf.layers.max_pooling2d(inputs=conv1,
                                    pool_size=[2,2],
                                    strides=2)
    conv2 = tf.laters.conv2d(inputs=pool1,
                             filters=64,
                             kernel_size=[5,5],
                             padding="same",
                             activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2d(inputs=conv2,
                                    pool_size=[2,2],
                                    strides=2)
    pool2flat = tf.reshape(pool2, [-1,7*7*64])
    dense = tf.layers.dense(inputs=pool2_flat,
                            units=1024,
                            activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense,
                                rate=0.4,
                                training=mode == tf.estimator.ModeKeys.TRAIN)
    output = tf.layers.dense(inputs=dropout,
                             units=1)
    predictions = {
        "output" : output
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.mean_squared_error(labels=labels, predictions=output)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(loss=loss,
                                      global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    

    return tf.estimator.EstimatorSpec(mode=mode,
                                      loss=loss)
def main(unused_argv):
    # Define the memes
    train_data = np.array([np.array(Image.open("danks/"+d.filename)) for d in succr.grab_danks() if "." in d.filename])
    train_labels = np.array([d.score for d in succr.grab_danks()])

    if len(train_data) > len(train_labels):
        while len(train_data) != len(train_labels):
            train_data = train_data[:-1]
    elif len(train_labels) > len(train_data):
        while len(train_labels) != len(train_data):
            train_labels = train_labels[:-1]
    
    # Create the Estimator
    mnist_classifier = tf.estimator.Estimator(
        model_fn=cnn_model_fn, model_dir="model/mnist_convnet_model")


    # Train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True)

    mnist_classifier.train(
        input_fn=train_input_fn,
        steps=20000)

# Start it
if __name__ == "__main__":
    tf.app.run()
