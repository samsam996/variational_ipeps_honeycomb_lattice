



### Variational optimization of iPEPS with the C3 honeycomb CTMRG

This code is an adaptation of https://github.com/wangleiphy/tensorgrad/blob/master/README.md to the honeycomb lattice, using the honeycomb CTMRG rather then the square CTMRG.

Run this to optimize an iPEPS wave function for 2D quantum Heisenberg model. 
 
Installation using conda:

```bash
conda create --name var_ipeps python=3.8
conda activate var_ipeps
pip install -r variational_iPEPS/requirements.txt
```

To use the program_
```bash
python variational_iPEPS/variational.py -D 3 -chi 30 
```

Finally, delete the conda environment using
```bash
conda remove --name var_ipeps --all
```


