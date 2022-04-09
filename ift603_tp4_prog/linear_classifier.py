###
#   Eliott THOMAS         —  21 164 874
#   Lilian FAVRE GARCIA   —  21 153 421
#   Tsiory Razafindramisa —  21 145 627
###


import numpy as np


class LinearClassifier(object):
    def __init__(self, x_train, y_train, x_val, y_val, num_classes, bias=False):
        self.x_train = x_train
        self.y_train = y_train
        self.x_val = x_val
        self.y_val = y_val
        self.bias = bias  # when bias is True then the feature vectors have an additional 1

        num_features = x_train.shape[1]
        if bias:
            num_features += 1

        self.num_features = num_features
        self.num_classes = num_classes
        self.W = self.generate_init_weights(0.01)

    def generate_init_weights(self, init_scale):
        return np.random.randn(self.num_features, self.num_classes) * init_scale

    def train(self, num_epochs=1, lr=1e-3, l2_reg=1e-4, lr_decay=1.0, init_scale=0.01):
        """
        Train the model with a cross-entropy loss
        Naive implementation (with loop)

        Inputs:
        - num_epochs: the number of training epochs
        - lr: learning rate
        - l2_reg: the l2 regularization strength
        - lr_decay: learning rate decay.  Typically a value between 0 and 1
        - init_scale : scale at which the parameters self.W will be randomly
        initialized

        Returns a tuple for:
        - training accuracy for each epoch
        - training loss for each epoch
        - validation accuracy for each epoch
        - validation loss for each epoch
        """
        loss_train_curve = []  # training loss for each epoch
        loss_val_curve = []  # validation loss for each epoch
        accu_train_curve = []  # training accuracy for each epoch
        accu_val_curve = []  # validation accuracy for each epoch

        self.W = self.generate_init_weights(init_scale)  # type: np.ndarray

        sample_idx = 0  # sample index
        num_iter = num_epochs * len(self.x_train)  # number of iterations
        for i in range(num_iter):
            # Take a sample
            x_sample = self.x_train[sample_idx]
            y_sample = self.y_train[sample_idx]
            if self.bias:  # augment the sample with a bias
                x_sample = augment(x_sample)

            # Compute loss and gradient of loss
            loss_train, dW = self.cross_entropy_loss(x_sample, y_sample, reg=l2_reg)  # loss and gradient of loss

            # Take gradient step
            self.W -= lr * dW  # update the weights

            # Advance in data
            sample_idx += 1  # advance in the training set
            if sample_idx >= len(self.x_train):  # End of epoch
                accu_train, loss_train = self.global_accuracy_and_cross_entropy_loss(self.x_train, self.y_train, l2_reg)  # compute training accuracy and loss
                accu_val, loss_val, = self.global_accuracy_and_cross_entropy_loss(self.x_val, self.y_val, l2_reg)  # compute validation accuracy and loss

                loss_train_curve.append(loss_train)
                loss_val_curve.append(loss_val)

                accu_train_curve.append(accu_train)
                accu_val_curve.append(accu_val)

                sample_idx = 0  # restart the sample index
                lr *= lr_decay  # decay the learning rate

        return loss_train_curve, loss_val_curve, accu_train_curve, accu_val_curve

    def predict(self, X):
        """
        return the class label with the highest class score i.e.

            argmax_c W.X

         X: A numpy array of shape (D,) containing one or many samples.

         Returns a class label for each sample (a number between 0 and
         num_classes-1)
        """
        #############################################################################
        # TODO: Return the best class label.                                        #
        #############################################################################
        class_label = np.zeros(X.shape[0])

        if self.bias:  # augment the sample with a bias
            X = augment(X)

        predictions = X@self.W   # bias in included
        class_label = np.argmax(predictions, axis=1)

        return class_label
        #############################################################################
        #                          END OF YOUR CODE                                 #
        #############################################################################

    def global_accuracy_and_cross_entropy_loss(self, X, y, reg=0.0):
        """
        Compute average accuracy and cross_entropy for a series of N data
        points.
        Naive implementation (with loop)
        Inputs:
        - X: A numpy array of shape (D, N) ----> (N,D) ? containing many
        samples.
        - y: A numpy array of shape (N) labels as an integer
        - reg: (float) regularization strength
        Returns a tuple of:
        - average accuracy as single float
        - average loss as single float
        """
        #############################################################################
        # TODO: Compute the softmax loss & accuracy for a series of samples X,y .   #
        #############################################################################
        accu = 0
        loss = 0

        # cross entropy
        for i in range(X.shape[0]):
            cross = self.cross_entropy_loss(X[i], y[i], reg)
            loss += cross[0]

        labels = self.predict(X)
        accu = np.mean(labels == y)

        # Normalisation
        loss /= X.shape[0]

        return (accu, loss)
        #############################################################################
        #                          END OF YOUR CODE                                 #
        #############################################################################

    def cross_entropy_loss(self, x, y, reg=0.0):
        """
        Cross-entropy loss function for one sample pair (X,y) (with softmax)
        C.f. Eq.(4.104 to 4.109) of Bishop book.

        Input have dimension D, there are C classes.
        Inputs:
        - W: A numpy array of shape (D, C) containing weights.
        - x: A numpy array of shape (D,) containing one sample.
        - y: training label as an integer
        - reg: (float) regularization strength
        Returns a tuple of:
        - loss as single float
        - gradient with respect to weights W; an array of same shape as W
        """
        # Initialize the loss and gradient to zero.
        loss = 0.0
        dW = np.zeros_like(self.W)  # initialize the gradient as zero

        #############################################################################
        # TODO: Compute the softmax loss and its gradient.                          #
        # Store the loss in loss and the gradient in dW.                            #
        # 1- Compute softmax => eq.(4.104) or eq.(5.25) Bishop                      #
        # 2- Compute cross-entropy loss => eq.(4.108)                               #
        # 3- Dont forget the regularization!                                        #
        # 4- Compute gradient => eq.(4.109)                                         #
        #############################################################################

        if self.bias:  # augment the sample with a bias
            if x[-1] != 1:  # if the bias is not already in the sample
                x = augment(x)

        predictions = x@self.W   # bias in included

        # Softmax
        predictions = np.exp(predictions)
        Sum = np.sum(predictions)
        predictions[:] /= Sum

        # CrossEntropy
        for i in range(len(predictions)):  # for each class
            # loss
            tnk = int(y == i)  # 1 if y == i, 0 otherwise
            loss -= tnk*np.log(predictions[i])  # eq.(4.108)

            # gradient
            err = (predictions[i]-tnk)

            # we apply the regularization to the gradient
            dW[:, i] = np.dot(x, err) + reg*self.W[:, i]  # eq.(4.109)        

        # Regularisation
        loss += 0.5 * reg * np.sum(np.power(self.W, 2))

        return loss, dW
        #############################################################################
        #                          END OF YOUR CODE                                 #
        #############################################################################


def augment(x):
    if len(x.shape) == 1:
        return np.concatenate([x, [1.0]])
    else:
        return np.concatenate([x, np.ones((len(x), 1))], axis=1)
