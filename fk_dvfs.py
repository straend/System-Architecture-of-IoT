import math
# Calculate the Extension Factor
def fk_eFactor(times, slack):
    return (sum(times) + slack ) / sum(times)

# Calculates V0 for given Vmax and Vt
def fk_V0(Vmax, Vt):
    return math.pow(Vmax-Vt,2) / Vmax

# Calculates a new VDD for a processor
def fk_Vdd(Vt, Vmax, eFactor, V0):
    tmp_1 = Vt
    tmp_2 = V0 / (2*eFactor)
    tmp_3 = math.sqrt( math.pow(Vt + (V0/(2*eFactor)),2) - math.pow(Vt,2))
    
    return tmp_1 + tmp_2 + tmp_3

# Calculate vdd from Vt, Vmax, times and slack
def fk_getVdd(Vt, Vmax, times, slack):
    e = fk_eFactor(times, slack)
    V0 = fk_V0(Vmax, Vt)
    Vdd = fk_Vdd(Vt, Vmax, e, V0)
    return Vdd

def fk_PVdd(oldP, eFactor, oldV, newV):
    return (oldP * 1/eFactor * math.pow(newV,2)/math.pow(oldV,2) )

def fk_egrad(Texe, Et, dT):
        return (Et*Texe) - (Et*(Texe + dT))

# Calculates an energy gradient for each task
# assings new voltage, power, timing, energy consumption
# to the task that benefits most
def fk_eg(delta_t, tasks):
    for a in tasks:
        t=tasks[a]
        
        eF =(t['time']+delta_t)/ t['time']
        nTime = t['time']+delta_t
        newVdd = fk_getVdd(t['Vtresh'], t['Vmax'], [t['time']], delta_t)

        oldE = t['p']* t['time']
        newP = fk_PVdd(t['p'], eF, t['Vmax'], newVdd )

        newE = newP * nTime
        energy_grad = oldE - newE

        tasks[a]['n'] = {'p': newP, 'Vmax': newVdd, 'time': nTime}
        tasks[a]['eg']= energy_grad
        
 
    # Get the maximum energy gradient
    max_in = max(tasks, key=lambda k: tasks[k]['eg'])
    
    # Copy task that we will get 
    nt = tasks[max_in]['n']
    tasks[max_in]['p']=nt['p']
    tasks[max_in]['Vmax']=nt['Vmax']
    tasks[max_in]['time']=nt['time']
    for t in tasks:
        del(tasks[t]['n'])
    return tasks
