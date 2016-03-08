import os.path
import scipy.io
import pandas as pd
import numpy as np

def load_data(fileroot, day=0, epoch=0, tetrode=0, datatype='eeg', version='old'):
    anim_prefix = os.path.split(os.path.normpath(fileroot))[1].lower();
    filename = "{}{}{:02d}.mat".format(anim_prefix, datatype, day)
    if (datatype=='eeg') :
        filename = "{}eeg{:02d}-{}-{:02d}.mat".format(anim_prefix, day, epoch, tetrode)
        print("Loading " + filename)
        mat = scipy.io.loadmat(os.path.join(fileroot,'EEG',filename), 
                               struct_as_record=False, squeeze_me=True)
        data = mat[datatype]
        if (version=='new'):
          if (day > 1):
            data = data[day-1]
          if (epoch > 1):
            data = data[epoch-1]
          if (tetrode > 1):
            data = data[tetrode-1]
        return data
    elif (datatype=='tetinfo') :
        filename = "{}{}.mat".format(anim_prefix, datatype)
        print("Loading " + filename)
        mat = scipy.io.loadmat(os.path.join(fileroot,filename), 
                               struct_as_record=False, squeeze_me=True)
        data = mat[datatype]
        tetinfo = {}
        idx_columns = ['Day', 'Epoch', 'Tetrode']
        for dayidx, da in enumerate(data) :
            for epidx, ep in enumerate(da):
                for tetidx, te in enumerate(ep):
                  #if isinstance(te, np.ndarray) :
                      tetrode_idx = (dayidx, epidx, tetidx)
                      df = dict(zip(idx_columns,list(tetrode_idx)))
                      if (isinstance(te, np.ndarray)) :
                          tetinfo[str(tetrode_idx)] = df                        
                          continue # No data for this tetrode/cell combo
                      ti = {f: getattr(te,f) for f in te._fieldnames}
                      df.update(ti)
                      tetinfo[str(tetrode_idx)] = df                        
        tetinfodf = pd.DataFrame.from_dict(tetinfo,orient='index')
        return tetinfodf, data
    elif (datatype=='cellinfo') :
        print("Loading " + filename)
        filename = "{}{}.mat".format(anim_prefix, datatype)
        mat = scipy.io.loadmat(os.path.join(fileroot,filename), 
                               struct_as_record=False, squeeze_me=True)
        data = mat[datatype]
        cellinfo = {}
        idx_columns = ['Day', 'Epoch', 'Tetrode','Cell']
        for dayidx, da in enumerate(data) :
            for epidx, ep in enumerate(da):
                for tetidx, te in enumerate(ep):
                    if isinstance(te, np.ndarray) :
                        for cellidx, cell in enumerate(te):
                            neuron_idx = (dayidx, epidx, tetidx, cellidx)
                            df = dict(zip(idx_columns,list(neuron_idx)))
                            if (isinstance(cell, np.ndarray)) :
                                cellinfo[str(neuron_idx)] = df                        
                                continue # No data for this tetrode/cell combo
                            ci = {f: getattr(cell,f) for f in cell._fieldnames}
                            df.update(ci)
                            cellinfo[str(neuron_idx)] = df                        
                    else: # Single cell on tetrode
                        neuron_idx = (dayidx, epidx, tetidx, 0)
                        ci = {f: getattr(te,f) for f in te._fieldnames}
                        df = dict(zip(idx_columns,list(neuron_idx)))
                        df.update(ci)
                        cellinfo[str(neuron_idx)] = df                        
        cellinfodf = pd.DataFrame.from_dict(cellinfo,orient='index')
        return cellinfodf, data
    elif (datatype=='task') :
        filename = "{}{}{:02d}.mat".format(anim_prefix, datatype, day)
        print("Loading " + filename)
        mat = scipy.io.loadmat(os.path.join(fileroot,filename), 
                               struct_as_record=False, squeeze_me=True)
        data = mat[datatype]
        return data
    elif (datatype=='spikes') :
        print("Loading " + filename)
        mat = scipy.io.loadmat(os.path.join(fileroot,filename), 
                               struct_as_record=False, squeeze_me=True)

        spikedata = {}
        # Spike files contain data for all epochs, tetrodes, and cells in a day
        # Some epochs have fields: ['data', 'descript', 'fields', 'depth', 'spikewidth', 'timerange']
        # but some epochs are missing 'spikewidth'
        data = mat[datatype]
        data = data[day-1]
        for epidx, da in enumerate(data):
            for tetidx, te in enumerate(da):
                if isinstance(te, np.ndarray) :
                    for cellidx, cell in enumerate(te):
                        neuron_idx = (day-1, epidx, tetidx, cellidx)
                        if (isinstance(cell, np.ndarray)) :
                            continue # No data for this tetrode/cell combo
                        spikedata[str(neuron_idx)] = {f: getattr(cell,f) for f in cell._fieldnames}
                else: # Single cell on tetrode
                    neuron_idx = (day-1, epidx, tetidx, 0)
                    spikedata[str(neuron_idx)] = {f: getattr(te,f) for f in te._fieldnames}
        return spikedata
    elif (datatype=='pos') :
        print("Loading " + filename)
        mat = scipy.io.loadmat(os.path.join(fileroot,filename), 
                               struct_as_record=False, squeeze_me=True)
        data = mat[datatype]
        return data
    elif (datatype=='rawpos') :
        x=0
    else :
        raise ValueError('datatype is not handled')


