import torch

## NEED TO BUILT GET_OBS_HONEYCOMB
def get_obs_honeycomb(A1symm, A2symm, H, Sx, Sy, Sz, C, Ea, Eb):
    # A(phy,u,l,d,r), C(d,r), E(u,r,d)
    
    d = 2
    # Da = Asymm.size()
    Da = A1symm.size()
    D = Da[1]
    # Td = torch.einsum('mefgh,nabcd->eafbgchdmn',(Asymm,Asymm)).contiguous().view(Da[1]**2, Da[2]**2, Da[3]**2, Da[4]**2, Da[0], Da[0])
    #print( torch.dist( Td, Td.permute(0,3,2,1,4,5) ) )    # test left-right reflection symmetry of Td
    Tda = torch.einsum('mefg,nabc->eafbgcmn',(A1symm,A1symm)).contiguous().view(D**2, D**2, D**2, d, d)
    Tdb = torch.einsum('mefg,nabc->eafbgcmn',(A2symm,A2symm)).contiguous().view(D**2, D**2, D**2, d, d)
    
    Ta = (A1symm.view(d, -1).t()@A1symm.view(d, -1)).contiguous().view(D, D, D, D, D, D)
    Ta = Ta.permute(0, 3, 1, 4, 2, 5).contiguous().view(D**2, D**2, D**2)
    Ta = Ta/Ta.norm()

    Tb = (A2symm.view(d, -1).t()@A2symm.view(d, -1)).contiguous().view(D, D, D, D, D, D)
    Tb = Tb.permute(0, 3, 1, 4, 2, 5).contiguous().view(D**2, D**2, D**2)
    Tb = Tb/Tb.norm()


    Cprime = torch.tensordot(C, Ea, ([1],[0]))   # C(ef)*Ea(fga)=Cprime(ega)
    Cprime = torch.tensordot(Eb, Cprime, ([2],[0])) # Eb(ije)*Cprime(ega)=Cprime(ijga)
    TaTb = torch.tensordot(Ta, Tb, ([2],[0])) # Ta(jkl)*Tb(lpg) = Tab(jkpg)
    Cprime = torch.tensordot(Cprime,TaTb, ([1,2],[0,3])) # Cprime(ijga)*Tab(jkpg) = Cprime(i,a,k,p)
    Cprime = Cprime.permute(0,2,1,3) # Cprime(i,k,a,p)

    Cdprime = torch.tensordot(C, Ea, ([1],[0]))   # C(ef)*Ea(fga) = Rho(ega)
    Cdprime = torch.tensordot(Eb, Cdprime, ([2],[0])) # Eb(ije)*Rgo(ega) = Rho(ijga)
    TaTb = torch.tensordot(Tda, Tdb, ([2],[0])) # Ta(jkl,d1,d1')*Tb(lpg,d2,d2') = Tab(jk,d1,d1',pg,d2,d2')
    TaTb = TaTb.permute(0,1,4,5,2,3,6,7) # Tab(jk,pg,d1,d1',d2,d2')  
    Cdprime = torch.tensordot(Cdprime,TaTb, ([1,2],[0,3])) # Rho(ijga)*Tab(jkpg,d1,d1',d2,d2') = Rho(iakp,d1,d1',d2,d2')
    Cdprime = Cdprime.permute(0,2,1,3,4,5,6,7) # Cprime(i,k,a,p,d1,d1',d2,d2')

    C2prime = torch.tensordot(Cprime, Cprime, ([2,3],[0,1])) # Cprime(i,k,a,p)*Cprime(a,p,l,m) = C2prime(i,k,l,m) ok
    Rho = torch.tensordot(C2prime, Cdprime, ([0,1,2,3],[2,3,0,1])) 
    # C2prime(i,k,l,m)*Cdprime(l,m,i,k,d1,d1',d2,d2') = Rho(d1,d1',d2,d2') ok
    Rho = Rho.permute(0,2,1,3) # Rho(d1,d2,d1',d2') ok
    Rho = Rho.contiguous().view(d**2,d**2)
    
    # Rho is the two sites density matrix

    Rho = 0.5*(Rho + Rho.t())

    Tnorm = Rho.trace()
    Energy = torch.mm(Rho,H).trace()/Tnorm
    Mx = torch.mm(Rho,Sx).trace()/Tnorm
    My = torch.mm(Rho,Sy).trace()/Tnorm
    Mz = torch.mm(Rho,Sz).trace()/Tnorm
   
    #print("Tnorm = %g, Energy = %g " % (Tnorm.item(), Energy.item()) )

    return Energy, Mx, My, Mz
