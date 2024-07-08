import time
import datetime
import numpy as np
import os
import functools

class CleanEeg:
    def __init__(self, algorithm):
        """
        Function: Class object to clean EEG signal
        Argument:
            algorithm: type str. Defines the algorithm to be used to clean the EEG signal. Acceptable input are:
                'iCanClean': iCanClean algorithm from https://arxiv.org/ftp/arxiv/papers/2201/2201.11798.pdf
        """
        self.algorithm = algorithm
       
        
    def calculate_cca(self, dat_x, dat_y, time_axis=0):
        r"""
        Calculate the Canonical Correlation Analysis (CCA).
        This method calculates the canonical correlation coefficient and
        corresponding weights which maximize a correlation coefficient
        between linear combinations of the two specified multivariable
        signals.
        Args:
            dat_x : continuous Data object
                these data should have the same length on the time axis.
            dat_y : continuous Data object
                these data should have the same length on the time axis.
            time_axis : int, optional
                the index of the time axis in ``dat_x`` and ``dat_y``.
        Returns:
            rho : float
                the canonical correlation coefficient.
            w_x, w_y : 1d array
                the weights for mapping from the specified multivariable signals
                to canonical variables.
        Raises:
            AssertionError :
                If:
                    * ``dat_x`` and ``dat_y`` is not continuous Data object
                    * the length of ``dat_x`` and ``dat_y`` is different on the
                      ``time_axis``
        Dependencies:
            functools : functools package
            np : numpy package
        Reference:
            https://github.com/venthur/wyrm/blob/master/wyrm/processing.py
            http://en.wikipedia.org/wiki/Canonical_correlation
        """
        x = dat_x
        y = dat_y

        # calculate covariances and it's inverses
        x -= x.mean(axis=0)
        y -= y.mean(axis=0)
        n = x.shape[0]
        c_xx = np.dot(x.T, x) / n
        c_yy = np.dot(y.T, y) / n
        c_xy = np.dot(x.T, y) / n
        c_yx = np.dot(y.T, x) / n
        ic_xx = np.linalg.pinv(c_xx)
        ic_yy = np.linalg.pinv(c_yy)
        
        # calculate w_x
        w, v = np.linalg.eig(functools.reduce(np.dot, [ic_xx, c_xy, ic_yy, c_yx]))
        w_x = v[:, np.argmax(w)].real
        w_x = w_x / np.sqrt(functools.reduce(np.dot, [w_x.T, c_xx, w_x]))
        
        # calculate w_y
        w, v = np.linalg.eig(functools.reduce(np.dot, [ic_yy, c_yx, ic_xx, c_xy]))
        w_y = v[:, np.argmax(w)].real
        w_y = w_y / np.sqrt(functools.reduce(np.dot, [w_y.T, c_yy, w_y]))
        
        # calculate rho
        rho = abs(functools.reduce(np.dot, [w_x.T, c_xy, w_y]))
        return rho, w_x, w_y, x, y
    
    

    def iCanClean_sgl(self, data_X, subject, noise_channel=4, threshold = 0.8):
        r"""
        Function to run iCanClean algorithm on 1 subject
        Input:
            data_X: type np.ndarry of shape (subject, trial, samples, channels)
            subject: type int
            # trials: type list where trials[0] is of type int. List of trials to extract data from
            noise_channel: type int. Denote noise channels
            threshold: type float. Threshold to denote noise channel correlation to eeg is sufficient to be subtraction
        Return
            output: type np.ndarry of shape (trial, samples, channels), where
                output.shape[0] = len(trial), 
                output.shape[1] = data_X.shape[2],
                output.shape[2] = data_X.shape[3]

        """
        # Extract relevant data
        samples = np.arange(data_X.shape[2])
#         subj_ix = np.array([subject])
        subj_ix = np.arange(data_X.shape[0])
        # trials_ix = np.array(trials)
        samples_ix =  np.array(samples)
        eeg_ix = np.array(data_X.shape[3])

        # dat_x = data_X[np.ix_(subj_ix, trials_ix, samples_ix, eeg_ix)][subject,:,:,:] # Shape (trial, samples, eeg_channels)
        dat_x = data_X[subject, :,:,:]
        dat_y = data_X[subject, :, :, noise_channel]  # Shape (trial, samples)
        dat_y = np.expand_dims(dat_y, axis = 2)  # Shape (trial, samples, 1)

        # Zeros array of output
        output = np.zeros((data_X.shape[1], data_X.shape[2], data_X.shape[3]))

        # Get CCA output
        for trial in range(data_X.shape[1]):
    #         for _, channel in enumerate(eeg_channels):
            rho, w_x, w_y, Xmc, Ymc = self.calculate_cca(dat_x[trial, :, :], dat_y[trial], 0)

            V = Ymc @ np.expand_dims(w_y, axis=1)
            U  = Xmc @ np.expand_dims(w_x, axis=1)

            bad_comp_list = np.where(rho >= threshold)
#             bad_comp_list = np.where(True)
            bad_comp_activity = U[:,bad_comp_list[0]]

            ProjectionMatrix = np.linalg.lstsq(bad_comp_activity, Xmc)
            ProjectedNoise = bad_comp_activity * ProjectionMatrix[0]
#             print(ProjectedNoise.shape)
#             print(dat_x[trial, :, :].shape)

            Xclean = dat_x[trial, :, :] - ProjectedNoise
#             print(Xclean.shape)

            # Write to output
            output[trial, :, :] = Xclean
#             print('Updated subject {}, trial {} in sgl'.format(subject, trial))

        return output
    
    
    
    def iCanClean(self, data_X, subject=None, trials=None, noise_channel=3, threshold=0.8):
        r"""
        Function to run iCanClean algorithm on the entire dataset. Function iteratively calls iCanClean_sgl for each subject.
        Argument:
            data_X: type np.ndarry of shape (subject, trial, samples, channels)
            subject: type list to defined which subjects to use. If None, use all subjects
            trials: type list where trials[0] is of type int. List of trials to extract data from. If None, use all trials.
            noise_channel: type int. Denote noise channels
            threshold: type float. Threshold to denote noise channel correlation to eeg is sufficient to be subtraction
        Return:
            output: type np.ndarray of shape (subject, trial, samples, channels), which is cleaned. 
            All channels are returned with cleaned data. I.e. output.shape = data_X.shape.
        """
        if subject is None:
            subj_lst = np.arange(data_X.shape[0])
        else:
            subj_lst = subject
        
        if trials is None:
            trial_lst = np.arange(data_X.shape[1])
        else:
            trial_lst = trials
            
        # Create zeros numpy ndarray to store the data
        output = np.zeros((len(subj_lst), len(trial_lst), data_X.shape[2], data_X.shape[3]))
        
        # Iteratively calls iCanClean_sgl on each subject
        for i in subj_lst:
            temp = self.iCanClean_sgl(data_X, i, noise_channel, threshold)
#             print(temp.shape)
            temp = np.expand_dims(temp, axis=0)
            output[i] = temp
        
        print('Completed iCanClean algorithm cleaning. Input shape = {}, Output shape = {}'.format(data_X.shape, output.shape))

        return output
            
        