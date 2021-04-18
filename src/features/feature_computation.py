import numpy as np
import librosa
import essentia
import essentia.standard as es

class Feature():
    def __init__(self, file_name, signal, win_length, hop_length, sr, features):
        self.file_name = file_name
        self.signal = signal
        self.win_length = win_length
        self.hop_length = hop_length
        self.sr = sr
        self.features = features
        self.methods = {    
            "sp_ce": 'spectral_centroid',
            "sp_co": 'spectral_contrast',
            "sp_ro": 'spectral_rolloff',
            "zcr": 'zero_crossing_rate',
            "mfcc": 'mfcc',
            "chroma": 'chroma',
            "bpm": 'bpm',
            "rms": 'rms',
            "onset_rate": "onset_rate",
            "flux": "flux",
            "hfc": "hfc"
        }
    
    def create_column_list(self, name, size):
        if size>1:
            return [name + str(i).zfill(2) if len(str(i))<2 else name + str(i) for i in range(1, size+1)]
        else:
            return [name]
    
    def mean_var(self, feature_vals):
        mean_vals = np.mean(feature_vals, axis=1)
        var_vals = np.var(feature_vals, axis=1)
        return mean_vals, var_vals

    def save_feature(self, aggr_feature_vals, feature_name, n=1):
        col_names = self.create_column_list(feature_name, n)
        
        for i, vals in enumerate(aggr_feature_vals):
            self.features[col_names[i]][self.file_name] = vals

    def feature_processing(self, feature_vals, feature_name, n=1, fo=True):
        # Take mean and variance and save
        mean_vals, var_vals = self.mean_var(feature_vals)
        self.save_feature(mean_vals, 'mean_' + feature_name, n)
        self.save_feature(var_vals, 'var_' + feature_name, n)

        # Take first-order difference mean and variance and save
        if fo:
            mean_vals, var_vals = self.mean_var(np.diff(feature_vals, axis=1))
            self.save_feature(mean_vals, 'mean_fo_' + feature_name, n)
            self.save_feature(var_vals, 'var_fo_' + feature_name, n)
            
    def spectral_centroid(self):
        print("Computing Spectral Centroid")
        spce = librosa.feature.spectral_centroid(self.signal, sr=self.sr, n_fft=self.win_length, hop_length=self.hop_length)
        self.feature_processing(spce, 'spce')

    def spectral_contrast(self, nbands):
        print("Computing Spectral Contrast")
        spco = librosa.feature.spectral_contrast(self.signal, sr=self.sr, n_fft=self.win_length, n_bands=nbands, hop_length=self.hop_length)
        self.feature_processing(spco, 'spco', nbands+1)

    def spectral_rolloff(self):
        print("Computing Spectral Rolloff")
        spro = librosa.feature.spectral_rolloff(self.signal, sr=self.sr, n_fft=self.win_length, hop_length=self.hop_length)
        self.feature_processing(spro, 'spro')

    def zero_crossing_rate(self):
        print("Computing Zero Crossing Rate")
        zcr = librosa.feature.zero_crossing_rate(self.signal, frame_length=self.win_length)
        self.feature_processing(zcr, 'zcr')

    def mfcc(self, nmfcc):
        print("Computing MFCC")
        mfcc = librosa.feature.mfcc(self.signal, sr=self.sr, n_mfcc=nmfcc, win_length=self.win_length, hop_length=self.hop_length)
        self.feature_processing(mfcc, 'mfcc', nmfcc)
    
    def chroma(self, nchroma):
        print("Computing Chroma")
        chroma = librosa.feature.chroma_cens(self.signal, sr=self.sr, n_chroma=nchroma)
        self.feature_processing(chroma, 'chroma', nchroma)

    # Essentia features
    def bpm(self):
        print("Computing BPM")
        rhythm_extractor = es.RhythmExtractor2013()
        bpm, _, _, _, _ = rhythm_extractor(self.signal)
        self.save_feature([bpm], 'bpm')
    
    def rms(self):
        print("Computing RMS")
        rms_calculator = es.RMS()
        rms = rms_calculator(self.signal)
        self.save_feature([rms], 'rms')
        
    def onset_rate(self):
        print("Computing Onset Rate")
        onset_rate_calculator = es.OnsetRate()
        _, onset_rate = onset_rate_calculator(self.signal)
        self.save_feature([onset_rate], 'onset_rate')

    def flux(self):
        print("Computing spectral flux")
        w = es.Windowing(type = 'hann')
        spectrum_calculator = es.Spectrum()
        flux_calculator = es.Flux()
        spectral_flux = []
        for frame in es.FrameGenerator(self.signal, frameSize=self.win_length, hopSize=self.hop_length):
            freq_bins = spectrum_calculator(w(frame))
            flux_n = flux_calculator(freq_bins)
            spectral_flux.append(flux_n)
        self.feature_processing(np.asarray(spectral_flux).reshape(1, -1), 'spflux', fo=False)

    def hfc(self):
        print("Computing High Frequency Content")

        # Compute spectrum
        w = es.Windowing(type = 'hann')
        spectrum_calculator = es.Spectrum()
        hfc_calculator = es.HFC()
        hfc = []
        for frame in es.FrameGenerator(self.signal, frameSize=self.win_length, hopSize=self.hop_length):
            freq_bins = spectrum_calculator(w(frame))
            hfc_n = hfc_calculator(freq_bins)
            hfc.append(hfc_n)
        self.feature_processing(np.asarray(hfc).reshape(1, -1), 'hfc', fo=False)

    def call_function(self, func_name, **args):
        return getattr(self, self.methods[func_name])(**args)