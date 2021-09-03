import math

def simulateQApprox(N,s1,s2,s3,k1,k2,k3, ptile='Avg'):
    # print(N,s1,s2,s3,k1,k2,k3, ptile)
    As = N/840
    mu1 =  1/s1
    mu2 = 1/s2
    mu3 = 1/s3
    rho1 = As/(k1*mu1)
    rho2 = As/(k2*mu2)
    rho3 = As/(k3*mu3)
    T = 30
    # print(rho1, rho2, rho3)

    if rho1 >= 1:
        return (N,s1,s2,s3,k1,k2,k3,'NA','NA','NA','NA')
    if rho2 >= 1:
        return (N,s1,s2,s3,k1,k2,k3,'NA','NA','NA','NA')
    if rho3 >= 1:
        return (N,s1,s2,s3,k1,k2,k3,'NA','NA','NA','NA')

    #Compute W1,
    One_over_P0 = pow(k1*rho1,k1)/((1-rho1)*(math.sqrt(2*math.pi*k1)*(k1/math.e)**k1))
    for m in range(1,k1):
        One_over_P0 += pow(k1*rho1,m)/(math.sqrt(2*math.pi*m)*(m/math.e)**m)
    P0 = 1/One_over_P0
    L1 = P0*rho1*pow(k1*rho1,k1)/((math.sqrt(2*math.pi*k1)*(k1/math.e)**k1)*pow(1-rho1,2))
    W1 = L1 / As

    #Compute W2,
    One_over_P0 = pow(k2*rho2,k2)/((1-rho2)*(math.sqrt(2*math.pi*k2)*(k2/math.e)**k2))
    for m in range(1,k2):
        One_over_P0 += pow(k2*rho2,m)/(math.sqrt(2*math.pi*m)*(m/math.e)**m)
    P0 = 1/One_over_P0
    L2 = P0*rho2*pow(k2*rho2,k2)/(((math.sqrt(2*math.pi*k2)*(k2/math.e)**k2))*pow(1-rho2,2))
    W2 = L2 / As

    #Compute W3,
    try:
        P3_num = k3*pow(As,k3) / (pow(mu3,k3-1)*(k3*mu3-As)*((math.sqrt(2*math.pi*k3)*(k3/math.e)**k3)))

        P3_denom = P3_num
        for m in range(1,k3):
            P3_denom += pow(As,m)/(pow(mu3,m)*(math.sqrt(2*math.pi*m)*(m/math.e)**m))

        P3 = P3_num / P3_denom
        W3 = (s3/k3+1)*P3/(1-rho3)
        L3 = W3*As

    except:
        if (k3 - (As*T)) >= 0:
            W3 = 0
            L3 = -1
        else:
            W3 = -1
            L3 = 0


    # If this is a constant multiplier, can we have a table for different percentiles and compute on the fly?
    W190 = W1*(2.645)
    W195 = W1*(2.960)
    W290 = W2*(2.645)
    W295 = W2*(2.960)
    W390 = W3*(2.645)
    W395 = W3*(2.960)
    L390 = L3*(2.645)
    L395 = L3*(2.960)

    W1s = math.ceil(W1*60)
    W2s = math.ceil(W2*60)
    W3s = math.ceil(W3*60)
    W190s = math.ceil(W190*60)
    W290s = math.ceil(W290*60)
    W390s = math.ceil(W390*60)
    W195s = math.ceil(W195*60)
    W295s = math.ceil(W295*60)
    W395s = math.ceil(W395*60)
    # print(L3)
    # L3 = math.ceil(L3)
    L390 =  math.ceil(L390)
    L395 =  math.ceil(L395)

    if ptile == 'Avg':
        return (N,s1,s2,s3,k1,k2,k3,W1s,W2s,W3s,L3)
    elif (ptile == 90) or (ptile == '90'):
        return (N,s1,s2,s3,k1,k2,k3,W190s,W290s,W390s,L390)
    elif (ptile == 95) or (ptile == '95'):
        return (N,s1,s2,s3,k1,k2,k3,W195s,W295s,W395s,L395)



