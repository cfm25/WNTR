from nose.tools import *
from os.path import abspath, dirname, join
import wntr

testdir = dirname(abspath(str(__file__)))
datadir = join(testdir,'..','..','tests','networks_for_testing')
packdir = join(testdir,'..','..','..')

"""
Compare results to WST impact files using TSG file
121          SETPOINT      100000          0                86400
"""

def test_mass_consumed():
    inp_file = join(datadir,'net_test_18.inp') 
    
    wn = wntr.network.WaterNetworkModel(inp_file)
        
    WQ = wntr.scenario.Waterquality('CHEM', ['121'], 'SETPOINT', 100, 0, 24*3600)
        
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim(WQ)
    
    nzd_junctions = wn.query_node_attribute('base_demand', np.greater, 0, 
                                        node_type=wntr.network.Junction).keys()
    node_results = results.node.loc[:, :, nzd_junctions]

    MC = wntr.metrics.mass_contaminant_consumed(node_results)
    MC_timeseries = MC.sum(axis=1)
    MC_cumsum = MC_timeseries.cumsum()
    MC_cummax = MC_cumsum.cummax()
    #MC_timeseries.to_csv('MC.txt')

    expected = float(39069900000/1000000) # hour 2
    error = abs((MC_cummax[2*3600] - expected)/expected)
    print MC_cummax[2*3600], expected, error
    assert_less(error, 0.05) # 5% error
    
    expected = float(1509440000000/1000000) # hour 12
    error = abs((MC_cummax[12*3600] - expected)/expected)
    print MC_cummax[12*3600], expected, error
    assert_less(error, 0.05) # 5% error
    
def test_volume_consumed():
    inp_file = join(datadir,'net_test_18.inp') 
    
    wn = wntr.network.WaterNetworkModel(inp_file)
        
    WQ = wntr.scenario.Waterquality('CHEM', ['121'], 'SETPOINT', 100, 0, 24*3600)
    
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim(WQ)
    
    nzd_junctions = wn.query_node_attribute('base_demand', np.greater, 0, 
                                        node_type=wntr.network.Junction).keys()
    node_results = results.node.loc[:, :, nzd_junctions]
    
    VC = wntr.metrics.volume_contaminant_consumed(node_results, 0)
    VC_timeseries = VC.sum(axis=1)
    VC_cumsum = VC_timeseries.cumsum()
    VC_timeseries.to_csv('VC.txt')
    
    expected = float(156760/35.3147) # hour 2
    error = abs((VC_cumsum[2*3600] - expected)/expected)
    print VC_cumsum[2*3600], expected, error
    #assert_less(error, 0.05) # 5% error
    
    expected = float(4867920/35.3147) # hour 12
    error = abs((VC_cumsum[12*3600] - expected)/expected)
    print VC_cumsum[12*3600], expected, error
    #assert_less(error, 0.05) # 5% error
    
def test_extent_contaminated():
    inp_file = join(datadir,'net_test_18.inp') 

    wn = wntr.network.WaterNetworkModel(inp_file)
    
    WQ = wntr.scenario.Waterquality('CHEM', ['121'], 'SETPOINT', 100, 0, 24*3600)
    
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim(WQ)
    
    EC = wntr.metrics.extent_contaminant(results.node, results.link, wn, 0)
    EC_timeseries = EC.sum(axis=1)
    EC_cummax = EC_timeseries.cummax()
    EC_timeseries.to_csv('EC.txt')
    
    expected = float(80749.9*0.3048) # hour 2
    error = abs((EC_cummax[2*3600] - expected)/expected)
    print EC_cummax[2*3600], expected, error
    assert_less(error, 0.05) # 5% error
    
    expected = float(135554*0.3048) # hour 12
    error = abs((EC_cummax[12*3600] - expected)/expected)
    print EC_cummax[12*3600], expected, error
    assert_less(error, 0.05) # 5% error
        
if __name__ == '__main__':
    #test_mass_consumed()
    test_volume_consumed()
    #test_extent_contaminated()
