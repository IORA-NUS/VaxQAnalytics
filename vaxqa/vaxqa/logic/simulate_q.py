import math

class SimulateQ:

    def run(N,s1,s2,s3,k1,k2,k3):
        As = N/840
        mu1 =  1/s1
        mu2 = 1/s2
        mu3 = 1/s3
        rho1 = As/(k1*mu1)
        rho2 = As/(k2*mu2)
        rho3 = As/(k3*mu3)

        if rho1 >= 1:
            return (N,s1,s2,s3,k1,k2,k3,'nan','nan','nan','nan')
        if rho2 >= 1:
            return (N,s1,s2,s3,k1,k2,k3,'nan','nan','nan','nan')
        if rho3 >= 1:
            return (N,s1,s2,s3,k1,k2,k3,'nan','nan','nan','nan')

        #Compute W1,
        One_over_P0 = pow(k1*rho1,k1)/((1-rho1)*math.factorial(k1))
        for m in range(k1):
            One_over_P0 += pow(k1*rho1,m)/(math.factorial(m))
        P0 = 1/One_over_P0
        L1 = P0*rho1*pow(k1*rho1,k1)/(math.factorial(k1)*pow(1-rho1,2))
        W1 = L1 / As

        #Compute W2,
        One_over_P0 = pow(k2*rho2,k2)/((1-rho2)*math.factorial(k2))
        for m in range(k2):
            One_over_P0 += pow(k2*rho2,m)/(math.factorial(m))
        P0 = 1/One_over_P0
        L2 = P0*rho2*pow(k2*rho2,k2)/(math.factorial(k2)*pow(1-rho2,2))
        W2 = L2 / As

        #Compute W3,
        P3_num = k3*pow(As,k3) / (pow(mu3,k3-1)*(k3*mu3-As)*math.factorial(k3))

        P3_denom = P3_num
        for m in range(k3):
            P3_denom += pow(As,m)/(pow(mu3,m)*math.factorial(m))


        P3 = P3_num / P3_denom
        W3 = (s3/k3+1)*P3/(1-rho3)
        L3 = W3*As

        return (N,s1,s2,s3,k1,k2,k3,W1,W2,W3,L3)
