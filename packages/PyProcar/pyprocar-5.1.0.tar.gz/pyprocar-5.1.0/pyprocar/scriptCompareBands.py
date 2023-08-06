from .utilsprocar import UtilsProcar
from .procarparser import ProcarParser
from .procarselect import ProcarSelect
from .procarplotcompare import ProcarPlotCompare
from .elkparser import ElkParser 
from .splash import welcome
import numpy as np
import matplotlib.pyplot as plt
import re





def bandscompare(file=None,file2=None,mode='plain',abinit_output=None,abinit_output2=None,spin='0',spin2='0',
                 atoms=None,atoms2=None,orbitals=None,orbitals2=None,fermi=None,fermi2=None,
                 elimit=None,mask=None,markersize=0.02,markersize2=0.02,cmap='jet',cmap2='hot_r',vmax=None,vmin=None,
                 vmax2=None,vmin2=None,grid=True,marker=',',marker2=',',permissive=False,human=False,
                 savefig=None,kticks=None,knames=None,title=None,outcar=None,outcar2=None,color='r',
                 color2='g',legend='PROCAR1',legend2='PROCAR2',kpointsfile=None,exportplt=False,kdirect=True, discontinuities = None, code='vasp'):
  """
  This module compares two band structures.
  """
  welcome()

  # Turn interactive plotting off
  plt.ioff()

  #First handling the options, to get feedback to the user and check
  #that the input makes sense.
  #It is quite long
  if atoms is None:
    atoms = [-1]
    if human is True:
      print("WARNING: `--human` option given without atoms list!")
      print("--human will be set to False (ignored)\n ")
      human = False
  
  #repeat for 2nd data set
  if atoms2 is None:
    atoms2 = [-1]         
      
  if orbitals is None:
    orbitals = [-1]
  #repeat for 2nd data set  
  if orbitals2 is None:
    orbitals2 = [-1]  
    

  print("Script initiated")
  print("input file 1   : ", file)
  print("input file 2   : ", file2) #2nd file
  print("Mode           : ", mode)
  
  print("spin comp.  #1 : ", spin)
  print("spin comp.  #2 : ", spin2)
  print("atoms list. #1 : ", atoms)
  print("atoms list. #2 : ", atoms2)
  print("orbs. list. #1 : ", orbitals)
  print("orbs. list  #2 : ", orbitals2)

  if fermi is None and outcar is None and abinit_output is None:
    print("WARNING: Fermi Energy not set! Please set manually or provide output file.")
    fermi = 0
    
  if fermi2 is None and outcar2 is None and abinit_output2 is None:
    print("WARNING: Fermi Energy #2 not set! Please set manually or provide output file.")
    fermi2 = 0


###################reading abinit output (added by uthpala) ##########################

  if abinit_output:
  	print("Abinit output used")

  #reading abinit output file
  	rf = open(abinit_output,'r')
  	data = rf.read()
  	rf.close()

  	fermi = float(re.findall('Fermi\w*.\(\w*.HOMO\)\s*\w*\s*\(\w*\)\s*\=\s*([0-9.+-]*)',data)[0])
   
   
  if abinit_output2:
  	print("Abinit output #2 used")

  #reading abinit output file
  	rf2 = open(abinit_output2,'r')
  	data2 = rf2.read()
  	rf2.close()

  	fermi2 = float(re.findall('Fermi\w*.\(\w*.HOMO\)\s*\w*\s*\(\w*\)\s*\=\s*([0-9.+-]*)',data2)[0])


####################################################################  

 
  print("Fermi Energy #1  : ", fermi)
  print("Fermi Energy #2  : ", fermi2)
  print("Energy range    : ", elimit)

  if mask is not None:
    print("masking thres.: ", mask) 
    
  print("Colormap #1        : ", cmap)
  print("Colormap #2        : ", cmap2)
  print("MarkerSize #1   : ", markersize)
  print("MarkerSize #2   : ", markersize2)
    
  print("Permissive      : ", permissive)
  if permissive:
    print("INFO: Permissive flag is on! Be careful")
  print("vmax            : ", vmax)
  print("vmin            : ", vmin)
  print("vmax #2         : ", vmax2)
  print("vmin #2         : ", vmin2)
  print("grid enabled    : ", grid) 
  if human is not None:
    print("human          : ", human)
  print("Savefig         : ", savefig)
  print("kticks          : ", kticks)
  if kpointsfile is None:
    print("kticks        : ", kticks)
    print("knames        : ", knames)
    if discontinuities:
        print("discontinuities :",discontinuities)
  print("title         : ", title)

  print("outcar #1       : ", outcar)
  print("outcar #2       : ", outcar2)
  
  print("legend #1       : ",legend)
  print("legend #2       : ",legend2)

  if kdirect:
    print("k-points  are in reduced coordinates")
  else:
    print("k-points  are in cartesian coordinates. Remember to supply an output file for this case to work.")

  #### READING KPOINTS FILE IF PRESENT ####

  #If KPOINTS file is given:
  if kpointsfile is not None:
    #Getting the high symmetry point names from KPOINTS file
    f = open(kpointsfile)
    KPread = f.read()
    f.close()

    KPmatrix = re.findall('reciprocal[\s\S]*',KPread)
    tick_labels = np.array(re.findall('!\s(.*)',KPmatrix[0]))
    knames=[]
    knames=[tick_labels[0]]    
   
    ################## Checking for discontinuities ########################
    discont_indx=[]
    icounter = 1
    while icounter<len(tick_labels)-1:
        if tick_labels[icounter] == tick_labels[icounter+1]:
            knames.append(tick_labels[icounter])
            icounter = icounter + 2
        else:
            discont_indx.append(icounter)
            knames.append(tick_labels[icounter]+'/'+tick_labels[icounter+1])
            icounter = icounter + 2
    knames.append(tick_labels[-1])                    
    discont_indx = list(dict.fromkeys(discont_indx))
    
    ################# End of discontinuity check ##########################
                  
    # Added by Nicholas Pike to modify the output of seekpath to allow for 
    # latex rendering.
    for i in range(len(knames)):
        if knames[i] =='GAMMA':
            knames[i] = '\Gamma'
        else:
            pass
            
    knames = [str("$"+latx+"$") for latx in knames] 

    #getting the number of grid points from the KPOINTS file
    f2 = open(kpointsfile)
    KPreadlines = f2.readlines()
    f2.close()
    numgridpoints = int(KPreadlines[1].split()[0])

    kticks=[0]
    gridpoint=0
    for kt in range(len(knames)-1):
      gridpoint=gridpoint+numgridpoints
      kticks.append(gridpoint-1)
      
    print("knames        : ", knames)
    print("kticks        : ", kticks)     
    
    # creating an array for discontunuity k-points. These are the indexes 
    # of the discontinuity k-points.
    discontinuities = []  
    for k in discont_indx:
        discontinuities.append( kticks[int(k/2)+1]  )  
    if discontinuities:
        print("discontinuities :",discontinuities)  
        
  #### END OF KPOINTS FILE DEPENDENT SECTION ####  

 
  #The spin argument should be a number (index of an array), or
  #'st'. In the last case it will be handled separately (later)

  spin = {'0':0, '1':1, '2':2, '3':3, 'st':'st'}[str(spin)]
  spin2 = {'0':0, '1':1, '2':2, '3':3, 'st':'st'}[str(spin2)]

  # parsing the PROCAR file
  if code == 'vasp' or code=='abinit':
      procarFile = ProcarParser()
      procarFile2 = ProcarParser()
  elif code == 'elk':
      procarFile = ElkParser(kdirect=kdirect)
      
      # Retrieving knames and kticks from Elk
      if kticks is None and knames is None:
          if procarFile.kticks and procarFile.knames:
              kticks = procarFile.kticks
              knames = procarFile.knames
      
  #If ticks and names are given by the user manually:
  if kticks is not None and knames is not None:
    ticks = list(zip(kticks,knames))
  elif kticks is not None:
    ticks = list(zip(kticks,kticks))
  else:
    ticks = None 


  #The second part of this function is parse/select/use the data in
  #OUTCAR (if given) and PROCAR

  #first parse the outcar if given, to get Efermi and Reciprocal lattice
  recLat = None 
  recLat2 = None
 
  if code == 'vasp':
    if outcar and outcar2:
      outcarparser = UtilsProcar()
      if fermi is None:
        fermi = outcarparser.FermiOutcar(outcar)
        print("Fermi energy found in outcar file = " + str(fermi))
      if fermi2 is None:  
        fermi2 = outcarparser.FermiOutcar(outcar2)
        print("Fermi energy #2 found in outcar file = " + str(fermi2))
      
      recLat = outcarparser.RecLatOutcar(outcar)
      recLat2 = outcarparser.RecLatOutcar(outcar2)

  elif code =='elk':
    if fermi is None:
      fermi = procarFile.fermi
      print("Fermi energy found in Elk output file = " + str(fermi))

  elif code=='abinit':    
    if fermi is None:
      rf = open(abinit_output,'r')
      data = rf.read()
      rf.close()
      fermi = float(re.findall('Fermi\w*.\(\w*.HOMO\)\s*\w*\s*\(\w*\)\s*\=\s*([0-9.+-]*)',data)[0])  
      print("Fermi energy found in Abinit output file = " + str(fermi))
             

  # if kdirect = False, then the k-points will be in cartesian coordinates. 
  # The outcar should be read to find the reciprocal lattice vectors to transform from direct to cartecian
  if code=='vasp' or code=='abinit':
      if kdirect:        
        procarFile.readFile(file, permissive)
        procarFile2.readFile(file2, permissive)

      else:    
        procarFile.readFile(file, permissive, recLattice=recLat)
        procarFile2.readFile(file2, permissive,recLattice=recLat2)

  # processing the data, getting an instance of the class that reduces the data
  data = ProcarSelect(procarFile, deepCopy=True)
  data2 = ProcarSelect(procarFile2,deepCopy=True)
  
  #handling the spin, `spin='st'` is not straightforward, needs
  #to calculate the k vector and its normal. Other `spin` values
  #are trivial.
  if spin is 'st':
    #two `ProcarSelect` instances, to store temporal values: spin_x, spin_y
    dataX = ProcarSelect(procarFile, deepCopy=True)
    dataX.selectIspin([1])
    dataX.selectAtoms(atoms, fortran=human)
    dataX.selectOrbital(orbitals)  
    dataY = ProcarSelect(procarFile, deepCopy=True)
    dataY.selectIspin([2])
    dataY.selectAtoms(atoms, fortran=human)
    dataY.selectOrbital(orbitals)
    #getting the signed angle of each K-vector
    angle = np.arctan2(dataX.kpoints[:,1], (dataX.kpoints[:,0]+0.000000001))
    sin = np.sin(angle)
    cos = np.cos(angle)
    sin.shape = (sin.shape[0],1)
    cos.shape = (cos.shape[0],1)
    ##print sin, cos
    #storing the spin projection into the original array
    data.spd = -sin*dataX.spd + cos*dataY.spd
  else:
    data.selectIspin([spin])
    data.selectAtoms(atoms, fortran=human)
    data.selectOrbital(orbitals)
    
  #repeat for dataset #2

  if spin2 is 'st':
    #two `ProcarSelect` instances, to store temporal values: spin_x, spin_y
    dataX2 = ProcarSelect(procarFile2, deepCopy=True)
    dataX2.selectIspin([1])
    dataX2.selectAtoms(atoms2, fortran=human)
    dataX2.selectOrbital(orbitals2)  
    dataY2 = ProcarSelect(procarFile2, deepCopy=True)
    dataY2.selectIspin([2])
    dataY2.selectAtoms(atoms2, fortran=human)
    dataY2.selectOrbital(orbitals2)
    #getting the signed angle of each K-vector
    angle2 = np.arctan2(dataX2.kpoints[:,1], (dataX2.kpoints[:,0]+0.000000001))
    sin2 = np.sin(angle2)
    cos2 = np.cos(angle2)
    sin2.shape = (sin2.shape[0],1)
    cos2.shape = (cos2.shape[0],1)
    ##print sin, cos
    #storing the spin projection into the original array
    data2.spd = -sin2*dataX2.spd + cos2*dataY2.spd
  else:
    data2.selectIspin([spin2])
    data2.selectAtoms(atoms2, fortran=human)
    data2.selectOrbital(orbitals2)  
    
 
  # Plotting the data
  data.bands = (data.bands.transpose() - np.array(fermi)).transpose()    
  # Plotting the data for data #2
  data2.bands = (data2.bands.transpose() - np.array(fermi2)).transpose()
  plot = ProcarPlotCompare(data.bands, data2.bands, data.spd, data2.spd, data.kpoints, data2.kpoints)
  
  
  ###### start of mode dependent options #########

  if mode == "scatter":
    plot.scatterPlot(mask=mask,size=markersize,size2= markersize2, cmap=cmap, cmap2 = cmap2, vmin=vmin, vmax=vmax,vmin2=vmin2, vmax2=vmax2, marker=marker, marker2=marker2,legend1=legend,legend2=legend2, ticks=ticks, discontinuities = discontinuities)
    if fermi is not None:
    	plt.ylabel(r"$E-E_f$ [eV]",fontsize=22)
    else:
    	plt.ylabel(r"Energy [eV]",fontsize=22)
    if elimit is not None:
      plt.ylim(elimit)
#
  if mode == "plain":
    plot.plotBands(size=markersize,size2= markersize2, marker=marker, marker2=marker2,color=color,color2=color2,legend1=legend,legend2=legend2, ticks=ticks, discontinuities = discontinuities)
    if fermi is not None:
    	plt.ylabel(r"$E-E_f$ [eV]",fontsize=22)
    else:
    	plt.ylabel(r"Energy [eV]",fontsize=22)
    if elimit:
      plt.ylim(elimit)
      
  if mode == "parametric":
    plot.parametricPlot(cmap=cmap,cmap2 = cmap2, vmin=vmin, vmax=vmax,vmin2=vmin2, vmax2=vmax2, marker='solid', marker2='solid', legend1=legend,legend2=legend2,ticks=ticks, discontinuities = discontinuities)
    if fermi is not None:
    	plt.ylabel(r"$E-E_f$ [eV]",fontsize=22)
    else:
    	plt.ylabel(r"Energy [eV]",fontsize=22)
    if elimit is not None:
      plt.ylim(elimit)

  elif mode == "atomic":
    plot.atomicPlot(cmap=cmap,cmap2 = cmap2, vmin=vmin, vmax=vmax,vmin2=vmin2, vmax2=vmax2)
    if fermi is not None:
    	plt.ylabel(r"$E-E_f$ [eV]",fontsize=22)
    else:
    	plt.ylabel(r"Energy [eV]",fontsize=22)
    if elimit is not None:
      plt.ylim(elimit)

  ##### end of mode dependent options ###########
  plt.tight_layout()
  if grid:
    plt.grid()
  
  if title:
    plt.title(title,fontsize=22)

  if exportplt:
    return plt 

  else:
    if savefig:
      plt.savefig(savefig,bbox_inches='tight')
      plt.close() #Added by Nicholas Pike to close memory issue of looping and creating many figures 
    else:
      plt.show()
    return 

#if __name__ == "__main__": 
    #bandscompare('./compare/PROCAR','./compare/PROCAR',outcar='./compare/OUTCAR',outcar2='./compare/OUTCAR2',kpointsfile='./compare/KPOINTS',mode='plain',elimit=[-6,6])